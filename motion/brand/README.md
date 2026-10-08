# Logo « Épargne malin »

L'accent du « é » devient une flèche qui monte (l'argent qui grandit), frappée dans une pièce d'or.
Typographie : Instrument Serif (SIL Open Font License), la même que dans les vidéos.

| Fichier | Usage |
|---|---|
| `avatar-or.png` (+ `-400`, `-200`) | **photo de profil TikTok recommandée** : fond or, se voit en mode clair comme sombre |
| `avatar-nom-or.png`, `avatar-nom.png`, `avatar-nom-creme.png` | photo de profil avec le nom « épargne malin » sous le é (or, noir, crème) |
| `avatar.png`, `avatar-creme.png` | variantes noir et or, crème (`apercu-tiktok.png` compare les trois) |
| `icone.png` / `icone.svg` | icône seule, fond transparent |
| `logo-horizontal.png` / `.svg` | bannières, miniatures, fond sombre |
| `logo-horizontal-clair.png` / `.svg` | fond clair (documents, site) |
| `logo-empile.png` / `.svg` | format carré : publications, couverture de playlist |
| `filigrane.png` / `.svg` | à poser en transparence sur une vidéo |

Couleurs : noir `#0d0c0a`, crème `#f3eee4`, or `#e2b467` (dégradé `#f6d690` → `#b98436`).

Les SVG ont leurs lettres vectorisées : ils s'affichent pareil partout, sans police installée.
Pour les régénérer : `python3 brand/logo.py` puis `node brand/export.mjs`
(prérequis : `pip install fonttools brotli uharfbuzz`).
