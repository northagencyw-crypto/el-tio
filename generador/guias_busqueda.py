# -*- coding: utf-8 -*-
"""Genera 21 guías SEO por búsqueda (21/11/2026, dos tandas). Solo español. Uso: python generador/guias_busqueda.py"""
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

# ---- 10 guías nuevas (21/11/2026, tanda 2) ----
F["lie"] = ("Ley de Inversión Extranjera, artículos 10 y 11: adquisición de inmuebles en la zona restringida mediante fideicomiso. Texto vigente en la Cámara de Diputados.", "https://www.diputados.gob.mx/LeyesBiblio/ref/lie.htm")
F["cpeum27"] = ("Constitución Política de los Estados Unidos Mexicanos, artículo 27, fracción I: zona restringida de 100 kilómetros en fronteras y 50 en playas.", "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf")
F["sch_rea"] = ("Schema.org, tipo «RealEstateAgent».", "https://schema.org/RealEstateAgent")
F["sch_bar"] = ("Schema.org, tipo «BarOrPub».", "https://schema.org/BarOrPub")
F["sch_cafe"] = ("Schema.org, tipo «CafeOrCoffeeShop».", "https://schema.org/CafeOrCoffeeShop")
F["sch_venue"] = ("Schema.org, tipo «EventVenue».", "https://schema.org/EventVenue")
F["wa_catalogo"] = ("Meta, «Sell products and services», documentación de WhatsApp Cloud API: catálogo y mensajes de uno o varios productos.", "https://developers.facebook.com/docs/whatsapp/cloud-api/guides/sell-products-and-services")

RE = ("Real estate", "/real-estate/")
GA = ("Gastronomía", "/gastronomia/")
EV = ("Eventos", "/eventos/")
FI = ("Fitness", "/fitness/")
DI = ("Distribución", "/distribucion/")

G["agente-whatsapp-inmobiliarias-cdmx"] = dict(
 titulo="Agente de WhatsApp para inmobiliarias en CDMX: contestar cada lead antes que el portal",
 corto="Agente de WhatsApp para inmobiliarias en CDMX",
 desc="Cómo una inmobiliaria en Ciudad de México puede contestar al momento los leads que llegan de portales, Instagram y su sitio, calificar por colonia y presupuesto y agendar visitas por WhatsApp, con las reglas de Meta y de la ley.",
 rubro=RE, audit="real-estate", og="og-real-estate.jpg",
 wa="Hola! Leí la guía de agente de WhatsApp para inmobiliarias en CDMX y quiero el Audit de mi inmobiliaria.",
 bajada="Un departamento en renta en la Narvarte o en la Del Valle recibe consultas de varias personas el mismo día, y cada una escribe también a otras tres inmobiliarias. La que contesta primero y con datos concretos agenda la visita. Esta guía explica qué tiene que hacer un agente de WhatsApp en una inmobiliaria de la capital y qué no le conviene hacer solo.",
 cuerpo=[
  ("origen", "De dónde llegan los leads", """
<p>En una inmobiliaria de Ciudad de México los contactos llegan por varios lados a la vez: portales, Marketplace, Instagram, el sitio propio y el letrero en la fachada. Cada canal trae a la persona con una pregunta distinta y casi siempre con la misma prisa. El primer paso es que todos terminen en un solo número de WhatsApp y en un solo registro, para saber quién preguntó por qué propiedad.</p>
<div class="tabla"><table><thead><tr><th>Origen</th><th>Qué suele preguntar</th></tr></thead><tbody>
<tr><td>Portal o Marketplace</td><td>Si sigue disponible, precio total y requisitos</td></tr>
<tr><td>Instagram</td><td>Zona, fotos de más y si se puede visitar el fin de semana</td></tr>
<tr><td>Letrero en la propiedad</td><td>Qué es exactamente, venta o renta, y cuándo verla</td></tr>
<tr><td>Sitio propio</td><td>Opciones parecidas en la misma colonia</td></tr>
</tbody></table></div>"""),
  ("calificar", "Calificar sin interrogar", """
<p>El agente no está para vender el departamento. Está para que el asesor llegue a la visita sabiendo lo esencial: colonia o alcaldía que busca, presupuesto, si es compra o renta, cuándo quiere mudarse y, en renta, si cumple con los requisitos que pide el propietario. Dos o tres preguntas bien puestas bastan; un formulario por chat espanta.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 22:40</span>
<span class="yo">Hola, ¿sigue disponible el depa de la Narvarte?</span>
<span class="bot">¡Hola! Sí, sigue disponible. ¿Lo buscas para mudarte este mes o más adelante? Si te queda bien, tengo visitas el sábado por la mañana. Soy el asistente con IA de la inmobiliaria.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("reglas", "Reglas de WhatsApp que importan aquí", """
<p>Para conectar un agente se usa la plataforma de WhatsApp Business, la API.<a class="ref" href="#f1">[1]</a> Cada mensaje del cliente abre una ventana de 24 horas para contestar libremente; fuera de ella, por ejemplo para avisar que bajó el precio o que entró una opción nueva en su colonia, se necesita una plantilla aprobada y su permiso.<a class="ref" href="#f2">[2]</a> La política de WhatsApp Business no permite escribir a listas compradas ni a quien no aceptó recibir mensajes.<a class="ref" href="#f3">[3]</a></p>"""),
  ("precio", "Precio y datos de la propiedad", """
<p>Si el agente da un precio, tiene que ser el total, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f4">[4]</a> En venta de vivienda, la NOM-247-SE-2021 fija qué información comercial debe darse al consumidor.<a class="ref" href="#f5">[5]</a> Por eso conviene que el agente responda solo con la ficha que cargó la inmobiliaria y pase a un asesor cualquier pregunta sobre escrituras, crédito o contrato.</p>"""),
  ("datos", "Datos del cliente", """
<p>Nombre, teléfono, ingresos y documentos para una renta son datos personales, y algunos son delicados. Los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f6">[6]</a> No pidas identificaciones ni comprobantes por el chat del agente: que los reciba el asesor por el canal que la inmobiliaria definió.</p>
<p>Para el seguimiento después de la visita, sigue con la guía de <a href="/guias/crm-inmobiliaria-seguimiento-leads/">CRM para inmobiliarias</a>. Lo que hacemos en la ciudad está en <a href="/negocios/ciudad-de-mexico/real-estate/">inmobiliarias en Ciudad de México</a>.</p>"""),
 ],
 faq=[
  ("¿Qué hace un agente de WhatsApp en una inmobiliaria?", "Contesta al momento si la propiedad sigue disponible, pregunta zona, presupuesto y fecha de mudanza, agenda la visita y pasa la conversación a un asesor."),
  ("¿Puede responder los leads que llegan de los portales?", "Sí, si el contacto termina en el WhatsApp de la inmobiliaria. Lo importante es que todos los canales lleguen a un solo número y a un solo registro."),
  ("¿Puedo avisar por WhatsApp cuando entra una propiedad nueva?", "Sí, con una plantilla aprobada por Meta y con el permiso del cliente, porque el aviso sale fuera de la ventana de 24 horas."),
  ("¿El agente puede pedir documentos para la renta?", "Conviene que no. Identificaciones y comprobantes son datos personales delicados y es mejor que los reciba un asesor por el canal que defina la inmobiliaria."),
 ],
 fuentes=["wa_api", "wa_precios", "wa_politica", "lfpc", "nom247", "lfpdppp"],
)

G["leads-inmobiliarios-guadalajara-zapopan"] = dict(
 titulo="Leads inmobiliarios en Guadalajara y Zapopan: de la consulta a la visita agendada",
 corto="Leads inmobiliarios en Guadalajara y Zapopan",
 desc="Cómo una inmobiliaria o desarrolladora en Guadalajara y Zapopan puede ordenar los leads de preventa y reventa, contestar por WhatsApp al momento y agendar visitas a la obra o al departamento muestra.",
 rubro=RE, audit="real-estate", og="og-real-estate.jpg",
 wa="Hola! Leí la guía de leads inmobiliarios en Guadalajara y quiero el Audit de mi inmobiliaria.",
 bajada="En la zona metropolitana de Guadalajara se buscan cosas muy distintas con la misma palabra: un departamento en preventa en Zapopan, una casa en reventa en Tlajomulco o una renta cerca de una universidad. Si todos los leads caen en el mismo chat y los contesta quien pueda, el que pregunta por la preventa espera lo mismo que el curioso. Esta guía explica cómo separar, contestar y agendar.",
 cuerpo=[
  ("separar", "Separa el lead por tipo de operación", """
<p>La primera pregunta que tiene que resolver la conversación es qué busca la persona, porque de eso depende quién la atiende y qué tan rápido.</p>
<div class="tabla"><table><thead><tr><th>Tipo de lead</th><th>Lo que necesita en el primer mensaje</th></tr></thead><tbody>
<tr><td>Preventa</td><td>Avance de obra, fecha estimada de entrega, esquema de pagos y visita al departamento muestra</td></tr>
<tr><td>Reventa</td><td>Disponibilidad, precio total, si acepta crédito y cuándo se puede ver</td></tr>
<tr><td>Renta</td><td>Disponibilidad, requisitos del propietario y fecha de mudanza</td></tr>
<tr><td>Propietario que quiere vender</td><td>Zona, tipo de inmueble y una persona del equipo que lo atienda por chat</td></tr>
</tbody></table></div>"""),
  ("preventa", "Lo que pide la norma en preventa", """
<p>La NOM-247-SE-2021 fija la información comercial y los elementos de los contratos de vivienda, incluida la que se vende antes de terminarse.<a class="ref" href="#f1">[1]</a> Para el agente eso significa una regla simple: responde con la información que la desarrolladora ya publicó y revisó, y cualquier pregunta sobre contrato, entrega o garantía va a una persona. Cuando da un precio, es el total.<a class="ref" href="#f2">[2]</a></p>"""),
  ("visita", "Agendar la visita en el mismo chat", """
<p>El lead que agenda en la misma conversación tiene más probabilidades de llegar que el que queda en «te marco mañana». El agente puede ofrecer horarios reales del asesor o del departamento muestra, confirmar y mandar la ubicación.</p>
<p>El recordatorio del día anterior sale fuera de la ventana de 24 horas, así que necesita plantilla aprobada y el permiso del cliente.<a class="ref" href="#f3">[3]</a> Pide ese permiso al confirmar la cita, no después.</p>"""),
  ("pagina", "Una página por desarrollo o por zona", """
<p>Quien busca en Google «departamentos en preventa en Zapopan» quiere ver ese desarrollo o esa zona, no la portada de la inmobiliaria. Una página por desarrollo, con su avance, su ubicación y un botón de WhatsApp que ya diga de qué desarrollo se trata, hace que el lead llegue con contexto. Los datos estructurados de agente inmobiliario ayudan a que el buscador entienda quién eres.<a class="ref" href="#f4">[4]</a></p>"""),
  ("datos", "Datos personales", """
<p>Los datos de quien pregunta y, más todavía, los de quien aparta una unidad, se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a> Ten el aviso de privacidad a la mano en el chat.</p>
<p>El seguimiento de preventa y renta está en la guía de <a href="/guias/crm-inmobiliaria-seguimiento-leads/">CRM para inmobiliarias</a>. Lo que hacemos en la ciudad está en <a href="/negocios/guadalajara/real-estate/">inmobiliarias en Guadalajara</a>.</p>"""),
 ],
 faq=[
  ("¿Cómo organizo los leads de una inmobiliaria en Guadalajara?", "Separa desde el primer mensaje preventa, reventa, renta y propietarios que quieren vender, porque cada uno necesita información y una persona distinta."),
  ("¿El agente puede contestar sobre una preventa?", "Sí, con la información que la desarrolladora ya publicó y revisó. Las preguntas de contrato, entrega o garantía van a una persona."),
  ("¿Puedo mandar recordatorio de la visita por WhatsApp?", "Sí, con una plantilla aprobada y el permiso del cliente, que conviene pedir al confirmar la cita."),
  ("¿Conviene una página por desarrollo?", "Sí. Quien busca un desarrollo o una zona quiere llegar a esa página, y el botón de WhatsApp ya lleva el contexto de lo que le interesa."),
 ],
 fuentes=["nom247", "lfpc", "wa_precios", "sch_rea", "lfpdppp"],
)

G["inmobiliarias-tulum-compradores-extranjeros"] = dict(
 titulo="Inmobiliarias en Tulum: cómo atender por WhatsApp a compradores extranjeros",
 corto="Inmobiliarias en Tulum y compradores extranjeros",
 desc="Cómo una inmobiliaria o desarrolladora en Tulum puede atender en inglés y en español a compradores de otros países, qué decir y qué no sobre el fideicomiso en la zona restringida, y cómo llevar el seguimiento con husos horarios distintos.",
 rubro=RE, audit="real-estate", og="og-real-estate.jpg",
 wa="Hola! Leí la guía de inmobiliarias en Tulum y compradores extranjeros y quiero el Audit de mi inmobiliaria.",
 bajada="En Tulum, buena parte de quien pregunta por un departamento o un terreno escribe en inglés, desde otro país y a una hora en la que tu equipo ya duerme. Pregunta por el precio, por la renta vacacional y por cómo puede comprar un extranjero cerca de la playa. Esta guía explica cómo contestar rápido sin dar asesoría legal que no te corresponde.",
 cuerpo=[
  ("idioma", "Contesta en el idioma en que te escriben", """
<p>Un agente con IA puede detectar el idioma del primer mensaje y seguir en ese idioma, en inglés, español o el que use el cliente. Lo que no puede hacer es traducir mal la ficha de la propiedad: conviene que la inmobiliaria cargue la información en los idiomas que atiende y que el agente responda con eso.</p>
<p>Con la API de WhatsApp, las plantillas para escribir fuera de la ventana de 24 horas se aprueban por idioma.<a class="ref" href="#f1">[1]</a> Si atiendes en inglés y en español, prepara las dos versiones del recordatorio de visita o del aviso de unidad disponible.</p>"""),
  ("fideicomiso", "Fideicomiso: informar sin asesorar", """
<p>La Constitución define una zona restringida de 50 kilómetros a lo largo de las playas en la que los extranjeros no adquieren el dominio directo de tierras.<a class="ref" href="#f2">[2]</a> La Ley de Inversión Extranjera permite que adquieran derechos sobre inmuebles en esa zona mediante un fideicomiso con una institución de crédito.<a class="ref" href="#f3">[3]</a></p>
<div class="aviso">En la práctica: el agente puede explicar que existe esta figura y ofrecer que un asesor y el notario den el detalle. No debe decir cuánto cuesta, cuánto tarda ni si una operación concreta es viable.</div>"""),
  ("horarios", "Husos horarios y seguimiento", """
<p>Si el cliente escribe de noche desde otro país, el agente contesta al momento y deja la conversación lista para que el asesor la retome al empezar el día: qué propiedad, qué presupuesto, si quiere comprar para vivir o para rentar y cuándo viaja a Tulum. Cuando el cliente vuelve a escribir, se abre otra vez la ventana de 24 horas.<a class="ref" href="#f1">[1]</a></p>"""),
  ("renta", "La pregunta de la renta vacacional", """
<p>Casi todo comprador extranjero pregunta cuánto puede rentar la unidad. Es la pregunta en la que más fácil se promete de más. El agente no debe dar rendimientos ni ocupaciones esperadas: si la inmobiliaria tiene números reales de unidades que administra, que los entregue una persona, con su origen y su fecha.</p>"""),
  ("precio", "Precio y datos", """
<p>El precio que se informe tiene que ser el total, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f4">[4]</a> Los datos de compradores extranjeros también se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a></p>
<p>Para el seguimiento de cada lead, mira la guía de <a href="/guias/crm-inmobiliaria-seguimiento-leads/">CRM para inmobiliarias</a>. Lo que hacemos en la ciudad está en <a href="/negocios/tulum/real-estate/">inmobiliarias en Tulum</a>.</p>"""),
 ],
 faq=[
  ("¿Un extranjero puede comprar un departamento en Tulum?", "En la zona restringida de 50 kilómetros desde la playa, la Ley de Inversión Extranjera permite adquirir derechos mediante un fideicomiso con un banco. El detalle de cada operación lo da un notario."),
  ("¿El agente de WhatsApp puede atender en inglés?", "Sí. Puede seguir la conversación en el idioma del cliente, con la información que la inmobiliaria cargó en ese idioma."),
  ("¿El agente puede decir cuánto rinde la renta vacacional?", "No conviene. Cualquier número de ocupación o renta lo da una persona, con datos reales y su origen."),
  ("¿Las plantillas de WhatsApp se aprueban por idioma?", "Sí. Si atiendes en inglés y en español, necesitas una versión aprobada de cada plantilla en cada idioma."),
 ],
 fuentes=["wa_precios", "cpeum27", "lie", "lfpc", "lfpdppp"],
)

G["reservas-whatsapp-bares-antros-cdmx"] = dict(
 titulo="Reservas por WhatsApp para bares y antros en CDMX: mesas, listas y grupos",
 corto="Reservas por WhatsApp para bares y antros en CDMX",
 desc="Cómo un bar o antro en Ciudad de México puede tomar reservas de mesa, armar la lista de la puerta y atender cumpleaños y grupos por WhatsApp a cualquier hora, con las reglas de Meta y lo que pide la ley sobre el precio.",
 rubro=GA, audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de reservas por WhatsApp para bares y antros en CDMX y quiero el Audit de mi bar.",
 bajada="En un bar de la Roma o un antro en Polanco, las consultas llegan cuando nadie puede contestar: el jueves en la tarde, el sábado a medianoche. «Somos ocho para un cumpleaños, ¿tienen mesa?» Si la respuesta tarda, el grupo ya está en otra lista. Esta guía explica qué automatizar y qué dejar siempre a una persona.",
 cuerpo=[
  ("consultas", "Las consultas de siempre", """
<div class="tabla"><table><thead><tr><th>Consulta</th><th>Lo que debe hacer el agente</th></tr></thead><tbody>
<tr><td>Mesa para hoy o el fin de semana</td><td>Ver la disponibilidad que cargó el bar y reservar, o pasar a la persona de reservas</td></tr>
<tr><td>Lista de la puerta</td><td>Tomar nombre y número de personas y sumarlos a la lista</td></tr>
<tr><td>Cumpleaños y grupos</td><td>Pedir fecha, personas y qué buscan, y pasar a una persona para la propuesta</td></tr>
<tr><td>Consumo mínimo o cover</td><td>Responder con el precio total vigente que cargó el bar</td></tr>
<tr><td>Quejas o algo que pasó en el lugar</td><td>Pasar a una persona siempre</td></tr>
</tbody></table></div>"""),
  ("precio", "Cover y consumo mínimo, claros", """
<p>Si hay cover, consumo mínimo o un paquete para la mesa, el agente tiene que decirlo con el precio total, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f1">[1]</a> Un precio que cambia en la puerta es la peor reseña posible. Que el bar actualice esos datos antes de cada fin de semana y el agente conteste solo con eso.</p>"""),
  ("whatsapp", "Reglas de WhatsApp", """
<p>Para un agente que entienda lo que escribe el cliente se usa la plataforma de WhatsApp Business, la API.<a class="ref" href="#f2">[2]</a> Cada mensaje abre una ventana de 24 horas para contestar libremente. El recordatorio de la reserva o el aviso del evento del próximo viernes salen fuera de esa ventana y necesitan plantilla aprobada y permiso del cliente.<a class="ref" href="#f3">[3]</a> Mandar promociones a quien no lo aceptó va contra la política de WhatsApp Business.<a class="ref" href="#f4">[4]</a></p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 23:10</span>
<span class="yo">Hola, somos 8 para un cumpleaños el sábado, ¿hay mesa?</span>
<span class="bot">¡Hola! Para el sábado tengo mesa para 8 desde las 22:00. ¿A nombre de quién la aparto? Si quieres, te aviso por aquí el viernes para confirmar. Soy el asistente con IA del bar.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("google", "Que te encuentren el viernes", """
<p>«Bar con terraza en la Condesa» o «antro en Polanco» se resuelve en el mapa. Google ordena esos resultados por relevancia, distancia y prominencia.<a class="ref" href="#f5">[5]</a> Horario real de cada día, fotos actuales, categoría correcta y respuestas a las reseñas pesan. En tu página, los datos estructurados de bar dicen dirección, horario y si aceptan reservas.<a class="ref" href="#f6">[6]</a></p>"""),
  ("datos", "Datos de la lista", """
<p>Nombres y teléfonos de la lista son datos personales y se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f7">[7]</a> Úsalos para lo que el cliente aceptó, la reserva y los avisos que pidió.</p>
<p>Para elegir proveedor, sigue con la guía de <a href="/guias/chatbot-whatsapp-restaurantes/">cómo elegir un chatbot de WhatsApp que sí reserve</a>. Lo que hacemos en la ciudad está en <a href="/negocios/ciudad-de-mexico/gastronomia/">gastronomía en Ciudad de México</a>.</p>"""),
 ],
 faq=[
  ("¿Un bar puede tomar reservas automáticas por WhatsApp?", "Sí, con un agente conectado a la API de WhatsApp Business y a la disponibilidad que carga el bar. Los grupos grandes y las quejas pasan a una persona."),
  ("¿El agente puede armar la lista de la puerta?", "Sí. Toma nombre y número de personas y los suma a la lista que ve el equipo de la puerta."),
  ("¿Tengo que informar el cover por WhatsApp?", "Si preguntan, el agente debe responder con el precio total vigente, como pide la Ley Federal de Protección al Consumidor."),
  ("¿Puedo mandar promociones del fin de semana por WhatsApp?", "Solo a quien aceptó recibirlas y con una plantilla aprobada por Meta."),
 ],
 fuentes=["lfpc", "wa_api", "wa_precios", "wa_politica", "gbp_rank", "sch_bar", "lfpdppp"],
)

G["reservas-mesas-bares-antros-monterrey"] = dict(
 titulo="Reservas de mesa para bares y antros en Monterrey: del DM a la lista",
 corto="Reservas de mesa para bares y antros en Monterrey",
 desc="Cómo un bar o antro en Monterrey puede convertir los DMs de Instagram y los mensajes de WhatsApp en mesas confirmadas para el fin de semana, con la ventana de 24 horas de Meta y el precio total claro.",
 rubro=GA, audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de reservas para bares y antros en Monterrey y quiero el Audit de mi bar.",
 bajada="En Monterrey la noche se decide por Instagram. El cartel del sábado sale el miércoles, y los DMs empiezan a llegar: «¿mesa para seis?», «¿hay paquete de botella?», «¿hasta qué hora es la lista?». Si los contesta quien tenga el celular a mano, la mitad se pierde. Esta guía explica cómo llevar esas consultas a una mesa confirmada.",
 cuerpo=[
  ("dm", "El DM es donde empieza la reserva", """
<p>Un agente conectado a la API de mensajes de Instagram puede contestar los DMs y las respuestas a tus historias al momento.<a class="ref" href="#f1">[1]</a> La regla clave es la ventana: puedes contestar libremente durante las 24 horas siguientes al último mensaje del cliente. Pasado ese plazo, solo una persona del equipo puede seguir, con la etiqueta de agente humano, hasta siete días.<a class="ref" href="#f1">[1]</a></p>
<p>Por eso conviene que la conversación termine en algo concreto el mismo día: la mesa confirmada o el número de WhatsApp para el recordatorio.</p>"""),
  ("flujo", "De la pregunta a la mesa", """
<div class="tabla"><table><thead><tr><th>Paso</th><th>Qué hace el agente</th></tr></thead><tbody>
<tr><td>1. Pregunta</td><td>Contesta qué hay esa noche, horario y si hay mesa para ese número de personas</td></tr>
<tr><td>2. Condiciones</td><td>Informa paquete o consumo mínimo con el precio total que cargó el bar</td></tr>
<tr><td>3. Datos</td><td>Pide nombre, personas y hora de llegada</td></tr>
<tr><td>4. Confirmación</td><td>Aparta la mesa o pasa a la persona de reservas si hace falta</td></tr>
<tr><td>5. Recordatorio</td><td>Pide permiso para avisar por WhatsApp el día anterior</td></tr>
</tbody></table></div>
<p>El recordatorio por WhatsApp sale fuera de la ventana de 24 horas, así que necesita plantilla aprobada.<a class="ref" href="#f2">[2]</a></p>"""),
  ("precio", "Paquetes y precio total", """
<p>Paquetes de botella, consumo mínimo o cover se informan con el precio total, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f3">[3]</a> Que el agente responda solo con lo que el bar cargó para esa noche, y que una persona confirme los grupos grandes.</p>"""),
  ("mapa", "En el mapa y en tu página", """
<p>Quien busca «bar en San Pedro» o «antro en Barrio Antiguo» decide en el mapa. Google ordena los resultados locales por relevancia, distancia y prominencia.<a class="ref" href="#f4">[4]</a> Mantén el horario real, las fotos de la temporada y responde las reseñas. En tu página, los datos estructurados de bar ordenan dirección, horario y reservas.<a class="ref" href="#f5">[5]</a></p>"""),
  ("datos", "Datos de quien reserva", """
<p>Nombre y teléfono de quien reserva son datos personales, regidos por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f6">[6]</a></p>
<p>Si además tienes cocina y reservas de comida, mira la guía de <a href="/guias/reservas-instagram-restaurantes-monterrey/">reservas por Instagram para restaurantes en Monterrey</a>. Lo que hacemos en la ciudad está en <a href="/negocios/monterrey/gastronomia/">gastronomía en Monterrey</a>.</p>"""),
 ],
 faq=[
  ("¿Puedo automatizar las reservas que llegan por DM de Instagram?", "Sí, con una cuenta profesional conectada a la API de mensajes de Instagram. El agente contesta dentro de las 24 horas desde el último mensaje del cliente."),
  ("¿Qué pasa si el cliente contesta dos días después?", "Pasadas las 24 horas, solo una persona del equipo puede seguir la conversación con la etiqueta de agente humano, hasta siete días."),
  ("¿El agente puede informar paquetes de botella?", "Sí, con el precio total que el bar cargó para esa noche. Los grupos grandes los confirma una persona."),
  ("¿Cómo mando el recordatorio de la mesa?", "Por WhatsApp, con una plantilla aprobada y el permiso del cliente, que conviene pedir al confirmar."),
 ],
 fuentes=["ig_api", "wa_precios", "lfpc", "gbp_rank", "sch_bar", "lfpdppp"],
)

G["cotizaciones-salones-eventos-guadalajara"] = dict(
 titulo="Cotizaciones para salones de eventos en Guadalajara: bodas, XV años y empresas",
 corto="Cotizaciones para salones de eventos en Guadalajara",
 desc="Cómo un salón o jardín de eventos en Guadalajara y Zapopan puede contestar al momento las consultas de bodas, XV años y eventos de empresa, revisar fechas libres y mandar la cotización el mismo día.",
 rubro=EV, audit="eventos", og="og-eventos.jpg",
 wa="Hola! Leí la guía de cotizaciones para salones de eventos en Guadalajara y quiero el Audit de mi salón.",
 bajada="Quien organiza una boda o unos XV años en Guadalajara le escribe a varios salones el mismo fin de semana, con la misma pregunta: «¿tienen libre el 14 de marzo para 200 personas?». El salón que contesta primero con la fecha y una propuesta clara se queda con la visita. Esta guía explica cómo responder ese primer mensaje sin que nadie del equipo esté pegado al teléfono.",
 cuerpo=[
  ("primer-mensaje", "Lo que se resuelve en el primer mensaje", """
<p>Para cotizar, el salón necesita lo mismo casi siempre. Un agente puede pedirlo de forma natural en la primera conversación y revisar si la fecha está libre en el calendario que lleva el salón.</p>
<div class="tabla"><table><thead><tr><th>Dato</th><th>Para qué sirve</th></tr></thead><tbody>
<tr><td>Tipo de evento</td><td>Boda, XV años, bautizo, posada o evento de empresa cambian el paquete</td></tr>
<tr><td>Fecha y horario</td><td>Saber si está libre antes de seguir</td></tr>
<tr><td>Número de invitados</td><td>Elegir salón o jardín y armar la propuesta</td></tr>
<tr><td>Qué necesitan</td><td>Solo el espacio, banquete, mobiliario o todo incluido</td></tr>
</tbody></table></div>"""),
  ("cotizacion", "Cotización el mismo día", """
<p>El agente no arma la propuesta final: la arma una persona con esos datos. Lo que sí hace es que la persona la reciba completa, ordenada y en el momento, para mandar la cotización el mismo día y ofrecer la visita al salón.</p>
<p>Si en la cotización hay precios, tienen que ser totales, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f1">[1]</a> El anticipo, lo que incluye y las condiciones de cancelación conviene dejarlos por escrito.</p>"""),
  ("whatsapp", "Seguimiento con las reglas de WhatsApp", """
<p>Entre la cotización y el anticipo pasan días o semanas. Dentro de las 24 horas desde el último mensaje del cliente contestas libremente; después, cualquier seguimiento sale con una plantilla aprobada y con su permiso.<a class="ref" href="#f2">[2]</a> La política de WhatsApp Business no permite escribir a quien no aceptó.<a class="ref" href="#f3">[3]</a></p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 21:05</span>
<span class="yo">Hola, ¿tienen libre el 14 de marzo para unos XV años, como 200 personas?</span>
<span class="bot">¡Hola! El 14 de marzo tenemos libre el jardín, con capacidad para ese número. ¿Buscan solo el espacio o con banquete? Con eso, mañana temprano te mandamos la cotización. Soy el asistente con IA del salón.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("google", "Que te encuentren en Zapopan y Tlaquepaque", """
<p>«Salón de eventos en Zapopan» o «jardín para bodas en Tlajomulco» son búsquedas locales que Google ordena por relevancia, distancia y prominencia.<a class="ref" href="#f4">[4]</a> Fotos reales de eventos, capacidad en texto y respuestas a las reseñas cuentan. En tu página, los datos estructurados de recinto de eventos ordenan dirección y capacidad.<a class="ref" href="#f5">[5]</a></p>"""),
  ("datos", "Datos de los clientes", """
<p>Los datos de quien cotiza se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f6">[6]</a></p>
<p>Para ver qué más puede hacer la IA en el rubro, sigue con <a href="/guias/como-usar-ia-en-eventos/">cómo usar IA en una empresa de eventos</a>. Lo que hacemos en la ciudad está en <a href="/negocios/guadalajara/eventos/">eventos en Guadalajara</a>.</p>"""),
 ],
 faq=[
  ("¿Un agente puede revisar si la fecha está libre?", "Sí, si está conectado al calendario que lleva el salón. Si no lo está, toma los datos y avisa a una persona."),
  ("¿El agente manda la cotización?", "Pide los datos y los ordena. La propuesta la arma una persona del equipo, para mandarla el mismo día."),
  ("¿Puedo dar seguimiento por WhatsApp a una cotización?", "Sí. Dentro de las 24 horas desde el último mensaje del cliente contestas libremente; después necesitas una plantilla aprobada y su permiso."),
  ("¿Tengo que poner precios totales en la cotización?", "Sí. La Ley Federal de Protección al Consumidor pide informar el precio total."),
 ],
 fuentes=["lfpc", "wa_precios", "wa_politica", "gbp_rank", "sch_venue", "lfpdppp"],
)

G["salones-eventos-monterrey-apartar-fechas"] = dict(
 titulo="Salones de eventos en Monterrey: agendar visitas y apartar fechas por WhatsApp",
 corto="Salones de eventos en Monterrey: visitas y fechas",
 desc="Cómo un salón o quinta de eventos en Monterrey puede pasar de la consulta a la visita agendada y a la fecha apartada por WhatsApp, con recordatorios y seguimiento que respetan las reglas de Meta.",
 rubro=EV, audit="eventos", og="og-eventos.jpg",
 wa="Hola! Leí la guía de salones de eventos en Monterrey y quiero el Audit de mi salón.",
 bajada="En Monterrey un salón no se contrata por chat: se contrata después de verlo. El trabajo del WhatsApp es llevar a la familia o a la empresa a la visita, y de la visita al anticipo. Lo que se pierde está en el medio: la visita que nadie confirmó, la cotización que nadie siguió, la fecha que se fue con otro. Esta guía explica cómo cubrir ese tramo.",
 cuerpo=[
  ("visita", "La visita es el objetivo", """
<p>En la primera conversación, el agente revisa si la fecha está libre, pide tipo de evento y número de invitados, y ofrece horarios reales de visita. Si la persona elige uno, queda agendada en el mismo chat, con la ubicación de la quinta o el salón.</p>"""),
  ("recordatorio", "Recordatorio y confirmación", """
<p>El recordatorio del día anterior a la visita sale fuera de la ventana de 24 horas, así que necesita una plantilla aprobada por Meta y el permiso del cliente.<a class="ref" href="#f1">[1]</a> Pídelo al agendar. Si la persona responde al recordatorio, se abre otra ventana y el agente puede contestar sus dudas antes de llegar.</p>"""),
  ("apartar", "De la visita a la fecha apartada", """
<div class="tabla"><table><thead><tr><th>Momento</th><th>Quién actúa</th></tr></thead><tbody>
<tr><td>Después de la visita</td><td>El agente manda el resumen de lo que se vio y pregunta si quedó alguna duda</td></tr>
<tr><td>Cotización</td><td>Una persona arma la propuesta con precios totales</td></tr>
<tr><td>Fecha en espera</td><td>Una persona define cuánto tiempo se sostiene la fecha sin anticipo y lo deja por escrito</td></tr>
<tr><td>Anticipo</td><td>Una persona confirma el pago y el agente manda el comprobante y los siguientes pasos</td></tr>
</tbody></table></div>
<p>Los precios de la cotización tienen que ser totales, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f2">[2]</a></p>"""),
  ("reglas", "Lo que no conviene automatizar", """
<p>Negociar el precio, mover una fecha ya apartada y atender un problema el día del evento son trabajo de una persona. La política de WhatsApp Business además pide no escribir a quien no lo aceptó y respetar cuando alguien pide dejar de recibir mensajes.<a class="ref" href="#f3">[3]</a></p>"""),
  ("mapa", "En el mapa de San Pedro, Santa Catarina o Apodaca", """
<p>Las búsquedas de salones son locales y Google las ordena por relevancia, distancia y prominencia.<a class="ref" href="#f4">[4]</a> Capacidad, estacionamiento y tipos de evento en texto, fotos reales y reseñas respondidas. Los datos de la familia o la empresa se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a></p>
<p>Para el resto de lo que puede hacer la IA en el rubro, mira <a href="/guias/como-usar-ia-en-eventos/">cómo usar IA en una empresa de eventos</a> y la guía de <a href="/guias/cotizaciones-salones-eventos-guadalajara/">cotizaciones para salones de eventos</a>. Lo que hacemos en la ciudad está en <a href="/negocios/monterrey/eventos/">eventos en Monterrey</a>.</p>"""),
 ],
 faq=[
  ("¿El agente puede agendar visitas al salón?", "Sí. Revisa si la fecha está libre, ofrece horarios reales de visita y la deja agendada en el mismo chat."),
  ("¿Puedo mandar recordatorio de la visita?", "Sí, con una plantilla aprobada por Meta y con el permiso del cliente, que conviene pedir al agendar."),
  ("¿El agente aparta la fecha?", "No. Cuánto tiempo se sostiene una fecha y el anticipo los define y confirma una persona."),
  ("¿Qué no conviene automatizar en un salón?", "Negociar el precio, mover una fecha apartada y atender problemas el día del evento."),
 ],
 fuentes=["wa_precios", "lfpc", "wa_politica", "gbp_rank", "lfpdppp"],
)

G["cafeterias-cdmx-pedidos-whatsapp-google-maps"] = dict(
 titulo="Cafeterías en CDMX: pedidos por WhatsApp y aparecer en Google Maps",
 corto="Cafeterías en CDMX: WhatsApp y Google Maps",
 desc="Cómo una cafetería en Ciudad de México puede aparecer cuando buscan café de especialidad en su colonia, tomar pedidos para llevar por WhatsApp sin frenar la barra y avisar a sus clientes frecuentes con permiso.",
 rubro=GA, audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de cafeterías en CDMX y quiero el Audit de mi cafetería.",
 bajada="En la Roma, la Condesa o Coyoacán hay una cafetería por cuadra. Quien busca «café de especialidad cerca» elige en el mapa en segundos, y quien ya te conoce quiere pedir su latte para llevar sin hacer fila. Las dos cosas pasan por el celular y casi nunca hay alguien libre para atenderlo. Esta guía explica cómo resolverlo sin frenar la barra.",
 cuerpo=[
  ("mapa", "El mapa decide", """
<p>Google ordena los resultados locales por relevancia, distancia y prominencia.<a class="ref" href="#f1">[1]</a> Para una cafetería eso se traduce en cosas concretas:</p>
<ul>
<li>Categoría exacta en tu Perfil de Empresa, horario real de cada día y fotos actuales de la barra y del espacio.</li>
<li>Lo que te distingue escrito en texto: tueste propio, métodos, opciones sin lácteos, enchufes para trabajar, si aceptan mascotas.</li>
<li>Respuesta a todas las reseñas, también las malas.</li>
</ul>
<p>En tu página, los datos estructurados de cafetería ordenan dirección, horario y menú.<a class="ref" href="#f2">[2]</a></p>"""),
  ("pedidos", "Pedidos para llevar sin frenar la barra", """
<p>Un agente de WhatsApp puede tomar el pedido completo, confirmar la hora de recogida y pasarlo a la barra o a tu sistema, para que quien prepara no tenga que contestar el celular. Si tienes catálogo cargado, el agente puede mandarlo dentro del chat.<a class="ref" href="#f3">[3]</a></p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 08:12</span>
<span class="yo">Hola, ¿me preparan un flat white con leche de avena para las 8:30?</span>
<span class="bot">¡Claro! Flat white con avena, listo a las 8:30 a tu nombre. Te esperamos en la barra. Soy el asistente con IA de la cafetería.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("frecuentes", "Clientes frecuentes, con permiso", """
<p>El cliente que viene todos los días es el que más vale. Avisarle de un grano nuevo o de un horario especial por WhatsApp es posible, pero sale fuera de la ventana de 24 horas: necesita una plantilla aprobada y que el cliente haya aceptado recibir esos mensajes.<a class="ref" href="#f4">[4]</a> La política de WhatsApp Business no permite escribir a quien no lo aceptó.<a class="ref" href="#f5">[5]</a> Pide el permiso en el mismo chat del pedido, con una línea clara.</p>"""),
  ("precio", "Precios y datos", """
<p>Si el agente da precios, son totales, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f6">[6]</a> Nombres y teléfonos de tus clientes son datos personales, regidos por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f7">[7]</a></p>
<p>Para elegir proveedor, mira la guía de <a href="/guias/chatbot-whatsapp-restaurantes/">cómo elegir un chatbot de WhatsApp</a>. Lo que hacemos en la ciudad está en <a href="/negocios/ciudad-de-mexico/gastronomia/">gastronomía en Ciudad de México</a>.</p>"""),
 ],
 faq=[
  ("¿Cómo aparece mi cafetería en Google Maps?", "Con un Perfil de Empresa completo: categoría exacta, horario real, fotos actuales, lo que te distingue en texto y respuesta a las reseñas."),
  ("¿Puedo tomar pedidos para llevar por WhatsApp?", "Sí. Un agente toma el pedido, confirma la hora de recogida y lo pasa a la barra sin que nadie conteste el celular."),
  ("¿Puedo avisar a mis clientes frecuentes por WhatsApp?", "Sí, si aceptaron recibir esos mensajes, con una plantilla aprobada por Meta."),
  ("¿Sirve el catálogo de WhatsApp para una cafetería?", "Sí. El agente puede mandar el catálogo dentro del chat para que el cliente elija."),
 ],
 fuentes=["gbp_rank", "sch_cafe", "wa_catalogo", "wa_precios", "wa_politica", "lfpc", "lfpdppp"],
)

G["estudios-pilates-monterrey-reservas-clases"] = dict(
 titulo="Estudios de pilates en Monterrey: reservas de clase y lista de espera por WhatsApp",
 corto="Estudios de pilates en Monterrey: reservas y lista de espera",
 desc="Cómo un estudio de pilates reformer en Monterrey puede tomar reservas de clase, llenar lugares cancelados con lista de espera y responder DMs al momento, con las reglas de WhatsApp, Instagram y la ley sobre precios.",
 rubro=FI, audit="fitness", og="og-fitness.jpg",
 wa="Hola! Leí la guía de estudios de pilates en Monterrey y quiero el Audit de mi estudio.",
 bajada="En un estudio de pilates reformer cada clase tiene pocos lugares. Una cancelación de último minuto es un reformer vacío, y una consulta por DM que tarda en contestarse es una alumna que se va al estudio de San Pedro o de Cumbres que respondió antes. Esta guía explica cómo usar WhatsApp e Instagram para que los lugares se llenen.",
 cuerpo=[
  ("reservas", "Reservar en el mismo chat", """
<p>Un agente de WhatsApp puede mostrar los lugares libres de cada clase, reservar y confirmar, si está conectado al sistema de reservas del estudio. Si el estudio usa una app de reservas, el agente responde las dudas y manda el enlace a la clase exacta.</p>"""),
  ("espera", "Lista de espera que se mueve sola", """
<div class="tabla"><table><thead><tr><th>Momento</th><th>Qué hace el agente</th></tr></thead><tbody>
<tr><td>Clase llena</td><td>Ofrece entrar a la lista de espera y pide permiso para avisar</td></tr>
<tr><td>Alguien cancela</td><td>Avisa a la primera persona de la lista y le da un tiempo para confirmar</td></tr>
<tr><td>No confirma</td><td>Pasa a la siguiente de la lista</td></tr>
<tr><td>Política de cancelación</td><td>La recuerda con la que fijó el estudio, sin cambiarla</td></tr>
</tbody></table></div>
<p>El aviso de lugar libre suele salir fuera de la ventana de 24 horas, así que necesita una plantilla aprobada y el permiso de la alumna.<a class="ref" href="#f1">[1]</a></p>"""),
  ("dm", "Los DMs de Instagram", """
<p>En pilates, Instagram es la vitrina. Un agente conectado a la API de mensajes de Instagram contesta los DMs y las respuestas a historias al momento, dentro de las 24 horas desde el último mensaje.<a class="ref" href="#f2">[2]</a> Que termine en algo concreto: la clase muestra reservada o el WhatsApp para seguir.</p>"""),
  ("precio", "Paquetes y precio total", """
<p>Si el agente informa paquetes de clases o membresías, el precio tiene que ser total, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f3">[3]</a> Vigencia de los paquetes y política de cancelación, por escrito y las mismas en el chat, la app y el mostrador.</p>"""),
  ("salud", "Lesiones y datos de salud", """
<p>Muchas alumnas preguntan si pueden tomar clase con una lesión o durante el embarazo. Esa respuesta la da una instructora, nunca el agente. Los datos sobre salud son datos personales sensibles para la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f4">[4]</a> No los pidas por el chat del agente.</p>
<p>Sigue con la guía de <a href="/guias/retencion-socios-gimnasio-reservas-clases/">retención de socios y reservas de clase</a> y la de <a href="/guias/responder-dms-instagram-automaticamente-gimnasios/">cómo responder DMs de Instagram</a>. Lo que hacemos en la ciudad está en <a href="/negocios/monterrey/fitness/">gimnasios y estudios en Monterrey</a>.</p>"""),
 ],
 faq=[
  ("¿Puedo tomar reservas de pilates por WhatsApp?", "Sí, con un agente conectado al sistema de reservas del estudio, o que mande el enlace a la clase exacta si usas una app."),
  ("¿Cómo funciona una lista de espera por WhatsApp?", "Cuando alguien cancela, el agente avisa a la primera persona de la lista, le da un tiempo para confirmar y si no, pasa a la siguiente."),
  ("¿El agente puede responder si puedo tomar clase con una lesión?", "No. Esa respuesta la da una instructora, y los datos de salud no se piden por el chat del agente."),
  ("¿Tengo que dar el precio total de los paquetes?", "Sí. La Ley Federal de Protección al Consumidor pide informar el precio total."),
 ],
 fuentes=["wa_precios", "ig_api", "lfpc", "lfpdppp"],
)

G["pedidos-recurrentes-whatsapp-distribuidoras"] = dict(
 titulo="Pedidos recurrentes por WhatsApp para distribuidoras: recompra, corte y ruta",
 corto="Pedidos recurrentes por WhatsApp para distribuidoras",
 desc="Cómo una distribuidora o mayorista puede tomar por WhatsApp los pedidos de sus clientes de siempre, con catálogo, horario de corte y ruta de entrega, y recordar la recompra con permiso y plantillas aprobadas.",
 rubro=DI, audit="distribucion", og="og-distribucion.jpg",
 wa="Hola! Leí la guía de pedidos recurrentes por WhatsApp para distribuidoras y quiero el Audit de mi distribuidora.",
 bajada="La mayoría de los pedidos de una distribuidora no son nuevos: son la tienda de abarrotes, el restaurante o la ferretería de siempre pidiendo lo mismo que la semana pasada, por WhatsApp, a la hora que pueden. El problema no es vender, es que ese pedido llegue completo, antes del corte y a la ruta correcta. Esta guía explica cómo ordenarlo.",
 cuerpo=[
  ("recompra", "El pedido de siempre, en un mensaje", """
<p>Un agente puede reconocer al cliente por su número, recordarle lo que pidió la última vez y preguntar si repite o cambia algo. Lo que necesita es tener a mano el historial de pedidos y el catálogo vigente con existencias.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 18:40</span>
<span class="yo">Buenas, lo mismo de la otra semana pero 2 cajas más de aceite.</span>
<span class="bot">¡Buenas! Queda igual que el pedido anterior con 2 cajas más de aceite. Entra antes del corte, así que sale en la ruta del jueves. ¿Lo confirmo? Soy el asistente con IA de la distribuidora.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("catalogo", "Catálogo dentro del chat", """
<p>La API de WhatsApp permite tener un catálogo y mandar mensajes con uno o varios productos para que el cliente elija sin salir del chat.<a class="ref" href="#f1">[1]</a> Para una distribuidora, sirve para el cliente que quiere probar algo nuevo; para el que repite, el atajo es el pedido anterior.</p>"""),
  ("corte", "Horario de corte y ruta", """
<div class="tabla"><table><thead><tr><th>Regla</th><th>Qué hace el agente</th></tr></thead><tbody>
<tr><td>Horario de corte</td><td>Dice si el pedido entra en la siguiente ruta o en la otra</td></tr>
<tr><td>Zona del cliente</td><td>Asigna el día de entrega que le toca</td></tr>
<tr><td>Sin existencia</td><td>Avisa y ofrece el sustituto que definió la distribuidora, o pasa a un vendedor</td></tr>
<tr><td>Crédito o saldo vencido</td><td>Pasa a una persona, sin negar ni aprobar nada</td></tr>
</tbody></table></div>"""),
  ("recordatorio", "Recordar la recompra, con permiso", """
<p>Escribirle al cliente que suele pedir cada semana y esta vez no pidió es de lo más útil que puede hacer una distribuidora. Ese mensaje sale fuera de la ventana de 24 horas, así que necesita una plantilla aprobada y que el cliente haya aceptado recibir esos avisos.<a class="ref" href="#f2">[2]</a> La política de WhatsApp Business no permite escribir a listas compradas.<a class="ref" href="#f3">[3]</a></p>"""),
  ("precios", "Precios y datos", """
<p>Los precios que dé el agente tienen que ser los vigentes y totales, como pide la Ley Federal de Protección al Consumidor cuando aplica.<a class="ref" href="#f4">[4]</a> Los datos de contacto de tus clientes se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a></p>
<p>Para pedidos nuevos que necesitan cotización, sigue con la guía de <a href="/guias/pedidos-whatsapp-cotizaciones-distribuidoras/">pedidos por WhatsApp a cotización</a>. Para el resto, mira <a href="/guias/como-usar-ia-en-una-distribuidora/">cómo usar IA en una distribuidora</a>.</p>"""),
 ],
 faq=[
  ("¿Un agente puede tomar el pedido de siempre por WhatsApp?", "Sí, si tiene el historial de pedidos y el catálogo con existencias. Reconoce al cliente, le recuerda el último pedido y confirma cambios."),
  ("¿Puede avisar si el pedido entra antes del corte?", "Sí. Con el horario de corte y las zonas de ruta, dice en qué entrega sale el pedido."),
  ("¿Puedo recordar la recompra a un cliente que no pidió?", "Sí, si aceptó recibir esos avisos, con una plantilla aprobada por Meta."),
  ("¿El agente puede aprobar crédito?", "No. Crédito y saldos vencidos pasan siempre a una persona."),
 ],
 fuentes=["wa_catalogo", "wa_precios", "wa_politica", "lfpc", "lfpdppp"],
)

# ---- 3 guias nuevas (22/11/2026) ----
F["sch_hotel"] = ("Schema.org, tipo «Hotel».", "https://schema.org/Hotel")
F["g_hreflang"] = ("Google Search Central, «Indicarle a Google las versiones traducidas de tus paginas (hreflang)».", "https://developers.google.com/search/docs/specialty/international/localized-versions")

HO = ("Hospitality", "/hospitality/")

G["confirmar-reservas-whatsapp-restaurantes-cdmx"] = dict(
 fecha="2026-11-22", fecha_txt="22 de noviembre de 2026",
 titulo="Mesas que se reservan y no llegan: confirmación por WhatsApp para restaurantes en CDMX",
 titulo_seo="Confirmar reservas por WhatsApp en restaurantes de CDMX",
 corto="Confirmar reservas por WhatsApp en restaurantes de CDMX",
 desc="Cómo confirmar por WhatsApp las reservas de tu restaurante en CDMX, liberar las mesas que no llegan y cuándo pedir anticipo, con las reglas de Meta.",
 rubro=GA, audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de confirmación de reservas por WhatsApp para restaurantes en CDMX y quiero probar el agente 14 días.",
 bajada="Un sábado en la Roma tu restaurante está lleno en el papel y con dos mesas vacías a las nueve y media. Reservaron y no avisaron. Esas dos mesas son la diferencia del servicio, y la fila de la puerta ya se fue a otro lado. Esta guía explica cómo confirmar cada reserva por WhatsApp, liberar la mesa a tiempo y cuándo pedir anticipo.",
 cuerpo=[
  ("por-que", "Por qué una mesa se queda vacía", """
<p>Casi nadie reserva pensando en faltar. Reserva en tres lugares por si acaso, o se le hace tarde y no avisa porque le da pena. En Ciudad de México se suma el tráfico: una reserva de las 21:00 en Polanco que sale de Santa Fe a las 20:30 llega tarde o no llega.</p>
<p>La mesa no se pierde por el cliente que falta. Se pierde porque te enteras cuando ya pasó la hora, y a esa altura no alcanzas a sentar a nadie más.</p>"""),
  ("cuando", "Cuándo conviene confirmar", """
<div class="tabla"><table><thead><tr><th>Momento</th><th>Qué manda el agente</th><th>Para qué sirve</th></tr></thead><tbody>
<tr><td>Al reservar</td><td>Confirmación con fecha, hora, personas y la política de la casa</td><td>Que quede escrito lo que acordaron</td></tr>
<tr><td>El día anterior</td><td>Un mensaje que se responde con sí o no</td><td>Liberar con un día de aviso</td></tr>
<tr><td>Tres horas antes</td><td>Recordatorio corto con la dirección y el estacionamiento</td><td>Bajar el que llega tarde</td></tr>
<tr><td>Sin respuesta</td><td>Avisa que la mesa se guarda 15 minutos</td><td>Dejar la regla clara antes, no después</td></tr>
<tr><td>Cancelación</td><td>Libera el lugar en el sistema y ofrece el horario a la lista de espera</td><td>Volver a vender esa mesa</td></tr>
</tbody></table></div>"""),
  ("reglas", "Lo que permiten las reglas de WhatsApp", """
<p>Para mandar estos mensajes se usa la plataforma de WhatsApp Business, la API, a través de un proveedor o directamente con Meta.<a class="ref" href="#f1">[1]</a> Dentro de las 24 horas siguientes al último mensaje del cliente contestas libremente. El recordatorio del día anterior cae fuera de esa ventana, así que necesita una plantilla aprobada por Meta y que el cliente haya aceptado recibir tus mensajes.<a class="ref" href="#f2">[2]</a></p>
<div class="aviso">En la práctica: pide el permiso en el mismo chat donde se confirma la mesa. Una línea basta, y queda registrada en la conversación.</div>
<p>La política de mensajería de WhatsApp Business no permite escribir a listas compradas ni a quien no te dio su número.<a class="ref" href="#f3">[3]</a></p>"""),
  ("lista-espera", "La lista de espera es la otra mitad", """
<p>Confirmar sirve si tienes a quién sentar. Cuando alguien cancela, el agente avisa a la primera persona de la lista de espera de ese horario y le da un tiempo para confirmar. Si no contesta, pasa a la siguiente.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 12:10</span>
<span class="bot">¡Hola, Ana! Te recuerdo tu mesa para 4 mañana a las 21:00 en Álvaro Obregón. ¿La confirmas? Responde 1 para confirmar o 2 para cancelar.</span>
<span class="yo">2, se nos complicó</span>
<span class="bot">Listo, cancelada sin costo. Liberé la mesa y te aviso cuando tengamos lugar el próximo fin. Soy el asistente con IA del restaurante.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("anticipo", "Anticipo solo donde hace falta", """
<p>Pedir anticipo a todo el mundo espanta reservas. Donde sí conviene es en grupos grandes, mesas de ventana, fin de año y menús de degustación. Si cobras anticipo o depósito, el monto total tiene que estar informado desde el principio, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f4">[4]</a> Escribe la política de cancelación en el mismo mensaje en que pides el pago.</p>"""),
  ("medir", "Qué mirar cada semana", """
<ol class="lista">
<li>Cuántas reservas confirmaron, cuántas cancelaron con aviso y cuántas faltaron sin avisar.</li>
<li>Cuántas mesas liberadas se volvieron a vender con la lista de espera.</li>
<li>A qué hora y qué día se concentra el que no llega. Casi siempre hay un patrón.</li>
</ol>
<p>Si además quieres que el agente tome la reserva desde cero, está en la guía de <a href="/guias/chatbot-whatsapp-restaurantes-ciudad-de-mexico/">chatbot de WhatsApp para restaurantes en Ciudad de México</a>, y lo que debe hacer cualquier chatbot de restaurante, en <a href="/guias/chatbot-whatsapp-restaurantes/">cómo elegir uno que sí reserve</a>. Lo que hacemos en la ciudad está en <a href="/negocios/ciudad-de-mexico/gastronomia/">restaurantes y bares en Ciudad de México</a>.</p>"""),
  ("datos", "Datos de tus clientes", """
<p>Nombre, teléfono y la fecha de la reserva son datos personales, y en México los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a> Ten el aviso de privacidad a mano y usa esos datos solo para lo que le dijiste al cliente. Esta guía no reemplaza a un abogado.</p>"""),
 ],
 faq=[
  ("¿Puedo mandar recordatorios de reserva por WhatsApp?", "Sí, con una plantilla aprobada por Meta y el permiso del cliente, porque el recordatorio sale fuera de la ventana de 24 horas."),
  ("¿Cuándo conviene mandar la confirmación?", "Al reservar, el día anterior con una respuesta de sí o no, y un recordatorio corto unas horas antes del servicio."),
  ("¿Puedo cobrar anticipo por una reserva?", "Sí, y conviene en grupos grandes y fechas pico. El monto total y la política de cancelación tienen que estar informados desde el principio."),
  ("¿Qué hago con la mesa que se libera?", "Ofrecerla a la lista de espera de ese horario. El agente avisa a la primera persona y le da un tiempo para confirmar."),
  ("¿Puedo escribirle a clientes que nunca me dieron su número?", "No. La política de mensajería de WhatsApp Business no permite escribir a listas compradas ni a quien no te dio su contacto."),
 ],
 fuentes=["wa_api", "wa_precios", "wa_politica", "lfpc", "lfpdppp"],
)

G["cotizaciones-grupos-hoteles-cdmx-whatsapp"] = dict(
 fecha="2026-11-22", fecha_txt="22 de noviembre de 2026",
 titulo="Hoteles en CDMX: cotizar grupos y viajeros de negocios por WhatsApp sin perder la noche",
 titulo_seo="Cotizar grupos por WhatsApp en hoteles de CDMX",
 corto="Cotizar grupos por WhatsApp en hoteles de CDMX",
 desc="Cómo responder al momento las solicitudes de grupos y viajeros corporativos de tu hotel en CDMX y pasarlas a ventas completas, por WhatsApp e Instagram.",
 rubro=HO, audit="hospitality", og="og-hospitality.jpg",
 wa="Hola! Leí la guía de cotizaciones de grupos por WhatsApp para hoteles en CDMX y quiero probar el agente 14 días.",
 bajada="En un hotel de Ciudad de México una solicitud de grupo vale diez habitaciones, no una. Llega por WhatsApp un viernes a las once de la noche, desde una asistente que está armando un viaje de equipo o una boda. El que contesta primero cotiza; el que contesta el lunes queda fuera. Esta guía explica cómo responder siempre y pasarle la solicitud a ventas lista.",
 cuerpo=[
  ("que-llega", "Qué llega por el chat de un hotel en la capital", """
<p>En Ciudad de México conviven tres demandas distintas en el mismo número: el viajero de negocios que necesita factura y salida tarde, el grupo corporativo con salón y coffee break, y la familia que viene por una boda en Polanco o en el Centro. Cada uno pregunta distinto y a cada uno le urge distinto.</p>
<p>Lo que casi nunca se puede es cotizar un grupo de forma automática. Lo que sí se puede, y cambia el resultado, es que nadie se quede esperando y que ventas reciba la solicitud completa.</p>"""),
  ("calificar", "Las siete preguntas que arman una cotización", """
<div class="tabla"><table><thead><tr><th>Dato</th><th>Por qué lo pide el agente</th></tr></thead><tbody>
<tr><td>Fechas y noches</td><td>Define temporada y si hay bloqueo posible</td></tr>
<tr><td>Habitaciones y ocupación</td><td>Separa un grupo real de una consulta suelta</td></tr>
<tr><td>Motivo del viaje</td><td>Corporativo, boda, congreso o placer cambian la tarifa</td></tr>
<tr><td>Salón o alimentos</td><td>Es la mitad del ingreso de un grupo</td></tr>
<tr><td>Empresa y facturación</td><td>Evita rehacer todo al final</td></tr>
<tr><td>Quién decide y para cuándo</td><td>Ordena la prioridad de ventas</td></tr>
<tr><td>WhatsApp y correo</td><td>Permite seguir después de la ventana de 24 horas</td></tr>
</tbody></table></div>
<div class="aviso">En la práctica: el agente no manda tarifas de grupo. Toma los siete datos, confirma que una persona de ventas responde con la cotización y dice en cuánto tiempo.</div>"""),
  ("reglas", "Qué permiten WhatsApp e Instagram", """
<p>Para que un agente conteste el WhatsApp del hotel se usa la plataforma de WhatsApp Business, la API.<a class="ref" href="#f1">[1]</a> Dentro de las 24 horas siguientes al último mensaje contestas libremente; para escribir después necesitas una plantilla aprobada y el permiso del huésped.<a class="ref" href="#f2">[2]</a> En Instagram, con una cuenta profesional conectada a la API de mensajes, pasa algo parecido: 24 horas para el agente y hasta siete días para una persona del equipo con la etiqueta de agente humano.<a class="ref" href="#f3">[3]</a></p>
<p>Por eso el primer objetivo del chat nocturno es tener el correo y el WhatsApp de quien pregunta. Sin eso, la conversación se cierra sola.</p>"""),
  ("respuesta", "Cómo se ve una buena respuesta de madrugada", """
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 23:20</span>
<span class="yo">Hola, necesito 12 habitaciones del 10 al 12 de marzo y un salón para 30 personas</span>
<span class="bot">¡Hola! Tomo los datos: 12 habitaciones del 10 al 12 de marzo y salón para 30. ¿Es un viaje de empresa o un evento social, y necesitan alimentos? Las tarifas de grupo las arma ventas y te llegan mañana antes de las 11:00. ¿Te las paso por este WhatsApp o por correo? Soy el asistente con IA del hotel.</span>
<span class="yo">Empresa, con coffee break. Por correo mejor.</span>
<span class="bot">Perfecto. Déjame el correo y el nombre de la empresa y queda agendado con ventas. Soy el asistente con IA del hotel.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("no-hace", "Lo que el agente no debe hacer", """
<ol class="lista">
<li><strong>No confirmar bloqueos.</strong> Un grupo se confirma contra inventario y con una persona. Si el agente confirma de más, el problema cuesta más que la venta.</li>
<li><strong>No inventar tarifas.</strong> Si no tiene la tarifa cargada, no la estima.</li>
<li><strong>No prometer salones.</strong> El montaje y los horarios los define el hotel.</li>
<li><strong>No tocar quejas.</strong> Un huésped molesto pasa a una persona siempre.</li>
</ol>"""),
  ("idiomas", "Dos idiomas y una ficha que se pueda leer", """
<p>Buena parte de las solicitudes corporativas de la capital llegan en inglés. El agente debe responder en el idioma en que le escriben y guardar ese idioma en el contacto. En el sitio del hotel, si hay una versión por idioma, conviene declararla con hreflang para que Google entienda cuál mostrar.<a class="ref" href="#f4">[4]</a> Suma datos estructurados de tipo Hotel con la dirección, el teléfono y los servicios.<a class="ref" href="#f5">[5]</a></p>
<p>Para el huésped individual que pregunta tarifa de una noche, sigue con la guía de <a href="/guias/reservas-directas-whatsapp-hoteles/">reservas directas por WhatsApp para hoteles</a>, y para los DMs, la de <a href="/guias/reservas-automaticas-instagram-hoteles-boutique/">reservas automáticas por Instagram</a>. Lo que hacemos en la ciudad está en <a href="/negocios/ciudad-de-mexico/hospitality/">hoteles y rentas en Ciudad de México</a>.</p>"""),
  ("datos", "Datos de quien cotiza", """
<p>Nombre, correo, empresa y fechas son datos personales y los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f6">[6]</a> Enlaza el aviso de privacidad en el mismo chat donde pides el correo.</p>"""),
 ],
 faq=[
  ("¿Un agente de IA puede cotizar un grupo solo?", "No conviene. Puede tomar los datos completos y avisar en cuánto tiempo responde ventas, pero la tarifa de grupo la arma una persona contra inventario."),
  ("¿Qué datos tiene que pedir antes de pasar la solicitud?", "Fechas, habitaciones, motivo del viaje, salón o alimentos, empresa y facturación, quién decide y para cuándo, más WhatsApp y correo."),
  ("¿Puede contestar en inglés?", "Sí. Responde en el idioma en que le escriben y guarda ese idioma en el contacto del huésped."),
  ("¿Hasta cuándo puede seguir la conversación?", "El agente contesta libremente durante 24 horas desde el último mensaje. Después se escribe con una plantilla aprobada en WhatsApp, o sigue una persona del equipo en Instagram hasta siete días."),
  ("¿Sirve para hoteles chicos?", "Sí. Un hotel de 20 habitaciones recibe menos solicitudes de grupo, y justamente por eso perder una pesa más."),
 ],
 fuentes=["wa_api", "wa_precios", "ig_api", "g_hreflang", "sch_hotel", "lfpdppp"],
)

G["recuperar-socios-inactivos-gimnasios-guadalajara"] = dict(
 fecha="2026-11-22", fecha_txt="22 de noviembre de 2026",
 titulo="Gimnasios en Guadalajara: recuperar al socio que dejó de venir, por WhatsApp",
 titulo_seo="Recuperar socios inactivos en gimnasios de Guadalajara",
 corto="Recuperar socios inactivos en gimnasios de Guadalajara",
 desc="Cómo detectar en Guadalajara al socio que dejó de entrenar y escribirle con permiso y plantillas aprobadas, sin regalar la membresía.",
 rubro=FI, audit="fitness", og="og-fitness.jpg",
 wa="Hola! Leí la guía de recuperar socios inactivos en gimnasios de Guadalajara y quiero probar el agente 14 días.",
 bajada="El socio que se da de baja no te avisa: deja de venir. Pasa tres semanas sin entrar al gimnasio de Providencia o de Zapopan, llega el cobro del mes y ahí cancela. Para entonces ya decidió. Esta guía explica cómo darte cuenta a tiempo y escribirle cuando todavía se puede hacer algo, con las reglas de Meta y de la ley.",
 cuerpo=[
  ("senal", "La señal llega antes de la baja", """
<p>La baja se ve en la asistencia, no en el cobro. Un socio que entrenaba tres veces por semana y lleva diez días sin aparecer es un socio en riesgo. Si tu control de acceso o tu sistema de clases guarda las entradas, ya tienes el dato; falta que alguien lo mire todos los días, y eso es lo que puede hacer un agente.</p>
<div class="tabla"><table><thead><tr><th>Señal</th><th>Cuándo escribir</th><th>Qué dice el mensaje</th></tr></thead><tbody>
<tr><td>7 días sin entrar</td><td>Al octavo día</td><td>Pregunta cómo va y ofrece reservar la clase de la semana</td></tr>
<tr><td>Faltó a dos clases reservadas</td><td>Al día siguiente</td><td>Pregunta si cambió de horario y ofrece otro</td></tr>
<tr><td>21 días sin entrar</td><td>Antes del siguiente cobro</td><td>Ofrece una sesión con un coach para rearmar la rutina</td></tr>
<tr><td>Pidió cancelar</td><td>En el momento</td><td>Pasa a una persona, sin retener a la fuerza</td></tr>
</tbody></table></div>"""),
  ("permiso", "Escribirle fuera de la conversación: permiso y plantilla", """
<p>Estos mensajes salen cuando el socio no escribió nada, es decir, fuera de la ventana de 24 horas. En WhatsApp eso significa plantilla aprobada por Meta y permiso previo del socio.<a class="ref" href="#f1">[1]</a> La política de mensajería de WhatsApp Business no permite escribir a quien no aceptó recibir tus mensajes.<a class="ref" href="#f2">[2]</a></p>
<div class="aviso">En la práctica: el permiso se pide al inscribirse, en el mismo formulario donde el socio deja su teléfono, con una casilla que diga para qué le vas a escribir.</div>
<p>Si el socio llegó por Instagram, el agente puede contestarle en el DM dentro de las 24 horas desde su último mensaje, y después sigue una persona del equipo hasta siete días con la etiqueta de agente humano.<a class="ref" href="#f3">[3]</a> Por eso conviene mover la conversación a WhatsApp apenas se pueda.</p>"""),
  ("mensaje", "El mensaje que trae de vuelta", """
<p>El que dejó de venir casi nunca se fue por el precio. Se fue porque cambió de horario, se lesionó, se aburrió de la misma rutina o perdió el hábito. Un mensaje que ofrece descuento le confirma que el gimnasio vale menos. Uno que ofrece resolver el motivo funciona mejor.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 09:30</span>
<span class="bot">¡Hola, Diego! Vi que no has venido estas dos semanas. ¿Se te cruzó el horario? Abrimos lugares a las 7:00 y a las 21:00, y si quieres te agendo 20 minutos con un coach para rearmar tu rutina. ¿Te late? Soy el asistente con IA del gimnasio.</span>
<span class="yo">Ando full en el trabajo, no alcanzo a las 8</span>
<span class="bot">Te dejo lugar mañana a las 21:00 y te mando el recordatorio. Si ese horario te funciona, lo dejamos fijo. Soy el asistente con IA del gimnasio.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("precio", "Promociones y precio total", """
<p>Si en algún momento ofreces una reactivación con precio, tiene que ser el precio total, con vigencia y condiciones claras, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f4">[4]</a> Que la condición sea la misma en el chat, en el mostrador y en Instagram.</p>"""),
  ("salud", "Lesiones y datos sensibles", """
<p>Muchos socios dejan de venir por una lesión. Esa conversación la toma un coach, no el agente. Los datos sobre salud son datos personales sensibles para la Ley Federal de Protección de Datos Personales en Posesión de los Particulares, que pide más cuidado con ellos.<a class="ref" href="#f5">[5]</a> Lo más simple es que el agente no los pregunte y pase el tema a una persona.</p>"""),
  ("medir", "Cómo saber si funcionó", """
<ol class="lista">
<li>Cuántos socios en riesgo detectaste en la semana y a cuántos les escribiste.</li>
<li>Cuántos volvieron a entrenar en los siete días siguientes.</li>
<li>Cuántas bajas hubo ese mes contra el anterior. Es el número que importa.</li>
</ol>
<p>Para el prospecto nuevo que escribe por DM, mira la guía de <a href="/guias/responder-dms-instagram-automaticamente-gimnasios/">cómo responder DMs de Instagram en un gimnasio</a>, y para el día a día de reservas y retención, la de <a href="/guias/retencion-socios-gimnasio-reservas-clases/">retención de socios y reservas de clases</a>. Lo que hacemos en la ciudad está en <a href="/negocios/guadalajara/fitness/">gimnasios y estudios en Guadalajara</a>.</p>"""),
 ],
 faq=[
  ("¿Cómo sé qué socio está por darse de baja?", "Por la asistencia. Diez días sin entrar, o dos clases reservadas a las que faltó, son la señal más clara, y está en el control de acceso o en el sistema de clases."),
  ("¿Puedo escribirle por WhatsApp a un socio que no me escribió?", "Sí, si aceptó recibir tus mensajes, y con una plantilla aprobada por Meta, porque el mensaje sale fuera de la ventana de 24 horas."),
  ("¿Conviene ofrecer un descuento para que vuelva?", "Casi nunca. El que dejó de venir suele irse por el horario, una lesión o el aburrimiento, y resolver eso funciona mejor que bajar el precio."),
  ("¿El agente puede hablar de una lesión?", "No. Ese tema pasa a un coach, y los datos de salud no se piden por el chat del agente."),
  ("¿Sirve en un estudio chico?", "Sí. Con 80 socios, recuperar tres al mes ya cambia el número del mes."),
 ],
 fuentes=["wa_precios", "wa_politica", "ig_api", "lfpc", "lfpdppp"],
)


# ---- 3 guias nuevas (24/11/2026) ----

G["posadas-fiestas-fin-de-ano-cotizaciones-cdmx"] = dict(
 fecha="2026-11-24", fecha_txt="24 de noviembre de 2026",
 titulo="Posadas y fiestas de fin de año en CDMX: cotizar sin perder al que escribe primero",
 titulo_seo="Cotizar posadas y fiestas de fin de año en CDMX",
 corto="Cotizar posadas y fiestas de fin de año en CDMX",
 desc="Cómo cotizar posadas y fiestas de fin de año de empresa en CDMX por WhatsApp: revisar la fecha al momento, dar el precio total y seguir hasta el anticipo.",
 rubro=EV, audit="eventos", og="og-eventos.jpg",
 wa="Hola! Leí la guía de cotizaciones de posadas en CDMX y quiero probar el agente 14 días.",
 bajada="Quien organiza la posada de la empresa le escribe a seis lugares el mismo martes y pregunta lo mismo: qué fecha tienen libre, cuántas personas caben y cuánto sale por persona. El que contesta primero con la fecha y un número claro se queda con la visita. Esta guía explica cómo contestar ese mensaje a la hora en que entra, sin que nadie del equipo esté pegado al teléfono.",
 cuerpo=[
  ("quien-escribe", "Quién escribe y qué pide", """
<p>En diciembre no te escribe un solo tipo de cliente. Son tres, y cada uno necesita una respuesta distinta en el primer mensaje.</p>
<div class="tabla"><table><thead><tr><th>Quién</th><th>Qué pregunta primero</th><th>Qué necesita para decidir</th></tr></thead><tbody>
<tr><td>Empresa chica, 30 a 60 personas</td><td>Fecha libre y precio por persona</td><td>Un número cerrado y qué incluye</td></tr>
<tr><td>Corporativo, 150 o más</td><td>Capacidad, factura y formas de pago</td><td>Propuesta formal y una persona a cargo</td></tr>
<tr><td>Grupo de amigos o familia</td><td>Si pueden llevar bebida y hasta qué hora</td><td>Las reglas de la casa por escrito</td></tr>
</tbody></table></div>
<p>El agente no decide nada de esto. Pide los cuatro datos que hacen falta para cotizar, revisa la fecha y deja la conversación lista para que una persona arme la propuesta.</p>"""),
  ("fecha", "La fecha se revisa en el primer mensaje", """
<p>En temporada, la fecha es el filtro. Si el 12 de diciembre ya está tomado, no tiene sentido pedir presupuesto ni número de invitados: lo que sirve es ofrecer las dos fechas cercanas que sí tienes y el horario de la segunda tanda, si la manejas.</p>
<p>Un agente conectado al calendario que ya lleva el salón contesta eso al momento. Si no está conectado a ningún calendario, toma los datos y avisa a una persona, que es mejor que dejar el mensaje sin leer hasta mañana.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 22:40</span>
<span class="yo">Hola, busco lugar para la posada de la empresa, somos 45. ¿Tienen el viernes 12?</span>
<span class="bot">¡Hola! El viernes 12 ya está apartado. Tengo libre el jueves 11 y el viernes 19, los dos con lugar para 45 personas. ¿Alguno te sirve? Con eso y si quieren solo el espacio o con alimentos, mañana temprano te mandamos la cotización con el total. Soy el asistente con IA del salón.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("precio", "Precio por persona y precio total", """
<p>En diciembre casi todos preguntan el precio por persona, y ahí se arman los malentendidos: el cliente compara un número que incluye alimentos contra otro que no. La Ley Federal de Protección al Consumidor pide informar el monto total a pagar.<a class="ref" href="#f1">[1]</a></p>
<p>Lo práctico es que la cotización diga el total para el número de personas acordado, qué incluye, qué no, el mínimo de consumo si lo hay, el horario que cubre y qué pasa si llegan menos invitados de los que se cotizaron. Esta guía no reemplaza a un abogado.</p>
<div class="aviso">Lo que más cancela un cierre en temporada: el cliente se enteró del descorche, del tiempo extra o del servicio después de recibir el total.</div>"""),
  ("seguimiento", "El seguimiento hasta el anticipo", """
<p>Entre la cotización y el anticipo pasan días, y en diciembre pasan horas. Con la plataforma de WhatsApp Business, cada mensaje del cliente abre una ventana de 24 horas en la que contestas libremente; para escribirle después necesitas una plantilla aprobada por Meta y que haya aceptado recibir tus mensajes.<a class="ref" href="#f2">[2]</a> La política de mensajería de WhatsApp Business no permite escribirle a quien no lo aceptó.<a class="ref" href="#f3">[3]</a></p>
<ol class="lista">
<li>Al mandar la cotización, pide el permiso para dar seguimiento en el mismo chat.</li>
<li>Deja escrito cuánto tiempo se sostiene la fecha sin anticipo. Esa decisión la toma una persona, no el agente.</li>
<li>Cuando entra el anticipo, el agente manda el comprobante, la hora de acceso y a quién buscar el día del evento.</li>
</ol>"""),
  ("encontrar", "Cómo te encuentran en la ciudad", """
<p>«Salón para posada en la Roma» o «terraza para fiesta de fin de año en Polanco» son búsquedas locales, y Google las ordena por relevancia, distancia y prominencia.<a class="ref" href="#f4">[4]</a> Que la capacidad, las colonias que atiendes y el tipo de evento estén escritos en texto en tu página, con fotos reales y las reseñas respondidas. Los datos estructurados de recinto de eventos ordenan dirección y capacidad para cualquier buscador.<a class="ref" href="#f5">[5]</a></p>
<p>Los datos de quien cotiza, incluidos los de la empresa que factura, se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f6">[6]</a></p>
<p>Para el resto del año, sigue con la guía de <a href="/guias/cotizaciones-salones-eventos-guadalajara/">cotizaciones para salones de eventos</a> y la de <a href="/guias/salones-eventos-monterrey-apartar-fechas/">visitas y fechas apartadas por WhatsApp</a>. Lo que puede hacer la IA en el rubro está en <a href="/guias/como-usar-ia-en-eventos/">cómo usar IA en una empresa de eventos</a>, y lo que hacemos en la ciudad en <a href="/negocios/ciudad-de-mexico/eventos/">eventos en Ciudad de México</a>.</p>"""),
 ],
 faq=[
  ("¿El agente puede decir si una fecha de diciembre está libre?", "Sí, si está conectado al calendario que ya lleva el salón. Si no lo está, toma los datos y avisa a una persona en el momento."),
  ("¿Tengo que dar el precio total y no solo el precio por persona?", "La Ley Federal de Protección al Consumidor pide informar el monto total a pagar. Lo práctico es dar el total para el número de personas acordado y decir qué incluye y qué no."),
  ("¿Puedo dar seguimiento por WhatsApp a una cotización de posada?", "Dentro de las 24 horas desde el último mensaje del cliente contestas libremente. Después necesitas una plantilla aprobada por Meta y su permiso, que conviene pedir al mandar la cotización."),
  ("¿El agente aparta la fecha?", "No. Cuánto tiempo se sostiene una fecha sin anticipo y la confirmación del pago las define una persona."),
  ("¿Sirve si ya estoy casi lleno en diciembre?", "Sirve para dos cosas: ofrecer las fechas que sí quedan en lugar de perder la conversación, y quedarte con el contacto de quien cotizó para el año que viene, si aceptó recibir tus mensajes."),
 ],
 fuentes=["lfpc", "wa_precios", "wa_politica", "gbp_rank", "sch_venue", "lfpdppp"],
)

G["reservas-restaurantes-tulum-ingles-whatsapp"] = dict(
 fecha="2026-11-24", fecha_txt="24 de noviembre de 2026",
 titulo="Restaurantes en Tulum: contestar en inglés las reservas que entran por Instagram y WhatsApp",
 titulo_seo="Reservas en inglés para restaurantes en Tulum",
 corto="Reservas en inglés para restaurantes en Tulum",
 desc="Cómo un restaurante en Tulum contesta en inglés las reservas que llegan por Instagram y WhatsApp a cualquier hora, con la carta y el precio total claros.",
 rubro=GA, audit="gastronomia", og="og-gastronomia.jpg",
 wa="Hola! Leí la guía de reservas en inglés para restaurantes en Tulum y quiero probar el agente 14 días.",
 bajada="En Tulum el mensaje llega a las once de la noche y en inglés: «table for two tomorrow at 8?». Si nadie contesta hasta el mediodía del día siguiente, esa pareja ya reservó en otro lado desde la cama del hotel. Esta guía explica cómo contestar esos mensajes en el idioma en que llegan y a la hora en que llegan.",
 cuerpo=[
  ("idioma", "El idioma en que llega el mensaje", """
<p>Un restaurante en Tulum recibe consultas en español, en inglés y bastantes en portugués, francés o italiano. El equipo del piso contesta lo que puede, cuando puede, y lo demás se acumula. El problema no es traducir: es que el que pregunta está decidiendo dónde cenar en los próximos diez minutos.</p>
<p>Un agente que responde en el idioma del mensaje resuelve lo que se repite siempre: si hay lugar, a qué hora, si aceptan tarjeta, si hay opciones sin gluten o veganas, si se puede llegar en bici y si hay que dejar anticipo. Lo que no sabe, lo pasa a una persona y no lo adivina.</p>"""),
  ("ventana", "La ventana de 24 horas en Instagram", """
<p>En Tulum buena parte de las consultas entran por DM de Instagram, no por WhatsApp. Para que un agente conteste esos DMs hace falta una cuenta profesional, y la respuesta tiene que salir dentro de la ventana de 24 horas desde el último mensaje de la persona.<a class="ref" href="#f1">[1]</a></p>
<p>Esa ventana es el motivo por el que conviene contestar de noche y no a la mañana siguiente: a las once de la mañana la ventana sigue abierta, pero el cliente ya cenó en otro lado. Si el agente deriva a una persona, Meta pide usar la etiqueta de agente humano para marcarlo.<a class="ref" href="#f1">[1]</a></p>"""),
  ("carta", "La carta, el precio y lo que no se improvisa", """
<p>La pregunta que más cuesta en inglés es el precio. Si la respuesta es un rango inventado, el cliente llega con una expectativa distinta a la cuenta. La Ley Federal de Protección al Consumidor pide informar el monto total a pagar.<a class="ref" href="#f2">[2]</a> Lo sano es que el agente mande la carta vigente con precios, y que no prometa nada sobre propina, cover de la música o servicio si no está escrito ahí.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">Instagram · 23:10</span>
<span class="yo">Hi! Table for 2 tomorrow at 8pm? Any vegan options?</span>
<span class="bot">Hi! Yes, we have a table for 2 tomorrow at 8:00 pm. We have three vegan dishes on the menu, I am sending it to you with prices. Should I book it under your name? I am the restaurant AI assistant, and someone from the team can jump in anytime.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("reserva", "De la reserva a la mesa ocupada", """
<p>En temporada alta, la reserva que no se confirma es una mesa vacía en la mejor hora. El recordatorio del mismo día sale fuera de la ventana de 24 horas en WhatsApp, así que necesita una plantilla aprobada por Meta y el permiso del cliente, que conviene pedir cuando se confirma la mesa.<a class="ref" href="#f3">[3]</a></p>
<ul>
<li>Confirmación al reservar, con hora, personas y cómo llegar.</li>
<li>Recordatorio el mismo día, en el idioma de la reserva.</li>
<li>Si no responde, el aviso de cuántos minutos se guarda la mesa, dicho antes y no después.</li>
</ul>"""),
  ("encontrar", "Que te encuentren los que ya están en Tulum", """
<p>Casi nadie reserva en Tulum con un mes de anticipación: busca desde el hotel, en el teléfono y en inglés. Google ordena esos resultados locales por relevancia, distancia y prominencia.<a class="ref" href="#f4">[4]</a> Tener la zona escrita en texto, la carta en una página propia y las reseñas respondidas pesa más que cualquier truco.</p>
<p>Los datos estructurados de restaurante ordenan la carta, la cocina y si aceptas reservas.<a class="ref" href="#f5">[5]</a> Si tienes la página en varios idiomas, una URL por idioma con hreflang evita que compitan entre ellas.<a class="ref" href="#f6">[6]</a> Y los datos de quien reserva se rigen por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f7">[7]</a></p>
<p>Para el DM de Instagram paso por paso, mira la guía de <a href="/guias/reservas-instagram-restaurantes-monterrey/">reservas por Instagram para restaurantes</a>, y para todo lo demás del rubro, <a href="/guias/como-usar-ia-en-un-restaurante/">cómo usar IA en un restaurante</a>. Lo mismo del lado de los hoteles está en <a href="/guias/automatizar-mensajes-hoteles-tulum/">automatizar mensajes para hoteles en Tulum</a>, y lo que hacemos en la zona en <a href="/negocios/tulum/gastronomia/">restaurantes y bares en Tulum</a>.</p>"""),
 ],
 faq=[
  ("¿El agente contesta en inglés y en español?", "Sí. Responde en el idioma del mensaje, con la información que el restaurante cargó, y pasa a una persona lo que no sabe."),
  ("¿Puedo contestar los DMs de Instagram con un agente?", "Sí, con una cuenta profesional y dentro de la ventana de 24 horas desde el último mensaje de la persona."),
  ("¿Puede mandar la carta con precios?", "Sí, la carta vigente que cargó el restaurante. Conviene que no improvise precios: la ley pide informar el monto total a pagar."),
  ("¿Sirve para recordar la reserva el mismo día?", "Sí, con una plantilla aprobada por Meta y el permiso del cliente, que conviene pedir al confirmar la mesa."),
  ("¿Qué no debería contestar el agente?", "Un reclamo, un cambio de precio o un pedido especial de cocina. Eso pasa a una persona del equipo."),
 ],
 fuentes=["ig_api", "lfpc", "wa_precios", "gbp_rank", "sch_rest", "g_hreflang", "lfpdppp"],
)

G["distribuidoras-monterrey-pedidos-whatsapp"] = dict(
 fecha="2026-11-24", fecha_txt="24 de noviembre de 2026",
 titulo="Distribuidoras en Monterrey: tomar el pedido por WhatsApp sin que se pierda en el chat",
 titulo_seo="Pedidos por WhatsApp para distribuidoras en Monterrey",
 corto="Pedidos por WhatsApp para distribuidoras en Monterrey",
 desc="Cómo una distribuidora en Monterrey recibe el pedido por WhatsApp con el catálogo y el precio claros, lo confirma y lo pasa a entrega sin releer la conversación.",
 rubro=DI, audit="distribucion", og="og-distribucion.jpg",
 wa="Hola! Leí la guía de pedidos por WhatsApp para distribuidoras en Monterrey y quiero probar el agente 14 días.",
 bajada="En una distribuidora de Monterrey el pedido entra a las seis de la mañana, en forma de nota de voz, y alguien lo pasa a mano a una hoja. Lo que se pierde ahí no es el pedido: es la clave equivocada, la caja que faltó y el reclamo del lunes. Esta guía explica cómo recibir el pedido por WhatsApp y que llegue completo a quien lo surte.",
 cuerpo=[
  ("pedido", "Lo que tiene que quedar escrito de cada pedido", """
<p>Un pedido sirve si quien surte no tiene que releer la conversación. Son siempre los mismos campos, y un agente los pide uno por uno en el chat antes de confirmar.</p>
<div class="tabla"><table><thead><tr><th>Dato</th><th>Para qué sirve</th></tr></thead><tbody>
<tr><td>Cliente y sucursal</td><td>Saber a qué dirección va y con qué precio de lista</td></tr>
<tr><td>Clave y cantidad por producto</td><td>Que almacén surta sin interpretar</td></tr>
<tr><td>Fecha de entrega</td><td>Cerrar la ruta del día en Monterrey, San Nicolás, Apodaca o Santa Catarina</td></tr>
<tr><td>Forma de pago y factura</td><td>No descubrirlo cuando el camión ya salió</td></tr>
<tr><td>Quién recibe</td><td>Evitar la entrega que vuelve</td></tr>
</tbody></table></div>
<p>Lo que el agente no hace es decidir. Un crédito, una excepción de precio o un faltante los resuelve una persona.</p>"""),
  ("catalogo", "Catálogo y precios en el chat", """
<p>La plataforma de WhatsApp Business permite mandar mensajes de uno o varios productos desde un catálogo, en lugar de pegar una lista en texto.<a class="ref" href="#f1">[1]</a> Para un distribuidor eso sirve sobre todo con el cliente nuevo, que todavía no sabe las claves.</p>
<p>Si en el chat hay precios, tienen que ser el monto total a pagar, como pide la Ley Federal de Protección al Consumidor.<a class="ref" href="#f2">[2]</a> Y conviene que el precio salga de tu lista, no de lo que el agente recuerde: si no tiene el precio cargado, lo correcto es que lo pase a una persona.</p>
<div class="chat" role="figure" aria-label="Ejemplo de conversación">
<span class="t">WhatsApp · 06:40</span>
<span class="yo">Mándame 10 cajas de la 250 y 4 de la chica, para mañana</span>
<span class="bot">Listo, don Raúl. Anoto 10 cajas de 250 ml y 4 de 355 ml para la sucursal Cumbres, entrega mañana en la ruta de la mañana. ¿Lo confirmo así y te paso el total con IVA de la lista? Soy el asistente con IA de la distribuidora.</span>
<span class="nota">Conversación de ejemplo.</span>
</div>"""),
  ("api", "Por qué hace falta la API y no la app", """
<p>La app gratuita de WhatsApp Business sirve para respuestas rápidas y mensaje de ausencia, pero no conecta un agente que entienda el pedido ni lo pase a tu sistema. Para eso se usa la plataforma de WhatsApp Business, la API, con un proveedor o directamente con Meta.<a class="ref" href="#f3">[3]</a></p>
<p>Con la API, cada mensaje del cliente abre una ventana de 24 horas para contestar libremente. Fuera de esa ventana, cualquier aviso tuyo sale con una plantilla aprobada por Meta y con el permiso del cliente.<a class="ref" href="#f4">[4]</a></p>"""),
  ("recurrente", "El cliente que pide lo mismo cada semana", """
<p>La mayor parte del volumen de una distribuidora es pedido repetido. Ahí es donde el agente ahorra más: propone el pedido anterior y el cliente solo ajusta cantidades.</p>
<ol class="lista">
<li>El agente manda el pedido de la semana pasada y pregunta si va igual. Si sale fuera de la ventana de 24 horas, va con plantilla y con permiso.<a class="ref" href="#f4">[4]</a></li>
<li>El cliente cambia dos líneas y confirma.</li>
<li>El pedido entra completo, con cliente, claves, cantidades, fecha y quién recibe.</li>
</ol>"""),
  ("datos", "Datos de tus clientes y de tu ruta", """
<p>Los nombres, teléfonos, direcciones de entrega y el historial de compra de tus clientes son datos personales, y en México los rige la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.<a class="ref" href="#f5">[5]</a> Lo básico es el aviso de privacidad a la mano y usarlos solo para lo que le dijiste al cliente. Esta guía no reemplaza a un abogado.</p>
<p>Para el detalle del pedido recurrente, sigue con la guía de <a href="/guias/pedidos-recurrentes-whatsapp-distribuidoras/">pedidos recurrentes por WhatsApp</a>, y para la cotización del cliente nuevo, la de <a href="/guias/pedidos-whatsapp-cotizaciones-distribuidoras/">pedidos y cotizaciones por WhatsApp</a>. Lo que puede hacer la IA en el rubro está en <a href="/guias/como-usar-ia-en-una-distribuidora/">cómo usar IA en una distribuidora</a>, y lo que hacemos en la ciudad en <a href="/negocios/monterrey/distribucion/">distribuidoras y mayoristas en Monterrey</a>.</p>"""),
 ],
 faq=[
  ("¿El agente puede tomar un pedido de una nota de voz?", "Puede pedir los datos que faltan y dejar el pedido escrito con claves y cantidades. Lo que no conviene es que interprete una nota de voz y lo dé por bueno sin confirmar."),
  ("¿Puedo mandar mi catálogo por WhatsApp?", "Sí. La plataforma de WhatsApp Business permite mensajes de uno o varios productos desde un catálogo, lo que ayuda sobre todo con el cliente nuevo."),
  ("¿Sirve la app gratuita de WhatsApp Business?", "Para respuestas rápidas y horario sí, pero no conecta un agente que entienda el pedido ni lo pase a tu sistema. Para eso se usa la API."),
  ("¿Puedo recordarle al cliente que le toca pedido?", "Sí, con una plantilla aprobada por Meta y con su permiso, porque ese mensaje sale fuera de la ventana de 24 horas."),
  ("¿Qué no debe decidir el agente?", "Crédito, excepciones de precio, faltantes y reclamos de entrega. Todo eso pasa a una persona."),
 ],
 fuentes=["wa_catalogo", "lfpc", "wa_api", "wa_precios", "lfpdppp"],
)

ORDEN = list(G.keys())


def renum(cuerpo_html, fuentes):
    # convierte [n] locales ya escritos en orden de fuentes de la guía: se escribieron con el índice de la lista
    return cuerpo_html


def pagina(slug, d, pie):
    url = f"https://eltio.net/guias/{slug}/"
    fecha, fecha_txt = d.get("fecha", FECHA), d.get("fecha_txt", FECHA_TXT)
    audit = f"https://app.eltio.net/auditoria/{d['audit']}" if d["audit"] else "/posicionamiento-en-ia/#audit"
    wa = WA + urllib.parse.quote(d["wa"])
    article = {"@context": "https://schema.org", "@type": "Article", "headline": d["titulo"], "description": d["desc"],
               "inLanguage": "es-MX", "datePublished": fecha, "dateModified": fecha,
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
    gen = next(s for s in ("como-aparecer-en-chatgpt-negocio-en-tu-ciudad", "como-pedir-resenas-google-sin-incentivos") if s != slug)
    rel = [s for s in ORDEN if s != slug and G[s]["rubro"] == d["rubro"] and s != gen] + [gen]
    otras = "".join(f'<li><a href="/guias/{s}/">{e(G[s]["titulo"])}</a></li>' for s in rel)
    fuentes = "".join(f'<li id="f{n}">{e(F[k][0])} <a href="{F[k][1]}">{e(F[k][1].split("://")[1].rstrip("/"))}</a></li>'
                      for n, k in enumerate(d["fuentes"], 1))
    ig = f' · <a class="enlace" data-cta="instagram" href="{IG}">Escribir por DM en Instagram</a>'
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d.get("titulo_seo") or d["titulo"])} · El Tío</title>
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
    <p class="fecha">Actualizada el {fecha_txt}</p>
    <nav class="indice" aria-label="En esta guía"><p>En esta guía</p><ol>{indice}<li><a href="#preguntas">Preguntas frecuentes</a></li><li><a href="#empezar">Por dónde empezar</a></li></ol></nav>
{cuerpo}
    <h2 id="preguntas">Preguntas frecuentes</h2>
{faqh}
    <section class="cierre" id="empezar">
      <h2>Por dónde empezar</h2>
      <p>Lo más rápido es probarlo: instalamos el agente que contesta los mensajes de Instagram y de WhatsApp de tu negocio, lo usas <a href="/prueba/">14 días gratis</a> y pagas solo si te sirvió. Si prefieres empezar mirando, el Audit también es gratis: un cuestionario de 15 a 25 minutos y, en 24 a 48 horas hábiles, el mapa de lo que conviene hacer primero.</p>
      <div class="acciones">
        <a class="btn" data-cta="prueba" href="/prueba/">Probar 14 días gratis</a>
        <a class="enlace" data-cta="audit" href="{audit}">Hacer el Audit gratis</a>
        <a class="enlace" data-cta="whatsapp" href="{wa}">Escribir por WhatsApp</a>{ig}
      </div>
    </section>
    <nav class="relacionado" aria-label="Para seguir">
      <p>Para seguir</p>
      <ul>
        <li><a href="{d['rubro'][1]}">{e(d['rubro'][0])}</a>: la página del rubro</li>
        {otras}
        <li><a href="/prueba/">Prueba gratis de 14 días</a>: el agente instalado y funcionando antes de pagar</li>
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
            fg = G[slug].get("fecha", FECHA)
            nuevas += f"  <url><loc>{u}</loc><lastmod>{fg}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
    if nuevas:
        txt = txt.replace("</urlset>", nuevas + "</urlset>")
        sm.write_text(txt, encoding="utf-8")
    print("ok", len(G), "sitemap +", nuevas.count("<url>"))


if __name__ == "__main__":
    main()
