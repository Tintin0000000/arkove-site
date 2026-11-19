import pathlib, re, subprocess, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD, WEB = ROOT / "build", ROOT / "web"
WEB.mkdir(exist_ok=True)

subprocess.run([
    "pandoc", str(BUILD / "book.md"),
    "-f", "markdown+fenced_divs+task_lists+pipe_tables+smart",
    "-t", "html5", "--section-divs", "--wrap=none",
    "-o", str(BUILD / "fragment.html"),
], check=True)

frag = (BUILD / "fragment.html").read_text(encoding="utf-8")

# --- Sommaire construit depuis les sections de niveau 1 et 2 ---
sec = re.compile(r'<section id="([^"]+)" class="level([12])">\s*<h([12])[^>]*>(.*?)</h\3>', re.S)
nodes = [(m.group(1), int(m.group(2)), re.sub(r"<[^>]+>", "", m.group(4)).strip())
         for m in sec.finditer(frag)]
if not nodes:
    raise SystemExit("aucune section détectée")

items, first_part = [], True
for sid, lvl, text in nodes:
    if lvl == 1:
        items.append(('part', sid, text))
        skip = first_part
        first_part = False
    else:
        if skip:
            continue
        items.append(('chap', sid, text))

def li(sid, text, part):
    m = re.match(r"^(\d+)\.\s+(.*)$", text)
    inner = (f'<span class="n">{m.group(1)}</span>{html.escape(m.group(2))}'
             if m else html.escape(text))
    return f'<li><a href="#{sid}" data-label="{html.escape(text)}">{inner}</a></li>'

toc_html = []
for kind, sid, text in items:
    if kind == 'part':
        toc_html.append(f'<li class="part"><a href="#{sid}" style="padding:0;border:0;'
                        f'font:inherit;color:inherit">{html.escape(text)}</a></li>')
    else:
        toc_html.append(li(sid, text, None))
toc = '<ol>' + "".join(toc_html) + '</ol>'

css = (BUILD / "web.css").read_text(encoding="utf-8")
js = (BUILD / "web.js").read_text(encoding="utf-8")

page = f"""<title>Argent Maîtrisé</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
{css}
</style>

<div id="progress"><i></i></div>

<div id="topbar">
  <button id="navbtn" class="iconbtn" aria-label="Ouvrir le sommaire">
    <svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    </svg>
  </button>
  <div class="now">Argent Maîtrisé</div>
</div>
<div id="scrim"></div>

<nav id="rail" aria-label="Sommaire">
  <div class="rail-head">
    <div class="mk">Guide pratique</div>
    <div class="tt">Argent<em>Maîtrisé</em></div>
  </div>
  <div id="toc">{toc}</div>
</nav>

<main>
  <div class="reader">
    <header class="hero">
      <div class="mk">Guide pratique · Débutant et intermédiaire</div>
      <h1>Argent<em>Maîtrisé</em></h1>
      <p class="sub">Du premier euro épargné au patrimoine qui travaille pour vous. Budget, épargne, investissement, enveloppes françaises, immobilier, fiscalité et transmission — avec les simulateurs pour appliquer chaque chapitre à vos propres chiffres.</p>
      <div class="chips">
        <span class="chip">32 chapitres</span>
        <span class="chip">5 simulateurs</span>
        <span class="chip">Plan 90 jours</span>
        <span class="chip">6 annexes</span>
      </div>
      <div class="rule"></div>
    </header>
{frag}
  </div>
  <div class="endnote">
    <strong>Argent Maîtrisé</strong> — document pédagogique et informatif. Il ne constitue ni un conseil en investissement personnalisé, ni un conseil fiscal ou juridique adapté à une situation individuelle. Tout investissement en actifs non garantis comporte un risque de perte en capital. Les taux, plafonds et barèmes cités sont susceptibles de modification : vérifiez-les à leur source officielle avant toute décision. Les simulateurs produisent des ordres de grandeur à partir des hypothèses que vous saisissez, non des projections.
  </div>
</main>

<script>
{js}
</script>
"""

out = WEB / "argent-maitrise.html"
out.write_text(page, encoding="utf-8")
print("page web :", out, "|", round(len(page) / 1024), "Ko |", len(items), "entrées de sommaire")
