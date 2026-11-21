# -*- coding: utf-8 -*-
"""Genera 11 guías SEO por búsqueda (21/11/2026). Solo español. Uso: python generador/guias_busqueda.py"""
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
 "nom247": ("Secretaría de Economía, NOM-247-SE-2021, «Prácticas comerciales. Requisitos de la información comercial y la publicidad de bienes inmuebles destinados a casa habitación y elementos mínimos que deben contener los contratos relacionados», Diario Oficial de la Federación, 22 de marzo de 2022.", "https://dof.gob.mx/nota_detalle.php?codigo=5646251&fecha=22/03/2022"),
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

F["g_resenas"] = ("Google, «Consejos para conseguir más reseñas», Ayuda de Perfil de Empresa: enlace o código QR para pedir reseñas y responderlas.", "https://support.google.com/business/answer/3474122?hl=es")
F["g_contenido"] = ("Google, «Contenido prohibido y restringido», Política de contenido aportado por usuarios de Maps: interacción falsa, incentivos y solicitud selectiva de reseñas.", "https://support.google.com/contributionpolicy/answer/7400114?hl=es")
F["g_responder"] = ("Google, «Leer y responder reseñas», Ayuda de Perfil de Empresa.", "https://support.google.com/business/answer/3474050?hl=es")
F["sch_gym"] = ("Schema.org, tipo «ExerciseGym».", "https://schema.org/ExerciseGym")
F["sch_rest"] = ("Schema.org, tipo «Restaurant»: propiedades acceptsReservations, menu y servesCuisine.", "https://schema.org/Restaurant")

G["chatbot-whatsapp-restaurantes-guadalajara"] = dict(
 titulo="Chatbot de WhatsApp para restaurantes en Guadalajara: reservas, pedidos y fin de semana",
 corto="Chatbot de WhatsApp para restaurantes en Guadalajara",
 desc="Cómo usar un chatbot de WhatsApp en un restaurante de Guadalajara o Zapopan para reservar, tomar pedidos y contestar en hora pico, con las reglas de WhatsApp y la ley de datos en México.",
 rubro=("Gastronomía", "/gastronomia/"), audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de chatbot de WhatsApp para restaurantes en Guadalajara y quiero el Audit de mi restaurante.",
 bajada="En Guadalajara el WhatsApp del restaurante se llena justo cuando nadie puede verlo: el sábado a mediodía, cuando la gente arma la comida familiar, y en las noches de partido. Esta guía explica qué conviene que conteste un chatbot en un restaurante de Guadalajara, qué no debe hacer nunca y cómo empezar sin cambiar tu número.",
 cuerpo=[
  ("zonas", "Una ciudad, varias formas de comer", """
<p>No es lo mismo un restaurante en la Colonia Americana o en Chapultepec, donde las mesas se piden para la noche, que una birriería o una marisquería en Zapopan o Tlaquepaque, donde el movimiento fuerte es de mediodía y en familia. El chatbot tiene que contestar lo que pregunta tu cliente, no lo que pregunta un cliente promedio.</p>
<ul>
<li><strong>Cena y barra:</strong> mesa para hoy, código de vestimenta, si hay música en vivo y hasta qué hora cocinan.</li>
<li><strong>Comida familiar:</strong> mesa para grupos grandes, sillas para niños, estacionamiento y si se puede apartar.</li>
<li><strong>Para llevar:</strong> menú vigente, tiempo de espera, zona de reparto y forma de pago.</li>
</ul>
<p>Antes de configurar nada, revisa los últimos chats de tu WhatsApp y anota las cinco preguntas que más se repiten. Ese es el guion del chatbot.</p>"""),
  ("hora-pico", "La hora pico es la que importa", """
<p>Un chatbot vale por lo que hace cuando el equipo está ocupado. Si a la hora de más servicio el mensaje espera, el cliente le escribe al de enfrente. Un agente conectado a la plataforma de WhatsApp Business contesta al momento, sin importar cuántos chats entren a la vez.<a class="ref" href="#f1">[1]</a></p>
<div class="tabla"><table><thead><tr><th>Momento</th><th>Qué conviene que haga</th></tr></thead><tbody>
<tr><td>Antes de abrir</td><td>Confirmar reservas del día y contestar horarios y ubicación</td></tr>
<tr><td>Servicio lleno</td><td>Tomar reservas y pedidos completos y pasar a una persona lo que no sabe</td></tr>
<tr><td>Después de cerrar</td><td>Dejar la reserva de mañana tomada y avisar al encargado</td></tr>
<tr><td>Evento o grupo</td><td>Pedir fecha, número de personas y tipo de evento y pasarlo a una persona</td></tr>
</tbody></table></div>"""),
  ("reglas", "Lo que permite WhatsApp", """
<p>Cuando el cliente te escribe se abre una ventana de 24 horas para contestarle libremente. Para escribirle después, por ejemplo para recordarle la reserva o avisar del menú de temporada, necesitas una plantilla aprobada por Meta y que el cliente haya aceptado tus mensajes.<a class="ref" href="#f2">[2]</a> Mandar promociones a quien no las pidió va contra la política de WhatsApp Business y puede terminar con el número bloqueado.<a class="ref" href="#f3">[3]</a></p>
<div class="aviso">En la práctica: pide el permiso en el mismo chat de la reserva con una pregunta simple, por ejemplo si quiere recibir un recordatorio el día anterior.</div>"""),
  ("precio", "Precios y menú: lo que dice la ley", """
<p>La Ley Federal de Protección al Consumidor pide informar el precio total.<a class="ref" href="#f4">[4]</a> Si el chatbot manda el menú o el costo de un pedido, que sea el vigente y con lo que el cliente va a pagar, incluido el envío si lo hay. Que el agente lea el menú que tú cargas y no conteste de memoria.</p>"""),
  ("datos", "Datos de tus clientes", """
<p>Nombre, teléfono y dirección de entrega son datos personales y los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a> Ten el aviso de privacidad a un enlace de distancia y usa los datos solo para lo que le dijiste al cliente. Esta guía no reemplaza a un abogado.</p>
<p>Para elegir proveedor, sigue con la guía de <a href="/guias/chatbot-whatsapp-restaurantes/">cómo elegir un chatbot de WhatsApp que sí reserve</a>. Lo que hacemos en la ciudad está en la página de <a href="/negocios/guadalajara/gastronomia/">restaurantes y cafeterías en Guadalajara</a>.</p>"""),
 ],
 faq=[
  ("¿Sirve un chatbot de WhatsApp para un restaurante en Guadalajara?", "Sirve si contesta lo que preguntan tus clientes y toma la reserva o el pedido completo, sobre todo en las horas de más servicio, cuando nadie del equipo puede ver el teléfono."),
  ("¿Tengo que cambiar el número del restaurante?", "No necesariamente. El número puede pasar a la plataforma de WhatsApp Business, y lo importante es que siga a nombre del restaurante."),
  ("¿Puedo mandar promociones a todos mis contactos?", "Solo a quien aceptó recibir tus mensajes y con una plantilla aprobada por Meta. Mandar promociones sin permiso va contra la política de WhatsApp Business."),
  ("¿Qué pasa con las reservas de grupos grandes?", "El chatbot pide fecha, número de personas y tipo de evento, y pasa la conversación a una persona del equipo para cerrar."),
 ],
 fuentes=["wa_api", "wa_precios", "wa_politica", "lfpc", "lfpdppp"],
)

G["reservas-instagram-restaurantes-monterrey"] = dict(
 titulo="Reservas por Instagram para restaurantes en Monterrey: del DM a la mesa",
 corto="Reservas por Instagram para restaurantes en Monterrey",
 desc="Cómo tomar reservas desde los DMs y las historias de Instagram en un restaurante de Monterrey o San Pedro, qué permite la API de Instagram y cómo no perder la mesa cuando nadie contesta.",
 rubro=("Gastronomía", "/gastronomia/"), audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de reservas por Instagram para restaurantes en Monterrey y quiero el Audit de mi restaurante.",
 bajada="En Monterrey mucha gente elige restaurante desde Instagram: ve el reel del corte o del brunch y escribe por DM «¿tienen mesa para el sábado?». Ese mensaje es una reserva casi hecha. Si nadie la contesta hasta el lunes, se pierde. Esta guía explica cómo convertir los DMs en mesas confirmadas sin tener a alguien pegado al teléfono.",
 cuerpo=[
  ("dm", "El DM es una reserva a medio camino", """
<p>Quien escribe por Instagram ya vio la comida, el lugar y el ambiente. No necesita que lo convenzas: necesita saber si hay lugar y a qué hora. En San Pedro, Valle Oriente o el Barrio Antiguo, donde la cena del fin de semana se decide con pocas horas de anticipación, contestar rápido vale más que cualquier promoción.</p>
<p>El problema de casi todos los restaurantes es el mismo: la cuenta la maneja alguien de marketing, la reserva la toma el gerente y los DMs se quedan en medio.</p>"""),
  ("api", "Qué permite Instagram", """
<p>Para que un agente conteste los DMs, la cuenta tiene que ser profesional y conectarse a la API de mensajes de Instagram, a través de Meta o de un proveedor.<a class="ref" href="#f1">[1]</a> El agente puede contestar los mensajes directos y las respuestas a tus historias durante las 24 horas siguientes al último mensaje del cliente. Pasado ese plazo, solo una persona del equipo puede seguir la conversación, hasta siete días.<a class="ref" href="#f1">[1]</a></p>
<div class="aviso">En la práctica: el agente debe pedir el WhatsApp del cliente al confirmar la mesa. Así el recordatorio del día y cualquier cambio llegan por un canal que no se cierra a las 24 horas.</div>"""),
  ("flujo", "Cómo se ve una reserva desde el DM", """
<div class="tabla"><table><thead><tr><th>Paso</th><th>Qué hace el agente</th></tr></thead><tbody>
<tr><td>Pregunta</td><td>Pide día, hora y número de personas</td></tr>
<tr><td>Disponibilidad</td><td>Lee el sistema de reservas del restaurante. Si no está conectado, toma la solicitud y avisa que el equipo confirma</td></tr>
<tr><td>Confirmación</td><td>Deja la reserva a nombre del cliente y pide su WhatsApp</td></tr>
<tr><td>Casos especiales</td><td>Grupos, cumpleaños con pastel, alergias o quejas pasan a una persona</td></tr>
</tbody></table></div>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">Instagram · 18:40</span>
<span class="yo">Hola, ¿tienen mesa para 6 este sábado en la noche?</span>
<span class="bot">¡Hola! El sábado tengo mesa para 6 a las 20:00 o a las 21:30. ¿Cuál te queda mejor? Soy el asistente con IA del restaurante.</span>
<span class="yo">20:00</span>
<span class="bot">Listo. ¿Me compartes un WhatsApp para mandarte la confirmación y un recordatorio el sábado?</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("contenido", "Que el contenido lleve al DM", """
<p>Las reservas por Instagram suben cuando cada publicación dice qué hacer. Un reel del platillo con un texto que invite a escribir «MESA» por DM, o una historia con el sticker de mensaje, le da al cliente el siguiente paso. El agente reconoce la palabra y abre la conversación de reserva.</p>
<p>En tu perfil, deja claro el horario, la dirección y que se reserva por DM o por WhatsApp. Y si usas un enlace en la biografía, que lleve a reservar, no a una página de inicio.</p>"""),
  ("datos", "Datos de tus clientes", """
<p>El nombre y el teléfono de quien reserva son datos personales y los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f2">[2]</a> Ten tu aviso de privacidad enlazado en la biografía o en el mismo chat.</p>
<p>Si tu restaurante también recibe reservas por WhatsApp, sigue con la guía de <a href="/guias/chatbot-whatsapp-restaurantes/">chatbot de WhatsApp para restaurantes</a>. Lo que hacemos en la ciudad está en la página de <a href="/negocios/monterrey/gastronomia/">restaurantes y cafeterías en Monterrey</a>.</p>"""),
 ],
 faq=[
  ("¿Se pueden tomar reservas automáticas por Instagram?", "Sí, con una cuenta profesional conectada a la API de mensajes de Instagram. El agente contesta los DMs y confirma la mesa si está conectado al sistema de reservas."),
  ("¿Qué pasa si el cliente contesta después de 24 horas?", "El agente ya no puede escribirle libremente. Por eso conviene pedir el WhatsApp al confirmar la reserva."),
  ("¿El agente puede contestar respuestas a historias?", "Sí. Las respuestas a historias llegan como mensajes directos y el agente puede contestarlas dentro de la ventana de 24 horas."),
  ("¿Qué no debe hacer el agente?", "Confirmar una mesa sin ver la disponibilidad real, inventar respuestas sobre alergias o resolver una queja. Esos casos pasan a una persona."),
 ],
 fuentes=["ig_api", "lfpdppp"],
)

G["automatizar-mensajes-hoteles-tulum"] = dict(
 titulo="Automatizar mensajes para hoteles en Tulum: antes, durante y después de la estancia",
 corto="Automatizar mensajes para hoteles en Tulum",
 desc="Qué mensajes conviene automatizar en un hotel boutique de Tulum, en español y en inglés, desde la consulta hasta la reseña, con las reglas de WhatsApp e Instagram y la ley mexicana.",
 rubro=("Hospitality", "/hospitality/"), audit="hospitality", og="og-hospitality.jpg",
 wa="Hola! Leí la guía de automatizar mensajes para hoteles en Tulum y quiero el Audit de mi hotel.",
 bajada="En un hotel de Tulum el huésped pregunta lo mismo una y otra vez: cómo llegar desde el aeropuerto, a qué hora es el check-in, si la playa está cerca y si aceptan tarjeta. Contestarlo a mano, en dos idiomas y de madrugada, se come la recepción. Esta guía ordena qué mensajes automatizar en cada momento de la estancia y cuáles dejar siempre a una persona.",
 cuerpo=[
  ("momentos", "Los cuatro momentos de la estancia", """
<p>Automatizar no es poner un bot que conteste todo. Es decidir qué mensaje sale en cada momento, en qué idioma y por qué canal. En un hotel boutique de Tulum, entre la zona hotelera, Aldea Zamá y el pueblo, las preguntas cambian según dónde esté el huésped en su viaje.</p>
<div class="tabla"><table><thead><tr><th>Momento</th><th>Mensajes que conviene automatizar</th><th>Lo que queda para una persona</th></tr></thead><tbody>
<tr><td>Consulta</td><td>Disponibilidad, tarifa directa y lo que incluye</td><td>Grupos, bodas y retiros</td></tr>
<tr><td>Antes de llegar</td><td>Confirmación, cómo llegar, hora de check-in y qué traer</td><td>Pedidos especiales y cambios de fecha</td></tr>
<tr><td>Durante la estancia</td><td>Horarios, recomendaciones que el hotel cargó y solicitudes a recepción</td><td>Quejas y cualquier tema de salud o seguridad</td></tr>
<tr><td>Después</td><td>Agradecimiento, enlace para dejar reseña y permiso para escribirle en otra temporada</td><td>Respuesta a una mala experiencia</td></tr>
</tbody></table></div>"""),
  ("idioma", "El idioma lo pone el huésped", """
<p>Una parte de los huéspedes de Tulum escribe en inglés y planea desde otro huso horario. El agente tiene que responder en el idioma en que le escriben, guardar ese idioma en el contacto y usarlo en cada mensaje que siga. Una plantilla de WhatsApp se aprueba por idioma, así que conviene tener cada una en español y en inglés.<a class="ref" href="#f1">[1]</a></p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 02:15</span>
<span class="yo">Hi, we land in Tulum at 4pm tomorrow. Can we check in early?</span>
<span class="bot">Hi! Check-in is from 3pm, so you're fine. I'll note your arrival time for reception. Do you need directions from the airport? I'm the hotel's AI assistant.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("reglas", "Las reglas de cada canal", """
<p>En WhatsApp, el huésped abre una ventana de 24 horas cada vez que escribe. Los mensajes que salen fuera de esa ventana, como la confirmación de la semana anterior o el enlace de la reseña, necesitan plantilla aprobada y permiso del huésped.<a class="ref" href="#f1">[1]</a> La política de WhatsApp Business no permite mensajes a quien no los aceptó.<a class="ref" href="#f2">[2]</a></p>
<p>En Instagram, la ventana también es de 24 horas, y después solo una persona del equipo puede seguir la conversación, hasta siete días.<a class="ref" href="#f3">[3]</a> Por eso, en Tulum, la consulta suele empezar por Instagram y la estancia conviene llevarla por WhatsApp.</p>"""),
  ("precio", "Tarifas en el mensaje", """
<p>Si el agente cotiza, el precio tiene que ser el total que va a pagar el huésped. Lo pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f4">[4]</a> Que la tarifa salga del sistema del hotel, con impuestos y cargos incluidos, y no de una lista que alguien actualiza a mano.</p>"""),
  ("datos", "Datos del huésped", """
<p>Nombre, fechas, teléfono y datos de pago son datos personales, regidos por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a> Pide solo lo necesario y enlaza tu aviso de privacidad en el primer mensaje.</p>
<p>Para que el huésped reserve directo y no por la plataforma, sigue con la guía de <a href="/guias/reservas-directas-whatsapp-hoteles/">reservas directas por WhatsApp para hoteles</a>. Si además vendes tours, mira la de <a href="/guias/chatbot-whatsapp-tours-riviera-maya/">chatbot de WhatsApp para tours en la Riviera Maya</a>. Lo que hacemos en la ciudad está en <a href="/negocios/tulum/hospitality/">hoteles y hospedajes en Tulum</a>.</p>"""),
 ],
 faq=[
  ("¿Qué mensajes conviene automatizar en un hotel de Tulum?", "La respuesta a consultas de disponibilidad, la confirmación, las indicaciones antes de llegar, las preguntas durante la estancia y el pedido de reseña al salir. Quejas, grupos y cambios quedan para una persona."),
  ("¿El agente contesta en inglés?", "Sí. Responde en el idioma del huésped y lo guarda en el contacto. Las plantillas de WhatsApp se aprueban por idioma, así que conviene tenerlas en español y en inglés."),
  ("¿Puedo mandar mensajes a un huésped después de su estancia?", "Solo con una plantilla aprobada y si el huésped aceptó recibir tus mensajes."),
  ("¿Conviene usar WhatsApp o Instagram?", "Los dos. La consulta suele llegar por Instagram y la estancia conviene llevarla por WhatsApp, porque la ventana de Instagram se cierra antes para el agente."),
 ],
 fuentes=["wa_precios", "wa_politica", "ig_api", "lfpc", "lfpdppp"],
)

G["automatizar-mensajes-hoteles-playa-del-carmen"] = dict(
 titulo="Automatizar mensajes para hoteles en Playa del Carmen: consultas, traslados y grupos",
 corto="Automatizar mensajes para hoteles en Playa del Carmen",
 desc="Cómo automatizar los mensajes de un hotel, condohotel o renta vacacional en Playa del Carmen: consultas en varios idiomas, traslados, grupos y check-in sin recepción, con las reglas de WhatsApp.",
 rubro=("Hospitality", "/hospitality/"), audit="hospitality", og="og-hospitality.jpg",
 wa="Hola! Leí la guía de automatizar mensajes para hoteles en Playa del Carmen y quiero el Audit de mi hotel.",
 bajada="En Playa del Carmen conviven hoteles con recepción las 24 horas, condohoteles y departamentos en renta que se entregan con un código. En todos, el teléfono suena por lo mismo: cómo llegar desde el aeropuerto de Cancún, dónde estacionar cerca de la Quinta Avenida, a qué hora se entra. Esta guía explica qué mensajes automatizar según el tipo de hospedaje y cómo no perder al grupo que pide cotización a varios a la vez.",
 cuerpo=[
  ("tipo", "Depende de cómo opera tu hospedaje", """
<p>No se automatiza igual un hotel con recepción que una renta vacacional sin personal en sitio. Lo primero es ver quién atiende hoy cada pregunta y a qué hora.</p>
<div class="tabla"><table><thead><tr><th>Tipo de hospedaje</th><th>Mensajes que conviene automatizar</th></tr></thead><tbody>
<tr><td>Hotel con recepción</td><td>Consultas fuera de horario, confirmación y preguntas frecuentes, para que la recepción atienda a quien está ahí</td></tr>
<tr><td>Condohotel o varias unidades</td><td>Instrucciones por unidad, horario de entrada y salida, reglas del edificio y avisos de limpieza</td></tr>
<tr><td>Renta vacacional sin personal</td><td>Cómo llegar, entrega del acceso el día de llegada, wifi, basura y contacto para emergencias, que siempre es una persona</td></tr>
</tbody></table></div>"""),
  ("llegada", "La llegada es el mensaje que más se repite", """
<p>Casi todos los huéspedes llegan por el aeropuerto de Cancún o por carretera, y muchos preguntan por el traslado, el estacionamiento y la hora de entrada. Un mensaje de llegada bien escrito, enviado el día anterior, resuelve la mayoría de esas consultas antes de que lleguen.</p>
<ul>
<li>Dirección exacta y un enlace al mapa, con una referencia que se vea desde la calle.</li>
<li>Opciones de traslado que ofreces o recomiendas, sin prometer horarios que no controlas.</li>
<li>Hora de entrada, qué hacer si llegan antes y a quién escribir si algo falla.</li>
</ul>
<p>Ese mensaje sale fuera de la ventana de 24 horas, así que necesita una plantilla aprobada y el permiso del huésped.<a class="ref" href="#f1">[1]</a></p>"""),
  ("grupos", "Grupos: el que contesta primero cotiza", """
<p>Bodas, viajes de amigos o equipos de trabajo piden cotización a varios hospedajes al mismo tiempo. El agente no cierra un grupo, pero puede pedir en el primer mensaje lo que tu equipo necesita para cotizar: fechas, número de personas, habitaciones y presupuesto. Con eso, una persona responde con la propuesta el mismo día.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 22:30</span>
<span class="yo">Hola, somos 14 para una boda en marzo, ¿tienen lugar?</span>
<span class="bot">¡Hola! Con gusto te cotizamos. ¿Me dices las fechas de entrada y salida y cuántas habitaciones necesitan? Mañana temprano alguien del equipo te manda la propuesta. Soy el asistente con IA del hotel.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("reglas", "Reglas de WhatsApp y del precio", """
<p>Cada mensaje del huésped abre una ventana de 24 horas para contestar libremente; fuera de ella solo salen plantillas aprobadas.<a class="ref" href="#f1">[1]</a> La política de WhatsApp Business no permite escribir a quien no lo aceptó.<a class="ref" href="#f2">[2]</a> Y si el agente da una tarifa, tiene que ser el precio total, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f3">[3]</a></p>"""),
  ("datos", "Datos del huésped y códigos de acceso", """
<p>Nombre, teléfono, fechas y documentos de identidad son datos personales, regidos por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f4">[4]</a> Si entregas códigos de acceso por mensaje, que se envíen solo el día de llegada y solo al huésped que reservó.</p>
<p>Si la consulta llega por Instagram, mira la guía de <a href="/guias/reservas-automaticas-instagram-hoteles-boutique/">reservas automáticas por Instagram para hoteles boutique</a>. Lo que hacemos en la ciudad está en <a href="/negocios/playa-del-carmen/hospitality/">hoteles y hospedajes en Playa del Carmen</a>.</p>"""),
 ],
 faq=[
  ("¿Qué mensajes conviene automatizar en un hotel de Playa del Carmen?", "Las consultas fuera de horario, la confirmación, el mensaje de llegada con traslado y estacionamiento, las preguntas frecuentes de la estancia y el primer contacto con grupos."),
  ("¿Sirve para una renta vacacional sin recepción?", "Sí. El agente envía las instrucciones de llegada y el acceso el día de entrada, y deja las emergencias siempre a una persona."),
  ("¿El agente puede cotizar un grupo?", "Puede pedir fechas, personas y habitaciones en el primer mensaje. La propuesta la arma una persona del equipo."),
  ("¿Puedo mandar el mensaje de llegada por WhatsApp?", "Sí, con una plantilla aprobada por Meta y con el permiso del huésped, porque sale fuera de la ventana de 24 horas."),
 ],
 fuentes=["wa_precios", "wa_politica", "lfpc", "lfpdppp"],
)

G["paginas-web-gimnasios-cdmx"] = dict(
 titulo="Páginas web para gimnasios en CDMX: qué necesita la tuya para llenar clases",
 corto="Páginas web para gimnasios en CDMX",
 desc="Qué tiene que tener la página web de un gimnasio o estudio en Ciudad de México para aparecer en búsquedas por colonia, mostrar horarios y llevar a la clase de prueba, con lo que piden Google y la ley.",
 rubro=("Fitness", "/fitness/"), audit="fitness", og="og-fitness.jpg",
 wa="Hola! Leí la guía de páginas web para gimnasios en CDMX y quiero el Audit de mi gimnasio.",
 bajada="En Ciudad de México la gente no busca «gimnasio». Busca «box en la Del Valle», «pilates en Polanco» o «gimnasio abierto a las 6 en la Narvarte». Si tu página es una portada bonita con un formulario, esa búsqueda se la queda el estudio de al lado o una app de reservas. Esta guía explica qué necesita la página de un gimnasio en la capital para que la encuentren y para que quien entra agende la clase de prueba.",
 cuerpo=[
  ("colonia", "La colonia va escrita", """
<p>Google ordena los resultados locales por relevancia, distancia y prominencia.<a class="ref" href="#f1">[1]</a> En una ciudad donde hay estudios en cada colonia, la distancia pesa, y la relevancia empieza por decir en texto dónde estás y qué das.</p>
<ul>
<li>Nombre de la colonia y de la disciplina en el título y en el primer párrafo: por ejemplo, «Estudio de pilates en la Roma Norte».</li>
<li>Dirección, referencias de llegada, estacionamiento o bicicletas y la estación de Metro o Metrobús más cercana.</li>
<li>Si tienes más de una sede, una página por sede con su horario y sus fotos.</li>
</ul>"""),
  ("horarios", "Horarios y clase de prueba, a un toque", """
<p>Lo primero que busca quien entra es el horario. Ponlo en texto, no en una imagen de Instagram, y que se lea bien en el celular: Google indexa la versión móvil de tu sitio.<a class="ref" href="#f2">[2]</a> Una página lenta pierde la visita antes de que llegue al botón.<a class="ref" href="#f3">[3]</a></p>
<div class="tabla"><table><thead><tr><th>Lo que debe estar arriba</th><th>Por qué</th></tr></thead><tbody>
<tr><td>Disciplina y colonia</td><td>Es lo que la persona buscó</td></tr>
<tr><td>Horario de la semana</td><td>Decide si le sirve antes de mirar cualquier otra cosa</td></tr>
<tr><td>Botón de clase de prueba</td><td>Es el siguiente paso, no la membresía</td></tr>
<tr><td>Botón de WhatsApp</td><td>Para quien quiere preguntar antes de agendar</td></tr>
</tbody></table></div>"""),
  ("precio", "Precios en la página", """
<p>Si publicas planes, la Ley Federal de Protección al Consumidor pide informar el precio total, con inscripción y cargos incluidos.<a class="ref" href="#f4">[4]</a> Si prefieres no publicarlos, deja claro cómo se piden y que la respuesta llegue al momento.</p>"""),
  ("datos-estructurados", "Datos estructurados para gimnasios", """
<p>Schema.org tiene un tipo específico para gimnasios, ExerciseGym, que hereda las propiedades de empresa local: dirección, horario, teléfono y área que atiendes.<a class="ref" href="#f5">[5]</a> Google usa los datos estructurados de empresa local para entender tu negocio.<a class="ref" href="#f6">[6]</a> No reemplazan al texto: lo ordenan.</p>"""),
  ("despues", "Lo que pasa después del clic", """
<p>La página trae la clase de prueba. Lo que la convierte en socio es el seguimiento: el recordatorio del día anterior, el mensaje después de entrenar y la respuesta rápida al DM. Lo explicamos en la guía de <a href="/guias/responder-dms-instagram-automaticamente-gimnasios/">cómo responder DMs de Instagram en un gimnasio</a> y en la de <a href="/guias/retencion-socios-gimnasio-reservas-clases/">retención de socios</a>.</p>
<p>Para aparecer también cuando alguien le pregunta a ChatGPT, sigue con <a href="/guias/como-aparecer-en-chatgpt-negocio-en-tu-ciudad/">cómo aparecer en ChatGPT en tu ciudad</a>. Lo que hacemos en la ciudad está en <a href="/negocios/ciudad-de-mexico/fitness/">gimnasios y estudios en Ciudad de México</a>.</p>"""),
 ],
 faq=[
  ("¿Qué tiene que tener la página web de un gimnasio?", "Disciplina y colonia en el título, horario en texto, botón de clase de prueba y de WhatsApp, carga rápida en el celular y datos estructurados de gimnasio."),
  ("¿Conviene una página por sede?", "Sí, si tienes más de una. Cada sede con su dirección, su horario y sus fotos."),
  ("¿Tengo que publicar los precios?", "No es obligatorio, pero si los publicas, la Ley Federal de Protección al Consumidor pide informar el precio total."),
  ("¿Sirve solo tener Instagram?", "Instagram ayuda, pero la búsqueda por colonia pasa por Google y por tu Perfil de Empresa. Una página propia te da un lugar que no depende de una red."),
 ],
 fuentes=["gbp_rank", "g_mobile", "g_cwv", "lfpc", "sch_gym", "g_localbiz"],
)

G["como-pedir-resenas-google-sin-incentivos"] = dict(
 titulo="Cómo pedir reseñas en Google sin incentivos (y sin romper las reglas)",
 corto="Pedir reseñas en Google sin incentivos",
 desc="Cómo pedir reseñas en Google a tus clientes sin ofrecer descuentos ni regalos, qué prohíbe la política de Google Maps, en qué momento pedirlas por WhatsApp y cómo responderlas.",
 rubro=("Posicionamiento en IA", "/posicionamiento-en-ia/"), audit="", og="og-portada.jpg",
 wa="Hola! Leí la guía de cómo pedir reseñas en Google y quiero el Audit de mi negocio.",
 bajada="«Déjanos cinco estrellas y te damos un postre» parece inofensivo, pero va contra las reglas de Google y puede costarte las reseñas que ya tienes. La buena noticia es que no hace falta: la mayoría de los clientes contentos dejan reseña si se la pides en el momento justo y con un enlace directo. Esta guía explica cómo hacerlo bien.",
 cuerpo=[
  ("reglas", "Lo que prohíbe Google", """
<p>La política de contenido de Google Maps considera interacción falsa ofrecer incentivos, como pagos, descuentos o productos gratis, a cambio de publicar una reseña o de cambiar o retirar una negativa.<a class="ref" href="#f1">[1]</a> También prohíbe desalentar las reseñas negativas y pedir reseñas positivas solo a los clientes que crees que van a hablar bien de ti.<a class="ref" href="#f1">[1]</a></p>
<div class="aviso">En la práctica: pídele reseña a todos tus clientes, de la misma forma, sin preguntar antes si quedaron contentos y sin ofrecer nada a cambio.</div>"""),
  ("enlace", "Usa el enlace directo", """
<p>Google permite compartir un enlace o un código QR que abre directamente la ventana para dejar la reseña de tu negocio.<a class="ref" href="#f2">[2]</a> Lo sacas desde tu Perfil de Empresa. Cuantos menos pasos tenga el cliente, más reseñas llegan.</p>
<ul>
<li>El enlace va en el mensaje de agradecimiento por WhatsApp.</li>
<li>El código QR va en la cuenta, en el mostrador o en la tarjeta que entregas con el pedido.</li>
<li>El mismo enlace va en tu firma de correo y en la biografía de Instagram si quieres.</li>
</ul>"""),
  ("momento", "El momento importa más que el texto", """
<p>Una reseña se pide cuando el cliente todavía tiene presente la experiencia. Cada rubro tiene su momento:</p>
<div class="tabla"><table><thead><tr><th>Rubro</th><th>Cuándo pedirla</th></tr></thead><tbody>
<tr><td>Restaurante</td><td>El mismo día, después de la visita</td></tr>
<tr><td>Hotel</td><td>Al hacer el check-out o al día siguiente</td></tr>
<tr><td>Gimnasio</td><td>Después de las primeras semanas, no después de la clase de prueba</td></tr>
<tr><td>Inmobiliaria</td><td>Al entregar las llaves o firmar el contrato</td></tr>
<tr><td>Servicio a domicilio</td><td>Cuando el trabajo quedó terminado</td></tr>
</tbody></table></div>
<p>Si lo pides por WhatsApp fuera de las 24 horas desde el último mensaje del cliente, necesitas una plantilla aprobada y su permiso para escribirle.<a class="ref" href="#f3">[3]</a></p>"""),
  ("mensaje", "Un mensaje que funciona", """
<div class="chat" role="figure" aria-label="Ejemplo de mensaje">
<span class="t">WhatsApp · 21:30</span>
<span class="bot">Gracias por venir hoy. Si tienes un minuto, nos ayuda mucho que cuentes en Google cómo te fue, lo bueno y lo que podemos mejorar: [enlace]</span>
<span class="nota">Mensaje de ejemplo.</span>
</div>
<p>Fíjate en lo que no dice: no pide cinco estrellas, no ofrece nada y no pregunta antes si le gustó. Pedir que cuente qué pidió o qué servicio recibió ayuda además a que la reseña nombre lo que vendes, que es lo que leen Google y los buscadores con IA cuando alguien pregunta por tu rubro en tu ciudad.</p>"""),
  ("responder", "Responde todas, también las malas", """
<p>Google recomienda responder las reseñas de forma clara, útil y educada.<a class="ref" href="#f4">[4]</a> Una respuesta tranquila a una reseña negativa le dice más al siguiente cliente que diez reseñas de cinco estrellas. Agradece, reconoce lo que pasó si pasó, y ofrece seguir la conversación por un canal privado.</p>
<p>Las reseñas son parte de lo que te hace aparecer en búsquedas locales. Sigue con la guía de <a href="/guias/como-aparecer-en-chatgpt-negocio-en-tu-ciudad/">cómo aparecer en ChatGPT en tu ciudad</a> y con la de <a href="/guias/como-aparecer-en-chatgpt-y-google-negocio-pequeno/">cómo aparecer en ChatGPT y en Google si tienes un negocio pequeño</a>.</p>"""),
 ],
 faq=[
  ("¿Puedo dar un descuento a cambio de una reseña en Google?", "No. La política de Google Maps considera interacción falsa ofrecer pagos, descuentos o productos gratis a cambio de una reseña, y esas reseñas se retiran."),
  ("¿Puedo pedir reseñas solo a los clientes contentos?", "No. Google prohíbe pedir reseñas positivas de forma selectiva. Pídele a todos de la misma forma."),
  ("¿Cómo saco el enlace para pedir reseñas?", "Desde tu Perfil de Empresa en Google puedes crear un enlace o un código QR que abre directamente la ventana de reseña."),
  ("¿Puedo pedir reseñas por WhatsApp?", "Sí. Dentro de las 24 horas desde el último mensaje del cliente contestas libremente; después necesitas una plantilla aprobada y su permiso."),
  ("¿Tengo que responder las reseñas negativas?", "Conviene responder todas. Una respuesta clara y educada a una reseña negativa le muestra al siguiente cliente cómo tratas los problemas."),
 ],
 fuentes=["g_contenido", "g_resenas", "wa_precios", "g_responder"],
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
