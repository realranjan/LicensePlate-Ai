import argparse
import io
import torch
from flask import Flask, request, jsonify
from PIL import Image
import sys
from pathlib import Path

# Add YOLOv5 root to sys.path
# Assuming ml_service/yolov5 is the YOLOv5 root
FILE = Path(__file__).resolve()
def find_yolov5_root(current_path):
    # Go up directories until yolov5 is found or max depth reached
    for _ in range(5): # Limit search depth
        if (current_path / "yolov5").is_dir():
            return current_path / "yolov5"
        current_path = current_path.parent
    return None # Not found

YOLOV5_ROOT = find_yolov5_root(FILE.parent)

if YOLOV5_ROOT and str(YOLOV5_ROOT) not in sys.path:
    sys.path.append(str(YOLOV5_ROOT))

# Import YOLOv5 components
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes, check_img_size
from utils.torch_utils import select_device

app = Flask(__name__)

# Load model globally when the Flask app starts up
# Update WEIGHTS_PATH to point to your model in ml_service/data/models
WEIGHTS_PATH = FILE.parent / "data" / "models" / "1500img.pt"
device = select_device("") # "" for CPU, "0" for GPU 0, etc.
model = DetectMultiBackend(WEIGHTS_PATH, device=device, dnn=False, data=YOLOV5_ROOT / "data/coco128.yaml", fp16=False)
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size((640, 640), s=stride) # inference size

@app.route("/predict", methods=["POST"])
def predict():
    if request.method != "POST":
        return jsonify({"error": "Only POST requests are accepted"}), 405

    if request.files.get("file"):
        im_file = request.files["file"]
        im_bytes = im_file.read()
        img = Image.open(io.BytesIO(im_bytes))

        # Prepare image for inference
        # Convert PIL Image to OpenCV format (BGR)
        im0 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Apply letterbox padding (function from YOLOv5 utils)
        img = letterbox(im0, imgsz, stride=stride, auto=pt)[0]
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, RGB to BGR
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if model.fp16 else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Inference
        pred = model(img, augment=False, visualize=False)

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic_nms=False, max_det=1000)

        detections_list = []
        riders_without_helmets = []

        # Process predictions
        for i, det in enumerate(pred):
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()

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
            "processing_time": 0 # TODO: Add actual processing time calculation
        })

    return jsonify({"error": "No image file provided"}), 400

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while maintaining aspect ratio
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        color = color  # set custom color

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=5000, type=int, help="port number")
    opt = parser.parse_args()

    # The model is loaded globally, no need to load here again
    app.run(host="0.0.0.0", port=opt.port) # debug=True causes Restarting with stat
