"""SEO programático de eltio.net: una página por ciudad y rubro.

Uso: python generador/pseo/build.py            (desde la raíz del repo)
Genera /negocios/, /negocios/{ciudad}/, /negocios/{ciudad}/{rubro}/ y sitemap-negocios.xml.
Para escalar: sumar ciudades en datos.py. Nada más.
"""
import hashlib, html, json, os, re, sys, urllib.parse
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from datos import CIUDADES, RUBROS, PAISES, PERFILES, VENTAJAS, VENTAJA_TITULOS
from datos_latam import LOCAL, LOCAL_RUBRO, FRONTERA_LATAM

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "https://eltio.net"
HOY = date.today().isoformat()
WA = "525568976898"
e = html.escape


def semilla(*partes):
    return int(hashlib.md5("|".join(partes).encode()).hexdigest()[:8], 16)


def rota(lista, n, s):
    """Elige n elementos en un orden propio de cada página (estable entre builds)."""
    return sorted(lista, key=lambda x: semilla(str(s), str(x)))[:n]


def wa(texto):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(texto)


def ciudad(c):
    slug, nombre, estado, pais, perfil, region, nota, eltio = c
    if not eltio and os.path.exists(os.path.join(RAIZ, "ciudades", slug, "index.html")):
        eltio = slug
    return dict(slug=slug, nombre=nombre, estado=estado, pais=pais, perfil=perfil, region=region, nota=nota, eltio=eltio)


CABECERA = """<header class="cabecera">
  <a class="marca" href="https://eltio.net/">EL TIO<span>.</span></a>
  <p class="estado"><i></i>EN LÍNEA</p>
</header>"""

PIE = """<footer class="pie">
  <div class="inner">
    <div class="pie-cols">
      <div><p>Servicios</p><ul>
        <li><a href="/paginas-web/">Páginas web</a></li>
        <li><a href="/servicios/agente-whatsapp-instagram/">Agente de WhatsApp e Instagram</a></li>
        <li><a href="/servicios/crm-y-seguimiento/">CRM y seguimiento</a></li>
        <li><a href="/posicionamiento-en-ia/">Posicionamiento en IA</a></li>
      </ul></div>
      <div><p>Rubros</p><ul>
        <li><a href="/gastronomia/">Gastronomía</a></li>
        <li><a href="/hospitality/">Hospitality</a></li>
        <li><a href="/real-estate/">Real estate</a></li>
        <li><a href="/fitness/">Fitness</a></li>
        <li><a href="/eventos/">Eventos</a></li>
        <li><a href="/artistas/">Artistas</a></li>
        <li><a href="/distribucion/">Distribución</a></li>
      </ul></div>
      <div><p>El Tío</p><ul>
        <li><a href="/negocios/">Ciudades y rubros</a></li>
        <li><a href="/como-trabajamos/">Cómo trabajamos</a></li>
        <li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li>
        <li><a href="/guias/">Guías</a></li>
        <li><a href="/ventaja/">Calculadora de ventaja</a></li>
        <li><a href="/referidos/">Programa de referidos</a></li>
        <li><a href="/contacto/">Contacto</a></li>
      </ul></div>
    </div>
    <div class="pie-base">
      <p>El Tío · Inteligencia artificial aplicada a empresas</p>
      <p><a href="mailto:hola@eltio.net">hola@eltio.net</a> · <a href="https://wa.me/525568976898?text=Hola%21%20Quiero%20hablar%20con%20El%20T%C3%ADo%20sobre%20inteligencia%20artificial%20para%20mi%20empresa." data-cta="whatsapp">WhatsApp +52 55 6897 6898</a></p>
    </div>
  </div>
</footer>"""


def documento(ruta, titulo, desc, lang, og, ld, cuerpo):
    url = BASE + ruta
    lds = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>' for x in ld)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)} · El Tío</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="{lang.replace('-', '_')}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{BASE}/assets/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-var.woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/guias/guias.css">
{lds}
<script src="/medicion.js" defer></script>
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{CABECERA}
<main id="contenido" class="guia">
{cuerpo}
</main>
{PIE}
</body>
</html>
"""


def migas(items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}
    vis = " / ".join(f'<a href="{u}">{e(n)}</a>' for n, u in items[:-1]) + " / " + e(items[-1][0])
    return ld, f'  <nav class="migas" aria-label="Ruta">{vis}</nav>'


def cercanas(c, todas, n=4):
    misma = [x for x in todas if x["region"] == c["region"] and x["slug"] != c["slug"] and x["pais"] == c["pais"]]
    otras = [x for x in todas if x["perfil"] == c["perfil"] and x["slug"] != c["slug"] and x not in misma and x["pais"] == c["pais"]]
    return (misma + otras)[:n]


def perfil(c):
    if c["pais"] == "mx":
        return PERFILES[c["perfil"]]
    base = FRONTERA_LATAM if c["perfil"] == "frontera" else PERFILES[c["perfil"]]
    nom = PAISES[c["pais"]]["nombre"]
    return {k: v.replace("en México", "en " + nom).replace("cada colonia", "cada barrio") for k, v in base.items()}


def pagina(c, rk, todas, guias):
    r, p, pais = RUBROS[rk], perfil(c), PAISES[c["pais"]]
    s = semilla(c["slug"], rk)
    nom, plural = c["nombre"], r["plural"]
    ruta = f"/negocios/{c['slug']}/{rk}/"
    titulo = f"Página web y chatbot para {plural} en {nom}"
    desc = f"Qué problemas tienen hoy los {plural} en {nom}, cómo se resuelven con una página web propia y un chatbot de WhatsApp, y un Audit gratis para saber por dónde empezar."
    probs = rota(r["problemas"], 4, s)
    faqs = rota(r["faq"], 3, s // 3)
    faqs = faqs + [
        (f"¿Atienden {plural} en {nom}?", f"Sí. Todo el trabajo es en línea, así que da igual si estás en {nom} o en cualquier otra ciudad de {c['estado'] if c['estado'] != nom else pais['nombre']}. Empiezas con el Audit gratis y seguimos por chat."),
        ("¿Qué es el Audit gratis?", f"Un cuestionario de 15 a 25 minutos sobre cómo trabaja hoy {r['uno']}. En 24 a 48 horas hábiles recibes un mapa con lo que conviene ordenar primero. Si una página o un chatbot no es lo que más te sirve, te lo decimos."),
        ("¿Y mis datos y los de mis clientes?", f"Son tuyos. En {pais['nombre']} el tratamiento de datos personales lo rige {pais['ley']}, y lo central es avisar a cada persona qué datos guardas y para qué."),
    ]
    audit = f"https://app.eltio.net/auditoria/{rk}"
    wtxt = wa(f"Hola! Tengo {('un negocio de ' + r['nombre'].lower()) if rk != 'artistas' else 'un proyecto artístico'} en {nom} y quiero el Audit gratis.")
    vecinas = cercanas(c, todas)
    otros = [k for k in RUBROS if k != rk]

    l_migas, h_migas = migas([("El Tío", "/"), ("Ciudades y rubros", "/negocios/"), (nom, f"/negocios/{c['slug']}/"), (r["nombre"], ruta)])
    l_serv = {"@context": "https://schema.org", "@type": "Service", "name": titulo, "description": desc,
              "serviceType": "Página web y chatbot de WhatsApp", "url": BASE + ruta,
              "provider": {"@type": "Organization", "name": "El Tío", "url": BASE},
              "areaServed": {"@type": "City", "name": nom, "containedInPlace": {"@type": "AdministrativeArea", "name": c["estado"]}},
              "audience": {"@type": "BusinessAudience", "audienceType": plural}}
    l_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

    h = [h_migas, "  <article>", f"    <h1>{e(titulo)}</h1>",
         f'    <p class="bajada">{e(c["nota"])} Esta página reúne los problemas que más se repiten en {e(plural)} y cómo se ordenan con una página web propia y un chatbot de WhatsApp e Instagram.</p>',
         f'    <p class="fecha">Actualizada el {HOY[8:10]}/{HOY[5:7]}/{HOY[:4]}</p>',
         '    <h2 id="problemas">Lo que más se repite</h2>']
    for t, d in probs:
        h += [f"    <h3>{e(t)}</h3>", f"    <p>{e(d)}</p>"]
    h += [f'    <h2 id="ciudad">Qué cambia en {e(nom)}</h2>',
          f"    <p>{e(p['general'])}</p>",
          f"    <p>{e(p[rk])}</p>",
          *([f"    <p>{e(LOCAL_RUBRO[rk].format(nom=nom, zonas=LOCAL[c['slug']][0], motor=LOCAL[c['slug']][1]))}</p>"] if c["slug"] in LOCAL else []),
          f'    <div class="aviso">Una prueba simple: busca en Google «{e(plural.split(" y ")[0])} en {e(nom)}» desde tu teléfono y mira si apareces, qué se ve de tu negocio y cuánto tardarías en contestar si alguien te escribe ahora.</div>',
          f'    <h2 id="ventaja">Tu ventaja en {e(r["nombre"].lower() if rk not in ("hospitality", "real-estate") else r["nombre"])} en {e(nom)}</h2>',
          f"    <p>La IA ya es una ventaja frente al mercado y la ventana es hoy: quien no da un paso ahora, mañana tiene que dar diez para llegar al mismo lugar. Estas son las cinco que más pesan en {e(plural)}.</p>",
          '    <ol class="lista">']
    h += [f"      <li><strong>{e(t)}.</strong> {e(x)}</li>" for t, x in zip(VENTAJA_TITULOS, VENTAJAS[rk])]
    h += ["    </ol>", f'    <p><a data-cta="ventaja" href="{e(wtxt)}">No pierdas la ventaja, es hoy. Habla con El Tío.</a></p>',
          '    <h2 id="como">Cómo se resuelve</h2>', '    <ol class="lista">']
    h += [f"      <li>{e(x)}</li>" for x in [r["pasos"][0]] + rota(r["pasos"][1:], 3, s)]
    h += ["    </ol>",
          f"    <p>La página sale en 8 idiomas, con dominio propio y preparada para aparecer en Google y en asistentes de IA como ChatGPT. Lo que no se usa no se instala: el orden lo define el Audit.</p>",
          '    <h2 id="preguntas">Preguntas frecuentes</h2>']
    for q, a in faqs:
        h += [f"    <h3>{e(q)}</h3>", f"    <p>{e(a)}</p>"]
    h += ['    <section class="cierre" id="empezar">', "      <h2>Por dónde empezar</h2>",
          f"      <p>El Audit es gratis: un cuestionario de 15 a 25 minutos sobre {e(r['uno'])} y, en 24 a 48 horas hábiles, el mapa de lo que conviene hacer primero. Todo sigue por chat.</p>",
          '      <div class="acciones">',
          f'        <a class="btn" data-cta="audit" href="{audit}">Hacer el Audit gratis</a>',
          f'        <a class="enlace" data-cta="whatsapp" href="{e(wtxt)}">Escribir por WhatsApp</a>',
          "      </div>", "    </section>",
          '    <nav class="relacionado" aria-label="Para seguir">', "      <p>Para seguir</p>", "      <ul>",
          f'        <li><a href="/{rk}/">{e(r["nombre"])}</a>: la página del rubro</li>',
          '        <li><a href="/paginas-web/">Páginas web de El Tío</a></li>']
    if c["eltio"]:
        h.append(f'        <li><a href="/ciudades/{c["eltio"]}/">El Tío en {e(nom if c["eltio"] != "tulum-riviera-maya" else "Tulum y Riviera Maya")}</a></li>')
    for g, t in guias.get(rk, []):
        if c["pais"] != "mx" and "mexico" in g:
            continue
        h.append(f'        <li><a href="/guias/{g}/">{e(t)}</a></li>')
    for v in vecinas:
        h.append(f'        <li><a href="/negocios/{v["slug"]}/{rk}/">{e(plural.capitalize())} en {e(v["nombre"])}</a></li>')
    for k in rota(otros, 3, s):
        h.append(f'        <li><a href="/negocios/{c["slug"]}/{k}/">{e(RUBROS[k]["plural"].capitalize())} en {e(nom)}</a></li>')
    h += [f'        <li><a href="/negocios/{c["slug"]}/">Todos los rubros en {e(nom)}</a></li>', "      </ul>", "    </nav>", "  </article>"]
    return ruta, documento(ruta, titulo, desc, pais["lang"], f"og-{rk}.jpg", [l_serv, l_faq, l_migas], "\n".join(h))


def hub_ciudad(c, todas):
    pais = PAISES[c["pais"]]
    ruta = f"/negocios/{c['slug']}/"
    titulo = f"Páginas web y chatbots para negocios en {c['nombre']}"
    desc = f"Página web propia y chatbot de WhatsApp para restaurantes, hoteles, inmobiliarias, gimnasios, eventos, artistas y distribuidoras de {c['nombre']}. Audit gratis."
    l_m, h_m = migas([("El Tío", "/"), ("Ciudades y rubros", "/negocios/"), (c["nombre"], ruta)])
    h = [h_m, "  <article>", f"    <h1>{e(titulo)}</h1>", f'    <p class="bajada">{e(c["nota"])} {e(perfil(c)["general"])}</p>',
         '    <h2>Elige tu rubro</h2>', '    <ul>']
    for k, r in RUBROS.items():
        h.append(f'      <li><a href="/negocios/{c["slug"]}/{k}/"><strong>{e(r["plural"].capitalize())}</strong></a>: {e(perfil(c)[k])}</li>')
    h += ["    </ul>", '    <section class="cierre"><h2>Por dónde empezar</h2><p>El Audit es gratis y en 24 a 48 horas hábiles tienes el mapa de lo que conviene hacer primero.</p>',
          '      <div class="acciones"><a class="btn" data-cta="audit" href="https://app.eltio.net/">Hacer el Audit gratis</a>',
          f'      <a class="enlace" data-cta="whatsapp" href="{e(wa("Hola! Tengo un negocio en " + c["nombre"] + " y quiero el Audit gratis."))}">Escribir por WhatsApp</a></div></section>',
          '    <nav class="relacionado" aria-label="Para seguir"><p>Ciudades cercanas</p><ul>']
    h += [f'      <li><a href="/negocios/{v["slug"]}/">{e(v["nombre"])}</a></li>' for v in cercanas(c, todas, 6)]
    h += ["    </ul></nav>"]
    if c["eltio"]:
        h.append(f'    <p class="relacionado"><a href="/ciudades/{c["eltio"]}/">El Tío en {e(c["nombre"] if c["eltio"] != "tulum-riviera-maya" else "Tulum y Riviera Maya")}</a></p>')
    h += ["  </article>"]
    return ruta, documento(ruta, titulo, desc, pais["lang"], "og-portada.jpg", [l_m], "\n".join(h))


def hub_indice(todas):
    ruta = "/negocios/"
    titulo = "Páginas web y chatbots por ciudad y rubro"
    desc = "El Tío en cada ciudad: página web propia y chatbot de WhatsApp por rubro, con los problemas típicos de cada negocio y un Audit gratis."
    l_m, h_m = migas([("El Tío", "/"), ("Ciudades y rubros", ruta)])
    h = [h_m, "  <article>", f"    <h1>{e(titulo)}</h1>",
         '    <p class="bajada">Cada página explica lo que más se repite en un rubro, qué cambia en esa ciudad y cómo se ordena con una página web propia y un chatbot. Elige tu ciudad.</p>']
    for pk, pv in PAISES.items():
        cs = [x for x in todas if x["pais"] == pk]
        if not cs:
            continue
        h += [f"    <h2>{e(pv['nombre'])}</h2>", "    <ul>"] + [f'      <li><a href="/negocios/{x["slug"]}/">{e(x["nombre"])}</a>, {e(x["estado"])}</li>' for x in sorted(cs, key=lambda x: x["nombre"])] + ["    </ul>"]
    h.append("  </article>")
    return ruta, documento(ruta, titulo, desc, "es-MX", "og-portada.jpg", [l_m], "\n".join(h))


def guias_por_rubro():
    m = {"gastronomia": ["chatbot-whatsapp-restaurantes-ciudad-de-mexico"], "hospitality": ["reservas-directas-whatsapp-hoteles"],
         "real-estate": ["crm-inmobiliaria-seguimiento-leads"], "fitness": ["retencion-socios-gimnasio-reservas-clases"],
         "distribucion": ["pedidos-whatsapp-cotizaciones-distribuidoras"]}
    out = {}
    for k, gs in m.items():
        for g in gs:
            f = os.path.join(RAIZ, "guias", g, "index.html")
            if os.path.exists(f):
                t = re.search(r"<h1>(.*?)</h1>", open(f, encoding="utf-8").read()).group(1)
                out.setdefault(k, []).append((g, "Guía: " + html.unescape(t)))
    return out


def main():
    todas = [ciudad(c) for c in CIUDADES]
    guias = guias_por_rubro()
    paginas = [hub_indice(todas)]
    for c in todas:
        paginas.append(hub_ciudad(c, todas))
        for rk in RUBROS:
            paginas.append(pagina(c, rk, todas, guias))
    for ruta, doc in paginas:
        if "—" in doc:
            raise SystemExit(f"raya larga en {ruta}")
        d = os.path.join(RAIZ, ruta.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(doc)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for ruta, _ in paginas:
        pr = "0.6" if ruta.count("/") > 3 else "0.7"
        sm.append(f"  <url><loc>{BASE}{ruta}</loc><lastmod>{HOY}</lastmod><changefreq>monthly</changefreq><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(RAIZ, "sitemap-negocios.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")
    n = sum(1 for r, _ in paginas if r.count("/") == 4)
    print(f"{len(paginas)} páginas ({n} ciudad x rubro, {len(todas)} ciudades)")


if __name__ == "__main__":
    main()
