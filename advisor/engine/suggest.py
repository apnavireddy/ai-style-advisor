import cv2
import numpy as np
from .classify import classify

# name: (hex colour, family)  -> family is warm / cool / any
PALETTE = {
    "mustard": ("#E1AD01", "warm"), "olive green": ("#6B7B3A", "warm"),
    "terracotta": ("#C8553D", "warm"), "coral": ("#FF7F6B", "warm"),
    "peach": ("#FFB38A", "warm"), "cream": ("#F5ECD7", "warm"),
    "rust": ("#B7410E", "warm"), "camel": ("#C19A6B", "warm"),
    "royal blue": ("#2F4DC6", "cool"), "emerald": ("#0F8A5F", "cool"),
    "plum": ("#6E2C6B", "cool"), "rose pink": ("#E0709A", "cool"),
    "lavender": ("#B9A7E0", "cool"), "navy": ("#1B2A5C", "cool"),
    "icy grey": ("#C9D1DB", "cool"),
    "white": ("#FFFFFF", "any"), "black": ("#111111", "any"),
    "teal": ("#127C8A", "any"), "charcoal": ("#3A3F47", "any"),
    "dusty rose": ("#C98B94", "any"),
}


def hex_to_L(hex_code):
    h = hex_code.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    pixel = np.array([[[b, g, r]]], dtype=np.uint8)
    return cv2.cvtColor(pixel, cv2.COLOR_BGR2LAB)[0][0][0] * 100 / 255


def suggest(L, undertone, style="contrast"):
    """style='contrast' -> colours far from skin lightness; 'soft' -> close to it."""
    allowed = {"warm": ["warm", "any"], "cool": ["cool", "any"],
               "neutral": ["warm", "cool", "any"]}[undertone]
    options = []
    for name, (hex_code, family) in PALETTE.items():
        if family in allowed:
            options.append((name, hex_code, round(abs(hex_to_L(hex_code) - L), 1)))
    options.sort(key=lambda x: -x[2] if style == "contrast" else x[2])
    return options[:5]


def colours_to_avoid(L, undertone):
    """Opposite-undertone colours closest in lightness to skin (likely to look washed out)."""
    if undertone == "neutral":
        return []
    opposite = "cool" if undertone == "warm" else "warm"
    options = [(name, round(abs(hex_to_L(h) - L), 1))
               for name, (h, fam) in PALETTE.items() if fam == opposite]
    options.sort(key=lambda x: x[1])
    return [name for name, _ in options[:3]]


if __name__ == "__main__":
    import os
    folder = "data/test_images"
    for name in sorted(os.listdir(folder)):
        try:
            r = classify(os.path.join(folder, name))
        except Exception:
            continue
        print(f"\n{name}: {r['group']} skin, {r['undertone']} undertone")
        print("  Bold:", [c[0] for c in suggest(r["L"], r["undertone"], "contrast")])
        print("  Soft:", [c[0] for c in suggest(r["L"], r["undertone"], "soft")])
        print("  Lower contrast:", colours_to_avoid(r["L"], r["undertone"]))