/**
 * GreenLoop AI - Client-side Interactions
 * Mobile nav, drag-and-drop preview, bilingual switch, SQLite activity logging.
 */

document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initImageUpload();
    initBilingualSwitch();
    initActivityLoggingModal();
});

/* -------------------------------------------------------------
 * 1. Mobile Navigation Toggle
 * ------------------------------------------------------------- */
function initNavigation() {
    const navToggle = document.getElementById("navToggle");
    const mainNav = document.getElementById("mainNav");

    if (navToggle && mainNav) {
        navToggle.addEventListener("click", () => {
            mainNav.classList.toggle("active");
            const isOpen = mainNav.classList.contains("active");
            navToggle.innerHTML = isOpen 
                ? '<i class="fa-solid fa-xmark"></i>' 
                : '<i class="fa-solid fa-bars"></i>';
        });

        // Close nav on clicking outside or clicking any nav link
        document.querySelectorAll(".nav-link").forEach(link => {
            link.addEventListener("click", () => {
                if (mainNav.classList.contains("active")) {
                    mainNav.classList.remove("active");
                    navToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
                }
            });
        });
    }
}

/* -------------------------------------------------------------
 * 2. Waste Photo Drag-and-Drop & Instant Preview
 * ------------------------------------------------------------- */
function initImageUpload() {
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("fileInput");
    const dropzonePrompt = document.getElementById("dropzonePrompt");
    const previewContainer = document.getElementById("previewContainer");
    const imagePreview = document.getElementById("imagePreview");
    const removeImageBtn = document.getElementById("removeImageBtn");

    if (!dropzone || !fileInput) return;

    // Drag-and-drop hover effects
    ["dragenter", "dragover"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove("dragover");
        });
    });

    // Handle dropped files
    dropzone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            fileInput.files = files;
            displayPreview(files[0]);
        }
    });

    // Handle file selection from dialog
    fileInput.addEventListener("change", () => {
        if (fileInput.files && fileInput.files[0]) {
            displayPreview(fileInput.files[0]);
        }
    });

    async function displayPreview(file) {
        // Validate file type
        const validTypes = ["image/jpeg", "image/png", "image/jpg", "image/webp"];
        if (!validTypes.includes(file.type)) {
            showToast("Please upload a valid image file (JPG, PNG, or WEBP).", "error");
            clearPreview();
            return;
        }

        // Keep the browser limit aligned with Flask's upload limit.
        if (file.size > 32 * 1024 * 1024) {
            showToast("File size exceeds 32MB limit. Please choose a smaller photo.", "error");
            clearPreview();
            return;
        }

        // Reject truly oversized pixel dimensions before reading a large file
        // into a data URL. The server repeats this check as the source of truth.
        if (typeof createImageBitmap === "function") {
            try {
                const bitmap = await createImageBitmap(file);
                const megapixels = bitmap.width * bitmap.height;
                bitmap.close();
                if (megapixels > 60_000_000) {
                    showToast("Image dimensions are too large. Please upload an image under 60 megapixels.", "error");
                    clearPreview();
                    return;
                }
            } catch (error) {
                // Let the server validate formats browsers cannot decode here.
            }
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            dropzonePrompt.classList.add("hidden");
            previewContainer.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
    }

    function clearPreview() {
        fileInput.value = "";
        imagePreview.src = "#";
        previewContainer.classList.add("hidden");
        dropzonePrompt.classList.remove("hidden");
    }

    if (removeImageBtn) {
        removeImageBtn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            clearPreview();
        });
    }
}

/* -------------------------------------------------------------
 * 3. Bilingual Instructions Toggle (English <-> Tamil)
 * ------------------------------------------------------------- */
function initBilingualSwitch() {
    const langBtnEn = document.getElementById("langBtnEn");
    const langBtnTa = document.getElementById("langBtnTa");

    if (!langBtnEn || !langBtnTa) return;

    function switchLanguage(targetLang) {
        const enElements = document.querySelectorAll(".lang-content.lang-en");
        const taElements = document.querySelectorAll(".lang-content.lang-ta");

        if (targetLang === "ta") {
            enElements.forEach(el => el.classList.add("hidden"));
            taElements.forEach(el => el.classList.remove("hidden"));
            langBtnTa.classList.add("active");
            langBtnEn.classList.remove("active");
        } else {
            taElements.forEach(el => el.classList.add("hidden"));
            enElements.forEach(el => el.classList.remove("hidden"));
            langBtnEn.classList.add("active");
            langBtnTa.classList.remove("active");
        }
    }

    langBtnEn.addEventListener("click", () => switchLanguage("en"));
    langBtnTa.addEventListener("click", () => switchLanguage("ta"));
}

/* -------------------------------------------------------------
 * 4. Modal & Asynchronous Activity Logging (SQLite)
 * ------------------------------------------------------------- */
function initActivityLoggingModal() {
    const modal = document.getElementById("logActivityModal");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const cancelModalBtn = document.getElementById("cancelModalBtn");
    const logForm = document.getElementById("activityLogForm");
    const modalItemName = document.getElementById("modalItemName");
    const modalProjectName = document.getElementById("modalProjectName");
    const modalCategory = document.getElementById("modalCategory");
    const modalImagePath = document.getElementById("modalImagePath");
    const modalPoints = document.getElementById("modalPoints");
    const modalPointsDisplay = document.getElementById("modalPointsDisplay");

    if (!modal || !logForm) return;

    // Attach click listener to all "I Made This!" buttons
    document.querySelectorAll(".log-trigger-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const category = btn.getAttribute("data-category");
            const item = btn.getAttribute("data-item");
            const project = btn.getAttribute("data-project");
            const points = btn.getAttribute("data-points") || "50";
            const image = btn.getAttribute("data-image");

            if (modalCategory) modalCategory.value = category || "plastic";
            if (modalItemName) modalItemName.value = item || "";
            if (modalProjectName) modalProjectName.value = project || "";
            if (modalImagePath) modalImagePath.value = image || "";
            if (modalPoints) modalPoints.value = points;
            if (modalPointsDisplay) modalPointsDisplay.innerText = points;

            modal.classList.remove("hidden");
        });
    });

    const closeModal = () => modal.classList.add("hidden");
    if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
    if (cancelModalBtn) cancelModalBtn.addEventListener("click", closeModal);

    // Close on clicking backdrop
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });

    // Form submission via AJAX
    logForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById("saveActivityBtn");
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

        const formData = new FormData(logForm);

        try {
            const response = await fetch("/api/log-activity", {
                method: "POST",
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                const pts = data.points_earned || 50;
                showToast(`Great job! Earned +${pts} Green Impact Points. Recorded to your Dashboard.`, "success", "/dashboard", "View Dashboard &rarr;");
                closeModal();
                logForm.reset();
            } else if (data.duplicate) {
                showToast(data.message, "warning", "/dashboard", "View in Dashboard &rarr;");
                closeModal();
            } else {
                showToast(data.message || "Failed to log activity.", "error");
            }
        } catch (err) {
            console.error("Logging error:", err);
            showToast("Server connection error while saving activity.", "error");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save to Dashboard';
        }
    });
}

/* -------------------------------------------------------------
 * 5. Delete Activity Function (for Dashboard)
 * ------------------------------------------------------------- */
window.deleteActivity = async function(activityId) {
    if (!confirm("Are you sure you want to remove this record from the activity log?")) {
        return;
    }

    try {
        const response = await fetch(`/api/delete-activity/${activityId}`, {
            method: "POST"
        });
        const data = await response.json();

        if (data.success) {
            showToast("Activity record deleted successfully.", "success");
            // Recompute all dashboard totals, category shares, points, and milestones.
            setTimeout(() => window.location.reload(), 350);
        } else {
            showToast(data.message || "Failed to delete activity.", "error");
        }
    } catch (err) {
        console.error("Delete error:", err);
        showToast("Error connecting to server to delete record.", "error");
    }
};

/* -------------------------------------------------------------
 * 6. Toast Notification Helper
 * ------------------------------------------------------------- */
function showToast(message, type = "success", linkUrl = null, linkText = null) {
    let container = document.getElementById("toastContainer");
    if (!container) {
        container = document.createElement("div");
        container.id = "toastContainer";
        container.className = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    
    const icon = type === "success" 
        ? '<i class="fa-solid fa-circle-check"></i>' 
        : '<i class="fa-solid fa-circle-exclamation"></i>';

    const iconEl = document.createElement("span");
    iconEl.innerHTML = icon;
    const messageEl = document.createElement("span");
    messageEl.textContent = message;
    toast.append(iconEl.firstElementChild, messageEl);
    if (linkUrl && linkText) {
        const linkEl = document.createElement("a");
        linkEl.href = linkUrl;
        linkEl.className = "toast-link";
        linkEl.textContent = linkText;
        toast.appendChild(linkEl);
    }
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(100%)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 4500);
}

