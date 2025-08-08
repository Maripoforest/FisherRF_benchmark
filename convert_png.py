# import os
# import json
# from pathlib import Path
# from PIL import Image

# # Paths
# image_dir = Path('./images')
# json_files = ['transforms_train.json', 'transforms_val.json', 'transforms_test.json']

# def convert_images_to_png():
#     print("Converting .jpg images to .png...")
#     for jpg_path in sorted(image_dir.glob("*.jpg")):
#         png_path = jpg_path.with_suffix(".png")
#         try:
#             with Image.open(jpg_path) as img:
#                 img.save(png_path)
#             print(f"Converted: {jpg_path.name} -> {png_path.name}")
#             jpg_path.unlink()
#         except Exception as e:
#             print(f"Failed to convert {jpg_path.name}: {e}")

# def strip_jpg_from_json(json_path):
#     print(f"Processing {json_path}...")
#     with open(json_path, 'r') as f:
#         data = json.load(f)

#     for frame in data.get("frames", []):
#         frame["file_path"] = frame["file_path"].replace(".jpg", "")

#     with open(json_path, 'w') as f:
#         json.dump(data, f, indent=2)
#     print(f"Updated: {json_path}")

# def main():
#     convert_images_to_png()
#     for json_file in json_files:
#         if Path(json_file).exists():
#             strip_jpg_from_json(json_file)
#         else:
#             print(f"Warning: {json_file} not found.")

# if __name__ == "__main__":
#     main()


import os
import json
from pathlib import Path
from PIL import Image

# === USER CONFIGURABLE VARIABLE ===
file_loc = Path("./dataset/fox")  # <- CHANGE this to your root folder
# ==================================

image_dir = file_loc / "images"
original_json_path = file_loc / "transforms.json"
split_jsons = {
    "train": file_loc / "transforms_train.json",
    "val": file_loc / "transforms_val.json",
    "test": file_loc / "transforms_test.json",
}

def convert_images_to_png():
    print("Converting .jpg images to .png...")
    for jpg_path in sorted(image_dir.glob("*.jpg")):
        png_path = jpg_path.with_suffix(".png")
        try:
            with Image.open(jpg_path) as img:
                img.save(png_path)
            jpg_path.unlink()
            print(f"✓ {jpg_path.name} -> {png_path.name}")
        except Exception as e:
            print(f"✗ Failed: {jpg_path.name} ({e})")

def split_transforms_and_save():
    print("Reading and splitting transforms.json...")
    with open(original_json_path, "r") as f:
        data = json.load(f)

    frames = data["frames"]
    total = len(frames)
    val_indices = set(range(0, total, 20))
    test_indices = set(range(10, total, 20))
    train_indices = [i for i in range(total) if i not in val_indices and i not in test_indices]

    splits = {
        "train": [frames[i] for i in train_indices],
        "val": [frames[i] for i in val_indices],
        "test": [frames[i] for i in test_indices],
    }

    for key in splits:
        new_data = {k: v for k, v in data.items() if k != "frames"}
        new_data["frames"] = []
        for frame in splits[key]:
            frame["file_path"] = frame["file_path"].replace(".jpg", "")
            new_data["frames"].append(frame)

        with open(split_jsons[key], "w") as f:
            json.dump(new_data, f, indent=2)
        print(f"✓ Wrote {split_jsons[key].name} with {len(splits[key])} frames")

def main():
    if not original_json_path.exists():
        print(f"Error: {original_json_path} not found.")
        return
    if not image_dir.exists():
        print(f"Error: {image_dir} not found.")
        return

    convert_images_to_png()
    split_transforms_and_save()
    print("✅ Dataset preparation complete.")

if __name__ == "__main__":
    main()
