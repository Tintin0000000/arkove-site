# Motion design finance, codé avec Claude

Quatre séquences animées sur le thème de la finance, prêtes à monter dans une vidéo :

| Scène | Format | Durée | Usage |
|---|---|---|---|
| `01-intro-youtube` | 16:9 · 1920×1080 | 7 s | Intro de vidéo YouTube |
| `02-interets-composes` | 9:16 · 1080×1920 | 9,5 s | TikTok / Reels / Shorts |
| `03-budget-50-30-20` | 9:16 · 1080×1920 | 9 s | TikTok / Reels / Shorts |
| `04-hook-3-erreurs` | 9:16 · 1080×1920 | 10 s | Hook d'ouverture d'un short |

Les MP4 déjà exportés sont dans `videos/`. La galerie `index.html` les montre tous.

## Le principe

Chaque scène est une simple page HTML. Il n'y a ni After Effects ni logiciel payant :

1. **`engine.js`** est un mini moteur (environ 150 lignes). Une scène est une fonction `render(t)`
   qui place chaque élément en fonction du temps `t`, en secondes. Avec la même valeur de `t`,
   on obtient toujours la même image.
2. **Dans le navigateur**, la scène se joue en boucle, avec une barre pour la parcourir
   (espace = lecture / pause).
3. **`render.mjs`** ouvre la scène dans un Chromium sans interface, avance le temps image par image
   (30 i/s), fait une capture à chaque fois et envoie le tout à `ffmpeg`. On obtient un MP4 H.264
   parfaitement fluide, quelle que soit la puissance de la machine.

Les polices (Inter Tight, Instrument Serif, JetBrains Mono, licence SIL OFL) sont incluses dans
`fonts/`. L'export fonctionne donc hors ligne.

## Reproduire chez toi

Prérequis : [Node.js](https://nodejs.org) 18 ou plus récent, et [ffmpeg](https://ffmpeg.org/download.html)
(`brew install ffmpeg` sur Mac, `winget install ffmpeg` sur Windows).

```bash
cd motion
npm install                 # installe Playwright
npx playwright install chromium

npx serve .                 # aperçu : ouvre http://localhost:3000
npm run render              # exporte toutes les scènes dans videos/
node render.mjs scenes/02-interets-composes.html             # une seule scène
node render.mjs scenes/02-interets-composes.html --still 7   # une image PNG à t = 7 s
node render.mjs scenes/01-intro-youtube.html --fps 60        # en 60 i/s
```

Le MP4 s'importe ensuite tel quel dans CapCut, Premiere ou DaVinci Resolve, où l'on ajoute la
voix off et la musique.

## Créer ta propre scène

Copie une scène existante, puis modifie les textes et les chiffres. Le squelette est le suivant :

```html
<div class="frame"><div id="stage">
  <h1 class="abs" id="titre">Mon titre</h1>
</div></div>
<script src="../engine.js"></script>
<script>
  M.scene({
    width: 1080, height: 1920, duration: 5,
    render(t) {
      const p = M.prog(t, 0.5, 0.8, M.ease.outBack); // 0 → 1 entre 0,5 s et 1,3 s
      document.getElementById('titre').style.transform = `scale(${p})`;
    },
  });
</script>
```

Les outils fournis par `M` :

- `M.prog(t, début, durée, easing)` renvoie la progression entre 0 et 1, avec un easing.
- `M.ease.*` propose `outCubic`, `inOutCubic`, `outExpo`, `inOutExpo`, `outBack` et `outElastic`.
- `M.splitWords(el)` découpe un titre en mots pour les animer un par un.
- `M.euro(7612)` affiche `7 612 €`.
- `M.rng(graine)` produit un aléatoire reproductible, utile pour générer des courbes boursières.

### Ou demande-la à Claude

Exemples de demandes qui produisent ce genre de scène :

> « Dans `motion/`, crée une scène 9:16 de 8 secondes sur l'effet de l'inflation :
> 1 000 € qui perdent de la valeur année après année, avec un compteur qui descend en rouge
> et une phrase choc à la fin. Garde le style des autres scènes. Exporte-la en MP4. »

> « Fais une variante de l'intro YouTube pour l'épisode 02, intitulé "Investir 100 € par mois",
> et remplace @tachaine par @monpseudo. »

## Conseils pour TikTok / Reels / Shorts

- Garde le texte important entre **y = 150 et y = 1550**. Le bas de l'écran est couvert par la
  légende et les boutons, et le bord droit par les icônes.
- Tout se joue dans les 2 premières secondes : un hook gros, court et contrasté.
- Les chiffres affichés sont **illustratifs**. Ce ne sont ni des cours réels ni un conseil en
  investissement. La scène des intérêts composés porte une mention à ce sujet.
