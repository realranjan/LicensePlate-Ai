import os
import torch
import numpy as np
import openvino.runtime as ov
from openvino.tools import mo
from pathlib import Path

# Add YOLOv5 root to sys.path
YOLOV5_ROOT = Path("/app") / "yolov5"
if str(YOLOV5_ROOT) not in os.sys.path:
    os.sys.path.append(str(YOLOV5_ROOT))

from models.common import DetectMultiBackend
from utils.general import check_yaml, check_dataset, LOGGER
from utils.dataloaders import create_dataloader

try:
    import nncf
except ImportError:
    LOGGER.warning("NNCF not installed, INT8 quantization will not be available.")
    nncf = None

def quantize_yolov5_model(weights_path, data_yaml_path, imgsz=(640, 640), output_dir="/app/data/models"):
    weights_path = Path(weights_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    LOGGER.info(f"Starting quantization of {weights_path.name}...")

    # Load PyTorch model
    device = torch.device("cpu") # Quantization should typically be done on CPU
    model = DetectMultiBackend(weights_path, device=device, dnn=False, data=data_yaml_path, fp16=False)
    model.eval()

    # Create dummy input for tracing
    im = torch.zeros(1, 3, *imgsz).to(device)

    # Export to ONNX (prerequisite for OpenVINO)
    onnx_path = output_dir / weights_path.with_suffix(".onnx").name
    torch.onnx.export(
        model,
        im,
        onnx_path,
        verbose=False,
        opset_version=12,
        input_names=["images"],
        output_names=["output"],
        dynamic_axes={"images": {0: "batch", 2: "height", 3: "width"}, "output": {0: "batch", 1: "anchors"}}
    )
    LOGGER.info(f"ONNX model exported to {onnx_path}")

    # Convert ONNX to OpenVINO IR
    ov_model = mo.convert_model(str(onnx_path), model_name=weights_path.stem, framework="onnx", compress_to_fp16=False)
    LOGGER.info(f"OpenVINO IR model converted from ONNX.")

    if nncf:
        LOGGER.info("Starting INT8 quantization with NNCF...")

        def gen_dummy_dataloader(imgsz, batch_size=1):
            # Create a dummy dataloader for quantization calibration
            # In a real scenario, use a representative subset of your training data.
            for _ in range(10): # Generate 10 dummy images for calibration
                dummy_img = np.random.randint(0, 256, (imgsz[0], imgsz[1], 3), dtype=np.uint8)
                dummy_img = np.transpose(dummy_img, (2, 0, 1)) # HWC to CHW
                yield [torch.from_numpy(dummy_img).unsqueeze(0)] # Add batch dim

        def transform_fn(data_item):
            """
            Quantization transform function.
            Extracts and preprocess input data from dataloader item for quantization.
            """
            img = data_item[0].numpy().astype(np.float32)  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            return np.expand_dims(img, 0) if img.ndim == 3 else img

        dummy_ds = gen_dummy_dataloader(imgsz)
        quantization_dataset = nncf.Dataset(dummy_ds, transform_fn)
        ov_model = nncf.quantize(ov_model, quantization_dataset, preset=nncf.QuantizationPreset.MIXED)
        LOGGER.info("INT8 quantization with NNCF completed.")
    else:
        LOGGER.warning("NNCF not available, skipping INT8 quantization.")

    # Save quantized OpenVINO IR model
    quantized_model_path = output_dir / f"{weights_path.stem}_int8_openvino_model"
    ov.serialize(ov_model, str(quantized_model_path / f"{weights_path.stem}.xml"))
    LOGGER.info(f"Quantized OpenVINO model saved to {quantized_model_path}")

    return quantized_model_path / f"{weights_path.stem}.xml"

if __name__ == "__main__":
    YOLOV5_ROOT = Path("/app") / "yolov5" # Ensure YOLOV5_ROOT is set correctly for the script
    original_weights = Path("/app") / "data" / "models" / "yolov5s.pt"
    data_config = YOLOV5_ROOT / "data" / "coco.yaml"
    quantize_yolov5_model(original_weights, data_config)
