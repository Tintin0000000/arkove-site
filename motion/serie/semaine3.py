#!/usr/bin/env python3
"""
Semaine 3 : la suite des 3 séries, 5 vidéos d'un peu plus d'une minute.

    affirmation surprenante (1re seconde) → 3 preuves visuelles → verdict →
    « sauvegarde cette vidéo avant de… » → une question pour faire commenter.

Plus d'une minute : seules ces vidéos comptent pour le programme de rémunération de TikTok.

    python3 serie/semaine3.py     # écrit serie/ep16.json … ep20.json et serie/scripts/epNN.txt

Les montants « exemple » sont signalés comme tels à l'écran.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
COMMON = {"voice": "siwis-medium", "speed": 0.97, "lead": 0.3, "gap": 0.18, "duration": "auto", "tail": 1.6,
          "handle": "@epargne.malin7"}
P = lambda n: [f"PREUVE NUMÉRO {n} :", f"Preuve numéro {['un', 'deux', 'trois'][n - 1]} :"]
PROOF = lambda seg, n, show, say: {"segment": seg, "sfx": "whoosh", "pause": 0.1, "chunks": [P(n), [show, say]]}
VERDICT = lambda *chunks: {"segment": "verdict", "sfx": "whoosh", "pause": 0.1, "chunks": [["VERDICT :", "Verdict :"], *chunks]}
SAVE = lambda show, say: {"segment": "cta", "sfx": "whoosh", "pause": 0.1, "chunks": [["*SAUVEGARDE CETTE VIDÉO", "Sauvegarde cette vidéo"], [show, say]]}
ASK = lambda show, say: {"segment": "cta", "chunks": [["ET TOI,", "Et toi,"], [show, say], ["*DIS-LE EN COMMENTAIRE.", "Dis-le en commentaire."]]}
S = lambda seg, *chunks: {"segment": seg, "chunks": list(chunks)}
CHIP = lambda n, at: {"text": f"PREUVE {n} / 3", "at": at}
CTA = lambda sub: {"type": "cta", "glow": "gold", "save": True, "heading": "<em>Sauvegarde</em>-la", "sub": sub}

eps = {}

# ---------------------------------------------------------------- 16 · 1 erreur : payer en 4 fois
eps[16] = {"title": "Le paiement en 4 fois", "series": "1 ERREUR QUI TE COÛTE · #2", "short": "PAIEMENT EN 4 FOIS",
  "next": "Achat-revente : rentable ou arnaque ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["*PAYER EN 4 FOIS", "Payer en quatre fois"], ["TES PETITS ACHATS ?", "tes petits achats ?"], ["*ÇA PEUT TE COÛTER CHER.", "Ça peut te coûter cher.", "boom"]]},
    S("hook", ["C'EST L'ERREUR :", "C'est l'erreur :"], ["*FRACTIONNER CE QUE TU PEUX", "fractionner ce que tu peux"], ["PAYER EN UNE FOIS.", "payer en une seule fois."]),
    PROOF("p1", 1, "*LES FRAIS.", "les frais."),
    S("p1", ["SELON LE MAGASIN,", "Selon le magasin,"], ["LE PAIEMENT EN PLUSIEURS FOIS", "le paiement en plusieurs fois"], ["*N'EST PAS TOUJOURS GRATUIT.", "n'est pas toujours gratuit."]),
    S("p1", ["EXEMPLE : 400 € EN 4 FOIS,", "Exemple : quatre cents euros en quatre fois,"], ["AVEC 2 % DE FRAIS :", "avec deux pour cent de frais :"], ["*8 € DE PLUS.", "huit euros de plus.", "coin"]),
    S("p1", ["ET EN CAS DE RETARD,", "Et en cas de retard,"], ["*DES FRAIS S'AJOUTENT.", "des frais s'ajoutent.", "stamp"]),
    PROOF("p2", 2, "*L'EFFET BOULE DE NEIGE.", "l'effet boule de neige."),
    S("p2", ["UN CASQUE, DES BASKETS,", "Un casque, des baskets,"], ["UN TÉLÉPHONE :", "un téléphone :"], ["*3 ACHATS EN 4 FOIS.", "trois achats en quatre fois."]),
    S("p2", ["ÇA FAIT", "Ça fait"], ["*125 € PRÉLEVÉS CHAQUE MOIS.", "cent vingt-cinq euros prélevés chaque mois.", "stamp"]),
    S("p2", ["ET TU NE LE VOIS PAS", "Et tu ne le vois pas"], ["*SUR TON SOLDE", "sur ton solde"], ["AU MOMENT D'ACHETER.", "au moment d'acheter."]),
    PROOF("p3", 3, "*LE MAGASIN Y GAGNE.", "le magasin y gagne."),
    S("p3", ["QUAND ON PAIE EN PLUSIEURS FOIS,", "Quand on paie en plusieurs fois,"], ["*ON ACHÈTE SOUVENT PLUS CHER.", "on achète souvent plus cher."]),
    S("p3", ["40 € PAR MOIS", "Quarante euros par mois"], ["*PARAÎT PLUS PETIT", "paraît plus petit"], ["QUE 160 € D'UN COUP.", "que cent soixante euros d'un coup."]),
    S("p3", ["C'EST POUR ÇA", "C'est pour ça"], ["*QUE LES MAGASINS LE PROPOSENT.", "que les magasins le proposent."]),
    VERDICT(["*UTILE POUR UN GROS ACHAT PRÉVU,", "utile pour un gros achat prévu,"], ["PAS POUR LES PETITS PLAISIRS.", "pas pour les petits plaisirs."]),
    SAVE("AVANT TON PROCHAIN ACHAT EN 4 FOIS.", "avant ton prochain achat en quatre fois."),
    ASK("COMBIEN DE PAIEMENTS EN COURS ?", "tu as combien de paiements en cours ?")],
  "shakes": ["0:2", "8:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "card",
      "lines": [{"text": "En 4 fois", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "tes petits achats ?", "at": "0:1", "size": "m"},
                {"text": "ça coûte cher", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Fractionner <em>ses petits achats</em>", "at": "1:1"}},
    "p1": {"type": "counter", "glow": "red", "chip": CHIP(1, "2:0"), "title": {"html": "Les <em>frais</em>", "at": "2:1"}, "label": "Achat en 4 fois · exemple", "color": "down",
      "stages": [{"to": 400, "at": "4:0", "label": "PRIX DE L'ACHAT"}, {"to": 408, "at": "4:2", "label": "AVEC 2 % DE FRAIS"}],
      "badge": {"text": "+ frais", "small": "SI RETARD", "at": "5:1", "color": "red"},
      "disclaimer": "Frais variables selon le magasin : lis les conditions"},
    "p2": {"type": "list", "glow": "red", "chip": CHIP(2, "6:0"), "title": {"html": "L'effet <em>boule de neige</em>", "at": "6:1"}, "top": 500,
      "items": [{"icon": "play", "label": "Casque", "sub": "120 € en 4 fois", "value": "30 €/mois", "at": "7:0"},
                {"icon": "basket", "label": "Baskets", "sub": "160 € en 4 fois", "value": "40 €/mois", "at": "7:0+0.6"},
                {"icon": "phone", "label": "Téléphone", "sub": "220 € en 4 fois", "value": "55 €/mois", "at": "7:1"}],
      "total": {"label": "PRÉLEVÉS CHAQUE MOIS", "color": "down", "stages": [{"to": 125, "at": "8:1", "label": "PRÉLEVÉS CHAQUE MOIS"}]}},
    "p3": {"type": "bars", "glow": "gold", "chip": CHIP(3, "10:0"), "title": {"html": "Le magasin <em>y gagne</em>", "at": "10:1"}, "label": "Le même achat · exemple", "top": 520,
      "items": [{"label": "En 4 fois", "sub": "par mois", "value": 40, "color": "gold", "at": "12:0"},
                {"label": "En 1 fois", "sub": "d'un coup", "value": 160, "color": "down", "at": "12:2"}],
      "badge": {"text": "Même prix", "small": "IMPRESSION DIFFÉRENTE", "at": "13:1", "color": "gold"}},
    "verdict": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "14:0", "text": "Gros achat <em>prévu</em> : oui", "textAt": "14:1",
      "sub": "petits plaisirs : paie en une fois", "subAt": "14:2"},
    "cta": CTA("avant ton prochain achat en 4 fois")},
  "post": {"caption": "Payer en 4 fois tes petits achats, ça peut coûter cher : frais selon le magasin, frais de retard, et des prélèvements qui s'empilent sans que tu le voies. Sauvegarde cette vidéo avant ton prochain achat en 4 fois. Et toi, tu as combien de paiements en cours ?",
           "hashtags": ["#paiementen4fois", "#budget", "#argent", "#economiser"]},
  "cover": {"chip": "1 ERREUR · #2", "kicker": "Payer en 4 fois tes petits achats ?", "icon": "card"}}

# ---------------------------------------------------------------- 17 · Rentable ou arnaque : l'achat-revente
eps[17] = {"title": "L'achat-revente", "series": "RENTABLE OU ARNAQUE ? · #3", "short": "ACHAT-REVENTE",
  "next": "Les IA gratuites : qui paie ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["ACHETER 5 €,", "Acheter cinq euros,"], ["REVENDRE 25 €…", "revendre vingt-cinq euros…"], ["*LE CALCUL QUE PERSONNE NE MONTRE.", "voici le calcul que personne ne montre.", "boom"]]},
    S("hook", ["L'ACHAT-REVENTE EN LIGNE :", "L'achat-revente en ligne :"], ["*RENTABLE OU ARNAQUE ?", "rentable ou arnaque ?"]),
    PROOF("p1", 1, "*LE VRAI CALCUL.", "le vrai calcul."),
    S("p1", ["TU ACHÈTES UN PULL 5 €.", "Tu achètes un pull cinq euros."], ["*AVEC LES FRAIS ET LA LIVRAISON :", "Avec les frais et la livraison :"], ["ENVIRON 10 €.", "environ dix euros."]),
    S("p1", ["TU LE REVENDS", "Tu le revends"], ["*25 €.", "vingt-cinq euros."]),
    S("p1", ["IL TE RESTE", "Il te reste"], ["*ENVIRON 15 €.", "environ quinze euros.", "coin"]),
    PROOF("p2", 2, "*TON TEMPS.", "ton temps."),
    S("p2", ["CHERCHER, LAVER,", "Chercher, laver,"], ["PHOTOGRAPHIER, RÉPONDRE,", "photographier, répondre aux messages,"], ["*EMBALLER, DÉPOSER LE COLIS.", "emballer, déposer le colis."]),
    S("p2", ["SI ÇA TE PREND 1 HEURE PAR ARTICLE,", "Si ça te prend une heure par article,"], ["*TU GAGNES 15 € DE L'HEURE.", "tu gagnes quinze euros de l'heure."]),
    S("p2", ["ET SI L'ARTICLE NE PART PAS,", "Et si l'article ne part pas,"], ["*TU PERDS TA MISE.", "tu perds ta mise.", "stamp"]),
    PROOF("p3", 3, "*LES IMPÔTS.", "les impôts."),
    S("p3", ["VENDRE TES AFFAIRES PERSONNELLES,", "Vendre tes affaires personnelles,"], ["*EN GÉNÉRAL, CE N'EST PAS IMPOSABLE.", "en général, ce n'est pas imposable."]),
    S("p3", ["MAIS ACHETER POUR REVENDRE,", "Mais acheter pour revendre,"], ["*C'EST UNE ACTIVITÉ COMMERCIALE", "c'est une activité commerciale"], ["À DÉCLARER.", "à déclarer."]),
    S("p3", ["DÈS 30 VENTES OU 2 000 € PAR AN,", "Et dès trente ventes, ou deux mille euros par an,"], ["*LA PLATEFORME TRANSMET TES VENTES", "la plateforme transmet tes ventes"], ["AUX IMPÔTS.", "aux impôts."]),
    VERDICT(["*RENTABLE EN PETIT,", "rentable en petit,"], ["MAIS C'EST UN VRAI TRAVAIL.", "mais c'est un vrai travail."]),
    SAVE("AVANT DE TE LANCER.", "avant de te lancer dans l'achat-revente."),
    ASK("DÉJÀ REVENDU PLUS CHER ?", "tu as déjà revendu un article plus cher ?")],
  "shakes": ["0:2", "9:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "cart",
      "lines": [{"text": "5 € → 25 €", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "le calcul que", "at": "0:2", "size": "m"},
                {"text": "personne ne montre", "at": "0:2+0.4", "size": "m", "hl": True}],
      "reveal": {"html": "Achat-revente : <em>rentable</em> ?", "at": "1:1"}},
    "p1": {"type": "list", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "Le <em>vrai calcul</em>", "at": "2:1"}, "top": 500,
      "items": [{"icon": "cart", "label": "Achat du pull", "sub": "5 € + frais + livraison", "value": "−10 €", "at": "3:1", "color": "down"},
                {"icon": "coin", "label": "Revente", "sub": "exemple", "value": "+25 €", "at": "4:1", "color": "up"}],
      "total": {"label": "IL TE RESTE", "color": "gold", "stages": [{"to": 15, "at": "5:1", "label": "IL TE RESTE"}]}},
    "p2": {"type": "list", "glow": "red", "chip": CHIP(2, "6:0"), "title": {"html": "Ton <em>temps</em>", "at": "6:1"}, "top": 500,
      "items": [{"icon": "basket", "label": "Chercher, laver", "value": "20 min", "at": "7:0"},
                {"icon": "phone", "label": "Photos, messages", "value": "20 min", "at": "7:1"},
                {"icon": "box", "label": "Emballer, déposer", "value": "20 min", "at": "7:2"}],
      "total": {"label": "DE L'HEURE · EXEMPLE", "color": "gold", "stages": [{"to": 15, "at": "8:1", "label": "DE L'HEURE · EXEMPLE"}]}},
    "p3": {"type": "steps", "glow": "gold", "chip": CHIP(3, "10:0"), "title": {"html": "Les <em>impôts</em>", "at": "10:1"}, "top": 520,
      "items": [{"icon": "house", "label": "Tes affaires perso", "sub": "en général non imposable", "at": "11:0", "color": "up"},
                {"icon": "cart", "label": "Acheter pour revendre", "sub": "activité commerciale à déclarer", "at": "12:1"},
                {"icon": "bank", "label": "30 ventes ou 2 000 €/an", "sub": "tes ventes transmises aux impôts", "at": "13:1", "color": "down"}]},
    "verdict": {"type": "icon", "glow": "gold", "icon": "coin", "color": "gold", "at": "14:0", "text": "Rentable <em>en petit</em>", "textAt": "14:1",
      "sub": "mais c'est un vrai travail", "subAt": "14:2"},
    "cta": CTA("avant de te lancer")},
  "post": {"caption": "Acheter 5 €, revendre 25 € : le vrai calcul de l'achat-revente. Frais, temps passé, invendus… et dès 30 ventes ou 2 000 € par an, la plateforme transmet tes ventes aux impôts. Sauvegarde cette vidéo avant de te lancer. Et toi, tu as déjà revendu un article plus cher ?",
           "hashtags": ["#vinted", "#achatrevente", "#sidehustle", "#argent"]},
  "cover": {"chip": "RENTABLE OU ARNAQUE ? · #3", "kicker": "Achat-revente : rentable ou arnaque ?", "icon": "cart"}}

# ---------------------------------------------------------------- 18 · Comment gagnent vraiment les IA gratuites
eps[18] = {"title": "Les IA gratuites", "series": "COMMENT GAGNE VRAIMENT… · #3", "short": "IA GRATUITES",
  "next": "Ta carte bancaire te coûte combien ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["DES MILLIONS DE GENS", "Des millions de gens"], ["UTILISENT L'IA GRATUITEMENT.", "utilisent l'intelligence artificielle gratuitement."], ["*ALORS, QUI PAIE ?", "Alors, qui paie ?", "boom"]]},
    S("hook", ["VOICI COMMENT", "Voici comment"], ["*LES IA GRATUITES", "les intelligences artificielles gratuites"], ["GAGNENT DE L'ARGENT.", "gagnent de l'argent."]),
    PROOF("p1", 1, "*LES ABONNEMENTS.", "les abonnements."),
    S("p1", ["LA VERSION GRATUITE", "La version gratuite"], ["*TE DONNE ENVIE", "te donne envie"], ["DE LA VERSION PAYANTE.", "de la version payante."]),
    S("p1", ["MESSAGES LIMITÉS,", "Messages limités,"], ["MEILLEUR MODÈLE RÉSERVÉ :", "meilleur modèle réservé :"], ["*ENVIRON 20 € PAR MOIS.", "environ vingt euros par mois.", "coin"]),
    PROOF("p2", 2, "*LES ENTREPRISES.", "les entreprises."),
    S("p2", ["LES APPLIS ET LES ENTREPRISES", "Les applications et les entreprises"], ["*PAIENT À L'USAGE", "paient à l'usage"], ["POUR INTÉGRER L'IA.", "pour intégrer ces outils."]),
    S("p2", ["LE CHAT D'UN SERVICE CLIENT ?", "Le chat d'un service client ?"], ["*SOUVENT, C'EST UNE IA", "Souvent, c'est une intelligence artificielle"], ["FACTURÉE À L'USAGE.", "facturée à l'usage."]),
    PROOF("p3", 3, "*LES INVESTISSEURS.", "les investisseurs."),
    S("p3", ["FAIRE TOURNER CES MODÈLES", "Faire tourner ces modèles"], ["*COÛTE TRÈS CHER EN SERVEURS.", "coûte très cher en serveurs."]),
    S("p3", ["DES MILLIARDS SONT INVESTIS", "Des milliards sont investis"], ["*EN PARIANT SUR LES PROFITS", "en pariant sur les profits"], ["DE DEMAIN.", "de demain."]),
    S("astuce", ["ET TES CONVERSATIONS", "Et tes conversations"], ["*PEUVENT SERVIR À ENTRAÎNER LES MODÈLES,", "peuvent servir à entraîner les modèles,"], ["SELON TES RÉGLAGES.", "selon tes réglages."]),
    S("astuce", ["ASTUCE :", "Astuce :"], ["*VÉRIFIE CE RÉGLAGE", "vérifie ce réglage"], ["DANS LES PARAMÈTRES.", "dans les paramètres."]),
    VERDICT(["*GRATUIT POUR TOI,", "gratuit pour toi,"], ["PAYÉ PAR LES AUTRES.", "payé par les abonnés, les entreprises et les investisseurs."]),
    SAVE("AVANT DE PAYER UNE IA.", "avant de payer un abonnement."),
    ASK("GRATUIT OU PAYANT ?", "tu utilises la version gratuite ou payante ?")],
  "shakes": ["0:2"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "robot",
      "lines": [{"text": "Des millions", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "l'utilisent gratuitement", "at": "0:1", "size": "m"},
                {"text": "qui paie ?", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Comment gagnent les <em>IA gratuites</em>", "at": "1:1"}},
    "p1": {"type": "counter", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "Les <em>abonnements</em>", "at": "2:1"}, "label": "Version payante · prix indicatif", "color": "gold",
      "stages": [{"to": 20, "at": "4:2", "label": "PAR MOIS"}, {"to": 240, "at": "4:end", "label": "PAR AN", "dur": 1.1}],
      "disclaimer": "Prix indicatif : vérifie le tarif de chaque service"},
    "p2": {"type": "steps", "glow": "gold", "chip": CHIP(2, "5:0"), "title": {"html": "Les <em>entreprises</em>", "at": "5:1"}, "top": 520,
      "items": [{"icon": "phone", "label": "Une appli, un site", "sub": "intègre l'IA", "at": "6:0"},
                {"icon": "coin", "label": "Payée à l'usage", "sub": "à chaque utilisation", "at": "6:1", "color": "gold"},
                {"icon": "envelope", "label": "Ex. : le chat du SAV", "sub": "souvent une IA", "at": "7:1"}]},
    "p3": {"type": "icon", "glow": "gold", "chip": CHIP(3, "8:0"), "icon": "bank", "color": "gold", "at": "8:0", "text": "Les <em>investisseurs</em>", "textAt": "8:1",
      "sub": "des serveurs très chers, financés en pariant sur demain", "subAt": "9:1"},
    "astuce": {"type": "icon", "glow": "red", "icon": "alert", "color": "gold", "at": "11:0", "text": "Tes <em>conversations</em>", "textAt": "11:1",
      "sub": "selon tes réglages : vérifie-les", "subAt": "12:1"},
    "verdict": {"type": "icon", "glow": "gold", "icon": "robot", "color": "gold", "at": "13:0", "text": "Gratuit <em>pour toi</em>", "textAt": "13:1",
      "sub": "payé par les abonnés, les entreprises et les investisseurs", "subAt": "13:2"},
    "cta": CTA("avant de payer une IA")},
  "post": {"caption": "Comment gagnent vraiment les IA gratuites ? Les abonnements payants, les entreprises qui paient à l'usage, et les investisseurs qui financent les serveurs. Et selon tes réglages, tes conversations peuvent servir à entraîner les modèles. Sauvegarde cette vidéo avant de payer une IA. Et toi, version gratuite ou payante ?",
           "hashtags": ["#ia", "#intelligenceartificielle", "#argent", "#tech"]},
  "cover": {"chip": "COMMENT GAGNE… · #3", "kicker": "Les IA gratuites : qui paie ?", "icon": "robot"}}

# ---------------------------------------------------------------- 19 · 1 erreur : la carte bancaire haut de gamme
eps[19] = {"title": "La carte premium", "series": "1 ERREUR QUI TE COÛTE · #3", "short": "CARTE PREMIUM",
  "next": "Comptes faceless : rentable ou arnaque ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TA CARTE BANCAIRE", "Ta carte bancaire"], ["*TE COÛTE PEUT-ÊTRE 150 € PAR AN", "te coûte peut-être cent cinquante euros par an"], ["POUR RIEN.", "pour rien.", "boom"]]},
    S("hook", ["C'EST L'ERREUR :", "C'est l'erreur :"], ["*GARDER UNE CARTE PREMIUM", "garder une carte haut de gamme"], ["SANS T'EN SERVIR.", "sans t'en servir."]),
    PROOF("p1", 1, "*LE PRIX.", "le prix."),
    S("p1", ["CARTE HAUT DE GAMME :", "Carte haut de gamme :"], ["*130 À 150 € PAR AN.", "entre cent trente et cent cinquante euros par an."]),
    S("p1", ["CARTE CLASSIQUE :", "Carte classique :"], ["*ENVIRON 40 €.", "environ quarante euros."]),
    S("p1", ["ET DANS CERTAINES BANQUES EN LIGNE,", "Et dans certaines banques en ligne,"], ["*0 €.", "zéro euro.", "coin"]),
    PROOF("p2", 2, "*LES ASSURANCES.", "les assurances."),
    S("p2", ["VOYAGE, LOCATION DE VOITURE…", "Voyage, location de voiture…"], ["*SOUVENT, ELLES NE MARCHENT QUE SI", "souvent, elles ne marchent que si"], ["TU AS PAYÉ AVEC LA CARTE.", "tu as payé avec la carte."]),
    S("p2", ["ET TU ES PEUT-ÊTRE DÉJÀ COUVERT", "Et tu es peut-être déjà couvert"], ["*PAR TON ASSURANCE HABITATION", "par ton assurance habitation"], ["OU TA MUTUELLE.", "ou ta mutuelle."]),
    PROOF("p3", 3, "*LES PLAFONDS.", "les plafonds."),
    S("p3", ["DES PLAFONDS PLUS HAUTS :", "Des plafonds plus hauts :"], ["*UTILE SEULEMENT", "utile seulement"], ["SI TU DÉPENSES BEAUCOUP.", "si tu dépenses beaucoup."]),
    S("p3", ["SINON, TU PAIES", "Sinon, tu paies"], ["*POUR UN SERVICE QUE TU N'UTILISES PAS.", "pour un service que tu n'utilises pas."]),
    S("astuce", ["ASTUCE :", "Astuce :"], ["*DEMANDE À TA BANQUE", "demande à ta banque"], ["DE PASSER À LA CARTE CLASSIQUE.", "de passer à la carte classique."]),
    VERDICT(["*JUSQU'À 110 € D'ÉCONOMIE", "jusqu'à cent dix euros d'économie"], ["PAR AN.", "par an."]),
    SAVE("AVANT TON RENDEZ-VOUS À LA BANQUE.", "avant ton prochain rendez-vous à la banque."),
    ASK("CLASSIQUE OU HAUT DE GAMME ?", "tu as quelle carte, classique ou haut de gamme ?")],
  "shakes": ["0:2"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "card",
      "lines": [{"text": "150 €", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "par an", "at": "0:0+0.3", "size": "m"},
                {"text": "ta carte", "at": "0:1", "size": "m"}, {"text": "pour rien ?", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Garder une <em>carte premium</em>", "at": "1:1"}},
    "p1": {"type": "bars", "glow": "red", "chip": CHIP(1, "2:0"), "title": {"html": "Le <em>prix</em>", "at": "2:1"}, "label": "Par an · prix indicatifs", "top": 520,
      "items": [{"label": "Haut de gamme", "sub": "130 à 150 €", "value": 150, "color": "down", "at": "3:1"},
                {"label": "Classique", "sub": "environ", "value": 40, "color": "gold", "at": "4:1"},
                {"label": "Banque en ligne", "sub": "sous conditions", "value": 0, "color": "up", "at": "5:1"}]},
    "p2": {"type": "steps", "glow": "gold", "chip": CHIP(2, "6:0"), "title": {"html": "Les <em>assurances</em>", "at": "6:1"}, "top": 520,
      "items": [{"icon": "bus", "label": "Voyage, location", "sub": "couverts si payés avec la carte", "at": "7:0"},
                {"icon": "alert", "label": "Conditions strictes", "sub": "lis les garanties", "at": "7:1", "color": "down"},
                {"icon": "house", "label": "Déjà couvert ?", "sub": "habitation ou mutuelle", "at": "8:1", "color": "up"}]},
    "p3": {"type": "icon", "glow": "red", "chip": CHIP(3, "9:0"), "icon": "card", "color": "down", "at": "9:0", "text": "Des plafonds <em>plus hauts</em>", "textAt": "10:0",
      "sub": "utile seulement si tu dépenses beaucoup", "subAt": "10:1"},
    "astuce": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "12:0", "text": "Passe à la <em>carte classique</em>", "textAt": "12:1",
      "sub": "demande-le simplement à ta banque", "subAt": "12:2"},
    "verdict": {"type": "counter", "glow": "green", "title": {"html": "Ton <em>économie</em>", "at": "13:0"}, "label": "Premium → classique · exemple", "color": "up",
      "stages": [{"to": 110, "at": "13:1", "label": "PAR AN"}]},
    "cta": CTA("avant ton rendez-vous à la banque")},
  "post": {"caption": "Ta carte bancaire haut de gamme te coûte peut-être 150 € par an. Ses assurances ne marchent souvent que si tu paies avec, et tu es peut-être déjà couvert par ton assurance habitation ou ta mutuelle. Sauvegarde cette vidéo avant ton prochain rendez-vous à la banque. Et toi, carte classique ou haut de gamme ?",
           "hashtags": ["#banque", "#cartebancaire", "#fraisbancaires", "#economiser"]},
  "cover": {"chip": "1 ERREUR · #3", "kicker": "Ta carte te coûte 150 € par an ?", "icon": "card"}}

# ---------------------------------------------------------------- 20 · Rentable ou arnaque : les comptes faceless
eps[20] = {"title": "Les comptes faceless", "series": "RENTABLE OU ARNAQUE ? · #4", "short": "FACELESS IA", "next": None,
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["100 VIDÉOS PAR JOUR", "Cent vidéos par jour"], ["AVEC L'IA,", "avec l'intelligence artificielle,"], ["*SANS MONTRER TON VISAGE ?", "sans montrer ton visage ?", "boom"]]},
    S("hook", ["LES COMPTES FACELESS :", "Les comptes sans visage :"], ["*RENTABLE OU ARNAQUE ?", "rentable ou arnaque ?"]),
    PROOF("p1", 1, "*LES VUES NE PAIENT PAS TOUT DE SUITE.", "les vues ne paient pas tout de suite."),
    S("p1", ["POUR ÊTRE PAYÉ PAR TIKTOK,", "Pour être payé par TikTok,"], ["*IL FAUT AU MOINS 10 000 ABONNÉS", "il faut au moins dix mille abonnés"], ["ET 100 000 VUES EN 30 JOURS.", "et cent mille vues en trente jours."]),
    S("p1", ["ET SEULES COMPTENT", "Et seules comptent"], ["*LES VIDÉOS DE PLUS D'UNE MINUTE.", "les vidéos de plus d'une minute."]),
    PROOF("p2", 2, "*LE COPIÉ-COLLÉ.", "le copié-collé."),
    S("p2", ["LES CONTENUS PAS ORIGINAUX", "Les contenus pas originaux"], ["*NE SONT PAS RÉMUNÉRÉS,", "ne sont pas rémunérés,"], ["ET SONT MOINS MONTRÉS.", "et sont moins montrés."]),
    S("p2", ["100 VIDÉOS À LA CHAÎNE ?", "Cent vidéos à la chaîne ?"], ["*SOUVENT, PRESQUE PERSONNE", "Souvent, presque personne"], ["NE LES VOIT.", "ne les voit."]),
    S("p2", ["ET LES CONTENUS RÉALISTES FAITS PAR IA", "Et les contenus réalistes faits par l'intelligence artificielle"], ["*DOIVENT ÊTRE SIGNALÉS.", "doivent être signalés."]),
    PROOF("p3", 3, "*QUI GAGNE VRAIMENT ?", "qui gagne vraiment ?"),
    S("p3", ["CEUX QUI VENDENT", "Ceux qui vendent"], ["*LES OUTILS ET LES FORMATIONS", "les outils et les formations"], ["POUR CRÉER CES COMPTES.", "pour créer ces comptes."]),
    S("p3", ["UN ABONNEMENT À 30 € PAR MOIS,", "Un abonnement à trente euros par mois,"], ["*QUE TU GAGNES DE L'ARGENT OU PAS.", "que tu gagnes de l'argent ou pas.", "stamp"]),
    VERDICT(["*PAS UNE ARNAQUE,", "pas une arnaque,"], ["MAIS L'IA NE FAIT PAS TOUT.", "mais l'intelligence artificielle ne fait pas tout."]),
    S("verdict", ["CE QUI MARCHE :", "Ce qui marche :"], ["*DES VIDÉOS ORIGINALES ET UTILES,", "des vidéos originales et utiles,"], ["PUBLIÉES RÉGULIÈREMENT.", "publiées régulièrement."]),
    SAVE("AVANT D'ACHETER UN OUTIL FACELESS.", "avant d'acheter un outil pour comptes sans visage."),
    ASK("TU SUIS DES COMPTES FACELESS ?", "tu suis des comptes sans visage ?")],
  "shakes": ["0:2", "11:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "play",
      "lines": [{"text": "100 vidéos", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "par jour avec l'IA", "at": "0:1", "size": "m"},
                {"text": "sans visage ?", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Comptes faceless : <em>rentable</em> ?", "at": "1:1"}},
    "p1": {"type": "list", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "Les vues <em>ne paient pas</em>", "at": "2:1"}, "top": 500,
      "items": [{"icon": "check", "label": "10 000 abonnés", "sub": "minimum", "value": "1", "at": "3:1", "color": "gold"},
                {"icon": "play", "label": "100 000 vues", "sub": "en 30 jours", "value": "2", "at": "3:2", "color": "gold"},
                {"icon": "clock", "label": "Plus d'1 minute", "sub": "seules ces vidéos comptent", "value": "3", "at": "4:1", "color": "gold"}]},
    "p2": {"type": "steps", "glow": "red", "chip": CHIP(2, "5:0"), "title": {"html": "Le <em>copié-collé</em>", "at": "5:1"}, "top": 520,
      "items": [{"icon": "cross", "label": "Pas original", "sub": "pas rémunéré, moins montré", "at": "6:1", "color": "down"},
                {"icon": "play", "label": "100 vidéos à la chaîne", "sub": "presque personne ne les voit", "at": "7:1", "color": "down"},
                {"icon": "robot", "label": "IA réaliste", "sub": "à signaler comme telle", "at": "8:1"}]},
    "p3": {"type": "counter", "glow": "red", "chip": CHIP(3, "9:0"), "title": {"html": "Qui gagne <em>vraiment</em> ?", "at": "9:1"}, "label": "Outil faceless · exemple", "color": "down",
      "stages": [{"to": 30, "at": "11:0", "label": "PAR MOIS"}, {"to": 360, "at": "11:1", "label": "PAR AN, GAGNANT OU PAS", "dur": 1.1}]},
    "verdict": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "12:0", "text": "Pas une arnaque, <em>pas magique</em>", "textAt": "12:1",
      "sub": "des vidéos originales et utiles, publiées régulièrement", "subAt": "13:1"},
    "cta": CTA("avant d'acheter un outil faceless")},
  "post": {"caption": "100 vidéos par jour avec l'IA sans montrer ton visage : rentable ou arnaque ? Pour être payé par TikTok, il faut 10 000 abonnés, 100 000 vues en 30 jours et des vidéos de plus d'une minute. Le copié-collé n'est pas rémunéré. Sauvegarde cette vidéo avant d'acheter un outil faceless. Et toi, tu suis des comptes sans visage ?",
           "hashtags": ["#faceless", "#ia", "#sidehustle", "#tiktok"]},
  "cover": {"chip": "RENTABLE OU ARNAQUE ? · #4", "kicker": "Comptes faceless : rentable ou arnaque ?", "icon": "play"}}

(OUT / "scripts").mkdir(exist_ok=True)
(OUT / "descriptions").mkdir(exist_ok=True)
for n, e in eps.items():
    data = {"_doc": "Semaine 3 : voir serie/semaine3.py.", "ep": n, **COMMON, **e}
    (OUT / f"ep{n:02d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    # Texte à lire si tu enregistres ta propre voix (une phrase par ligne).
    (OUT / "scripts" / f"ep{n:02d}.txt").write_text(
        "\n".join(" ".join(c[1] for c in s["chunks"]) for s in e["sentences"]) + "\n", encoding="utf-8")
    (OUT / "descriptions" / f"ep{n:02d}.txt").write_text(
        e["post"]["caption"] + "\n\n" + " ".join(e["post"]["hashtags"]) + "\n", encoding="utf-8")
print("ok", sorted(eps))
