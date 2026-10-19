import os
import subprocess
import sys
from pathlib import Path

ARIA2C = "aria2c"
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    # 1. AnimateDiff Motion Adapter v1-5-2
    (
        "https://huggingface.co/guoyww/animatediff-motion-adapter-v1-5-2/resolve/main/config.json",
        MODELS_DIR / "animatediff-motion-adapter-v1-5-2",
        "config.json"
    ),
    (
        "https://huggingface.co/guoyww/animatediff-motion-adapter-v1-5-2/resolve/main/diffusion_pytorch_model.safetensors",
        MODELS_DIR / "animatediff-motion-adapter-v1-5-2",
        "diffusion_pytorch_model.safetensors"
    ),
    # 2. Stable Diffusion v1.5 (fp16 components for AnimateDiff)
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/model_index.json",
        MODELS_DIR / "stable-diffusion-v1-5",
        "model_index.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/scheduler/scheduler_config.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "scheduler",
        "scheduler_config.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/tokenizer/vocab.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "tokenizer",
        "vocab.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/tokenizer/merges.txt",
        MODELS_DIR / "stable-diffusion-v1-5" / "tokenizer",
        "merges.txt"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/tokenizer/special_tokens_map.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "tokenizer",
        "special_tokens_map.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/tokenizer/tokenizer_config.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "tokenizer",
        "tokenizer_config.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/text_encoder/config.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "text_encoder",
        "config.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/text_encoder/model.fp16.safetensors",
        MODELS_DIR / "stable-diffusion-v1-5" / "text_encoder",
        "model.fp16.safetensors"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/vae/config.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "vae",
        "config.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/vae/diffusion_pytorch_model.fp16.safetensors",
        MODELS_DIR / "stable-diffusion-v1-5" / "vae",
        "diffusion_pytorch_model.fp16.safetensors"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/unet/config.json",
        MODELS_DIR / "stable-diffusion-v1-5" / "unet",
        "config.json"
    ),
    (
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/unet/diffusion_pytorch_model.fp16.safetensors",
        MODELS_DIR / "stable-diffusion-v1-5" / "unet",
        "diffusion_pytorch_model.fp16.safetensors"
    ),
]

def main():
    print(f"Target directory: {MODELS_DIR}")
    for url, out_dir, filename in FILES:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / filename
        if target.exists() and target.stat().st_size > 0 and not (out_dir / f"{filename}.aria2").exists():
            print(f"[SKIP] {filename} already exists ({target.stat().st_size / 1024 / 1024:.2f} MB)")
            continue

        print(f"\n[DOWNLOAD] {filename} -> {out_dir}")
        cmd = [
            ARIA2C,
            "-x", "16",
            "-s", "16",
            "-k", "1M",
            "-c", # resume
            "--file-allocation=none",
            "-d", str(out_dir),
            "-o", filename,
            url
        ]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"Error downloading {filename}, code {res.returncode}")
            sys.exit(res.returncode)

    print("\nALL ANIMATEDIFF MODEL FILES DOWNLOADED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
