# Série TikTok « Épargne malin »

10 vidéos verticales (1080×1920, 22 à 30 s, voix off, sous-titres, musique), une par jour.

| Jour | Épisode | Durée |
|---|---|---|
| 1 | Le fonds d'urgence | 30 s |
| 2 | La règle 50/30/20 | 27 s |
| 3 | Paie-toi en premier | 23 s |
| 4 | Les abonnements fantômes | 22 s |
| 5 | Le vrai prix de ton café | 23 s |
| 6 | Le défi des 52 semaines | 27 s |
| 7 | La règle des 72 heures | 22 s |
| 8 | L'inflation et ton épargne | 22 s |
| 9 | Pourquoi commencer tôt | 24 s |
| 10 | La méthode des enveloppes | 24 s |

- Les vidéos : `videos/ep01.mp4` à `videos/ep10.mp4`.
- Les légendes et hashtags à copier : `PUBLICATION.md`.

## Comment c'est fait

Chaque épisode est un fichier `epNN.json` qui contient trois parties :

- `sentences` : le script de la voix off, phrase par phrase, découpé en morceaux
  `[texte affiché, texte prononcé, bruitage optionnel]`, comme dans `voix/script-30s.json` ;
- `blocks` : un bloc visuel par partie de la vidéo (`segment`), avec les instants écrits
  `"phrase:morceau"` (`"3:1"` = 2e morceau de la 4e phrase, `"3:end"` = fin de la phrase,
  `"3:1+0.4"` = 0,4 s plus tard) ;
- `post` : la légende TikTok et les hashtags.

Blocs disponibles (`serie.js`) :

| Bloc | Pour |
|---|---|
| `hook` | gros mots qui claquent + icône, puis la « réponse » en italique doré |
| `icon` | grande icône, une phrase et un sous-titre |
| `counter` | grand montant qui grimpe ou descend en plusieurs étapes, courbe, tampon |
| `bars` | comparaison de montants en barres |
| `donut` | répartition en pourcentages |
| `grid` | cases qui se remplissent (semaines, mois) + total |
| `list` | lignes icône / libellé / montant + total |
| `curves` | deux courbes de croissance comparées |
| `timer` | compte à rebours circulaire + jauge |
| `steps` | étapes reliées par des flèches |
| `cta` | abonnement, pseudo et annonce de l'épisode suivant |

Le premier épisode est la scène sur mesure `scenes/06-fonds-urgence.html`.

## Refaire ou ajouter un épisode

```bash
cd motion
python3 serie/episodes.py                               # (ré)écrit ep02…ep10.json
python3 voix/voiceover.py serie/ep11.json --prises 5    # voix + musique + minutage
python3 serie/build.py                                  # epNN.html + PUBLICATION.md
node render.mjs serie/ep11.html --audio serie/ep11-mix.wav --out serie/videos
```

Ou tout d'un coup (voix + vidéos des épisodes 02 à 10, compte environ une heure) :
`python3 serie/build.py --tout`.

Les fichiers audio (`*-voix.wav`, `*-mix.wav`) ne sont pas versionnés. Pour ne refaire que
l'image d'un épisode (changer le pseudo, une couleur…), réutilise le son de la vidéo :

```bash
ffmpeg -i serie/videos/ep02.mp4 -vn -c:a copy /tmp/ep02.m4a
node render.mjs serie/ep02.html --audio /tmp/ep02.m4a --out serie/videos
```

Voix de synthèse : Piper `fr_FR-siwis-medium`, entraînée sur le corpus SIWIS (CC-BY 4.0).
Mentionne-le dans ta bio ou tes descriptions.
