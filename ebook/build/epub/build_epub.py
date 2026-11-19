# -*- coding: utf-8 -*-
"""Construit l'EPUB destiné à Amazon KDP depuis l'édition essentielle."""
import pathlib, re, subprocess, sys, json

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent

AUTEUR = "À COMPLÉTER — votre nom"   # <<< une seule ligne à changer
TITRE  = "Argent Maîtrisé"
STITRE = "Du premier euro épargné au patrimoine qui travaille pour vous"

md = "\n\n".join(p.read_text(encoding="utf-8").strip()
                 for p in sorted((ROOT / "content-court").glob("*.md")))

# 1. Les simulateurs n'existent que sur le web
md = re.sub(r'\n*::: \{\.widget[^}]*\}\n:::\n*', '\n\n', md)

# 2. Le classeur n'est pas livré avec l'achat Amazon : ne rien promettre qu'on ne donne pas
ancien = ("Le **classeur de calcul** fourni avec ce guide reprend les six outils des chapitres "
          "1, 2, 19, 26 et 30, formules déjà écrites : entrées et sorties, bilan patrimonial, "
          "suivi trimestriel, allocation, cash-flow locatif et plan 90 jours.")
nouveau = ("Les chapitres 1, 2, 19, 26 et 30 contiennent des tableaux à remplir : entrées et sorties, "
           "bilan patrimonial, allocation, cash-flow locatif et plan 90 jours. Recopiez-les dans un "
           "tableur ou sur papier — un guide lu sans être appliqué ne vaut rien.")
if ancien not in md:
    sys.exit("le paragraphe sur le classeur a changé : vérifier avant de publier sur Amazon")
md = md.replace(ancien, nouveau, 1)

# 3. Les SVG en ligne passent mal sur Kindle : on les remplace par les PNG rendus
figs = json.loads((HERE / "figs.json").read_text(encoding="utf-8"))
n = 0
def img(m):
    global n
    n += 1
    cap = figs[n - 1]["cap"]
    return (f'<figure class="figure"><img src="figure-{n}.png" alt="Figure {n}"/>'
            f'<figcaption>{cap}</figcaption></figure>')
md = re.sub(r'<figure class="figure">\s*<svg.*?</svg>\s*<figcaption>.*?</figcaption>\s*</figure>',
            img, md, flags=re.S)
if n != len(figs):
    sys.exit(f"{n} figures remplacées sur {len(figs)} attendues")

(HERE / "amazon.md").write_text(md, encoding="utf-8")

meta = HERE / "metadata.yaml"
meta.write_text(
    f'---\ntitle: "{TITRE}"\nsubtitle: "{STITRE}"\nauthor: "{AUTEUR}"\n'
    f'lang: fr-FR\npublisher: "{AUTEUR}"\n'
    f'description: "Guide pratique de finances personnelles : budget, épargne de précaution, '
    f'investissement, PEA, assurance-vie, PER, immobilier, fiscalité et transmission. '
    f'32 chapitres et un plan en 90 jours."\n---\n', encoding="utf-8")

out = ROOT / "Argent-Maitrise-kindle.epub"
subprocess.run([
    "pandoc", str(HERE / "amazon.md"), str(meta),
    "-f", "markdown+fenced_divs+task_lists+pipe_tables+smart",
    "-t", "epub3", "--toc", "--toc-depth=2", "--split-level=1",
    "--css", str(HERE / "style.css"),
    "--epub-cover-image", str(HERE / "couverture-kindle.png"),
    "--resource-path", f"{HERE / 'img'}:{HERE}",
    "-o", str(out),
], check=True)
print(f"EPUB écrit : {out.name}, {out.stat().st_size // 1024} Ko, {n} figures intégrées")
