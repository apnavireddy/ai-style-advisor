import os
import cv2
from skin_detect import get_skin_patches

folder = "data/test_images"
os.makedirs("data/output", exist_ok=True)

for name in sorted(os.listdir(folder)):
    try:
        patches, marked = get_skin_patches(os.path.join(folder, name))
        cv2.imwrite(os.path.join("data/output", name), marked)
        print(name, "OK")
    except Exception as e:
        print(name, "FAILED:", e)