#!/usr/bin/env python3
"""
Semaine 4 : la fin des 15 idées, 5 vidéos d'un peu plus d'une minute.

    affirmation surprenante (1re seconde) → 3 preuves visuelles → verdict →
    « sauvegarde cette vidéo avant de… » → une question pour faire commenter.

Plus d'une minute : seules ces vidéos comptent pour le programme de rémunération de TikTok.

    python3 serie/semaine4.py     # écrit serie/ep21.json … ep25.json et serie/scripts/epNN.txt

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

# ---------------------------------------------------------------- 21 · 1 erreur : ne jamais comparer sa banque
eps[21] = {"title": "Comparer sa banque", "series": "1 ERREUR QUI TE COÛTE · #4", "short": "COMPARER SA BANQUE",
  "next": "Les néobanques : comment elles gagnent ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["10 ANS", "Dix ans"], ["DANS LA MÊME BANQUE", "dans la même banque"], ["*PEUT TE COÛTER PRÈS DE 1 000 €.", "peut te coûter près de mille euros.", "boom"]]},
    S("hook", ["C'EST L'ERREUR :", "C'est l'erreur :"], ["*NE JAMAIS COMPARER SA BANQUE.", "ne jamais comparer sa banque."]),
    PROOF("p1", 1, "*LES FRAIS QUI S'ADDITIONNENT.", "les frais qui s'additionnent."),
    S("p1", ["TENUE DE COMPTE :", "Tenue de compte :"], ["*ENVIRON 25 € PAR AN.", "environ vingt-cinq euros par an."]),
    S("p1", ["CARTE BANCAIRE :", "Carte bancaire :"], ["*ENVIRON 45 €.", "environ quarante-cinq euros."]),
    S("p1", ["ASSURANCE DES MOYENS DE PAIEMENT :", "Assurance des moyens de paiement :"], ["*ENCORE 25 €.", "encore vingt-cinq euros."]),
    S("p1", ["*PRESQUE 100 € PAR AN,", "Au total, presque cent euros par an,", "coin"], ["950 € EN 10 ANS.", "neuf cent cinquante euros en dix ans."]),
    S("p1", ["ET C'EST SANS COMPTER", "Et c'est sans compter"], ["*LES FRAIS D'INCIDENT.", "les frais d'incident."]),
    PROOF("p2", 2, "*LES BANQUES EN LIGNE.", "les banques en ligne."),
    S("p2", ["BEAUCOUP PROPOSENT", "Beaucoup proposent"], ["*UN COMPTE ET UNE CARTE GRATUITS,", "un compte et une carte gratuits,"], ["SOUS CONDITIONS.", "sous conditions."]),
    S("p2", ["CONDITION DE REVENUS,", "Condition de revenus,"], ["OU D'UTILISER LA CARTE", "ou d'utiliser la carte"], ["*CHAQUE MOIS.", "chaque mois."]),
    S("p2", ["LIS-LES AVANT DE CHANGER,", "Lis-les avant de changer,"], ["*SINON DES FRAIS TOMBENT.", "sinon des frais tombent.", "stamp"]),
    PROOF("p3", 3, "*CHANGER EST FACILE.", "changer est facile."),
    S("p3", ["AVEC LA MOBILITÉ BANCAIRE,", "Avec la mobilité bancaire,"], ["*TA NOUVELLE BANQUE S'OCCUPE", "ta nouvelle banque s'occupe"], ["DE TOUT TRANSFÉRER.", "de tout transférer."]),
    S("p3", ["PRÉLÈVEMENTS ET VIREMENTS :", "Prélèvements et virements :"], ["*C'EST GRATUIT.", "c'est gratuit."]),
    S("p3", ["ET TU PEUX GARDER", "Et tu peux garder"], ["*TON ANCIEN COMPTE", "ton ancien compte"], ["LE TEMPS DE VÉRIFIER.", "le temps de vérifier."]),
    VERDICT(["*COMPARE UNE FOIS PAR AN.", "compare une fois par an."], ["10 MINUTES SUFFISENT.", "Dix minutes suffisent."]),
    SAVE("AVANT TON PROCHAIN RELEVÉ DE FRAIS.", "avant ton prochain relevé de frais."),
    ASK("COMBIEN DE FRAIS PAR AN ?", "tu paies combien de frais bancaires par an ?")],
  "shakes": ["0:2", "6:0"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "bank",
      "lines": [{"text": "10 ans", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "même banque", "at": "0:1", "size": "m"},
                {"text": "≈ 1 000 €", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Ne jamais <em>comparer</em> sa banque", "at": "1:1"}},
    "p1": {"type": "list", "glow": "red", "chip": CHIP(1, "2:0"), "title": {"html": "Les frais qui <em>s'additionnent</em>", "at": "2:1"}, "top": 500,
      "items": [{"icon": "bank", "label": "Tenue de compte", "sub": "exemple", "value": "25 €/an", "at": "3:0", "color": "down"},
                {"icon": "card", "label": "Carte bancaire", "sub": "exemple", "value": "45 €/an", "at": "4:0", "color": "down"},
                {"icon": "shield", "label": "Assurance", "sub": "moyens de paiement", "value": "25 €/an", "at": "5:0", "color": "down"}],
      "total": {"label": "PAR AN", "color": "down", "stages": [{"to": 95, "at": "6:0", "label": "PAR AN"}, {"to": 950, "at": "6:1", "label": "EN 10 ANS"}]}},
    "p2": {"type": "steps", "glow": "gold", "chip": CHIP(2, "8:0"), "title": {"html": "Les banques <em>en ligne</em>", "at": "8:1"}, "top": 520,
      "items": [{"icon": "phone", "label": "Compte + carte", "sub": "souvent gratuits", "at": "9:1", "color": "up"},
                {"icon": "alert", "label": "Sous conditions", "sub": "revenus, usage de la carte", "at": "10:0"},
                {"icon": "cross", "label": "Condition ratée", "sub": "des frais tombent", "at": "11:1", "color": "down"}]},
    "p3": {"type": "steps", "glow": "green", "chip": CHIP(3, "12:0"), "title": {"html": "Changer est <em>facile</em>", "at": "12:1"}, "top": 520,
      "items": [{"icon": "bank", "label": "Nouvelle banque", "sub": "elle s'occupe du transfert", "at": "13:1"},
                {"icon": "envelope", "label": "Prélèvements, virements", "sub": "transférés gratuitement", "at": "14:1", "color": "up"},
                {"icon": "check", "label": "Ancien compte", "sub": "gardé le temps de vérifier", "at": "15:1", "color": "up"}]},
    "verdict": {"type": "icon", "glow": "green", "icon": "calendar", "color": "up", "at": "16:0", "text": "Compare <em>1 fois par an</em>", "textAt": "16:1",
      "sub": "10 minutes suffisent", "subAt": "16:2"},
    "cta": CTA("avant ton prochain relevé de frais")},
  "post": {"caption": "Rester 10 ans dans la même banque sans comparer, ça peut coûter près de 1 000 € de frais. Les banques en ligne sont souvent gratuites sous conditions, et avec la mobilité bancaire, ta nouvelle banque transfère tout gratuitement. Sauvegarde cette vidéo avant ton prochain relevé de frais. Et toi, tu paies combien de frais bancaires par an ?",
           "hashtags": ["#banque", "#fraisbancaires", "#economiser", "#budget"]},
  "cover": {"chip": "1 ERREUR · #4", "kicker": "10 ans dans la même banque ?", "icon": "bank"}}

# ---------------------------------------------------------------- 22 · Comment gagnent vraiment les néobanques
eps[22] = {"title": "Les néobanques", "series": "COMMENT GAGNE VRAIMENT… · #4", "short": "NÉOBANQUES",
  "next": "Copy trading : rentable ou arnaque ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["UNE BANQUE SANS FRAIS…", "Une banque sans frais…"], ["*QUI GAGNE QUAND MÊME DE L'ARGENT.", "qui gagne quand même de l'argent.", "boom"]]},
    S("hook", ["VOICI COMMENT", "Voici comment"], ["*LES NÉOBANQUES", "les néobanques"], ["GAGNENT VRAIMENT LEUR VIE.", "gagnent vraiment leur vie."]),
    PROOF("p1", 1, "*CHAQUE PAIEMENT PAR CARTE.", "chaque paiement par carte."),
    S("p1", ["À CHAQUE PAIEMENT,", "À chaque paiement,"], ["LE COMMERÇANT PAIE UNE COMMISSION,", "le commerçant paie une commission,"], ["*ET LA BANQUE EN TOUCHE UNE PART.", "et la banque en touche une part."]),
    S("p1", ["EN EUROPE, ELLE EST PLAFONNÉE", "En Europe, elle est plafonnée"], ["*À 0,2 % POUR UNE CARTE DE DÉBIT.", "à zéro virgule deux pour cent pour une carte de débit."]),
    S("p1", ["C'EST PETIT PAR PAIEMENT,", "C'est petit par paiement,"], ["*MAIS ÉNORME SUR DES MILLIONS DE CLIENTS.", "mais énorme sur des millions de clients.", "coin"]),
    PROOF("p2", 2, "*LES OFFRES PAYANTES.", "les offres payantes."),
    S("p2", ["CARTE EN MÉTAL, ASSURANCES,", "Carte en métal, assurances,"], ["*RETRAITS EN PLUS :", "retraits en plus :"], ["JUSQU'À PLUS DE 15 € PAR MOIS.", "jusqu'à plus de quinze euros par mois."]),
    S("p2", ["L'OFFRE GRATUITE", "L'offre gratuite"], ["*SERT AUSSI À TE FAIRE MONTER EN GAMME.", "sert aussi à te faire monter en gamme."]),
    S("p2", ["ET LES CLIENTS QUI PAIENT", "Et les clients qui paient"], ["*FINANCENT EN PARTIE LES AUTRES.", "financent en partie les autres."]),
    PROOF("p3", 3, "*LES PETITES LIGNES.", "les petites lignes."),
    S("p3", ["RETRAITS AU-DELÀ D'UN QUOTA,", "Retraits au-delà d'un quota,"], ["PAIEMENTS EN DEVISES,", "paiements en devises,"], ["*CARTE PERDUE À REMPLACER.", "carte perdue à remplacer."]),
    S("p3", ["CHACUN NE COÛTE PAS GRAND-CHOSE,", "Chacun ne coûte pas grand-chose,"], ["*MAIS ILS S'ADDITIONNENT.", "mais ils s'additionnent.", "stamp"]),
    S("astuce", ["ET L'ARGENT QUI DORT SUR TON COMPTE ?", "Et l'argent qui dort sur ton compte ?"], ["*LA BANQUE PEUT EN TIRER DES INTÉRÊTS.", "La banque peut en tirer des intérêts."]),
    S("astuce", ["ASTUCE :", "Astuce :"], ["*LIS LA GRILLE TARIFAIRE", "lis la grille tarifaire"], ["AVANT D'OUVRIR TON COMPTE.", "avant d'ouvrir ton compte."]),
    VERDICT(["*GRATUIT,", "gratuit,"], ["SI TU RESTES DANS LES CLOUS.", "si tu restes dans les clous."]),
    SAVE("AVANT D'OUVRIR UN COMPTE.", "avant d'ouvrir un compte en ligne."),
    ASK("TU ES DANS UNE NÉOBANQUE ?", "tu as un compte dans une néobanque ?")],
  "shakes": ["0:1", "12:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "phone",
      "lines": [{"text": "Sans frais…", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "et pourtant", "at": "0:1", "size": "m"},
                {"text": "elle gagne", "at": "0:1+0.4", "size": "xl", "hl": True}],
      "reveal": {"html": "Comment gagnent les <em>néobanques</em>", "at": "1:1"}},
    "p1": {"type": "steps", "glow": "gold", "chip": CHIP(1, "2:0"), "title": {"html": "Chaque <em>paiement</em>", "at": "2:1"}, "top": 520,
      "items": [{"icon": "card", "label": "Tu paies par carte", "sub": "chez un commerçant", "at": "3:0"},
                {"icon": "basket", "label": "Commission du commerçant", "sub": "0,2 % max. (carte de débit, UE)", "at": "4:1", "color": "gold"},
                {"icon": "bank", "label": "Une part pour la banque", "sub": "× des millions de paiements", "at": "5:1"}]},
    "p2": {"type": "bars", "glow": "gold", "chip": CHIP(2, "6:0"), "title": {"html": "Les offres <em>payantes</em>", "at": "6:1"}, "label": "Par mois · ordres de grandeur", "top": 520,
      "items": [{"label": "Offre gratuite", "value": 0, "color": "up", "at": "7:0"},
                {"label": "Intermédiaire", "sub": "assurances", "value": 8, "color": "gold", "at": "7:1"},
                {"label": "Haut de gamme", "sub": "carte en métal", "value": 16, "color": "down", "at": "7:2"}]},
    "p3": {"type": "list", "glow": "red", "chip": CHIP(3, "10:0"), "title": {"html": "Les <em>petites lignes</em>", "at": "10:1"}, "top": 500,
      "items": [{"icon": "bank", "label": "Retrait au-delà du quota", "value": "frais", "at": "11:0", "color": "down"},
                {"icon": "coin", "label": "Paiement en devises", "value": "frais", "at": "11:1", "color": "down"},
                {"icon": "card", "label": "Carte à remplacer", "value": "frais", "at": "11:2", "color": "down"}]},
    "astuce": {"type": "icon", "glow": "gold", "icon": "bank", "color": "gold", "at": "13:0", "text": "Ton argent qui dort <em>rapporte… à elle</em>", "textAt": "13:1",
      "sub": "Astuce : lis la grille tarifaire avant d'ouvrir", "subAt": "14:1"},
    "verdict": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "15:0", "text": "Gratuit, <em>dans les clous</em>", "textAt": "15:1",
      "sub": "quota de retraits, devises, options", "subAt": "15:2"},
    "cta": CTA("avant d'ouvrir un compte")},
  "post": {"caption": "Comment gagnent vraiment les néobanques ? Une commission sur chaque paiement par carte, des offres payantes, et des frais dans les petites lignes : retraits au-delà du quota, paiements en devises… Sauvegarde cette vidéo avant d'ouvrir un compte. Et toi, tu as un compte dans une néobanque ?",
           "hashtags": ["#neobanque", "#banque", "#argent", "#financepersonnelle"]},
  "cover": {"chip": "COMMENT GAGNE… · #4", "kicker": "Les néobanques : comment elles gagnent ?", "icon": "phone"}}

# ---------------------------------------------------------------- 23 · Rentable ou arnaque : le copy trading
eps[23] = {"title": "Le copy trading", "series": "RENTABLE OU ARNAQUE ? · #5", "short": "COPY TRADING",
  "next": "1 million de vues = combien ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["COPIER UN PRO", "Copier les investissements d'un pro"], ["ET GAGNER COMME LUI ?", "et gagner comme lui ?"], ["*CE QU'ON NE TE DIT PAS.", "Voici ce qu'on ne te dit pas.", "boom"]]},
    S("hook", ["LE COPY TRADING :", "La copie d'investissements :"], ["*RENTABLE OU ARNAQUE ?", "rentable ou arnaque ?"]),
    PROOF("p1", 1, "*L'AVERTISSEMENT OBLIGATOIRE.", "l'avertissement obligatoire."),
    S("p1", ["SUR BEAUCOUP DE PLATEFORMES,", "Sur beaucoup de plateformes,"], ["*UN MESSAGE INDIQUE", "un message indique"], ["LA PART DES COMPTES QUI PERDENT.", "la part des comptes qui perdent de l'argent."]),
    S("p1", ["SOUVENT,", "Souvent,"], ["*PLUS DE LA MOITIÉ.", "c'est plus de la moitié.", "stamp"]),
    S("p1", ["LIS-LE AVANT DE COMMENCER :", "Lis-le avant de commencer :"], ["*IL EST LÀ POUR UNE RAISON.", "il est là pour une raison."]),
    PROOF("p2", 2, "*LE PASSÉ NE GARANTIT RIEN.", "le passé ne garantit rien."),
    S("p2", ["+50 % L'AN DERNIER", "Plus cinquante pour cent l'an dernier"], ["*PEUT DEVENIR UNE GROSSE PERTE", "peut devenir une grosse perte"], ["CETTE ANNÉE.", "cette année."]),
    S("p2", ["PLUS IL PREND DE RISQUES,", "Plus il prend de risques,"], ["*PLUS SES GAINS AFFICHÉS", "plus ses gains affichés"], ["PEUVENT ÊTRE BEAUX.", "peuvent être beaux."]),
    S("p2", ["ET TU COPIES", "Et tu copies"], ["*SES PERTES AUSSI.", "ses pertes aussi.", "stamp"]),
    PROOF("p3", 3, "*QUI GAGNE À COUP SÛR ?", "qui gagne à coup sûr ?"),
    S("p3", ["LA PLATEFORME :", "La plateforme :"], ["*FRAIS, ÉCARTS DE PRIX,", "frais, écarts de prix,"], ["À CHAQUE OPÉRATION.", "à chaque opération."]),
    S("p3", ["ET LE TRADER COPIÉ", "Et l'investisseur copié"], ["*EST SOUVENT PAYÉ", "est souvent payé"], ["SELON LE NOMBRE DE COPIEURS.", "selon le nombre de copieurs."]),
    S("astuce", ["MÉFIE-TOI DES GROUPES", "Méfie-toi des groupes"], ["*QUI VENDENT DES « SIGNAUX »", "qui vendent des signaux"], ["SUR LES RÉSEAUX.", "sur les réseaux."]),
    S("astuce", ["VÉRIFIE TOUJOURS", "Vérifie toujours"], ["*LES LISTES NOIRES DE L'AMF.", "les listes noires de l'Autorité des marchés financiers."]),
    VERDICT(["*PAS FORCÉMENT UNE ARNAQUE,", "pas forcément une arnaque,"], ["MAIS TRÈS RISQUÉ.", "mais très risqué."]),
    S("verdict", ["N'Y METS JAMAIS", "N'y mets jamais"], ["*L'ARGENT DONT TU AS BESOIN.", "l'argent dont tu as besoin."]),
    SAVE("AVANT DE COPIER QUELQU'UN.", "avant de copier quelqu'un."),
    ASK("TU AS DÉJÀ ESSAYÉ ?", "tu as déjà essayé ?")],
  "shakes": ["0:2", "9:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "bolt",
      "lines": [{"text": "Copier", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "un pro ?", "at": "0:0+0.3", "size": "m"},
                {"text": "ce qu'on ne dit pas", "at": "0:2", "size": "m", "hl": True}],
      "reveal": {"html": "Copy trading : <em>rentable</em> ?", "at": "1:1"}},
    "p1": {"type": "donut", "glow": "red", "chip": {"text": "PREUVE 1 / 3 · EXEMPLE", "at": "2:0"},
      "parts": [{"pct": 70, "label": "Perdent", "color": "down", "at": "4:1"}, {"pct": 30, "label": "Gagnent", "color": "ink", "at": "4:1"}],
      "final": {"big": "+50 %", "small": "des comptes perdent", "color": "down", "at": "5:0", "highlight": 0}},
    "p2": {"type": "icon", "glow": "red", "chip": CHIP(2, "6:0"), "icon": "alert", "color": "down", "at": "6:0", "text": "+50 %… puis <em>la chute</em>", "textAt": "7:1",
      "sub": "plus de risque = plus beaux gains affichés… et tu copies les pertes", "subAt": "8:1"},
    "p3": {"type": "list", "glow": "gold", "chip": CHIP(3, "10:0"), "title": {"html": "Qui gagne <em>à coup sûr</em> ?", "at": "10:1"}, "top": 500,
      "items": [{"icon": "bank", "label": "La plateforme", "sub": "frais, écarts de prix", "value": "gagne", "at": "11:0", "color": "up"},
                {"icon": "party", "label": "Le trader copié", "sub": "payé selon les copieurs", "value": "gagne", "at": "12:1", "color": "up"},
                {"icon": "wallet", "label": "Toi", "sub": "seulement si ça monte", "value": "?", "at": "12:2", "color": "down"}]},
    "astuce": {"type": "icon", "glow": "red", "icon": "alert", "color": "gold", "at": "13:0", "text": "Méfie-toi des <em>« signaux »</em>", "textAt": "13:1",
      "sub": "vérifie les listes noires de l'AMF", "subAt": "14:1"},
    "verdict": {"type": "icon", "glow": "gold", "icon": "shield", "color": "gold", "at": "15:0", "text": "Pas une arnaque, <em>très risqué</em>", "textAt": "15:1",
      "sub": "jamais l'argent dont tu as besoin", "subAt": "16:1"},
    "cta": CTA("avant de copier quelqu'un")},
  "post": {"caption": "Copier les trades d'un pro : rentable ou arnaque ? Sur beaucoup de plateformes, plus de la moitié des comptes perdent de l'argent, et les performances passées ne garantissent rien. Vérifie toujours les listes noires de l'AMF. Sauvegarde cette vidéo avant de copier quelqu'un. Et toi, tu as déjà essayé ?",
           "hashtags": ["#copytrading", "#trading", "#arnaque", "#argent"]},
  "cover": {"chip": "RENTABLE OU ARNAQUE ? · #5", "kicker": "Copy trading : rentable ou arnaque ?", "icon": "bolt"}}

# ---------------------------------------------------------------- 24 · Comment gagnent vraiment les créateurs TikTok
eps[24] = {"title": "Les créateurs TikTok", "series": "COMMENT GAGNE VRAIMENT… · #5", "short": "CRÉATEURS TIKTOK",
  "next": "Ton épargne dort sur ton compte ?",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["1 MILLION DE VUES", "Un million de vues"], ["*NE RAPPORTE PAS CE QUE TU CROIS.", "ne rapporte pas ce que tu crois.", "boom"]]},
    S("hook", ["VOICI COMMENT", "Voici comment"], ["*LES CRÉATEURS TIKTOK", "les créateurs TikTok"], ["GAGNENT VRAIMENT DE L'ARGENT.", "gagnent vraiment de l'argent."]),
    PROOF("p1", 1, "*LES VUES.", "les vues."),
    S("p1", ["TIKTOK PAIE SEULEMENT", "TikTok paie seulement"], ["*LES VIDÉOS DE PLUS D'UNE MINUTE,", "les vidéos de plus d'une minute,"], ["ET PAS TOUTES LES VUES.", "et pas toutes les vues."]),
    S("p1", ["UN MILLION DE VUES,", "Un million de vues,"], ["*C'EST SOUVENT QUELQUES CENTAINES D'EUROS.", "c'est souvent quelques centaines d'euros."]),
    S("p1", ["ET ÇA VARIE BEAUCOUP", "Et ça varie beaucoup"], ["*SELON LE PAYS ET LE SUJET.", "selon le pays et le sujet."]),
    PROOF("p2", 2, "*LES MARQUES.", "les marques."),
    S("p2", ["UNE MARQUE PAIE", "Une marque paie"], ["*POUR APPARAÎTRE DANS UNE VIDÉO.", "pour apparaître dans une vidéo."]),
    S("p2", ["POUR BEAUCOUP DE CRÉATEURS,", "Pour beaucoup de créateurs,"], ["*C'EST LA PLUS GROSSE SOURCE", "c'est la plus grosse source"], ["DE REVENUS.", "de revenus.", "coin"]),
    S("p2", ["ET LA LOI IMPOSE", "Et la loi impose"], ["*DE LE SIGNALER :", "de le signaler :"], ["« COLLABORATION COMMERCIALE ».", "collaboration commerciale."]),
    PROOF("p3", 3, "*LES LIVES ET LA VENTE.", "les directs et la vente."),
    S("p3", ["EN LIVE, LES CADEAUX VIRTUELS", "En direct, les cadeaux virtuels"], ["*SE TRANSFORMENT EN ARGENT,", "se transforment en argent,"], ["MOINS LA PART DE TIKTOK.", "moins la part de TikTok."]),
    S("p3", ["ET AVEC L'AFFILIATION,", "Et avec l'affiliation,"], ["*LE CRÉATEUR TOUCHE UNE COMMISSION", "le créateur touche une commission"], ["SUR CHAQUE VENTE.", "sur chaque vente."]),
    S("astuce", ["LE VRAI CAPITAL :", "Le vrai capital :"], ["*UNE AUDIENCE QUI TE FAIT CONFIANCE.", "une audience qui te fait confiance."]),
    S("astuce", ["C'EST POUR ÇA QUE DES PETITS COMPTES", "C'est pour ça que des petits comptes"], ["*GAGNENT PARFOIS PLUS", "gagnent parfois plus"], ["QUE DES GROS.", "que des gros."]),
    VERDICT(["*LES VUES PAIENT PEU,", "les vues paient peu,"], ["LA CONFIANCE PAIE BEAUCOUP.", "la confiance paie beaucoup."]),
    SAVE("AVANT DE RÊVER DE MILLIONS DE VUES.", "avant de rêver de millions de vues."),
    ASK("TU CROYAIS QUE ÇA RAPPORTAIT COMBIEN ?", "tu croyais que ça rapportait combien ?")],
  "shakes": ["0:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "play",
      "lines": [{"text": "1 million", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "de vues", "at": "0:0+0.3", "size": "m"},
                {"text": "= combien ?", "at": "0:1", "size": "xl", "hl": True}],
      "reveal": {"html": "Comment gagnent les <em>créateurs TikTok</em>", "at": "1:1"}},
    "p1": {"type": "icon", "glow": "gold", "chip": CHIP(1, "2:0"), "icon": "play", "color": "gold", "at": "2:0", "text": "1 million de vues : <em>quelques centaines d'€</em>", "textAt": "4:1",
      "sub": "vidéos de plus d'1 minute seulement · varie selon le pays et le sujet", "subAt": "5:1"},
    "p2": {"type": "steps", "glow": "gold", "chip": CHIP(2, "6:0"), "title": {"html": "Les <em>marques</em>", "at": "6:1"}, "top": 520,
      "items": [{"icon": "basket", "label": "Une marque paie", "sub": "pour apparaître dans la vidéo", "at": "7:1"},
                {"icon": "coin", "label": "La plus grosse source", "sub": "pour beaucoup de créateurs", "at": "8:1", "color": "gold"},
                {"icon": "alert", "label": "À signaler", "sub": "« collaboration commerciale »", "at": "9:1"}]},
    "p3": {"type": "list", "glow": "gold", "chip": CHIP(3, "10:0"), "title": {"html": "Les lives et <em>la vente</em>", "at": "10:1"}, "top": 500,
      "items": [{"icon": "party", "label": "Cadeaux en live", "sub": "moins la part de TikTok", "value": "€", "at": "11:1", "color": "gold"},
                {"icon": "cart", "label": "Affiliation", "sub": "commission sur chaque vente", "value": "%", "at": "12:1", "color": "gold"}]},
    "astuce": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "13:0", "text": "Une audience qui te <em>fait confiance</em>", "textAt": "13:1",
      "sub": "des petits comptes gagnent parfois plus que des gros", "subAt": "14:1"},
    "verdict": {"type": "icon", "glow": "gold", "icon": "coin", "color": "gold", "at": "15:0", "text": "Les vues paient <em>peu</em>", "textAt": "15:1",
      "sub": "la confiance paie beaucoup", "subAt": "15:2"},
    "cta": CTA("avant de rêver de millions de vues")},
  "post": {"caption": "1 million de vues ne rapporte pas ce que tu crois : souvent quelques centaines d'euros seulement. Le vrai argent des créateurs vient des marques, des lives et de l'affiliation, grâce à une audience qui leur fait confiance. Sauvegarde cette vidéo avant de rêver de millions de vues. Et toi, tu croyais que ça rapportait combien ?",
           "hashtags": ["#createurdecontenu", "#tiktok", "#argent", "#sidehustle"]},
  "cover": {"chip": "COMMENT GAGNE… · #5", "kicker": "1 million de vues = combien ?", "icon": "play"}}

# ---------------------------------------------------------------- 25 · 1 erreur : laisser dormir son épargne
eps[25] = {"title": "L'épargne qui dort", "series": "1 ERREUR QUI TE COÛTE · #5", "short": "ÉPARGNE QUI DORT", "next": None,
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TON ÉPARGNE DORT", "Ton épargne dort"], ["SUR TON COMPTE COURANT ?", "sur ton compte courant ?"], ["*ELLE PERD DE LA VALEUR.", "Elle perd de la valeur chaque année.", "boom"]]},
    S("hook", ["C'EST L'ERREUR :", "C'est l'erreur :"], ["*LAISSER DORMIR SON ARGENT.", "laisser dormir son argent."]),
    PROOF("p1", 1, "*0 % D'INTÉRÊTS.", "zéro pour cent d'intérêts."),
    S("p1", ["SUR UN COMPTE COURANT,", "Sur un compte courant,"], ["*TON ARGENT NE RAPPORTE RIEN.", "ton argent ne rapporte rien."]),
    S("p1", ["5 000 € AUJOURD'HUI,", "Cinq mille euros aujourd'hui,"], ["*5 000 € DANS UN AN.", "cinq mille euros dans un an."]),
    PROOF("p2", 2, "*L'INFLATION.", "l'inflation."),
    S("p2", ["LES PRIX MONTENT", "Les prix montent"], ["*PRESQUE CHAQUE ANNÉE.", "presque chaque année."]),
    S("p2", ["AVEC 2 % D'INFLATION,", "Avec deux pour cent d'inflation,"], ["*TES 5 000 €", "tes cinq mille euros"], ["ACHÈTENT 100 € DE MOINS.", "achètent environ cent euros de moins."]),
    S("p2", ["ET CHAQUE ANNÉE,", "Et chaque année,"], ["*ÇA RECOMMENCE.", "ça recommence.", "stamp"]),
    PROOF("p3", 3, "*LE LIVRET.", "le livret."),
    S("p3", ["UN LIVRET A", "Un Livret A"], ["*SE RETIRE QUAND TU VEUX,", "se retire quand tu veux,"], ["SANS IMPÔT SUR LES INTÉRÊTS.", "sans impôt sur les intérêts."]),
    S("p3", ["EXEMPLE À 1,5 % :", "Exemple, avec un taux d'un et demi pour cent :"], ["*75 € PAR AN", "soixante-quinze euros par an"], ["SANS RIEN FAIRE.", "sans rien faire.", "coin"]),
    S("p3", ["LE TAUX CHANGE :", "Le taux change :"], ["*VÉRIFIE LE TAUX ACTUEL.", "vérifie le taux actuel."]),
    S("astuce", ["ASTUCE :", "Astuce :"], ["*GARDE UN MOIS DE DÉPENSES", "garde un mois de dépenses"], ["SUR TON COMPTE COURANT.", "sur ton compte courant."]),
    S("astuce", ["LE RESTE DE TON ÉPARGNE", "Le reste de ton épargne"], ["*VA SUR UN LIVRET.", "va sur un livret."]),
    VERDICT(["*UN SIMPLE VIREMENT,", "un simple virement,"], ["ET TON ARGENT TRAVAILLE.", "et ton argent travaille."]),
    SAVE("AVANT TON PROCHAIN SALAIRE.", "avant ton prochain salaire."),
    ASK("TON ÉPARGNE EST OÙ ?", "ton épargne est sur quel compte ?")],
  "shakes": ["0:2", "8:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "piggy",
      "lines": [{"text": "0 %", "at": "0:0-0.6", "size": "xl", "color": "gold"}, {"text": "sur ton compte", "at": "0:1", "size": "m"},
                {"text": "elle fond", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Laisser <em>dormir</em> son argent", "at": "1:1"}},
    "p1": {"type": "counter", "glow": "red", "chip": CHIP(1, "2:0"), "title": {"html": "<em>0 %</em> d'intérêts", "at": "2:1"}, "label": "Compte courant · exemple", "color": "gold",
      "stages": [{"to": 5000, "at": "4:0", "label": "AUJOURD'HUI"}, {"to": 5000, "at": "4:1", "label": "DANS UN AN"}]},
    "p2": {"type": "bars", "glow": "red", "chip": CHIP(2, "5:0"), "title": {"html": "L'<em>inflation</em>", "at": "5:1"}, "label": "Ce que tes 5 000 € achètent · 2 %/an (exemple)", "top": 520,
      "items": [{"label": "Aujourd'hui", "value": 5000, "color": "gold", "at": "6:1"},
                {"label": "Dans 1 an", "value": 4900, "color": "down", "at": "7:2"},
                {"label": "Dans 5 ans", "value": 4530, "color": "down", "at": "8:1"}],
      "badge": {"text": "−470 €", "small": "EN 5 ANS", "at": "8:1", "color": "red"}},
    "p3": {"type": "counter", "glow": "green", "chip": CHIP(3, "9:0"), "title": {"html": "Le <em>livret</em>", "at": "9:1"}, "label": "5 000 € à 1,5 % · exemple", "color": "up",
      "stages": [{"to": 75, "at": "11:1", "label": "D'INTÉRÊTS PAR AN"}],
      "disclaimer": "Taux d'exemple : vérifie le taux actuel du Livret A"},
    "astuce": {"type": "steps", "glow": "green", "title": {"html": "Le bon <em>réglage</em>", "at": "13:0"}, "top": 560,
      "items": [{"icon": "wallet", "label": "1 mois de dépenses", "sub": "sur le compte courant", "at": "13:1"},
                {"icon": "piggy", "label": "Le reste", "sub": "sur un livret", "at": "14:1", "color": "up"}]},
    "verdict": {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": "15:0", "text": "Un virement, <em>ton argent travaille</em>", "textAt": "15:1"},
    "cta": CTA("avant ton prochain salaire")},
  "post": {"caption": "Ton épargne dort sur ton compte courant ? À 0 %, elle perd de la valeur chaque année avec l'inflation. Garde un mois de dépenses sur ton compte courant et mets le reste sur un livret. Sauvegarde cette vidéo avant ton prochain salaire. Et toi, ton épargne est sur quel compte ?",
           "hashtags": ["#epargne", "#livretA", "#inflation", "#argent"]},
  "cover": {"chip": "1 ERREUR · #5", "kicker": "Ton épargne dort sur ton compte ?", "icon": "piggy"}}

# ---------------------------------------------------------------- au-delà d'une minute
import re as _re

def insert_after(e, idx, sentence):
    """Insère une phrase après la phrase idx et décale tous les instants « n:… » qui suivent."""
    e["sentences"].insert(idx + 1, sentence)
    shift = lambda m: f'"{int(m.group(1)) + (1 if int(m.group(1)) > idx else 0)}:'
    e["blocks"] = json.loads(_re.sub(r'"(\d+):', shift, json.dumps(e["blocks"], ensure_ascii=False)))
    e["shakes"] = [f"{int(x.split(':')[0]) + (1 if int(x.split(':')[0]) > idx else 0)}:{x.split(':', 1)[1]}" for x in e["shakes"]]

insert_after(eps[21], 16, S("verdict", ["COMMENCE PAR TON RELEVÉ", "Commence par ton relevé"], ["*DE FRAIS ANNUEL.", "de frais annuel : ta banque te l'envoie chaque année."]))
insert_after(eps[24], 5, S("p1", ["IL FAUT AUSSI", "Il faut aussi"], ["*10 000 ABONNÉS MINIMUM.", "au moins dix mille abonnés."]))
insert_after(eps[25], 8, S("p2", ["EN 5 ANS,", "En cinq ans,"], ["*PRÈS DE 470 € EN MOINS.", "près de quatre cent soixante-dix euros de pouvoir d'achat en moins.", "stamp"]))
eps[25]["blocks"]["p2"]["badge"]["at"] = "9:1"
eps[25]["blocks"]["p2"]["items"][2]["at"] = "9:0"
insert_after(eps[25], 15, S("astuce", ["C'EST AUSSI", "C'est aussi"], ["*TON FONDS D'URGENCE.", "ton fonds d'urgence, comme dans l'épisode un."]))
for n in (21, 24, 25):
    eps[n]["tail"] = 2.4  # garde la vidéo nettement au-dessus d'une minute

(OUT / "scripts").mkdir(exist_ok=True)
(OUT / "descriptions").mkdir(exist_ok=True)
for n, e in eps.items():
    data = {"_doc": "Semaine 4 : voir serie/semaine4.py.", "ep": n, **COMMON, **e}
    (OUT / f"ep{n:02d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    # Texte à lire si tu enregistres ta propre voix (une phrase par ligne).
    (OUT / "scripts" / f"ep{n:02d}.txt").write_text(
        "\n".join(" ".join(c[1] for c in s["chunks"]) for s in e["sentences"]) + "\n", encoding="utf-8")
    (OUT / "descriptions" / f"ep{n:02d}.txt").write_text(
        e["post"]["caption"] + "\n\n" + " ".join(e["post"]["hashtags"]) + "\n", encoding="utf-8")
print("ok", sorted(eps))
