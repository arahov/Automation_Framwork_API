import os
from PIL import Image

def create_simple_demo_gif(source_folder, output_path, duration_per_frame=3000):
    # 1. Collect and filter images
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(valid_extensions)]
    
    # Sort numerically (ensures '2' comes before '10')
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or 0))

    if not files:
        print(f"No images found in {source_folder}")
        return

    # 2. Process frames
    frames = []
    max_size = (1280, 1280) # Resizes to a standard HD-ish width for sharing
    
    for img_name in files:
        img_path = os.path.join(source_folder, img_name)
        img = Image.open(img_path).convert("RGB")
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        frames.append(img)

    # 3. Save to Desktop
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_per_frame,
        loop=0,
        optimize=True
    )
    print(f"Success! Clean GIF saved to: {output_path}")

# --- Configuration ---
SOURCE = r'C:\Users\araho\Pictures\Screenshots'
DESKTOP = os.path.join(os.environ['USERPROFILE'], 'Desktop')
OUTPUT = os.path.join(DESKTOP, 'clean_automation_demo.gif')

if __name__ == "__main__":
    create_simple_demo_gif(SOURCE, OUTPUT)