"""Genera /indice/2026/ (dataset, CSV) y /prensa/ desde generador/indice2026.json.
Los conteos salen de eltio-ops/indice/2026/agregar.py (DENUE INEGI, solo agregados).
Uso: python -X utf8 generador/indice2026.py"""
import csv, json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(R, "generador", "indice2026.json"), encoding="utf-8"))
BASE = open(os.path.join(R, "indice", "index.html"), encoding="utf-8").read()
HEADER = BASE[BASE.index('<header class="cabecera">'):BASE.index('</header>') + 9]
HEADER = re.sub(r'\s*<details class="idioma">.*?</details>', '', HEADER, flags=re.S)
FOOTER = BASE[BASE.index('<footer class="pie">'):BASE.index('</footer>') + 9]
AUDIT = BASE[BASE.index('<section class="franja">\n    <div class="audit"'):BASE.index('</main>')]
WA = "https://wa.me/525568976898?text=Hola%21%20Escribo%20por%20el%20%C3%8Dndice%20El%20T%C3%ADo."
FECHA = "2026-11-07"
PARCIAL = {"Guerrero"}  # descarga incompleta


def n(x): return f"{x:,}".replace(",", ".")
def pct(s, t): return round(100 * s / t, 1)
def p(x): return f"{x:.1f}".replace(".", ",") + " %"
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
def corto(e): return e.replace(" de Ocampo", "").replace(" de Ignacio de la Llave", "").replace(" de Zaragoza", "")


TOT, SIN = D["total"]
TP = pct(SIN, TOT)
EST = [(e, t, s, pct(s, t)) for e, t, s in D["estados"]]
EST_OK = [x for x in EST if x[0] not in PARCIAL]
RUB = [(r, t, s, pct(s, t)) for r, t, s in D["rubros"]]
CIU = [(c, e, t, s, pct(s, t)) for c, e, t, s in D["ciudades"]]
TOPE, BAJO = EST_OK[0], EST_OK[-1]
GUE = next(t for e, t, s, v in EST if e == "Guerrero")

CSS = (".cifras{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:24px 0}"
       ".cifras div{border:1px solid rgba(127,201,242,.3);border-radius:10px;padding:16px}"
       ".cifras b{display:block;font-size:2rem;color:#7FC9F2}.descargas li{margin:6px 0}"
       ".cita{border-left:3px solid #7FC9F2;padding:4px 0 4px 16px;margin:16px 0}"
       ".fotos{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}"
       ".fotos figure{margin:0}.fotos img{width:100%;height:auto;border-radius:8px}")


def head(title, desc, url, ld):
    scripts = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, indent=1)}</script>\n' for x in ld)
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#04070B">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="El Tío">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://eltio.net/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2304070B'/%3E%3Ctext x='16' y='23' font-family='monospace' font-size='19' font-weight='700' fill='%237FC9F2' text-anchor='middle'%3ET%3C/text%3E%3C/svg%3E">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-var.woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/paginas.css">
<style>{CSS}</style>
{scripts}<script src="/medicion.js" defer></script>
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{HEADER}
<main id="contenido">
"""


def migas(*items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": a, "item": u} for i, (a, u) in enumerate(items)]}
    html = " / ".join(f'<a href="{u.replace("https://eltio.net", "")}">{a}</a>' for a, u in items[:-1]) + f" / {items[-1][0]}"
    return ld, f'  <nav class="migas franja" aria-label="Ruta" style="padding-bottom:0">{html}</nav>\n'


def barras(filas, label, lo=75):
    h, w, x0 = 26, 210, 170
    out = [f'<svg viewBox="0 0 440 {len(filas) * h + 24}" width="100%" role="img" aria-label="{label}">']
    for i, (nom, v) in enumerate(filas):
        y = i * h
        ancho = max(2, (v - lo) / (100 - lo) * w)
        out.append(f'<text x="0" y="{y + 16}" font-size="13" fill="currentColor">{esc(nom)}</text>'
                   f'<rect x="{x0}" y="{y + 4}" width="{ancho:.0f}" height="16" rx="3" fill="#7FC9F2"/>'
                   f'<text x="{x0 + ancho + 6:.0f}" y="{y + 17}" font-size="12" fill="currentColor">{p(v)}</text>')
    y = len(filas) * h + 16
    out.append(f'<text x="{x0}" y="{y}" font-size="11" fill="currentColor" opacity=".7">{lo} %</text>'
               f'<text x="{x0 + w}" y="{y}" font-size="11" fill="currentColor" opacity=".7" text-anchor="end">100 %</text></svg>')
    return "".join(out)


def tabla(cab, filas):
    th = "".join(f"<th>{c}</th>" for c in cab)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f'<div class="tabla"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def escribir_csv(nombre, cab, filas):
    with open(os.path.join(R, "indice", "2026", nombre), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows(filas)


def brecha(v):
    d = round(v - TP, 1)
    return (f"+{d}" if d > 0 else f"{d}").replace(".", ",") + " pp"


os.makedirs(os.path.join(R, "indice", "2026"), exist_ok=True)
escribir_csv("estados.csv", ["estado", "negocios", "sin_web_registrada", "pct_sin_web", "cobertura"],
             [(e, t, s, v, "parcial" if e in PARCIAL else "completa") for e, t, s, v in EST])
escribir_csv("rubros.csv", ["rubro", "negocios", "sin_web_registrada", "pct_sin_web", "con_web_registrada", "brecha_pp_vs_promedio"],
             [(r, t, s, v, t - s, round(v - TP, 1)) for r, t, s, v in RUB])
escribir_csv("ciudades-top10.csv", ["ciudad", "estado", "negocios", "sin_web_registrada", "pct_sin_web"], CIU)
escribir_csv("estado-rubro.csv", ["estado", "rubro", "negocios", "sin_web_registrada", "pct_sin_web"],
             [(e, r, t, s, pct(s, t)) for e, r, t, s in D["rubro_estado"]])

CSVS = [("estados.csv", "Por estado (32 entidades)"),
        ("rubros.csv", "Por rubro, con la brecha contra el promedio nacional"),
        ("ciudades-top10.csv", "Las 10 ciudades con más negocios"),
        ("estado-rubro.csv", "Estado por rubro (cruce completo)")]
URL = "https://eltio.net/indice/2026/"
TIT = "Índice El Tío 2026: negocios chicos de México sin web"
DESC = (f"{n(SIN)} de {n(TOT)} negocios de hasta 50 personas de México ({p(TP)}) no registran página web en el DENUE del INEGI. "
        "Por estado, rubro y ciudad, con CSV.")
dataset = {
    "@context": "https://schema.org", "@type": "Dataset", "name": "Índice El Tío 2026",
    "description": DESC, "url": URL, "inLanguage": "es-MX", "datePublished": FECHA, "dateModified": FECHA,
    "temporalCoverage": "2026", "spatialCoverage": {"@type": "Place", "name": "México"},
    "keywords": ["pymes", "México", "página web", "digitalización", "DENUE", "INEGI", "brecha digital"],
    "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/",
    "creator": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net"},
    "isBasedOn": {"@type": "Dataset", "name": "Directorio Estadístico Nacional de Unidades Económicas (DENUE)",
                  "url": "https://www.inegi.org.mx/app/mapa/denue/",
                  "creator": {"@type": "Organization", "name": "INEGI"}},
    "variableMeasured": ["negocios", "sin_web_registrada", "pct_sin_web"],
    "measurementTechnique": "Conteo de establecimientos de 0 a 50 personas ocupadas con el campo de sitio web vacío en el DENUE",
    "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "name": d, "contentUrl": URL + f} for f, d in CSVS]}
ld_m, html_m = migas(("El Tío", "https://eltio.net/"), ("Índice El Tío", "https://eltio.net/indice/"), ("Edición 2026", URL))

hosp = next(x for x in RUB if x[0] == "Hospitality")
cdmx = CIU[0]
html = head(TIT, DESC, URL, [dataset, ld_m]) + html_m + f"""  <section class="franja" style="padding-top:8px">
    <p class="ojo">Índice El Tío · edición 2026 · datos al 07/11/2026</p>
    <h1>{p(TP)} de los negocios chicos de México no tienen web registrada</h1>
    <p class="bajada">Contamos {n(TOT)} negocios de hasta 50 personas en los 32 estados con el DENUE del INEGI. {n(SIN)} no registran una página web. Abajo están las cifras por estado, por rubro y por ciudad, las tablas para descargar y el método.</p>
    <div class="cifras">
      <div><b>{p(TP)}</b>sin web registrada en todo el país</div>
      <div><b>{p(RUB[0][3])}</b>en {RUB[0][0].lower()}, el rubro con la brecha más grande</div>
      <div><b>{p(TOPE[3])}</b>en {corto(TOPE[0])}, el estado más alto con cobertura completa</div>
      <div><b>{p(BAJO[3])}</b>en {corto(BAJO[0])}, el estado más bajo</div>
    </div>
    <div class="acciones">
      <a class="btn" data-cta="audit" href="#audit">Hacer el Audit gratis</a>
      <a class="enlace" href="#descargas">Descargar las tablas (CSV)</a>
    </div>
  </section>
  <section class="franja">
    <h2>Por estado</h2>
    <p>Los estados del sur y del centro van arriba. Nuevo León, Quintana Roo, Querétaro y las dos Baja California van abajo, y ninguno baja de 87 %.</p>
    <figure class="grafico" style="max-width:640px;margin:24px 0">{barras([(corto(e), v) for e, t, s, v in EST_OK], "Porcentaje de negocios sin web registrada por estado")}<figcaption>Negocios de hasta 50 personas sin web registrada en el DENUE, por estado. La escala empieza en 75 %. Guerrero queda fuera del gráfico porque su descarga está incompleta.</figcaption></figure>
    {tabla(["Estado", "Negocios", "Sin web registrada", "%"], [(e + (" (cobertura parcial)" if e in PARCIAL else ""), n(t), n(s), p(v)) for e, t, s, v in EST])}
  </section>
  <section class="franja">
    <h2>Por rubro: dónde está la brecha</h2>
    <p>Talleres, belleza y restaurantes casi no tienen web registrada: 99, 99 y 98 de cada 100. En el otro extremo están turismo y hospitality, que venden a gente de fuera, y aun así 8 de cada 10 no la registran. La brecha es la distancia contra el promedio nacional de {p(TP)}.</p>
    <figure class="grafico" style="max-width:640px;margin:24px 0">{barras([(r, v) for r, t, s, v in RUB], "Porcentaje de negocios sin web registrada por rubro")}<figcaption>Por rubro. «Otros» reúne comercio y servicios fuera de los nueve rubros que sigue El Tío. La escala empieza en 75 %.</figcaption></figure>
    {tabla(["Rubro", "Negocios", "Sin web registrada", "%", "Brecha contra el promedio"], [(r, n(t), n(s), p(v), brecha(v)) for r, t, s, v in RUB])}
  </section>
  <section class="franja">
    <h2>Las 10 ciudades con más negocios</h2>
    <p>Ciudad de México es la entidad completa. Guadalajara suma Zapopan, Tlaquepaque, Tonalá y Tlajomulco. Monterrey suma San Pedro, Guadalupe, San Nicolás, Apodaca y Santa Catarina. El resto es el municipio.</p>
    <figure class="grafico" style="max-width:640px;margin:24px 0">{barras([(c, v) for c, e, t, s, v in CIU], "Porcentaje de negocios sin web registrada en las 10 ciudades con más negocios")}<figcaption>Las 10 ciudades ordenadas por cantidad de negocios. La escala empieza en 75 %.</figcaption></figure>
    {tabla(["Ciudad", "Estado", "Negocios", "Sin web registrada", "%"], [(c, e, n(t), n(s), p(v)) for c, e, t, s, v in CIU])}
  </section>
  <section class="franja" id="descargas">
    <h2>Descargas</h2>
    <p>Tablas en CSV (UTF-8, coma como separador, punto decimal). Solo totales: no hay nombres, teléfonos ni direcciones de negocios. Uso libre (CC BY 4.0) citando «Índice El Tío 2026, con datos del DENUE del INEGI».</p>
    <ul class="descargas">{''.join(f'<li><a href="/indice/2026/{f}" download>{f}</a>: {d}</li>' for f, d in CSVS)}</ul>
  </section>
  <section class="franja" id="metodo">
    <h2>Método y fuentes</h2>
    <p><b>Fuente.</b> Directorio Estadístico Nacional de Unidades Económicas (DENUE) del INEGI, descarga masiva por entidad, datos abiertos (<a href="https://www.inegi.org.mx/app/mapa/denue/">inegi.org.mx</a>). Procesado por El Tío en noviembre de 2026.</p>
    <p><b>Universo.</b> Establecimientos de 0 a 50 personas ocupadas (estratos 0 a 5, 6 a 10, 11 a 30 y 31 a 50). Se quitan gobierno, asociaciones, banca y agencias de marketing y de sistemas (SCIAN 93, 813, 521, 522, 5415, 5416 y 5418). No es el total de negocios del país, es ese universo.</p>
    <p><b>Rubros.</b> Por código SCIAN: restaurantes (722), hospitality (7211, 7212), salud (6211, 6212), belleza (8121), talleres (8111), fitness (7139), real estate (5311, 5312), eventos (7111, 53228) y turismo (5615). Lo demás va a «Otros».</p>
    <p><b>Qué es «sin web».</b> El campo de sitio web del DENUE vacío, o sea «sin web registrada en el directorio». Un negocio pudo tener una y no declararla, así que la cifra puede estar algo alta. Por eso este índice no dice que estos negocios «no existen en internet».</p>
    <p><b>Validación.</b> En la edición 1 revisamos 375 de las webs que sí figuran en el DENUE: 45 % no cargó. La validación inversa (negocios sin web registrada buscados uno por uno) queda para la próxima edición.</p>
    <p><b>Límites.</b> La descarga de Guerrero está incompleta ({n(GUE)} registros) y se marca como cobertura parcial; entra en el total nacional y en las tablas, no en el gráfico ni en los extremos. No hay intervalo de confianza porque no es una muestra: es el conteo del directorio.</p>
    <p><b>Cambios contra la edición 1.</b> La edición 1 (04/11/2026, <a href="/indice/">eltio.net/indice</a>) contó 83.714 negocios con teléfono publicado, de nueve rubros y en cuatro estados (94 %). Esta edición cubre los 32 estados y todos los rubros, con o sin teléfono, por eso las cifras por ciudad cambian.</p>
  </section>
{AUDIT}</main>
{FOOTER}
</body>
</html>
"""
open(os.path.join(R, "indice", "2026", "index.html"), "w", encoding="utf-8").write(html)

# Prensa
PURL = "https://eltio.net/prensa/"
org = {"@context": "https://schema.org", "@type": "Organization", "name": "El Tío", "url": "https://eltio.net",
       "contactPoint": [{"@type": "ContactPoint", "contactType": "press", "email": "hola@eltio.net",
                         "telephone": "+52-55-6897-6898", "availableLanguage": ["es", "en"]}]}
ld_m, html_m = migas(("El Tío", "https://eltio.net/"), ("Prensa", PURL))
ld_p = {"@context": "https://schema.org", "@type": "WebPage", "name": "Prensa · El Tío", "url": PURL,
        "inLanguage": "es-MX", "about": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net"}}
gdl = next(x for x in CIU if x[0] == "Guadalajara")
mty = next(x for x in CIU if x[0] == "Monterrey")
rest = next(x for x in RUB if x[0] == "Restaurantes")
CITAS = [
    f"{p(TP)} de los negocios de hasta 50 personas de México no tienen página web registrada en el DENUE del INEGI: {n(SIN)} de {n(TOT)}.",
    f"Por rubro, la brecha más grande está en talleres ({p(RUB[0][3])}), belleza ({p(RUB[1][3])}) y restaurantes ({p(rest[3])}). La más chica, en turismo ({p(RUB[-1][3])}) y hospitality ({p(hosp[3])}).",
    f"{corto(TOPE[0])} es el estado con más negocios sin web registrada ({p(TOPE[3])}) y {corto(BAJO[0])} el que menos ({p(BAJO[3])}).",
    f"En Ciudad de México, {n(cdmx[3])} de {n(cdmx[2])} negocios chicos no registran web ({p(cdmx[4])}). En la zona de Guadalajara, {p(gdl[4])}; en la de Monterrey, {p(mty[4])}.",
    f"Restaurantes: {n(rest[2])} de {n(rest[1])} establecimientos de hasta 50 personas no registran web.",
]
FOTOS = [("tio-1.jpg", "El Tío, el personaje de la marca"), ("re-tio-retrato.webp", "Retrato del personaje"),
         ("gas-tio-avatar.webp", "El Tío en un restaurante"), ("ho-tio-recepcion.webp", "El Tío en la recepción de un hotel"),
         ("og.jpg", "Tarjeta de la marca, 1200 x 630")]
ph = head("Prensa · El Tío", "Kit de prensa de El Tío: quiénes somos, cifras del Índice El Tío 2026 listas para citar, imágenes y contacto.",
          PURL, [ld_p, org, ld_m]) + html_m + f"""  <section class="franja" style="padding-top:8px">
    <p class="ojo">Prensa</p>
    <h1>Kit de prensa de El Tío</h1>
    <p class="bajada">Para periodistas, editores y productores. Todo lo de esta página se puede usar citando la fuente.</p>
  </section>
  <section class="franja">
    <h2>Quién es El Tío</h2>
    <p>El Tío es una empresa de Ciudad de México que aplica inteligencia artificial a la operación de negocios chicos y medianos de Latinoamérica. Hace páginas web con dominio propio en ocho idiomas, las posiciona en Google y en los asistentes de IA, instala agentes que responden por WhatsApp e Instagram y ordena el seguimiento de clientes en un CRM.</p>
    <p>Trabaja con restaurantes, hoteles, inmobiliarias, gimnasios, productoras de eventos, artistas y distribuidoras. Empieza siempre por un Audit gratis que muestra qué ve un cliente cuando busca al negocio.</p>
    <p>Publica el Índice El Tío, un conteo abierto de los negocios chicos que no tienen web, hecho con datos públicos del INEGI.</p>
  </section>
  <section class="franja">
    <h2>Cifras listas para citar</h2>
    <p>Fuente de todas: Índice El Tío 2026, con datos del DENUE del INEGI. Universo: negocios de 0 a 50 personas en los 32 estados. «Sin web» quiere decir sin página registrada en el directorio.</p>
    {''.join(f'<p class="cita">{c}</p>' for c in CITAS)}
    <p>Tablas completas, gráficos, CSV y método: <a href="/indice/2026/">eltio.net/indice/2026</a>.</p>
  </section>
  <section class="franja">
    <h2>Imágenes</h2>
    <p>El personaje de El Tío está hecho con IA. Al publicarlo, indicar «Imagen: El Tío, hecha con IA».</p>
    <div class="fotos">{''.join(f'<figure><a href="/assets/{f}" download><img src="/assets/{f}" alt="{a}" loading="lazy"></a><figcaption>{a}</figcaption></figure>' for f, a in FOTOS)}</div>
    <p>Colores de la marca: fondo #04070B y celeste #7FC9F2. Tipografías Archivo y Geist.</p>
  </section>
  <section class="franja">
    <h2>Contacto de prensa</h2>
    <p>Correo: <a href="mailto:hola@eltio.net?subject=Prensa">hola@eltio.net</a>, con el asunto «Prensa».<br>WhatsApp: <a href="{WA}">+52 55 6897 6898</a>.</p>
    <p>Respondemos en el día hábil. Podemos preparar tablas a medida por estado, municipio o rubro.</p>
  </section>
</main>
{FOOTER}
</body>
</html>
"""
open(os.path.join(R, "prensa", "index.html"), "w", encoding="utf-8").write(ph)
print("ok", TP, TOPE, BAJO)
for c in CITAS:
    print("-", c)
