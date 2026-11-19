import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
BUILD = ROOT / "build"

TITLE = "Argent Maîtrisé"
SUBTITLE = ("Du premier euro épargné au patrimoine qui travaille.<br>"
            "Le guide complet de la gestion de son argent — niveau débutant et intermédiaire.")

files = sorted(CONTENT.glob("*.md"))
if len(files) != 8:
    sys.exit(f"attendu 8 fichiers de contenu, trouvé {len(files)}")

book_md = "\n\n".join(f.read_text(encoding="utf-8").strip() for f in files)
(BUILD / "book.md").write_text(book_md, encoding="utf-8")

subprocess.run([
    "pandoc", str(BUILD / "book.md"),
    "-f", "markdown+fenced_divs+task_lists+pipe_tables+smart",
    "-t", "html5", "--standalone", "--section-divs",
    "--toc", "--toc-depth=2",
    "--template", str(BUILD / "template.html"),
    "--metadata", f"title={TITLE}",
    "-o", str(BUILD / "body.html"),
], check=True)

titlepage = f"""<div class="titlepage">
  <div class="tp-mark">Guide pratique</div>
  <h1 class="tp-title">{TITLE}</h1>
  <div class="tp-sub">{SUBTITLE}</div>
  <div class="tp-meta">
    Édition {__import__("datetime").date.today().year}<br>
    Document pédagogique — ne constitue pas un conseil en investissement personnalisé
  </div>
</div>"""

html = (BUILD / "body.html").read_text(encoding="utf-8")
assert "<!--TITLEPAGE-->" in html
(BUILD / "body.html").write_text(html.replace("<!--TITLEPAGE-->", titlepage), encoding="utf-8")

cover = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>{TITLE}</title>
<style>
  @page {{ size:6in 9in; margin:0; }}
  html,body {{ margin:0; padding:0; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  .cover {{
    width:6in; height:9in; background:#F7F8F6; color:#16202A;
    display:flex; flex-direction:column; justify-content:space-between;
    padding:0.95in 0.8in; position:relative; overflow:hidden;
    font-family:"Inter Display","Inter","Liberation Sans",sans-serif;
  }}
  .band {{
    position:absolute; left:0; right:0; top:0; height:0.34in; background:#0E6B5C;
  }}
  .top, .mid, .bot {{ position:relative; z-index:2; }}
  .mark {{ font-size:9pt; letter-spacing:0.32em; text-transform:uppercase; color:#0E6B5C; }}
  .rule {{ width:48px; height:3px; background:#0E6B5C; margin:0.28in 0 0.3in; }}
  h1 {{
    font-size:47pt; line-height:0.96; font-weight:800; letter-spacing:-0.038em;
    margin:0 0 0.26in; color:#16202A;
  }}
  h1 span {{ display:block; color:#0E6B5C; }}
  .sub {{ font-size:11.5pt; line-height:1.5; color:#3A4A57; max-width:3.9in; font-weight:400; }}
  .bot {{ font-size:8.6pt; line-height:1.75; color:#6B7A86; letter-spacing:0.02em; }}
  .bot .chips {{ display:flex; gap:0.14in; margin-bottom:0.26in; flex-wrap:wrap; }}
  .chip {{
    border:1px solid #9FC4BB; border-radius:999px;
    padding:0.055in 0.15in; font-size:8pt; color:#0E6B5C; letter-spacing:0.07em;
    text-transform:uppercase;
  }}
  .bot .line {{ height:1px; background:#D9E0E3; margin-bottom:0.2in; }}
</style></head>
<body><div class="cover">
  <div class="band"></div>
  <div class="top"><div class="mark">Guide pratique</div><div class="rule"></div></div>
  <div class="mid">
    <h1>Argent<span>Maîtrisé</span></h1>
    <div class="sub">Du premier euro épargné au patrimoine qui travaille pour vous.</div>
  </div>
  <div class="bot">
    <div class="chips">
      <span class="chip">Débutant</span><span class="chip">Intermédiaire</span>
      <span class="chip">31 chapitres</span><span class="chip">Plan 90 jours</span>
    </div>
    <div class="line"></div>
    Budget · Épargne · Investissement · PEA, assurance-vie, PER · Immobilier · Fiscalité · Transmission
  </div>
</div></body></html>"""
(BUILD / "cover.html").write_text(cover, encoding="utf-8")
print("assemblé :", (BUILD / "body.html").stat().st_size, "octets de HTML")
