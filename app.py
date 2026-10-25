"""
GreenLoop AI - Local Waste-to-Value Assistant
Flask Application with image validation, rule-based upcycling recommendations,
bilingual Tamil/English guidance, and SQLite sustainability tracking.
"""

import os
import uuid
from urllib.parse import urlsplit
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from PIL import Image

import database
import ai_classifier
from waste_data import WASTE_CATEGORIES, detect_category_from_keywords, get_category_data

app = Flask(__name__)
app.secret_key = os.environ.get("GREENLOOP_SECRET_KEY") or os.urandom(32)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.environ.get("GREENLOOP_STORAGE_DIR", os.path.join(BASE_DIR, "static"))
UPLOAD_FOLDER = os.environ.get("GREENLOOP_UPLOAD_FOLDER", os.path.join(STORAGE_FOLDER, "uploads"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # Allow typical downloaded phone photos.
MAX_IMAGE_PIXELS = 60_000_000  # Bound decode work, while allowing common 48 MP photos.

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("GREENLOOP_HTTPS", "0") == "1"

# Ensure upload directory & database exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
database.init_db()


@app.before_request
def protect_state_changing_requests():
    """Reject cross-site browser requests to state-changing endpoints."""
    if request.method not in {"POST", "PUT", "PATCH", "DELETE"}:
        return None
    if request.headers.get("Sec-Fetch-Site", "").lower() == "cross-site":
        abort(403)
    origin = request.headers.get("Origin")
    if origin and urlsplit(origin).netloc.lower() != request.host.lower():
        abort(403)
    return None


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_and_save_image(file_storage):
    """Validate, sanitize, resize, and save one supported image upload."""
    if not file_storage or file_storage.filename == "":
        return None, "No file selected."

    if not allowed_file(file_storage.filename):
        file_storage.close()
        return None, "Invalid file format. Please upload PNG, JPG, JPEG, or WEBP."

    try:
        extension = file_storage.filename.rsplit(".", 1)[1].lower()
        expected_formats = {"png": {"PNG"}, "jpg": {"JPEG"}, "jpeg": {"JPEG"}, "webp": {"WEBP"}}

        # Verify actual content and integrity, then reopen for dimensions and conversion.
        with Image.open(file_storage.stream) as check_image:
            if check_image.format not in {"PNG", "JPEG", "WEBP"}:
                return None, "Unsupported image content. Please upload PNG, JPG, JPEG, or WEBP."
            if check_image.format not in expected_formats[extension]:
                return None, "The file extension does not match its image content. Please rename it correctly and try again."
            check_image.verify()

        file_storage.stream.seek(0)
        with Image.open(file_storage.stream) as img:
            if img.width <= 0 or img.height <= 0 or img.width * img.height > MAX_IMAGE_PIXELS:
                return None, "Image dimensions are too large. Please upload an image under 60 megapixels."

            ext = extension
            raw_name = file_storage.filename.rsplit(".", 1)[0]
            sanitized_base = secure_filename(raw_name) or "upload"
            safe_name = f"waste_{uuid.uuid4().hex}_{sanitized_base}.{ext}"
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)

            converted = None
            try:
                output_image = img
                if img.mode == "CMYK" or (img.mode in ("RGBA", "P") and ext in ("jpg", "jpeg")):
                    converted = img.convert("RGB")
                    output_image = converted

                output_image.thumbnail((1200, 1200))
                output_format = {"png": "PNG", "jpg": "JPEG", "jpeg": "JPEG", "webp": "WEBP"}[ext]
                if output_format == "JPEG" and output_image.mode not in ("RGB", "L"):
                    if converted is not None:
                        converted.close()
                    converted = output_image.convert("RGB")
                    output_image = converted
                with open(save_path, "wb") as output_file:
                    output_image.save(output_file, format=output_format, optimize=True, quality=85)
            finally:
                if converted is not None:
                    converted.close()

        return f"uploads/{safe_name}", None
    except Exception:
        return None, "Image validation failed. Please upload a valid, uncorrupted image file."
    finally:
        file_storage.close()

def classify_waste_heuristic(filename, user_category=None, item_description="", image_path=None, image_prediction=None):
    """
    Transparent Waste Classification:
    Uses explicit user selection, then pixel-based model inference when an image
    is available, then clearly labelled text keyword fallbacks.
    
    Academic Note:
    The preferred offline vision model is trained on waste-material classes.
    Its result is still a suggestion users can change; ImageNet is a fallback.
    Filename and description keyword matching is a labelled fallback only.
    """
    # 1. Direct user manual selection takes highest precedence
    if user_category in WASTE_CATEGORIES:
        return user_category, "User-Selected & Confirmed"

    # Inference uses the saved, validated image content. The original filename is
    # not passed to the model and cannot affect its prediction.
    if image_path:
        prediction = image_prediction if image_prediction is not None else ai_classifier.predict_waste_image(image_path)
        predicted_category = prediction.get("category_id") if prediction.get("recognized") else None
        if predicted_category in WASTE_CATEGORIES:
            model_name = prediction.get("model_name", "Local Vision Model")
            return predicted_category, f"Image Model Suggestion ({model_name})"
        model_status = (
            "Image Model Uncertain" if prediction.get("is_ai")
            else "Image Model Unavailable"
        )
    else:
        model_status = "No Image Model Result"

    # 2. Check description keywords
    if item_description:
        detected = detect_category_from_keywords(item_description)
        if detected:
            return detected, "Keyword Heuristic (from Item Description)"

    # 3. Check filename keywords
    if filename:
        detected = detect_category_from_keywords(filename)
        if detected:
            return detected, "Filename Heuristic (from File Name)"

    # 4. Unknown: no reliable classification could be made
    return None, model_status


@app.route("/")
def home():
    """Homepage with hero, upload tool, categories overview, and AI transparency info."""
    stats = database.get_sustainability_stats()
    recent_activities = database.get_all_activities(limit=4)
    return render_template(
        "index.html",
        categories=WASTE_CATEGORIES,
        stats=stats,
        recent_activities=recent_activities
    )


@app.route("/analyze", methods=["POST"])
def analyze_waste():
    """
    Handles image upload and waste analysis.
    Renders the analysis result page or returns JSON depending on client request.
    """
    submitted_category = request.form.get("category", "").strip().lower()
    user_category = submitted_category if submitted_category in WASTE_CATEGORIES else ""
    item_description = request.form.get("item_description", "").strip()
    existing_image_path = request.form.get("existing_image_path", "").strip()
    file = request.files.get("waste_image")

    if submitted_category and not user_category:
        flash("Please choose one of the five supported waste categories.", "danger")
        return redirect(url_for("home"))
    if len(item_description) > 160:
        flash("Item descriptions must be 160 characters or fewer.", "danger")
        return redirect(url_for("home"))

    image_rel_path = None
    upload_error = None

    if file and file.filename != "":
        image_rel_path, upload_error = validate_and_save_image(file)
        if upload_error:
            flash(upload_error, "danger")
            return redirect(url_for("home"))
    elif existing_image_path:
        # Only allow paths created by this application; never accept arbitrary filesystem paths.
        candidate = existing_image_path.replace("\\", "/")
        basename = candidate[8:] if candidate.startswith("uploads/") else ""
        if basename and os.path.basename(basename) == basename and os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], basename)):
            image_rel_path = f"uploads/{basename}"

    # Determine category
    filename = file.filename if file else ""
    saved_image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_rel_path[8:]) if image_rel_path else None
    image_prediction = (
        ai_classifier.predict_waste_image(saved_image_path)
        if saved_image_path and not user_category else None
    )
    cat_id, detection_method = classify_waste_heuristic(
        filename, user_category, item_description, saved_image_path, image_prediction
    )
    category_data = get_category_data(cat_id)

    # Determine item name to display
    if item_description:
        display_item_name = item_description
    elif (image_prediction and image_prediction.get("recognized")
          and image_prediction.get("category_id") == cat_id
          and image_prediction.get("detected_item")):
        display_item_name = image_prediction["detected_item"]
    elif category_data:
        display_item_name = category_data["common_items"][0]
    else:
        display_item_name = "Unknown Waste Item"

    # If async JSON request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.args.get("format") == "json":
        return jsonify({
            "success": True,
            "category_id": cat_id,
            "category": category_data,
            "image_url": url_for("uploaded_file", filename=image_rel_path[8:]) if image_rel_path else None,
            "detection_method": detection_method,
            "item_name": display_item_name
        })

    # Render analysis result on template
    return render_template(
        "analysis_result.html",
        category=category_data,
        category_id=cat_id,
        all_categories=WASTE_CATEGORIES,
        image_path=image_rel_path,
        detection_method=detection_method,
        item_name=display_item_name
    )


@app.route("/dashboard")
def dashboard():
    """Dashboard of user-entered activity records and gamification points."""
    stats = database.get_sustainability_stats()
    activities = database.get_all_activities(limit=100)
    return render_template(
        "dashboard.html",
        stats=stats,
        activities=activities,
        categories=WASTE_CATEGORIES
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """Serve only sanitized upload basenames from the configured upload directory."""
    if os.path.basename(filename) != filename:
        abort(404)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, max_age=0)


@app.route("/api/log-activity", methods=["POST"])
def log_activity_api():
    """Logs an upcycling activity to the SQLite database and awards Green Impact Points."""
    category = request.form.get("category", "").lower().strip()
    item_name = request.form.get("item_name", "").strip()
    project_name = request.form.get("project_name", "").strip()
    image_path = request.form.get("image_path", "").strip().replace("\\", "/")
    if not (image_path.startswith("uploads/") and os.path.basename(image_path) == image_path[8:]):
        image_path = ""
    notes = request.form.get("notes", "").strip()

    if category not in WASTE_CATEGORIES or not item_name or not project_name:
        return jsonify({"success": False, "message": "Choose a supported category and provide an item and project name."}), 400

    project = next((p for p in WASTE_CATEGORIES[category]["upcycling_projects"] if p["title_en"] == project_name), None)
    if not project:
        return jsonify({"success": False, "message": "Choose a project from the selected category."}), 400
    # Points are taken from the curated project record, never from the browser.
    impact_points = int(project.get("points", 50))
    if len(item_name) > 120 or len(notes) > 1000:
        return jsonify({"success": False, "message": "Item names must be under 120 characters and notes under 1,000."}), 400
    # Prevent accidental duplicate submissions from awarding points twice
    row_id = database.log_activity_once(
        category=category, item_name=item_name, project_name=project_name,
        image_path=image_path, notes=notes, impact_points=impact_points
    )
    if row_id is None:
        return jsonify({
            "success": False,
            "duplicate": True,
            "message": f"'{item_name}' was already recorded recently! Duplicate points are not awarded to keep impact scores authentic."
        }), 409

    return jsonify({
        "success": True,
        "message": f"Great job! You earned +{impact_points} Green Impact Points.",
        "id": row_id,
        "points_earned": impact_points
    })


@app.route("/api/delete-activity/<int:activity_id>", methods=["POST"])
def delete_activity_api(activity_id):
    """Deletes an activity record from SQLite."""
    success = database.delete_activity(activity_id)
    if success:
        return jsonify({"success": True, "message": "Activity removed."})
    return jsonify({"success": False, "message": "Activity not found."}), 404


@app.route("/api/categories")
def get_categories_api():
    """Returns waste categories metadata."""
    return jsonify(WASTE_CATEGORIES)


@app.errorhandler(413)
def file_too_large(e):
    flash("Uploaded file exceeds 32MB limit. Please upload a smaller image.", "danger")
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("GREENLOOP_PORT", "5000"))
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=port)
