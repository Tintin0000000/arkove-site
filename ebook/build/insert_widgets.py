import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAN = [
    ("01-fondations.md", "L'essentiel du chapitre 3", ["precaution"]),
    ("01-fondations.md", "L'essentiel du chapitre 5", ["compound", "fees"]),
    ("04-portefeuille.md", "L'essentiel du chapitre 18", ["risk"]),
    ("05-optimiser.md", "L'essentiel du chapitre 25", ["cashflow"]),
]

for fname, marker, widgets in PLAN:
    p = ROOT / "content" / fname
    t = p.read_text(encoding="utf-8")
    if "data-widget" in t and marker in t and any(w in t for w in widgets):
        pass
    i = t.find(marker)
    if i < 0:
        sys.exit(f"marqueur introuvable: {marker} dans {fname}")
    j = t.find("\n:::", i)
    if j < 0:
        sys.exit(f"fin d'encadré introuvable après {marker}")
    end = j + len("\n:::")
    block = "".join(f'\n\n::: {{.widget data-widget="{w}"}}\n:::' for w in widgets)
    if t[end:end+len(block)] == block:
        continue
    t = t[:end] + block + t[end:]
    p.write_text(t, encoding="utf-8")
    print(f"{fname}: {', '.join(widgets)} après « {marker} »")
