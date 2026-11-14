import os
import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from .skin_detect import get_skin_patches


def dominant_color(patch, k=3):
    """Most common colour cluster in a patch (BGR)."""
    pixels = patch.reshape(-1, 3).astype(np.float32)
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(pixels)
    counts = np.bincount(km.labels_)
    return km.cluster_centers_[counts.argmax()]


def to_lab(bgr):
    """Convert one BGR colour to standard LAB (L: 0-100, a/b: about -128 to 127)."""
    pixel = np.array([[bgr]]).round().astype(np.uint8)
    L, a, b = cv2.cvtColor(pixel, cv2.COLOR_BGR2LAB)[0][0]
    return L * 100 / 255, float(a) - 128, float(b) - 128


def analyze(image_path):
    patches, _ = get_skin_patches(image_path)
    colors = [dominant_color(p) for p in patches.values()]
    avg_bgr = np.mean(colors, axis=0)
    L, a, b = to_lab(avg_bgr)
    return {"L": round(L, 1), "a": round(a, 1), "b": round(b, 1)}


if __name__ == "__main__":
    folder = "data/test_images"
    rows = []
    for name in sorted(os.listdir(folder)):
        try:
            result = analyze(os.path.join(folder, name))
            result["image"] = name
            rows.append(result)
        except Exception as e:
            print(name, "SKIPPED:", e)

    df = pd.DataFrame(rows)[["image", "L", "a", "b"]]
    print(df.to_string(index=False))
    df.to_csv("data/output/skin_results.csv", index=False)