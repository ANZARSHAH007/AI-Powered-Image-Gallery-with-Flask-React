from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from PIL import Image
import torch
import wikipedia

# BLIP for Captioning
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_pil):
    inputs = blip_processor(image_pil, return_tensors="pt")
    with torch.no_grad():
        out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption

# CLIP for Semantic Embedding
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")

def get_clip_embedding(image_pil):
    inputs = clip_processor(images=image_pil, return_tensors="pt")
    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)
    return image_features[0].tolist()  # Convert tensor to list for storage

# YOLOv8 for Object Detection (requires ultralytics package)
try:
    from ultralytics import YOLO
    yolo_model = YOLO('yolov8n.pt')  # Downloaded automatically if not present

    def detect_objects(image_pil):
        results = yolo_model(image_pil)
        objects = []
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = yolo_model.model.names[cls]
                objects.append(label)
        return list(set(objects))  # Unique objects
except ImportError:
    def detect_objects(image_pil):
        return ["YOLOv8 not installed"]

# Placeholder for Reverse Image Search and Metadata Enrichment
def reverse_image_search(image_pil):
    # Integrate with Google Vision/Bing API here
    return {}


def enrich_metadata(caption, objects):
    enriched = {
        "caption_description": "",
        "object_descriptions": {}
    }

    # Try to describe the caption topic
    try:
        enriched["caption_description"] = wikipedia.summary(caption, sentences=2)
    except Exception:
        enriched["caption_description"] = "No description found."

    # Try to describe each object
    for obj in objects:
        try:
            enriched["object_descriptions"][obj] = wikipedia.summary(obj, sentences=1)
        except Exception:
            enriched["object_descriptions"][obj] = "No description found."

    return enriched
