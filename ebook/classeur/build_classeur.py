# -*- coding: utf-8 -*-
"""Classeur compagnon d'« Argent Maîtrisé ». Charte du guide : encre, vert sapin, ivoire."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

INK, GREEN, IVORY, TINT, LINE, RED = "16202A", "0E6B5C", "F7F8F6", "E9F4F0", "D9E0E3", "C0392B"
F = "Arial"
EUR, EUR0, PCT, PTS = '#,##0 "€"', '#,##0.00 "€"', '0.0%', '+0.0;-0.0;0.0'

thin = Side(style="thin", color=LINE)
box = Border(left=thin, right=thin, top=thin, bottom=thin)
topline = Border(top=Side(style="thin", color=INK))

def title(ws, row, text, sub=""):
    ws.cell(row, 1, text).font = Font(F, 16, bold=True, color=INK)
    if sub:
        ws.cell(row + 1, 1, sub).font = Font(F, 9, italic=True, color="6B7A86")
    return row + (3 if sub else 2)

def header(ws, row, cols, widths=None):
    for i, c in enumerate(cols, start=1):
        cell = ws.cell(row, i, c)
        cell.font = Font(F, 10, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=INK)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = box
    ws.row_dimensions[row].height = 26
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return row + 1

def section(ws, row, text, span=2):
    c = ws.cell(row, 1, text)
    c.font = Font(F, 10, bold=True, color=GREEN)
    for i in range(1, span + 1):
        ws.cell(row, i).fill = PatternFill("solid", fgColor=TINT)
        ws.cell(row, i).border = box
    return row + 1

def inp(ws, row, label, value, col=2, fmt=EUR, note=None):
    ws.cell(row, 1, label).font = Font(F, 10, color=INK)
    ws.cell(row, 1).border = box
    c = ws.cell(row, col, value)
    c.font = Font(F, 10, color="0000FF")
    c.fill = PatternFill("solid", fgColor="FFFDF0")
    c.number_format = fmt
    c.border = box
    if note:
        n = ws.cell(row, col + 1, note)
        n.font = Font(F, 9, italic=True, color="6B7A86")
    return row + 1

def calc(ws, row, label, formula, col=2, fmt=EUR, bold=True, big=False):
    c0 = ws.cell(row, 1, label)
    c0.font = Font(F, 11 if big else 10, bold=bold, color=INK)
    c0.border = topline if bold else box
    c = ws.cell(row, col, formula)
    c.font = Font(F, 12 if big else 10, bold=bold, color=GREEN if big else INK)
    c.number_format = fmt
    c.border = topline if bold else box
    return row + 1

wb = Workbook()

# ============================= Mode d'emploi =============================
ws = wb.active
ws.title = "Mode d'emploi"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 100
r = 1
ws.cell(r, 1, "ARGENT MAÎTRISÉ — Classeur compagnon").font = Font(F, 20, bold=True, color=INK); r += 1
ws.cell(r, 1, "Les six outils du guide, prêts à remplir.").font = Font(F, 11, italic=True, color=GREEN); r += 3

for h, lines in [
 ("Comment lire ce classeur", [
   "• Les cellules en BLEU sur fond crème sont les seules à remplir. Tout le reste se calcule tout seul.",
   "• Les totaux et les résultats sont en noir ou en vert : ne les écrasez pas, vous casseriez les formules.",
   "• Chaque feuille est pré-remplie avec l'exemple chiffré du guide. Remplacez ces valeurs par les vôtres.",
 ]),
 ("Les six feuilles, et le chapitre correspondant", [
   "1. Entrées-sorties     — chapitre 1 : ce qui entre, ce qui sort, et votre solde réel.",
   "2. Bilan               — chapitre 2 : actifs moins dettes, et vos trois ratios.",
   "3. Suivi               — chapitres 2 et 31 : le patrimoine net trimestre par trimestre.",
   "4. Allocation          — chapitres 19 et 20 : cible contre réel, et la perte envisageable en euros.",
   "5. Locatif             — chapitre 26 : le calcul complet d'un projet, charges comprises.",
   "6. Plan 90 jours       — chapitre 30 : les 26 actions, à cocher.",
 ]),
 ("L'ordre recommandé", [
   "Remplissez la feuille 1 d'abord : tout le reste en dépend. Le solde mensuel alimente le bilan,",
   "le total des dépenses détermine votre épargne de précaution, et la capacité d'épargne fixe",
   "le montant de votre virement automatique.",
 ]),
 ("Avertissement", [
   "Ce classeur est un outil de calcul personnel, pas un conseil en investissement.",
   "Les résultats dépendent entièrement des hypothèses que vous saisissez.",
   "Vérifiez les chiffres réglementaires à leur source officielle avant toute décision.",
 ]),
]:
    ws.cell(r, 1, h).font = Font(F, 12, bold=True, color=GREEN); r += 1
    for ln in lines:
        ws.cell(r, 1, ln).font = Font(F, 10, color=INK); r += 1
    r += 1

# ============================= 1. Entrées-sorties =============================
ws = wb.create_sheet("1. Entrées-sorties")
ws.sheet_view.showGridLines = False
r = title(ws, 1, "Vos entrées et vos sorties", "Chapitre 1 — relevez trois mois, ne reconstituez rien de mémoire.")
r = header(ws, r, ["Poste", "Montant mensuel", "Remarque"], [46, 18, 46])

r = section(ws, r, "ENTRÉES", 3)
e0 = r
for lab, val, note in [("Salaire net 1", 2310, "Ce qui arrive réellement sur le compte"),
                       ("Salaire net 2", 0, ""),
                       ("Primes et 13e mois (annuel ÷ 12)", 150, "1 800 € ÷ 12 dans l'exemple"),
                       ("Revenus d'activité indépendante", 0, "Moyenne sur 12 mois, jamais le meilleur mois"),
                       ("Allocations et prestations", 0, ""),
                       ("Revenus locatifs nets", 0, ""),
                       ("Autres", 0, "")]:
    r = inp(ws, r, lab, val, note=note)
e1 = r - 1
r = calc(ws, r, "TOTAL DES ENTRÉES", f"=SUM(B{e0}:B{e1})"); ENT = r - 1
r += 1

r = section(ws, r, "SORTIES — CHARGES FIXES", 3)
f0 = r
for lab, val in [("Loyer ou mensualité de crédit", 820), ("Charges de copropriété", 110),
                 ("Électricité, gaz, eau", 95), ("Internet et mobile", 48),
                 ("Assurances (habitation, auto)", 72), ("Transports (abonnement)", 0),
                 ("Crédits à la consommation", 0), ("Garde d'enfants, scolarité", 0),
                 ("Abonnements divers", 39)]:
    r = inp(ws, r, lab, val)
f1 = r - 1
r = calc(ws, r, "Sous-total charges fixes", f"=SUM(B{f0}:B{f1})", bold=False); FIX = r - 1
ws.cell(FIX, 1).font = Font(F, 10, bold=True, color=INK)
r += 1

r = section(ws, r, "SORTIES — DÉPENSES VARIABLES", 3)
v0 = r
for lab, val in [("Courses", 380), ("Carburant et transports", 145),
                 ("Restaurants et sorties", 190), ("Vêtements", 60),
                 ("Loisirs", 50), ("Santé non remboursée", 0), ("Divers", 0)]:
    r = inp(ws, r, lab, val)
v1 = r - 1
r = calc(ws, r, "Sous-total dépenses variables", f"=SUM(B{v0}:B{v1})", bold=False); VAR = r - 1
ws.cell(VAR, 1).font = Font(F, 10, bold=True, color=INK)
r += 1

r = section(ws, r, "SORTIES — DÉPENSES ANNUELLES (le bloc que tout le monde oublie)", 3)
hr = r
for i, t in enumerate(["Poste", "Montant ANNUEL", "Ramené au mois"], start=1):
    c = ws.cell(hr, i, t); c.font = Font(F, 9, bold=True, color="6B7A86"); c.border = box
r += 1
a0 = r
for lab, val in [("Taxe foncière", 980), ("Impôt sur le revenu non mensualisé", 0),
                 ("Assurances à échéance annuelle", 0), ("Entretien et contrôle du véhicule", 600),
                 ("Vacances", 1500), ("Cadeaux et fêtes", 400),
                 ("Rentrée scolaire", 0), ("Mutuelle", 0), ("Cotisations professionnelles", 0)]:
    ws.cell(r, 1, lab).font = Font(F, 10, color=INK); ws.cell(r, 1).border = box
    c = ws.cell(r, 2, val); c.font = Font(F, 10, color="0000FF")
    c.fill = PatternFill("solid", fgColor="FFFDF0"); c.number_format = EUR; c.border = box
    m = ws.cell(r, 3, f"=B{r}/12"); m.font = Font(F, 10, color=INK); m.number_format = EUR; m.border = box
    r += 1
a1 = r - 1
ws.cell(r, 1, "Sous-total annualisé, ramené au mois").font = Font(F, 10, bold=True, color=INK)
ws.cell(r, 1).border = topline
c = ws.cell(r, 3, f"=SUM(C{a0}:C{a1})"); c.font = Font(F, 10, bold=True, color=INK)
c.number_format = EUR; c.border = topline
ANN = r
r += 2

r = calc(ws, r, "TOTAL DES SORTIES", f"=B{FIX}+B{VAR}+C{ANN}"); SOR = r - 1
r = calc(ws, r, "SOLDE MENSUEL", f"=B{ENT}-B{SOR}", big=True); SOL = r - 1
r = calc(ws, r, "Taux d'épargne", f"=IF(B{ENT}=0,0,B{SOL}/B{ENT})", fmt=PCT, big=True); TAUX = r - 1
r += 1
ws.cell(r, 1, "Lecture").font = Font(F, 10, bold=True, color=GREEN)
lect = (f'=IF(B{ENT}=0,"Remplissez vos entrées",'
        f'IF(B{SOL}<0,"Solde négatif — réduire les charges fixes et traiter les dettes coûteuses avant d\'investir",'
        f'IF(B{TAUX}<0.05,"Marge très faible — dégager du surplus avant toute autre chose",'
        f'IF(B{TAUX}<0.15,"Situation courante — automatiser et capter les augmentations",'
        f'IF(B{TAUX}<0.25,"Bonne dynamique — structurer : précaution, puis investissement",'
        f'"Trajectoire d\'indépendance — optimiser allocation et fiscalité")))))')
c = ws.cell(r, 2, lect); c.font = Font(F, 10, bold=True, color=INK)
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
r += 2
r = calc(ws, r, "Épargne de précaution — cible 3 mois de dépenses", f"=B{SOR}*3", bold=False)
r = calc(ws, r, "Épargne de précaution — cible 6 mois de dépenses", f"=B{SOR}*6", bold=False)
r = calc(ws, r, "Épargne de précaution — cible 12 mois (indépendant)", f"=B{SOR}*12", bold=False)

ws.conditional_formatting.add(f"B{SOL}",
    CellIsRule(operator="lessThan", formula=["0"], font=Font(F, 12, bold=True, color=RED)))
ws.freeze_panes = "A4"
S1 = "'1. Entrées-sorties'"

# ============================= 2. Bilan =============================
ws = wb.create_sheet("2. Bilan")
ws.sheet_view.showGridLines = False
r = title(ws, 1, "Bilan patrimonial", "Chapitre 2 — actifs moins dettes. Datez-le, c'est la pente qui compte.")
r = inp(ws, r, "Date du bilan", "01/01/2026", fmt="@", note="Refaites-le chaque trimestre")
r += 1
r = header(ws, r, ["Poste", "Montant", "Remarque"], [46, 18, 46])
r = section(ws, r, "ACTIFS", 3)
ac0 = r
for lab, val, note in [("Comptes courants", 4200, ""), ("Livret A, LDDS, LEP", 11000, ""),
                       ("Assurance-vie (valeur de rachat)", 9500, ""), ("PEA", 0, ""),
                       ("Compte-titres ordinaire", 0, ""), ("PER et épargne retraite", 0, ""),
                       ("Épargne salariale (PEE, PERCO)", 6800, ""),
                       ("Immobilier", 215000, "Estimation réaliste, pas optimiste"),
                       ("SCPI, parts de société, autres", 0, "")]:
    r = inp(ws, r, lab, val, note=note)
ac1 = r - 1
r = calc(ws, r, "TOTAL DES ACTIFS", f"=SUM(B{ac0}:B{ac1})"); ACT = r - 1
r += 1
r = section(ws, r, "DETTES", 3)
de0 = r
for lab, val in [("Crédit immobilier (capital restant dû)", 168000), ("Crédits à la consommation, auto", 4300),
                 ("Découvert, crédit renouvelable, fractionnés", 0), ("Dettes fiscales et sociales", 0)]:
    r = inp(ws, r, lab, val)
de1 = r - 1
r = calc(ws, r, "TOTAL DES DETTES", f"=SUM(B{de0}:B{de1})"); DET = r - 1
r += 1
r = calc(ws, r, "PATRIMOINE NET", f"=B{ACT}-B{DET}", big=True); PN = r - 1
r += 1
r = section(ws, r, "LES TROIS RATIOS", 3)
r = inp(ws, r, "Mensualités de crédit totales", 820, note="Pour le taux d'endettement")
MENS = r - 1
r = calc(ws, r, "Taux d'épargne", f"=IF({S1}!B{ENT}=0,0,{S1}!B{SOL}/{S1}!B{ENT})", fmt=PCT, bold=False)
r = calc(ws, r, "Taux d'endettement", f"=IF({S1}!B{ENT}=0,0,B{MENS}/{S1}!B{ENT})", fmt=PCT, bold=False)
END = r - 1
r = calc(ws, r, "Mois de coussin", f"=IF({S1}!B{SOR}=0,0,(B{ac0}+B{ac0+1})/{S1}!B{SOR})",
         fmt='0.0 "mois"', bold=False)
COU = r - 1
ws.conditional_formatting.add(f"B{END}",
    CellIsRule(operator="greaterThan", formula=["0.33"], font=Font(F, 10, bold=True, color=RED)))
ws.conditional_formatting.add(f"B{COU}",
    CellIsRule(operator="lessThan", formula=["3"], font=Font(F, 10, bold=True, color=RED)))
ws.freeze_panes = "A4"

# ============================= 3. Suivi =============================
ws = wb.create_sheet("3. Suivi")
ws.sheet_view.showGridLines = False
r = title(ws, 1, "Suivi trimestriel", "Chapitres 2 et 31 — une ligne par trimestre, toujours le même jour.")
r = header(ws, r, ["Trimestre", "Patrimoine net", "Variation", "Épargne versée", "Effet marché", "Commentaire"],
           [16, 18, 16, 16, 16, 40])
first = r
for i in range(16):
    lab = ["T1 2026", "T2 2026"][i] if i < 2 else ""
    val = [74200, 76800][i] if i < 2 else None
    eps = [None, 1500][i] if i < 2 else None
    c = ws.cell(r, 1, lab); c.font = Font(F, 10, color="0000FF"); c.border = box
    c.fill = PatternFill("solid", fgColor="FFFDF0")
    c = ws.cell(r, 2, val); c.font = Font(F, 10, color="0000FF"); c.number_format = EUR; c.border = box
    c.fill = PatternFill("solid", fgColor="FFFDF0")
    if i == 0:
        ws.cell(r, 3, "").border = box
        ws.cell(r, 5, "").border = box
    else:
        c = ws.cell(r, 3, f"=IF(OR(B{r}=\"\",B{r-1}=\"\"),\"\",B{r}-B{r-1})")
        c.font = Font(F, 10, color=INK); c.number_format = EUR; c.border = box
        c = ws.cell(r, 5, f"=IF(OR(C{r}=\"\",D{r}=\"\"),\"\",C{r}-D{r})")
        c.font = Font(F, 10, color=INK); c.number_format = EUR; c.border = box
    c = ws.cell(r, 4, eps); c.font = Font(F, 10, color="0000FF"); c.number_format = EUR; c.border = box
    c.fill = PatternFill("solid", fgColor="FFFDF0")
    ws.cell(r, 6, "").border = box
    r += 1
last = r - 1
r += 1
ws.cell(r, 1, "La colonne « effet marché » sépare ce que vous avez construit de ce que les marchés ont fait.").font = Font(F, 9, italic=True, color="6B7A86")
ws.freeze_panes = "A4"

# ============================= 4. Allocation =============================
ws = wb.create_sheet("4. Allocation")
ws.sheet_view.showGridLines = False
r = title(ws, 1, "Allocation cible et réelle", "Chapitres 19 et 20 — agir au-delà de 5 points d'écart.")
r = header(ws, r, ["Poche", "Cible", "Montant réel", "Réel", "Écart (points)", "Action"],
           [32, 12, 18, 12, 16, 26])
p0 = r
for lab, cible, reel in [("Actions monde", 0.45, 22000), ("Actions émergents", 0.10, 4000),
                         ("Obligations", 0.25, 9000), ("Fonds euros et monétaire", 0.20, 13000),
                         ("Immobilier (SCPI)", 0.00, 0), ("Autres", 0.00, 0)]:
    ws.cell(r, 1, lab).font = Font(F, 10, color=INK); ws.cell(r, 1).border = box
    c = ws.cell(r, 2, cible); c.font = Font(F, 10, color="0000FF"); c.number_format = PCT
    c.fill = PatternFill("solid", fgColor="FFFDF0"); c.border = box
    c = ws.cell(r, 3, reel); c.font = Font(F, 10, color="0000FF"); c.number_format = EUR
    c.fill = PatternFill("solid", fgColor="FFFDF0"); c.border = box
    r += 1
p1 = r - 1
TOTC = p1 + 1
for i in range(p0, p1 + 1):
    c = ws.cell(i, 4, f"=IF($C${TOTC}=0,0,C{i}/$C${TOTC})")
    c.font = Font(F, 10, color=INK); c.number_format = PCT; c.border = box
    c = ws.cell(i, 5, f"=(D{i}-B{i})*100"); c.font = Font(F, 10, color=INK)
    c.number_format = PTS; c.border = box
    c = ws.cell(i, 6, f'=IF(ABS(E{i})>5,"Rééquilibrer","OK")')
    c.font = Font(F, 10, color=INK); c.border = box
ws.cell(TOTC, 1, "TOTAL").font = Font(F, 10, bold=True, color=INK)
ws.cell(TOTC, 1).border = topline
for col, form, fmt in ((2, f"=SUM(B{p0}:B{p1})", PCT), (3, f"=SUM(C{p0}:C{p1})", EUR),
                       (4, f"=SUM(D{p0}:D{p1})", PCT)):
    c = ws.cell(TOTC, col, form); c.font = Font(F, 10, bold=True, color=INK)
    c.number_format = fmt; c.border = topline
c = ws.cell(TOTC, 6, f'=IF(ROUND(B{TOTC},4)<>1,"La colonne Cible doit totaliser 100 %","")')
c.font = Font(F, 10, bold=True, color=RED)
r = TOTC + 2
r = section(ws, r, "LE TEST EN EUROS (chapitre 19)", 6)
r = calc(ws, r, "Part actions", f"=IF(C{TOTC}=0,0,(C{p0}+C{p0+1})/C{TOTC})", fmt=PCT, bold=False)
PA = r - 1
r = calc(ws, r, "Baisse envisageable en crise (part actions × 45 %)", f"=C{TOTC}*B{PA}*0.45", bold=False)
BA = r - 1
r = calc(ws, r, "Valeur du portefeuille au plus bas", f"=C{TOTC}-B{BA}", big=True)
r += 1
ws.cell(r, 1, "Si ce montant vous ferait vendre, votre part actions est trop élevée. Baissez-la.").font = Font(F, 9, italic=True, color="6B7A86")
ws.conditional_formatting.add(f"E{p0}:E{p1}",
    CellIsRule(operator="greaterThan", formula=["5"], font=Font(F, 10, bold=True, color=RED)))
ws.conditional_formatting.add(f"E{p0}:E{p1}",
    CellIsRule(operator="lessThan", formula=["-5"], font=Font(F, 10, bold=True, color=RED)))
ws.freeze_panes = "A4"

# ============================= 5. Locatif =============================
ws = wb.create_sheet("5. Locatif")
ws.sheet_view.showGridLines = False
r = title(ws, 1, "Cash-flow d'un investissement locatif",
          "Chapitre 26 — les charges pèsent 25 à 35 % du loyer. Ne les oubliez pas.")
r = header(ws, r, ["Paramètre", "Valeur", "Remarque"], [46, 18, 46])
r = section(ws, r, "L'OPÉRATION", 3)
r = inp(ws, r, "Prix d'achat", 150000); PRIX = r - 1
r = inp(ws, r, "Frais de notaire", 0.0767, fmt=PCT, note="7 à 8 % dans l'ancien, 2 à 3 % dans le neuf"); NOT = r - 1
r = inp(ws, r, "Travaux", 8500); TRAV = r - 1
r = inp(ws, r, "Frais de dossier et garantie", 0); GAR = r - 1
r = calc(ws, r, "Coût total de l'opération", f"=B{PRIX}*(1+B{NOT})+B{TRAV}+B{GAR}", big=True); COUT = r - 1
r += 1
r = section(ws, r, "LE FINANCEMENT", 3)
r = inp(ws, r, "Apport", 0); APP = r - 1
r = inp(ws, r, "Taux du crédit (hors assurance)", 0.035, fmt=PCT); TX = r - 1
r = inp(ws, r, "Assurance emprunteur (par an)", 0.003, fmt=PCT, note="% du capital emprunté"); ASS = r - 1
r = inp(ws, r, "Durée (années)", 20, fmt="0"); DUR = r - 1
r = calc(ws, r, "Montant emprunté", f"=B{COUT}-B{APP}", bold=False); EMP = r - 1
r = calc(ws, r, "Mensualité de crédit", f"=IF(OR(B{TX}=0,B{DUR}=0),0,-PMT(B{TX}/12,B{DUR}*12,B{EMP}))",
         fmt=EUR0, bold=False); CRED = r - 1
r = calc(ws, r, "Assurance mensuelle", f"=B{EMP}*B{ASS}/12", fmt=EUR0, bold=False); AMEN = r - 1
r = calc(ws, r, "Mensualité totale", f"=B{CRED}+B{AMEN}", fmt=EUR0, big=True); MENSU = r - 1
r += 1
r = section(ws, r, "LES REVENUS", 3)
r = inp(ws, r, "Loyer mensuel hors charges", 750); LOY = r - 1
r = inp(ws, r, "Provision pour vacance locative", 0.04, fmt=PCT, note="1 mois tous les 2 ans ≈ 4 %"); VAC = r - 1
r = calc(ws, r, "Loyer annuel brut", f"=B{LOY}*12", bold=False); LAN = r - 1
r = calc(ws, r, "Loyer annuel après vacance", f"=B{LAN}*(1-B{VAC})", bold=False); LNET = r - 1
r += 1
r = section(ws, r, "LES CHARGES ANNUELLES", 3)
ch0 = r
for lab, val, note in [("Taxe foncière", 900, ""), ("Copropriété non récupérable", 600, ""),
                       ("Assurance propriétaire non occupant", 150, ""),
                       ("Comptabilité", 400, "Si régime réel"),
                       ("Assurance loyers impayés", 0, "2 à 3 % des loyers")]:
    r = inp(ws, r, lab, val, note=note)
ch1 = r - 1
r = inp(ws, r, "Frais de gestion", 0.07, fmt=PCT, note="6 à 9 % si vous déléguez"); GES = r - 1
r = inp(ws, r, "Provision pour travaux", 0.08, fmt=PCT, note="5 à 10 % des loyers"); PTR = r - 1
r = calc(ws, r, "Total des charges annuelles",
         f"=SUM(B{ch0}:B{ch1})+B{LAN}*B{GES}+B{LAN}*B{PTR}"); CHT = r - 1
r += 1
r = section(ws, r, "LE RÉSULTAT", 3)
r = calc(ws, r, "Revenu net de charges (annuel)", f"=B{LNET}-B{CHT}", bold=False); REV = r - 1
r = calc(ws, r, "CASH-FLOW MENSUEL AVANT IMPÔT", f"=B{REV}/12-B{MENSU}", fmt=EUR0, big=True); CF = r - 1
r = calc(ws, r, "Rendement brut", f"=IF(B{COUT}=0,0,B{LAN}/B{COUT})", fmt=PCT, bold=False)
r = calc(ws, r, "Rendement net de charges", f"=IF(B{COUT}=0,0,B{REV}/B{COUT})", fmt=PCT, bold=False)
r = calc(ws, r, "Effort d'épargne total sur la durée du crédit",
         f'=IF(B{CF}>=0,0,-B{CF}*12*B{DUR})', bold=False)
r += 1
c = ws.cell(r, 1, f'=IF(B{CF}>=0,"Cash-flow positif — vérifiez que les provisions sont réalistes avant de conclure.","Ce projet exige un effort d\'épargne mensuel. Ce n\'est pas disqualifiant, mais il ne s\'autofinance pas.")')
c.font = Font(F, 10, bold=True, color=INK)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
r += 1
ws.cell(r, 1, "Faites valider le régime fiscal par un expert-comptable avant de signer.").font = Font(F, 9, italic=True, color="6B7A86")
ws.conditional_formatting.add(f"B{CF}",
    CellIsRule(operator="lessThan", formula=["0"], font=Font(F, 12, bold=True, color=RED)))
ws.freeze_panes = "A4"

# ============================= 6. Plan 90 jours =============================
ws = wb.create_sheet("6. Plan 90 jours")
ws.sheet_view.showGridLines = False
r = title(ws, 1, "Votre plan en 90 jours", "Chapitre 30 — inscrivez O dans la colonne « Fait » au fur et à mesure.")
r = header(ws, r, ["Semaines", "Action", "Fait (O/N)", "Date", "Note"], [14, 66, 12, 14, 34])
PLAN = [
 ("1-2", "Remplir la feuille « 1. Entrées-sorties » depuis trois mois de relevés"),
 ("1-2", "Remplir la feuille « 2. Bilan » et calculer les trois ratios"),
 ("1-2", "Lister toutes les dettes avec leur taux et leur capital restant dû"),
 ("3-4", "Ouvrir le livret dédié aux dépenses irrégulières"),
 ("3-4", "Programmer le virement mensuel vers ce livret"),
 ("3-4", "Programmer le virement automatique d'épargne, le lendemain de la paie"),
 ("3-4", "Résilier les abonnements inutilisés repérés dans les relevés"),
 ("5-6", "Déterminer la cible d'épargne de précaution"),
 ("5-6", "Vérifier l'éligibilité au LEP et l'ouvrir le cas échéant"),
 ("5-6", "Transférer les liquidités excédentaires du compte courant vers les livrets"),
 ("5-6", "Attaquer la dette la plus coûteuse"),
 ("7-8", "Ouvrir un PEA chez un courtier à frais faibles et y verser 100 €"),
 ("7-8", "Ouvrir une assurance-vie sans frais sur versement, avec ETF disponibles"),
 ("7-8", "Faire l'audit de frais de tous les contrats existants"),
 ("7-8", "Vérifier si l'employeur propose un abondement, et à quelles conditions"),
 ("9-10", "Remplir la grille objectif / horizon / perte tolérée pour chaque poche"),
 ("9-10", "Choisir la part actions avec la feuille « 4. Allocation », en euros"),
 ("9-10", "Choisir un portefeuille modèle et l'adapter"),
 ("9-10", "Sélectionner les supports avec les sept critères, et écrire la liste"),
 ("11-12", "Mettre en place le versement programmé à date fixe"),
 ("11-12", "Effectuer le premier investissement selon l'allocation décidée"),
 ("11-12", "Rédiger et signer la règle de conduite en cas de baisse"),
 ("11-12", "Vérifier et mettre à jour les clauses bénéficiaires"),
 ("11-12", "Relire le contrat de prévoyance : carence, barème d'invalidité, exclusions"),
 ("11-12", "Si pacsé sans testament : prendre rendez-vous chez un notaire"),
 ("11-12", "Noter la date de la revue annuelle dans l'agenda"),
]
t0 = r
for sem, act in PLAN:
    ws.cell(r, 1, sem).font = Font(F, 10, bold=True, color=GREEN); ws.cell(r, 1).border = box
    c = ws.cell(r, 2, act); c.font = Font(F, 10, color=INK); c.border = box
    c.alignment = Alignment(wrap_text=True, vertical="center")
    for col in (3, 4, 5):
        c = ws.cell(r, col); c.border = box
        c.fill = PatternFill("solid", fgColor="FFFDF0")
        c.font = Font(F, 10, color="0000FF")
        c.alignment = Alignment(horizontal="center" if col == 3 else "left")
    r += 1
t1 = r - 1
r += 1
r = calc(ws, r, "Actions réalisées", f'=COUNTIF(C{t0}:C{t1},"O")', fmt="0", bold=False)
r = calc(ws, r, "Avancement", f'=COUNTIF(C{t0}:C{t1},"O")/{len(PLAN)}', fmt=PCT, big=True)
ws.freeze_panes = "A4"

wb.save("Argent-Maitrise-classeur.xlsx")
print("classeur écrit :", len(wb.sheetnames), "feuilles —", ", ".join(wb.sheetnames))
