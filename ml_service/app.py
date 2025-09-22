import argparse
import io
import torch
from flask import Flask, request, jsonify
from PIL import Image
import sys
from pathlib import Path
import numpy as np # Required for cv2 and numpy operations
import cv2 # Required for OpenCV image processing
import openvino.runtime as ov # Required for OpenVINO inference

# Explicitly set YOLOv5 root for Docker environment for consistent pathing
YOLOV5_ROOT = Path("/app") / "yolov5"

if str(YOLOV5_ROOT) not in sys.path:
    sys.path.append(str(YOLOV5_ROOT))

from models.common import DetectMultiBackend # Keep for metadata (names/stride)
from utils.general import non_max_suppression, scale_boxes, check_img_size
from utils.torch_utils import select_device

app = Flask(__name__)

# Initialize OpenVINO runtime
core = ov.Core()

# Path to the quantized OpenVINO model
QUANTIZED_MODEL_DIR = Path("/app") / "data" / "models" / "yolov5s_int8_openvino_model"
QUANTIZED_MODEL_XML = QUANTIZED_MODEL_DIR / "yolov5s.xml"
QUANTIZED_MODEL_BIN = QUANTIZED_MODEL_DIR / "yolov5s.bin"

# Load and compile the OpenVINO model
try:
    model = core.read_model(QUANTIZED_MODEL_XML)
    compiled_model = core.compile_model(model, "CPU")
    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)
    # Get model info (names, stride, imgsz) if needed from the original PyTorch model or configuration
    # For simplicity, we'll assume constants or extract from a dummy PyTorch model for names
    # In a full conversion, names would be embedded or passed through configuration
    # As a fallback, we can load a dummy PyTorch model to get names
    dummy_pt_model = DetectMultiBackend(Path("/app") / "data" / "models" / "yolov5s.pt", device=torch.device("cpu"), dnn=False, data=YOLOV5_ROOT / "data" / "coco.yaml", fp16=False)
    names = dummy_pt_model.names
    stride = dummy_pt_model.stride
    imgsz = (416, 416)
except Exception as e:
    print(f"Error loading OpenVINO model: {e}", file=sys.stderr)
    sys.exit(1)

@app.route("/predict", methods=["POST"])
def predict():
    if request.method != "POST":
        return jsonify({"error": "Only POST requests are accepted"}), 405

    if request.files.get("file"):
        im_file = request.files["file"]
        im_bytes = im_file.read()
        img = Image.open(io.BytesIO(im_bytes))

        im0 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Preprocess image for OpenVINO model
        # This uses the letterbox function from YOLOv5 utils
        img_preprocessed = letterbox(im0, imgsz, stride=stride, auto=True)[0]
        img_preprocessed = img_preprocessed.transpose((2, 0, 1))[::-1]  # HWC to CHW, RGB to BGR
        img_preprocessed = np.ascontiguousarray(img_preprocessed)
        img_preprocessed = img_preprocessed.astype(np.float32) / 255.0  # Normalize to 0.0 - 1.0
        img_preprocessed = np.expand_dims(img_preprocessed, 0) # Add batch dimension

        # OpenVINO Inference
        results = compiled_model([img_preprocessed])[output_layer]

        # Post-process results using YOLOv5 NMS on CPU tensor
        pred = non_max_suppression(torch.from_numpy(results), conf_thres=0.25, iou_thres=0.45, classes=None, agnostic_nms=False, max_det=1000)

        detections_list = []
        riders_without_helmets = []

        for i, det in enumerate(pred):
            if det is not None and len(det):
                det[:, :4] = scale_boxes(img_preprocessed.shape[2:], det[:, :4], im0.shape).round()

                license_plates = []
                riders = []
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = names[c]
                    confidence = float(conf)
                    bbox = [int(x) for x in xyxy]

                    detections_list.append({
                        "box": bbox,
                        "label": label,
                        "confidence": confidence
                    })

                    if label == "license-plate":
                        license_plates.append({"box": bbox, "confidence": confidence})
                    elif label == "rider":
                        riders.append({"box": bbox, "confidence": confidence})

                has_helmet_detection = any(d["label"] == "helmet" for d in detections_list)
                if len(riders) > 0 and not has_helmet_detection:
                    riders_without_helmets.append("A rider was detected without a helmet.")

        return jsonify({
            "success": True,
            "detections": detections_list,
            "riders_without_helmets": riders_without_helmets,
            "processing_time": 0 
        })

    return jsonify({"error": "No image file provided"}), 400

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    shape = im.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:
        r = min(r, 1.0)

    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    if auto:
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)
    elif scaleFill:
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        color = color

    dw /= 2
    dh /= 2

    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return im, r, (dw, dh)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=5000, type=int, help="port number")
    opt = parser.parse_args()

    app.run(host="0.0.0.0", port=opt.port)
