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
    width:6in; height:9in; background:#17140F; color:#F6F1E7;
    display:flex; flex-direction:column; justify-content:space-between;
    padding:0.95in 0.8in; position:relative; overflow:hidden;
    font-family:"Inter Display","Inter","Liberation Sans",sans-serif;
  }}
  .glow {{
    position:absolute; width:9in; height:9in; border-radius:50%;
    background:radial-gradient(circle, rgba(168,118,44,0.30) 0%, rgba(168,118,44,0.07) 42%, rgba(23,20,15,0) 68%);
    top:-3.2in; right:-3.6in;
  }}
  .grid {{
    position:absolute; inset:0;
    background-image:linear-gradient(rgba(201,169,120,0.032) 1px, transparent 1px);
    background-size:100% 0.42in;
  }}
  .top, .mid, .bot {{ position:relative; z-index:2; }}
  .mark {{ font-size:9pt; letter-spacing:0.34em; text-transform:uppercase; color:#C9A978; }}
  .rule {{ width:52px; height:3px; background:#A8762C; margin:0.3in 0 0.34in; }}
  h1 {{
    font-size:46pt; line-height:0.97; font-weight:800; letter-spacing:-0.035em;
    margin:0 0 0.26in; color:#FFFCF6;
  }}
  h1 span {{ display:block; color:#C9A978; }}
  .sub {{ font-size:11.5pt; line-height:1.5; color:#CFC6B5; max-width:4in; font-weight:400; }}
  .bot {{ font-size:8.6pt; line-height:1.75; color:#8E8472; letter-spacing:0.02em; }}
  .bot .chips {{ display:flex; gap:0.18in; margin-bottom:0.26in; flex-wrap:wrap; }}
  .chip {{
    border:1px solid rgba(201,169,120,0.42); border-radius:999px;
    padding:0.055in 0.16in; font-size:8pt; color:#C9A978; letter-spacing:0.07em;
    text-transform:uppercase;
  }}
</style></head>
<body><div class="cover">
  <div class="grid"></div><div class="glow"></div>
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
    Budget · Épargne · Investissement · PEA, assurance-vie, PER · Immobilier · Fiscalité · Transmission
  </div>
</div></body></html>"""
(BUILD / "cover.html").write_text(cover, encoding="utf-8")
print("assemblé :", (BUILD / "body.html").stat().st_size, "octets de HTML")
