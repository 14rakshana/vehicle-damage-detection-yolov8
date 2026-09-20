import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import time
from pathlib import Path

# ============================================================
# AI CAR DAMAGE DETECTION
# ============================================================

st.set_page_config(
    page_title="AI Car Damage Detection",
    page_icon="🚗",
    layout="wide"
)

# Model path
MODEL_PATH = Path(
    "runs/detect/runs/cardd_yolov8n/weights/best.pt"
)

# Load model
@st.cache_resource
def load_model():
    return YOLO(str(MODEL_PATH))


model = load_model()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.title("🚗 AI-Based Car Damage Detection")

st.markdown(
    """
    **Deep Learning based vehicle damage detection using YOLOv8**

    The system identifies visible vehicle damage and displays
    the damage category, confidence score and detected region.
    """
)

st.divider()

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.header("Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.25,
    step=0.05
)

st.sidebar.markdown("### Model")
st.sidebar.write("YOLOv8n")
st.sidebar.write("CarDD Dataset")
st.sidebar.write("6 Damage Classes")

# ------------------------------------------------------------
# Upload
# ------------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a vehicle image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Original Image
    # --------------------------------------------------------

    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    with st.spinner("Analyzing vehicle damage..."):

        image_array = np.array(image)

        start_time = time.perf_counter()

        results = model.predict(
            source=image_array,
            conf=confidence,
            verbose=False
        )

        inference_time = (
            time.perf_counter() - start_time
        ) * 1000

    result = results[0]

    # Annotated image
    annotated = result.plot()

    # --------------------------------------------------------
    # Detection Image
    # --------------------------------------------------------

    with col2:
        st.subheader("AI Detection Result")
        st.image(
            annotated,
            channels="BGR",
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    st.subheader("🔍 Detection Results")

    if result.boxes is not None and len(result.boxes) > 0:

        names = model.names

        detections = []

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence_score = float(box.conf[0])

            class_name = names[class_id]

            detections.append(
                {
                    "Damage Type": class_name.title(),
                    "Confidence": confidence_score
                }
            )

        # Display each detection
        for detection in detections:

            st.success(
                f"🔴 {detection['Damage Type']}  —  "
                f"{detection['Confidence'] * 100:.2f}%"
            )

        # Summary table
        st.subheader("Detection Summary")

        st.dataframe(
            detections,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No visible damage detected above the selected "
            "confidence threshold."
        )

    # --------------------------------------------------------
    # Performance
    # --------------------------------------------------------

    st.divider()

    st.subheader("⚡ Model Performance")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Inference Time",
            f"{inference_time:.1f} ms"
        )

    with c2:
        st.metric(
            "Confidence Threshold",
            f"{confidence:.2f}"
        )

    with c3:
        st.metric(
            "Model",
            "YOLOv8n"
        )

else:

    st.info(
        "👆 Upload a car image above to start damage detection."
    )

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.divider()

st.caption(
    "AI-Based Car Damage Detection | "
    "YOLOv8n + CarDD Dataset | "
    "Prototype for academic research"
)