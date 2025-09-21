import torch
import sys
import os

# Load the YOLOv5 model with custom weights from the data/models directory
model_path = os.path.join('..', 'data', 'models', 'best.pt')  # Adjust to use best.pt or 1500img.pt as needed
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

# Use sample image from data/images directory
img_path = os.path.join('..', 'data', 'images', 'samples', 'Screenshot 2024-02-27 172328_SAu1DqF.png')

# Check if image exists, if not use a placeholder path
if not os.path.exists(img_path):
    print(f"Sample image not found at {img_path}")
    print("Please place sample images in data/images/samples/ directory")
    # Use any available image in the samples directory
    samples_dir = os.path.join('..', 'data', 'images', 'samples')
    if os.path.exists(samples_dir):
        sample_files = [f for f in os.listdir(samples_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if sample_files:
            img_path = os.path.join(samples_dir, sample_files[0])
            print(f"Using {img_path} instead")
        else:
            print("No sample images found in data/images/samples/")
            sys.exit(1)
    else:
        print("Sample images directory not found")
        sys.exit(1)

# Perform inference on the image
result = model(img_path)

# Display the results
result.show()

# Save results to outputs directory
output_dir = os.path.join('..', 'outputs', 'detections')
os.makedirs(output_dir, exist_ok=True)
result.save(save_dir=output_dir)

print(f"Results saved to {output_dir}")