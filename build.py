"""
Builds index.html from FixtureDB.db.

Usage:  python build.py
        python build.py path/to/FixtureDB.db

Needs only Python 3 (no extra packages). Put build.py, template.html and
FixtureDB.db in the same folder, run it, then upload the new index.html.
"""
import json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).parent
DB = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "FixtureDB.db"
TEMPLATE = HERE / "template.html"
OUT = HERE / "index.html"

TYPE_NAMES = {"led wash": "LED Wash", "pxl bar": "Pixel bar", "fx": "FX", "cyc": "Cyc",
              "softlight": "Softlight", "tube": "Tube", "scan": "Scan", "fresnel": "Fresnel"}
WHITE_ONLY = {"WW", "CW", "TW", "DTW", "WW/Amber", "CW/WW/Amber"}

def num(v):
    if v in ("", None):
        return None
    try:
        f = float(v)
        return int(f) if f.is_integer() else round(f, 2)
    except (TypeError, ValueError):
        return None

def txt(v):
    if v is None:
        return None
    v = str(v).strip()
    if v in ("", "NO DATA"):
        return None
    return "Proprietary" if v == "Proprietaer" else v

def source_family(s):
    s = (s or "").lower()
    if "laser" in s: return "Laser"
    if "led" in s: return "LED"
    if "tungsten" in s or "halogen" in s: return "Halogen"
    return "Discharge"

def mix_group(m):
    if not m or m == "none": return "None"
    if m.startswith("CMY"): return "CMY"
    if m == "Color Wheel": return "Colour wheel"
    if m in WHITE_ONLY: return "White only"
    if m == "UV": return "UV"
    return "Additive (RGB…)"

def main():
    if not DB.exists():
        sys.exit(f"Database not found: {DB}")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    fixtures = []
    for r in con.execute("SELECT * FROM fixture_specs ORDER BY manufacturer, model"):
        t = (r["fixture_type"] or "").strip().lower()
        mix = txt(r["color_mixing_system"])
        fs = r["has_framing_shutters"]
        dc = txt(r["data_connector"])
        modes = txt(r["dmx_channel_modes_csv"])
        f = {
            "id": r["fixture_id"], "mf": (r["manufacturer"] or "").strip(), "md": (r["model"] or "").strip(),
            "cat": "Moving" if r["category"] == "moving" else "Static",
            "ty": TYPE_NAMES.get(t, t.capitalize()),
            "kg": num(r["weight_kg"]), "h": num(r["height_mm"]), "w": num(r["width_mm"]), "d": num(r["depth_mm"]),
            "ip": txt(r["ip_rating"]), "pw": num(r["power_consumption_w_max"]),
            "vmin": num(r["voltage_min_v"]), "vmax": num(r["voltage_max_v"]),
            "src": txt(r["source_type"]), "sf": source_family(r["source_type"]), "sw": num(r["source_power_w"]),
            "lm": num(r["luminous_flux_lm"]), "z0": num(r["zoom_min_deg"]), "z1": num(r["zoom_max_deg"]),
            "mix": None if mix == "none" else mix, "mg": mix_group(mix),
            "fs": None if fs in ("", None) else int(fs),
            "iris": num(r["has_iris"]) or 0, "gobo": num(r["has_gobos"]) or 0,
            "pc": txt(r["power_connector"]), "dc": None if dc == "none" else dc,
            "pr": txt(r["protocols_csv"]), "modes": None if modes == "none" else modes,
        }
        fixtures.append({k: v for k, v in f.items() if v is not None})
    data = json.dumps(fixtures, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", data)
    OUT.write_text(html, encoding="utf-8")
    print(f"Done: {len(fixtures)} fixtures written to {OUT}")

if __name__ == "__main__":
    main()
