from .classify import classify
from .suggest import suggest, colours_to_avoid, PALETTE
from .body_shape import advise


def _swatches(names):
    return [{"name": n, "hex": PALETTE[n][0]} for n in names]


def analyse_skin(image_path):
    r = classify(image_path)
    L, undertone = r["L"], r["undertone"]
    return {
        "tone": r["tone"],
        "group": r["group"],
        "undertone": undertone,
        "lab": {"L": r["L"], "a": r["a"], "b": r["b"]},
        "bold_colours": _swatches([c[0] for c in suggest(L, undertone, "contrast")]),
        "soft_colours": _swatches([c[0] for c in suggest(L, undertone, "soft")]),
        "lower_contrast": colours_to_avoid(L, undertone),
    }


def analyse_body(shoulder, bust, waist, hips):
    shape, rules = advise(shoulder, bust, waist, hips)
    return {"shape": shape, "advice": rules}