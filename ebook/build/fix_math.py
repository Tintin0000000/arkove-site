import re, pathlib

p = pathlib.Path("content/07-annexes.md")
t = p.read_text(encoding="utf-8")

blocks = {
    r"$$VF = V_0 \times (1 + r)^n$$":
        "::: {.formule}\nVF = V₀ × (1 + r)ⁿ\n:::",
    r"$$VF = P \times \frac{(1 + i)^n - 1}{i}$$":
        "::: {.formule}\nVF = P × [ (1 + i)ⁿ − 1 ] ÷ i\n:::",
    r"$$r_{réel} = \frac{1 + r_{nominal}}{1 + inflation} - 1$$":
        "::: {.formule}\nRendement réel = [ (1 + rendement nominal) ÷ (1 + inflation) ] − 1\n:::",
    r"$$M = \frac{C \times i}{1 - (1 + i)^{-n}}$$":
        "::: {.formule}\nM = (C × i) ÷ [ 1 − (1 + i)⁻ⁿ ]\n:::",
    r"$$Mensualité_{max} \approx 0{,}35 \times revenus\ nets\ mensuels - crédits\ en\ cours$$":
        "::: {.formule}\nMensualité maximale ≈ (0,35 × revenus nets mensuels) − crédits en cours\n:::",
    r"$$Perte_{crise} \approx part\ actions \times 45\,\%$$":
        "::: {.formule}\nPerte envisageable en crise ≈ part actions × 45 %\n:::",
}
for k, v in blocks.items():
    if k not in t:
        raise SystemExit("BLOC NON TROUVE: " + k)
    t = t.replace(k, v)

inline = {
    "$V_0$": "**V₀**", "$r$": "**r**", "$n$": "**n**", "$P$": "**P**",
    "$i$": "**i**", "$C$": "**C**",
}
for k, v in inline.items():
    t = t.replace(k, v)

if "$" in t:
    raise SystemExit("MATH RESTANT: " + repr([l for l in t.split("\n") if "$" in l]))

p.write_text(t, encoding="utf-8")
print("formules converties, aucun math LaTeX restant")
