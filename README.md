# app.py
# AI Waste Intelligence Platform
# Streamlit-based end-to-end demo application

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import datetime
import random
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Waste Intelligence Platform", page_icon="♻️", layout="wide")

# ---------------- UTILS ----------------
WASTE_CLASSES = ["Plastic", "Organic", "Paper", "Metal", "Glass"]
RECOMMENDATIONS = {
    "Plastic": "Recycle – Clean and send to plastic recycling facility",
    "Organic": "Compost – Convert into manure or biogas",
    "Paper": "Recycle – Paper recycling or reuse",
    "Metal": "Recycle – High value recyclable material",
    "Glass": "Recycle – Send to glass recycling unit"
}

DATA_FILE = "waste_data.csv"


def initialize_data():
    try:
        pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "location", "waste_type", "fill_level"])
        df.to_csv(DATA_FILE, index=False)


def fake_image_classifier(image):
    """
    Simulated ML model (replace with real CNN later)
    """
    waste_type = random.choice(WASTE_CLASSES)
    fill_level = random.randint(20, 100)
    return waste_type, fill_level


def save_data(location, waste_type, fill_level):
    df = pd.read_csv(DATA_FILE)
    new_row = {
        "date": datetime.date.today(),
        "location": location,
        "waste_type": waste_type,
        "fill_level": fill_level
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# ---------------- APP ----------------
initialize_data()

st.title("♻️ AI Waste Intelligence Platform")
st.caption("Image-based waste detection • Hotspot prediction • Circular recommendations")

# ----------- IMAGE UPLOAD -----------
st.header("📷 Image-Based Waste Detection")

uploaded_file = st.file_uploader("Upload a waste image", type=["jpg", "png", "jpeg"])
location = st.text_input("Enter Location / Area", "Campus Zone A")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)

    if st.button("Analyze Waste"):
        with st.spinner("Analyzing using AI..."):
            waste_type, fill_level = fake_image_classifier(image)

        st.success("Analysis Complete")

        st.metric("Detected Waste Type", waste_type)
        st.metric("Bin Fill Level (%)", fill_level)

        st.info(f"💡 Recommendation: {RECOMMENDATIONS[waste_type]}")

        save_data(location, waste_type, fill_level)

# ----------- DASHBOARD -----------
st.header("📊 Waste Analytics Dashboard")

df = pd.read_csv(DATA_FILE)

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Waste Type Distribution")
        fig, ax = plt.subplots()
        df["waste_type"].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Average Fill Level")
        fig, ax = plt.subplots()
        df.groupby("waste_type")["fill_level"].mean().plot(kind="bar", ax=ax)
        st.pyplot(fig)

# ----------- HOTSPOT PREDICTION -----------
st.header("🔥 ML-Based Hotspot Prediction")

if not df.empty:
    hotspot = df.groupby("loca
