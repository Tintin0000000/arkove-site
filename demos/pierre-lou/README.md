# Pierre-Lou Automobiles — maquette V1

Premier jet du site vitrine pour Pierre-Lou (achat-revente de véhicules d'occasion, Rennes).
Site statique : HTML, CSS et JavaScript, sans dépendance ni étape de build. Seule la police Archivo est chargée depuis Google Fonts.

## Pages

| Fichier | Contenu |
|---|---|
| `index.html` | Accueil : intro rideau métallique + plaque animée, titre qui s'étire au survol, vitrine glissable, services, présentation, avis, estimation de reprise par plaque |
| `garage.html` | Présentation : Pierre-Lou, histoire, méthode en 4 étapes (défilement horizontal), engagements, galerie |
| `vehicules.html` | Tout le stock : recherche, filtres (marque, énergie, boîte, budget, km, année), tri, réarrangement animé |
| `vehicule.html?id=…` | Fiche véhicule : galerie 6 photos, caractéristiques, équipements, simulateur de mensualité, véhicules similaires |
| `contact.html` | Formulaire qui s'adapte à la demande (achat, reprise, dépôt-vente, financement, recherche), horaires avec statut ouvert/fermé en direct, carte |

Les liens se pré-remplissent : `contact.html?demande=reprise&immat=AB-123-CD`, `contact.html?demande=achat&vehicule=peugeot-208-2021&essai=1`, `vehicules.html?carburant=Hybride`.

## Voir le site en local

```bash
cd demos/pierre-lou
npx http-server -p 8080 .
# puis ouvrir http://localhost:8080
```

L'intro complète (rideau + plaque) ne se joue qu'à la première visite de l'accueil dans l'onglet. Pour la revoir : nouvel onglet, ou `sessionStorage.clear()` dans la console.

## Espace d'administration (`/admin`)

Pierre-Lou gère lui-même son stock et ses photos depuis `pierrelou-auto.fr/admin`, sur téléphone ou ordinateur :

- **Véhicules** : ajouter une voiture, modifier prix, kilométrage, équipements, ajouter les photos depuis la galerie du téléphone (la 1re sert de vignette), cocher « vitrine » pour l'accueil. Une voiture vendue passe en statut « Vendu » et disparaît du site.
- **Photos du site** : les 19 emplacements de l'accueil et de la page Le garage. Un emplacement laissé vide garde son cadre provisoire.

Chaque enregistrement met à jour `content/vehicules.json` ou `content/photos.json` dans le dépôt GitHub, et l'hébergeur republie le site en 1 à 2 minutes. Les photos sont rangées dans `assets/photos/uploads/`.

L'outil est [Decap CMS](https://decapcms.org) (gratuit, open source), chargé depuis `admin/index.html`, configuré dans `admin/config.yml`.

**Mode démonstration** : en dehors du domaine déclaré dans `admin/index.html` (`PL_PROD_HOSTS`), l'espace s'ouvre sans mot de passe avec le contenu actuel du site chargé en mémoire. On peut tout essayer, rien n'est enregistré. C'est ce mode qui tourne sur la maquette.

### Mise en ligne (à faire une fois)

1. Mettre le contenu de ce dossier dans un dépôt GitHub dédié au client (par ex. `pierrelou-site`).
2. Relier ce dépôt à un hébergeur qui republie à chaque modification : Netlify, Cloudflare Pages ou Vercel (offres gratuites suffisantes). Brancher le domaine `pierrelou-auto.fr`.
3. Créer un compte sur [DecapBridge](https://decapbridge.com) (connexion des éditeurs par e-mail et mot de passe, Google ou Microsoft, sans compte GitHub ; offre gratuite annoncée : 3 sites, 10 personnes par site), y ajouter le site, puis **remplacer le bloc `backend:` de `admin/config.yml`** par celui que DecapBridge fournit.
4. Vérifier que le domaine réel figure dans `PL_PROD_HOSTS` (`admin/index.html`).
5. Inviter Pierre-Lou depuis DecapBridge avec son e-mail. Il reçoit un lien, choisit son mot de passe, puis se connecte sur `/admin`.

### Sans l'espace d'administration

Les emplacements fonctionnent aussi « à la main » : un fichier déposé avec le nom indiqué dans l'emplacement le remplace automatiquement.

- Véhicules : `assets/photos/vehicules/<id>-1.jpg` à `-6.jpg` (l'id est `marque-modele-annee`, ex. `peugeot-208-2021`).
- Garage et accueil : `assets/photos/accueil-vedette.jpg` et `assets/photos/garage/<nom>.jpg` (noms affichés dans chaque emplacement).

## À récupérer auprès de Pierre-Lou

- [ ] Nom commercial exact et logo éventuel (la plaque `PL-035-RN` sert de logo provisoire)
- [ ] Adresse, téléphone, e-mail (actuellement fictifs : `02 99 00 00 00`, `contact@pierrelou-auto.fr`)
- [ ] Horaires (dans `assets/js/main.js`, tableau `PL.HOURS`)
- [ ] Stock réel (les 12 véhicules de `content/vehicules.json` sont des exemples ; il pourra les remplacer lui-même depuis `/admin`)
- [ ] Durées de garantie, services proposés (dépôt-vente, LOA…), taux de financement indicatif (`PL.TAUX`)
- [ ] Son parcours pour la page Le garage, et 3 vrais avis Google
- [ ] Les photos listées ci-dessus

## À brancher avant la mise en ligne

- Le formulaire de contact n'envoie rien pour l'instant (écran de confirmation seulement). Point de branchement commenté dans `assets/js/contact.js` (Formspree, Brevo ou un simple script d'envoi d'e-mail).
- Mentions légales et page de confidentialité.
- Carte : remplacer le cadrage OpenStreetMap de `contact.html` par l'adresse exacte.
