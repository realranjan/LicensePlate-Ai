import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import os

# Function to perform YOLOv5 object detection
def perform_object_detection(image_path):
    # Get the project root directory (parent of desktop_app)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Updated paths to reference ML models in new location
    detect_script = os.path.join(project_root, "ml_models", "detection", "detect2.py")
    weights_path = os.path.join(project_root, "data", "models", "1500img.pt")
    
    result = subprocess.run([
        "python",
        detect_script,
        "--weights", weights_path,
        "--source", image_path,
        "--img", "416"
    ], capture_output=True, text=True)
    return result.stdout

# Function to handle image upload and object detection
def upload_and_detect():
    filename = filedialog.askopenfilename()
    if filename:
        output_text.delete(1.0, tk.END)  # Clear previous output
        output = perform_object_detection(filename)
        output_text.insert(tk.END, output)

# Create Tkinter GUI
root = tk.Tk()
root.title("YOLOv5 Object Detection")

# Create and configure upload button
upload_button = tk.Button(root, text="Upload Image", command=upload_and_detect)
upload_button.pack()

# Create and configure text widget to display output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
output_text.pack()

root.mainloop()