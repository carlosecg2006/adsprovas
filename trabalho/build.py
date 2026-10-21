"""Monta quem-eu-sou.html a partir de capitulos.html + etapa*.md."""
import re, html, pathlib, markdown

D = pathlib.Path(__file__).parent
OUT = D.parent / "quem-eu-sou.html"

CHIPS = {
    "M": ("Mapa", "ap-a"), "X": ("Matriz", "ap-c"), "N": ("Numerologia", "ap-e"),
    "A": ("Análise", "ap-d"), "W": ("Web", "ap-g"), "T": ("Tradição", "ap-g"),
    "O": ("Fora do esoterismo", "ap-g"), "C": ("Calculado", "ap-h"),
}
BADGES = {
    "FORTE": ("FORTE", "b-forte"), "MEDIO": ("MÉDIO", "b-medio"), "FRACO": ("FRACO", "b-fraco"),
    "SOLIDA": ("SÓLIDA", "b-solida"), "ESPEC": ("ESPECULATIVA", "b-espec"),
}

def chips(s):
    for k, (lbl, href) in CHIPS.items():
        s = s.replace("{%s}" % k, f'<a class="src" href="#{href}">{lbl}</a>')
    for k, (lbl, cls) in BADGES.items():
        s = s.replace("{%s}" % k, f'<span class="badge {cls}">{lbl}</span>')
    return s

def md(path):
    t = (D / path).read_text()
    t = re.sub(r"^# .*\n", "", t, count=1)  # o título vira o <summary>
    h = markdown.markdown(t, extensions=["tables"])
    # fontes entre colchetes viram chips clicáveis
    for lbl, href in [("Mapa", "ap-a"), ("Matriz", "ap-c"), ("Numerologia", "ap-e"), ("Análise", "ap-d"), ("Calc", "ap-h")]:
        h = h.replace(f"[{lbl}]", f'<a class="src" href="#{href}">{lbl}</a>')
    h = re.sub(r"\[(Web|Tradição|Fora do esoterismo)([^\]]*)\]",
               lambda m: f'<a class="src" href="#ap-g">{m.group(1)}{html.escape(m.group(2))}</a>', h)
    for w, cls in [("FORTE", "b-forte"), ("MÉDIO", "b-medio"), ("FRACO", "b-fraco"),
                   ("SÓLIDA", "b-solida"), ("ESPECULATIVA", "b-espec")]:
        h = h.replace(f"<strong>{w}</strong>", f'<span class="badge {cls}">{w}</span>')
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return h

APPX = [
    ("ap-a", "A. Transcrição completa dos dados (Etapa 1)", "etapa1.md"),
    ("ap-b", "B. Astrologia detalhada (Etapa 2)", "etapa2.md"),
    ("ap-c", "C. Matriz do Destino detalhada (Etapa 3)", "etapa3.md"),
    ("ap-d", "D. Auditoria da análise anterior (Etapa 4)", "etapa4.md"),
    ("ap-e", "E. Numerologia detalhada (Etapa 5)", "etapa5.md"),
    ("ap-f", "F. Cruzamento dos sistemas (Etapas 6, 7 e 8)", ["etapa6.md", "etapa7.md", "etapa8.md"]),
    ("ap-g", "G. Todas as fontes e checagem de cobertura", "fontes.md"),
    ("ap-h", "H. Cálculos feitos (método e conferência)", "calculos.md"),
]

def appendix():
    out = []
    for aid, title, src in APPX:
        srcs = src if isinstance(src, list) else [src]
        body = "".join(
            (f"<h2 class='sub'>{html.escape((D / s).read_text().splitlines()[0][2:])}</h2>" if len(srcs) > 1 else "") + md(s)
            for s in srcs)
        out.append(f'<details class="appx" id="{aid}"><summary>{title}</summary><div class="appx-body">{body}</div></details>')
    return "\n".join(out)

NAV = [("c0", "Abertura"), ("c1", "Essência"), ("c2", "Facetas"), ("c3", "Mente"), ("c4", "Emoções"),
       ("c5", "Relações"), ("c6", "Família"), ("c7", "Vocação"), ("c8", "Sombras"),
       ("c9", "Espiritualidade"), ("s-astro", "Planetas"), ("s-casas", "Casas"), ("s-asp", "Aspectos"),
       ("s-matriz", "Matriz"), ("s-num", "Numerologia"), ("c10", "Linha do tempo"), ("c11", "Guia prático"),
       ("apx", "Apêndice")]

from sistemas import sistemas

tpl = (D / "template.html").read_text()
page = (tpl.replace("%%NAV%%", "".join(f'<a href="#{i}">{t}</a>' for i, t in NAV))
           .replace("%%CHAPTERS%%", chips((D / "capitulos.html").read_text().replace("<!--SISTEMAS-->", sistemas())))
           .replace("%%APPENDIX%%", appendix()))
OUT.write_text(page)
print(OUT, len(page))
