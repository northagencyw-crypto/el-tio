"""Guías «2027» por rubro y ciudad: /guias/2027/{slug}/ y el índice /guias/2027/.

Uso: python generador/guias_2027.py   (desde la raíz del repo)
Genera las páginas, sitemap-2027.xml (sumado a sitemap-index.xml) y el bloque 2027 de llms.txt.
Reglas: respuesta directa en el primer párrafo, criterios, FAQ con schema, enlaces a la ciudad, a la guía
pilar y a /ventaja/. Solo datos con fuente (FUENTES de guias_pilar_datos), sin precios, sin rayas, tuteo neutro.
"""
import os, re, sys, json, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "pseo"))
from build import documento, migas, semilla, rota, e, BASE, HOY, RAIZ
from guias_pilar_datos import FUENTES

WA = "525568976898"
CIUDAD = {"ciudad-de-mexico": "Ciudad de México", "monterrey": "Monterrey", "guadalajara": "Guadalajara",
          "tulum": "Tulum", "cancun": "Cancún", "playa-del-carmen": "Playa del Carmen", "puebla": "Puebla",
          "queretaro": "Querétaro", "merida": "Mérida", "leon": "León"}
CARIBE = {"tulum", "cancun", "playa-del-carmen"}

# Por rubro: textos base, guía pilar, ciudades (9, en orden de prioridad) y lo que se pide por chat.
R = {
 "gastronomia": dict(nombre="Gastronomía", plural="restaurantes", uno="un restaurante", tu="tu restaurante",
    cliente="comensales", pide="reservas, pedidos para llevar y preguntas por el menú",
    pilar="como-usar-ia-en-un-restaurante",
    ciudades=["ciudad-de-mexico", "monterrey", "guadalajara", "puebla", "queretaro", "merida", "tulum", "cancun", "leon"]),
 "hospitality": dict(nombre="Hospitality", plural="hoteles", uno="un hotel", tu="tu hotel",
    cliente="huéspedes", pide="disponibilidad, tarifas por fecha, traslados y preguntas de llegada",
    pilar="como-usar-ia-en-un-hotel",
    ciudades=["tulum", "cancun", "playa-del-carmen", "ciudad-de-mexico", "merida", "guadalajara", "queretaro", "puebla", "monterrey"]),
 "real-estate": dict(nombre="Real estate", plural="inmobiliarias", uno="una inmobiliaria", tu="tu inmobiliaria",
    cliente="interesados", pide="informes de una propiedad, visitas y condiciones de renta o compra",
    pilar="como-usar-ia-en-una-inmobiliaria",
    ciudades=["monterrey", "ciudad-de-mexico", "guadalajara", "queretaro", "tulum", "playa-del-carmen", "merida", "cancun", "puebla"]),
 "fitness": dict(nombre="Fitness", plural="gimnasios", uno="un gimnasio", tu="tu gimnasio",
    cliente="socios", pide="horarios, clases de prueba, altas y renovaciones",
    pilar="como-usar-ia-en-un-gimnasio",
    ciudades=["ciudad-de-mexico", "monterrey", "guadalajara", "queretaro", "puebla", "merida", "leon", "cancun", "playa-del-carmen"]),
 "eventos": dict(nombre="Eventos", plural="salones y productoras de eventos", uno="un salón de eventos", tu="tu salón o productora",
    cliente="clientes", pide="fechas disponibles, cotizaciones y paquetes",
    pilar="como-usar-ia-en-eventos",
    ciudades=["ciudad-de-mexico", "monterrey", "guadalajara", "cancun", "queretaro", "puebla", "merida", "tulum", "leon"]),
 "artistas": dict(nombre="Artistas", plural="artistas y músicos", uno="un proyecto artístico", tu="tu proyecto artístico",
    cliente="público y contratantes", pide="fechas, contrataciones, entradas y obra disponible",
    pilar="como-usar-ia-siendo-artista",
    ciudades=["ciudad-de-mexico", "guadalajara", "monterrey", "tulum", "merida", "puebla", "queretaro", "playa-del-carmen", "cancun"]),
 "distribucion": dict(nombre="Distribución", plural="distribuidoras", uno="una distribuidora", tu="tu distribuidora",
    cliente="clientes", pide="pedidos, disponibilidad, listas de productos y estado de entregas",
    pilar="como-usar-ia-en-una-distribuidora",
    ciudades=["monterrey", "guadalajara", "ciudad-de-mexico", "queretaro", "puebla", "leon", "merida", "cancun", "tulum"]),
}

TEMAS = ["chatbot", "ia", "clientes"]


def titulo(t, r, c):
    if t == "chatbot":
        return f"Mejores chatbots de WhatsApp para {r['plural']} en {c} 2027: cómo elegir"
    if t == "ia":
        return f"IA para {r['plural']} en {c}: guía 2027"
    return f"Cómo conseguir clientes para {r['tu']} en {c} en 2027"


def slug(t, rk, cs):
    base = {"chatbot": "mejores-chatbots-whatsapp", "ia": "ia-para", "clientes": "conseguir-clientes"}[t]
    return f"{base}-{rk}-{cs}-2027"


def respuesta(t, r, c):
    if t == "chatbot":
        return (f"El mejor chatbot de WhatsApp para {r['plural']} en {c} en 2027 es el que contesta en minutos, a cualquier hora, "
                f"con la información que tú aprobaste ({r['pide']}), pasa a una persona lo que no sabe resolver y deja cada conversación "
                f"guardada en un CRM a nombre del negocio. No hay una marca que sea la mejor para todos: hay cinco criterios para comparar, "
                f"y abajo están en orden.")
    if t == "ia":
        return (f"En 2027 la IA le sirve a {r['uno']} en {c} para cinco cosas: volver a vender a quien ya te conoce, encontrar clientes nuevos "
                f"antes que tu competencia, mostrarte con constancia en redes, contestar a cualquier hora y sacar del día a día el trabajo "
                f"que se repite. Conviene empezar por una sola, la que más pesa en tu operación, y medirla unas semanas antes de sumar la siguiente.")
    return (f"Para conseguir clientes para {r['tu']} en {c} en 2027 hace falta, en este orden: que te encuentren en Google y en los "
            f"buscadores con IA con una web propia, contestar cada mensaje en minutos, volver a escribirle a quien ya preguntó y no compró, "
            f"y buscar tú a los clientes grandes antes de que ellos busquen a otro. La mayoría de los negocios chicos todavía no hace lo primero, "
            f"y ahí está la ventaja.")


def criterios(t, r, c):
    if t == "chatbot":
        return [
            ("Velocidad de respuesta, de día y de noche", f"Mide cuánto tarda en contestar un mensaje que llega a las 11 de la noche. Un interesado que espera hasta el otro día ya les escribió a otros {r['plural']} de {c}. Harvard Business Review encontró que las empresas que respondían a un contacto en la primera hora tenían muchas más probabilidades de calificarlo que las que tardaban más.{{{{hbr}}}}"),
            ("Contesta con tu información, no inventa", f"Pide ver qué responde ante preguntas de {r['pide']}. Debe usar solo lo que tú cargaste y decir «te paso con el equipo» cuando no sabe."),
            ("Pasa a una persona en el momento justo", f"Un buen chatbot no retiene a nadie. Detecta la queja, el caso especial o el cliente listo para cerrar y lo deriva a tu equipo con el contexto de la conversación."),
            ("Cada conversación queda en tu CRM", "Si los chats viven solo en un teléfono, cuando alguien del equipo se va, se van sus contactos. Los datos tienen que quedar a nombre del negocio y exportables."),
            ("Respeta las reglas de WhatsApp y de datos", f"Fuera de la ventana de 24 horas solo se puede escribir con plantillas aprobadas y con permiso del cliente.{{{{meta}}}} En México, además, rige la ley de protección de datos personales de 2025.{{{{lfpd}}}}"),
        ]
    if t == "ia":
        return [
            ("Despertar datos dormidos", f"Los {r['cliente']} que ya te escribieron o compraron son una lista. Ordenada, se les invita a volver en el momento justo."),
            ("Prospectar antes que tu competencia", f"Encontrar en {c} a quien necesita lo que haces y escribirle primero, con una propuesta que habla de su caso."),
            ("Confianza en redes", "Se compra a quien se conoce. Publicar con constancia lo que haces y cómo lo haces hace que te elijan antes de probarte."),
            ("Presencia a cualquier hora", f"Contestar {r['pide']} al instante, también fuera de horario y en el idioma de quien escribe."),
            ("Menos trabajo repetitivo", "Recordatorios, confirmaciones y preguntas de siempre salen solos. El equipo queda para lo que solo hace una persona."),
        ]
    return [
        ("Que te encuentren en Google y en la IA", f"Cuando alguien en {c} pregunta a Google o a ChatGPT por {r['plural']}, la respuesta sale de las webs que pueden leer. Una web propia, rápida, con tu ficha de Google y datos claros es el punto de partida. En el Índice El Tío, 94 de cada 100 negocios chicos de cuatro estados de México no tenían una web registrada.{{{{ind}}}}"),
        ("Contestar en minutos", f"El cliente que escribe a tres {r['plural']} a la vez se queda con el primero que responde bien.{{{{hbr}}}}"),
        ("Volver a escribirle a quien ya preguntó", f"Muchos {r['cliente']} que no compraron la primera vez siguen buscando. Retomar el contacto cuesta mucho menos que conseguir uno nuevo."),
        ("Buscar tú a los clientes grandes", f"Empresas, agencias y organizadores de {c} que compran en volumen. Se encuentran con listas por zona y rubro y se les escribe por correo, Instagram o LinkedIn, nunca por WhatsApp en frío."),
        ("Medir cada semana", "Mensajes recibidos, tiempo de primera respuesta, clientes que volvieron y de dónde llegó cada venta. Lo que no se mide no se puede mejorar."),
    ]


def faqs(t, r, c, cs):
    base = [
        (f"¿El Tío trabaja con {r['plural']} en {c}?", f"Sí. Todo el trabajo es en línea, por chat, así que da igual en qué parte de {c} estés. Empiezas con el Audit gratis."),
        ("¿Qué es el Audit gratis?", f"Un cuestionario de 15 a 25 minutos sobre cómo trabaja hoy {r['tu']}. En 24 a 48 horas hábiles recibes un mapa con lo que conviene hacer primero y por qué. Queda tuyo, contrates o no."),
    ]
    if t == "chatbot":
        esp = [(f"¿Un chatbot de WhatsApp reemplaza a mi equipo?", "No. Contesta lo que se repite y pasa a tu equipo lo que necesita una persona. El equipo atiende mejor porque llega a la conversación con el contexto."),
               ("¿Puede escribirles primero a mis clientes por WhatsApp?", "Solo con una plantilla aprobada por WhatsApp y con permiso del cliente. Dentro de las 24 horas después de que el cliente te escribe, la conversación es libre.")]
    elif t == "ia":
        esp = [(f"¿Por dónde empieza {r['uno']} con IA?", f"Por la ventaja que más pesa en tu operación. En muchos {r['plural']} es contestar fuera de horario o volver a escribirle a quien ya te conoce."),
               ("¿Hace falta saber de tecnología?", "No. El equipo recibe todo instalado y aprende a operarlo. Lo que sí hace falta es decidir qué quieres lograr primero.")]
    else:
        esp = [(f"¿Conviene pagar anuncios para conseguir clientes en {c}?", "Primero conviene que la web, la ficha de Google y la respuesta a los mensajes estén en orden. Un anuncio que lleva a un chat que tarda en contestar se pierde."),
               ("¿Cómo aparezco en ChatGPT y en Google?", "Con una web propia que los buscadores puedan leer, datos claros del negocio y una ficha de Google completa. No se puede prometer aparecer: se mide cada mes con una lista fija de preguntas.")]
    return esp + base


def wa(txt):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(txt)


def refs(txt, orden):
    def f(m):
        k = m.group(1)
        if k not in orden:
            orden.append(k)
        return f'<a class="ref" href="#f{orden.index(k) + 1}">[{orden.index(k) + 1}]</a>'
    return re.sub(r"\{\{(\w+)\}\}", f, txt)


def pagina(t, rk, cs, todas):
    r, c = R[rk], CIUDAD[cs]
    s = slug(t, rk, cs)
    ruta = f"/guias/2027/{s}/"
    tit = titulo(t, r, c)
    resp = respuesta(t, r, c)
    desc = resp[:155].rsplit(" ", 1)[0] + "…"
    orden = []
    crit = criterios(t, r, c)
    fq = faqs(t, r, c, cs)
    ctx = [f"Las empresas grandes ya se movieron: en la encuesta global de McKinsey publicada en noviembre de 2025, 88 % de las organizaciones dijo usar IA de forma habitual en al menos una función del negocio.{{{{mck}}}} Entre los negocios chicos, en cambio, la mayoría todavía no empezó. Quien da el paso en {c} en 2027 queda adelante de su zona."]
    if rk == "hospitality" and cs in CARIBE:
        ctx.append("El aeropuerto de Cancún movió 29,345,538 pasajeros en 2025, y 19,464,554 fueron internacionales.{{asur}} Muchos de esos viajeros escriben desde otro huso horario y en otro idioma, y reservan donde les contestan primero.")
    h = [f"  <article>", f"    <h1>{e(tit)}</h1>",
         f'    <p class="bajada"><strong>{e(resp)}</strong></p>',
         f'    <p class="fecha">Actualizada el 7 de noviembre de 2026 · guía para 2027</p>',
         '    <h2 id="contexto">Por qué importa en 2027</h2>']
    h += [f"    <p>{refs(x, orden)}</p>" for x in ctx]
    h.append('    <h2 id="criterios">Criterios para comparar</h2>')
    h.append('    <ol class="lista">' + "".join(f"<li><strong>{e(a)}.</strong> {refs(b, orden)}</li>" for a, b in crit) + "</ol>")
    h.append('    <h2 id="uso">Cómo usarlos</h2>')
    uso = {"chatbot": f"Pon a prueba cada opción con tres mensajes reales de tus {r['cliente']}, uno de día, uno de noche y uno complicado, y anota qué pasó con cada criterio. La opción que cumple los cinco es la mejor para {r['tu']}, aunque no sea la más conocida.",
           "ia": f"No hace falta tomar las cinco. Elige la que más pesa hoy en {r['tu']}, ponla en marcha y mídela cuatro semanas. Si mueve el número que te importa, suma la siguiente.",
           "clientes": f"Revisa los cinco puntos en orden. Si el primero falla, los demás rinden menos: un cliente que no te encuentra en {c} no llega a escribirte."}[t]
    h.append(f"    <p>{e(uso)}</p>")
    h.append('    <h2 id="preguntas">Preguntas frecuentes</h2>')
    h += [f"    <h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in fq]
    audit = f"https://app.eltio.net/auditoria/{rk}"
    h.append(f"""    <section class="cierre" id="empezar">
      <h2>Por dónde empezar</h2>
      <p>El Audit gratis de El Tío mira cómo trabaja hoy {e(r['tu'])} y te dice qué ventaja tomar primero. Es un cuestionario de 15 a 25 minutos y el mapa llega en 24 a 48 horas hábiles.</p>
      <p><strong>No pierdas la ventaja, es hoy. Habla con El Tío.</strong></p>
      <div class="acciones">
        <a class="btn" data-cta="audit" href="{audit}">Hacer el Audit gratis</a>
        <a class="enlace" data-cta="whatsapp" href="{e(wa(f'Hola! Leí la guía 2027 para {r["plural"]} en {c} y quiero el Audit de mi negocio.'))}">Escribir por WhatsApp</a>
      </div>
    </section>""")
    rel = [(f"/negocios/{cs}/{rk}/", f"{r['nombre']} en {c}"), (f"/guias/{r['pilar']}/", "La guía a fondo del rubro"),
           ("/ventaja/", "Calcula tu ventaja"), (f"/{rk}/", f"{r['nombre']}: la página del rubro")]
    otras = [x for x in todas if x[1] == rk and x[2] != cs][:2] + [x for x in todas if x[2] == cs and x[1] != rk][:2]
    rel += [(f"/guias/2027/{slug(*x)}/", titulo(x[0], R[x[1]], CIUDAD[x[2]])) for x in otras]
    h.append('    <nav class="relacionado" aria-label="Para seguir">\n      <p>Para seguir</p>\n      <ul>' +
             "".join(f'<li><a href="{u}">{e(n)}</a></li>' for u, n in rel) + "</ul>\n    </nav>")
    h.append('    <section class="fuentes" aria-labelledby="fuentes-t">\n      <h2 id="fuentes-t">Fuentes</h2>\n      <ol>' +
             "".join(f'<li id="f{i + 1}">{FUENTES[k][0]} <a href="{FUENTES[k][1]}">{FUENTES[k][1]}</a></li>' for i, k in enumerate(orden)) +
             "</ol>\n    </section>\n  </article>")
    l_m, h_m = migas([("El Tío", "/"), ("Guías", "/guias/"), ("Guías 2027", "/guias/2027/"), (f"{r['nombre']} en {c}", ruta)])
    l_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}
    l_art = {"@context": "https://schema.org", "@type": "Article", "headline": tit, "description": resp,
             "datePublished": "2026-11-07", "dateModified": HOY, "inLanguage": "es-MX", "url": BASE + ruta,
             "author": {"@type": "Organization", "name": "El Tío", "url": BASE},
             "publisher": {"@type": "Organization", "name": "El Tío", "url": BASE},
             "about": [{"@type": "Place", "name": c}], "mainEntityOfPage": BASE + ruta}
    cuerpo = h_m + "\n" + "\n".join(h)
    return ruta, tit, documento(ruta, tit, desc, "es-MX", f"og-{rk}.jpg", [l_art, l_faq, l_m], cuerpo)


def combos():
    out = []
    for rk, r in R.items():
        for i, cs in enumerate(r["ciudades"]):
            out.append((TEMAS[i % 3], rk, cs))
    # Pedidos explícitos del fundador (07/11) que la rotación no cubre.
    out += [x for x in [("ia", "gastronomia", "ciudad-de-mexico"), ("clientes", "real-estate", "monterrey")] if x not in out]
    return out


def indice(lista):
    ruta = "/guias/2027/"
    tit = "Guías 2027 por rubro y ciudad"
    desc = "Guías 2027 de El Tío para negocios de México: chatbots de WhatsApp, IA y cómo conseguir clientes, por rubro y ciudad."
    l_m, h_m = migas([("El Tío", "/"), ("Guías", "/guias/"), ("Guías 2027", ruta)])
    grupos = ""
    for rk, r in R.items():
        items = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for u, t, k in lista if k == rk)
        grupos += f"    <h2>{e(r['nombre'])}</h2>\n    <ul>{items}</ul>\n"
    cuerpo = f"""{h_m}
  <article>
    <h1>{tit}</h1>
    <p class="bajada">Cada guía responde una pregunta concreta de un rubro en una ciudad, con criterios para comparar y fuentes. Si quieres saber qué le conviene a tu negocio, el Audit es gratis.</p>
{grupos}    <p><a class="btn" data-cta="audit" href="https://app.eltio.net/auditoria">Hacer el Audit gratis</a> · <a href="/ventaja/">Calcula tu ventaja</a></p>
  </article>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": tit, "url": BASE + ruta}
    return ruta, documento(ruta, tit, desc, "es-MX", "og-portada.jpg", [ld, l_m], cuerpo)


def main():
    todas = combos()
    paginas, lista = [], []
    for x in todas:
        ruta, tit, doc = pagina(*x, todas)
        paginas.append((ruta, doc)); lista.append((ruta, tit, x[1]))
    paginas.insert(0, indice(lista))
    for ruta, doc in paginas:
        for malo in ("—", "USD", "$", "llamada"):
            if malo in re.sub(r"<script.*?</script>", "", doc, flags=re.S).replace("$(", ""):
                raise SystemExit(f"{malo!r} en {ruta}")
        d = os.path.join(RAIZ, ruta.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(doc)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{BASE}{r}</loc><lastmod>{HOY}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>" for r, _ in paginas]
    sm.append("</urlset>")
    open(os.path.join(RAIZ, "sitemap-2027.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")
    si = os.path.join(RAIZ, "sitemap-index.xml"); x = open(si, encoding="utf-8").read()
    if "sitemap-2027.xml" not in x:
        x = x.replace("</sitemapindex>", "  <sitemap><loc>https://eltio.net/sitemap-2027.xml</loc></sitemap>\n</sitemapindex>")
        open(si, "w", encoding="utf-8", newline="\n").write(x)
    lt = os.path.join(RAIZ, "llms.txt"); x = open(lt, encoding="utf-8").read()
    bloque = "<!-- guias 2027 -->\n## Guias 2027 por rubro y ciudad\n\n- Indice: https://eltio.net/guias/2027/\n" + \
             "".join(f"- {t}: {BASE}{r}\n" for r, t, _ in lista) + "<!-- fin guias 2027 -->\n"
    x = re.sub(r"<!-- guias 2027 -->.*?<!-- fin guias 2027 -->\n", "", x, flags=re.S)
    x = x.replace("<!-- fin otros idiomas -->", "<!-- fin otros idiomas -->\n\n" + bloque) if "<!-- fin otros idiomas -->" in x else x + "\n" + bloque
    open(lt, "w", encoding="utf-8", newline="\n").write(x)
    print(f"{len(paginas)} páginas (índice + {len(lista)} guías)")


if __name__ == "__main__":
    main()
