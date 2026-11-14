def classify_shape(shoulder, bust, waist, hips):
    """All values in the same unit (cm or inches). Returns a body shape label."""
    upper = max(shoulder, bust)

    if abs(upper - hips) <= 0.05 * hips:          # shoulders/bust and hips within 5%
        if waist <= 0.75 * min(upper, hips):
            return "hourglass"
        return "rectangle"
    if hips > upper:
        return "pear"
    if waist >= 0.9 * upper:
        return "apple"
    return "inverted triangle"


STYLE_RULES = {
    "hourglass": {
        "highlight": "your defined waist",
        "tops": "fitted or wrap tops, V-necks",
        "bottoms": "high-waisted skirts and trousers, pencil cuts",
        "dresses": "wrap, bodycon, belted styles",
        "avoid": "very boxy, shapeless cuts that hide the waist",
    },
    "pear": {
        "highlight": "balance by drawing attention to the upper body",
        "tops": "boat necks, structured shoulders, light colours or prints on top",
        "bottoms": "A-line skirts, straight or bootcut trousers, darker colours below",
        "dresses": "fit-and-flare, empire waist",
        "avoid": "heavy detail or very tight fits at the hips",
    },
    "apple": {
        "highlight": "your legs and neckline",
        "tops": "V-necks, empire-line or flowy tops, open jackets",
        "bottoms": "straight-leg trousers, mid-rise cuts",
        "dresses": "empire waist, A-line, wrap",
        "avoid": "clingy fabrics gathered at the waist",
    },
    "rectangle": {
        "highlight": "adding shape and curves",
        "tops": "ruffles, peplum, layered looks",
        "bottoms": "pleated or full skirts, paperbag waists",
        "dresses": "belted, wrap, tiered styles",
        "avoid": "straight, boxy cuts with no shaping",
    },
    "inverted triangle": {
        "highlight": "balance by adding volume below",
        "tops": "soft necklines, simple tops, avoid heavy shoulder detail",
        "bottoms": "A-line skirts, wide-leg trousers, patterns or lighter colours below",
        "dresses": "A-line, fit-and-flare",
        "avoid": "padded shoulders and very broad necklines",
    },
}


def advise(shoulder, bust, waist, hips):
    shape = classify_shape(shoulder, bust, waist, hips)
    return shape, STYLE_RULES[shape]


if __name__ == "__main__":
    shape, rules = advise(shoulder=96, bust=92, waist=72, hips=98)
    print("Shape:", shape)
    for key, value in rules.items():
        print(f"  {key}: {value}")