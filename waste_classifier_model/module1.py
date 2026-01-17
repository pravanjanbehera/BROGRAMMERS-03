import os
import urllib.request
import torch
from torchvision import models, transforms
from PIL import Image

# -------------------------------
# Load pretrained model once
# -------------------------------
print("🔄 Loading AI model...")

model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

# -------------------------------
# Image preprocessing pipeline
# -------------------------------
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])

# -------------------------------
# Auto-download ImageNet labels
# -------------------------------
LABEL_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABEL_FILE = "imagenet_classes.txt"

if not os.path.exists(LABEL_FILE):
    print("📥 Downloading ImageNet labels...")
    urllib.request.urlretrieve(LABEL_URL, LABEL_FILE)

with open(LABEL_FILE, "r") as f:
    IMAGENET_LABELS = [line.strip() for line in f.readlines()]

print("✅ Model and labels loaded successfully.")

# -------------------------------
# Mapping detected object → waste category
# -------------------------------
def map_to_waste(label):
    label = label.lower()

    if "bottle" in label or "plastic" in label:
        return "Plastic Bottle", 7
    elif "banana" in label or "apple" in label or "food" in label:
        return "Organic Waste", 1
    elif "can" in label or "metal" in label:
        return "Aluminium Can", 5
    elif "paper" in label or "book" in label or "box" in label:
        return "Cardboard Box", 2
    elif "battery" in label or "remote" in label:
        return "Old Battery", 9
    else:
        return "Mixed Waste", 5


# -------------------------------
# Image Analysis (Mini Google Lens)
# -------------------------------
def analyze_waste_image(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        predicted_index = outputs.argmax(1).item()

    detected_object = IMAGENET_LABELS[predicted_index]

    # Map detected object to waste category
    waste_label, risk = map_to_waste(detected_object)

    return waste_label, risk, detected_object


# -------------------------------
# Hotspot Classification
# -------------------------------
def classify_hotspot(risk_score):
    if risk_score >= 7:
        return "🔴 RED HOTSPOT"
    elif risk_score >= 4:
        return "🟡 YELLOW HOTSPOT"
    else:
        return "🟢 GREEN HOTSPOT"