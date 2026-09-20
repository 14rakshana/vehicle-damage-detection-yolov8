import json
import shutil
from pathlib import Path

# ============================================================
# CarDD COCO -> YOLO Dataset Converter
# ============================================================

# Original CarDD dataset
CARDD_ROOT = Path(
    r"C:\Users\raksh\Downloads\CarDD_release\CarDD_release\CarDD_COCO"
)

# Our project dataset
OUTPUT_ROOT = Path("dataset")

# CarDD classes confirmed from your JSON
CLASSES = [
    "dent",
    "scratch",
    "crack",
    "glass shatter",
    "lamp broken",
    "tire flat"
]

CLASS_MAP = {name: i for i, name in enumerate(CLASSES)}

SPLITS = {
    "train": "train2017",
    "val": "val2017",
    "test": "test2017"
}


def convert_split(split_name, source_folder, json_name):

    print(f"\n========== {split_name.upper()} ==========")

    image_source = CARDD_ROOT / source_folder
    annotation_file = CARDD_ROOT / "annotations" / json_name

    image_output = OUTPUT_ROOT / "images" / split_name
    label_output = OUTPUT_ROOT / "labels" / split_name

    image_output.mkdir(parents=True, exist_ok=True)
    label_output.mkdir(parents=True, exist_ok=True)

    print("Reading:", annotation_file)

    with open(annotation_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    images = {img["id"]: img for img in data["images"]}

    categories = {
        cat["id"]: cat["name"]
        for cat in data["categories"]
    }

    annotations_by_image = {}

    for ann in data["annotations"]:
        image_id = ann["image_id"]
        annotations_by_image.setdefault(image_id, []).append(ann)

    converted = 0
    skipped = 0
    total_annotations = 0

    for image_id, image_info in images.items():

        filename = image_info["file_name"]
        width = image_info["width"]
        height = image_info["height"]

        source_image = image_source / filename
        destination_image = image_output / filename

        if not source_image.exists():
            skipped += 1
            continue

        # Copy image
        shutil.copy2(source_image, destination_image)

        label_file = label_output / (Path(filename).stem + ".txt")

        lines = []

        for ann in annotations_by_image.get(image_id, []):

            category_id = ann["category_id"]

            if category_id not in categories:
                continue

            class_name = categories[category_id]

            if class_name not in CLASS_MAP:
                continue

            class_id = CLASS_MAP[class_name]

            x, y, w, h = ann["bbox"]

            # COCO -> YOLO
            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height

            norm_width = w / width
            norm_height = h / height

            # Keep values valid
            x_center = max(0, min(1, x_center))
            y_center = max(0, min(1, y_center))
            norm_width = max(0, min(1, norm_width))
            norm_height = max(0, min(1, norm_height))

            lines.append(
                f"{class_id} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{norm_width:.6f} "
                f"{norm_height:.6f}"
            )

            total_annotations += 1

        with open(label_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        converted += 1

    print("Images converted:", converted)
    print("Images skipped:", skipped)
    print("Annotations converted:", total_annotations)


# ============================================================
# Convert all three splits
# ============================================================

for split, folder in SPLITS.items():

    json_file = f"instances_{folder}.json"

    convert_split(
        split,
        folder,
        json_file
    )


# ============================================================
# Create data.yaml
# ============================================================

yaml_file = OUTPUT_ROOT / "data.yaml"

yaml_content = f"""path: {OUTPUT_ROOT.resolve().as_posix()}
train: images/train
val: images/val
test: images/test

nc: {len(CLASSES)}

names:
"""

for i, name in enumerate(CLASSES):
    yaml_content += f"  {i}: {name}\n"

with open(yaml_file, "w", encoding="utf-8") as f:
    f.write(yaml_content)


print("\n======================================")
print("CONVERSION COMPLETE")
print("======================================")
print("Dataset:", OUTPUT_ROOT.resolve())
print("YAML:", yaml_file.resolve())

print("\nClasses:")
for i, name in enumerate(CLASSES):
    print(i, "->", name)