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

## Ajouter les photos

Chaque emplacement photo affiche son nom de fichier. Il suffit de déposer le fichier au bon endroit avec ce nom : la photo remplace automatiquement l'emplacement, sans toucher au code.

**Véhicules** — `assets/photos/vehicules/<id>-1.jpg` à `<id>-6.jpg`
(1 = 3/4 avant, utilisée en vignette ; 2 = profil ; 3 = 3/4 arrière ; 4 = poste de conduite ; 5 = places arrière ; 6 = coffre). Format paysage, 1600 × 1000 px conseillé.

**Garage** — `assets/photos/` et `assets/photos/garage/` :

| Fichier | Où |
|---|---|
| `accueil-vedette.jpg` | Grande photo de l'accueil (paysage 16:9) |
| `garage/portrait-pierre-lou.jpg` | Accueil, présentation (vertical 4:5) |
| `garage/service-achat.jpg`, `service-reprise.jpg`, `service-depot.jpg`, `service-financement.jpg`, `service-recherche.jpg` | Aperçus au survol des services (4:3) |
| `garage/garage-facade.jpg`, `garage-pierre-lou.jpg`, `garage-parc.jpg` | En-tête de la page Le garage |
| `garage/methode-1-selection.jpg` à `methode-4-livraison.jpg` | Les 4 étapes de la méthode (16:9) |
| `garage/galerie-1.jpg` à `galerie-5.jpg` | Galerie « Le garage en images » |

## À récupérer auprès de Pierre-Lou

- [ ] Nom commercial exact et logo éventuel (la plaque `PL-035-RN` sert de logo provisoire)
- [ ] Adresse, téléphone, e-mail (actuellement fictifs : `02 99 00 00 00`, `contact@pierrelou-auto.fr`)
- [ ] Horaires (dans `assets/js/main.js`, tableau `PL.HOURS`)
- [ ] Stock réel (dans `assets/js/data.js` : les 12 véhicules actuels sont des exemples)
- [ ] Durées de garantie, services proposés (dépôt-vente, LOA…), taux de financement indicatif (`PL.TAUX`)
- [ ] Son parcours pour la page Le garage, et 3 vrais avis Google
- [ ] Les photos listées ci-dessus

## À brancher avant la mise en ligne

- Le formulaire de contact n'envoie rien pour l'instant (écran de confirmation seulement). Point de branchement commenté dans `assets/js/contact.js` (Formspree, Brevo ou un simple script d'envoi d'e-mail).
- Mentions légales et page de confidentialité.
- Carte : remplacer le cadrage OpenStreetMap de `contact.html` par l'adresse exacte.
