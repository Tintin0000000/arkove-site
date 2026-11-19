# Fiche Amazon KDP — Argent Maîtrisé

Tout ce qui suit se copie-colle dans le formulaire KDP. Les champs marqués
**À COMPLÉTER** sont les seuls qui demandent une décision de ta part.

---

## 1. Fichiers à téléverser

| Champ KDP | Fichier |
|---|---|
| Manuscrit | `Argent-Maitrise-kindle.epub` |
| Couverture | `build/epub/couverture-kindle.png` (1600 × 2560, format exigé) |

Avant de téléverser, ouvre l'EPUB dans **Kindle Previewer** (gratuit, Amazon) et
regarde les pages qui contiennent des tableaux : c'est le seul endroit où le
rendu peut surprendre sur un petit écran.

---

## 2. Titre et sous-titre

**Titre**
```
Argent Maîtrisé
```

**Sous-titre** — c'est lui qui travaille pour la recherche, pas le titre
```
Le guide pratique des finances personnelles : budget, épargne, investissement, PEA, assurance-vie, immobilier et fiscalité
```

**Auteur** — **À COMPLÉTER**. Même nom que dans l'EPUB (modifie la variable
`AUTEUR` en haut de `build/epub/build_epub.py`, puis régénère).

---

## 3. Description

KDP accepte quelques balises HTML simples. Colle ceci tel quel.

```html
<b>Vous gagnez votre vie, mais vous ne savez pas où part votre argent.</b>

Ce guide répond à la question dans l'ordre : d'abord ce qui entre et ce qui sort chaque mois, ensuite ce que vous possédez vraiment, et seulement après, comment investir.

<b>32 chapitres, six parties, un plan en 90 jours.</b>

<b>Pour les débutants</b> — Faire le point sur ses entrées et ses sorties. Construire un budget qui tient sans effort de volonté. Dimensionner son épargne de précaution. Éteindre les dettes qui coûtent cher. Comprendre les trois forces qui décident de tout : les intérêts composés, l'inflation et les frais.

<b>Pour ceux qui ont déjà commencé</b> — Choisir entre PEA, assurance-vie, PER et compte-titres, et dans quel ordre les remplir. Construire une allocation d'actifs adaptée à son horizon. Sélectionner ses ETF sur sept critères. Calculer le vrai cash-flow d'un investissement locatif, charges comprises. Anticiper la transmission.

<b>Ce que ce livre ne fait pas</b> — Il ne recommande aucun produit, ne nomme aucun établissement et ne promet aucun rendement. Il explique les mécanismes, donne les chiffres, et dit clairement quand il faut consulter un professionnel.

Chaque partie se termine par un encadré « L'essentiel ». Cinq annexes rassemblent le lexique, les tableaux de référence, les checklists et les formules de calcul.

<i>Document pédagogique et informatif. Ne constitue pas un conseil en investissement personnalisé. Tout investissement en actifs non garantis comporte un risque de perte en capital.</i>
```

---

## 4. Les sept mots-clés

Un par champ. Ne répète pas les mots déjà présents dans le titre ou le
sous-titre : Amazon les indexe déjà.

```
1. gerer son argent au quotidien
2. investir en bourse pour les debutants
3. independance financiere france
4. placement epargne debutant
5. etf gestion passive
6. revenus passifs immobilier locatif
7. education financiere livre francais
```

**À vérifier avant de valider** : tape chacun de ces termes dans la barre de
recherche d'Amazon.fr sans valider. Si l'autocomplétion le propose, des gens le
cherchent vraiment — garde-le. Sinon, remplace-le par la suggestion la plus
proche qu'Amazon affiche. C'est de la donnée gratuite et fiable, et elle vaut
mieux que mes suppositions.

---

## 5. Catégories

KDP t'en fait choisir plusieurs dans sa propre arborescence. Vise :

- Boutique Kindle → Entreprise et Bourse → **Finances personnelles**
- Boutique Kindle → Entreprise et Bourse → **Investissement**

Choisis les catégories les plus **spécifiques** disponibles plutôt que les plus
larges : il est bien plus facile d'être visible dans une sous-catégorie.

---

## 6. Prix

**9,99 €**

Pourquoi ce chiffre : la redevance à 70 % n'existe en France qu'entre **2,69 € et
12,99 €**. En dessous de 2,69 € ou au-dessus de 12,99 €, tu tombes à 35 %.

| Prix | Redevance | Tu touches environ |
|---|---|---|
| 9,99 € | 70 % | ≈ 6,60 € |
| 12,99 € | 70 % | ≈ 8,60 € |
| 17,00 € | 35 % | ≈ 5,60 € |

À 17 €, tu gagnes **moins** qu'à 9,99 €. C'est contre-intuitif, et c'est la
raison de ne pas aligner le prix Amazon sur celui de ton pack.

Les montants ci-dessus sont des ordres de grandeur hors TVA et hors frais de
livraison numérique. Le simulateur de KDP te donnera le chiffre exact.

---

## 7. Deux décisions à prendre

**KDP Select : non, pour l'instant.** Ce programme donne de la visibilité et les
pages lues en Kindle Unlimited, mais il impose **l'exclusivité numérique** :
tu ne pourrais plus vendre le PDF ailleurs. Comme ton pack Payhip contient le
PDF, les deux sont incompatibles. Tu pourras basculer plus tard si Amazon
devient ton canal principal.

**DRM : non.** Il n'empêche pas la copie et gêne les lecteurs honnêtes.

---

## 8. Après la mise en ligne

1. La fiche met **24 à 72 heures** à être validée.
2. Tes **dix premiers avis** valent plus que tout le reste : demande-les à ton
   entourage, sans jamais les acheter ni les échanger — Amazon supprime les
   comptes pour ça.
3. Relève ton **classement des ventes** chaque semaine. C'est ton seul indicateur
   fiable de ce qui marche.
