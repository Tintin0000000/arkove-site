#!/usr/bin/env python3
"""
Source des épisodes 02 à 10 de la série « Épargne malin ».

    python3 serie/episodes.py      # réécrit serie/ep02.json … ep10.json

Les montants (intérêts composés de l'épisode 9 notamment) sont calculés ici.
Tu peux aussi modifier directement les fichiers epNN.json.
"""
import json, math
from pathlib import Path
OUT = Path(__file__).resolve().parent

BASE = ["#epargne", "#argent", "#financepersonnelle", "#budget", "#astuceargent", "#apprendresurtiktok"]
def post(caption, extra):
    return {"caption": caption, "hashtags": extra + BASE}

COMMON = {"voice": "siwis-medium", "speed": 1.04, "lead": 0.3, "gap": 0.18, "duration": "auto", "tail": 3.2,
          "handle": "@epargne.malin"}
CTA = lambda sub="pour la suite": {"segment": "cta", "sfx": "whoosh", "pause": 0.1,
    "chunks": [["ABONNE-TOI", "Abonne-toi"], [sub.upper() + ".", sub + "."]]}

eps = {}

# ---------------------------------------------------------------- 02 · 50/30/20
eps[2] = {"title": "La règle 50/30/20", "short": "RÈGLE 50/30/20", "next": "Paie-toi en premier",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TON SALAIRE", "Ton salaire"], ["DISPARAÎT", "disparaît", "boom"], ["AVANT LA FIN DU MOIS ?", "avant la fin du mois ?"]]},
    {"segment": "hook", "chunks": [["TESTE", "Teste"], ["*LA RÈGLE 50/30/20.", "la règle cinquante, trente, vingt."]]},
    {"segment": "donut", "sfx": "whoosh", "pause": 0.1, "chunks": [["*50 %", "Cinquante pour cent"], ["POUR LES BESOINS :", "pour les besoins :"], ["LOYER, COURSES,", "loyer, courses,"], ["FACTURES.", "factures."]]},
    {"segment": "donut", "chunks": [["*30 %", "Trente pour cent"], ["POUR LES ENVIES.", "pour les envies."]]},
    {"segment": "donut", "chunks": [["*20 %", "Vingt pour cent"], ["POUR L'ÉPARGNE.", "pour l'épargne."]]},
    {"segment": "counter", "sfx": "whoosh", "pause": 0.1, "chunks": [["SUR 2 000 €,", "Sur deux mille euros,"], ["ÇA FAIT", "ça fait"], ["*400 €", "quatre cents euros", "coin"], ["PAR MOIS.", "par mois."]]},
    {"segment": "counter", "chunks": [["SOIT", "Soit"], ["*4 800 € PAR AN.", "quatre mille huit cents euros par an.", "coin"]]},
    CTA()],
  "shakes": ["0:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "wallet",
      "lines": [{"text": "Ton salaire", "at": "0:0"}, {"text": "disparaît", "at": "0:1", "size": "xl", "hl": True}, {"text": "avant la fin", "at": "0:2", "size": "m"}, {"text": "du mois ?", "at": "0:2+0.3", "size": "m"}],
      "reveal": {"html": "La règle <em>50/30/20</em>", "at": "1:1"}},
    "donut": {"type": "donut", "glow": "gold", "chip": {"text": "TON BUDGET", "at": "2:0"},
      "parts": [{"pct": 50, "label": "Besoins", "amount": "1 000 €", "color": "ink", "at": "2:0"},
                {"pct": 30, "label": "Envies", "amount": "600 €", "color": "gold", "at": "3:0"},
                {"pct": 20, "label": "Épargne", "amount": "400 €", "color": "up", "at": "4:0"}],
      "final": {"big": "20 %", "small": "pour toi", "color": "up", "at": "4:1", "highlight": 2}},
    "counter": {"type": "counter", "glow": "green", "title": {"html": "Sur <em>2 000 €</em> net", "at": "5:0"}, "label": "Ton épargne", "color": "up",
      "stages": [{"to": 400, "at": "5:2", "label": "PAR MOIS"}, {"to": 4800, "at": "6:1", "label": "PAR AN", "dur": 1.1}],
      "badge": {"text": "×12", "small": "EN 1 AN", "at": "6:1+0.6", "color": "green"}},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("Ton salaire part trop vite ? Teste la règle 50/30/20 : 50 % besoins, 30 % envies, 20 % épargne. Tu es à combien en ce moment ? 👇",
               ["#regle503020", "#gestionbudget"])}

# ---------------------------------------------------------------- 03 · Paie-toi en premier
eps[3] = {"title": "Paie-toi en premier", "short": "PAIE-TOI D'ABORD", "next": "Les abonnements fantômes",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TU ÉPARGNES", "Tu épargnes"], ["CE QUI RESTE", "ce qui reste"], ["À LA FIN DU MOIS ?", "à la fin du mois ?"]]},
    {"segment": "hook", "chunks": [["*ERREUR :", "Erreur :", "boom"], ["IL NE RESTE", "il ne reste"], ["*JAMAIS RIEN.", "jamais rien."]]},
    {"segment": "steps", "sfx": "whoosh", "pause": 0.1, "chunks": [["PAIE-TOI", "Paie-toi"], ["*EN PREMIER.", "en premier."]]},
    {"segment": "steps", "chunks": [["LE JOUR DE LA PAIE,", "Le jour de la paie,"], ["UN VIREMENT", "un virement"], ["*AUTOMATIQUE", "automatique"], ["VERS TON ÉPARGNE.", "vers ton épargne."]]},
    {"segment": "counter", "sfx": "whoosh", "pause": 0.1, "chunks": [["*10 %", "Dix pour cent"], ["DE 2 000 €,", "de deux mille euros,"], ["*200 € PAR MOIS.", "c'est deux cents euros par mois.", "coin"]]},
    {"segment": "counter", "chunks": [["*2 400 € PAR AN,", "Deux mille quatre cents euros par an,", "coin"], ["SANS Y PENSER.", "sans y penser."]]},
    CTA()],
  "shakes": ["1:0"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "wallet",
      "lines": [{"text": "Tu épargnes", "at": "0:0"}, {"text": "ce qui reste", "at": "0:1", "size": "m"}, {"text": "?", "at": "0:2", "size": "xl", "color": "gold"}],
      "reveal": {"html": "Il ne reste <em>jamais rien.</em>", "at": "1:1"}},
    "steps": {"type": "steps", "glow": "gold", "title": {"html": "Paie-toi <em>en premier</em>", "at": "2:0"}, "top": 500,
      "items": [{"icon": "wallet", "label": "Le salaire tombe", "sub": "le jour de la paie", "at": "3:0"},
                {"icon": "bolt", "label": "Virement automatique", "sub": "programmé une fois pour toutes", "at": "3:2"},
                {"icon": "piggy", "label": "Ton épargne", "sub": "avant toute dépense", "at": "3:3", "color": "up"}]},
    "counter": {"type": "counter", "glow": "green", "title": {"html": "<em>10 %</em> de ton salaire", "at": "4:0"}, "label": "Sur 2 000 € net", "color": "up",
      "stages": [{"to": 200, "at": "4:2", "label": "PAR MOIS"}, {"to": 2400, "at": "5:0", "label": "PAR AN", "dur": 1.1}],
      "badge": {"text": "AUTO ✓", "small": "SANS EFFORT", "at": "5:1", "color": "green"}},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("La règle d'or : on se paie en premier. Un virement automatique le jour de la paie, et l'épargne se fait toute seule. Tu l'as déjà mis en place ?",
               ["#paietoienpremier", "#virementautomatique"])}

# ---------------------------------------------------------------- 04 · Abonnements
eps[4] = {"title": "Les abonnements fantômes", "short": "ABONNEMENTS", "next": "Le vrai prix de ton café",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["COMBIEN", "Combien"], ["D'ABONNEMENTS", "d'abonnements"], ["*TU PAIES", "tu paies"], ["SANS T'EN SERVIR ?", "sans t'en servir ?"]]},
    {"segment": "hook", "chunks": [["FAISONS", "Faisons"], ["*LE COMPTE.", "le compte."]]},
    {"segment": "list", "sfx": "whoosh", "pause": 0.1, "chunks": [["STREAMING :", "Streaming :"], ["*14 €.", "quatorze euros."]]},
    {"segment": "list", "chunks": [["SALLE DE SPORT :", "Salle de sport :"], ["*30 €.", "trente euros."]]},
    {"segment": "list", "chunks": [["APPLIS ET JEUX :", "Applis et jeux :"], ["*8 €.", "huit euros."]]},
    {"segment": "list", "chunks": [["*52 € PAR MOIS,", "Cinquante-deux euros par mois,", "coin"], ["SOIT", "soit"], ["*624 € PAR AN.", "six cent vingt-quatre euros par an.", "coin"]]},
    {"segment": "icon", "sfx": "whoosh", "pause": 0.1, "chunks": [["CE SOIR,", "Ce soir,"], ["OUVRE TES RELEVÉS", "ouvre tes relevés"], ["*ET RÉSILIE.", "et résilie.", "stamp"]]},
    CTA()],
  "shakes": ["6:2"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "phone",
      "lines": [{"text": "Combien", "at": "0:0", "size": "m"}, {"text": "d'abonnements", "at": "0:1"}, {"text": "fantômes ?", "at": "0:2", "size": "xl", "hl": True}],
      "reveal": {"html": "Faisons le <em>compte</em>", "at": "1:0"}},
    "list": {"type": "list", "glow": "red", "chip": {"text": "CHAQUE MOIS", "at": "2:0", "color": "red"}, "top": 270,
      "items": [{"icon": "play", "label": "Streaming", "sub": "regardé 2 fois", "value": "14 €", "at": "2:0", "color": "ink"},
                {"icon": "dumbbell", "label": "Salle de sport", "sub": "pas mis les pieds", "value": "30 €", "at": "3:0", "color": "ink"},
                {"icon": "gamepad", "label": "Applis et jeux", "sub": "oubliées", "value": "8 €", "at": "4:0", "color": "ink"}],
      "total": {"label": "PAR MOIS", "color": "down", "stages": [{"to": 52, "at": "5:0", "label": "PAR MOIS"}, {"to": 624, "at": "5:2", "label": "PAR AN", "dur": 1.0}]}},
    "icon": {"type": "icon", "glow": "green", "icon": "cut", "color": "up", "at": "6:0", "text": "Ce soir, <em>résilie.</em>", "textAt": "6:2", "sub": "Vérifie tes 3 derniers relevés", "subAt": "6:1"},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("Streaming, salle de sport, applis… 52 € par mois partent sans que tu t'en rendes compte : 624 € par an. Lequel tu résilies ce soir ?",
               ["#abonnements", "#economiser"])}

# ---------------------------------------------------------------- 05 · Café
eps[5] = {"title": "Le vrai prix de ton café", "short": "PETITES DÉPENSES", "next": "Le défi des 52 semaines",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TON CAFÉ À 3 €", "Ton café à trois euros"], ["*COÛTE PLUS CHER", "coûte plus cher", "boom"], ["QUE TU NE CROIS.", "que tu ne crois."]]},
    {"segment": "counter", "sfx": "whoosh", "pause": 0.1, "chunks": [["*3 € PAR JOUR,", "Trois euros par jour,"], ["C'EST", "c'est"], ["*90 € PAR MOIS,", "quatre-vingt-dix euros par mois,"]]},
    {"segment": "counter", "chunks": [["ET", "et"], ["*1 095 € PAR AN.", "mille quatre-vingt-quinze euros par an.", "coin"]]},
    {"segment": "counter", "chunks": [["EN 10 ANS :", "En dix ans :"], ["*PLUS DE 10 000 €.", "plus de dix mille euros.", "stamp"]]},
    {"segment": "bars", "sfx": "whoosh", "pause": 0.1, "chunks": [["PAS BESOIN", "Pas besoin"], ["DE TOUT ARRÊTER :", "de tout arrêter :"]]},
    {"segment": "bars", "chunks": [["UN CAFÉ SUR DEUX", "Un café sur deux"], ["À LA MAISON,", "à la maison,"], ["ET TU GARDES", "et tu gardes"], ["*547 € PAR AN.", "cinq cent quarante-sept euros par an.", "coin"]]},
    CTA()],
  "shakes": ["0:1", "3:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "coffee",
      "lines": [{"text": "Ton café", "at": "0:0", "size": "m"}, {"text": "à 3 €", "at": "0:0+0.5", "size": "xl", "color": "gold"}, {"text": "coûte cher", "at": "0:1", "hl": True}]},
    "counter": {"type": "counter", "glow": "red", "title": {"html": "<em>3 €</em> par jour…", "at": "1:0"}, "label": "Dépensé en café", "color": "down",
      "stages": [{"to": 90, "at": "1:2", "label": "PAR MOIS"}, {"to": 1095, "at": "2:1", "label": "PAR AN"}, {"to": 10950, "at": "3:1", "label": "EN 10 ANS", "dur": 1.1}],
      "badge": {"text": "3 650", "small": "CAFÉS EN 10 ANS", "at": "3:1+0.9", "color": "red"}},
    "bars": {"type": "bars", "glow": "green", "title": {"html": "Un café sur deux <em>à la maison</em>", "at": "4:0"}, "label": "Par an", "top": 520,
      "items": [{"label": "Tous les jours", "sub": "au café", "value": 1095, "color": "down", "at": "4:1"},
                {"label": "1 sur 2", "sub": "à la maison", "value": 548, "color": "gold", "at": "5:1"}],
      "badge": {"text": "+547 €", "small": "POUR TOI", "at": "5:3", "color": "green"}},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("3 € par jour, ça paraît rien… jusqu'à ce que tu fasses le calcul sur un an. Pas besoin d'arrêter, juste de réduire. Tu dépenses combien en café ? ☕",
               ["#petitesdepenses", "#cafe"])}

# ---------------------------------------------------------------- 06 · 52 semaines
eps[6] = {"title": "Le défi des 52 semaines", "short": "DÉFI 52 SEMAINES", "next": "La règle des 72 heures",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["*1 378 €", "Mille trois cent soixante-dix-huit euros", "stamp"], ["EN UN AN,", "en un an,"], ["SANS TE PRIVER.", "sans te priver."]]},
    {"segment": "hook", "chunks": [["C'EST", "C'est"], ["*LE DÉFI DES 52 SEMAINES.", "le défi des cinquante-deux semaines."]]},
    {"segment": "grid", "sfx": "whoosh", "pause": 0.1, "chunks": [["SEMAINE 1 :", "Semaine un :"], ["*TU METS 1 €.", "tu mets un euro.", "coin"]]},
    {"segment": "grid", "chunks": [["SEMAINE 2 :", "Semaine deux :"], ["*2 €.", "deux euros.", "coin"]]},
    {"segment": "grid", "chunks": [["ET AINSI DE SUITE", "Et ainsi de suite,"], ["JUSQU'À 52 €.", "jusqu'à cinquante-deux euros."]]},
    {"segment": "grid", "chunks": [["À LA FIN DE L'ANNÉE :", "À la fin de l'année :"], ["*1 378 € DE CÔTÉ.", "mille trois cent soixante-dix-huit euros de côté.", "stamp"]]},
    CTA("pour relever le défi")],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "calendar",
      "lines": [{"text": "1 378 €", "at": "0:0", "size": "xl", "color": "gold"}, {"text": "en un an", "at": "0:1", "size": "m"}, {"text": "sans te priver", "at": "0:2", "size": "m"}],
      "reveal": {"html": "Le défi des <em>52 semaines</em>", "at": "1:1"}},
    "grid": {"type": "grid", "glow": "gold", "title": {"html": "Semaine <em>n</em> = <em>n</em> €", "at": "2:0"}, "top": 480, "cells": 52, "cols": 13,
      "fill": [[1, "2:1", "2:1"], [2, "3:1", "3:1"], [52, "4:0", "4:end"]],
      "counter": {"label": "Mis de côté", "mode": "sum"},
      "badge": {"text": "1 AN", "small": "52 SEMAINES", "at": "5:1", "color": "gold"}},
    "cta": {"type": "cta", "glow": "gold", "sub": "pour relever le défi"}},
  "post": post("Le défi des 52 semaines : 1 € la semaine 1, 2 € la semaine 2… jusqu'à 52 €. Résultat : 1 378 € en un an. Qui le commence avec moi lundi ? 💪",
               ["#defi52semaines", "#challengeepargne"])}

# ---------------------------------------------------------------- 07 · 72 heures
eps[7] = {"title": "La règle des 72 heures", "short": "RÈGLE DES 72 H", "next": "L'inflation et ton épargne",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TU CRAQUES SOUVENT", "Tu craques souvent"], ["*SUR DES ACHATS ?", "sur des achats ?", "boom"]]},
    {"segment": "hook", "chunks": [["TESTE", "Teste"], ["*LA RÈGLE DES 72 HEURES.", "la règle des soixante-douze heures."]]},
    {"segment": "timer", "sfx": "whoosh", "pause": 0.1, "chunks": [["UNE ENVIE D'ACHAT ?", "Une envie d'achat ?"], ["METS-LA AU PANIER", "Mets-la au panier,"], ["*ET ATTENDS 3 JOURS.", "et attends trois jours."]]},
    {"segment": "timer", "chunks": [["LA PLUPART DU TEMPS,", "La plupart du temps,"], ["*L'ENVIE PASSE.", "l'envie passe."]]},
    {"segment": "counter", "sfx": "whoosh", "pause": 0.1, "chunks": [["UN ACHAT DE 40 €", "Un achat de quarante euros"], ["ÉVITÉ PAR SEMAINE,", "évité par semaine,"], ["C'EST", "c'est"], ["*2 080 € PAR AN.", "deux mille quatre-vingts euros par an.", "coin"]]},
    CTA()],
  "shakes": ["0:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "cart",
      "lines": [{"text": "Tu craques", "at": "0:0"}, {"text": "souvent ?", "at": "0:1", "size": "xl", "hl": True}],
      "reveal": {"html": "La règle des <em>72 heures</em>", "at": "1:1"}},
    "timer": {"type": "timer", "glow": "gold", "chip": {"text": "ATTENDS 72 H", "at": "2:0"}, "icon": "cart", "hours": 72, "start": "2:2", "end": "3:1",
      "done": {"text": "✓ L'envie est passée", "at": "3:1"}},
    "counter": {"type": "counter", "glow": "green", "title": {"html": "<em>40 €</em> évités par semaine", "at": "4:0"}, "label": "Économisé", "color": "up",
      "stages": [{"to": 2080, "at": "4:2", "label": "PAR AN", "dur": 1.3}],
      "badge": {"text": "×52", "small": "SEMAINES", "at": "4:3+0.4", "color": "green"}},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("Avant d'acheter : panier, puis 72 heures d'attente. Dans la plupart des cas, l'envie passe et l'argent reste. Tu as déjà testé ? 🛒",
               ["#achatimpulsif", "#consommerresponsable"])}

# ---------------------------------------------------------------- 08 · Inflation
eps[8] = {"title": "L'inflation et ton épargne", "short": "INFLATION", "next": "Pourquoi commencer tôt",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TON ARGENT", "Ton argent"], ["*PERD DE LA VALEUR", "perd de la valeur", "boom"], ["EN DORMANT.", "en dormant."]]},
    {"segment": "hook", "chunks": [["LA FAUTE À", "La faute à"], ["*L'INFLATION.", "l'inflation."]]},
    {"segment": "counter", "sfx": "whoosh", "pause": 0.1, "chunks": [["AVEC 2 % PAR AN,", "Avec deux pour cent par an,"], ["*1 000 €", "mille euros"], ["D'AUJOURD'HUI", "d'aujourd'hui"]]},
    {"segment": "counter", "chunks": [["N'ACHÈTERONT PLUS", "n'achèteront plus"], ["*QUE POUR 820 €", "que pour huit cent vingt euros"], ["DANS 10 ANS.", "dans dix ans."]]},
    {"segment": "icon", "sfx": "whoosh", "pause": 0.1, "chunks": [["LA PARADE ?", "La parade ?"], ["UNE ÉPARGNE", "Une épargne"], ["*QUI RAPPORTE", "qui rapporte"], ["AU MOINS L'INFLATION.", "au moins autant que l'inflation."]]},
    CTA()],
  "shakes": ["0:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "moon",
      "lines": [{"text": "Ton argent", "at": "0:0", "size": "m"}, {"text": "fond", "at": "0:1", "size": "xl", "hl": True}, {"text": "en dormant", "at": "0:2", "size": "m"}],
      "reveal": {"html": "La faute à <em>l'inflation</em>", "at": "1:1"}},
    "counter": {"type": "counter", "glow": "red", "title": {"html": "<em>2 %</em> d'inflation par an", "at": "2:0"}, "label": "Pouvoir d'achat de 1 000 €", "color": "down",
      "from": 1000, "fromLabel": "AUJOURD'HUI", "stages": [{"to": 820, "at": "3:0", "label": "DANS 10 ANS", "dur": 1.6}],
      "badge": {"text": "−18 %", "small": "EN 10 ANS", "at": "3:1+0.3", "color": "red"}},
    "icon": {"type": "icon", "glow": "green", "icon": "shield", "color": "up", "at": "4:0", "text": "Fais-le <em>travailler</em>", "textAt": "4:2", "sub": "Rendement ≥ inflation", "subAt": "4:3"},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("Laisser son argent dormir, c'est perdre du pouvoir d'achat : avec 2 % d'inflation par an, 1 000 € n'en valent plus que 820 dans 10 ans. Ton épargne rapporte combien ?",
               ["#inflation", "#pouvoirdachat"])}

# ---------------------------------------------------------------- 09 · Commencer tôt
def fv(years, m=100, r=0.05):
    i = r / 12; n = round(years * 12)
    return m * ((1 + i) ** n - 1) / i if n > 0 else 0
ages = list(range(25, 66))
lea = [round(fv(a - 25)) for a in ages]
tom = [None if a < 35 else round(fv(a - 35)) for a in ages]
L, T = lea[-1], tom[-1]
eps[9] = {"title": "Pourquoi commencer tôt", "short": "COMMENCER TÔT", "next": "La méthode des enveloppes",
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["*100 € PAR MOIS.", "Cent euros par mois."], ["MÊME SOMME,", "Même somme,"], ["*RÉSULTAT PRESQUE DOUBLÉ ?", "résultat presque doublé ?", "boom"]]},
    {"segment": "curves", "sfx": "whoosh", "pause": 0.1, "chunks": [["LÉA COMMENCE", "Léa commence"], ["*À 25 ANS.", "à vingt-cinq ans."]]},
    {"segment": "curves", "chunks": [["TOM", "Tom"], ["À 35 ANS.", "à trente-cinq ans."]]},
    {"segment": "curves", "chunks": [["TOUS LES DEUX", "Tous les deux"], ["PLACENT À 5 %", "placent à cinq pour cent"], ["JUSQU'À 65 ANS.", "jusqu'à soixante-cinq ans."]]},
    {"segment": "curves", "chunks": [["LÉA :", "Léa :"], ["*152 000 €.", "cent cinquante-deux mille euros.", "coin"]]},
    {"segment": "curves", "chunks": [["TOM :", "Tom :"], ["83 000 €.", "quatre-vingt-trois mille euros."]]},
    {"segment": "curves", "chunks": [["10 ANS D'AVANCE", "Dix ans d'avance,"], ["*= 69 000 € DE PLUS.", "soixante-neuf mille euros de plus.", "stamp"]]},
    CTA()],
  "shakes": ["0:2"],
  "blocks": {
    "hook": {"type": "hook", "glow": "gold", "icon": "clock",
      "lines": [{"text": "100 €/mois", "at": "0:0", "size": "xl", "color": "gold"}, {"text": "même somme", "at": "0:1", "size": "m"}, {"text": "×2 ?", "at": "0:2", "size": "xl", "hl": True}]},
    "curves": {"type": "curves", "glow": "gold", "title": {"html": "Léa <em>vs</em> Tom", "at": "1:0"}, "label": "100 €/mois à 5 %/an", "top": 420,
      "xLabels": ["25 ans", "35", "45", "55", "65 ans"],
      "series": [{"name": "Léa", "color": "gold", "values": lea, "draw": ["1:1", "3:end"], "end": {"text": f"Léa · {L:,} €".replace(",", " "), "at": "4:1"}},
                 {"name": "Tom", "color": "#8f8573", "values": tom, "draw": ["2:1", "3:end"], "end": {"text": f"Tom · {T:,} €".replace(",", " "), "at": "5:1"}}],
      "badge": {"text": "+69 000 €", "small": "10 ANS D'AVANCE", "at": "6:1", "color": "gold", "top": 270},
      "disclaimer": "Exemple illustratif · rendement non garanti · intérêts mensuels"},
    "cta": {"type": "cta", "glow": "gold"}},
  "post": post("Même effort, 100 € par mois, mais 10 ans d'écart : 152 000 € contre 83 000 € à 65 ans (à 5 %/an, exemple illustratif). Le meilleur moment pour commencer, c'est maintenant. Tu as commencé à quel âge ?",
               ["#interetscomposes", "#investir"])}

# ---------------------------------------------------------------- 10 · Enveloppes
eps[10] = {"title": "La méthode des enveloppes", "short": "ENVELOPPES", "next": None,
  "sentences": [
    {"segment": "hook", "sfx": "whoosh", "chunks": [["TU NE SAIS JAMAIS", "Tu ne sais jamais"], ["*OÙ PASSE", "où passe", "boom"], ["TON ARGENT ?", "ton argent ?"]]},
    {"segment": "hook", "chunks": [["TESTE", "Teste"], ["*LA MÉTHODE DES ENVELOPPES.", "la méthode des enveloppes."]]},
    {"segment": "list", "sfx": "whoosh", "pause": 0.1, "chunks": [["CHAQUE MOIS,", "Chaque mois,"], ["UN BUDGET", "un budget"], ["PAR DÉPENSE.", "par type de dépense."]]},
    {"segment": "list", "chunks": [["COURSES :", "Courses :"], ["*350 €.", "trois cent cinquante euros."]]},
    {"segment": "list", "chunks": [["SORTIES :", "Sorties :"], ["*150 €.", "cent cinquante euros."]]},
    {"segment": "list", "chunks": [["TRANSPORT :", "Transport :"], ["*120 €.", "cent vingt euros."]]},
    {"segment": "icon", "sfx": "whoosh", "pause": 0.1, "chunks": [["ENVELOPPE VIDE ?", "Enveloppe vide ?"], ["*ON ARRÊTE.", "On arrête.", "stamp"], ["CE QUI RESTE", "Ce qui reste"], ["*PART EN ÉPARGNE.", "part en épargne.", "coin"]]},
    CTA("pour toute la série")],
  "shakes": ["0:1", "6:1"],
  "blocks": {
    "hook": {"type": "hook", "glow": "red", "icon": "envelope",
      "lines": [{"text": "Tu ne sais pas", "at": "0:0", "size": "m"}, {"text": "où passe", "at": "0:1", "size": "m"}, {"text": "ton argent ?", "at": "0:2", "hl": True}],
      "reveal": {"html": "La méthode des <em>enveloppes</em>", "at": "1:1"}},
    "list": {"type": "list", "glow": "gold", "title": {"html": "1 enveloppe = <em>1 budget</em>", "at": "2:0"}, "top": 500,
      "items": [{"icon": "basket", "label": "Courses", "value": "350 €", "at": "3:0", "color": "gold"},
                {"icon": "party", "label": "Sorties", "value": "150 €", "at": "4:0", "color": "gold"},
                {"icon": "bus", "label": "Transport", "value": "120 €", "at": "5:0", "color": "gold"}]},
    "icon": {"type": "icon", "glow": "green", "icon": "piggy", "color": "up", "at": "6:0", "text": "Le reste → <em>épargne</em>", "textAt": "6:2", "sub": "Enveloppe vide = on arrête", "subAt": "6:1"},
    "cta": {"type": "cta", "glow": "gold", "sub": "pour toute la série"}},
  "post": post("La méthode des enveloppes : un budget par type de dépense. Enveloppe vide, on arrête. Ce qui reste part en épargne. Simple, et ça marche. Tu utilises quelle méthode ?",
               ["#methodedesenveloppes", "#gestionbudget"])}

# ---------------------------------------------------------------- révisions (prononciation + durée ~30 s)
COMMON["speed"] = 1.0
def insert_before_cta(e, sentences, block_name=None, block=None):
    i = next(k for k, x in enumerate(e["sentences"]) if x["segment"] == "cta")
    e["sentences"][i:i] = sentences
    if block_name:
        e["blocks"] = {**{k: v for k, v in e["blocks"].items() if k != "cta"}, block_name: block, "cta": e["blocks"]["cta"]}
def n_cta(e):
    return next(k for k, x in enumerate(e["sentences"]) if x["segment"] == "cta")

# 02 : commencer à 10 %
e = eps[2]; k = n_cta(e)
insert_before_cta(e, [
  {"segment": "tip", "sfx": "whoosh", "pause": 0.1, "chunks": [["PAS ENCORE 20 % ?", "Pas encore vingt pour cent ?"], ["*COMMENCE PAR 10.", "Commence par dix."]]},
  {"segment": "tip", "chunks": [["CE QUI COMPTE,", "Ce qui compte,"], ["*C'EST LA RÉGULARITÉ.", "c'est la régularité."]]}],
  "tip", {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": f"{k}:0", "text": "Commence par <em>10 %</em>", "textAt": f"{k}:1", "sub": "La régularité compte plus que le montant", "subAt": f"{k+1}:0"})

# 03 : « un virement » mal prononcé → « programme un virement »
e = eps[3]
e["sentences"][3]["chunks"] = [["LE JOUR DE LA PAIE,", "Le jour de la paie,"], ["PROGRAMME UN VIREMENT", "programme un virement"], ["*AUTOMATIQUE", "automatique"], ["VERS TON ÉPARGNE.", "vers ton épargne."]]
k = n_cta(e)
insert_before_cta(e, [
  {"segment": "tip", "sfx": "whoosh", "pause": 0.1, "chunks": [["FAIS-LE AUJOURD'HUI :", "Fais-le aujourd'hui :"], ["*DEUX MINUTES", "deux minutes"], ["DANS TON APPLI BANCAIRE.", "dans ton appli bancaire."]]}],
  "tip", {"type": "icon", "glow": "gold", "icon": "phone", "color": "gold", "at": f"{k}:0", "text": "Fais-le <em>aujourd'hui</em>", "textAt": f"{k}:1", "sub": "2 minutes dans ton appli bancaire", "subAt": f"{k}:2"})

# 04 : hook, « applis » et « relevés » reformulés
e = eps[4]
e["sentences"][0]["chunks"] = [["TU PAIES", "Tu paies"], ["COMBIEN D'ABONNEMENTS", "combien d'abonnements"], ["*POUR RIEN ?", "pour rien ?"]]
e["blocks"]["hook"]["lines"] = [{"text": "Tu paies", "at": "0:0", "size": "m"}, {"text": "combien", "at": "0:1", "size": "m"}, {"text": "d'abonnements", "at": "0:1+0.4"}, {"text": "pour rien ?", "at": "0:2", "size": "xl", "hl": True}]
e["sentences"][4]["chunks"] = [["LES APPLIS :", "Les applis :"], ["*8 €.", "huit euros."]]
e["blocks"]["list"]["items"][2]["label"] = "Applis"
e["sentences"][6]["chunks"] = [["CE SOIR,", "Ce soir,"], ["REGARDE TES RELEVÉS", "regarde tes relevés bancaires"], ["*ET RÉSILIE.", "et résilie.", "stamp"]]
k = n_cta(e)
insert_before_cta(e, [{"segment": "icon", "chunks": [["GARDE SEULEMENT", "Garde seulement"], ["CE QUE TU UTILISES", "ce que tu utilises"], ["*CHAQUE SEMAINE.", "chaque semaine."]]}])
e["blocks"]["icon"]["sub"] = "Garde seulement ce que tu utilises chaque semaine"
e["blocks"]["icon"]["subAt"] = f"{k}:0"

# 05 : « 1 095 € » mal lu → « plus de mille euros »
e = eps[5]
e["sentences"][2]["chunks"] = [["ET", "et"], ["*+ DE 1 000 € PAR AN.", "plus de mille euros par an.", "coin"]]
k = n_cta(e)
insert_before_cta(e, [{"segment": "tip", "sfx": "whoosh", "pause": 0.1, "chunks": [["PAREIL POUR", "Pareil pour"], ["*LES LIVRAISONS DE REPAS", "les livraisons de repas"], ["ET LES PETITS ACHATS.", "et les petits achats en ligne."]]}],
  "tip", {"type": "icon", "glow": "gold", "icon": "basket", "color": "gold", "at": f"{k}:0", "text": "Pareil pour <em>les petits achats</em>", "textAt": f"{k}:1", "sub": "livraisons, achats en ligne, snacks…", "subAt": f"{k}:2"})

# 06 : « semaine un / deux » mal prononcés
e = eps[6]
e["sentences"][2]["chunks"] = [["LA 1RE SEMAINE,", "La première semaine,"], ["*TU METS 1 €.", "tu mets un euro.", "coin"]]
e["sentences"][3]["chunks"] = [["LA 2E,", "La deuxième,"], ["*2 €.", "deux euros.", "coin"]]
k = n_cta(e)
insert_before_cta(e, [
  {"segment": "tip", "sfx": "whoosh", "pause": 0.1, "chunks": [["ASTUCE :", "Astuce :"], ["*FAIS-LE À L'ENVERS,", "fais-le à l'envers,"], ["DE 52 À 1.", "de cinquante-deux à un."]]},
  {"segment": "tip", "chunks": [["DÉCEMBRE", "Décembre"], ["*DEVIENT LE MOIS LE PLUS LÉGER.", "devient le mois le plus léger."]]}],
  "tip", {"type": "icon", "glow": "gold", "icon": "bolt", "color": "gold", "at": f"{k}:0", "text": "Astuce : <em>à l'envers</em>", "textAt": f"{k}:1", "sub": "52 € en janvier… 1 € à Noël", "subAt": f"{k+1}:0"})

# 07 : toujours envie ? achète
e = eps[7]; k = n_cta(e)
insert_before_cta(e, [{"segment": "tip", "sfx": "whoosh", "pause": 0.1, "chunks": [["ET SI L'ENVIE", "Et si l'envie"], ["EST TOUJOURS LÀ ?", "est toujours là ?"], ["*ACHÈTE,", "Achète,"], ["SANS CULPABILISER.", "sans culpabiliser."]]}],
  "tip", {"type": "icon", "glow": "green", "icon": "check", "color": "up", "at": f"{k}:0", "text": "Toujours envie ? <em>Achète.</em>", "textAt": f"{k}:2", "sub": "sans culpabiliser", "subAt": f"{k}:3"})

# 08 : comparer le taux de son livret
e = eps[8]; k = n_cta(e)
insert_before_cta(e, [{"segment": "icon", "chunks": [["COMPARE LE TAUX", "Compare le taux"], ["DE TON LIVRET", "de ton livret"], ["*À L'INFLATION.", "à l'inflation."]]}])
e["blocks"]["icon"]["sub"] = "Compare le taux de ton livret à l'inflation"
e["blocks"]["icon"]["subAt"] = f"{k}:0"

# 09 : prénoms et « placent » mal prononcés → Emma et Lucas
e = eps[9]
e["sentences"][1]["chunks"] = [["EMMA COMMENCE", "Emma commence"], ["*À 25 ANS.", "à vingt-cinq ans."]]
e["sentences"][2]["chunks"] = [["LUCAS", "Lucas"], ["À 35 ANS.", "à trente-cinq ans."]]
e["sentences"][3]["chunks"] = [["TOUS LES DEUX", "Tous les deux"], ["INVESTISSENT À 5 %", "investissent à cinq pour cent par an,"], ["JUSQU'À 65 ANS.", "jusqu'à soixante-cinq ans."]]
e["sentences"][4]["chunks"] = [["EMMA :", "Emma :"], ["*152 000 €.", "cent cinquante-deux mille euros.", "coin"]]
e["sentences"][5]["chunks"] = [["LUCAS :", "Lucas :"], ["83 000 €.", "quatre-vingt-trois mille euros."]]
k = n_cta(e)
insert_before_cta(e, [{"segment": "curves", "chunks": [["LE TEMPS COMPTE", "Le temps compte"], ["*PLUS QUE LE MONTANT.", "plus que le montant."]]}])
cv = e["blocks"]["curves"]
cv["title"]["html"] = "Emma <em>vs</em> Lucas"
cv["series"][0]["name"] = "Emma"; cv["series"][0]["end"]["text"] = cv["series"][0]["end"]["text"].replace("Léa", "Emma")
cv["series"][0]["end"]["y"] = 100
cv["series"][1]["end"]["y"] = 170
cv["series"][1]["name"] = "Lucas"; cv["series"][1]["end"]["text"] = cv["series"][1]["end"]["text"].replace("Tom", "Lucas")
e["post"]["caption"] = e["post"]["caption"]

# 10 : « par type de dépense » et « part en épargne »
e = eps[10]
e["sentences"][2]["chunks"] = [["CHAQUE MOIS,", "Chaque mois,"], ["UN BUDGET", "tu fixes un budget"], ["POUR CHAQUE DÉPENSE.", "pour chaque dépense."]]
e["sentences"][6]["chunks"] = [["ENVELOPPE VIDE ?", "Enveloppe vide ?"], ["*ON ARRÊTE.", "On arrête.", "stamp"], ["CE QUI RESTE", "Ce qui reste"], ["*VA SUR TON ÉPARGNE.", "va sur ton épargne.", "coin"]]
k = n_cta(e)
insert_before_cta(e, [{"segment": "icon", "chunks": [["ÇA MARCHE AUSSI", "Ça marche aussi"], ["*AVEC PLUSIEURS COMPTES.", "avec plusieurs comptes."]]}])
e["blocks"]["icon"]["sub"] = "Ça marche aussi avec plusieurs comptes"
e["blocks"]["icon"]["subAt"] = f"{k}:0"

for n, e in eps.items():
    data = {"_doc": "Épisode de la série Épargne malin. Voir serie/README.md.", "ep": n, **COMMON, **e}
    (OUT / f"ep{n:02d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sorted(eps))
