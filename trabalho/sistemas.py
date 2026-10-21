"""Gera as seções 'ponto a ponto' (astrologia, casas, aspectos, Matriz, numerologia)."""
from html import escape as e
from conteudo_astro import PONTOS, CASAS, ASPECTOS
from conteudo_matriz_num import ARC, MATRIZ, PROPOSITOS, CHAKRAS, NUMEROS, INTENSIDADE

def badge(p):
    return "{%s}" % p

def head(id_, kicker, title, intro):
    return f'<section id="{id_}" class="chapter"><p class="kicker">{kicker}</p><h2>{title}</h2><p class="intro">{intro}</p>'

def astro():
    out = [head("s-astro", "Parte II · Astrologia", "Cada planeta e ponto, separado",
        "Toque em cada item para abrir. Posição do seu print {M}; minutos e aspectos calculados para 19/10/2006, 11:40 {C}.")]
    for p in PONTOS:
        out.append(f'''<details class="item"><summary><span class="glyph">{e(p["g"])}</span><span class="it-t"><strong>{e(p["nome"])}</strong><span class="it-s">{e(p["pos"])} · Casa {p["casa"]} · {e(p["est"])}</span></span>{badge(p["peso"])}</summary>
<div class="item-b"><p class="what">{e(p["o"])}</p><p>{e(p["txt"])} {p["src"]}</p>
<p class="asp"><strong>Aspectos:</strong> {e(p["asp"])}</p>
<div class="ls"><p><span class="lz">Em equilíbrio</span> {e(p["luz"])}</p><p><span class="sb">Em sombra</span> {e(p["sombra"])}</p></div></div></details>''')
    out.append("</section>")
    return "".join(out)

def casas():
    out = [head("s-casas", "Parte II · Astrologia", "As 12 casas, uma por uma",
        "Cúspides calculadas pelo sistema Placidus para 11:40 e um local estimado (~22,5°S, 48°O) que reproduz o seu Ascendente e Meio do Céu {C}. Os planetas dentro de cada casa são do print {M}. Regente = planeta que governa o signo da cúspide {T}.")]
    for n, area, cusp, reg, dentro, txt in CASAS:
        out.append(f'''<details class="item"><summary><span class="glyph num">{n}</span><span class="it-t"><strong>Casa {n} · {e(area)}</strong><span class="it-s">{e(cusp)} · regente {e(reg)}</span></span></summary>
<div class="item-b"><p><strong>Dentro:</strong> {e(dentro)}</p><p>{e(txt)}</p></div></details>''')
    out.append('<p class="tip"><strong>Padrão das casas:</strong> os regentes de <strong>9 das 12 casas</strong> estão na <strong>casa 10</strong>. As exceções são a 1ª e a 2ª (regidas por Saturno, na casa 8) e a 7ª (regida pela Lua, na casa 9). Quase toda área da sua vida "escoa" para a carreira e a vida pública. Casas sem planetas: 3, 4, 5, 6, 7 e 12 (algumas têm pontos menores). Vazia não quer dizer sem importância: a área é lida pelo regente. {C}{FORTE}</p></section>')
    return "".join(out)

def aspectos():
    out = [head("s-asp", "Parte II · Astrologia", "Todos os aspectos, do mais exato ao mais largo",
        "Aspecto = ângulo entre dois pontos. ☌ conjunção (fundem) · ☍ oposição (polarizam) · □ quadratura (atrito que move) · △ trígono (fluem) · ⚹ sextil (oportunidade) · ⚻ quincúncio (ajuste). Orbe = distância do ângulo exato; quanto menor, mais forte. {C}")]
    out.append('<div class="filters" role="group" aria-label="Filtrar aspectos"><button data-f="all" class="on">Todos</button><button data-f="tenso">Tensos</button><button data-f="fluido">Fluidos</button><button data-f="neutro">Conjunções</button><button data-f="menor">Ajustes</button></div><ul class="asplist">')
    for orb, a, s, b, txt, tipo in ASPECTOS:
        out.append(f'<li data-t="{tipo}"><span class="orb">{e(orb)}</span><span class="pair t-{tipo}">{e(a)} {s} {e(b)}</span><span class="atxt">{e(txt)}</span></li>')
    out.append("</ul></section>")
    return "".join(out)

def matriz():
    out = [head("s-matriz", "Parte III · Matriz do Destino", "Cada ponto da Matriz, separado",
        "Arcanos do seu diagrama {X}. O sentido de cada posição segue o método mais difundido (Natalia Ladini) {W}; posições não rotuladas no diagrama estão com (?).")]
    grupo = None
    for g, pos, arc, func, txt, src in MATRIZ:
        if g != grupo:
            out.append(f"<h3>{e(g)}</h3>"); grupo = g
        nome = ARC.get(arc, "") if isinstance(arc, int) else " · ".join(ARC[int(x)] for x in arc.split(" · "))
        out.append(f'''<details class="item"><summary><span class="glyph arc">{arc}</span><span class="it-t"><strong>{e(nome)}</strong><span class="it-s">{e(pos)}</span></span></summary>
<div class="item-b"><p class="what">{e(func)}</p><p>{e(txt)} {src}</p></div></details>''')
    out.append('<h3>Propósitos (calculados)</h3><div class="tw"><table><tr><th>Propósito</th><th>Conta</th><th>Arcano</th><th>Leitura</th></tr>')
    for n, conta, arc, txt in PROPOSITOS:
        out.append(f"<tr><td>{e(n)}</td><td>{e(conta)}</td><td><strong>{arc}</strong> {e(ARC[arc])}</td><td>{e(txt)}</td></tr>")
    out.append('</table></div><p class="why">Fórmulas padrão: Céu = topo + base; Terra = esquerda + direita; números acima de 22 são somados dígito a dígito {C}.</p>')
    out.append('<h3>Mapa de chakras (calculado)</h3><div class="tw"><table><tr><th>Chakra</th><th>Físico</th><th>Energia</th><th>Emoção</th></tr>')
    for n, f, en, em in CHAKRAS:
        out.append(f"<tr><td>{e(n)}</td><td>{f}</td><td>{en}</td><td>{em}</td></tr>")
    out.append('''</table></div><p>Destaques, como mapa simbólico de equilíbrio e <strong>não como avaliação de saúde</strong>: <strong>Coração (Anahata) = 19, Sol</strong>: o afeto se nutre de alegria e calor. <strong>Plexo solar = 22, Louco</strong>: a força pessoal pede liberdade, e o controle a sufoca. <strong>Garganta = 6</strong>: falar com amor, sem medo de desagradar. O total físico <strong>15 (Diabo)</strong> sugere atenção a excessos e apegos do corpo, como trabalhar sem parar. {C}{X}{ESPEC}</p>''')
    out.append('<h3>Linha de idades completa</h3><p>Cada idade tem um arcano. Os pontos grandes (0, 10, 20…) marcam a energia principal de cada fase. A interpretação está na <a href="#c10">Linha do tempo</a>. {X}</p></section>')
    return "".join(out)

def glyph(v):
    if len(v) <= 5: return v
    t = v.split()[0]
    return t if t.replace("/", "").isdigit() else "✦"

def numerologia():
    out = [head("s-num", "Parte IV · Numerologia", "Cada número, separado",
        "Método pitagórico. Os números do app {N} foram conferidos pelo cálculo com o seu nome completo e a sua data {C}: Expressão 6, Alma 11 e Personalidade 4 batem.")]
    for nome, val, conta, o, txt, peso, src in NUMEROS:
        out.append(f'''<details class="item"><summary><span class="glyph num">{e(glyph(val))}</span><span class="it-t"><strong>{e(nome)}: {e(val)}</strong><span class="it-s">{e(conta)}</span></span>{badge(peso)}</summary>
<div class="item-b"><p class="what">{e(o)}</p><p>{e(txt)} {src}</p></div></details>''')
    bars = "".join(f'<div class="bar-r"><span>{k}</span><i style="width:{v*18}%"></i><b>{v}</b></div>' for k, v in INTENSIDADE.items())
    out.append(f'<h3>Quantas letras de cada número tem o seu nome</h3><div class="bars">{bars}</div><p class="why">0 letras = Lição cármica (2). 5 letras = forças mais disponíveis (1, 3, 6, 9). {{C}}</p></section>')
    return "".join(out)

def sistemas():
    return astro() + casas() + aspectos() + matriz() + numerologia()
