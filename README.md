---
# 🎨 Face-Consistent Image Generator

A **Streamlit-based AI image generator** that produces **face-consistent images** using **Stable Diffusion 1.5 + IP-Adapter**.

The application generates different scenes while **preserving the identity of a reference face**.

The model loads **once and remains in GPU memory**, making repeated generations fast.
---

# ✨ Features

- 🎭 Face identity preservation using IP-Adapter
- 🧠 Stable Diffusion 1.5 image generation
- ⚡ GPU accelerated inference
- 🎛 Adjustable generation parameters
- 🔁 Model loaded once and reused
- 📦 Fully reproducible dependency installation using **uv lock file**
- 🐍 Portable **Python 3.10.6 included inside project**

---

# 🖥️ System Requirements

| Component | Requirement                        |
| --------- | ---------------------------------- |
| GPU       | NVIDIA GPU (8GB+ VRAM recommended) |
| RAM       | 8GB minimum                        |
| Storage   | ~10GB                              |
| OS        | Windows 10/11                      |

---

# 📂 Project Structure

```
Generator
│
├── models
│   ├── ip-adapter-sd15
│   └── sd15-realistic
│
├── python
│   └── python.exe
│
├── .gitignore
├── app.py
├── face_generator.py
├── model_download.py
├── pyproject.toml
└── uv.lock
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

Users must first download the project using **Git**.

```bash
git clone https://github.com/rohit-singh-git/Face-Consistent-Image-Generator.git
```

Move into the project directory:

```bash
cd Face-Consistent-Image-Generator
```

---

# 2️⃣ Install `uv`

This project uses **`uv` package manager** to install exact dependency versions.

Install `uv`:

### Windows (PowerShell)

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```
uv --version
```

---

# 3️⃣ Create Virtual Environment

The project already includes **Python 3.10.6** inside the `python` folder.

Create a virtual environment using it:

```
python\python.exe -m venv .venv
```

---

# 4️⃣ Activate Virtual Environment

### PowerShell

```
.venv\Scripts\Activate.ps1
```

### CMD

```
.venv\Scripts\activate
```

---

# 5️⃣ Install Dependencies

Install packages exactly as defined in `uv.lock`.

```
uv sync --frozen --index-strategy=unsafe-best-match
```

Explanation:

| Flag                                 | Purpose                               |
| ------------------------------------ | ------------------------------------- |
| `--frozen`                           | Install exact versions from `uv.lock` |
| `--index-strategy=unsafe-best-match` | Needed for CUDA PyTorch builds        |

---

Good idea 👍 Adding a **model download step** makes the project reproducible so users don't have to manually download the models.

You should place it **after Step 5 (Install Dependencies)**.
Here is the clean section you can add to your README.

---

# 6️⃣ Download Required Models

After installing dependencies, download the required models using the provided script.

Run:

```bash
python model_download.py
```

This script will automatically download the following models from Hugging Face:

```
models/
├── ip-adapter-sd15
│   └── IP-Adapter weights
│
└── sd15-realistic
    └── Stable Diffusion 1.5 Realistic Vision model
```

The download may take several minutes depending on your internet speed because the models are **several gigabytes in size**.

Once the download completes, the folder structure will look like this:

```
models
│
├── ip-adapter-sd15
│   ├── ip-adapter-full-face_sd15.bin
│   └── image_encoder
│
└── sd15-realistic
    ├── scheduler
    ├── text_encoder
    ├── tokenizer
    ├── unet
    ├── vae
    └── model_index.json
```

---

# 7️⃣ Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

✅ **Tip for users**

If model download fails due to network interruption, simply run the command again:

```bash
python model_download.py
```

The script will **resume downloading missing files automatically**.

---

# 🎮 Using the App

1️⃣ Enter **reference face path**

Example

```
my_face.jpg
```

2️⃣ Adjust generation settings

- IP Adapter strength
- Steps
- Guidance scale
- Image resolution

3️⃣ Click **Generate Image**

Generated images are saved in:

```
output/
```

---

# 🎛️ Recommended Settings

| Setting          | Value       |
| ---------------- | ----------- |
| Steps            | 40 – 100    |
| Guidance         | 7 – 8       |
| IP Adapter Scale | 0.60 – 0.75 |
| Resolution       | 512x512     |

Higher resolutions require **more GPU VRAM**.

---

# 🧠 How It Works

```
Reference Face
      │
      ▼
IP-Adapter
      │
      ▼
Stable Diffusion
      │
      ▼
Face-consistent image
```

IP-Adapter injects the **reference face embedding** into the diffusion pipeline so the identity stays consistent.

---

# 🧹 GPU Memory Behavior

When the model is loaded:

```
Load Model
```

It stays in GPU memory until the Streamlit server stops.

Stop server:

```
CTRL + C
```

---

# ⚠️ Troubleshooting

### GPU not detected

Run:

```
nvidia-smi
```

---

### Missing models

Ensure folders exist:

```
models/ip-adapter-sd15
models/sd15-realistic
```

---

# 🧾 Built With

- Streamlit
- PyTorch
- Stable Diffusion
- Diffusers

---

# 🤝 Contributions

Contributions are welcome!

If you are experienced with **computer vision, diffusion models, or face recognition**, you are encouraged to improve the **face-consistency logic** used in this project.

Possible areas of improvement include:

- Improving **identity preservation accuracy**
- Better **face embedding extraction**
- Enhancing **IP-Adapter integration**
- Reducing **identity drift across generations**
- Supporting **multiple reference images**

If you develop improvements that make the generated faces **more accurate or stable**, please consider submitting a **pull request**.

Your contributions can help make this project more reliable for everyone.

---

⭐ If you find this project useful, please consider **starring the repository** to support further development.

---
