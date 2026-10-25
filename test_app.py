"""
Automated Test Suite for GreenLoop AI
Tests Flask endpoints, Pillow image validation, SQLite database logging,
and knowledge repository bilingual queries.
"""

import os
import io
import html
import re
import hashlib
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

import app as flask_app
import ai_classifier
import database
import waste_data

class GreenLoopTestCase(unittest.TestCase):
    def setUp(self):
        # Configure test client
        flask_app.app.config["TESTING"] = True
        flask_app.app.config["WTF_CSRF_ENABLED"] = False
        self.original_upload_folder = flask_app.app.config["UPLOAD_FOLDER"]
        self.original_db_path = database.DB_PATH
        self.real_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "greenloop.db")
        with open(self.real_db_path, "rb") as db_file:
            self.real_db_hash = hashlib.sha256(db_file.read()).hexdigest()
        self.test_upload_dir = tempfile.TemporaryDirectory()
        flask_app.app.config["UPLOAD_FOLDER"] = self.test_upload_dir.name
        database.DB_PATH = os.path.join(self.test_upload_dir.name, "test.db")
        self.client = flask_app.app.test_client()
        self.classifier_patch = patch.object(
            flask_app.ai_classifier,
            "predict_waste_image",
            return_value={"recognized": False, "category_id": None},
        )
        self.classifier_mock = self.classifier_patch.start()
        self.addCleanup(self.classifier_patch.stop)

        # Ensure DB is ready
        database.init_db()

    def tearDown(self):
        flask_app.app.config["UPLOAD_FOLDER"] = self.original_upload_folder
        database.DB_PATH = self.original_db_path
        self.test_upload_dir.cleanup()
        with open(self.real_db_path, "rb") as db_file:
            self.assertEqual(hashlib.sha256(db_file.read()).hexdigest(), self.real_db_hash)

    def test_database_logging_and_stats(self):
        """Test logging upcycle activity and reading back verified metrics."""
        # Log an activity
        row_id = database.log_activity(
            category="plastic",
            item_name="Test PET Bottle",
            project_name="Self-Watering Planter",
            notes="Automated test note"
        )
        self.assertIsNotNone(row_id)
        self.assertTrue(row_id > 0)

        # Check stats
        stats = database.get_sustainability_stats()
        self.assertGreaterEqual(stats["total_diverted"], 1)
        self.assertGreaterEqual(stats["category_counts"]["plastic"], 1)

        # Delete activity
        deleted = database.delete_activity(row_id)
        self.assertTrue(deleted)

    def test_categories_and_bilingual_data(self):
        """Verify all 5 waste streams exist with English and Tamil fields, and at least 3 projects with points."""
        categories = waste_data.WASTE_CATEGORIES
        required_keys = ["plastic", "paper", "glass", "metal", "organic"]
        for key in required_keys:
            self.assertIn(key, categories)
            cat = categories[key]
            self.assertEqual(cat["id"], key)
            self.assertIn("name_en", cat)
            self.assertIn("name_ta", cat)
            self.assertIn("upcycling_projects", cat)
            self.assertGreaterEqual(len(cat["upcycling_projects"]), 3, f"Category {key} should have at least 3 upcycling projects")
            self.assertTrue(cat["summary_en"].strip())
            self.assertTrue(cat["summary_ta"].strip())
            self.assertIn("safe_disposal_steps_en", cat["disposal_guidance"])
            self.assertIn("safe_disposal_steps_ta", cat["disposal_guidance"])
            project_ids = [project["id"] for project in cat["upcycling_projects"]]
            self.assertEqual(len(project_ids), len(set(project_ids)))
            
            # Check bilingual project details and points on all projects
            for project in cat["upcycling_projects"]:
                self.assertIn("title_en", project)
                self.assertIn("title_ta", project)
                self.assertIn("steps_en", project)
                self.assertIn("steps_ta", project)
                self.assertIn("materials_en", project)
                self.assertIn("materials_ta", project)
                self.assertIn("safety_tip_en", project)
                self.assertIn("safety_tip_ta", project)
                self.assertIn("points", project)
                self.assertGreater(project["points"], 0)
                self.assertLessEqual(project["points"], 500)
                self.assertTrue(project["materials_en"])
                self.assertTrue(project["materials_ta"])
                self.assertTrue(project["steps_en"])
                self.assertTrue(project["steps_ta"])

    def test_home_route(self):
        """Verify homepage renders with HTTP 200 and key elements."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GreenLoop", response.data)
        self.assertIn(b"Turn Everyday Waste into", response.data)

    def test_dashboard_route(self):
        """Verify dashboard renders with HTTP 200."""
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Activity & Points Dashboard", response.data)

    def test_category_api_and_upload_serving(self):
        response = self.client.get("/api/categories")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.get_json()), {"plastic", "paper", "glass", "metal", "organic"})

        upload = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(self._png_bytes()), "photo.png"),
        })
        match = re.search(rb'src="(/uploads/[^\"]+)"', upload.data)
        self.assertIsNotNone(match)
        image_response = self.client.get(match.group(1).decode("ascii"))
        self.assertEqual(image_response.status_code, 200)
        self.assertEqual(image_response.mimetype, "image/png")
        image_response.close()

        self.assertEqual(self.client.get("/uploads/../app.py").status_code, 404)

    def test_waste_analysis_route(self):
        """Verify analyzing waste route accepts form inputs."""
        response = self.client.post("/analyze", data={
            "category": "glass",
            "item_description": "Pickle Jar"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Glass Bottles &amp; Jars", response.data)
        self.assertIn(b"Pickle Jar", response.data)

    def test_image_model_item_label_is_shown_with_its_category(self):
        """Show the model's specific object label, not the category's generic example."""
        prediction = {
            "recognized": True, "category_id": "metal",
            "detected_item": "Nail / Metal Fastener", "is_ai": True,
            "model_name": "Waste-trained model + hardware object check",
        }
        with patch.object(flask_app.ai_classifier, "predict_waste_image", return_value=prediction):
            response = self.client.post("/analyze", data={
                "waste_image": (io.BytesIO(self._png_bytes()), "generic-photo.png"),
            })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Metal Cans &amp; Tins", response.data)
        self.assertIn(b"Nail / Metal Fastener", response.data)
        self.assertIn(b"hardware object check", response.data)

    def test_image_validation_with_pillow(self):
        """Verify Pillow correctly validates real images and rejects corrupted ones."""
        # 1. Create a genuine in-memory test image with Pillow
        img_byte_arr = io.BytesIO()
        test_img = Image.new("RGB", (200, 200), color="green")
        test_img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        response = self.client.post("/analyze", data={
            "waste_image": (img_byte_arr, "test_leaf.png"),
            "category": "organic",
            "item_description": "Banana Peel"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Organic &amp; Kitchen Waste", response.data)

        # 2. Test corrupted non-image file
        fake_file = io.BytesIO(b"Not an image at all!")
        response_invalid = self.client.post("/analyze", data={
            "waste_image": (fake_file, "fake.png"),
            "category": "plastic"
        }, follow_redirects=True)
        # Should redirect with flash alert
        self.assertEqual(response_invalid.status_code, 200)
        self.assertIn(b"Image validation failed", response_invalid.data)

    def test_oversized_and_unsupported_uploads_are_graceful(self):
        """Unsupported extensions and request bodies over the limit return friendly redirects."""
        unsupported = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(b"not an image"), "waste.gif")
        }, follow_redirects=True)
        self.assertEqual(unsupported.status_code, 200)
        self.assertIn(b"Invalid file format", unsupported.data)

        oversized = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(b"x" * (flask_app.MAX_CONTENT_LENGTH + 1)), "large.jpg")
        })
        self.assertEqual(oversized.status_code, 302)
        self.assertEqual(oversized.location, "/")
        oversized.request.environ["wsgi.input"].close()
        oversized.close()

    def test_large_downloaded_photo_is_resized_and_accepted(self):
        image = io.BytesIO()
        Image.new("RGB", (5000, 5000), color="white").save(image, format="PNG")
        image.seek(0)
        response = self.client.post("/analyze", data={
            "waste_image": (image, "large-dimensions.png"),
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"dimensions are too large", response.data)
        saved = [name for name in os.listdir(self.test_upload_dir.name) if name.startswith("waste_")]
        self.assertEqual(len(saved), 1)
        with Image.open(os.path.join(self.test_upload_dir.name, saved[0])) as uploaded:
            self.assertLessEqual(max(uploaded.size), 1200)

    def test_upload_must_contain_supported_image_content(self):
        response = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(b"not a jpeg"), "photo.jpg"),
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Image validation failed", response.data)

    def test_upload_extension_must_match_image_content(self):
        response = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(self._png_bytes()), "photo.jpg"),
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"extension does not match", response.data)

    def test_cross_site_state_changing_request_is_rejected(self):
        response = self.client.post("/api/delete-activity/1", headers={
            "Origin": "https://attacker.example",
            "Sec-Fetch-Site": "cross-site",
        })
        self.assertEqual(response.status_code, 403)

    def test_api_log_and_delete(self):
        """Verify REST API for logging and deleting activities."""
        # Log via API
        response = self.client.post("/api/log-activity", data={
            "category": "metal",
            "item_name": "Tomato Soup Can",
            "project_name": waste_data.WASTE_CATEGORIES["metal"]["upcycling_projects"][0]["title_en"],
            "impact_points": 999,
            "notes": "Kitchen test"
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["points_earned"], waste_data.WASTE_CATEGORIES["metal"]["upcycling_projects"][0]["points"])
        item_id = json_data["id"]

        # Delete via API
        del_response = self.client.post(f"/api/delete-activity/{item_id}")
        self.assertEqual(del_response.status_code, 200)
        del_json = del_response.get_json()
        self.assertTrue(del_json["success"])
        invalid = self.client.post("/api/log-activity", data={
            "category": "wood", "item_name": "item", "project_name": "Anything"
        })
        self.assertEqual(invalid.status_code, 400)

    def test_empty_database_milestones_and_delete_recalculation(self):
        """Empty stats are safe and all derived values follow inserts/deletes."""
        original_path = database.DB_PATH
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                database.DB_PATH = os.path.join(temp_dir, "test.db")
                database.init_db()
                empty = database.get_sustainability_stats()
                self.assertEqual(empty["total_activities"], 0)
                self.assertEqual(empty["total_points"], 0)
                self.assertEqual(empty["next_achievement_progress"], 0)
                self.assertEqual(empty["category_counts"]["plastic"], 0)
                row_id = database.log_activity_once("plastic", "Bottle", "Planter", impact_points=50)
                filled = database.get_sustainability_stats()
                self.assertEqual(filled["category_counts"]["plastic"], 1)
                self.assertIn("First Loop", filled["achievements"])
                self.assertTrue(database.delete_activity(row_id))
                self.assertEqual(database.get_sustainability_stats()["total_points"], 0)
        finally:
            database.DB_PATH = original_path

    def test_unicode_filename_upload(self):
        """Verify upload with non-ASCII / Tamil filename is accepted safely."""
        img_buf = io.BytesIO()
        Image.new("RGB", (100, 100), color="blue").save(img_buf, format="JPEG")
        img_buf.seek(0)

        response = self.client.post("/analyze", data={
            "waste_image": (img_buf, "பாட்டில்.jpg"),
            "category": "plastic"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Image validation failed", response.data)
        self.assertIn(b"Plastic Waste", response.data)

    def test_unknown_classification_when_no_keywords(self):
        """Verify generic images with no matching keywords display Unknown rather than defaulting to plastic."""
        img_buf = io.BytesIO()
        Image.new("RGB", (100, 100), color="gray").save(img_buf, format="JPEG")
        img_buf.seek(0)

        response = self.client.post("/analyze", data={
            "waste_image": (img_buf, "IMG_20261010_123456.jpg"),
            "category": "",
            "item_description": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1 class="result-heading">Unknown Material \xe2\x80\x94 Please select a category</h1>', response.data)
        self.assertIn(b"Unknown Material", response.data)
        # Must NOT falsely claim it's a plastic bottle in the result heading
        self.assertNotIn(b'<h1 class="result-heading">PET Water Bottles</h1>', response.data)

    def test_filename_keyword_fallback_for_all_five_categories(self):
        """Verify filename keywords suggest each category; blank pixels are not classifier evidence."""
        test_cases = [
            ("water_bottle.jpg", b"Plastic Waste"),
            ("cardboard_delivery_box.png", b"Paper &amp; Cardboard"),
            ("pickle_jar.jpg", b"Glass Bottles &amp; Jars"),
            ("soda_can.png", b"Metal Cans &amp; Tins"),
            ("banana_peel.jpg", b"Organic &amp; Kitchen Waste"),
        ]

        for filename, expected_snippet in test_cases:
            img_buf = io.BytesIO()
            image_format = "JPEG" if filename.lower().endswith((".jpg", ".jpeg")) else "PNG"
            Image.new("RGB", (60, 60), color="white").save(img_buf, format=image_format)
            img_buf.seek(0)

            response = self.client.post("/analyze", data={
                "waste_image": (img_buf, filename),
                "category": "",
                "item_description": ""
            })
            self.assertEqual(response.status_code, 200, f"Failed for {filename}")
            self.assertIn(expected_snippet, response.data, f"Snippet {expected_snippet} not found in response for {filename}")
            self.assertIn(b"Filename Heuristic", response.data)

    def test_manual_selection_with_generic_image(self):
        """Verify user category selection correctly guides generic photos."""
        img_buf = io.BytesIO()
        Image.new("RGB", (60, 60), color="white").save(img_buf, format="PNG")
        img_buf.seek(0)

        response = self.client.post("/analyze", data={
            "waste_image": (img_buf, "photo_123.png"),
            "category": "metal",
            "item_description": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Metal Cans &amp; Tins", response.data)
        self.assertIn(b"User-Selected &amp; Confirmed", response.data)
        self.classifier_mock.assert_not_called()

    def test_analyze_invokes_image_classifier_with_saved_upload(self):
        self.classifier_mock.return_value = {"recognized": True, "category_id": "paper"}
        response = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(self._png_bytes()), "IMG_20261010_123456.png"),
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Paper &amp; Cardboard", response.data)
        self.assertIn(b"Image Model Suggestion", response.data)
        self.classifier_mock.assert_called_once()
        model_input = self.classifier_mock.call_args.args[0]
        self.assertTrue(os.path.isfile(model_input))
        self.assertTrue(model_input.startswith(self.test_upload_dir.name))
        self.assertNotEqual(model_input, "IMG_20261010_123456.png")

    def test_prediction_uses_saved_pixels_not_original_filename(self):
        self.classifier_mock.return_value = {"recognized": True, "category_id": "glass"}
        results = []
        for filename in ("glass_jar.png", "IMG_00042.png"):
            response = self.client.post("/analyze", data={
                "waste_image": (io.BytesIO(self._png_bytes()), filename),
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Glass Bottles &amp; Jars", response.data)
            results.append(self.classifier_mock.call_args.args[0])
        self.assertNotEqual(results[0], results[1])
        self.assertTrue(all(os.path.isfile(path) for path in results))

    def test_all_five_model_categories_precede_conflicting_keywords(self):
        cases = (
            ("plastic", "banana_peel.png"),
            ("paper", "glass_jar.png"),
            ("glass", "metal_can.png"),
            ("metal", "paper_box.png"),
            ("organic", "plastic_bottle.png"),
        )
        for category_id, conflicting_filename in cases:
            with self.subTest(category=category_id):
                self.classifier_mock.return_value = {
                    "recognized": True,
                    "category_id": category_id,
                }
                response = self.client.post("/analyze", data={
                    "waste_image": (io.BytesIO(self._png_bytes()), conflicting_filename),
                })
                self.assertEqual(response.status_code, 200)
                expected_name = html.escape(waste_data.WASTE_CATEGORIES[category_id]["name_en"]).encode()
                self.assertIn(expected_name, response.data)
                self.assertIn(b"Image Model Suggestion", response.data)

    def test_classifier_maps_model_outputs_to_all_five_categories(self):
        import numpy as np

        mapping = ai_classifier._build_waste_mapping()
        class_indices = {
            "plastic": 898,
            "paper": 478,
            "glass": 907,
            "metal": 738,
            "organic": 954,
        }

        class FakeSession:
            def __init__(self, logits):
                self.logits = logits

            @staticmethod
            def get_inputs():
                return [type("Input", (), {"name": "pixels"})()]

            def run(self, _outputs, _inputs):
                return [self.logits]

        for expected_category, class_index in class_indices.items():
            with self.subTest(category=expected_category):
                logits = np.full((1, 1000), -20, dtype=np.float32)
                logits[0, class_index] = 20
                with patch.object(ai_classifier, "_SESSION", FakeSession(logits)), \
                     patch.object(ai_classifier, "_MAPPING", mapping), \
                     patch.object(ai_classifier, "_CLASSES", ["n00000000 object"] * 1000), \
                     patch.object(ai_classifier, "preprocess_image", return_value="pixels"), \
                     patch.object(ai_classifier, "predict_waste_image", self.classifier_patch.temp_original):
                    result = ai_classifier.predict_waste_image("unused-image-path")
                self.assertTrue(result["recognized"], result)
                self.assertEqual(result["category_id"], expected_category)

    def test_top_ranked_mapped_label_is_suggested_without_uncalibrated_cutoff(self):
        import numpy as np

        mapping = ai_classifier._build_waste_mapping()
        class FakeSession:
            @staticmethod
            def get_inputs():
                return [type("Input", (), {"name": "pixels"})()]

            @staticmethod
            def run(_outputs, _inputs):
                probabilities = np.full(1000, 0.651 / 997, dtype=np.float32)
                probabilities[549] = 0.132  # ImageNet's Envelope class maps to paper.
                probabilities[591] = 0.115
                probabilities[465] = 0.102
                return [np.log(probabilities)[None, :]]

        with patch.object(ai_classifier, "_SESSION", FakeSession()), \
             patch.object(ai_classifier, "_MAPPING", mapping), \
             patch.object(ai_classifier, "_CLASSES", ["n00000000 object"] * 1000), \
             patch.object(ai_classifier, "preprocess_image", return_value="pixels"), \
             patch.object(ai_classifier, "predict_waste_image", self.classifier_patch.temp_original):
            result = ai_classifier.predict_waste_image("unused-image-path")

        self.assertTrue(result["recognized"], result)
        self.assertEqual(result["category_id"], "paper")
        self.assertAlmostEqual(result["confidence_percent"], 13.2, places=1)
    def test_unavailable_and_uncertain_model_results_stay_unknown(self):
        for model_result, expected_message in (
            ({"recognized": False, "is_ai": False}, b"local image model is unavailable"),
            ({"recognized": False, "is_ai": True}, b"sufficiently supported category suggestion"),
        ):
            with self.subTest(is_ai=model_result["is_ai"]):
                self.classifier_mock.return_value = model_result
                response = self.client.post("/analyze", data={
                    "waste_image": (io.BytesIO(self._png_bytes()), "IMG_20261020_0042.png"),
                })
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"Unknown Material", response.data)
                self.assertIn(expected_message, response.data)

    def test_real_model_smoke_on_available_banana_image(self):
        """Smoke-test genuine pixel inference when local model assets are installed."""
        sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_assets", "banana.jpg")
        if not os.path.isfile(sample_path) or os.path.getsize(sample_path) == 0:
            self.skipTest("A non-empty representative image fixture is unavailable")

        # setUp mocks the route's classifier; use the saved original for this real smoke test.
        result = self.classifier_patch.temp_original(sample_path)
        if not result.get("is_ai"):
            self.skipTest("The local ONNX model or its runtime dependencies are unavailable")
        self.assertTrue(result["recognized"], result)
        self.assertEqual(result["category_id"], "organic")
        self.assertEqual(result["detected_item"], "Organic / Kitchen Waste")
        self.assertIn("waste-trained", result["model_name"].lower())

    def test_waste_model_classifies_real_banana_photo_without_filename_hint(self):
        sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_assets", "banana.jpg")
        if not os.path.isfile(sample_path) or not os.path.getsize(sample_path):
            self.skipTest("Representative banana image is unavailable")
        original = self.classifier_patch.temp_original
        with patch.object(flask_app.ai_classifier, "predict_waste_image", original):
            # Route inference uses the saved image and ignores the generic filename.
            with open(sample_path, "rb") as image_file:
                response = self.client.post("/analyze", data={
                    "waste_image": (io.BytesIO(image_file.read()), "IMG_20261020_0043.jpg"),
                })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Organic &amp; Kitchen Waste", response.data)
        self.assertIn(b"Waste-trained MobileNetV2", response.data)

    def test_low_resolution_photo_is_not_confidently_misclassified(self):
        import numpy as np
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads",
                            "waste_15785ba0c2644f3b8998cf48f01c72df_banana_peel.jpg")
        if not os.path.isfile(path):
            self.skipTest("Low-resolution fixture is unavailable")
        result = self.classifier_patch.temp_original(path)
        self.assertFalse(result["recognized"])
        self.assertEqual(result["detected_item"], "Photo Too Small")
    def test_classifier_unavailable_fails_closed(self):
        with patch.object(ai_classifier, "load_waste_model", return_value=False), \
             patch.object(ai_classifier, "is_model_available", return_value=False):
            result = ai_classifier.predict_waste_image("unused-image-path")
        self.assertFalse(result["recognized"])
        self.assertIsNone(result["category_id"])

    def test_manual_category_selection_shows_only_its_own_guides(self):
        for category_id, other_category in (("paper", "organic"), ("organic", "metal"),
                                             ("metal", "glass"), ("glass", "plastic"),
                                             ("plastic", "paper")):
            response = self.client.post("/analyze", data={
                "category": category_id,
                "item_description": "Generic item",
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"User-Selected &amp; Confirmed", response.data)
            for project in waste_data.WASTE_CATEGORIES[category_id]["upcycling_projects"]:
                self.assertIn(html.escape(project["title_en"]).encode(), response.data)
            for project in waste_data.WASTE_CATEGORIES[other_category]["upcycling_projects"]:
                self.assertNotIn(html.escape(project["title_en"]).encode(), response.data)

    def test_invalid_manual_category_is_rejected_even_with_matching_filename(self):
        response = self.client.post("/analyze", data={
            "category": "wood",
            "waste_image": (io.BytesIO(self._png_bytes()), "banana_peel.png"),
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please choose one of the five supported", response.data)
        self.assertNotIn(b"User-Selected &amp; Confirmed", response.data)

    @staticmethod
    def _png_bytes():
        buffer = io.BytesIO()
        Image.new("RGB", (20, 20), color="green").save(buffer, format="PNG")
        return buffer.getvalue()

    def test_filename_keyword_suggestion_is_explicit_and_generic_name_stays_unknown(self):
        keyword = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(self._png_bytes()), "banana_peel.png"),
        })
        generic = self.client.post("/analyze", data={
            "waste_image": (io.BytesIO(self._png_bytes()), "Screenshot.png"),
        })
        self.assertIn(b"Organic &amp; Kitchen Waste", keyword.data)
        self.assertIn(b"Filename Heuristic", keyword.data)
        self.assertIn(b"Unknown Material", generic.data)

    def test_tamil_keyword_detection(self):
        """Verify keyword heuristic detection accurately resolves Tamil waste terms."""
        self.assertEqual(waste_data.detect_category_from_keywords("பாட்டில்"), "plastic")
        self.assertEqual(waste_data.detect_category_from_keywords("கண்ணாடி ஜாடி"), "glass")
        self.assertEqual(waste_data.detect_category_from_keywords("செய்தித்தாள்"), "paper")
        self.assertEqual(waste_data.detect_category_from_keywords("காய்கறி கழிவு"), "organic")
        self.assertEqual(waste_data.detect_category_from_keywords("தகர டப்பா"), "metal")

    def test_green_impact_points_and_stats(self):
        """Verify Green Impact Points are correctly awarded, stored, and calculated in stats."""
        init_stats = database.get_sustainability_stats()
        initial_points = init_stats["total_points"]
        initial_items = init_stats["total_diverted"]

        # Log an activity with specific points (60 points)
        row_id = database.log_activity(
            category="plastic",
            item_name="2L Soda Bottle Unique Test",
            project_name="Hanging Eco Bird Feeder",
            impact_points=60,
            notes="Points verification test"
        )
        self.assertIsNotNone(row_id)

        # Check that stats accurately computed the additional points and items
        new_stats = database.get_sustainability_stats()
        self.assertEqual(new_stats["total_points"], initial_points + 60)
        self.assertEqual(new_stats["total_diverted"], initial_items + 1)

        # Clean up test row
        deleted = database.delete_activity(row_id)
        self.assertTrue(deleted)

    def test_duplicate_submission_prevention(self):
        """Verify accidental duplicate submissions are blocked from awarding double points."""
        # First submission via API -> Should succeed and award 45 points
        project_name = waste_data.WASTE_CATEGORIES["metal"]["upcycling_projects"][0]["title_en"]
        project_points = waste_data.WASTE_CATEGORIES["metal"]["upcycling_projects"][0]["points"]
        response1 = self.client.post("/api/log-activity", data={
            "category": "metal",
            "item_name": "Test Baked Bean Can",
            "project_name": project_name,
            "impact_points": 1,
            "notes": "First attempt"
        })
        self.assertEqual(response1.status_code, 200)
        data1 = response1.get_json()
        self.assertTrue(data1["success"])
        self.assertEqual(data1["points_earned"], project_points)
        row_id = data1["id"]

        # Second submission with identical item & project immediately -> Should be rejected with HTTP 409
        response2 = self.client.post("/api/log-activity", data={
            "category": "metal",
            "item_name": "Test Baked Bean Can",
            "project_name": project_name,
            "impact_points": 1,
            "notes": "Accidental duplicate click"
        })
        self.assertEqual(response2.status_code, 409)
        data2 = response2.get_json()
        self.assertFalse(data2["success"])
        self.assertTrue(data2.get("duplicate"))
        self.assertIn("already recorded recently", data2["message"])

        # Clean up
        database.delete_activity(row_id)

    def test_dashboard_displays_points_and_completed_activities(self):
        """Verify dashboard displays Green Impact Points and activities table columns."""
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Gamification Points", response.data)
        self.assertIn(b"Logged Activities", response.data)
        self.assertIn(b"Impact Points", response.data)

    def test_analysis_page_displays_all_three_upcycling_recommendations(self):
        """Verify analysis result page renders all 3 upcycling projects with materials, steps, and points."""
        categories = ["plastic", "paper", "glass", "metal", "organic"]
        for cat_id in categories:
            response = self.client.post("/analyze", data={
                "category": cat_id,
                "item_description": f"Test {cat_id} item"
            })
            self.assertEqual(response.status_code, 200)
            cat_data = waste_data.WASTE_CATEGORIES[cat_id]
            self.assertIn(html.escape(cat_data["name_ta"]).encode("utf-8"), response.data)
            for proj in cat_data["upcycling_projects"]:
                self.assertIn(html.escape(proj["title_en"]).encode("utf-8"), response.data)
                self.assertIn(html.escape(proj["title_ta"]).encode("utf-8"), response.data)
                # Verify points badge is present
                points_badge = f"+{proj['points']} Pts".encode("utf-8")
                self.assertIn(points_badge, response.data)

if __name__ == "__main__":
    unittest.main()
