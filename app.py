import streamlit as st

from face_generator import FaceGenerator

# ---------------- CONFIG ----------------
MODEL_SD15 = "./models/sd15-realistic"

st.set_page_config(
    page_title="Face Consistent Image Generator",
    layout="wide"
)

st.title("🎨 Face-Consistent Image Generator (SD + IP-Adapter)")
st.caption("Model loads once • Reused until app is closed")

# ---------------- SESSION STATE ----------------
if "generator" not in st.session_state:
    st.session_state.generator = None


# ---------------- MODEL LOADING ----------------
@st.cache_resource(show_spinner=True)
def load_generator(model_path, scale):
    return FaceGenerator(
        model_path=model_path,
        ip_adapter_scale=scale
    )


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    ref_face = st.text_input("Reference Face Path", "my_face.jpg")

    ip_scale = st.slider(
        "IP-Adapter Face Strength",
        0.50, 0.85, 0.60, 0.01
    )

    steps = st.slider("Steps", 20, 150, 100)
    guidance = st.slider("Guidance Scale", 1.0, 10.0, 7.5)
    seed = st.number_input("Seed (0 = random)", min_value=0, value=0)

    width = st.selectbox("Width", [512, 640, 768], index=0)
    height = st.selectbox("Height", [512, 640, 768], index=0)

    load_btn = st.button("🚀 Load Model")

# ---------------- LOAD MODEL BUTTON ----------------
if load_btn:
    with st.spinner("Loading model (only once)..."):
        st.session_state.generator = load_generator(
            MODEL_SD15,
            ip_scale
        )
    st.success("✅ Model loaded and cached")

# ---------------- MAIN UI ----------------
prompt = st.text_area(
    "Prompt",
    height=120,
    value="Ultra-realistic cinematic portrait, natural lighting, professional photography"
)

negative_prompt = st.text_area(
    "Negative Prompt",
    height=90,
    value="cartoon, anime, illustration, painting, drawing, 3d render, cgi, deformed face, distorted face, asymmetrical face, mutated face, bad anatomy, bad proportions, extra limbs, extra fingers, missing fingers, cross-eyed, lazy eye, warped eyes, unnatural eyes blurry, out of focus, motion blur, low resolution, low quality, grainy, plastic skin, waxy skin, over-smoothed skin, fake texture harsh lighting, over exposed, under exposed watermark, logo, text, signature, jpeg artifact"
)

generate_btn = st.button("🎨 Generate Image")

# ---------------- GENERATION ----------------
if generate_btn:
    if st.session_state.generator is None:
        st.error("❌ Please load the model first")
    else:
        with st.spinner("Generating image..."):
            result, path = st.session_state.generator.generate(
                ref_face_path=ref_face,
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_steps=steps,
                guidance=guidance,
                ip_adapter_scale=ip_scale,
                seed=None if seed == 0 else int(seed),
                width=width,
                height=height
            )

        st.image(result, caption="Generated Image", width='stretch')
        st.success(f"Saved to {path}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("GPU memory stays allocated until Streamlit app is closed.")
