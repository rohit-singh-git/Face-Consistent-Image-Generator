import gc
import time
import os

import torch
from PIL import Image
from diffusers import StableDiffusionPipeline


class FaceGenerator:
    """Persistent face generation pipeline - loads models once"""

    def __init__(self, model_path, ip_adapter_scale=0.60):
        """
        Initialize the generator (do this once)

        Args:
            model_path: Path to SD1.5 model
            ip_adapter_scale: Face preservation strength (0.6-0.8)
                             0.6 = more creative freedom
                             0.8 = stronger face preservation
        """
        print("🔧 Loading models (one-time setup)...")

        # Clean memory first
        gc.collect()
        torch.cuda.empty_cache()

        # Load pipeline
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_path, torch_dtype=torch.float16, safety_checker=None
        ).to("cuda")

        # Load IP-Adapter for face preservation
        self.pipe.load_ip_adapter(
            "./models/ip-adapter-sd15",
            subfolder="models",
            weight_name="ip-adapter-full-face_sd15.bin",
        )

        # Track current scale manually
        self.current_scale = ip_adapter_scale
        self.pipe.set_ip_adapter_scale(self.current_scale)

        # Cache for reference face
        self.cached_ref_face = None
        self.cached_ref_path = None

        print("✅ Models loaded and ready!")

    def generate(
        self,
        ref_face_path,
        prompt,
        negative_prompt="",
        num_steps=40,
        guidance=7.5,
        ip_adapter_scale=None,  # Override default if needed
        seed=None,
        width=512,
        height=512,
    ):
        """
        Generate image with face consistency

        Args:
            ref_face_path: Path to reference face
            prompt: Scene description
            negative_prompt: Things to avoid
            num_steps: Quality (30-70, higher=better)
            guidance: Prompt strength (7-8 recommended)
            ip_adapter_scale: Override default face preservation
            seed: Random seed for reproducibility (None=random)
            width/height: Output dimensions (512 recommended)
        """

        # Load and cache reference face
        if self.cached_ref_path != ref_face_path:
            print(f"📸 Loading reference face: {ref_face_path}")
            self.cached_ref_face = (
                Image.open(ref_face_path).convert("RGB").resize((512, 512))
            )
            self.cached_ref_path = ref_face_path

        # Update IP-Adapter scale if specified
        if ip_adapter_scale is not None and ip_adapter_scale != self.current_scale:
            self.pipe.set_ip_adapter_scale(ip_adapter_scale)
            self.current_scale = ip_adapter_scale

        # Set seed for reproducibility
        if seed is not None:
            generator = torch.Generator(device="cuda").manual_seed(seed)
        else:
            generator = None

        print(f"🎨 Generating: {prompt[:50]}...")

        # Enhanced negative prompt for better quality
        full_negative = (
            f"{negative_prompt}, "
            "cartoon, anime, 3d render, cgi, painting, drawing, illustration, "
            "deformed face, blurry face, bad anatomy, ugly, distorted, "
            "low quality, blurry, grainy, watermark"
        ).strip(", ")

        # Generate
        result = self.pipe(
            prompt=f"{prompt}, high quality, detailed, professional photography, 8k uhd, sharp focus",
            negative_prompt=full_negative,
            ip_adapter_image=self.cached_ref_face,
            num_inference_steps=num_steps,
            guidance_scale=guidance,
            height=height,
            width=width,
            generator=generator,
        ).images[0]

        # Save with timestamp
        os.makedirs("output", exist_ok=True)
        output_path = f"./output/{time.time()}.png"
        result.save(output_path)
        print(f"✅ Saved to {output_path}")

        return result, output_path

    def batch_generate(self, ref_face_path, prompts_list, **kwargs):
        """
        Generate multiple images efficiently

        Args:
            ref_face_path: Reference face path
            prompts_list: List of (prompt, negative_prompt) tuples or just prompts
            **kwargs: Additional arguments passed to generate()
        """
        results = []

        for i, prompt_data in enumerate(prompts_list, 1):
            # Handle both tuple and string inputs
            if isinstance(prompt_data, tuple):
                prompt, neg_prompt = prompt_data
            else:
                prompt = prompt_data
                neg_prompt = kwargs.get("negative_prompt", "")
            print(f"\n--- Generating {i}/{len(prompts_list)} ---")

            result, path = self.generate(
                ref_face_path=ref_face_path,
                prompt=prompt,
                negative_prompt=neg_prompt,
                **{k: v for k, v in kwargs.items() if k != "negative_prompt"},
            )

            results.append((result, path))

        return results

    def cleanup(self):
        """Free GPU memory when done"""
        del self.pipe
        self.cached_ref_face = None
        gc.collect()
        torch.cuda.empty_cache()
        print("🧹 Cleaned up GPU memory")
