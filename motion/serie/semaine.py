#!/usr/bin/env python3
"""
Semaine 2 : 5 vidéos de 45 à 70 s, même structure pour toutes.

    affirmation surprenante (1re seconde) → 3 preuves visuelles → « sauvegarde cette vidéo
    avant de… » → une question pour faire commenter.

    python3 serie/semaine.py      # écrit serie/ep11.json … ep15.json et serie/scripts/epNN.txt

Les montants « exemple » sont signalés comme tels à l'écran.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
COMMON = {"voice": "siwis-medium", "speed": 1.0, "lead": 0.3, "gap": 0.18, "duration": "auto", "tail": 1.6,
          "handle": "@epargne.malin7"}
P = lambda n, what: [f"PREUVE NUMÉRO {n} :", f"Preuve numéro {['un', 'deux', 'trois'][n - 1]} :"]
SAVE = lambda show, say: {"segment": "cta", "sfx": "whoosh", "pause": 0.1, "chunks": [["*SAUVEGARDE CETTE VIDÉO", "Sauvegarde cette vidéo"], [show, say]]}
ASK = lambda show, say: {"segment": "cta", "chunks": [["ET TOI,", "Et toi,"], [show, say], ["*DIS-LE EN COMMENTAIRE.", "Dis-le en commentaire."]]}
CHIP = lambda n, at, label="PREUVE": {"text": f"{label} {n} / 3", "at": at, **({"color": "red"} if label == "SIGNAL" else {})}

eps = {}

# ---------------------------------------------------------------- 11 · 1 erreur : cumuler les IA
eps[11] = {"title": "Les abonnements IA", "series": "1 ERREUR QUI TE COÛTE · #1", "short": "ABONNEMENTS IA", "next": "Comment gagne vraiment ta banque ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["*720 € PAR AN", "Sept cent vingt euros par an"], ["POUR DES IA", "pour des IA"], ["QUE TU UTILISES À PEINE.", "que tu utilises à peine.", "boom"]]},
    {"segment": "hook", "chunks": [["C'EST L'ERREUR :", "C'est l'erreur :"], ["*CUMULER LES ABONNEMENTS IA.", "cumuler les abonnements d'intelligence artificielle."]]},
    {"segment": "p1", "sfx": "whoosh", "pause": 0.1, "chunks": [P(1, ""), ["*LE PRIX.", "le prix."]]},
    {"segment": "p1", "chunks": [["UN ABONNEMENT IA,", "Un abonnement IA,"], ["C'EST SOUVENT", "c'est souvent"], ["*ENVIRON 20 € PAR MOIS.", "environ vingt euros par mois."]]},
    {"segment": "p1", "chunks": [["TROIS ABONNEMENTS :", "Trois abonnements :"], ["*60 € PAR MOIS.", "soixante euros par mois."], ["*720 € SUR UN AN.", "Et sur un an : sept cent vingt euros.", "coin"]]},
    {"segment": "p2", "sfx": "whoosh", "pause": 0.1, "chunks": [P(2, ""), ["*TON USAGE RÉEL.", "ton usage réel."]]},
    {"segment": "p2", "chunks": [["REGARDE TON HISTORIQUE :", "Regarde ton historique :"], ["TU UTILISES VRAIMENT", "tu utilises vraiment"], ["*LES TROIS CHAQUE SEMAINE ?", "les trois chaque semaine ?"]]},
    {"segment": "p2", "chunks": [["SI DEUX NE SERVENT PAS,", "Si deux ne servent pas,"], ["*480 € PAR AN", "ça fait quatre cent quatre-vingts euros par an", "stamp"], ["POUR RIEN.", "pour rien."]]},
    {"segment": "p3", "sfx": "whoosh", "pause": 0.1, "chunks": [P(3, ""), ["LES VERSIONS GRATUITES", "les versions gratuites"], ["*SUFFISENT SOUVENT.", "suffisent souvent."]]},
    {"segment": "p3", "chunks": [["GARDE UN SEUL ABONNEMENT,", "Garde un seul abonnement,"], ["*ET PAIE LES AUTRES", "et paie les autres"], ["UN MOIS, SI BESOIN.", "un mois, seulement si besoin."]]},
    SAVE("AVANT DE T'ABONNER.", "avant de t'abonner."),
    ASK("TU PAIES COMBIEN D'IA ?", "tu paies combien d'IA ?")],
  "shakes": ["0:2", "7:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "robot",
      "lines": [{"text": "720 €", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "par an", "at": "0:0+0.3", "size": "m"},
                {"text": "pour des IA", "at": "0:1", "size": "m"}, {"text": "inutiles ?", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Cumuler les <em>abonnements IA</em>", "at": "1:1"}},
    "p1": {"type": "counter", "glow": "red", "chip": CHIP(1, "2:0"), "title": {"html": "Le <em>prix</em>", "at": "2:1"}, "label": "Abonnements IA", "color": "down",
      "stages": [{"to": 20, "at": "3:2", "label": "PAR MOIS · 1 IA"}, {"to": 60, "at": "4:1", "label": "PAR MOIS · 3 IA"}, {"to": 720, "at": "4:2", "label": "PAR AN · 3 IA", "dur": 1.1}],
      "disclaimer": "Prix indicatifs : vérifie le tarif de chaque service"},
    "p2": {"type": "list", "glow": "red", "chip": CHIP(2, "5:0"), "title": {"html": "Ton <em>usage réel</em>", "at": "5:1"}, "top": 500,
      "items": [{"icon": "robot", "label": "IA n°1", "sub": "tous les jours", "value": "20 €/mois", "at": "6:0", "color": "up"},
                {"icon": "robot", "label": "IA n°2", "sub": "une fois par mois", "value": "20 €/mois", "at": "6:1", "color": "down"},
                {"icon": "robot", "label": "IA n°3", "sub": "oubliée", "value": "20 €/mois", "at": "6:2", "color": "down"}],
      "total": {"label": "POUR RIEN", "color": "down", "stages": [{"to": 480, "at": "7:1", "label": "PAR AN · POUR RIEN"}]}},
    "p3": {"type": "steps", "glow": "green", "chip": CHIP(3, "8:0"), "title": {"html": "Le <em>bon réflexe</em>", "at": "8:1"}, "top": 500,
      "items": [{"icon": "check", "label": "1 seule IA payante", "sub": "celle que tu utilises vraiment", "at": "9:0", "color": "up"},
                {"icon": "bolt", "label": "Les autres en gratuit", "sub": "elles suffisent souvent", "at": "9:1"},
                {"icon": "calendar", "label": "1 mois payant", "sub": "seulement si besoin", "at": "9:2"}]},
    "cta": {"type": "cta", "glow": "gold", "save": True, "heading": "<em>Sauvegarde</em>-la", "sub": "avant de t'abonner"}},
  "post": {"caption": "Cumuler les abonnements IA, c'est vite 720 € par an. Garde un seul abonnement, celui que tu utilises vraiment, et passe les autres en version gratuite. Sauvegarde cette vidéo avant de t'abonner. Et toi, tu paies combien d'IA ?",
           "hashtags": ["#ia", "#abonnements", "#economiser", "#argent"]},
  "cover": {"chip": "1 ERREUR · #1", "kicker": "720 € par an d'IA", "icon": "robot"}}

# ---------------------------------------------------------------- 12 · Comment gagne vraiment ta banque
eps[12] = {"title": "Ta banque", "series": "COMMENT GAGNE VRAIMENT… · #1", "short": "TA BANQUE", "next": "Dropshipping : rentable ou arnaque ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TON COMPTE EST GRATUIT ?", "Ton compte est gratuit ?"], ["*TA BANQUE GAGNE", "Ta banque gagne"], ["QUAND MÊME SUR TOI.", "quand même de l'argent sur toi.", "boom"]]},
    {"segment": "hook", "chunks": [["VOICI", "Voici"], ["*SES 3 SOURCES DE REVENUS.", "ses trois sources de revenus."]]},
    {"segment": "p1", "sfx": "whoosh", "pause": 0.1, "chunks": [P(1, ""), ["*LA MARGE D'INTÉRÊTS.", "la marge d'intérêts."]]},
    {"segment": "p1", "chunks": [["TON COMPTE COURANT", "Ton compte courant"], ["TE RAPPORTE 0 %.", "te rapporte zéro pour cent."]]},
    {"segment": "p1", "chunks": [["ELLE, ELLE PRÊTE", "Elle, elle prête"], ["*AVEC INTÉRÊTS.", "avec intérêts."]]},
    {"segment": "p1", "chunks": [["LA DIFFÉRENCE ?", "La différence ?"], ["*C'EST POUR ELLE.", "C'est pour elle.", "coin"]]},
    {"segment": "p2", "sfx": "whoosh", "pause": 0.1, "chunks": [P(2, ""), ["*LES FRAIS.", "les frais."]]},
    {"segment": "p2", "chunks": [["CARTE,", "Carte,"], ["TENUE DE COMPTE,", "tenue de compte,"], ["*INCIDENTS :", "incidents :"], ["LA FACTURE GRIMPE.", "la facture grimpe."]]},
    {"segment": "p3", "sfx": "whoosh", "pause": 0.1, "chunks": [P(3, ""), ["*CHAQUE PAIEMENT PAR CARTE.", "chaque paiement par carte."]]},
    {"segment": "p3", "chunks": [["LE COMMERÇANT PAIE", "Le commerçant paie"], ["UNE COMMISSION,", "une commission,"], ["*ET UNE PART", "et une part"], ["REVIENT À TA BANQUE.", "revient à ta banque."]]},
    SAVE("AVANT DE CHOISIR TA BANQUE.", "avant de choisir ta banque."),
    ASK("COMBIEN DE FRAIS PAR AN ?", "tu paies combien de frais par an ?")],
  "shakes": ["0:2"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "bank",
      "lines": [{"text": "Compte gratuit ?", "at": "0:0-0.6", "size": "m"}, {"text": "ta banque", "at": "0:1", "size": "m"},
                {"text": "gagne", "at": "0:1+0.3", "size": "xl", "hl": True}, {"text": "quand même", "at": "0:2", "size": "m"}],
      "reveal": {"html": "Ses <em>3 sources</em> de revenus", "at": "1:1"}},
    "p1": {"type": "bars", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "La marge <em>d'intérêts</em>", "at": "2:1"}, "label": "Exemple", "format": "pct", "top": 520, "max": 5,
      "items": [{"label": "Ton compte courant", "sub": "ce qu'il te rapporte", "value": 0, "color": "down", "at": "3:0"},
                {"label": "Un crédit", "sub": "ce qu'elle facture", "value": 4, "color": "gold", "at": "4:1"}],
      "badge": {"text": "MARGE", "small": "POUR LA BANQUE", "at": "5:1", "color": "gold"}},
    "p2": {"type": "list", "glow": "red", "chip": CHIP(2, "6:0"), "title": {"html": "Les <em>frais</em>", "at": "6:1"}, "top": 500,
      "items": [{"icon": "card", "label": "Cotisation carte", "sub": "exemple", "value": "45 €/an", "at": "7:0", "color": "down"},
                {"icon": "bank", "label": "Tenue de compte", "sub": "exemple", "value": "24 €/an", "at": "7:1", "color": "down"},
                {"icon": "alert", "label": "Rejet de prélèvement", "sub": "jusqu'à 20 € chacun", "value": "20 €", "at": "7:2", "color": "down"}],
      "total": {"label": "PAR AN", "color": "down", "stages": [{"to": 89, "at": "7:3", "label": "PAR AN · EXEMPLE"}]}},
    "p3": {"type": "steps", "glow": "gold", "chip": CHIP(3, "8:0"), "title": {"html": "La commission <em>d'interchange</em>", "at": "8:1"}, "top": 520,
      "items": [{"icon": "card", "label": "Tu paies 50 € par carte", "sub": "chez un commerçant", "at": "9:0"},
                {"icon": "basket", "label": "Commission du commerçant", "sub": "sur chaque paiement", "at": "9:1"},
                {"icon": "bank", "label": "Une part pour ta banque", "sub": "0,2 à 0,3 % max. en Europe", "at": "9:2", "color": "gold"}]},
    "cta": {"type": "cta", "glow": "gold", "save": True, "heading": "<em>Sauvegarde</em>-la", "sub": "avant de choisir ta banque"}},
  "post": {"caption": "Comment gagne vraiment ta banque ? La marge d'intérêts, les frais, et une commission à chaque paiement par carte. Sauvegarde cette vidéo avant de choisir ta banque. Et toi, tu paies combien de frais par an ?",
           "hashtags": ["#banque", "#fraisbancaires", "#argent", "#financepersonnelle"]},
  "cover": {"chip": "COMMENT GAGNE… · #1", "kicker": "Comment gagne vraiment ta banque ?", "icon": "bank"}}

# ---------------------------------------------------------------- 13 · Dropshipping : rentable ou arnaque
eps[13] = {"title": "Le dropshipping", "series": "RENTABLE OU ARNAQUE ? · #1", "short": "DROPSHIPPING", "next": "Formations IA : rentable ou arnaque ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["LE DROPSHIPPING", "Le dropshipping"], ["N'EST PAS UNE ARNAQUE…", "n'est pas une arnaque…"], ["*MAIS BEAUCOUP PERDENT DE L'ARGENT.", "mais beaucoup perdent de l'argent.", "boom"]]},
    {"segment": "hook", "chunks": [["ALORS, RENTABLE OU ARNAQUE ?", "Alors, rentable ou arnaque ?"], ["*VOICI 3 PREUVES.", "Voici trois preuves."]]},
    {"segment": "p1", "sfx": "whoosh", "pause": 0.1, "chunks": [P(1, ""), ["*LE VRAI CALCUL.", "le vrai calcul."]]},
    {"segment": "p1", "chunks": [["PRIX DE VENTE :", "Prix de vente :"], ["*30 €.", "trente euros."]]},
    {"segment": "p1", "chunks": [["PRODUIT ET LIVRAISON :", "Produit et livraison :"], ["*12 €.", "douze euros."]]},
    {"segment": "p1", "chunks": [["PUBLICITÉ PAR VENTE :", "Publicité par vente :"], ["*15 €.", "quinze euros."]]},
    {"segment": "p1", "chunks": [["IL TE RESTE", "Il te reste"], ["*3 €,", "trois euros,", "stamp"], ["AVANT LES RETOURS.", "avant les retours."]]},
    {"segment": "p2", "sfx": "whoosh", "pause": 0.1, "chunks": [P(2, ""), ["*LE SERVICE CLIENT.", "le service client."]]},
    {"segment": "p2", "chunks": [["RETARDS DE LIVRAISON,", "Retards de livraison,"], ["CLIENTS MÉCONTENTS,", "clients mécontents,"], ["*REMBOURSEMENTS.", "remboursements."]]},
    {"segment": "p3", "sfx": "whoosh", "pause": 0.1, "chunks": [P(3, ""), ["*LA CONCURRENCE.", "la concurrence."]]},
    {"segment": "p3", "chunks": [["LE MÊME PRODUIT", "Le même produit"], ["EST VENDU", "est vendu"], ["*PAR DES DIZAINES DE BOUTIQUES.", "par des dizaines d'autres boutiques."]]},
    {"segment": "verdict", "sfx": "whoosh", "pause": 0.1, "chunks": [["VERDICT :", "Verdict :"], ["*PAS UNE ARNAQUE,", "pas une arnaque,"], ["MAIS PAS DE L'ARGENT FACILE.", "mais pas de l'argent facile."]]},
    SAVE("AVANT DE TE LANCER.", "avant de te lancer."),
    ASK("TU AS DÉJÀ ESSAYÉ ?", "tu as déjà essayé ?")],
  "shakes": ["0:2", "6:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "box",
      "lines": [{"text": "Dropshipping", "at": "0:0-0.6", "size": "m"}, {"text": "pas une arnaque…", "at": "0:1", "size": "m"},
                {"text": "mais beaucoup", "at": "0:2", "size": "m"}, {"text": "perdent", "at": "0:2+0.35", "size": "xl", "hl": True}],
      "reveal": {"html": "Rentable ou <em>arnaque</em> ?", "at": "1:0"}},
    "p1": {"type": "list", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "Le <em>vrai calcul</em>", "at": "2:1"}, "top": 500,
      "items": [{"icon": "basket", "label": "Prix de vente", "sub": "exemple", "value": "+30 €", "at": "3:1", "color": "up"},
                {"icon": "box", "label": "Produit + livraison", "value": "−12 €", "at": "4:0", "color": "down"},
                {"icon": "phone", "label": "Publicité par vente", "value": "−15 €", "at": "5:0", "color": "down"}],
      "total": {"label": "IL TE RESTE", "color": "gold", "stages": [{"to": 3, "at": "6:1", "label": "IL TE RESTE"}]}},
    "p2": {"type": "icon", "glow": "red", "chip": CHIP(2, "7:0"), "icon": "box", "color": "down", "at": "7:0", "text": "Le <em>service client</em>", "textAt": "7:1",
      "sub": "Délais, retours, remboursements : c'est toi qui gères", "subAt": "8:0"},
    "p3": {"type": "grid", "glow": "red", "chip": CHIP(3, "9:0"), "title": {"html": "La <em>concurrence</em>", "at": "9:1"}, "top": 480, "cells": 40, "cols": 10, "format": "n",
      "fill": [[40, "10:0", "10:end"]], "counter": {"label": "Boutiques, même produit", "mode": "count"},
      "badge": {"text": "×40", "small": "MÊME PRODUIT", "at": "10:2", "color": "red"}},
    "verdict": {"type": "icon", "glow": "gold", "icon": "alert", "color": "gold", "at": "11:0", "text": "Pas une arnaque, <em>pas facile</em>", "textAt": "11:1",
      "sub": "Méfie-toi surtout des formations qui le vendent", "subAt": "11:2"},
    "cta": {"type": "cta", "glow": "gold", "save": True, "heading": "<em>Sauvegarde</em>-la", "sub": "avant de te lancer"}},
  "post": {"caption": "Dropshipping : business rentable ou arnaque ? Pas une arnaque, mais le calcul est souvent serré : pub, livraison, retours, concurrence. Sauvegarde cette vidéo avant de te lancer. Et toi, tu as déjà essayé ?",
           "hashtags": ["#dropshipping", "#sidehustle", "#business", "#argent"]},
  "cover": {"chip": "RENTABLE OU ARNAQUE ? · #1", "kicker": "Dropshipping : rentable ou arnaque ?", "icon": "box"}}

# ---------------------------------------------------------------- 14 · Formations IA : rentable ou arnaque
eps[14] = {"title": "Les formations IA", "series": "RENTABLE OU ARNAQUE ? · #2", "short": "FORMATIONS IA", "next": "Comment gagnent les applis gratuites ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["« 5 000 € PAR MOIS", "Cinq mille euros par mois"], ["AVEC L'IA » ?", "avec l'IA ?"], ["SOUVENT, LE SEUL QUI GAGNE,", "Souvent, le seul qui gagne,"], ["*C'EST LE VENDEUR.", "c'est le vendeur.", "boom"]]},
    {"segment": "hook", "chunks": [["*3 SIGNAUX", "Trois signaux"], ["POUR REPÉRER L'ARNAQUE.", "pour repérer l'arnaque."]]},
    {"segment": "s1", "sfx": "whoosh", "pause": 0.1, "chunks": [["SIGNAL NUMÉRO 1 :", "Signal numéro un :"], ["*DES REVENUS SANS PREUVE.", "des revenus sans preuve."]]},
    {"segment": "s1", "chunks": [["CAPTURES D'ÉCRAN,", "Captures d'écran,"], ["VOITURES DE LUXE…", "voitures de luxe…"], ["*JAMAIS DE FACTURES.", "mais jamais de factures."]]},
    {"segment": "s2", "sfx": "whoosh", "pause": 0.1, "chunks": [["SIGNAL NUMÉRO 2 :", "Signal numéro deux :"], ["*L'URGENCE.", "l'urgence."]]},
    {"segment": "s2", "chunks": [["« PLUS QUE 3 PLACES »,", "Plus que trois places,"], ["*« LE PRIX DOUBLE CE SOIR ».", "le prix double ce soir."]]},
    {"segment": "s3", "sfx": "whoosh", "pause": 0.1, "chunks": [["SIGNAL NUMÉRO 3 :", "Signal numéro trois :"], ["*LE VRAI BUSINESS,", "le vrai business,"], ["C'EST LA FORMATION.", "c'est la formation."]]},
    {"segment": "s3", "chunks": [["1 000 ÉLÈVES À 500 €,", "Mille élèves à cinq cents euros,"], ["*C'EST 500 000 €", "c'est cinq cent mille euros"], ["POUR LE VENDEUR.", "pour le vendeur.", "coin"]]},
    {"segment": "verdict", "sfx": "whoosh", "pause": 0.1, "chunks": [["CE QUI MARCHE VRAIMENT :", "Ce qui marche vraiment :"], ["*UNE COMPÉTENCE", "une compétence"], ["QUE DES CLIENTS PAIENT.", "que des clients paient."]]},
    SAVE("AVANT D'ACHETER UNE FORMATION.", "avant d'acheter une formation."),
    ASK("ON T'EN A DÉJÀ PROPOSÉ ?", "on t'en a déjà proposé une ?")],
  "shakes": ["0:3"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "robot",
      "lines": [{"text": "5 000 €/mois", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "avec l'IA ?", "at": "0:1", "size": "m"},
                {"text": "pour le vendeur", "at": "0:3", "size": "m", "hl": True}],
      "reveal": {"html": "<em>3 signaux</em> d'arnaque", "at": "1:0"}},
    "s1": {"type": "icon", "glow": "red", "chip": CHIP(1, "2:0", "SIGNAL"), "icon": "cross", "color": "down", "at": "2:0", "text": "Des revenus <em>sans preuve</em>", "textAt": "2:1",
      "sub": "Captures, voitures… jamais de factures", "subAt": "3:0"},
    "s2": {"type": "icon", "glow": "red", "chip": CHIP(2, "4:0", "SIGNAL"), "icon": "clock", "color": "down", "at": "4:0", "text": "L'<em>urgence</em> artificielle", "textAt": "4:1",
      "sub": "« Plus que 3 places », « le prix double ce soir »", "subAt": "5:0"},
    "s3": {"type": "counter", "glow": "gold", "chip": CHIP(3, "6:0", "SIGNAL"), "title": {"html": "Le business, <em>c'est la formation</em>", "at": "6:1"}, "label": "1 000 élèves × 500 € (exemple)", "color": "gold", "bigSize": 140,
      "stages": [{"to": 500000, "at": "7:1", "label": "POUR LE VENDEUR", "dur": 1.3}]},
    "verdict": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "8:0", "text": "Une compétence, <em>des clients</em>", "textAt": "8:1",
      "sub": "pas une formation miracle", "subAt": "8:2"},
    "cta": {"type": "cta", "glow": "gold", "save": True, "heading": "<em>Sauvegarde</em>-la", "sub": "avant d'acheter une formation"}},
  "post": {"caption": "« 5 000 € par mois avec l'IA » ? 3 signaux pour repérer une formation douteuse : des revenus sans preuve, l'urgence, et un business qui vit… de la formation. Sauvegarde cette vidéo avant d'acheter. Et toi, on t'en a déjà proposé une ?",
           "hashtags": ["#ia", "#arnaque", "#formation", "#argent"]},
  "cover": {"chip": "RENTABLE OU ARNAQUE ? · #2", "kicker": "Formations IA : rentable ou arnaque ?", "icon": "robot"}}

# ---------------------------------------------------------------- 15 · Comment gagnent les applis gratuites
eps[15] = {"title": "Les applis gratuites", "series": "COMMENT GAGNE VRAIMENT… · #2", "short": "APPLIS GRATUITES", "next": "Payer en 4 fois tes petits achats ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["SI C'EST GRATUIT,", "Si c'est gratuit,"], ["*C'EST TOI", "c'est toi"], ["LE PRODUIT.", "le produit.", "boom"]]},
    {"segment": "hook", "chunks": [["VOICI COMMENT", "Voici comment"], ["*LES APPLIS GRATUITES", "les applications gratuites"], ["GAGNENT DE L'ARGENT.", "gagnent de l'argent."]]},
    {"segment": "p1", "sfx": "whoosh", "pause": 0.1, "chunks": [P(1, ""), ["*LA PUBLICITÉ CIBLÉE.", "la publicité ciblée."]]},
    {"segment": "p1", "chunks": [["CE QUE TU REGARDES,", "Ce que tu regardes,"], ["CE QUE TU CLIQUES :", "ce que tu cliques :"], ["*ÇA SERT À CIBLER LES PUBS.", "ça sert à cibler les pubs."]]},
    {"segment": "p2", "sfx": "whoosh", "pause": 0.1, "chunks": [P(2, ""), ["*LA VERSION PREMIUM.", "la version premium."]]},
    {"segment": "p2", "chunks": [["LA PLUPART RESTENT", "La plupart restent"], ["EN VERSION GRATUITE ;", "en version gratuite ;"], ["*UNE PETITE MINORITÉ PAIE", "une petite minorité paie"], ["POUR TOUS LES AUTRES.", "pour tous les autres."]]},
    {"segment": "p3", "sfx": "whoosh", "pause": 0.1, "chunks": [P(3, ""), ["*L'ESSAI GRATUIT.", "l'essai gratuit."]]},
    {"segment": "p3", "chunks": [["7 JOURS OFFERTS,", "Sept jours offerts,"], ["PUIS TU PAIES L'ABONNEMENT", "puis tu paies l'abonnement"], ["*SI TU OUBLIES D'ANNULER.", "si tu oublies d'annuler.", "stamp"]]},
    SAVE("AVANT D'INSTALLER UNE APPLI.", "avant d'installer une application gratuite."),
    ASK("UN ESSAI OUBLIÉ ?", "tu as déjà oublié un essai gratuit ?")],
  "shakes": ["0:2", "7:2"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "phone",
      "lines": [{"text": "Gratuit ?", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "c'est toi", "at": "0:1", "size": "m"}, {"text": "le produit", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Comment gagnent les <em>applis gratuites</em>", "at": "1:1"}},
    "p1": {"type": "steps", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "La pub <em>ciblée</em>", "at": "2:1"}, "top": 520,
      "items": [{"icon": "phone", "label": "Tu utilises l'appli", "sub": "gratuitement", "at": "3:0"},
                {"icon": "bolt", "label": "Tes clics, tes goûts", "sub": "analysés", "at": "3:1"},
                {"icon": "coin", "label": "Des pubs ciblées", "sub": "vendues aux annonceurs", "at": "3:2", "color": "gold"}]},
    "p2": {"type": "donut", "glow": "gold", "chip": {"text": "PREUVE 2 / 3 · EXEMPLE", "at": "4:0"},
      "parts": [{"pct": 95, "label": "Gratuit", "color": "ink", "at": "5:0"}, {"pct": 5, "label": "Payant", "color": "gold", "at": "5:2"}],
      "final": {"big": "5 %", "small": "paient pour tous", "color": "gold", "at": "5:3", "highlight": 1}},
    "p3": {"type": "timer", "glow": "red", "chip": CHIP(3, "6:0"), "icon": "phone", "hours": 7, "unit": "j", "alarm": True, "start": "7:0", "end": "7:2",
      "meterLabel": "ESSAI GRATUIT RESTANT", "done": {"text": "Abonnement lancé automatiquement", "at": "7:2", "color": "red"}},
    "cta": {"type": "cta", "glow": "gold", "save": True, "heading": "<em>Sauvegarde</em>-la", "sub": "avant d'installer une appli"}},
  "post": {"caption": "Comment gagnent vraiment les applis gratuites ? La pub ciblée, le freemium, et l'essai gratuit qui se transforme en abonnement. Sauvegarde cette vidéo avant d'installer une appli. Et toi, tu as déjà oublié un essai gratuit ?",
           "hashtags": ["#applis", "#abonnements", "#argent", "#astuceargent"]},
  "cover": {"chip": "COMMENT GAGNE… · #2", "kicker": "Comment gagnent les applis gratuites ?", "icon": "phone"}}

# ---------------------------------------------------------------- allongement à 45–60 s
import re as _re
COMMON["speed"] = 0.97

def insert_after(e, idx, sentence):
    """Insère une phrase après la phrase idx et décale tous les instants « n:… » qui suivent."""
    e["sentences"].insert(idx + 1, sentence)
    def shift(m):
        n = int(m.group(1))
        return f'"{n + 1 if n > idx else n}:'
    e["blocks"] = json.loads(_re.sub(r'"(\d+):', shift, json.dumps(e["blocks"], ensure_ascii=False)))
    e["shakes"] = [f"{int(x.split(':')[0]) + (1 if int(x.split(':')[0]) > idx else 0)}:{x.split(':', 1)[1]}" for x in e.get("shakes", [])]

def add_segment_before_cta(e, sentences, name, block):
    i = next(k for k, x in enumerate(e["sentences"]) if x["segment"] == "cta")
    for j, snt in enumerate(sentences):
        insert_after(e, i - 1 + j, snt)
    blocks = {k: v for k, v in e["blocks"].items() if k != "cta"}
    blocks[name] = json.loads(json.dumps(block).replace('"@', f'"{i}:').replace('"#', f'"{i + 1}:'))
    blocks["cta"] = e["blocks"]["cta"]
    e["blocks"] = blocks

S = lambda seg, chunks: {"segment": seg, "chunks": chunks}
V = lambda chunks: {"segment": "verdict", "sfx": "whoosh", "pause": 0.1, "chunks": chunks}

# 11 · IA
e = eps[11]
insert_after(e, 4, S("p1", [["PLUS CHER QUE", "C'est plus cher que"], ["*STREAMING ET MUSIQUE", "le streaming et la musique"], ["RÉUNIS.", "réunis."]]))
insert_after(e, 10, S("p3", [["ASTUCE :", "Astuce :"], ["*NOTE LA DATE", "note la date"], ["DE RENOUVELLEMENT.", "de renouvellement."]]))
add_segment_before_cta(e, [V([["VERDICT :", "Verdict :"], ["*UN SEUL ABONNEMENT", "un seul abonnement"], ["SUFFIT LA PLUPART DU TEMPS.", "suffit la plupart du temps."]])],
    "verdict", {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "@0", "text": "<em>Un seul</em> abonnement IA", "textAt": "@1", "sub": "suffit la plupart du temps", "subAt": "@2"})

# 12 · Banque
e = eps[12]
insert_after(e, 5, S("p1", [["SUR DES MILLIONS DE COMPTES,", "Sur des millions de comptes,"], ["*ÇA FAIT DES MILLIARDS.", "ça fait des milliards.", "coin"]]))
insert_after(e, 8, S("p2", [["BON RÉFLEXE :", "Bon réflexe :"], ["*COMPARE LES GRILLES", "compare les grilles"], ["DE TARIFS DES BANQUES.", "de tarifs des banques."]]))
insert_after(e, 11, S("p3", [["SUR 50 € DE COURSES,", "Sur cinquante euros de courses,"], ["*QUELQUES CENTIMES…", "quelques centimes…"], ["MAIS À CHAQUE PAIEMENT.", "mais à chaque paiement."]]))
add_segment_before_cta(e, [V([["VERDICT :", "Verdict :"], ["*GRATUIT", "gratuit"], ["NE VEUT PAS DIRE SANS PROFIT.", "ne veut pas dire sans profit."]])],
    "verdict", {"type": "icon", "glow": "gold", "icon": "bank", "color": "gold", "at": "@0", "text": "Gratuit ≠ <em>sans profit</em>", "textAt": "@1", "sub": "compare les grilles de tarifs", "subAt": "@2"})

# 13 · Dropshipping
e = eps[13]
insert_after(e, 6, S("p1", [["ET AVEC 10 % DE RETOURS,", "Et avec dix pour cent de retours,"], ["*TU PERDS DE L'ARGENT.", "tu perds de l'argent.", "boom"]]))
insert_after(e, 9, S("p2", [["ET C'EST TA BOUTIQUE", "Et c'est ta boutique"], ["*QUI PREND LES AVIS NÉGATIFS.", "qui prend les avis négatifs."]]))

# 14 · Formations IA
e = eps[14]
insert_after(e, 3, S("s1", [["DEMANDE TOUJOURS :", "Demande toujours :"], ["*COMBIEN DE CLIENTS,", "combien de clients,"], ["ET QUEL CHIFFRE D'AFFAIRES ?", "et quel chiffre d'affaires ?"]]))
insert_after(e, 6, S("s2", [["UNE VRAIE OFFRE", "Une vraie offre"], ["*PEUT ATTENDRE DEMAIN.", "peut attendre demain."]]))
insert_after(e, 9, S("s3", [["LES ÉLÈVES, EUX,", "Les élèves, eux,"], ["*N'ONT AUCUNE GARANTIE.", "n'ont aucune garantie."]]))

# 15 · Applis gratuites
e = eps[15]
insert_after(e, 3, S("p1", [["TU NE PAIES PAS EN EUROS :", "Tu ne paies pas en euros :"], ["*TU PAIES EN ATTENTION.", "tu paies en attention."]]))
insert_after(e, 6, S("p2", [["POUR TE FAIRE PASSER EN PREMIUM :", "Pour te faire passer en premium :"], ["*PUBS, LIMITES,", "pubs, limites,"], ["FONCTIONS BLOQUÉES.", "fonctions bloquées."]]))
insert_after(e, 9, S("p3", [["ASTUCE :", "Astuce :"], ["*ARRÊTE L'ABONNEMENT DÈS LE 1ER JOUR :", "arrête l'abonnement dès le premier jour :"], ["L'ESSAI CONTINUE SOUVENT.", "l'essai continue souvent jusqu'au bout."]]))
add_segment_before_cta(e, [V([["VERDICT :", "Verdict :"], ["*RIEN N'EST", "rien n'est"], ["VRAIMENT GRATUIT.", "vraiment gratuit."]])],
    "verdict", {"type": "icon", "glow": "gold", "icon": "phone", "color": "gold", "at": "@0", "text": "Rien n'est <em>vraiment gratuit</em>", "textAt": "@1", "sub": "pub, données ou abonnement", "subAt": "@2"})

(OUT / "scripts").mkdir(exist_ok=True)
for n, e in eps.items():
    data = {"_doc": "Semaine 2 : voir serie/semaine.py.", "ep": n, **COMMON, **e}
    (OUT / f"ep{n:02d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    # Texte à lire si tu enregistres ta propre voix (une phrase par ligne).
    (OUT / "scripts" / f"ep{n:02d}.txt").write_text(
        "\n".join(" ".join(c[1] for c in s["chunks"]) for s in e["sentences"]) + "\n", encoding="utf-8")
print("ok", sorted(eps))
