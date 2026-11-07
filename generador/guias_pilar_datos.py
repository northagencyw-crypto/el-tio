"""Contenido de las guias pilar «Como usar IA en ... en 2026». Ver guias_pilar.py.
Reglas: solo datos con fuente (FUENTES), ejemplos marcados, sin precios, sin llamadas, sin rayas, tuteo neutro,
sin herramientas ni pasos internos."""

CIUDADES = {"ciudad-de-mexico": "Ciudad de México", "monterrey": "Monterrey", "guadalajara": "Guadalajara",
            "tulum": "Tulum", "cancun": "Cancún", "playa-del-carmen": "Playa del Carmen", "puebla": "Puebla",
            "queretaro": "Querétaro"}

FUENTES = {
    "mck": ("McKinsey &amp; Company, «The State of AI in 2025», encuesta global publicada en noviembre de 2025: 88 % de las organizaciones usa IA de forma habitual en al menos una función del negocio.",
            "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
    "ind": ("El Tío, «Índice El Tío», edición 1, noviembre de 2026: 83,714 negocios de hasta 50 personas en cuatro estados de México, sobre el Directorio Estadístico Nacional de Unidades Económicas (DENUE) del INEGI.",
            "https://eltio.net/indice/"),
    "hbr": ("James B. Oldroyd, Kristina McElheran y David Elkington, «The Short Life of Online Sales Leads», Harvard Business Review, marzo de 2011.",
            "https://hbr.org/2011/03/the-short-life-of-online-sales-leads"),
    "asur": ("ASUR, «ASUR Announces Total Passenger Traffic for December 2025», comunicado del 6 de enero de 2026 con el tráfico de enero a diciembre de 2025 del aeropuerto de Cancún, reproducido en Stock Titan.",
             "https://www.stocktitan.net/news/ASR/asur-announces-total-passenger-traffic-for-december-53f52b4efyoo.html"),
    "della": ("Stefano DellaVigna y Ulrike Malmendier, «Paying Not to Go to the Gym», American Economic Review, vol. 96, núm. 3, junio de 2006, págs. 694 a 719.",
              "https://www.aeaweb.org/articles?id=10.1257/aer.96.3.694"),
    "meta": ("Meta, «Pricing on the WhatsApp Business Platform», documentación para desarrolladores: ventana de atención de 24 horas, mensajes con y sin plantilla y permiso del usuario.",
             "https://developers.facebook.com/docs/whatsapp/pricing"),
    "wapol": ("WhatsApp, «Política de mensajería de WhatsApp Business», actualizada el 23 de septiembre de 2026.",
              "https://whatsappbusiness.com/es-la/policy/"),
    "lfpd": ("Ley Federal de Protección de Datos Personales en Posesión de los Particulares, Diario Oficial de la Federación, 20 de marzo de 2025. Texto vigente en la Cámara de Diputados.",
             "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf"),
}


def hoy(rubro_txt, extra):
    return {"id": "hoy", "h2": "Por qué la ventaja es hoy", "bloques": [
        "Las empresas grandes ya se movieron. En la encuesta global de McKinsey publicada en noviembre de 2025, 88 % de las organizaciones dijo usar inteligencia artificial de forma habitual en al menos una función de su negocio.{{mck}}",
        f"Los negocios chicos, en cambio, en su mayoría todavía no empiezan. En el Índice El Tío contamos 83,714 negocios de hasta 50 personas en cuatro estados de México con el directorio del INEGI, y 94 de cada 100 no tienen una web registrada.{{{{ind}}}} Si muchos {rubro_txt} todavía no tienen lo básico, quien hoy suma IA a su forma de trabajar queda adelante en su zona.",
        extra,
        "Esa distancia es la ventana. Hoy alcanza con dar un paso. Cuando la mayoría de tu competencia haya empezado, vas a tener que dar diez para llegar al mismo lugar. Las cinco ventajas que siguen son las que más se repiten en tu rubro, ordenadas de lo que ya tienes a lo que te falta.",
    ]}


def nohace(txt):
    return {"id": "no-hace", "h2": "Lo que la IA no hace por ti", "bloques": [
        "Conviene tenerlo claro desde el principio, porque evita expectativas que después decepcionan.",
        txt,
        "Tampoco reemplaza a tu equipo. Lo que hace es quitarle el trabajo que se repite y avisarle a tiempo de lo que necesita una persona. Los negocios que mejor la aprovechan son los que deciden primero qué quieren lograr y después qué automatizar, no al revés.",
        "Y no se instala de un día para otro. Empieza por una ventaja, se mide unas semanas y se suma la siguiente. Lo importante es dar el primer paso mientras la mayoría todavía no lo dio.",
    ]}


def cuidar(extra):
    return {"id": "cuidar", "h2": "Lo que conviene cuidar", "bloques": [
        "La IA trabaja con tus clientes, y las reglas son las mismas que para tu equipo.",
        {"lista": [
            "<strong>Permiso para escribir primero.</strong> Si el cliente te escribe, tienes 24 horas para contestar con mensajes libres. Para escribirle tú primero por WhatsApp hace falta una plantilla aprobada y que la persona haya aceptado recibir tus mensajes.{{meta}}",
            "<strong>Respetar a quien dice que no.</strong> La política de WhatsApp Business pide dejar de escribir a quien lo solicita, y escribirle en frío a una base comprada pone en riesgo tu número.{{wapol}}",
            "<strong>Datos personales.</strong> Los nombres, teléfonos e historiales de tus clientes se rigen por la ley mexicana de 2025: tu aviso de privacidad tiene que decir qué guardas y para qué.{{lfpd}}",
            "<strong>Decir que es un asistente.</strong> Quien escribe sabe que le contesta un asistente de IA y que una persona puede tomar la conversación cuando haga falta.",
            extra,
        ]},
    ]}


from guias_pilar_en import _HREF_HOTEL

GUIAS = [
# ---------------------------------------------------------------- GASTRONOMIA
{
 "slug": "como-usar-ia-en-un-restaurante", "rubro": "gastronomia", "rubro_nombre": "Gastronomía",
 "wa": "restaurantes", "about": "Inteligencia artificial para restaurantes",
 "title": "Cómo usar IA en un restaurante en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA en un restaurante en 2026: 5 ventajas que tu competencia ya aprovecha",
 "desc": "Las 5 ventajas de la inteligencia artificial para restaurantes, bares y cafeterías en México: clientes que vuelven, eventos de empresa, redes, respuesta en pleno servicio y menos trabajo repetido.",
 "bajada": "Un restaurante ya tiene lo que más vale para la IA: cientos de clientes que le escribieron, reservaron o pidieron a domicilio. Esta guía explica las cinco ventajas que hoy separan a los restaurantes que se mueven de los que esperan, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "gas-ent-telefono-noche", "wh": (1024, 1536), "alt": "Teléfono encendido en el atril de recepción con el local ya cerrado"},
 "ciudades": ["ciudad-de-mexico", "monterrey", "guadalajara", "puebla", "queretaro"],
 "guias_rel": [("/guias/chatbot-whatsapp-restaurantes-ciudad-de-mexico/", "Chatbot de WhatsApp para restaurantes en Ciudad de México: la guía a fondo de reservas y pedidos")],
 "secciones": [
  hoy("restaurantes, bares y cafeterías",
      "En un restaurante la diferencia se nota rápido. El cliente que pregunta por una mesa a las nueve de la noche reserva donde le contestan primero, y el grupo que busca dónde festejar elige al lugar que ve seguido en sus redes."),
  {"id": "datos", "h2": "1. Los clientes que ya te escribieron vuelven", "bloques": [
    "Cada reserva, cada pedido a domicilio y cada pregunta por WhatsApp deja un nombre, una fecha y lo que esa persona pidió. En la mayoría de los restaurantes esa información queda dormida en el teléfono del encargado. Ordenada, es la lista de clientes más valiosa que tienes, porque son personas que ya te conocen.",
    "La ventaja está en invitarlos a volver en el momento justo: el cumpleaños, el aniversario de la primera visita, el regreso del platillo de temporada que pidieron el año pasado. Es más fácil que vuelva alguien que ya comió contigo que convencer a un desconocido.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Clientes para invitar esta semana", "filas": [
        ("Mariana R.", "Cumpleaños el jueves · 4 visitas", "Invitación lista"),
        ("Grupo oficina Polanco", "Comida de fin de mes · 12 personas", "Recordar el lunes"),
        ("Jorge T.", "Pidió chiles en nogada en 2025", "Avisar el regreso"),
        ("Lucía M.", "Sin visita desde julio", "Invitación de regreso")]},
  ]},
  {"id": "prospectar", "h2": "2. Empresas y grupos antes que tu competencia", "bloques": [
    "Las cenas de equipo, los desayunos de trabajo, las fiestas de fin de año y los pedidos grandes para oficinas son mesas llenas en días flojos. Casi nunca llegan solas: alguien de la empresa busca opciones, pregunta en dos o tres lugares y reserva donde le contestan primero y mejor.",
    "La IA ayuda a encontrar a esas empresas de tu zona y a escribirles con una propuesta pensada para ellas antes de que lo haga el restaurante de enfrente. Quien llega primero con una opción clara suele quedarse con el evento.",
  ]},
  {"id": "confianza", "h2": "3. Confianza en redes, semana tras semana", "bloques": [
    "Antes de probar un lugar, la gente lo mira. Revisa tus fotos, tus historias y cómo contestas los comentarios. Contar la cocina, al equipo y los platillos cada semana hace que te elijan antes de haber probado nada, porque ya te sienten conocido.",
    "El problema de siempre es el tiempo: en temporada alta nadie se acuerda de publicar. Con IA el contenido se planea, se escribe y se ordena con tu voz, y tu equipo solo aporta lo que pasa en la cocina.",
  ]},
  {"id": "presencia", "h2": "4. Contestar en pleno servicio", "bloques": [
    "Los mensajes llegan justo cuando nadie puede mirar el teléfono: a la hora de la comida, en el pico de la cena, al cerrar. Un estudio publicado en Harvard Business Review encontró que las empresas que contestaban a un interesado dentro de la primera hora tenían casi siete veces más probabilidades de concretar algo con él que las que esperaban una hora más.{{hbr}} El estudio no es sobre restaurantes, pero la lógica se aplica igual a quien pregunta por una mesa para hoy.",
    "Un asistente de IA contesta horarios, menú, ubicación y disponibilidad al momento, toma la reserva y pasa a una persona lo que no sabe resolver.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "WhatsApp · 21:40", "lineas": [
        ("yo", "Hola, ¿tienen mesa para 6 hoy a las 22:00?"),
        ("bot", "Hola. Soy el asistente de IA del restaurante. Tengo mesa para 6 a las 22:15 en terraza. ¿Te la aparto a nombre de quién?"),
        ("yo", "A nombre de Daniel. ¿Tienen opciones sin gluten?"),
        ("bot", "Listo, Daniel, mesa para 6 a las 22:15. Sí, en el menú marcamos los platillos sin gluten; te paso la carta. Si alguien tiene una alergia, avísale al mesero al llegar."),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Menos trabajo repetido, más equipo en el salón", "bloques": [
    "Confirmar reservas, recordar la mesa del día, contestar diez veces si hay estacionamiento, pasar el pedido a la cocina: todo eso consume horas del mejor personal que tienes. Cuando sale solo, el equipo queda para lo que solo hace una persona: atender la mesa, recomendar un vino, resolver un problema en el momento.",
    "Lo repetitivo también deja números. Sabes cuántas reservas llegaron por mensaje, a qué hora preguntan más y qué días conviene reforzar el turno.",
  ]},
  nohace("La IA no cocina ni atiende la mesa. Un platillo flojo o un mal servicio no se arreglan con mensajes rápidos: la experiencia en el salón sigue siendo lo que hace que alguien vuelva. Lo que sí hace es que más gente llegue a probarla y que quien ya vino se acuerde de ti."),
  cuidar("<strong>Información de alérgenos.</strong> El asistente responde solo con el menú que aprobó tu cocina y deriva a una persona cualquier pregunta de alergias que no esté ahí."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Tiempo hasta la primera respuesta a cada mensaje, también en servicio.",
            "Reservas que llegaron por mensaje y cuántas se presentaron.",
            "Clientes que volvieron después de una invitación.",
            "Eventos y pedidos de empresa cotizados y cerrados.",
            "Publicaciones de la semana y mensajes que llegaron por redes."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial en un restaurante?", "Para que vuelvan los clientes que ya tienes, encontrar empresas y grupos que llenan días flojos, mostrarte con constancia en redes, contestar mensajes en pleno servicio y quitarle al equipo el trabajo repetido, como confirmar reservas."),
  ("¿Un chatbot de WhatsApp reemplaza a mi equipo de recepción?", "No. Contesta lo que se repite y toma reservas, y pasa a una persona lo que no sabe resolver. El equipo queda para atender a los clientes en el salón."),
  ("¿Puedo escribirle a mis clientes anteriores por WhatsApp?", "Sí, si aceptaron recibir tus mensajes y usas una plantilla aprobada para escribir tú primero. Si el cliente te escribe, tienes 24 horas para contestar con mensajes libres.{{meta}}"),
  ("¿Sirve para una cafetería o un bar chico?", "Sí. Las cinco ventajas son las mismas; cambia el volumen. En un negocio chico suele convenir empezar por los clientes que ya tienes y por contestar a tiempo."),
  ("¿Por dónde empiezo?", "Por ver dónde se pierden hoy las reservas y los clientes. El Audit gratis de El Tío arma ese mapa para tu restaurante y te dice qué ventaja conviene tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabaja hoy tu restaurante: cuántos mensajes llegan, cuánto tardan en recibir respuesta, qué pasa con los clientes que ya vinieron y dónde se pierden reservas.",
},
# ---------------------------------------------------------------- HOSPITALITY
{
 "slug": "como-usar-ia-en-un-hotel", "rubro": "hospitality",
 "hreflang": _HREF_HOTEL, "rubro_nombre": "Hospitality",
 "wa": "hoteles", "about": "Inteligencia artificial para hoteles y turismo",
 "title": "Cómo usar IA en un hotel en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA en un hotel en 2026: 5 ventajas que tu competencia ya aprovecha",
 "desc": "Las 5 ventajas de la inteligencia artificial para hoteles boutique, rentas vacacionales y tours en México: huéspedes que vuelven, grupos, reseñas, respuesta en otro idioma y menos trabajo en recepción.",
 "bajada": "Un hotel boutique, una renta vacacional o un operador de tours compite con las plataformas grandes por la atención del viajero. Esta guía explica las cinco ventajas que la IA da hoy en hospitality, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "ho-libro-novedades", "wh": (1024, 1024), "alt": "Libro de novedades abierto sobre el mostrador de recepción"},
 "ciudades": ["tulum", "cancun", "playa-del-carmen", "ciudad-de-mexico", "guadalajara"],
 "guias_rel": [("/guias/reservas-directas-whatsapp-hoteles/", "Reservas directas por WhatsApp para hoteles y rentas vacacionales"),
               ("/guias/chatbot-whatsapp-tours-riviera-maya/", "Chatbot de WhatsApp para tours en Tulum y la Riviera Maya")],
 "secciones": [
  hoy("hoteles, rentas y operadores de tours",
      "En hospitality el viajero llega de lejos. El aeropuerto de Cancún movió 29,345,538 pasajeros en 2025, y 19,464,554 fueron internacionales.{{asur}} Son pasajeros que llegan y salen, no personas distintas, pero dejan clara una cosa: buena parte de tus huéspedes escribe en otro idioma y desde otro huso horario."),
  {"id": "datos", "h2": "1. Los huéspedes de temporadas pasadas vuelven", "bloques": [
    "Cada huésped que se hospedó contigo dejó un nombre, una fecha, a veces un motivo: luna de miel, viaje con amigos, trabajo remoto. Esa lista es la forma más directa de llenar la próxima temporada, porque ya conocen el lugar y ya confían.",
    "La ventaja está en invitarlos antes de que reserven en otro lado: unas semanas antes de la fecha en que vinieron el año pasado, o cuando abre la temporada que eligieron. Un huésped que vuelve directo no pasa por una plataforma.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Huéspedes para invitar · diciembre", "filas": [
        ("Familia Ortega", "Vino en Navidad 2025 · 3 noches", "Invitación lista"),
        ("Emma y Paul", "Aniversario en enero · escriben en inglés", "Enviar en inglés"),
        ("Retiro de yoga A.", "Grupo de 14 en marzo", "Proponer fechas"),
        ("Carlos V.", "Trabajo remoto · 2 semanas", "Avisar la temporada baja")]},
  ]},
  {"id": "prospectar", "h2": "2. Grupos que llenan semanas enteras", "bloques": [
    "Agencias, empresas con viajes de incentivo, organizadores de bodas y de retiros traen grupos que ocupan varias habitaciones a la vez. Buscan opciones con meses de anticipación y eligen a quien les contesta con una propuesta clara.",
    "La IA ayuda a encontrar a esos organizadores y a escribirles antes que tu competencia, con una propuesta que habla de lo que ellos necesitan: capacidad, espacios comunes, traslados y fechas.",
  ]},
  {"id": "confianza", "h2": "3. Reseñas y día a día que dan confianza", "bloques": [
    "El viajero reserva donde confía, y confía en lo que ve: reseñas recientes, fotos reales, respuestas a los comentarios. Mostrar el día a día del lugar con constancia, contestar cada reseña y pedirlas en el momento justo hace que te elijan frente a un hotel que solo tiene fotos de catálogo.",
    "Con IA el contenido y las respuestas salen todas las semanas, en tu tono y en los idiomas de tus huéspedes.",
  ]},
  {"id": "presencia", "h2": "4. Contestar en el idioma y el horario del huésped", "bloques": [
    "Quien planea un viaje desde otro país escribe cuando para ti es de madrugada, y escribe en su idioma. Si tarda en recibir respuesta, reserva en la plataforma que sí le contesta. Un asistente de IA responde al momento, en el idioma del huésped, con la información que aprobaste: disponibilidad, cómo llegar, qué incluye.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "WhatsApp · 03:12", "lineas": [
        ("yo", "Hi! Do you have a room for 2 adults from Jan 14 to 18?"),
        ("bot", "Hi! I'm the hotel's AI assistant. Yes, we have a garden suite for those dates. Would you like me to send the details and how to book directly?"),
        ("yo", "Yes please. Is there airport transfer?"),
        ("bot", "We can arrange a transfer from Cancún airport. I'll include it in the details, and our team will confirm the time with you in the morning."),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Recepción libre para atender", "bloques": [
    "Instrucciones de llegada, la clave del wifi, el horario del desayuno, el recordatorio del check-out: las mismas preguntas, todos los días. Cuando salen solas, recepción queda para recibir bien a quien llega y resolver lo que de verdad necesita una persona.",
    "También se ordena lo que pasa entre turnos: qué huésped pidió qué, qué quedó pendiente y qué reseña falta contestar.",
  ]},
  nohace("La IA no reemplaza la hospitalidad. Un cuarto que no está como en las fotos o una llegada mal resuelta no se compensan con respuestas en otro idioma. Lo que sí hace es que más viajeros te encuentren, reserven directo y lleguen bien informados."),
  cuidar("<strong>Reglas de cada plataforma.</strong> Si el huésped reservó por una plataforma, revisa sus condiciones antes de llevar la conversación o el pago a otro canal."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Tiempo hasta la primera respuesta, de día y de noche.",
            "Reservas directas frente a reservas por plataforma.",
            "Huéspedes que volvieron después de una invitación.",
            "Cotizaciones de grupos enviadas y cerradas.",
            "Reseñas nuevas y reseñas contestadas."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial en un hotel boutique?", "Para que vuelvan los huéspedes de temporadas pasadas, encontrar grupos, cuidar las reseñas, contestar en el idioma y el horario del huésped y quitarle a recepción las preguntas repetidas."),
  ("¿El asistente contesta en inglés y otros idiomas?", "Sí. Contesta en el idioma en que escribe el huésped, con la información que aprobaste, y pasa a tu equipo lo que no sabe resolver."),
  ("¿Ayuda a depender menos de las plataformas de reservas?", "Ayuda a que más reservas lleguen directo, sobre todo de huéspedes que ya te conocen. Las plataformas siguen siendo un canal; conviene revisar sus condiciones antes de mover conversaciones a otro lado."),
  ("¿Sirve para rentas vacacionales y tours?", "Sí. Las cinco ventajas son las mismas para un hotel, una renta o un operador de tours; cambian los detalles de cada conversación."),
  ("¿Por dónde empiezo?", "Por ver cuántos mensajes llegan fuera de horario y qué pasa con tus huéspedes anteriores. El Audit gratis de El Tío arma ese mapa y te dice qué ventaja tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabaja hoy tu hotel: de dónde llegan las reservas, cuánto tardan en recibir respuesta los mensajes de noche, qué pasa con tus huéspedes anteriores y dónde se va el tiempo de recepción.",
},
# ---------------------------------------------------------------- REAL ESTATE
{
 "slug": "como-usar-ia-en-una-inmobiliaria", "rubro": "real-estate", "rubro_nombre": "Real estate",
 "wa": "inmobiliarias", "about": "Inteligencia artificial para inmobiliarias",
 "title": "Cómo usar IA en una inmobiliaria en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA en una inmobiliaria en 2026: 5 ventajas que tu competencia ya aprovecha",
 "desc": "Las 5 ventajas de la inteligencia artificial para inmobiliarias, desarrolladoras y brokers en México: leads dormidos, propietarios nuevos, confianza, respuesta en minutos y seguimiento sin perder a nadie.",
 "bajada": "En una inmobiliaria cada contacto puede ser una operación grande, y la mayoría se pierde por falta de seguimiento, no por falta de interés. Esta guía explica las cinco ventajas que la IA da hoy en real estate, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "re-activo-archivo", "wh": (1536, 1024), "alt": "Archivo con carpetas de propiedades sobre un escritorio"},
 "ciudades": ["ciudad-de-mexico", "monterrey", "guadalajara", "queretaro", "tulum", "playa-del-carmen"],
 "guias_rel": [("/guias/crm-inmobiliaria-seguimiento-leads/", "CRM para inmobiliarias: seguimiento de leads de preventa y renta, con lo que pide la ley")],
 "secciones": [
  hoy("inmobiliarias y brokers",
      "En real estate la velocidad pesa. Un estudio publicado en Harvard Business Review encontró que las empresas que contactaban a un interesado dentro de la primera hora tenían casi siete veces más probabilidades de calificarlo que las que esperaban una hora más.{{hbr}} El estudio no es sobre inmobiliarias, pero quien deja sus datos en tres portales un domingo suele visitar con el primero que le contesta."),
  {"id": "datos", "h2": "1. Los contactos que no compraron siguen buscando", "bloques": [
    "Toda inmobiliaria tiene cientos de personas que preguntaron hace meses por una propiedad y no compraron. Muchas no compraron todavía: cambió su presupuesto, esperaban un crédito o no encontraron lo que buscaban. Esa lista está repartida en el WhatsApp de cada asesor y en hojas que nadie revisa.",
    "Ordenada, vale más que cualquier campaña nueva. La ventaja está en volver a escribirles con algo que encaje con lo que buscaban: la nueva preventa en la zona que pidieron, la baja de una renta, la unidad que se liberó.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Contactos para reactivar", "filas": [
        ("Andrea P.", "Buscaba 2 recámaras en Narvarte · marzo", "Nueva unidad en la zona"),
        ("Inversionista R.", "Preguntó por preventa · junio", "Avisar nueva torre"),
        ("Familia Gómez", "Esperaba crédito · agosto", "Preguntar cómo va"),
        ("Diego L.", "Renta hasta un tope · septiembre", "Dos opciones nuevas")]},
  ]},
  {"id": "prospectar", "h2": "2. Propietarios y compradores antes que otra inmobiliaria", "bloques": [
    "El inventario manda. Encontrar a propietarios que quieren vender o rentar antes que la inmobiliaria de al lado, y a compradores con un perfil claro, es lo que define cuántas operaciones cierras en el año.",
    "La IA ayuda a ubicar esas oportunidades en tus zonas y a escribir primero, con un mensaje que habla de la propiedad o de la búsqueda de cada persona y no de tu inmobiliaria.",
  ]},
  {"id": "confianza", "h2": "3. Confianza antes de la primera visita", "bloques": [
    "En una compra grande se elige a quien se conoce. Mostrar con constancia operaciones cerradas, el conocimiento de cada zona y el criterio para elegir una propiedad hace que el comprador llegue a la visita ya confiando en ti.",
    "Con IA ese contenido sale cada semana con tu voz, a partir de lo que tu equipo ya sabe y ya vive en la calle.",
  ]},
  {"id": "presencia", "h2": "4. Cada consulta contestada en minutos", "bloques": [
    "Las consultas llegan de noche y en fin de semana, justo cuando la oficina no está. Un asistente de IA contesta al momento con la ficha que aprobó tu equipo, hace las preguntas que el asesor necesita y agenda la visita.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "WhatsApp · domingo 20:05", "lineas": [
        ("yo", "Hola, vi la casa en renta de 3 recámaras. ¿Sigue disponible?"),
        ("bot", "Hola. Soy el asistente de IA de la inmobiliaria. Sí, sigue disponible. ¿Para cuándo buscas mudarte y cuántas personas vivirían?"),
        ("yo", "En diciembre, somos 4."),
        ("bot", "Perfecto. Te paso la ficha con los requisitos. ¿Te agendo una visita con un asesor? Tengo lugar el martes a las 17:00."),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Seguimiento sin perder a nadie entre chats", "bloques": [
    "Filtrar consultas, agendar visitas, recordar el siguiente contacto después de la visita, pedir documentos: es trabajo que se repite en cada operación y que se corta cuando el asesor está ocupado. Cuando sale solo, cada contacto tiene un responsable y un siguiente paso con fecha.",
    "El equipo comercial queda para lo que cierra operaciones: la visita, la negociación y la relación con el cliente.",
  ]},
  nohace("La IA no vende propiedades por sí sola. La visita, la negociación y la confianza con el comprador siguen en manos de tus asesores. Lo que sí hace es que ningún contacto se enfríe por falta de respuesta y que cada asesor llegue a la visita con la información completa."),
  cuidar("<strong>Información de cada propiedad.</strong> El asistente contesta solo con la ficha aprobada. En preventa, la ley pide información específica al comprador; la guía de CRM para inmobiliarias la explica a fondo."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Tiempo hasta el primer contacto con cada lead.",
            "Leads sin responsable o sin siguiente paso con fecha.",
            "Visitas agendadas y visitas hechas.",
            "Contactos anteriores que volvieron a responder.",
            "Leads por origen: portales, redes, referidos, anuncios."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial en una inmobiliaria?", "Para reactivar contactos que no compraron, encontrar propietarios y compradores antes que otra inmobiliaria, generar confianza con contenido constante, contestar cada consulta en minutos y no perder a nadie en el seguimiento."),
  ("¿La IA puede agendar visitas?", "Sí. Contesta con la ficha aprobada, hace las preguntas que el asesor necesita y agenda la visita en el horario disponible. Lo que no sabe resolver lo pasa a una persona."),
  ("¿Puedo escribirle a los leads de portales por WhatsApp?", "Para escribir tú primero por WhatsApp hace falta una plantilla aprobada y que la persona haya aceptado recibir tus mensajes. Si el lead te escribe, tienes 24 horas para contestar con mensajes libres.{{meta}}"),
  ("¿Sirve para una inmobiliaria chica o un broker independiente?", "Sí. Con menos asesores, cada contacto perdido pesa más; ordenar el seguimiento suele ser el primer paso."),
  ("¿Por dónde empiezo?", "Por ver cuántos contactos tienes sin seguimiento y cuánto tarda hoy la primera respuesta. El Audit gratis de El Tío arma ese mapa y te dice qué ventaja tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabaja hoy tu inmobiliaria: de dónde llegan los contactos, cuánto tardan en recibir respuesta, quién los atiende y dónde se corta el seguimiento.",
},
# ---------------------------------------------------------------- FITNESS
{
 "slug": "como-usar-ia-en-un-gimnasio", "rubro": "fitness", "rubro_nombre": "Fitness",
 "wa": "gimnasios", "about": "Inteligencia artificial para gimnasios y estudios",
 "title": "Cómo usar IA en un gimnasio en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA en un gimnasio en 2026: 5 ventajas que tu competencia ya aprovecha",
 "desc": "Las 5 ventajas de la inteligencia artificial para gimnasios y estudios en México: socios que vuelven, empresas y vecinos, comunidad en redes, respuesta al instante y altas y renovaciones solas.",
 "bajada": "Un gimnasio o un estudio vive de que la gente vuelva. Esta guía explica las cinco ventajas que la IA da hoy en fitness, desde recuperar socios que se fueron hasta que las renovaciones salgan solas, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "fi-clase-vacia", "wh": (1536, 1024), "alt": "Salón de clases vacío con colchonetas ordenadas"},
 "ciudades": ["ciudad-de-mexico", "monterrey", "guadalajara", "queretaro", "puebla"],
 "guias_rel": [("/guias/retencion-socios-gimnasio-reservas-clases/", "Retención de socios en gimnasios y estudios: bajas y reservas de clase")],
 "secciones": [
  hoy("gimnasios y estudios",
      "En fitness el problema de fondo es el hábito. Stefano DellaVigna y Ulrike Malmendier siguieron a 7,752 socios de tres gimnasios de Estados Unidos durante tres años: muchos iban menos de lo que esperaban al inscribirse y tardaban en darse de baja aunque ya no fueran.{{della}} Quien acompaña a sus socios a tiempo los conserva."),
  {"id": "datos", "h2": "1. Los socios que se fueron pueden volver", "bloques": [
    "Cada gimnasio tiene una lista larga de socios que se dieron de baja, alumnos que tomaron la clase de prueba y no volvieron y personas que preguntaron y nunca se inscribieron. Son personas que ya quisieron entrenar contigo.",
    "La ventaja está en escribirles en el momento justo: el inicio de año, el regreso de vacaciones, la clase nueva que encaja con lo que buscaban. Una invitación a tiempo regresa a más gente que un anuncio a desconocidos.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Socios para invitar esta semana", "filas": [
        ("Paola S.", "Baja en agosto · iba a spinning", "Nueva clase de las 7:00"),
        ("Ricardo M.", "Clase de prueba sin volver", "Invitación a segunda clase"),
        ("Fernanda L.", "Sin asistir hace 3 semanas", "Mensaje de su coach"),
        ("Equipo oficina Norte", "Preguntó por plan de empresa", "Enviar propuesta")]},
  ]},
  {"id": "prospectar", "h2": "2. Empresas y vecinos que todavía no te conocen", "bloques": [
    "Las empresas de tu zona buscan opciones de bienestar para sus equipos, y los vecinos que se mudaron hace poco todavía no eligieron dónde entrenar. Los dos llegan al gimnasio que les habla primero.",
    "La IA ayuda a encontrar a esas empresas y a escribirles con una propuesta pensada para su equipo, antes que el gimnasio de la otra cuadra.",
  ]},
  {"id": "confianza", "h2": "3. Comunidad que se ve en redes", "bloques": [
    "Se entrena donde uno se siente parte. Contar las clases, a los coaches y los avances de los socios cada semana hace que quien todavía no se inscribe ya sienta que conoce el lugar.",
    "Con IA el contenido se planea y se escribe todas las semanas con tu tono, y tu equipo solo aporta lo que pasa en el piso.",
  ]},
  {"id": "presencia", "h2": "4. Horarios y clases de prueba contestados al instante", "bloques": [
    "Las preguntas llegan a cualquier hora: qué clases hay mañana, si hay lugar, cómo es la clase de prueba. Si nadie contesta, la persona sigue buscando. Un asistente de IA contesta al momento y reserva el lugar.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "Instagram · 23:18", "lineas": [
        ("yo", "Hola, ¿tienen clase de prueba de funcional?"),
        ("bot", "Hola. Soy el asistente de IA del estudio. Sí, la clase de prueba es para nuevos alumnos. Hay lugar mañana a las 7:00 y a las 19:00. ¿Cuál te aparto?"),
        ("yo", "La de las 19:00."),
        ("bot", "Listo, quedó a tu nombre. Trae ropa cómoda y agua; llega diez minutos antes para conocer al coach."),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Altas, renovaciones y recordatorios solos", "bloques": [
    "Dar de alta a un socio, recordar el vencimiento, avisar el cambio de horario, confirmar la clase del día: trabajo que se repite cada mes y que se olvida en la semana más ocupada. Cuando sale solo, recepción y coaches quedan para entrenar y acompañar.",
    "También aparecen las señales a tiempo: quién dejó de venir, qué clase se vacía y qué horario conviene abrir.",
  ]},
  nohace("La IA no entrena a nadie ni crea comunidad desde cero. Una mala clase o un ambiente frío no se arreglan con recordatorios. Lo que sí hace es que más personas lleguen a probar y que nadie se vaya sin que te enteres."),
  cuidar("<strong>Condiciones de la membresía.</strong> El asistente explica las condiciones tal como están en tu contrato y pasa a una persona cualquier pedido de baja o de excepción."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Tiempo hasta la primera respuesta a cada consulta.",
            "Clases de prueba agendadas y alumnos que se inscribieron después.",
            "Socios sin asistir en las últimas tres semanas.",
            "Socios que volvieron después de una invitación.",
            "Renovaciones a tiempo frente a renovaciones atrasadas."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial en un gimnasio?", "Para que vuelvan los socios que se fueron, encontrar empresas y vecinos, mostrar la comunidad en redes, contestar horarios y clases de prueba al instante y que altas, renovaciones y recordatorios salgan solos."),
  ("¿La IA ayuda a que los socios no se den de baja?", "Ayuda a detectar a tiempo a quien dejó de venir y a escribirle antes de que se vaya. Lo que retiene es el gimnasio; la IA hace que nadie se pierda sin que te enteres."),
  ("¿Puedo escribirle a socios dados de baja por WhatsApp?", "Sí, si aceptaron recibir tus mensajes y usas una plantilla aprobada para escribir primero. Si alguien pide no recibir más mensajes, se respeta.{{wapol}}"),
  ("¿Sirve para un estudio chico de yoga o pilates?", "Sí. Las cinco ventajas son las mismas; en un estudio chico suele convenir empezar por los alumnos de prueba que no volvieron."),
  ("¿Por dónde empiezo?", "Por ver cuántos socios se fueron este año y cuánto tarda la primera respuesta. El Audit gratis de El Tío arma ese mapa y te dice qué ventaja tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabaja hoy tu gimnasio: cuántas consultas llegan, qué pasa con las clases de prueba, cuántos socios se fueron y dónde se va el tiempo de recepción.",
},
# ---------------------------------------------------------------- EVENTOS
{
 "slug": "como-usar-ia-en-eventos", "rubro": "eventos", "rubro_nombre": "Eventos",
 "wa": "eventos", "about": "Inteligencia artificial para empresas de eventos",
 "title": "Cómo usar IA en eventos en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA en una empresa de eventos en 2026: 5 ventajas que tu competencia ya aprovecha",
 "desc": "Las 5 ventajas de la inteligencia artificial para productoras, salones, promotores y wedding planners en México: clientes que repiten, empresas y agencias, confianza, cotizaciones el mismo día y todo en un solo lugar.",
 "bajada": "Productoras, salones, promotores y organizadores trabajan con fechas que no se mueven y clientes que deciden rápido. Esta guía explica las cinco ventajas que la IA da hoy en eventos, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "ev-consulta-noche", "wh": (1536, 1024), "alt": "Consulta de evento abierta en el teléfono de noche"},
 "ciudades": ["ciudad-de-mexico", "monterrey", "guadalajara", "cancun", "queretaro"],
 "guias_rel": [],
 "secciones": [
  hoy("productoras, salones y organizadores",
      "En eventos, quien cotiza primero suele quedarse con la fecha. Un estudio publicado en Harvard Business Review encontró que las empresas que contestaban a un interesado dentro de la primera hora tenían casi siete veces más probabilidades de concretar algo con él que las que esperaban una hora más.{{hbr}} Cuando alguien pide tres cotizaciones para la misma fecha, la que llega a la mañana siguiente compite en desventaja."),
  {"id": "datos", "h2": "1. Los clientes de eventos pasados repiten", "bloques": [
    "Cumpleaños, aniversarios de empresa, fiestas de fin de año, congresos anuales: muchas fechas vuelven cada año. Cada cliente que ya trabajó contigo dejó una fecha, un tipo de evento y un contacto. Esa lista es la forma más directa de llenar la agenda del año que viene.",
    "La ventaja está en escribirles antes de que empiecen a cotizar en otro lado, con la propuesta del evento que ya conocen.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Fechas que vuelven · próximos 90 días", "filas": [
        ("Empresa Logística N.", "Posada 2025 · 180 personas", "Proponer fecha"),
        ("Familia Herrera", "XV años de la hermana menor", "Escribir en enero"),
        ("Congreso dental", "Edición anual en marzo", "Enviar propuesta"),
        ("Agencia R.", "3 lanzamientos en 2025", "Pedir calendario 2027")]},
  ]},
  {"id": "prospectar", "h2": "2. Empresas, agencias y planners con varias fechas al año", "bloques": [
    "Un solo cliente que organiza varios eventos al año vale más que diez eventos sueltos. Empresas con equipos grandes, agencias de marketing y wedding planners buscan proveedores de confianza y se quedan con quien les resuelve bien la primera vez.",
    "La IA ayuda a encontrar a esos clientes en tu ciudad y a escribirles primero, con una propuesta que habla de lo que organizan.",
  ]},
  {"id": "confianza", "h2": "3. Nadie contrata un evento a ciegas", "bloques": [
    "Antes de contratar, el cliente quiere ver: montajes reales, detalles, testimonios, cómo se resolvió un imprevisto. Mostrar eso con constancia hace que llegue a la cotización ya convencido.",
    "Con IA el contenido de cada evento se convierte en publicaciones de la semana, sin que tu equipo deje de producir.",
  ]},
  {"id": "presencia", "h2": "4. Cotizaciones respondidas el mismo día", "bloques": [
    "Las consultas llegan mientras estás en pleno montaje. Un asistente de IA contesta al momento, hace las preguntas que necesitas para cotizar (fecha, personas, tipo de evento, lugar) y te deja la solicitud lista para responder.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "WhatsApp · sábado 18:30", "lineas": [
        ("yo", "Hola, quiero cotizar una boda para 150 personas en abril."),
        ("bot", "Hola. Soy el asistente de IA de la productora. Con gusto. ¿Ya tienen fecha y lugar, o buscan también el salón?"),
        ("yo", "Fecha 18 de abril, buscamos salón en la zona sur."),
        ("bot", "Anotado. El equipo te manda la cotización con opciones de salón el lunes antes de las 13:00. ¿Te la envío por aquí?"),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Cotizar, confirmar y cobrar desde un solo lugar", "bloques": [
    "Cotizaciones en un chat, proveedores en otro, anticipos en una hoja: así se pierden fechas y pagos. Cuando cotizar, confirmar proveedores y dar seguimiento a los pagos queda en un solo lugar, el equipo deja de buscar información y se dedica a producir.",
    "Los recordatorios de anticipo y de saldo salen solos, y cada evento tiene su historial para la próxima vez.",
  ]},
  nohace("La IA no produce el evento. El montaje, los proveedores y la operación del día siguen siendo trabajo de tu equipo. Lo que sí hace es que no se te escape una solicitud por estar en pleno montaje y que cada cliente vuelva a pensar en ti cuando se acerque su fecha."),
  cuidar("<strong>Lo que se promete.</strong> El asistente no confirma fechas ni condiciones que no aprobó tu equipo; toma los datos y pasa la cotización a una persona."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Tiempo hasta la primera respuesta a cada solicitud.",
            "Cotizaciones enviadas el mismo día.",
            "Cotizaciones que se convirtieron en evento.",
            "Clientes anteriores que volvieron a contratar.",
            "Anticipos y saldos cobrados a tiempo."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial en una empresa de eventos?", "Para que repitan los clientes de eventos pasados, encontrar empresas y planners con varias fechas al año, mostrar tu trabajo con constancia, contestar solicitudes el mismo día y ordenar cotizaciones, proveedores y pagos."),
  ("¿La IA puede cotizar un evento?", "Puede tomar todos los datos que necesitas para cotizar y dejarte la solicitud lista. La cotización final y las condiciones las define tu equipo."),
  ("¿Sirve para un salón o un promotor chico?", "Sí. Las cinco ventajas son las mismas; en un negocio chico suele convenir empezar por contestar a tiempo y por los clientes que ya tienes."),
  ("¿Puedo escribirle a clientes de años anteriores?", "Sí, si aceptaron recibir tus mensajes y usas una plantilla aprobada para escribir tú primero por WhatsApp.{{meta}}"),
  ("¿Por dónde empiezo?", "Por ver cuántas solicitudes llegan, cuánto tardas en cotizar y cuántos clientes repiten. El Audit gratis de El Tío arma ese mapa y te dice qué ventaja tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabaja hoy tu empresa de eventos: cuántas solicitudes llegan, cuánto tardas en cotizar, qué pasa con los clientes de años anteriores y dónde se pierden pagos y fechas.",
},
# ---------------------------------------------------------------- ARTISTAS
{
 "slug": "como-usar-ia-siendo-artista", "rubro": "artistas", "rubro_nombre": "Artistas",
 "wa": "artistas", "about": "Inteligencia artificial para artistas, DJs y managers",
 "title": "Cómo usar IA siendo artista en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA siendo artista en 2026: 5 ventajas que otros artistas ya aprovechan",
 "desc": "Las 5 ventajas de la inteligencia artificial para artistas, músicos, DJs y managers en México: público que vuelve, salas y marcas, constancia en redes y la agenda en orden sin dejar de crear.",
 "bajada": "Un artista, un DJ o un manager vive de su público y de su agenda, y casi nunca tiene tiempo para ordenar ninguno de los dos. Esta guía explica las cinco ventajas que la IA da hoy a quien crea, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "ar-fichas-fans", "wh": (1024, 1024), "alt": "Fichas de público ordenadas sobre una mesa de estudio"},
 "ciudades": ["ciudad-de-mexico", "guadalajara", "monterrey", "tulum"],
 "guias_rel": [("/guias/como-aparecer-en-chatgpt-y-google-negocio-pequeno/", "Cómo aparecer en ChatGPT y en Google si tienes un negocio pequeño")],
 "secciones": [
  hoy("artistas, estudios y proyectos independientes",
      "En el mundo de los artistas la diferencia la hace la constancia. Las salas, los festivales y las marcas eligen a quien ven activo, y el público sigue a quien le habla seguido. Quien ordena su público y su agenda hoy llega antes a las fechas que importan."),
  {"id": "datos", "h2": "1. Tu público se entera primero", "bloques": [
    "Quien ya compró una entrada, una obra, un disco o una clase tuya es tu público más valioso. Esos contactos suelen quedar repartidos entre la boletera, los mensajes directos y una lista vieja.",
    "La ventaja está en ordenarlos y avisarles primero de lo próximo: la fecha nueva en su ciudad, la preventa, la obra que salió del estudio. Un público avisado llena la primera fila.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Público para avisar · fecha en Guadalajara", "filas": [
        ("312 personas", "Compraron entrada en GDL en 2025", "Aviso de preventa"),
        ("48 personas", "Preguntaron por la gira y no había fecha", "Avisar primero"),
        ("Coleccionistas", "Compraron obra en la última muestra", "Invitación privada"),
        ("Alumnos del taller", "Taller de verano", "Nueva fecha")]},
  ]},
  {"id": "prospectar", "h2": "2. Salas, marcas y festivales que buscan perfiles como el tuyo", "bloques": [
    "Las salas arman su programación con meses de anticipación, los festivales buscan nombres para cada edición y las marcas buscan artistas para sus activaciones. Muchas de esas oportunidades se cierran antes de que te enteres.",
    "La IA ayuda a encontrar a esos programadores y productores y a escribirles a tiempo, con una propuesta que muestra por qué tu perfil encaja con lo que hacen.",
  ]},
  {"id": "confianza", "h2": "3. El público sigue a las personas", "bloques": [
    "La gente se engancha con el proceso: el ensayo, el boceto, la prueba de sonido, el viaje a la próxima fecha. Contarlo con constancia construye un público que te elige cuando sale algo nuevo.",
    "Con IA lo que ya pasa en tu día se convierte en publicaciones de la semana con tu voz, sin que tengas que sentarte a escribir cada una.",
  ]},
  {"id": "presencia", "h2": "4. Publicar seguido sin dejar de crear", "bloques": [
    "El riesgo de cualquier artista es desaparecer de las redes cuando está creando. Planear y preparar el contenido por adelantado te mantiene presente mientras estás en el estudio, y un asistente de IA contesta las preguntas de siempre: fechas, dónde comprar, cómo contratarte.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "Instagram · 01:47", "lineas": [
        ("yo", "¿Cuándo vienes a Monterrey?"),
        ("bot", "Hola. Soy el asistente de IA del equipo. Todavía no hay fecha en Monterrey. ¿Quieres que te avisemos primero cuando se anuncie?"),
        ("yo", "Sí porfa"),
        ("bot", "Listo, quedaste en la lista de Monterrey. Te escribimos por aquí en cuanto haya fecha y preventa."),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Agenda y contrataciones en orden", "bloques": [
    "Solicitudes de contratación por cinco canales, condiciones técnicas que se piden una y otra vez, fechas que se cruzan: el desorden de la agenda le quita horas a la obra. Cuando las solicitudes entran a un solo lugar con los datos completos, tú o tu manager deciden rápido y bien.",
    "El tiempo que se libera vuelve a lo que solo tú haces: crear.",
  ]},
  nohace("La IA no crea tu obra ni reemplaza tu voz. Lo que publicas y lo que dices a tu público tiene que sonar a ti, y eso lo decides tú. Lo que sí hace es ordenar todo lo que rodea a la obra para que te quede tiempo para crearla."),
  cuidar("<strong>Tu voz es tuya.</strong> El asistente se presenta como asistente del equipo, nunca como el artista, y lo que se publica pasa por tu aprobación."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Personas en tu lista de público, por ciudad.",
            "Entradas u obras vendidas en la preventa a tu lista.",
            "Propuestas enviadas a salas, festivales y marcas, y respuestas.",
            "Publicaciones de la semana.",
            "Solicitudes de contratación respondidas el mismo día."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial a un artista?", "Para ordenar a tu público y avisarle primero, encontrar salas, marcas y festivales, contar tu proceso con constancia, publicar seguido sin dejar de crear y tener la agenda y las contrataciones en orden."),
  ("¿La IA va a crear mi obra?", "No. Esta guía es sobre el negocio alrededor de tu obra: público, agenda, contrataciones y redes. Lo que creas sigue siendo tuyo."),
  ("¿Sirve para un DJ o un músico independiente?", "Sí. Con un equipo chico o sin equipo, ordenar el público y la agenda es lo que más tiempo libera."),
  ("¿Puedo escribirle a quien compró entradas?", "Sí, si aceptó recibir tus mensajes. Para escribir tú primero por WhatsApp hace falta una plantilla aprobada.{{meta}}"),
  ("¿Por dónde empiezo?", "Por ver dónde está hoy tu público y cómo llegan las contrataciones. El Audit gratis de El Tío arma ese mapa y te dice qué ventaja tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabajas hoy: dónde está tu público, cómo llegan las contrataciones, qué publicas y dónde se va el tiempo que debería ser para crear.",
},
# ---------------------------------------------------------------- DISTRIBUCION
{
 "slug": "como-usar-ia-en-una-distribuidora", "rubro": "distribucion", "rubro_nombre": "Distribución",
 "wa": "distribuidoras", "about": "Inteligencia artificial para distribuidoras y mayoristas",
 "title": "Cómo usar IA en una distribuidora en 2026: 5 ventajas · El Tío",
 "h1": "Cómo usar IA en una distribuidora en 2026: 5 ventajas que tu competencia ya aprovecha",
 "desc": "Las 5 ventajas de la inteligencia artificial para distribuidoras, mayoristas, ferreterías e importadores en México: clientes que dejaron de pedir, cuentas nuevas, confianza, catálogo al instante y pedidos en orden.",
 "bajada": "Una distribuidora vive de clientes que piden seguido, y pierde dinero cada vez que uno deja de pedir sin que nadie lo note. Esta guía explica las cinco ventajas que la IA da hoy en distribución, con ejemplos de cómo se ven y qué conviene medir.",
 "img": {"src": "di-mostrador-pedidos", "wh": (1536, 1024), "alt": "Mostrador de pedidos de una distribuidora con hojas y cajas"},
 "ciudades": ["monterrey", "guadalajara", "ciudad-de-mexico", "puebla", "queretaro"],
 "guias_rel": [("/guias/pedidos-whatsapp-cotizaciones-distribuidoras/", "Pedidos por WhatsApp a cotización para distribuidoras y ferreterías")],
 "secciones": [
  hoy("distribuidoras, mayoristas y ferreterías",
      "En distribución el comprador compara rápido. Un estudio publicado en Harvard Business Review encontró que las empresas que contestaban a un interesado dentro de la primera hora tenían casi siete veces más probabilidades de concretar algo con él que las que esperaban una hora más.{{hbr}} Cuando una tienda pide precio y disponibilidad a tres proveedores, suele comprarle al que contesta primero con el dato correcto."),
  {"id": "datos", "h2": "1. Los clientes que dejaron de pedir, a tiempo", "bloques": [
    "Una tienda que pedía cada semana y lleva un mes sin pedir casi siempre está comprando en otro lado. En la mayoría de las distribuidoras nadie se da cuenta hasta que ya es tarde, porque los pedidos están repartidos entre vendedores, mensajes y notas.",
    "La ventaja está en detectar ese silencio a tiempo y escribir antes de perder al cliente, con algo concreto: el producto que pedía siempre, la reposición que le toca, la novedad que encaja con su negocio.",
    {"h3": "Cómo se ve"},
    {"tipo": "panel", "titulo": "Clientes que bajaron su pedido", "filas": [
        ("Ferretería El Puente", "Pedía cada semana · 34 días sin pedir", "Escribir hoy"),
        ("Abarrotes Sofi", "Bajó a la mitad su pedido", "Preguntar qué pasó"),
        ("Restaurante La Loma", "Dejó de pedir aceite", "Ofrecer reposición"),
        ("Tlapalería Centro", "Pide cada 15 días · al día", "Sin acción")]},
  ]},
  {"id": "prospectar", "h2": "2. Tiendas y negocios que todavía no te compran", "bloques": [
    "En tu zona de reparto hay tiendas, restaurantes y negocios que hoy le compran a otro proveedor o que abrieron hace poco. Cada uno es una ruta más llena con el mismo camión.",
    "La IA ayuda a encontrarlos y a escribirles primero, con una propuesta que habla de lo que venden ellos y no de tu catálogo completo.",
  ]},
  {"id": "confianza", "h2": "3. Confianza para cambiar de proveedor", "bloques": [
    "El comprador cambia de proveedor cuando confía en que no le vas a fallar. Mostrar con constancia tu catálogo, tus entregas y el respaldo que das cuando algo sale mal hace que esa decisión sea más fácil.",
    "Con IA ese contenido sale cada semana sin quitarle tiempo al almacén ni a los vendedores.",
  ]},
  {"id": "presencia", "h2": "4. Catálogo y disponibilidad al instante", "bloques": [
    "Las preguntas de siempre llegan a toda hora: si hay, cuánto tarda, si llega a tal colonia. Un asistente de IA contesta al momento con el catálogo y la disponibilidad que aprobaste, arma el pedido y lo pasa a tu equipo para confirmar.",
    {"h3": "Cómo se ve"},
    {"tipo": "chat", "titulo": "WhatsApp · 06:50", "lineas": [
        ("yo", "Buen día, ¿tienen cemento gris y varilla de 3/8?"),
        ("bot", "Buen día. Soy el asistente de IA de la distribuidora. Sí, hay de los dos. ¿Cuántas piezas de cada uno y para qué dirección?"),
        ("yo", "20 bultos y 50 varillas, colonia Industrial."),
        ("bot", "Anotado. Te paso el pedido para confirmar y el horario de entrega en tu zona. Un vendedor te confirma antes de las 9:00."),
        ("nota", "Conversación de ejemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Pedidos, inventario y rutas sin capturar a mano", "bloques": [
    "Pasar pedidos de mensajes a una hoja, revisar existencias, armar la ruta del día y avisar al cliente que va en camino: trabajo que se repite todos los días y donde aparecen los errores. Cuando sale solo, el equipo se dedica a vender y a resolver.",
    "Y con los pedidos ordenados ves lo que antes no se veía: qué clientes crecen, qué productos rotan y qué ruta conviene ajustar.",
  ]},
  nohace("La IA no reparte ni negocia precios. La entrega a tiempo y la relación con cada comprador siguen siendo de tu equipo. Lo que sí hace es que ningún pedido se pierda entre mensajes y que te enteres antes de que un cliente se vaya con otro proveedor."),
  cuidar("<strong>Precios y existencias reales.</strong> El asistente contesta solo con el catálogo y la disponibilidad que tu equipo aprobó, y cualquier pedido fuera de lo normal pasa a un vendedor."),
  {"id": "medir", "h2": "Cómo saber si funciona", "bloques": [
    "Cinco números, cada semana:",
    {"ol": ["Tiempo hasta la primera respuesta a cada consulta.",
            "Clientes que bajaron su frecuencia de pedido.",
            "Clientes recuperados después de un mensaje.",
            "Cuentas nuevas abiertas en el mes.",
            "Pedidos capturados sin errores."]},
  ]},
 ],
 "faq": [
  ("¿Para qué sirve la inteligencia artificial en una distribuidora?", "Para detectar a tiempo a los clientes que dejan de pedir, abrir cuentas nuevas en tu zona, generar confianza, contestar catálogo y disponibilidad al instante y ordenar pedidos, inventario y rutas."),
  ("¿La IA puede tomar pedidos por WhatsApp?", "Sí. Contesta con el catálogo aprobado, arma el pedido y lo pasa a tu equipo para confirmar. La guía de pedidos por WhatsApp para distribuidoras lo explica a fondo."),
  ("¿Sirve para una ferretería o un mayorista chico?", "Sí. Con menos vendedores, cada cliente que deja de pedir pesa más; detectarlo a tiempo suele ser el primer paso."),
  ("¿Puedo escribirle a mis clientes por WhatsApp para ofrecer productos?", "Sí, si aceptaron recibir tus mensajes y usas una plantilla aprobada para escribir tú primero. Si el cliente te escribe, tienes 24 horas para contestar con mensajes libres.{{meta}}"),
  ("¿Por dónde empiezo?", "Por ver cuántos clientes bajaron su pedido este año y cuánto tarda la primera respuesta. El Audit gratis de El Tío arma ese mapa y te dice qué ventaja tomar primero."),
 ],
 "cierre": "Antes de instalar nada, El Tío mira cómo trabaja hoy tu distribuidora: cómo llegan los pedidos, cuánto tardan en recibir respuesta, qué clientes bajaron su pedido y dónde se va el tiempo de captura.",
},
]
