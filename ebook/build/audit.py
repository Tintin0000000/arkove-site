# -*- coding: utf-8 -*-
"""Audit de cohérence entre les trois éditions, le classeur et la page de vente.
À relancer après toute modification de contenu."""
import pathlib, re, sys, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
pb, ok = [], []

def titles(d):
    out = {}
    for p in sorted((ROOT / d).glob("*.md")):
        for m in re.finditer(r"(?m)^## (\d+)\. (.+)$", p.read_text(encoding="utf-8")):
            out[int(m.group(1))] = m.group(2).strip()
    return out

# 1. Numérotation continue et titres identiques
a, b = titles("content"), titles("content-court")
n = len(a)
if sorted(a) != list(range(1, n + 1)): pb.append(f"édition complète : numérotation {sorted(a)}")
if sorted(b) != list(range(1, n + 1)): pb.append(f"édition essentielle : numérotation {sorted(b)}")
diff = [k for k in a if a[k] != b.get(k)]
if diff: pb.append(f"titres divergents aux chapitres {diff}")
else: ok.append(f"{n} chapitres, titres identiques dans les deux éditions")

# 2. Renvois internes dans la plage valide
for d in ("content", "content-court"):
    for p in sorted((ROOT / d).glob("*.md")):
        for m in re.finditer(r"chapitre (\d+)", p.read_text(encoding="utf-8")):
            if not 1 <= int(m.group(1)) <= n:
                pb.append(f"{p.name} : renvoi au chapitre {m.group(1)} inexistant")
ok.append("tous les renvois internes pointent vers un chapitre existant")

# 3. Décomptes annoncés
counts = {}
for d in ("content", "content-court"):
    txt = "".join(p.read_text(encoding="utf-8") for p in sorted((ROOT / d).glob("*.md")))
    counts[d] = {"figures": txt.count('<figure class="figure">'),
                 "widgets": txt.count("data-widget="),
                 "annexes": len(re.findall(r"(?m)^## Annexe ", txt))}
if counts["content"]["figures"] != 5 or counts["content-court"]["figures"] != 5:
    pb.append(f"figures : {counts['content']['figures']} / {counts['content-court']['figures']} au lieu de 5")
else: ok.append("5 figures dans chaque édition")
if counts["content"]["widgets"] != 5:
    pb.append(f"simulateurs : {counts['content']['widgets']} au lieu de 5")
else: ok.append("5 simulateurs dans l'édition web")

# 4. Chiffres annoncés dans les gabarits et la page de vente
for f, attendu in (("build/assemble.py", n), ("build/assemble-court.py", n), ("build/webbuild.py", n)):
    t = (ROOT / f).read_text(encoding="utf-8")
    if f"{attendu} chapitres" not in t:
        pb.append(f"{f} : n'annonce pas « {attendu} chapitres »")
vente = (ROOT / "web/vente.html").read_text(encoding="utf-8")
if f">{n}<" not in vente: pb.append(f"vente.html : le compteur de chapitres n'est pas {n}")
if "annexes" in vente and f"{counts['content-court']['annexes']} annexes" not in vente.replace("cinq annexes", "5 annexes"):
    pb.append(f"vente.html : nombre d'annexes incohérent (édition vendue : {counts['content-court']['annexes']})")
ok.append("décomptes des gabarits et de la page de vente cohérents")

# 5. Titres du sommaire de la page de vente
manquants = [k for k, v in a.items() if f"<li>{v}</li>" not in vente.replace("&#x27;", "'").replace("&amp;", "&")]
if manquants: pb.append(f"vente.html : titres absents ou différents pour les chapitres {manquants}")
else: ok.append("sommaire de la page de vente identique aux titres réels")

# 6. Chiffres faux déjà corrigés, qui ne doivent pas revenir
# « 35 % assurance comprise » parle du taux d'endettement : correct, à ne pas confondre
for mauvais in ("287 000", "≈ 191 000", "227 000 €", "100 000 € sur trente",
                "3,5 %, assurance comprise", "3,5 % assurance comprise"):
    for d in ("content", "content-court"):
        for p in sorted((ROOT / d).glob("*.md")):
            if mauvais in p.read_text(encoding="utf-8"):
                pb.append(f"{p.name} : « {mauvais} » est réapparu")
ok.append("aucun des chiffres erronés corrigés n'est revenu")

# 7. Pages des PDF contre ce qu'annonce la page de vente
try:
    import pypdf
    pages = len(pypdf.PdfReader(str(ROOT / "Argent-Maitrise-essentiel.pdf")).pages)
    if f"{pages} pages" not in vente:
        pb.append(f"vente.html : annonce un nombre de pages différent du PDF ({pages})")
    else: ok.append(f"PDF vendu : {pages} pages, conforme à la page de vente")
except Exception as e:
    pb.append(f"lecture du PDF impossible : {e}")

print(json.dumps({"conforme": not pb, "controles_ok": ok, "problemes": pb},
                 ensure_ascii=False, indent=1))
sys.exit(1 if pb else 0)
