# Argent Maîtrisé — e-book

Guide de finances personnelles (français), niveaux débutant et intermédiaire.
32 chapitres, décliné en trois éditions.

| Édition | Source | Sortie | Volume |
|---|---|---|---|
| **Essentielle** (PDF vendu) | `content-court/` | `Argent-Maitrise-essentiel.pdf` | 66 p., 15 200 mots |
| **Complète** (PDF long) | `content/` | `Argent-Maitrise-ebook.pdf` | 145 p., 25 500 mots |
| **Web interactive** | `content/` | `web/argent-maitrise.html` | texte long + 5 simulateurs |
| **Page de vente** | écrite à la main | `web/vente.html` | page autonome à déposer sur le domaine |

L'édition essentielle couvre les mêmes 32 chapitres, resserrés : développements
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
- `<figure class="figure">` — illustration SVG en HTML brut, rendue dans les
  deux formats. Les couleurs viennent des tokens avec repli
  (`var(--gold-soft, var(--gold-2, …))`), car les feuilles print et web ne
  nomment pas les nuances secondaires de la même façon.

## Règle de pagination

**Aucun tableau, encadré ou figure ne doit se couper entre deux pages.** Tous
sont en `break-inside: avoid`, ce qui ne suffit pas si un élément dépasse la
hauteur utile d'une page : le navigateur le coupe quand même. Après toute
modification de contenu, vérifiez avec :

```bash
node build/checktables.js       # édition essentielle
node build/checktables-long.js  # édition complète
```

Le tableau `over` doit rester vide. S'il ne l'est pas, scindez l'élément — c'est
ainsi que l'exemple du chapitre 1 a été sorti de son encadré.

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

## Identité visuelle — distincte d'Arkove

Ce produit ne porte **pas** la charte d'Arkove et ne doit pas la reprendre.
Arkove est sombre et doré (`#141210` / `#CE9B4C`, titres Didot) ; « Argent
Maîtrisé » est clair et vert sapin. Les deux marques doivent rester
reconnaissables séparément.

| | Valeur | Rôle |
|---|---|---|
| Encre | `#16202A` | Texte, titres, en-têtes de tableaux |
| Accent | `#0E6B5C` | Filets, étiquettes, chiffres mis en avant |
| Accent clair | `#7FB9AC` | Bordures, états secondaires |
| Fond couverture | `#F7F8F6` | Couverture claire, bandeau vert en tête |
| Teinte « action » | `#E9F4F0` | Encadrés d'action |
| Alerte | `#C0392B` | Avertissements et points de vigilance |

Typographie : Inter Display (titres) + Bitstream Charter (corps) pour le PDF,
Bricolage Grotesque + Source Serif 4 pour le web. Aucun serif didone, pour
éviter l'écho avec Arkove.

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
3. **Les mentions légales** (dernière annexe) : à faire relire si l'e-book est vendu.
4. **Les neuf placeholders de `web/vente.html`** — repérables à leur fond jaune
   dans la page, et en cherchant `class="todo"` dans le fichier : nom et bio de
   l'auteur, lien de paiement, garantie éventuelle, mentions légales, CGV,
   politique de confidentialité, adresse de contact, et le bloc éditeur avec le
   SIRET. **La page ne doit pas être mise en ligne tant qu'il en reste un.**
