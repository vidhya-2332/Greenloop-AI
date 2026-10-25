"""Offline waste-image suggestions with a legacy ImageNet fallback.

The primary MobileNetV2 model predicts waste-material classes. A legacy general
ImageNet model is used only when the waste-specific ONNX asset is unavailable.
Predictions are suggestions users can correct; unclear images remain uncertain.
"""
import os
import re
from PIL import Image, ImageOps

# Global state for model session and class definitions
_SESSION = None
_CLASSES = []
_MAPPING = {}
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "mobilenetv2-7.onnx")
CLASSES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "imagenet_classes.txt")
WASTE_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "waste_mobilenetv2.onnx")
WASTE_LABELS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "waste_mobilenetv2_labels.txt")
_WASTE_SESSION = None
_WASTE_LABELS = []

# Dedicated waste model labels from sengtha/iany-waste-v1 (CC BY 4.0).
# Its `can` output is GreenLoop's metal stream; both plastic outputs map to plastic.
WASTE_CATEGORY_MAP = {
    "can": ("metal", "Metal Can / Tin"),
    "glass": ("glass", "Glass Bottle / Jar"),
    "organic": ("organic", "Organic / Kitchen Waste"),
    "paper": ("paper", "Paper / Cardboard"),
    "plastic_bottle": ("plastic", "Plastic Bottle"),
    "plastic_other": ("plastic", "Plastic Item"),
}


def load_waste_model():
    """Load the waste-specific ONNX classifier, returning False if unavailable."""
    global _WASTE_SESSION, _WASTE_LABELS
    if _WASTE_SESSION is not None:
        return True
    if not os.path.isfile(WASTE_MODEL_PATH) or not os.path.isfile(WASTE_LABELS_PATH):
        return False
    try:
        import onnxruntime as ort
        options = ort.SessionOptions()
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        session = ort.InferenceSession(WASTE_MODEL_PATH, options, providers=["CPUExecutionProvider"])
        with open(WASTE_LABELS_PATH, "r", encoding="utf-8") as label_file:
            labels = [line.strip() for line in label_file if line.strip()]
        if len(labels) != 7 or session.get_outputs()[0].shape[-1] != len(labels):
            return False
        _WASTE_SESSION, _WASTE_LABELS = session, labels
        return True
    except Exception as exc:
        print(f"[GreenLoop AI] Warning: Could not initialize waste model: {exc}")
        _WASTE_SESSION = None
        return False


def _predict_waste_model(image_input):
    """Return a prediction from the waste-trained model, or None if unavailable/invalid."""
    if not load_waste_model():
        return None
    try:
        import numpy as np
        with Image.open(image_input) as source:
            # Tiny uploads do not contain enough visual detail for material sorting.
            if min(source.size) < 96:
                return {
                    "recognized": False, "category_id": None, "confidence": 0.0,
                    "confidence_percent": 0.0, "detected_item": "Photo Too Small",
                    "top_predictions": [], "is_ai": True,
                    "model_name": "Waste-trained MobileNetV2 (ONNX)",
                }
            oriented = ImageOps.exif_transpose(source)
            rgb = oriented.convert("RGB")
            if oriented is not source:
                oriented.close()
            try:
                width, height = rgb.size
                side = min(width, height)
                left, top = (width - side) // 2, (height - side) // 2
                cropped = rgb.crop((left, top, left + side, top + side))
                try:
                    resized = cropped.resize((224, 224), Image.Resampling.BILINEAR)
                    try:
                        tensor = np.asarray(resized, dtype=np.float32) / 127.5 - 1.0
                    finally:
                        resized.close()
                finally:
                    cropped.close()
            finally:
                rgb.close()

        input_name = _WASTE_SESSION.get_inputs()[0].name
        scores = np.asarray(_WASTE_SESSION.run(None, {input_name: tensor[None, ...]})[0]).reshape(-1)
        # Model output is a softmax. Normalize defensively if an export returns logits.
        if np.any(scores < 0) or not np.isfinite(scores).all() or not np.isclose(scores.sum(), 1.0, atol=0.02):
            scores = np.exp(scores - np.max(scores))
            scores /= scores.sum()
        order = np.argsort(scores)[::-1]
        top = [{"label": _WASTE_LABELS[int(i)], "confidence": round(float(scores[i]) * 100, 1)}
               for i in order[:3]]
        idx = int(order[0])
        label = _WASTE_LABELS[idx]
        confidence = float(scores[idx])
        mapped = WASTE_CATEGORY_MAP.get(label)
        recognized = mapped is not None and confidence >= 0.35
        return {
            "recognized": recognized,
            "category_id": mapped[0] if recognized else None,
            "confidence": confidence,
            "confidence_percent": round(confidence * 100, 1),
            "detected_item": mapped[1] if recognized else label.title(),
            "top_predictions": top,
            "is_ai": True,
            "model_name": "Waste-trained MobileNetV2 (ONNX)",
        }
    except Exception as exc:
        print(f"[GreenLoop AI] Waste-model inference error: {exc}")
        return None

# Candidate ImageNet synset indices mapped to the five GreenLoop streams.
# Plastic Waste
PLASTIC_INDICES = {
    455: "Bottle Cap",
    463: "Plastic Bucket / Pail",
    529: "Diaper / Plastic Lining",
    631: "Lotion / Toiletry Bottle",
    647: "Measuring Cup",
    680: "Silicone / Plastic Nipple",
    720: "Pill Bottle",
    728: "Plastic Bag / Polybag",
    737: "PET Soda / Pop Bottle",
    838: "Sunscreen Container",
    845: "Medical Syringe",
    898: "PET Water Bottle",
    899: "Plastic Water Jug",
}

# Glass Bottles & Jars
GLASS_INDICES = {
    438: "Laboratory Beaker",
    440: "Glass Beer Bottle",
    572: "Glass Goblet / Chalice",
    901: "Glass Whiskey Jug",
    907: "Glass Wine Bottle",
}

# Metal Cans & Tins
METAL_INDICES = {
    412: "Metal Dustbin / Wastebin",
    469: "Metal Cauldron",
    473: "Metal Can / Tin Opener",
    488: "Metal Chain",
    521: "Metal Crock Pot",
    567: "Metal Frying Pan / Skillet",
    587: "Hammer / Metal Tool",
    653: "Galvanized Milk Can",
    677: "Nail / Metal Fastener",
    738: "Metal Herb / Flower Pot",
    740: "Power Drill / Metal Tool",
    783: "Screw / Metal Fastener",
    784: "Screwdriver / Metal Tool",
    849: "Metal Teapot",
    859: "Electric Metal Toaster",
    926: "Metal Cooking Hotpot",
}

# Hardware labels absent from the waste model's can-focused metal class.
METAL_HARDWARE_INDICES = {
    473: "Can Opener / Tin Opener",
    488: "Metal Chain",
    587: "Hammer / Metal Tool",
    677: "Nail / Metal Fastener",
    740: "Power Drill / Metal Tool",
    783: "Screw / Metal Fastener",
    784: "Screwdriver / Metal Tool",
}

# Paper & Cardboard
PAPER_INDICES = {
    446: "Cardboard Binder / Folder",
    478: "Cardboard Delivery Carton",
    549: "Paper Envelope / Mailer",
    692: "Cardboard Packet / Box",
    700: "Paper Towel / Napkin",
    917: "Comic Book / Newsprint",
    921: "Book Jacket / Paper Cover",
    922: "Printed Paper Menu",
    999: "Toilet Tissue / Paper Roll",
}

# Organic & Kitchen Waste
ORGANIC_INDICES = {
    936: "Head Cabbage",
    937: "Broccoli Floret",
    938: "Cauliflower Scrap",
    939: "Zucchini / Courgette",
    940: "Spaghetti Squash",
    941: "Acorn Squash",
    942: "Butternut Squash",
    943: "Cucumber / Cuke",
    944: "Artichoke / Plant Scrap",
    945: "Bell Pepper / Capsicum",
    946: "Cardoon Stalk",
    947: "Mushroom Cap",
    948: "Granny Smith Apple",
    949: "Fresh Strawberry",
    950: "Orange / Citrus Fruit",
    951: "Lemon / Lime Citrus",
    952: "Fig Fruit",
    953: "Pineapple Fruit Peel",
    954: "Banana Fruit / Peel",
    955: "Jackfruit Husk",
    956: "Custard Apple",
    957: "Pomegranate Fruit",
    987: "Corn / Maize Cob",
    988: "Acorn Nut",
}

def _build_waste_mapping():
    """Builds the comprehensive lookup from class index to (category_id, clean_label)."""
    mapping = {}
    for idx, name in PLASTIC_INDICES.items():
        mapping[idx] = ("plastic", name)
    for idx, name in GLASS_INDICES.items():
        mapping[idx] = ("glass", name)
    for idx, name in METAL_INDICES.items():
        mapping[idx] = ("metal", name)
    for idx, name in PAPER_INDICES.items():
        mapping[idx] = ("paper", name)
    for idx, name in ORGANIC_INDICES.items():
        mapping[idx] = ("organic", name)
    return mapping


def _predict_metal_hardware_hint(image_input):
    """Recognize a small set of clear hardware objects omitted from waste labels.

    The waste dataset's metal class is largely cans, so its confident organic
    guesses can be wrong for screws and nails. A narrowly scoped ImageNet hint
    fixes those cases without treating arbitrary ImageNet objects as waste.
    """
    if not is_model_available():
        return None
    try:
        import numpy as np
        tensor = preprocess_image(image_input)
        input_name = _SESSION.get_inputs()[0].name
        logits = _SESSION.run(None, {input_name: tensor})[0][0]
        logits = logits - np.max(logits)
        probabilities = np.exp(logits)
        probabilities /= probabilities.sum()
        best = int(np.argmax(probabilities))
        confidence = float(probabilities[best])
        label = METAL_HARDWARE_INDICES.get(best)
        if label and confidence >= 0.30:
            return {"category_id": "metal", "detected_item": label,
                    "confidence": confidence, "confidence_percent": round(confidence * 100, 1)}
    except Exception as exc:
        print(f"[GreenLoop AI] Hardware hint inference error: {exc}")
    return None

def load_ai_model():
    """
    Initializes ONNX Runtime session and class definitions.
    Returns True if successfully loaded, False otherwise.
    """
    global _SESSION, _CLASSES, _MAPPING

    if _SESSION is not None:
        return True

    if not os.path.exists(MODEL_PATH):
        return False

    try:
        import onnxruntime as ort
        # CPU execution provider for 100% offline compatibility
        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        _SESSION = ort.InferenceSession(MODEL_PATH, opts, providers=["CPUExecutionProvider"])

        if os.path.exists(CLASSES_PATH):
            with open(CLASSES_PATH, "r", encoding="utf-8") as f:
                _CLASSES = [line.strip() for line in f]
        else:
            _CLASSES = []

        _MAPPING = _build_waste_mapping()
        return True
    except Exception as e:
        print(f"[GreenLoop AI] Warning: Could not initialize ONNX model: {e}")
        _SESSION = None
        return False

def is_model_available():
    """Checks if the local AI vision model is ready for inference."""
    global _SESSION
    if _SESSION is None:
        return load_ai_model()
    return True

def preprocess_image(image_input):
    """
    Preprocesses image to MobileNetV2 input specifications:
    - Resize to 224x224
    - Convert RGB to float32 normalized in [0, 1]
    - Standard ImageNet standardization (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    - Shape: (1, 3, 224, 224)
    """
    import numpy as np

    if isinstance(image_input, str) or hasattr(image_input, "read"):
        # Close files opened here even when decoding or resizing raises an error.
        with Image.open(image_input) as img:
            return _image_to_tensor(img, np)
    return _image_to_tensor(image_input, np)


def _image_to_tensor(img, np):
    """Convert an open Pillow image to a normalized MobileNetV2 tensor."""
    rgb = img.convert("RGB")
    try:
        resized = rgb.resize((224, 224), Image.Resampling.BILINEAR)
        try:
            arr = np.array(resized, dtype=np.float32) / 255.0
        finally:
            resized.close()
    finally:
        rgb.close()

    # Normalize with ImageNet mean and standard deviation
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    normalized = (arr - mean) / std

    # Transpose from (H, W, C) to (C, H, W)
    chw = np.transpose(normalized, (2, 0, 1))

    # Add batch dimension -> (1, 3, 224, 224)
    batch = np.expand_dims(chw, axis=0).astype(np.float32)
    return batch

def predict_waste_image(image_input):
    """
    Runs genuine deep-learning inference using MobileNetV2.
    Returns:
    {
        'recognized': bool,
        'category_id': str or None,   # 'plastic', 'paper', 'glass', 'metal', 'organic', or None
        'confidence': float,          # 0.0 to 1.0
        'confidence_percent': float,  # e.g. 87.5
        'detected_item': str,         # Clean human-readable item name
        'top_predictions': list,      # Top-3 predictions with labels and percentages
        'is_ai': True,
        'model_name': 'MobileNetV2 (ONNX Neural Network)'
    }
    """
    # Prefer the waste-trained model. The general ImageNet classifier remains a
    # compatibility fallback only when the dedicated model files are unavailable.
    waste_prediction = _predict_waste_model(image_input)
    if waste_prediction is not None:
        hardware_hint = _predict_metal_hardware_hint(image_input)
        if hardware_hint:
            waste_prediction = dict(waste_prediction)
            waste_prediction.update(hardware_hint)
            waste_prediction.update({"recognized": True, "is_ai": True,
                                     "model_name": "Waste-trained model + hardware object check"})
        return waste_prediction

    if not is_model_available():
        return {
            "recognized": False,
            "category_id": None,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "detected_item": "Model Not Loaded",
            "top_predictions": [],
            "is_ai": False,
            "model_name": "None"
        }

    try:
        import numpy as np

        # Preprocess input image
        input_tensor = preprocess_image(image_input)

        # Forward pass
        input_name = _SESSION.get_inputs()[0].name
        outputs = _SESSION.run(None, {input_name: input_tensor})[0]

        # Numerically stable Softmax probabilities
        logits = outputs[0]
        exp_logits = np.exp(logits - np.max(logits))
        probabilities = exp_logits / np.sum(exp_logits)

        # Sort top-5 indices by probability
        top_indices = np.argsort(probabilities)[::-1][:5]

        top_predictions = []
        for idx in top_indices:
            prob = float(probabilities[idx])
            raw_label = _CLASSES[idx] if idx < len(_CLASSES) else f"Class #{idx}"
            # Extract clean name after synset id
            clean_name = raw_label.split(" ", 1)[1] if " " in raw_label else raw_label
            clean_name = clean_name.split(",")[0].strip().title()
            top_predictions.append({
                "index": int(idx),
                "label": clean_name,
                "confidence": round(prob * 100, 1)
            })

        # Use the top-ranked mapped object as a suggestion. ImageNet softmax scores
        # are not calibrated waste confidence values, so a fixed probability cutoff
        # can discard a relevant label (for example, this user's paper sheet as Envelope).
        best_index = int(top_indices[0])
        matched_category, matched_item = _MAPPING.get(best_index, (None, None))
        matched_confidence = float(probabilities[best_index]) if matched_category else 0.0

        if matched_category is not None:
            return {
                "recognized": True,
                "category_id": matched_category,
                "confidence": matched_confidence,
                "confidence_percent": round(matched_confidence * 100, 1),
                "detected_item": matched_item,
                "top_predictions": top_predictions[:3],
                "is_ai": True,
                "model_name": "MobileNetV2 (ONNX Deep Neural Network)"
            }
        else:
            # Uncertain / Unsupported object
            top_prob = float(probabilities[top_indices[0]])
            top_item = top_predictions[0]["label"] if top_predictions else "Unknown Object"
            return {
                "recognized": False,
                "category_id": None,
                "confidence": top_prob,
                "confidence_percent": round(top_prob * 100, 1),
                "detected_item": top_item,
                "top_predictions": top_predictions[:3],
                "is_ai": True,
                "model_name": "MobileNetV2 (ONNX Deep Neural Network)"
            }

    except Exception as e:
        print(f"[GreenLoop AI] Inference error: {e}")
        return {
            "recognized": False,
            "category_id": None,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "detected_item": "Inference Error",
            "top_predictions": [],
            "is_ai": False,
            "model_name": "MobileNetV2"
        }

