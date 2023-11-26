from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Define path to the image file
source = 'https://www.youtube.com/watch?v=2Z52M8KP3m8'

# Run inference on the source
results = model(source)  # list of Results objects