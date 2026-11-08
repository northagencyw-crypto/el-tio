# Páginas /ciudades/{slug}/ para Colombia, Argentina, Chile y Perú.
# Toma cabecera y pie de /ciudades/monterrey/ y arma el cuerpo. Sin precios, sin llamadas.
# Uso: python generador/ciudades_latam.py (desde el-tio). Idempotente.
import json, re, pathlib
from urllib.parse import quote

R = pathlib.Path(__file__).resolve().parent.parent
BASE = (R / "ciudades/monterrey/index.html").read_text(encoding="utf-8")
HEADER = BASE[BASE.index('<body>'):BASE.index('<main id="contenido">')]
FOOTER = BASE[BASE.index('</main>') + len('</main>'):]
# Estas páginas solo existen en español: sin selector de idioma.
HEADER = re.sub(r'\s*<details class="idioma">.*?</details>', '', HEADER, flags=re.S)
ICONO = BASE[BASE.index('<link rel="icon"'):BASE.index('<script type="application/ld+json">')]
WA = "https://wa.me/525568976898?text="

PAIS = {
    "co": ("Colombia", "es_CO", "es-CO", "la Ley 1581 de 2012 de protección de datos personales"),
    "ar": ("Argentina", "es_AR", "es-AR", "la Ley 25.326 de protección de datos personales"),
    "cl": ("Chile", "es_CL", "es-CL", "la Ley 19.628 sobre protección de la vida privada y su reforma, la Ley 21.719"),
    "pe": ("Perú", "es_PE", "es-PE", "la Ley 29733 de protección de datos personales"),
}
RUB = {
    "gastronomia": ("Gastronomía", "Restaurantes, bares y cafeterías", "Reservas por WhatsApp e Instagram, confirmación la víspera y la carta a la vista cuando alguien pregunta dónde comer."),
    "hospitality": ("Hospitality", "Hoteles boutique, hostales y tours", "Respuesta en español y en inglés a cualquier hora y reservas que pasan a tu canal directo."),
    "real-estate": ("Real estate", "Inmobiliarias y desarrolladoras", "Respuesta inmediata a cada consulta, visita agendada y la base de interesados ordenada por zona y presupuesto."),
    "fitness": ("Fitness", "Gimnasios y estudios", "Clase de prueba, seguimiento a quien no se inscribió y aviso antes de que un socio se dé de baja."),
    "eventos": ("Eventos", "Productoras, promotores y salas", "Atención de cada fecha y la lista de compradores para la siguiente."),
    "artistas": ("Artistas", "Artistas, DJs y managers", "Consultas de contratación ordenadas y la agenda al día."),
    "distribucion": ("Distribución", "Mayoristas, ferreterías e importadores", "El pedido llega como el cliente quiere y sale como una cotización lista para revisar."),
}
AUD = [
    ("distribucion", "Distribución", "Mayoristas, ferreterías e importadores"),
    ("real-estate", "Real estate", "Inmobiliarias, desarrolladoras y brokers"),
    ("fitness", "Fitness", "Gimnasios y estudios"),
    ("gastronomia", "Gastronomía", "Restaurantes, bares, cafeterías y panaderías"),
    ("eventos", "Eventos", "Productoras, promotores y salas"),
    ("hospitality", "Hospitality", "Hoteles boutique, rentas vacacionales y tours"),
    ("artistas", "Artistas", "Artistas, DJs y managers"),
]

C = [
    dict(slug="bogota", nombre="Bogotá", region="Bogotá D. C.", pais="co", zona="Bogotá y la Sabana",
         rubros=["gastronomia", "real-estate", "fitness", "eventos", "distribucion"],
         intro="Página web, agentes de WhatsApp e Instagram y CRM para negocios de Bogotá y la Sabana, de Chapinero y Usaquén a la zona T.",
         parr=["Bogotá es una ciudad grande, repartida en localidades que funcionan casi como ciudades aparte. Quien busca un restaurante, un gimnasio o un apartamento casi siempre busca cerca de donde vive o trabaja, y lo hace desde el celular. Si tu negocio no aparece en esa búsqueda, la visita se la lleva otro de la misma cuadra.",
               "En Bogotá casi todo se conversa por WhatsApp. El problema suele ser el tiempo de respuesta: el mensaje llega en hora pico, nadie lo ve hasta la noche y para entonces el cliente ya reservó en otro lado. Por eso aquí El Tío empieza por la página web y por un agente que contesta al instante, agenda y deja cada contacto guardado."]),
    dict(slug="medellin", nombre="Medellín", region="Antioquia", pais="co", zona="Medellín y el Valle de Aburrá",
         rubros=["hospitality", "gastronomia", "real-estate", "fitness", "eventos"],
         intro="Página web en 8 idiomas, agentes de WhatsApp e Instagram y CRM para negocios de Medellín, Envigado, Sabaneta y el resto del Valle de Aburrá.",
         parr=["Medellín recibe muchos visitantes y personas de otros países que se quedan a vivir por temporadas. Eso cambia cómo te buscan: parte de tus clientes pregunta en inglés, compara desde antes de llegar y le pide recomendaciones a un asistente de IA en lugar de a un amigo.",
               "Para un hostal en Laureles, un restaurante en El Poblado o una inmobiliaria que arrienda amoblados, eso significa estar en Google y en esos asistentes con información clara, y contestar a cualquier hora en el idioma de quien escribe. Ahí empieza El Tío en Medellín: la web en 8 idiomas y un agente que responde mientras tu equipo atiende a quien ya llegó."]),
    dict(slug="buenos-aires", nombre="Buenos Aires", region="Ciudad Autónoma de Buenos Aires", pais="ar", zona="la Ciudad de Buenos Aires y el conurbano",
         rubros=["gastronomia", "eventos", "fitness", "real-estate", "hospitality"],
         intro="Página web, agentes de WhatsApp e Instagram y CRM para negocios de Buenos Aires, de Palermo y Recoleta a San Telmo y Belgrano.",
         parr=["Buenos Aires tiene una oferta enorme en cada barrio y un público que compara mucho antes de elegir. Quien busca dónde cenar, un gimnasio o una sala para un evento mira reseñas, fotos y horarios, y cada vez más le pregunta directo a ChatGPT o a Gemini. Si tu negocio no tiene una web clara con esos datos, el asistente recomienda a otro.",
               "La otra mitad del problema es la respuesta. Los mensajes por WhatsApp e Instagram llegan a cualquier hora y se acumulan justo en los momentos de más trabajo. El Tío en Buenos Aires arranca por la web y por un agente que contesta, toma la reserva o la consulta y la deja ordenada en un CRM para que no se pierda ninguna."]),
    dict(slug="cordoba", nombre="Córdoba", region="Provincia de Córdoba", pais="ar", zona="Córdoba capital y las Sierras",
         rubros=["gastronomia", "fitness", "real-estate", "eventos", "distribucion"],
         intro="Página web, agentes de WhatsApp y CRM para negocios de Córdoba, de Nueva Córdoba y Güemes al Cerro de las Rosas.",
         parr=["Córdoba es una ciudad universitaria, con mucha gente joven que decide desde el celular y en el momento. Un bar, un gimnasio o un departamento para estudiantes se eligen en minutos, y gana el que aparece primero y contesta rápido.",
               "Córdoba también es el centro comercial de una región grande, con distribuidoras y mayoristas que reciben pedidos por WhatsApp todo el día. En los dos casos El Tío empieza por lo mismo: una web que te haga aparecer en Google y en los asistentes de IA, y un agente que responda y ordene cada consulta o pedido."]),
    dict(slug="santiago", nombre="Santiago", region="Región Metropolitana", pais="cl", zona="Santiago y las comunas de la Región Metropolitana",
         rubros=["gastronomia", "real-estate", "fitness", "distribucion", "eventos"],
         intro="Página web, agentes de WhatsApp e Instagram y CRM para negocios de Santiago, de Providencia y Las Condes a Ñuñoa y el Centro.",
         parr=["Santiago concentra buena parte de los negocios del país en comunas muy distintas entre sí. Quien busca en Providencia no busca lo mismo que quien busca en Maipú, y la búsqueda casi siempre incluye la comuna. Una web pensada para tu comuna y tu rubro es lo que hace que aparezcas en esa búsqueda, en Google y en los asistentes de IA.",
               "En inmobiliarias, gimnasios y restaurantes el cuello de botella suele ser el mismo: llegan consultas por WhatsApp e Instagram que nadie alcanza a contestar a tiempo. El Tío en Santiago empieza por la web y por un agente que responde al instante, agenda la visita o la reserva y deja el historial de cada cliente en un CRM."]),
    dict(slug="lima", nombre="Lima", region="Lima Metropolitana", pais="pe", zona="Lima Metropolitana y el Callao",
         rubros=["gastronomia", "hospitality", "real-estate", "fitness", "distribucion"],
         intro="Página web, agentes de WhatsApp e Instagram y CRM para negocios de Lima, de Miraflores y San Isidro a Barranco y Surco.",
         parr=["Lima es uno de los centros gastronómicos de la región y recibe visitantes todo el año. Eso hace que la competencia en restaurantes, hoteles y tours sea fuerte, y que buena parte de los clientes llegue preguntando en inglés o desde un asistente de IA que arma la lista de recomendaciones.",
               "Al mismo tiempo, en Lima casi todo se cierra por WhatsApp, y el mensaje que no se contesta en minutos se va a otro distrito. El Tío en Lima empieza por la web en 8 idiomas para que te encuentren, y por un agente que contesta, toma la reserva o el pedido y deja cada contacto guardado."]),
    dict(slug="cali", nombre="Cali", region="Valle del Cauca", pais="co", zona="Cali y el Valle del Cauca",
         rubros=["gastronomia", "eventos", "fitness", "distribucion", "real-estate"],
         intro="Página web, agentes de WhatsApp e Instagram y CRM para negocios de Cali, de Granada y San Antonio al Peñón y el sur de la ciudad.",
         parr=["Cali vive de noche y de fin de semana: restaurantes, bares, escuelas de salsa y eventos que llenan la agenda, sobre todo cuando se acerca la Feria de diciembre. Quien sale a comer o busca dónde bailar decide desde el celular y en el momento, y elige al que aparece primero y contesta rápido.",
               "Cali también es el centro comercial del Valle, con distribuidoras y mayoristas que reciben pedidos por WhatsApp todo el día. En los dos casos El Tío empieza igual: una web que te haga aparecer en Google y en los asistentes de IA, y un agente que contesta, toma la reserva o el pedido y lo deja guardado en un CRM."]),
    dict(slug="rosario", nombre="Rosario", region="Provincia de Santa Fe", pais="ar", zona="Rosario y el Gran Rosario",
         rubros=["gastronomia", "distribucion", "real-estate", "fitness", "eventos"],
         intro="Página web, agentes de WhatsApp y CRM para negocios de Rosario, del centro y Pichincha a Fisherton y la costa del Paraná.",
         parr=["Rosario es una ciudad de comercio, con una economía muy ligada al campo y al puerto. Muchas empresas de la zona, de distribuidoras a corralones, reciben pedidos y consultas por WhatsApp a toda hora y los contestan a mano, uno por uno, cuando el equipo puede.",
               "Al mismo tiempo, Rosario tiene una vida gastronómica y nocturna fuerte, con un público que elige dónde ir mirando el celular. Para unos y otros El Tío empieza por la web, para que te encuentren en Google y en los asistentes de IA, y por un agente que responde al instante y ordena cada pedido o reserva."]),
    dict(slug="valparaiso", nombre="Valparaíso", region="Región de Valparaíso", pais="cl", zona="Valparaíso y Viña del Mar",
         rubros=["hospitality", "gastronomia", "eventos", "real-estate", "distribucion"],
         intro="Página web en 8 idiomas, agentes de WhatsApp e Instagram y CRM para negocios de Valparaíso, de los cerros Alegre y Concepción al Plan y Viña del Mar.",
         parr=["Valparaíso recibe turistas de todo el mundo durante el año, y en temporada de cruceros y en Año Nuevo la ciudad se llena. Buena parte de esos visitantes busca hospedaje, restaurantes y paseos en inglés, desde antes de llegar, y cada vez más le pide la lista a un asistente de IA.",
               "Para un hostal en los cerros, un restaurante con vista a la bahía o una agencia de paseos, eso significa estar en Google y en esos asistentes con datos claros, y contestar en el idioma de quien escribe aunque sea de madrugada. Ahí empieza El Tío en Valparaíso: la web en 8 idiomas y un agente que responde mientras tu equipo atiende a quien ya está ahí."]),
    dict(slug="arequipa", nombre="Arequipa", region="Región Arequipa", pais="pe", zona="Arequipa y el sur del Perú",
         rubros=["gastronomia", "hospitality", "distribucion", "real-estate", "fitness"],
         intro="Página web, agentes de WhatsApp e Instagram y CRM para negocios de Arequipa, del Centro Histórico y Yanahuara a Cayma y Cerro Colorado.",
         parr=["Arequipa es la puerta de entrada al Colca y recibe visitantes todo el año, que llegan buscando hospedaje en el centro, una picantería o un tour para el día siguiente. Muchos preguntan en inglés y comparan desde el celular, así que gana el negocio que aparece con información clara y contesta primero.",
               "Arequipa también es el centro comercial del sur del país, con distribuidoras e importadores que atienden pedidos por WhatsApp desde varias regiones. El Tío en Arequipa empieza por la web, para que te encuentren en Google y en los asistentes de IA, y por un agente que responde, toma la reserva o el pedido y deja cada contacto guardado."]),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def page(c):
    pn, ogl, lang, ley = PAIS[c["pais"]]
    url = f"https://eltio.net/ciudades/{c['slug']}/"
    title = f"Página web y agentes de IA para negocios en {c['nombre']} · El Tío"
    desc = (f"Página web con dominio propio, en 8 idiomas y con posicionamiento en Google y en IA para negocios de "
            f"{c['nombre']}, {pn}. Además, agentes de WhatsApp, CRM y automatizaciones. Audit gratis.")
    faqs = [
        (f"¿Trabajan con negocios de {c['nombre']}?", "Sí. El Audit es en línea, las dudas se resuelven por chat y la instalación se prueba de punta a punta a distancia. No hace falta que nadie vaya a tu negocio."),
        (f"¿Cómo cuidan los datos de mis clientes en {pn}?", f"Los datos de tus clientes son tuyos y se usan solo para atenderlos. Trabajamos dentro de {ley}, y en el Audit revisamos qué avisos y permisos necesitas antes de instalar nada."),
        ("¿Por qué conviene empezar ahora?", "Porque hoy la mayoría de los negocios de tu rubro todavía no usa IA para atender ni para aparecer en los asistentes. Quien lo hace primero se queda con esas consultas, y esa ventaja se achica a medida que los demás se suman."),
        ("¿Cuánto cuesta?", "El Audit es gratis. Los paquetes y sus condiciones están en la página de paquetes, y todo es mes a mes, sin contrato largo."),
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "ProfessionalService", "name": f"El Tío · IA para empresas en {c['nombre']}",
         "description": desc, "url": url, "email": "hola@eltio.net", "telephone": "+52 55 6897 6898", "inLanguage": lang,
         "areaServed": [{"@type": "City", "name": c["nombre"], "containedInPlace": {"@type": "Country", "name": pn}}],
         "parentOrganization": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net/", "email": "hola@eltio.net"},
         "knowsAbout": ["Páginas web", "Posicionamiento en IA", "Agentes de IA para WhatsApp", "CRM", "Automatización de procesos"],
         "makesOffer": [{"@type": "Offer", "name": "Audit", "price": 0, "priceCurrency": "USD", "url": "https://eltio.net/paquetes/"}]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "El Tío", "item": "https://eltio.net/"},
            {"@type": "ListItem", "position": 2, "name": "Ciudades", "item": "https://eltio.net/ciudades/"},
            {"@type": "ListItem", "position": 3, "name": c["nombre"], "item": url}]},
    ]
    wa = WA + quote(f"¡Hola! Tengo un negocio en {c['nombre']} y quiero hablar con El Tío.")
    scripts = "".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>\n' for x in ld)
    head = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#04070B">
<meta property="og:type" content="website">
<meta property="og:locale" content="{ogl}">
<meta property="og:site_name" content="El Tío">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title.replace(' · El Tío', ''))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://eltio.net/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
{ICONO}{scripts}<script src="/medicion.js" defer></script>
</head>
'''
    rub = "\n".join(
        f'      <a class="tarjeta" href="/negocios/{c["slug"]}/{r}/"><span class="tag">{RUB[r][0]}</span><h3>{RUB[r][1]}</h3><p>{RUB[r][2]}</p></a>'
        for r in c["rubros"])
    fuerte = ' class="fuerte"'
    aud = "\n".join(
        f'        <li><a{fuerte if k in c["rubros"] else ""} data-cta="audit" href="https://app.eltio.net/auditoria/{k}">{n}<span>{d}</span></a></li>'
        for k, n, d in sorted(AUD, key=lambda x: x[0] not in c["rubros"]))
    parr = "\n".join(f"    <p>{p}</p>" for p in c["parr"])
    faqh = "\n".join(f'      <details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in faqs)
    faqh = faqh.replace("la página de paquetes", '<a href="/paquetes/">la página de paquetes</a>')
    main = f'''<main id="contenido">
  <nav class="migas franja" aria-label="Ruta" style="padding-bottom:0"><a href="/">El Tío</a> / <a href="/ciudades/">Ciudades</a> / {c["nombre"]}</nav>
  <section class="franja" style="padding-top:8px">
    <p class="ojo">{c["region"]}, {pn}</p>
    <h1>Tu página web para que te encuentren en {c["nombre"]}</h1>
    <p class="bajada">Una página con dominio propio, en 8 idiomas y con posicionamiento en Google y en los asistentes de IA, para que quien busca en {c["nombre"]} llegue a tu negocio y no al de al lado.</p>
    <div class="acciones">
      <a class="btn" data-cta="audit" href="#audit">Hacer el Audit gratis</a>
      <a class="enlace" data-cta="whatsapp" href="{wa}">Escribir por WhatsApp</a>
    </div>
  </section>
  <section class="franja">
    <h2>Qué trae tu página</h2>
    <div class="grilla">
      <a class="tarjeta" href="/paginas-web/"><span class="tag">Web</span><h3>Dominio propio</h3><p>A nombre de tu negocio, con correo en ese dominio si lo necesitas.</p></a>
      <a class="tarjeta" href="/paginas-web/"><span class="tag">Web</span><h3>8 idiomas</h3><p>Español, inglés, portugués, francés, alemán, italiano, chino y japonés, cada uno con su dirección.</p></a>
      <a class="tarjeta" href="/posicionamiento-en-ia/"><span class="tag">Web</span><h3>Google y asistentes de IA</h3><p>Lista para aparecer en Google, ChatGPT, Perplexity y Gemini, con seguimiento cada mes.</p></a>
    </div>
    <p style="margin-top:20px"><a href="/paquetes/">Ver los paquetes</a></p>
  </section>
  <section class="franja">
    <h2>Además, para tu negocio en {c["nombre"]}</h2>
    <p>{c["intro"]}</p>
{parr}
  </section>
  <section class="franja">
    <h2>Tu ventaja en {c["nombre"]} es hoy</h2>
    <p>La mayoría de los negocios de {c["zona"]} todavía no usa IA para contestar, dar seguimiento ni aparecer cuando alguien le pregunta a un asistente. Eso no va a durar: cada mes se suma alguien de tu rubro y de tu zona.</p>
    <p>Quien se mueve ahora se queda con las consultas que hoy nadie contesta a tiempo. El primer paso es saber cómo está tu negocio, y para eso está el Audit gratis.</p>
    <div class="acciones"><a class="btn" data-cta="audit" href="#audit">No pierdas la ventaja, es hoy</a></div>
  </section>
  <section class="franja">
    <h2>Rubros en {c["nombre"]}</h2>
    <div class="grilla">
{rub}
    </div>
    <p style="margin-top:20px"><a href="/negocios/{c["slug"]}/">Ver todos los rubros en {c["nombre"]}</a></p>
  </section>
  <section class="franja">
    <h2>Lo que se puede sumar a la web</h2>
    <div class="grilla">
      <a class="tarjeta" href="/servicios/agente-whatsapp-instagram/"><span class="tag">Atención</span><h3>Agente de WhatsApp e Instagram</h3><p>Contesta, agenda y guarda cada contacto.</p></a>
      <a class="tarjeta" href="/servicios/crm-y-seguimiento/"><span class="tag">Operación</span><h3>CRM y seguimiento</h3><p>Contactos en un lugar, recordatorios y cobranza.</p></a>
      <a class="tarjeta" href="/servicios/automatizaciones-y-reportes/"><span class="tag">Operación</span><h3>Automatizaciones y reportes</h3><p>Tareas repetidas en flujos y el reporte del lunes.</p></a>
      <a class="tarjeta" href="/servicios/capacitacion/"><span class="tag">Equipo</span><h3>Capacitación</h3><p>Tu equipo usando IA con reglas claras.</p></a>
    </div>
    <p style="margin-top:20px"><a href="/como-trabajamos/">Cómo trabajamos</a></p>
  </section>
  <section class="franja" id="preguntas">
    <h2>Preguntas frecuentes</h2>
    <div class="preguntas">
{faqh}
    </div>
  </section>
  <section class="franja">
    <div class="audit" id="audit">
      <p class="ojo">Audit gratis</p>
      <h2>Audit gratis para tu negocio en {c["nombre"]}</h2>
      <p>Un cuestionario guiado de 15 a 25 minutos sobre cómo trabaja hoy tu negocio. Lo revisa una persona y en 24 a 48 horas hábiles recibes el mapa de lo que conviene hacer primero, con el motivo de cada cosa. El mapa es tuyo, contrates o no.</p>
      <ul class="rubros">
{aud}
      </ul>
      <p class="nota">Elige tu rubro para abrir su cuestionario. ¿Prefieres escribir primero? <a href="{wa}" data-cta="whatsapp">Escríbenos por WhatsApp</a>.</p>
    </div>
  </section>
</main>'''
    return head + HEADER + main + FOOTER


def hub():
    p = R / "ciudades/index.html"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'  <section class="franja" id="latam">.*?</section>\n', '', s, flags=re.S)
    cards = "\n".join(
        f'      <a class="tarjeta" href="/ciudades/{c["slug"]}/"><span class="tag">{PAIS[c["pais"]][0]}</span><h3>{c["nombre"]}</h3><p>{c["intro"]}</p></a>'
        for c in sorted(C, key=lambda c: list(PAIS).index(c["pais"])))
    sec = f'  <section class="franja" id="latam">\n    <h2>Colombia, Argentina, Chile y Perú</h2>\n    <div class="grilla">\n{cards}\n    </div>\n  </section>\n'
    i = s.index('  <section class="franja">\n    <h2>Lo que sigue</h2>')
    s = s[:i] + sec + s[i:]
    s = s.replace("y luego Bogotá, Buenos Aires, Santiago y Lima. Si tu negocio",
                  "y en el resto de Latinoamérica seguimos sumando ciudades. Si tu negocio")
    p.write_text(s, encoding="utf-8")


def sitemap():
    p = R / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    for c in C:
        loc = f"https://eltio.net/ciudades/{c['slug']}/"
        if f"<loc>{loc}</loc>" in s:
            continue
        s = s.replace("</urlset>", f"  <url><loc>{loc}</loc><lastmod>2026-11-08</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>")
    p.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    for c in C:
        d = R / "ciudades" / c["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(c), encoding="utf-8", newline="\n")
    hub()
    sitemap()
    print("ok", [c["slug"] for c in C])
