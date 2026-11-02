
import os

from helpers.utils import load_image, CACHED_DIR, THEME_DIR
from scripts.modifiers.insert_background import add_background
from scripts.modifiers.insert_vbucks import add_vbucks


def generate_icon_final_images(config):
    print("⏳ Generating Final Images with Icons...")

    # Ensure required directories exist
    os.makedirs(CACHED_DIR, exist_ok=True)

    output_dir = os.path.join(THEME_DIR, "icons")
    os.makedirs(output_dir, exist_ok=True)

    # Get cached images
    if not os.path.isdir(CACHED_DIR):
        print(f"❌ Error: Cache directory not found: {CACHED_DIR}")
        return

    cached_images = sorted(
        filename
        for filename in os.listdir(CACHED_DIR)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    )

    if not cached_images:
        print(
            f"❌ Error: No cached images found in {CACHED_DIR}. "
            "Please run the caching step first."
        )
        return

    # Generate final images
    for img_name in cached_images:
        cached_img_path = os.path.join(CACHED_DIR, img_name)

        try:
            cached_img = load_image(cached_img_path)

            if cached_img is None:
                raise ValueError("Image loader returned None")

            # Apply background
            modified_img = add_background(cached_img, config)

            # Apply V-Bucks
            modified_img = add_vbucks(modified_img, config)

            # Save final image
            output_path = os.path.join(output_dir, img_name)
            modified_img.save(output_path)

            print(f"✅ Saved final image to {output_path}")

        except Exception as e:
            print(f"❌ Failed to process {img_name}: {e}")
            raise

    print("✅ Final images generated successfully!")
