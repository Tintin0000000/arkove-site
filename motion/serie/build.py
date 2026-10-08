#!/usr/bin/env python3
"""
Série « Épargne malin » : assemble les épisodes.

    python3 serie/build.py              # écrit serie/epNN.html et serie/PUBLICATION.md
    python3 serie/build.py --tout       # + voix (voiceover.py --prises 4) + vidéos MP4

Un épisode = serie/epNN.json : script de la voix off (« sentences »), visuels
(« blocks », un par segment) et texte de publication (« post »).
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Épargne malin · ép. {num} · {title}</title>
  <link rel="stylesheet" href="../motion.css">
  <link rel="stylesheet" href="serie.css">
</head>
<body>
  <div class="frame"><div id="stage"><div class="gridbg"></div><div class="grain" style="z-index:6"></div><div class="vignette" style="z-index:6"></div></div></div>
  <script>window.EP = {ep};</script>
  <script src="{stem}-timeline.js"></script>
  <script src="../engine.js"></script>
  <script src="serie.js"></script>
</body>
</html>
"""


def episodes():
    return sorted(HERE.glob("ep[0-9][0-9].json"))


def build():
    posts = []
    for path in episodes():
        e = json.loads(path.read_text(encoding="utf-8"))
        visual = {k: e.get(k) for k in ("ep", "title", "short", "handle", "next", "blocks", "shakes")}
        (HERE / f"{path.stem}.html").write_text(PAGE.format(
            num=f"{e['ep']:02d}", title=e["title"], stem=path.stem,
            ep=json.dumps(visual, ensure_ascii=False)), encoding="utf-8")
        posts.append(e)
    write_publication(posts)
    print(f"✓ {len(posts)} épisodes assemblés")


def write_publication(posts):
    ep1 = json.loads((HERE / "ep01-post.json").read_text(encoding="utf-8")) if (HERE / "ep01-post.json").exists() else None
    eps = ([ep1] if ep1 else []) + posts
    lines = [
        "# Épargne malin : guide de publication TikTok", "",
        "## Le rythme", "",
        "- **Une vidéo par jour, dans l'ordre**, à heure fixe : 18 h 30 ou 20 h (quand ton audience",
        "  est sur l'appli ; vérifie dans *Outils pour créateurs → Statistiques → Abonnés* après",
        "  quelques jours et ajuste).",
        "- **Crée une playlist « Épargne malin »** sur ton profil et ajoute-y chaque épisode.",
        "- **Épingle les épisodes 01 et 02** sur ton profil.", "",
        "## Pour chaque vidéo", "",
        "1. Importe le MP4 tel quel (1080×1920, 30 i/s, son déjà mixé).",
        "2. Couverture : choisis l'image où le gros titre du début est entièrement affiché.",
        "3. Colle la légende et les hashtags ci-dessous (bloc à copier).",
        "4. Dans les 30 minutes, réponds aux premiers commentaires : la question de fin de",
        "   légende est là pour ça. Épingle la meilleure réponse.", "",
        "## Les hashtags", "",
        "Chaque vidéo a 8 hashtags : 2 propres au sujet, puis 6 communs à la série",
        "(#epargne #argent #financepersonnelle #budget #astuceargent #apprendresurtiktok).",
        "Les hashtags aident TikTok à classer la vidéo, mais ce sont surtout les 2 premières",
        "secondes et le taux de visionnage complet qui la rendent virale. Avant de publier, tape",
        "chaque hashtag dans la recherche TikTok pour vérifier qu'il est actif, et remplace-le si",
        "un hashtag proche a beaucoup plus de vues. Évite #fyp / #pourtoi : ils n'aident pas.", "",
        "Ces vidéos donnent des informations générales sur l'épargne. Ce ne sont pas des conseils",
        "en investissement personnalisés : les chiffres sont des exemples.", "",
    ]
    for e in eps:
        lines += [f"## Épisode {e['ep']:02d} · {e['title']}", "",
                  f"Jour {e['ep']} · vidéo : `serie/videos/ep{e['ep']:02d}.mp4`", "",
                  "```", e["post"]["caption"], "", " ".join(e["post"]["hashtags"]), "```", ""]
    (HERE / "PUBLICATION.md").write_text("\n".join(lines), encoding="utf-8")


def render_all():
    (HERE / "videos").mkdir(exist_ok=True)
    for path in episodes():
        subprocess.run([sys.executable, str(ROOT / "voix" / "voiceover.py"), str(path), "--prises", "4"], check=True)
    build()
    for path in episodes():
        subprocess.run(["node", str(ROOT / "render.mjs"), str(HERE / f"{path.stem}.html"),
                        "--audio", str(HERE / f"{path.stem}-mix.wav"), "--out", str(HERE / "videos")], check=True)


if __name__ == "__main__":
    render_all() if "--tout" in sys.argv else build()
