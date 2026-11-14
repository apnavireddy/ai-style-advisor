import math
import os
import pandas as pd
from .skin_tone import analyze

# --- Undertone thresholds (hue angle in degrees). Starting values: tune with your data ---
COOL_MAX = 47   # below this = cool
WARM_MIN = 53   # above this = warm


def ita(L, b):
    """Individual Typology Angle, a standard dermatology measure of skin lightness."""
    return math.degrees(math.atan2(L - 50, b))


def skin_tone(L, b):
    angle = ita(L, b)
    if angle > 55:
        detail = "very light"
    elif angle > 41:
        detail = "light"
    elif angle > 28:
        detail = "intermediate"
    elif angle > 10:
        detail = "tan"
    elif angle > -30:
        detail = "brown"
    else:
        detail = "dark"

    if detail in ("very light", "light"):
        group = "fair"
    elif detail in ("intermediate", "tan"):
        group = "medium"
    else:
        group = "deep"
    return detail, group, round(angle, 1)


def undertone(a, b):
    hue = math.degrees(math.atan2(b, a))
    if hue < COOL_MAX:
        label = "cool"
    elif hue > WARM_MIN:
        label = "warm"
    else:
        label = "neutral"
    return label, round(hue, 1)


def classify(image_path):
    r = analyze(image_path)
    detail, group, ita_angle = skin_tone(r["L"], r["b"])
    under, hue = undertone(r["a"], r["b"])
    return {**r, "ITA": ita_angle, "tone": detail, "group": group,
            "hue": hue, "undertone": under}


if __name__ == "__main__":
    folder = "data/test_images"
    rows = []
    for name in sorted(os.listdir(folder)):
        try:
            res = classify(os.path.join(folder, name))
            res["image"] = name
            rows.append(res)
        except Exception as e:
            print(name, "SKIPPED:", e)

    df = pd.DataFrame(rows)[["image", "L", "a", "b", "ITA", "tone", "group", "hue", "undertone"]]
    print(df.to_string(index=False))
    os.makedirs("data/output", exist_ok=True)
    df.to_csv("data/output/classified.csv", index=False)