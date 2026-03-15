import os
from huggingface_hub import hf_hub_download

# ip-adapter-sd15 model download

os.makedirs("./models/ip-adapter-sd15/models/image_encoder/", exist_ok=True)

hf_hub_download(
    repo_id="h94/IP-Adapter",
    subfolder="models",
    filename="ip-adapter-full-face_sd15.bin",
    local_dir="./models/ip-adapter-sd15",
)

hf_hub_download(
    repo_id="h94/IP-Adapter",
    subfolder="models/image_encoder",
    filename="config.json",
    local_dir="./models/ip-adapter-sd15",
)

hf_hub_download(
    repo_id="h94/IP-Adapter",
    subfolder="models/image_encoder",
    filename="model.safetensors",
    local_dir="./models/ip-adapter-sd15",
)

# sd15-realistic model download

BASE_DIR = "./models/sd15-realistic/"
os.makedirs(f"{BASE_DIR}/scheduler", exist_ok=True)
os.makedirs(f"{BASE_DIR}/text_encoder", exist_ok=True)
os.makedirs(f"{BASE_DIR}/tokenizer", exist_ok=True)
os.makedirs(f"{BASE_DIR}/unet", exist_ok=True)
os.makedirs(f"{BASE_DIR}/vae", exist_ok=True)

REPO_ID = "SG161222/Realistic_Vision_V5.1_noVAE"  # change if needed

files = [
    # root
    ".gitattributes",
    "model_index.json",
    "README.md",
    "Realistic_Vision_V5.1.safetensors",
    "SG161222_Realistic_Vision_V5.1_noVAE.json",
    # scheduler
    "scheduler/scheduler_config.json",
    # text_encoder
    "text_encoder/config.json",
    "text_encoder/model.safetensors",
    # tokenizer
    "tokenizer/merges.txt",
    "tokenizer/special_tokens_map.json",
    "tokenizer/tokenizer_config.json",
    "tokenizer/vocab.json",
    # unet
    "unet/config.json",
    "unet/diffusion_pytorch_model.safetensors",
    # vae
    "vae/config.json",
    "vae/diffusion_pytorch_model.safetensors",
]

for file in files:
    hf_hub_download(
        repo_id=REPO_ID, filename=file, local_dir=BASE_DIR
    )

print("Download complete.")
