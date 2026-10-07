import streamlit as st
import requests

st.set_page_config(page_title="NutriLens", page_icon="🔬", layout="wide")
st.title("🔬 NutriLens — Autonomous Food Integrity Agent")
st.caption("Powered by Gemma 4 Multimodal Agent Skill (Open Standard)")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("1. Ingest Food Label")
    cloud_toggle = st.toggle("Force Cloud Inference (Gemma 4 API)", value=False)
    source = st.radio("Input Source", ["Upload Image", "Use Webcam"], horizontal=True)

    img_file = None
    if source == "Upload Image":
        img_file = st.file_uploader("Upload nutrition table photo", type=["jpg", "png", "jpeg"])
    else:
        img_file = st.camera_input("Capture live label")

    if img_file and st.button("Run Audit Inspection", type="primary", use_container_width=True):
        with st.spinner("Analyzing tokens and running verification..."):
            try:
                files = {"file": (img_file.name, img_file.getvalue(), "image/jpeg")}
                data = {"force_cloud": str(cloud_toggle).lower()}
                resp = requests.post("http://127.0.0.1:8000/api/audit", files=files, data=data, timeout=60)
                if resp.status_code == 200:
                    st.session_state["report"] = resp.json()
                else:
                    st.error(f"Backend returned error: {resp.text}")
            except Exception as e:
                st.error(f"Cannot connect to backend: {e}")

with c2:
    st.subheader("2. Compliance & Verification Report")
    if "report" in st.session_state:
        rep = st.session_state["report"]
        audit = rep["audit"]
        ext = rep["extracted"]

        score = audit["integrity_score"]
        st.metric("Claim Integrity Score", f"{score} / 100", delta=f"{score - 100} pts")

        if audit["deceptive_ingredients"]:
            st.error(f"⚠️ Deceptive High-GI Fillers Detected: {', '.join(audit['deceptive_ingredients'])}")
        else:
            st.success("✅ Clean Formulation: No hidden glycemic fillers detected.")

        st.markdown("#### Caloric Verification (Atwater Factor)")
        col_a, col_b = st.columns(2)
        col_a.metric("Declared Calories", f"{audit['declared_calories']} kcal")
        col_b.metric("Calculated Calories", f"{audit['calculated_calories']} kcal", delta=f"{audit['variance_percentage']}% var")

        st.markdown("#### Extracted Nutrients")
        st.json(ext)