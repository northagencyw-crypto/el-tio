# -*- coding: utf-8 -*-
"""Genera 5 guías SEO por búsqueda (21/11/2026). Solo español. Uso: python generador/guias_busqueda.py"""
import json, html, pathlib, re, urllib.parse

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FECHA = "2026-11-21"
FECHA_TXT = "21 de noviembre de 2026"
WA = "https://wa.me/525568976898?text="
IG = "https://ig.me/m/eltio.ia"

F = {
 "wa_precios": ("Meta, «Pricing on the WhatsApp Business Platform», documentación para desarrolladores: ventana de atención de 24 horas, mensajes con plantilla y permiso del usuario.", "https://developers.facebook.com/docs/whatsapp/pricing"),
 "wa_politica": ("WhatsApp, «Política de mensajería de WhatsApp Business».", "https://whatsappbusiness.com/es-la/policy/"),
 "wa_api": ("Meta, «WhatsApp Cloud API», documentación para desarrolladores.", "https://developers.facebook.com/docs/whatsapp/cloud-api"),
 "lfpdppp": ("Ley Federal de Protección de Datos Personales en Posesión de los Particulares, Diario Oficial de la Federación, 20 de marzo de 2025. Texto vigente en la Cámara de Diputados.", "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf"),
 "ig_api": ("Meta, «Messenger Platform: Instagram», documentación para desarrolladores: cuenta profesional, ventana de 24 horas y etiqueta de agente humano.", "https://developers.facebook.com/docs/messenger-platform/instagram"),
 "oai_search": ("OpenAI, «ChatGPT search», Centro de ayuda: cómo ChatGPT busca en la web y cita fuentes.", "https://help.openai.com/en/articles/9237897-chatgpt-search"),
 "oai_bots": ("OpenAI, «Overview of OpenAI Crawlers»: OAI-SearchBot, GPTBot y ChatGPT-User, y cómo controlarlos con robots.txt.", "https://platform.openai.com/docs/bots"),
 "gbp_rank": ("Google, «Consejos para mejorar tu posicionamiento local en Google», Ayuda de Perfil de Empresa: relevancia, distancia y prominencia.", "https://support.google.com/business/answer/7091"),
 "bing_places": ("Microsoft, Bing Places for Business.", "https://www.bingplaces.com/"),
 "g_localbiz": ("Google Search Central, «Datos estructurados de empresa local (LocalBusiness)».", "https://developers.google.com/search/docs/appearance/structured-data/local-business"),
 "g_mobile": ("Google Search Central, «Prácticas recomendadas de indexación mobile-first».", "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"),
 "g_cwv": ("Google Search Central, «Métricas web esenciales (Core Web Vitals) y los resultados de búsqueda».", "https://developers.google.com/search/docs/appearance/core-web-vitals"),
 "lfpc": ("Ley Federal de Protección al Consumidor, artículo 7 Bis: obligación de informar el precio total. Texto vigente en la Cámara de Diputados.", "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPC.pdf"),
 "nom247": ("Secretaría de Economía, NOM-247-SE-2021, «Prácticas comerciales. Requisitos de la información comercial y la publicidad de bienes inmuebles destinados a casa habitación». Consulta en Profeco.", "https://www.gob.mx/profeco"),
}

G = {}  # slug -> datos

G["chatbot-whatsapp-restaurantes"] = dict(
 titulo="Chatbot de WhatsApp para restaurantes: cómo elegir uno que sí reserve",
 corto="Chatbot de WhatsApp para restaurantes",
 desc="Qué tiene que hacer un chatbot de WhatsApp para un restaurante en México, la diferencia entre la app y la API, y las preguntas que conviene hacerle a cualquier proveedor antes de contratar.",
 rubro=("Gastronomía", "/gastronomia/"), audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de chatbot de WhatsApp para restaurantes y quiero el Audit de mi restaurante.",
 bajada="Un viernes a las ocho de la noche nadie en tu restaurante tiene tiempo de contestar WhatsApp. Justo a esa hora alguien pregunta si hay mesa para cuatro, y si no le contestas, reserva en el de al lado. Esta guía no te vende un chatbot: te dice qué tiene que hacer uno bueno y qué preguntar antes de pagar por él.",
 cuerpo=[
  ("que-hace", "Lo que tiene que resolver", """
<p>Un chatbot de restaurante sirve si cierra la conversación, no si solo saluda. Las consultas que llegan por WhatsApp a casi cualquier restaurante son las mismas: si hay mesa, a qué hora abren, dónde estacionarse, si tienen opción sin gluten, cuánto tarda un pedido para llevar y si aceptan grupos.</p>
<p>La prueba es simple. Escríbele al chatbot como lo haría un cliente con hambre y prisa. Si al tercer mensaje no tienes una reserva confirmada o una persona del equipo enterada, no está haciendo su trabajo.</p>
<div class="tabla"><table><thead><tr><th>Lo que pide el cliente</th><th>Lo que debe hacer el chatbot</th></tr></thead><tbody>
<tr><td>Mesa para hoy</td><td>Ver la disponibilidad real y reservar, o tomar los datos y avisar al encargado</td></tr>
<tr><td>Menú y alergias</td><td>Mandar el menú vigente y responder con lo que el restaurante cargó, sin adivinar</td></tr>
<tr><td>Pedido para llevar</td><td>Tomar el pedido completo y pasarlo a cocina o a tu sistema</td></tr>
<tr><td>Evento o grupo grande</td><td>Pedir fecha, personas y presupuesto, y pasarlo a una persona</td></tr>
<tr><td>Queja</td><td>Pasar a una persona siempre</td></tr>
</tbody></table></div>"""),
  ("app-o-api", "WhatsApp Business app o API", """
<p>La app gratuita de WhatsApp Business sirve para respuestas rápidas, horario y mensaje de ausencia. No conecta un agente de IA que entienda lo que escribe el cliente. Para eso se usa la plataforma de WhatsApp Business, la API, a través de un proveedor o directamente con Meta.<a class="ref" href="#f1">[1]</a></p>
<p>Con la API, cada mensaje del cliente abre una ventana de 24 horas en la que contestas libremente. Para escribirle fuera de esa ventana, por ejemplo para recordar la reserva del sábado, necesitas una plantilla aprobada y que el cliente haya aceptado recibir tus mensajes.<a class="ref" href="#f2">[2]</a> Todo eso tiene que cumplir la política de mensajería de WhatsApp Business.<a class="ref" href="#f3">[3]</a></p>
<div class="aviso">En la práctica: el recordatorio de reserva es la plantilla que más se usa en un restaurante. Pide el permiso en el mismo chat donde se confirma la mesa.</div>"""),
  ("preguntas-proveedor", "Seis preguntas para cualquier proveedor", """
<ol class="lista">
<li><strong>¿Reserva de verdad o solo toma datos?</strong> Pregunta con qué sistema de reservas se conecta. Si no se conecta con ninguno, va a anotar y alguien tiene que confirmar.</li>
<li><strong>¿Qué pasa cuando no sabe algo?</strong> La respuesta correcta es que pasa la conversación a una persona y no inventa.</li>
<li><strong>¿Quién carga el menú y los horarios?</strong> Si cambias el menú del día, alguien tiene que actualizarlo. Pregunta cómo y en cuánto tiempo.</li>
<li><strong>¿El número sigue siendo tuyo?</strong> El número y la lista de clientes tienen que quedar a nombre del restaurante.</li>
<li><strong>¿Dice que es un asistente?</strong> Conviene que se presente como asistente y no finja ser una persona.</li>
<li><strong>¿Qué reporte recibes?</strong> Cuántas conversaciones, cuántas reservas y cuántas pasaron a una persona, cada semana.</li>
</ol>"""),
  ("datos", "Datos de tus clientes", """
<p>Nombre, teléfono y la fecha de la reserva son datos personales. En México los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f4">[4]</a> Lo básico es tener un aviso de privacidad a la mano y usar los datos solo para lo que le dijiste al cliente. Esta guía no reemplaza a un abogado.</p>"""),
  ("ejemplo", "Cómo se ve una conversación", """
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 20:12</span>
<span class="yo">Hola, ¿tienen mesa para 4 a las 9?</span>
<span class="bot">¡Hola! Sí, tengo una mesa para 4 a las 21:00 en terraza o a las 21:30 adentro. ¿Cuál prefieres?</span>
<span class="yo">Terraza. Uno de nosotros es celíaco.</span>
<span class="bot">Listo, quedó a tu nombre a las 21:00 en terraza. Le aviso a cocina. Soy un asistente con IA; si necesitas algo más, alguien del equipo te contesta.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>
<p>Si buscas el detalle de cómo funciona en la capital, con colonias, horarios pico y sistemas de reserva, está en la guía de <a href="/guias/chatbot-whatsapp-restaurantes-ciudad-de-mexico/">chatbot de WhatsApp para restaurantes en Ciudad de México</a>.</p>"""),
 ],
 faq=[
  ("¿Puedo usar la app gratuita de WhatsApp Business como chatbot?", "Sirve para respuestas rápidas y mensaje de ausencia, pero no para un agente que entienda lo que escribe el cliente y reserve. Para eso se usa la plataforma de WhatsApp Business (API)."),
  ("¿El chatbot puede mandar recordatorios de reserva?", "Sí, con una plantilla aprobada por Meta y con el permiso del cliente, que conviene pedir en el mismo chat donde se confirma la mesa."),
  ("¿Qué pasa si el cliente pregunta algo que el chatbot no sabe?", "Un buen chatbot pasa la conversación a una persona del equipo y no inventa la respuesta."),
  ("¿Necesito cambiar de número?", "No necesariamente. Lo importante es que el número y la lista de clientes queden a nombre del restaurante."),
 ],
 fuentes=["wa_api", "wa_precios", "wa_politica", "lfpdppp"],
)

G["como-aparecer-en-chatgpt-negocio-en-tu-ciudad"] = dict(
 titulo="Cómo aparecer cuando le preguntan a ChatGPT por un negocio en tu ciudad",
 corto="Aparecer en ChatGPT en tu ciudad",
 desc="Qué mira ChatGPT cuando alguien pregunta por «el mejor restaurante en Monterrey» o «un gimnasio en la Roma», y los pasos para que tu negocio aparezca en Ciudad de México, Guadalajara, Monterrey o Tulum.",
 rubro=("Posicionamiento en IA", "/posicionamiento-en-ia/"), audit="", og="og-portada.jpg",
 wa="Hola! Leí la guía de cómo aparecer en ChatGPT en mi ciudad y quiero el Audit de mi negocio.",
 bajada="Cada vez más gente no busca «restaurante Monterrey» en Google. Le pregunta a ChatGPT «¿dónde como cabrito bueno en Monterrey?» y va al primero que le nombra. Si tu negocio no aparece, no perdiste un clic: perdiste al cliente. Esta guía explica qué mira ChatGPT en una búsqueda local y qué hacer para estar en esa respuesta.",
 cuerpo=[
  ("como-busca", "Cómo arma ChatGPT una respuesta local", """
<p>Cuando la pregunta necesita información actual, ChatGPT busca en la web y muestra las fuentes que usó.<a class="ref" href="#f1">[1]</a> Para eso usa proveedores de búsqueda externos y su propio rastreador, OAI-SearchBot.<a class="ref" href="#f2">[2]</a> En una pregunta local, eso significa que lee directorios, mapas, reseñas y páginas de negocios que mencionan la ciudad y la colonia.</p>
<p>La consecuencia práctica: ChatGPT no te conoce porque existas. Te conoce si hay texto público y claro que diga qué haces, dónde estás y qué opinan tus clientes.</p>"""),
  ("ciudad", "La ciudad tiene que estar escrita", """
<p>Las preguntas locales casi siempre nombran un lugar: «en la Condesa», «en San Pedro», «cerca de la Quinta Avenida». Si tu sitio dice solo «somos el mejor gimnasio», no hay nada que conecte tu negocio con esa pregunta.</p>
<ul>
<li>Escribe la ciudad y la colonia en el título de tu página principal y en el primer párrafo.</li>
<li>Usa el mismo nombre, dirección y teléfono en tu sitio, tu Perfil de Empresa, Instagram y cualquier directorio.</li>
<li>Si atiendes varias zonas, una página por zona con contenido propio, no la misma página con otro nombre.</li>
</ul>"""),
  ("perfiles", "Perfil de Empresa en Google y Bing Places", """
<p>Google ordena los resultados locales por relevancia, distancia y prominencia, y la prominencia incluye las reseñas y lo que se dice de tu negocio en la web.<a class="ref" href="#f3">[3]</a> Completa el Perfil con categoría exacta, horario, fotos reales y respuestas a las reseñas.</p>
<p>Da de alta también tu negocio en Bing Places.<a class="ref" href="#f4">[4]</a> Es gratis, tarda poco y es la ficha local del buscador de Microsoft, que alimenta a Copilot.</p>"""),
  ("robots", "Deja entrar a los buscadores de IA", """
<p>Revisa el archivo robots.txt de tu sitio. Si bloquea a OAI-SearchBot, tu sitio no aparece en las respuestas de búsqueda de ChatGPT.<a class="ref" href="#f2">[2]</a> Muchos sitios lo bloquean sin saberlo, por una plantilla o un plugin de seguridad.</p>
<p>Suma datos estructurados de empresa local (LocalBusiness) con tu dirección, horario y teléfono.<a class="ref" href="#f5">[5]</a> Le dicen a cualquier buscador, de forma ordenada, lo que tu página ya dice en texto.</p>"""),
  ("resenas", "Reseñas que nombran lo que vendes", """
<p>Una reseña que dice «excelente» ayuda poco. Una que dice «el mejor brunch de la Roma, el pan de masa madre vale la pena» le da a cualquier buscador las palabras que la gente pregunta. No escribas reseñas falsas ni las pagues: pide a tus clientes contentos que cuenten qué pidieron y dónde.</p>"""),
  ("probar", "Cómo saber si ya apareces", """
<ol class="lista">
<li>Abre ChatGPT con búsqueda activada y pregunta como lo haría un cliente: rubro, ciudad y colonia.</li>
<li>Repite con dos o tres formas distintas de preguntar y anota si apareces y qué fuente cita.</li>
<li>Haz lo mismo en Copilot y en Google. Repite cada mes.</li>
</ol>
<p>Si quieres el detalle técnico de cada paso, con llms.txt e idiomas, está en la guía de <a href="/guias/como-aparecer-en-chatgpt-y-google-negocio-pequeno/">cómo aparecer en ChatGPT y en Google si tienes un negocio pequeño</a>.</p>"""),
 ],
 faq=[
  ("¿ChatGPT busca en internet para responder sobre negocios locales?", "Sí. Cuando la pregunta necesita información actual, ChatGPT busca en la web y muestra las fuentes que usó."),
  ("¿Puedo pagar para aparecer en ChatGPT?", "No hay un lugar pagado en las respuestas de búsqueda de ChatGPT. Aparecer depende de que haya información pública y clara sobre tu negocio."),
  ("¿Qué es OAI-SearchBot?", "Es el rastreador que usa OpenAI para la búsqueda de ChatGPT. Si tu robots.txt lo bloquea, tu sitio no aparece en esas respuestas."),
  ("¿Sirve tener solo Instagram?", "Ayuda, pero no alcanza. Conviene tener Perfil de Empresa en Google, Bing Places y una página propia que diga en texto qué haces y en qué ciudad."),
 ],
 fuentes=["oai_search", "oai_bots", "gbp_rank", "bing_places", "g_localbiz"],
)

G["reservas-automaticas-instagram-hoteles-boutique"] = dict(
 titulo="Reservas automáticas por Instagram para hoteles boutique",
 corto="Reservas por Instagram para hoteles boutique",
 desc="Cómo convertir los DMs de Instagram de un hotel boutique en reservas a cualquier hora y en dos idiomas, qué permite la API de Instagram y cómo evitar la sobreventa.",
 rubro=("Hospitality", "/hospitality/"), audit="hospitality", og="og-hospitality.jpg",
 wa="Hola! Leí la guía de reservas por Instagram para hoteles boutique y quiero el Audit de mi hotel.",
 bajada="En un hotel boutique, Instagram es la vitrina. Las fotos de la alberca hacen el trabajo y el huésped escribe por DM: «¿precio para el puente de diciembre?». Si la respuesta llega al día siguiente, ya reservó en Booking. Esta guía explica cómo responder y reservar desde el DM sin perder el toque del hotel.",
 cuerpo=[
  ("por-que", "Por qué el DM es el mejor canal directo", """
<p>Quien escribe por Instagram ya vio tus fotos y le gustó lo que vio. Es el huésped más caliente que tienes, y llega sin comisión de plataforma. El problema es el horario: los DMs llegan de noche, los fines de semana y desde otros países.</p>"""),
  ("api", "Qué permite Instagram", """
<p>Para automatizar los mensajes, la cuenta tiene que ser profesional y conectarse a la API de mensajes de Instagram, a través de Meta o de un proveedor.<a class="ref" href="#f1">[1]</a> Desde ahí un agente puede contestar los DMs y las respuestas a tus historias.</p>
<p>La regla clave es la ventana de 24 horas: puedes contestar libremente durante las 24 horas siguientes al último mensaje del huésped. Pasado ese plazo, solo una persona del equipo puede seguir la conversación, con la etiqueta de agente humano, hasta siete días.<a class="ref" href="#f1">[1]</a> Por eso conviene que el agente pida el WhatsApp o el correo del huésped dentro de la primera conversación.</p>"""),
  ("flujo", "El flujo de una reserva desde el DM", """
<div class="tabla"><table><thead><tr><th>Paso</th><th>Qué hace el agente</th></tr></thead><tbody>
<tr><td>Consulta</td><td>Pregunta fechas, personas y tipo de habitación, en el idioma del huésped</td></tr>
<tr><td>Disponibilidad</td><td>Lee el channel manager o el sistema del hotel. Si no está conectado, no confirma</td></tr>
<tr><td>Tarifa</td><td>Responde con la tarifa directa y lo que incluye</td></tr>
<tr><td>Anticipo</td><td>Envía el enlace de pago con la política de cancelación escrita</td></tr>
<tr><td>Contacto</td><td>Guarda nombre, idioma y WhatsApp en el CRM para antes de la llegada</td></tr>
</tbody></table></div>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">Instagram · 23:48</span>
<span class="yo">Hi! Price for a double room Dec 20 to 23?</span>
<span class="bot">Hi! For those dates I have the garden suite. I can send you the direct rate and the deposit link. Shall I? I'm the hotel's AI assistant.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("sobreventa", "La regla que no se rompe: no vender la misma noche dos veces", """
<p>Un agente que confirma sin leer la disponibilidad real es peor que no tener agente. En temporada alta, una sobreventa cuesta más que cualquier comisión. Si tu sistema no se conecta, el agente toma la solicitud y avisa que alguien la confirma en minutos.</p>"""),
  ("datos", "Datos del huésped", """
<p>Nombre, fechas y datos de pago son datos personales y en México los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f2">[2]</a> Ten tu aviso de privacidad enlazado en el mismo chat donde pides los datos.</p>
<p>Si además quieres que el huésped vuelva sin pasar por la plataforma, sigue con la guía de <a href="/guias/reservas-directas-whatsapp-hoteles/">reservas directas por WhatsApp para hoteles</a>.</p>"""),
 ],
 faq=[
  ("¿Se pueden automatizar los DMs de Instagram de un hotel?", "Sí, con una cuenta profesional conectada a la API de mensajes de Instagram, a través de Meta o de un proveedor."),
  ("¿Hasta cuándo puede contestar el agente?", "Durante las 24 horas siguientes al último mensaje del huésped. Después, solo una persona del equipo puede seguir, hasta siete días, con la etiqueta de agente humano."),
  ("¿El agente puede confirmar la reserva solo?", "Solo si lee la disponibilidad real del channel manager o del sistema del hotel. Si no, toma la solicitud y una persona confirma."),
  ("¿Contesta en inglés?", "Sí. Responde en el idioma en que escribe el huésped y guarda ese idioma en su contacto."),
 ],
 fuentes=["ig_api", "lfpdppp"],
)

G["responder-dms-instagram-automaticamente-gimnasios"] = dict(
 titulo="Cómo responder DMs de Instagram automáticamente en un gimnasio",
 corto="Responder DMs de Instagram en gimnasios",
 desc="Cómo contestar al instante los DMs de Instagram de un gimnasio o estudio, agendar la clase de prueba y no perder prospectos, con las reglas de la API de Instagram.",
 rubro=("Fitness", "/fitness/"), audit="fitness", og="og-fitness.jpg",
 wa="Hola! Leí la guía de DMs de Instagram para gimnasios y quiero el Audit de mi gimnasio.",
 bajada="Subes un reel del box lleno y llegan veinte DMs: «¿precio?», «¿horarios?», «¿tienen clase de prueba?». Tu coach está dando clase y los contesta a la noche, cuando la mitad ya se olvidó. Esta guía explica cómo responder cada DM al momento y llevar a esa persona a la clase de prueba.",
 cuerpo=[
  ("por-que", "Por qué se pierden los prospectos", """
<p>El que pregunta por DM está decidiendo hoy. Si la respuesta tarda horas, sigue mirando reels de otros gimnasios. En la mayoría de los estudios, los DMs los contesta quien tiene un rato libre, entre clase y clase. No es falta de ganas, es falta de manos.</p>"""),
  ("api", "Qué permite Instagram", """
<p>Para que un agente conteste los DMs, la cuenta tiene que ser profesional y conectarse a la API de mensajes de Instagram.<a class="ref" href="#f1">[1]</a> El agente puede contestar libremente durante las 24 horas siguientes al último mensaje de la persona. Después, solo alguien del equipo puede seguir, hasta siete días.<a class="ref" href="#f1">[1]</a></p>
<div class="aviso">En la práctica: el objetivo del primer DM no es vender la membresía. Es agendar la clase de prueba y guardar el WhatsApp para el recordatorio.</div>"""),
  ("respuestas", "Lo que conviene que conteste", """
<div class="tabla"><table><thead><tr><th>Lo que preguntan</th><th>Qué hace el agente</th><th>Cuándo pasa a una persona</th></tr></thead><tbody>
<tr><td>Precio</td><td>Responde con los planes que cargó el gimnasio y ofrece la clase de prueba</td><td>Planes corporativos o familiares</td></tr>
<tr><td>Horarios</td><td>Envía los horarios de la semana</td><td>Nunca</td></tr>
<tr><td>Clase de prueba</td><td>Agenda día y hora y pide el WhatsApp</td><td>Grupos llenos</td></tr>
<tr><td>Lesiones o salud</td><td>No opina: pasa a un coach</td><td>Siempre</td></tr>
<tr><td>Comentario en un reel con palabra clave</td><td>Abre el DM con la información pedida</td><td>Nunca</td></tr>
</tbody></table></div>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">Instagram · 07:05</span>
<span class="yo">Hola, cuánto cuesta y tienen clase de prueba?</span>
<span class="bot">¡Hola! Sí, la primera clase es de prueba. Hoy hay lugar a las 19:00 y mañana a las 7:00. ¿Cuál te late? Te paso los planes después de que entrenes. Soy el asistente con IA del gimnasio.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("despues", "Después de la clase de prueba", """
<p>La venta se cierra después de entrenar, no antes. Con el WhatsApp guardado, un recordatorio el día anterior y un mensaje al día siguiente preguntando cómo le fue hacen más que cualquier promoción. Para escribirle por WhatsApp fuera de la ventana de 24 horas necesitas una plantilla aprobada y su permiso.<a class="ref" href="#f2">[2]</a></p>
<p>Para retener a los socios que ya tienes, sigue con la guía de <a href="/guias/retencion-socios-gimnasio-reservas-clases/">retención de socios y reservas de clases</a>.</p>"""),
  ("datos", "Datos y salud", """
<p>Si el agente pregunta por lesiones o condiciones de salud, está tratando datos personales sensibles. La Ley Federal de Protección de Datos Personales en Posesión de los Particulares pide más cuidado con ellos.<a class="ref" href="#f3">[3]</a> Lo más simple: que el agente no los pregunte y pase esos temas a un coach.</p>"""),
 ],
 faq=[
  ("¿Se pueden responder los DMs de Instagram automáticamente?", "Sí, con una cuenta profesional conectada a la API de mensajes de Instagram. El agente contesta durante las 24 horas siguientes al último mensaje de la persona."),
  ("¿El agente puede agendar la clase de prueba?", "Sí. Ofrece los horarios disponibles, agenda la clase y pide el WhatsApp para el recordatorio."),
  ("¿Conviene que el agente diga el precio?", "Puede responder con los planes que cargó el gimnasio, pero lo que más convierte es llevar a la persona a la clase de prueba primero."),
  ("¿Qué pasa si alguien pregunta por una lesión?", "El agente no opina sobre salud y pasa la conversación a un coach."),
 ],
 fuentes=["ig_api", "wa_precios", "lfpdppp"],
)

G["pagina-web-inmobiliaria-monterrey"] = dict(
 titulo="Página web para inmobiliaria en Monterrey: qué necesita para traer clientes",
 corto="Página web para inmobiliaria en Monterrey",
 desc="Qué tiene que tener la página web de una inmobiliaria en Monterrey para aparecer en Google y en ChatGPT, mostrar propiedades por zona y convertir visitas en citas, con lo que pide la ley sobre precios.",
 rubro=("Real estate", "/real-estate/"), audit="real-estate", og="og-real-estate.jpg",
 wa="Hola! Leí la guía de página web para inmobiliaria en Monterrey y quiero el Audit de mi inmobiliaria.",
 bajada="En Monterrey, quien busca casa no busca «inmobiliaria». Busca «departamento en renta en San Pedro» o «casa en venta en Cumbres». Si tu página solo tiene el logo, un formulario y un enlace a los portales, ese cliente se lo lleva el portal. Esta guía explica qué necesita la página de una inmobiliaria regia para traer clientes propios.",
 cuerpo=[
  ("zonas", "Una página por zona", """
<p>La búsqueda inmobiliaria es por zona. San Pedro Garza García, Cumbres, Valle Oriente, Carretera Nacional, Santa Catarina o Apodaca son búsquedas distintas, con precios y compradores distintos. Una página por zona donde operas, con las propiedades de esa zona y un texto propio sobre ella, le da a Google y a ChatGPT algo concreto para responder.</p>
<p>No copies el mismo texto cambiando el nombre de la colonia. Escribe lo que sabes de esa zona: qué tipo de propiedades hay, para quién conviene y qué preguntan tus clientes.</p>"""),
  ("ficha", "Fichas de propiedad que se lean en el celular", """
<p>Google indexa la versión móvil de tu sitio.<a class="ref" href="#f1">[1]</a> Si la ficha de la propiedad no carga rápido en un celular, pierdes la visita y la posición.<a class="ref" href="#f2">[2]</a></p>
<ul>
<li>Fotos comprimidas y una galería que no tarde en abrir.</li>
<li>Precio, metros, recámaras, baños, estacionamientos y mantenimiento en texto, no dentro de una imagen.</li>
<li>Un botón de WhatsApp en cada ficha que diga qué propiedad le interesa al cliente.</li>
</ul>"""),
  ("ley", "Lo que pide la ley sobre el precio", """
<p>La Ley Federal de Protección al Consumidor obliga a informar el precio total.<a class="ref" href="#f3">[3]</a> Para la venta de vivienda, la NOM-247-SE-2021 fija requisitos de información comercial y publicidad de los inmuebles.<a class="ref" href="#f4">[4]</a> Antes de publicar precios y condiciones en tu sitio, revisa con tu abogado cómo te aplica.</p>"""),
  ("ia", "Que te encuentren también en ChatGPT", """
<p>Escribe en texto quién eres, en qué zonas de Monterrey operas y qué tipo de operación haces. Suma datos estructurados de empresa local con tu dirección y horario.<a class="ref" href="#f5">[5]</a> El paso a paso está en la guía de <a href="/guias/como-aparecer-en-chatgpt-negocio-en-tu-ciudad/">cómo aparecer en ChatGPT en tu ciudad</a>.</p>"""),
  ("leads", "De la visita a la cita", """
<p>La página trae el contacto. Lo que pasa después decide la venta: quién contesta el WhatsApp a las diez de la noche, quién agenda la visita y quién le escribe al que no volvió. Un agente que conteste al momento y un CRM que no deje a nadie sin seguimiento valen tanto como la página. Lo explicamos en la guía de <a href="/guias/crm-inmobiliaria-seguimiento-leads/">CRM para inmobiliarias</a>.</p>
<p>Si quieres ver cómo trabajamos en la ciudad, mira <a href="/ciudades/monterrey/">El Tío en Monterrey</a> y la página de <a href="/negocios/monterrey/real-estate/">inmobiliarias en Monterrey</a>.</p>"""),
 ],
 faq=[
  ("¿Qué tiene que tener la página web de una inmobiliaria?", "Páginas por zona, fichas de propiedad rápidas en el celular con los datos en texto, un botón de WhatsApp por propiedad y datos estructurados de empresa local."),
  ("¿Conviene una página por colonia en Monterrey?", "Sí, si operas ahí y escribes contenido propio de cada zona. Copiar el mismo texto cambiando el nombre no ayuda."),
  ("¿Tengo que publicar el precio de las propiedades?", "La Ley Federal de Protección al Consumidor pide informar el precio total, y la NOM-247-SE-2021 fija requisitos para la publicidad de vivienda. Revisa con tu abogado cómo te aplica."),
  ("¿Sirve si ya publico en los portales?", "Los portales traen visitas, pero el cliente queda en el portal. Tu página construye un canal propio que también aparece en Google y en ChatGPT."),
 ],
 fuentes=["g_mobile", "g_cwv", "lfpc", "nom247", "g_localbiz"],
)

ORDEN = list(G.keys())


def renum(cuerpo_html, fuentes):
    # convierte [n] locales ya escritos en orden de fuentes de la guía: se escribieron con el índice de la lista
    return cuerpo_html


def pagina(slug, d, pie):
    url = f"https://eltio.net/guias/{slug}/"
    audit = f"https://app.eltio.net/auditoria/{d['audit']}" if d["audit"] else "/posicionamiento-en-ia/#audit"
    wa = WA + urllib.parse.quote(d["wa"])
    article = {"@context": "https://schema.org", "@type": "Article", "headline": d["titulo"], "description": d["desc"],
               "inLanguage": "es-MX", "datePublished": FECHA, "dateModified": FECHA,
               "image": f"https://eltio.net/assets/{d['og']}",
               "author": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net"},
               "publisher": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net"},
               "mainEntityOfPage": url, "spatialCoverage": {"@type": "Place", "name": "México"}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    migas = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "El Tío", "item": "https://eltio.net/"},
        {"@type": "ListItem", "position": 2, "name": d["rubro"][0], "item": "https://eltio.net" + d["rubro"][1]},
        {"@type": "ListItem", "position": 3, "name": d["titulo"], "item": url}]}
    js = lambda o: json.dumps(o, ensure_ascii=False, indent=1)
    e = html.escape
    indice = "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t, _ in d["cuerpo"])
    cuerpo = "\n".join(f'<h2 id="{i}">{e(t)}</h2>{c}' for i, t, c in d["cuerpo"])
    faqh = "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in d["faq"])
    otras = "".join(f'<li><a href="/guias/{s}/">{e(G[s]["titulo"])}</a></li>' for s in ORDEN if s != slug)
    fuentes = "".join(f'<li id="f{n}">{e(F[k][0])} <a href="{F[k][1]}">{e(F[k][1].split("://")[1].rstrip("/"))}</a></li>'
                      for n, k in enumerate(d["fuentes"], 1))
    ig = f' · <a class="enlace" data-cta="instagram" href="{IG}">Escribir por DM en Instagram</a>'
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d['titulo'])} · El Tío</title>
<meta name="description" content="{e(d['desc'])}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#04070B">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_MX">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(d['titulo'])}">
<meta property="og:description" content="{e(d['desc'])}">
<meta property="og:image" content="https://eltio.net/assets/{d['og']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2304070B'/%3E%3Ctext x='16' y='23' font-family='monospace' font-size='19' font-weight='700' fill='%237FC9F2' text-anchor='middle'%3ET%3C/text%3E%3C/svg%3E">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-var.woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/guias/guias.css">
<script type="application/ld+json">
{js(article)}
</script>
<script type="application/ld+json">
{js(faq)}
</script>
<script type="application/ld+json">
{js(migas)}
</script>
<script src="/medicion.js" defer></script>
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
  <a class="marca" href="https://eltio.net/">EL TIO<span>.</span></a>
  <p class="estado"><i></i>EN LÍNEA</p>
</header>
<main id="contenido" class="guia">
  <nav class="migas" aria-label="Ruta"><a href="https://eltio.net">El Tío</a> / <a href="{d['rubro'][1]}">{e(d['rubro'][0])}</a> / Guía</nav>
  <article>
    <h1>{e(d['titulo'])}</h1>
    <p class="bajada">{e(d['bajada'])}</p>
    <p class="fecha">Actualizada el {FECHA_TXT}</p>
    <nav class="indice" aria-label="En esta guía"><p>En esta guía</p><ol>{indice}<li><a href="#preguntas">Preguntas frecuentes</a></li><li><a href="#empezar">Por dónde empezar</a></li></ol></nav>
{cuerpo}
    <h2 id="preguntas">Preguntas frecuentes</h2>
{faqh}
    <section class="cierre" id="empezar">
      <h2>Por dónde empezar</h2>
      <p>Antes de instalar nada, El Tío mira cómo trabaja hoy tu negocio: cuántos mensajes llegan, a qué hora, quién los contesta y cuántos se quedan sin respuesta. El Audit es gratis: un cuestionario de 15 a 25 minutos y, en 24 a 48 horas hábiles, el mapa de lo que conviene hacer primero. Si prefieres, escríbenos y lo vemos por chat.</p>
      <div class="acciones">
        <a class="btn" data-cta="audit" href="{audit}">Hacer el Audit gratis</a>
        <a class="enlace" data-cta="whatsapp" href="{wa}">Escribir por WhatsApp</a>{ig}
      </div>
    </section>
    <nav class="relacionado" aria-label="Para seguir">
      <p>Para seguir</p>
      <ul>
        <li><a href="{d['rubro'][1]}">{e(d['rubro'][0])}</a>: la página del rubro</li>
        {otras}
        <li><a href="/guias/">Todas las guías</a></li>
      </ul>
    </nav>
    <section class="fuentes" aria-labelledby="fuentes-t">
      <h2 id="fuentes-t">Fuentes</h2>
      <ol>{fuentes}</ol>
    </section>
  </article>
</main>
{pie}
</body>
</html>
"""


def main():
    ref = (RAIZ / "guias/reservas-directas-whatsapp-hoteles/index.html").read_text(encoding="utf-8")
    pie = ref[ref.index('<footer class="pie">'):ref.index("</footer>") + 9]
    for slug, d in G.items():
        out = pagina(slug, d, pie)
        assert "—" not in out, slug
        p = RAIZ / "guias" / slug
        p.mkdir(exist_ok=True)
        (p / "index.html").write_text(out, encoding="utf-8")
    # sitemap: solo suma las URL que falten, sin reescribir el resto
    sm = RAIZ / "sitemap.xml"
    txt = sm.read_text(encoding="utf-8")
    nuevas = ""
    for slug in ORDEN:
        u = f"https://eltio.net/guias/{slug}/"
        if f"<loc>{u}</loc>" not in txt:
            nuevas += f"  <url><loc>{u}</loc><lastmod>{FECHA}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
    if nuevas:
        txt = txt.replace("</urlset>", nuevas + "</urlset>")
        sm.write_text(txt, encoding="utf-8")
    print("ok", len(G), "sitemap +", nuevas.count("<url>"))


if __name__ == "__main__":
    main()
