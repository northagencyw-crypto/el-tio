"""Genera las guias pilar por rubro (eje «La ventaja es hoy») en /guias/como-usar-ia-*/.
Uso: python generador/guias_pilar.py
Contenido en generador/guias_pilar_datos.py. Solo datos con fuente; ejemplos marcados como ejemplo."""
import html, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guias_pilar_datos import GUIAS, FUENTES, CIUDADES

FECHA = "2026-11-06"
FECHA_TXT = "6 de noviembre de 2026"
WA = "525568976898"
ICONO = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' "
         "fill='%2304070B'/%3E%3Ctext x='16' y='23' font-family='monospace' font-size='19' font-weight='700' fill='%237FC9F2' "
         "text-anchor='middle'%3ET%3C/text%3E%3C/svg%3E")

PIE = open(os.path.join(RAIZ, "guias", "crm-inmobiliaria-seguimiento-leads", "index.html"), encoding="utf-8").read()
PIE = PIE[PIE.index('<footer class="pie">'):]


def limpio(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def ventana(v):
    if v["tipo"] == "chat":
        cuerpo = "".join(f'<span class="{q}">{t}</span>' for q, t in v["lineas"])
        cuerpo = f'<div class="cuerpo chat">{cuerpo}</div>'
    else:
        filas = "".join(f"<li><b>{a}</b><span>{b}</span><em>{c}</em></li>" for a, b, c in v["filas"])
        cuerpo = f'<div class="cuerpo"><ul class="filas">{filas}</ul></div>'
    return (f'<figure class="ventana" role="figure" aria-label="Simulación de ejemplo: {html.escape(v["titulo"])}">'
            f'<div class="barra"><i></i><i></i><i></i><span>{v["titulo"]}</span></div>{cuerpo}'
            f'<figcaption>Simulación de ejemplo. Nombres, mensajes y cifras inventados para mostrar la idea.</figcaption></figure>')


def pagina(g):
    url = g.get("url", f"https://eltio.net/guias/{g['slug']}/")
    orden = []

    def refs(txt):
        def r(m):
            k = m.group(1)
            if k not in orden:
                orden.append(k)
            n = orden.index(k) + 1
            return f'<a class="ref" href="#f{n}">[{n}]</a>'
        return re.sub(r"\{\{(\w+)\}\}", r, txt)

    cuerpo = []
    indice = []
    for s in g["secciones"]:
        indice.append(f'<li><a href="#{s["id"]}">{s["h2"]}</a></li>')
        cuerpo.append(f'<h2 id="{s["id"]}">{s["h2"]}</h2>')
        for b in s["bloques"]:
            if isinstance(b, dict):
                if "h3" in b:
                    cuerpo.append(f"<h3>{b['h3']}</h3>")
                elif "lista" in b:
                    cuerpo.append('<ul>' + "".join(f"<li>{refs(x)}</li>" for x in b["lista"]) + "</ul>")
                elif "ol" in b:
                    cuerpo.append('<ol class="lista">' + "".join(f"<li>{refs(x)}</li>" for x in b["ol"]) + "</ol>")
                elif "aviso" in b:
                    cuerpo.append(f'<div class="aviso">{refs(b["aviso"])}</div>')
                elif "tipo" in b:
                    cuerpo.append(ventana(b))
            else:
                cuerpo.append(f"<p>{refs(b)}</p>")
    indice.append('<li><a href="#preguntas">Preguntas frecuentes</a></li>')
    cuerpo.append('<h2 id="preguntas">Preguntas frecuentes</h2>')
    for q, a in g["faq"]:
        cuerpo.append(f"<h3>{q}</h3><p>{refs(a)}</p>")
    indice.append('<li><a href="#empezar">Por dónde empezar</a></li>')

    fuentes = "".join(f'<li id="f{i+1}">{g.get("fuentes_txt", {}).get(k, FUENTES[k][0])} <a href="{FUENTES[k][1]}">{FUENTES[k][1].split("//")[1].rstrip("/")}</a></li>'
                      for i, k in enumerate(orden))
    ciudades = [c for c in g["ciudades"] if os.path.isdir(os.path.join(RAIZ, "negocios", c, g["rubro"]))]
    rel = [f'<li><a href="/{g["rubro"]}/">{g["rubro_nombre"]}</a>: la página del rubro</li>']
    rel += [f'<li><a href="/negocios/{c}/{g["rubro"]}/">{g["rubro_nombre"]} en {CIUDADES[c]}</a></li>' for c in ciudades]
    rel += [f'<li><a href="{u}">{t}</a></li>' for u, t in g.get("guias_rel", [])]
    rel += ['<li><a href="/indice/">Índice El Tío</a>: cuántos negocios de tu ciudad no tienen web</li>',
            '<li><a href="/cronometro/">El Cronómetro del Tío</a>: calcula cuántas ventas esperan respuesta en tus mensajes</li>',
            f'<li><a data-cta="audit" href="https://app.eltio.net/auditoria/{g["rubro"]}">Audit gratis de tu negocio</a></li>']

    if "rel" in g:
        rel = g["rel"]
    wa_txt = urllib_quote(f"Hola! Leí la guía de IA para {g['wa']} y quiero el Audit de mi negocio.")
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": limpio(q),
                              "acceptedAnswer": {"@type": "Answer", "text": limpio(re.sub(r"\{\{\w+\}\}", "", a))}} for q, a in g["faq"]]}
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"],
              "inLanguage": "es-MX", "datePublished": FECHA, "dateModified": FECHA,
              "image": f"https://eltio.net/assets/og-{g['rubro']}.jpg",
              "author": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net"},
              "publisher": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net"},
              "mainEntityOfPage": url, "about": {"@type": "Thing", "name": g["about"]},
              "spatialCoverage": {"@type": "Country", "name": "México"}}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "El Tío", "item": "https://eltio.net/"},
        {"@type": "ListItem", "position": 2, "name": "Guías", "item": "https://eltio.net/guias/"},
        {"@type": "ListItem", "position": 3, "name": g["h1"], "item": url}]}
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>\n' for x in (art_ld, bc_ld, faq_ld))
    img = g["img"]
    w, h = img["wh"]
    big = "1200w" if os.path.exists(os.path.join(RAIZ, "assets", img["src"] + "-1200.webp")) else None
    srcset = f'/assets/{img["src"]}-480.webp 480w, /assets/{img["src"]}-768.webp 768w, /assets/{img["src"]}.webp {w}w'
    e = html.escape
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(g['title'])}</title>
<meta name="description" content="{e(g['desc'])}">
<link rel="canonical" href="{url}">{g.get("hreflang", "")}
<meta name="theme-color" content="#04070B">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="El Tío">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(g['h1'])}">
<meta property="og:description" content="{e(g['desc'])}">
<meta property="og:image" content="https://eltio.net/assets/og-{g['rubro']}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ICONO}">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-var.woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/guias/guias.css">
{ld}<script src="/medicion.js" defer></script>
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
  <a class="marca" href="https://eltio.net/">EL TIO<span>.</span></a>
  <p class="estado"><i></i>EN LÍNEA</p>
</header>
<main id="contenido" class="guia">
  <nav class="migas" aria-label="Ruta"><a href="https://eltio.net">El Tío</a> / <a href="https://eltio.net/guias/">Guías</a> / {g['rubro_nombre']}</nav>
  <article>
    <h1>{g['h1']}</h1>
    <p class="bajada">{g['bajada']}</p>
    <p class="fecha">Actualizada el {FECHA_TXT}</p>
    <figure class="portada"><img src="/assets/{img['src']}.webp" srcset="{srcset}" sizes="(max-width: 760px) 100vw, 720px" alt="{e(img['alt'])}" width="{w}" height="{h}" fetchpriority="high"></figure>
    <nav class="indice" aria-label="En esta guía">
      <p>En esta guía</p>
      <ol>{''.join(indice)}</ol>
    </nav>
    {chr(10).join('    ' + c for c in cuerpo)}
    <section class="cierre" id="empezar">
      <h2>Por dónde empezar</h2>
      <p>{g['cierre']}</p>
      <p>El Audit es gratis: un cuestionario de 15 a 25 minutos sobre cómo trabaja hoy tu negocio y, en 24 a 48 horas hábiles, el mapa de qué ventaja conviene tomar primero. Si lo que más te sirve no es algo que hagamos nosotros, te lo decimos.</p>
      <p><strong>No pierdas la ventaja, es hoy. Habla con El Tío.</strong></p>
      <div class="acciones">
        <a class="btn" data-cta="audit" href="https://app.eltio.net/auditoria/{g['rubro']}">Hacer el Audit gratis</a>
        <a class="enlace" data-cta="whatsapp" href="https://wa.me/{WA}?text={wa_txt}">Escribir por WhatsApp</a>
      </div>
    </section>
    <nav class="relacionado" aria-label="Para seguir">
      <p>Para seguir</p>
      <ul>{''.join(rel)}</ul>
    </nav>
    <section class="fuentes" aria-labelledby="fuentes-t">
      <h2 id="fuentes-t">Fuentes</h2>
      <ol>{fuentes}</ol>
    </section>
  </article>
</main>
{PIE}"""


def urllib_quote(s):
    from urllib.parse import quote
    return quote(s, safe="")


EN_UI = [
    ('<html lang="es-MX">', '<html lang="en">'), ('content="es_MX"', 'content="en_US"'), ('"es-MX"', '"en"'),
    ("Saltar al contenido", "Skip to content"), ("EN LÍNEA", "ONLINE"), ('aria-label="Ruta"', 'aria-label="Breadcrumb"'),
    ('<a href="https://eltio.net">El Tío</a> / <a href="https://eltio.net/guias/">Guías</a>', '<a href="https://eltio.net/en/">El Tío</a> / <a href="https://eltio.net/en/guides/">Guides</a>'),
    ('"name": "Guías",\n   "item": "https://eltio.net/guias/"', '"name": "Guides",\n   "item": "https://eltio.net/en/guides/"'),
    ("Actualizada el " + FECHA_TXT, "Updated November 6, 2026"), ('aria-label="En esta guía"', 'aria-label="In this guide"'),
    ("<p>En esta guía</p>", "<p>In this guide</p>"), ("Preguntas frecuentes", "Frequently asked questions"),
    ("Por dónde empezar", "Where to start"), ("Simulación de ejemplo: ", "Example simulation: "),
    ("Simulación de ejemplo. Nombres, mensajes y cifras inventados para mostrar la idea.", "Example simulation. Names, messages and figures are made up to show the idea."),
    ("El Audit es gratis: un cuestionario de 15 a 25 minutos sobre cómo trabaja hoy tu negocio y, en 24 a 48 horas hábiles, el mapa de qué ventaja conviene tomar primero. Si lo que más te sirve no es algo que hagamos nosotros, te lo decimos.",
     "The Audit is free: a 15 to 25 minute questionnaire about how your business works today and, within 24 to 48 business hours, a map of which advantage to take first. If what would help you most isn't something we do, we'll tell you."),
    ("No pierdas la ventaja, es hoy. Habla con El Tío.", "Don't lose the advantage. It's today. Talk to El Tío."),
    (">Hacer el Audit gratis</a>", ">Take the free Audit</a><small class=\"nota-idioma\">The Audit is only available in Spanish for now. If you'd rather talk in your language, message us on WhatsApp or at hola@eltio.net.</small>"),
    (">Escribir por WhatsApp</a>", ">Message us on WhatsApp</a>"), ('aria-label="Para seguir"', 'aria-label="Keep reading"'),
    ("<p>Para seguir</p>", "<p>Keep reading</p>"), (">Fuentes</h2>", ">Sources</h2>"),
]


def en_pagina(g):
    out = pagina(g)
    for a, b in EN_UI:
        out = out.replace(a, b)
    pie = open(os.path.join(RAIZ, "en", "guides", "direct-bookings-whatsapp-hotels", "index.html"), encoding="utf-8").read()
    out = out[:out.index('<footer class="pie">')] + pie[pie.index('<footer class="pie">'):]
    return out


if __name__ == "__main__":
    from guias_pilar_en import GUIAS_EN
    for g in GUIAS_EN:
        d = os.path.join(RAIZ, *g["dir"].split("/"))
        os.makedirs(d, exist_ok=True)
        out = en_pagina(g)
        assert "—" not in out and "–" not in out
        open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(out)
        print(g["dir"], len(limpio(re.search(r"<article>.*?<section class=\"fuentes\"", out, re.S).group(0)).split()), "words")
    for g in GUIAS:
        d = os.path.join(RAIZ, "guias", g["slug"])
        os.makedirs(d, exist_ok=True)
        out = pagina(g)
        assert "—" not in out and "–" not in out, g["slug"]
        open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(out)
        main = re.search(r"<article>.*?<section class=\"fuentes\"", out, re.S).group(0)
        print(g["slug"], len(limpio(main).split()), "palabras")
