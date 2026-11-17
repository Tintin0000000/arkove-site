# Argent Maîtrisé — e-book

Guide de finances personnelles (français), niveaux débutant et intermédiaire.
31 chapitres, décliné en trois éditions.

| Édition | Source | Sortie | Volume |
|---|---|---|---|
| **Essentielle** (PDF vendu) | `content-court/` | `Argent-Maitrise-essentiel.pdf` | 60 p., 14 300 mots |
| **Complète** (PDF long) | `content/` | `Argent-Maitrise-ebook.pdf` | 135 p., 24 000 mots |
| **Web interactive** | `content/` | `web/argent-maitrise.html` | texte long + 5 simulateurs |

L'édition essentielle couvre les mêmes 31 chapitres, resserrés : développements
coupés, moins d'exemples, un encadré « L'essentiel » par partie au lieu d'un par
chapitre, annexes allégées. La mise en page est aussi plus dense — pas de saut de
page à chaque chapitre, marges et interligne réduits, tableaux sécables.

**Deux arborescences de contenu distinctes.** `content-court/` a été réécrit à la
main : ce n'est pas une génération automatique depuis `content/`. Une correction
de fond doit donc être reportée dans les deux, ou l'une des deux abandonnée.

## Règle commune

**Ne modifiez jamais le PDF ou le HTML directement** : modifiez le Markdown et
relancez la chaîne.

| Fichier | Contenu |
|---|---|
| `content/00-front.md` | Avant-propos, mode d'emploi, avertissement |
| `content/01-fondations.md` | Partie I — chapitres 1 à 5 |
| `content/02-comprendre.md` | Partie II — chapitres 6 à 9 |
| `content/03-enveloppes.md` | Partie III — chapitres 10 à 16 |
| `content/04-portefeuille.md` | Partie IV — chapitres 17 à 23 |
| `content/05-optimiser.md` | Partie V — chapitres 24 à 28 |
| `content/06-action.md` | Partie VI — chapitres 29 à 31 |
| `content/07-annexes.md` | Annexes A à F |

Conventions de balisage, en plus du Markdown standard :

- `::: {.encadre}` — encadré « L'essentiel du chapitre N »
- `::: {.alerte}` — avertissement ou point de vigilance
- `::: {.action}` — passage à l'action
- `::: {.exemple}` — exemple chiffré
- `::: {.formule}` — formule de calcul
- `::: {.widget data-widget="xxx"}` — simulateur : **invisible dans le PDF**,
  rendu en interactif sur le web (`precaution`, `compound`, `fees`, `risk`, `cashflow`)

## Régénérer

```bash
cd ebook

# 1. Édition essentielle — 60 pages
python3 build/assemble-court.py
node build/topdf-court.js
python3 - <<'PY'
import pypdf
w = pypdf.PdfWriter()
w.append("build/part-cover-court.pdf"); w.append("build/part-body-court.pdf")
with open("Argent-Maitrise-essentiel.pdf","wb") as f: w.write(f)
PY

# 2. Édition complète — 135 pages
python3 build/assemble.py
node build/topdf.js
python3 - <<'PY'
import pypdf
w = pypdf.PdfWriter()
w.append("build/part-cover.pdf"); w.append("build/part-body.pdf")
with open("Argent-Maitrise-ebook.pdf","wb") as f: w.write(f)
PY

# 3. Édition web interactive (depuis content/)
python3 build/webbuild.py
```

Dépendances : `pandoc`, `python3` + `pypdf`, `node` + `playwright` (Chromium).

## Fichiers de mise en forme

- `build/book.css` — style d'impression, édition complète (format 6×9 pouces)
- `build/book-court.css` — style d'impression, édition essentielle (plus dense)
- `build/web.css` — feuille de style de l'édition web
- `build/web.js` — navigation, suivi de lecture, cases à cocher, 5 simulateurs
- `build/template.html` — gabarit pandoc du PDF

## À vérifier avant toute diffusion

1. **Les chiffres réglementaires** (Annexe B) : taux, plafonds, barèmes,
   abattements. Ils changent chaque année. Sources : `impots.gouv.fr`,
   `service-public.fr`, `service-public.fr` pour les livrets réglementés.
2. **La mention d'auteur** : les couvertures et pages de titre n'en portent
   aucune. À ajouter dans `build/assemble.py` et `build/assemble-court.py`
   (variables en haut de chaque fichier).
3. **Les mentions légales** (Annexe F) : à faire relire si l'e-book est vendu.
