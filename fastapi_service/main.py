from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import torch
import numpy as np
import cv2
from PIL import Image
import sys
import json

app = FastAPI()

sys.path.append(str(Path(__file__).parent / "yolov5"))
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import (non_max_suppression, scale_boxes, check_img_size)
from yolov5.utils.torch_utils import select_device

# Define paths relative to the current file (main.py)
YOLOV5_ROOT = Path(__file__).parent / "yolov5"
WEIGHTS_PATH = Path(__file__).parent / "data" / "models" / "1500img.pt"

# Load model globally when the FastAPI app starts up
device = select_device("") # "" for CPU, "0" for GPU 0, etc.
model = DetectMultiBackend(WEIGHTS_PATH, device=device, dnn=False, data=YOLOV5_ROOT / "data/coco128.yaml", fp16=False)
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size((640, 640), s=stride) # inference size

@app.post("/detect-license-plate/")
async def detect_license_plate(file: UploadFile = File(...)):
    """
    Receives an image, forwards it to the ML Models service, and returns the detection results.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        image_np = np.array(image)
        # Convert RGB to BGR for OpenCV processing
        im0 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Prepare image for inference
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
            s = "" # string for logging
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()

                # Filter detections to find license plates and riders for helmet detection
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
                    
                    if label == "license-plate": # Assuming "license-plate" is one of your classes
                        license_plates.append({"box": bbox, "confidence": confidence})
                    elif label == "rider": # Assuming "rider" is one of your classes
                        riders.append({"box": bbox, "confidence": confidence})
                
                # Simple helmet detection logic (you might need a more sophisticated approach)
                # This assumes if a rider is detected, there should be a helmet detection associated
                # within a certain proximity. For simplicity, we'll just check if any "helmet" class is present.
                has_helmet_detection = any(d["label"] == "helmet" for d in detections_list)
                if len(riders) > 0 and not has_helmet_detection:
                    riders_without_helmets.append("A rider was detected without a helmet.")
            
        return JSONResponse(content={
            "success": True,
            "image_url": "processed_image_url_placeholder", # You might want to upload processed image
            "detections": json.dumps(detections_list),
            "riders_without_helmets": riders_without_helmets,
            "processing_time": 0 # TODO: Add actual processing time calculation
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during detection: {e}")

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

@app.get("/")
@app.head("/")  # Add this line to allow HEAD requests
async def root():
    return {"message": "Welcome to the FastAPI License Plate Detection API!"}
