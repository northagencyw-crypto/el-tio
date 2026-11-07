"""English version of the pillar guides. See guias_pilar.py.
Rules: only sourced data, examples marked as examples, no prices, no calls, no dashes."""

FUENTES_EN = {
 "mck": "McKinsey &amp; Company, «The State of AI in 2025», global survey published in November 2025: 88% of organizations regularly use AI in at least one business function.",
 "ind": "El Tío, «Índice El Tío», edition 1, November 2026: 83,714 businesses with up to 50 people in four Mexican states, based on INEGI's National Statistical Directory of Economic Units (DENUE).",
 "hbr": "James B. Oldroyd, Kristina McElheran and David Elkington, «The Short Life of Online Sales Leads», Harvard Business Review, March 2011.",
 "asur": "ASUR, «ASUR Announces Total Passenger Traffic for December 2025», January 6, 2026 release with Cancún airport traffic from January to December 2025, reproduced by Stock Titan.",
 "della": "Stefano DellaVigna and Ulrike Malmendier, «Paying Not to Go to the Gym», American Economic Review, vol. 96, no. 3, June 2006, pp. 694 to 719.",
 "meta": "Meta, «Pricing on the WhatsApp Business Platform», developer documentation: 24-hour customer service window, template and free-form messages and user opt-in.",
 "wapol": "WhatsApp, «WhatsApp Business Messaging Policy», updated September 23, 2026.",
 "lfpd": "Mexico's Federal Law on the Protection of Personal Data Held by Private Parties, Diario Oficial de la Federación, March 20, 2025. Current text at the Chamber of Deputies.",
}

CITY_EN = {"ciudad-de-mexico": "Mexico City", "monterrey": "Monterrey", "guadalajara": "Guadalajara", "tulum": "Tulum",
           "cancun": "Cancún", "playa-del-carmen": "Playa del Carmen", "puebla": "Puebla", "queretaro": "Querétaro"}


def rel_en(pag, nombre, es_slug, es_titulo, guias, ciudades, rubro):
    r = [f'<li><a href="{pag}">{nombre}</a>: the industry page</li>',
         f'<li><a href="/guias/{es_slug}/">{es_titulo}</a>: this guide in Spanish</li>']
    r += [f'<li><a href="{u}">{t}</a></li>' for u, t in guias]
    r += [f'<li><a href="/negocios/{c}/{rubro}/">{nombre} in {CITY_EN[c]}</a></li>' for c in ciudades]
    r += [f'<li><a data-cta="audit" href="https://app.eltio.net/auditoria/{rubro}">Free Audit for your business</a></li>']
    return r


def hoy(rubro_txt, extra):
    return {"id": "hoy", "h2": "Why the advantage is today", "bloques": [
        "Large companies have already moved. In McKinsey's global survey published in November 2025, 88% of organizations said they regularly use artificial intelligence in at least one business function.{{mck}}",
        f"Most small businesses have not started yet. In the Índice El Tío we counted 83,714 businesses with up to 50 people in four Mexican states using INEGI's business directory, and 94 out of 100 have no registered website.{{{{ind}}}} If many {rubro_txt} still lack the basics, whoever adds AI to the way they work today gets ahead in their area.",
        extra,
        "That gap is the window. Today one step is enough. Once most of your competitors have started, you will need ten steps to reach the same place. The five advantages below are the ones that come up most in your industry, ordered from what you already have to what you are missing.",
    ]}


def nohace(txt):
    return {"id": "no-hace", "h2": "What AI does not do for you", "bloques": [
        "It is worth being clear from the start, because it avoids expectations that disappoint later.",
        txt,
        "It does not replace your team either. It takes the repetitive work off their hands and alerts them in time to what needs a person. The businesses that get the most out of it decide first what they want to achieve and only then what to automate, not the other way around.",
        "And it is not installed overnight. You start with one advantage, measure it for a few weeks and add the next one. What matters is taking the first step while most of your competitors have not.",
    ]}


def cuidar(extra):
    return {"id": "cuidar", "h2": "What to look after", "bloques": [
        "AI works with your customers, and the rules are the same as for your team.",
        {"lista": [
            "<strong>Permission to write first.</strong> If the customer writes to you, you have 24 hours to reply with free-form messages. To write first on WhatsApp you need an approved template and the person's consent to receive your messages.{{meta}}",
            "<strong>Respect whoever says no.</strong> The WhatsApp Business policy requires you to stop messaging anyone who asks, and cold messaging a purchased list puts your number at risk.{{wapol}}",
            "<strong>Personal data.</strong> Your customers' names, phone numbers and history are covered by Mexico's 2025 data protection law: your privacy notice has to say what you keep and why.{{lfpd}}",
            "<strong>Say it is an assistant.</strong> Whoever writes knows an AI assistant is replying and that a person can take over when needed.",
            extra,
        ]},
    ]}


def medir(items):
    return {"id": "medir", "h2": "How to know it works", "bloques": ["Five numbers, every week:", {"ol": items}]}


GUIAS_EN = [
# ---------------------------------------------------------------- RESTAURANTS
{
 "es": "como-usar-ia-en-un-restaurante", "slug": "how-to-use-ai-in-a-restaurant", "rubro": "gastronomia", "rubro_nombre": "Restaurants",
 "wa": "restaurantes", "about": "Artificial intelligence for restaurants",
 "title": "How to use AI in a restaurant in 2026: 5 advantages · El Tío",
 "h1": "How to use AI in a restaurant in 2026: 5 advantages your competitors already use",
 "desc": "The 5 advantages of artificial intelligence for restaurants, bars and cafés in Mexico: returning customers, company events, social media, replies in the middle of service and less repetitive work.",
 "bajada": "A restaurant already has what matters most for AI: hundreds of customers who messaged, booked or ordered delivery. This guide explains the five advantages that separate the restaurants that move from the ones that wait, with examples of what they look like and what to measure.",
 "img": {"src": "gas-ent-telefono-noche", "wh": (1024, 1536), "alt": "Phone lit up on the host stand after closing time"},
 "rel": rel_en("/en/restaurants/", "Restaurants", "como-usar-ia-en-un-restaurante", "Cómo usar IA en un restaurante en 2026",
               [("/en/guides/whatsapp-chatbot-restaurants-mexico-city/", "WhatsApp chatbot for restaurants in Mexico City: the in-depth guide to bookings and orders")],
               ["ciudad-de-mexico", "monterrey", "guadalajara"], "gastronomia"),
 "secciones": [
  hoy("restaurants, bars and cafés",
      "In a restaurant the difference shows quickly. The customer asking for a table at nine at night books wherever answers first, and the group looking for a place to celebrate picks the spot they keep seeing on social media."),
  {"id": "datos", "h2": "1. Customers who already messaged you come back", "bloques": [
    "Every booking, every delivery order and every WhatsApp question leaves a name, a date and what that person ordered. In most restaurants that information sits idle on the manager's phone. Organized, it is the most valuable customer list you have, because these are people who already know you.",
    "The advantage is inviting them back at the right moment: their birthday, the anniversary of their first visit, the return of the seasonal dish they ordered last year. Bringing back someone who already ate with you is easier than convincing a stranger.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Customers to invite this week", "filas": [
        ("Mariana R.", "Birthday on Thursday · 4 visits", "Invitation ready"),
        ("Polanco office group", "End of month lunch · 12 people", "Remind on Monday"),
        ("Jorge T.", "Ordered chiles en nogada in 2025", "Announce its return"),
        ("Lucía M.", "No visit since July", "Come back invitation")]},
  ]},
  {"id": "prospectar", "h2": "2. Companies and groups before your competitors", "bloques": [
    "Team dinners, business breakfasts, year-end parties and large office orders fill tables on slow days. They rarely arrive on their own: someone at the company looks for options, asks two or three places and books wherever answers first and best.",
    "AI helps you find those companies in your area and reach them with a proposal made for them before the restaurant across the street does. Whoever arrives first with a clear option usually gets the event.",
  ]},
  {"id": "confianza", "h2": "3. Trust on social media, week after week", "bloques": [
    "Before trying a place, people look at it. They check your photos, your stories and how you answer comments. Showing the kitchen, the team and the dishes every week makes them choose you before tasting anything, because you already feel familiar.",
    "The usual problem is time: in high season nobody remembers to post. With AI the content is planned, written and organized in your voice, and your team only contributes what happens in the kitchen.",
  ]},
  {"id": "presencia", "h2": "4. Replying in the middle of service", "bloques": [
    "Messages arrive exactly when nobody can look at the phone: at lunch, at the dinner peak, at closing. A study published in Harvard Business Review found that companies that replied to a prospect within the first hour were nearly seven times more likely to make something happen with them than those that waited one hour longer.{{hbr}} The study is not about restaurants, but the logic applies just the same to someone asking for a table tonight.",
    "An AI assistant answers hours, menu, location and availability on the spot, takes the booking and hands a person whatever it cannot solve.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "WhatsApp · 21:40", "lineas": [
        ("yo", "Hi, do you have a table for 6 tonight at 10?"),
        ("bot", "Hi. I'm the restaurant's AI assistant. I have a table for 6 at 10:15 on the terrace. What name should I put it under?"),
        ("yo", "Daniel. Do you have gluten free options?"),
        ("bot", "Done, Daniel, table for 6 at 10:15. Yes, gluten free dishes are marked on the menu; here it is. If anyone has an allergy, let the waiter know when you arrive."),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. Less repetitive work, more team on the floor", "bloques": [
    "Confirming bookings, sending same-day reminders, answering ten times whether there is parking, passing orders to the kitchen: all of that eats hours of your best staff. When it runs on its own, the team is free for what only a person does: serving the table, recommending a wine, solving a problem on the spot.",
    "The repetitive work also leaves numbers. You know how many bookings came in by message, at what time people ask most and which days need an extra shift.",
  ]},
  nohace("AI does not cook or wait tables. A weak dish or bad service is not fixed with fast messages: the experience in the dining room is still what makes someone come back. What it does is bring more people in to try it and make sure those who already came remember you."),
  cuidar("<strong>Allergen information.</strong> The assistant answers only with the menu your kitchen approved and passes any allergy question that is not covered there to a person."),
  medir(["Time to first reply to each message, during service too.",
         "Bookings that came in by message and how many showed up.",
         "Customers who came back after an invitation.",
         "Company events and orders quoted and closed.",
         "Posts this week and messages that came in through social media."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for in a restaurant?", "To bring back the customers you already have, find companies and groups that fill slow days, show up consistently on social media, reply to messages in the middle of service and take repetitive work off the team, like confirming bookings."),
  ("Does a WhatsApp chatbot replace my host team?", "No. It answers what repeats and takes bookings, and hands a person whatever it cannot solve. The team stays free to look after customers in the dining room."),
  ("Can I message my past customers on WhatsApp?", "Yes, if they agreed to receive your messages and you use an approved template to write first. If the customer writes to you, you have 24 hours to reply with free-form messages.{{meta}}"),
  ("Does it work for a café or a small bar?", "Yes. The five advantages are the same; the volume changes. In a small business it usually makes sense to start with the customers you already have and with replying on time."),
  ("Where do I start?", "By looking at where bookings and customers get lost today. El Tío's free Audit maps that out for your restaurant and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how your restaurant works today: how many messages come in, how long they wait for a reply, what happens with customers who already came and where bookings get lost.",
},
# ---------------------------------------------------------------- HOSPITALITY
{
 "es": "como-usar-ia-en-un-hotel", "slug": "how-to-use-ai-in-a-hotel", "rubro": "hospitality", "rubro_nombre": "Hospitality",
 "wa": "hoteles", "about": "Artificial intelligence for hotels and tourism",
 "title": "How to use AI in a hotel in 2026: 5 advantages · El Tío",
 "h1": "How to use AI in a hotel in 2026: 5 advantages your competitors already use",
 "desc": "The 5 advantages of artificial intelligence for boutique hotels, vacation rentals and tour operators in Mexico: returning guests, groups, reviews, replies in the guest's language and less front desk busywork.",
 "bajada": "A boutique hotel, a vacation rental or a tour operator competes with the big platforms for the traveler's attention. This guide explains the five advantages AI gives hospitality businesses today, with examples of what they look like and what to measure.",
 "img": {"src": "ho-libro-novedades", "wh": (1024, 1024), "alt": "Logbook open on the front desk"},
 "rel": rel_en("/en/hospitality/", "Hospitality", "como-usar-ia-en-un-hotel", "Cómo usar IA en un hotel en 2026",
               [("/en/guides/direct-bookings-whatsapp-hotels/", "Direct bookings on WhatsApp for hotels and vacation rentals"),
                ("/en/guides/whatsapp-chatbot-tours-riviera-maya/", "WhatsApp chatbot for tours in Tulum and the Riviera Maya")],
               ["tulum", "cancun", "playa-del-carmen", "ciudad-de-mexico"], "hospitality"),
 "secciones": [
  {"id": "hoy", "h2": "Why the advantage is today", "bloques": [
    "Large companies have already moved. In McKinsey's global survey published in November 2025, 88% of organizations said they regularly use artificial intelligence in at least one business function.{{mck}}",
    "Most small businesses have not started yet. In the Índice El Tío we counted 83,714 businesses with up to 50 people in four Mexican states using INEGI's business directory, and 94 out of 100 have no registered website.{{ind}} If many hotels, rentals and tour operators still lack the basics, whoever adds AI to the way they work today gets ahead in their area.",
    "In hospitality the traveler comes from far away. Cancún airport handled 29,345,538 passengers in 2025, and 19,464,554 of them were international.{{asur}} Those are arriving and departing passengers, not distinct people, but the point is clear: a large share of your guests write in another language and from another time zone.",
    "That gap is the window. Today one step is enough. Once most of your competitors have started, you will need ten steps to reach the same place. The five advantages below are the ones that come up most in hospitality, ordered from what you already have to what you are missing.",
  ]},
  {"id": "datos", "h2": "1. Guests from past seasons come back", "bloques": [
    "Every guest who stayed with you left a name, a date and often a reason: honeymoon, a trip with friends, remote work. That list is the most direct way to fill next season, because they already know the place and already trust it.",
    "The advantage is inviting them before they book somewhere else: a few weeks before the date they came last year, or when the season they chose opens. A guest who comes back directly does not go through a platform.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Guests to invite · December", "filas": [
        ("Ortega family", "Came for Christmas 2025 · 3 nights", "Invitation ready"),
        ("Emma and Paul", "Anniversary in January · write in English", "Send in English"),
        ("Yoga retreat A.", "Group of 14 in March", "Propose dates"),
        ("Carlos V.", "Remote work · 2 weeks", "Announce low season")]},
  ]},
  {"id": "prospectar", "h2": "2. Groups that fill entire weeks", "bloques": [
    "Agencies, companies with incentive trips, wedding planners and retreat organizers bring groups that take several rooms at once. They look for options months ahead and choose whoever answers with a clear proposal.",
    "AI helps you find those organizers and reach them before your competitors, with a proposal about what they need: capacity, common areas, transfers and dates.",
  ]},
  {"id": "confianza", "h2": "3. Reviews and daily life that build trust", "bloques": [
    "Travelers book where they trust, and they trust what they see: recent reviews, real photos, replies to comments. Showing daily life at your place consistently, answering every review and asking for reviews at the right moment makes guests choose you over a hotel with catalog photos only.",
    "With AI, content and replies go out every week, in your tone and in your guests' languages.",
  ]},
  {"id": "presencia", "h2": "4. Replying in the guest's language and time zone", "bloques": [
    "Someone planning a trip from another country writes when it is the middle of the night for you, and writes in their language. If the reply takes too long, they book on the platform that does answer. An AI assistant replies right away, in the guest's language, with the information you approved: availability, how to get there, what is included.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "WhatsApp · 03:12", "lineas": [
        ("yo", "Hi! Do you have a room for 2 adults from Jan 14 to 18?"),
        ("bot", "Hi! I'm the hotel's AI assistant. Yes, we have a garden suite for those dates. Would you like me to send the details and how to book directly?"),
        ("yo", "Yes please. Is there airport transfer?"),
        ("bot", "We can arrange a transfer from Cancún airport. I'll include it in the details, and our team will confirm the time with you in the morning."),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. A front desk free to welcome guests", "bloques": [
    "Arrival instructions, the wifi password, breakfast hours, the check-out reminder: the same questions every day. When they are handled automatically, the front desk can welcome arriving guests properly and solve what really needs a person.",
    "What happens between shifts gets organized too: which guest asked for what, what is pending and which review still needs a reply.",
  ]},
  nohace("AI does not replace hospitality. A room that does not match the photos or a badly handled arrival is not fixed by fast replies in another language. What it does is help more travelers find you, book directly and arrive well informed."),
  {"id": "cuidar", "h2": "What to look after", "bloques": [
    "AI works with your guests, and the rules are the same as for your team.",
    {"lista": [
      "<strong>Permission to write first.</strong> If the guest writes to you, you have 24 hours to reply with free-form messages. To write first on WhatsApp you need an approved template and the person's consent to receive your messages.{{meta}}",
      "<strong>Respect whoever says no.</strong> The WhatsApp Business policy requires you to stop messaging anyone who asks, and cold messaging a purchased list puts your number at risk.{{wapol}}",
      "<strong>Personal data.</strong> Your guests' names, phone numbers and history are covered by Mexico's 2025 data protection law: your privacy notice has to say what you keep and why.{{lfpd}}",
      "<strong>Say it is an assistant.</strong> Whoever writes knows an AI assistant is replying and that a person can take over when needed.",
      "<strong>Each platform's rules.</strong> If the guest booked through a platform, check its terms before moving the conversation or the payment to another channel.",
    ]},
  ]},
  medir(["Time to first reply, day and night.",
         "Direct bookings versus platform bookings.",
         "Guests who came back after an invitation.",
         "Group quotes sent and closed.",
         "New reviews and reviews answered."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for in a boutique hotel?", "To bring back guests from past seasons, find groups, look after your reviews, reply in the guest's language and time zone and take repetitive questions off the front desk."),
  ("Does the assistant reply in English and other languages?", "Yes. It replies in the language the guest writes in, with the information you approved, and hands your team whatever it cannot solve."),
  ("Does it help me depend less on booking platforms?", "It helps more bookings come in directly, especially from guests who already know you. Platforms remain a channel; check their terms before moving conversations elsewhere."),
  ("Does it work for vacation rentals and tours?", "Yes. The five advantages are the same for a hotel, a rental or a tour operator; the details of each conversation change."),
  ("Where do I start?", "By looking at how many messages arrive after hours and what happens with your past guests. El Tío's free Audit maps that out and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how your hotel works today: where bookings come from, how long night messages wait for a reply, what happens with your past guests and where front desk time goes.",
},
# ---------------------------------------------------------------- REAL ESTATE
{
 "es": "como-usar-ia-en-una-inmobiliaria", "slug": "how-to-use-ai-in-a-real-estate-agency", "rubro": "real-estate", "rubro_nombre": "Real estate",
 "wa": "inmobiliarias", "about": "Artificial intelligence for real estate agencies",
 "title": "How to use AI in a real estate agency in 2026: 5 advantages · El Tío",
 "h1": "How to use AI in a real estate agency in 2026: 5 advantages your competitors already use",
 "desc": "The 5 advantages of artificial intelligence for real estate agencies, developers and brokers in Mexico: dormant leads, new owners, trust, replies within minutes and follow-up without losing anyone.",
 "bajada": "In a real estate agency every contact can become a large deal, and most are lost to missing follow-up, not to lack of interest. This guide explains the five advantages AI gives real estate today, with examples of what they look like and what to measure.",
 "img": {"src": "re-activo-archivo", "wh": (1536, 1024), "alt": "File box with property folders on a desk"},
 "rel": rel_en("/en/real-estate/", "Real estate", "como-usar-ia-en-una-inmobiliaria", "Cómo usar IA en una inmobiliaria en 2026",
               [("/en/guides/real-estate-crm-lead-follow-up/", "CRM for real estate: following up on pre-construction and rental leads, with what the law requires")],
               ["ciudad-de-mexico", "monterrey", "guadalajara", "tulum"], "real-estate"),
 "secciones": [
  hoy("real estate agencies and brokers",
      "In real estate speed matters. A study published in Harvard Business Review found that companies that contacted a prospect within the first hour were nearly seven times more likely to qualify them than those that waited one hour longer.{{hbr}} The study is not about real estate, but someone who leaves their details on three listing sites on a Sunday usually tours with whoever answers first."),
  {"id": "datos", "h2": "1. Contacts who did not buy are still looking", "bloques": [
    "Every agency has hundreds of people who asked about a property months ago and did not buy. Many simply have not bought yet: their budget changed, they were waiting on a mortgage or they did not find what they wanted. That list is scattered across each agent's WhatsApp and spreadsheets nobody checks.",
    "Organized, it is worth more than any new campaign. The advantage is writing to them again with something that fits what they were after: the new pre-construction project in the area they asked for, a rent that dropped, the unit that just opened up.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Contacts to reactivate", "filas": [
        ("Andrea P.", "Wanted 2 bedrooms in Narvarte · March", "New unit in the area"),
        ("Investor R.", "Asked about pre-construction · June", "Announce new tower"),
        ("Gómez family", "Waiting on a mortgage · August", "Ask how it is going"),
        ("Diego L.", "Rental with a set budget · September", "Two new options")]},
  ]},
  {"id": "prospectar", "h2": "2. Owners and buyers before another agency", "bloques": [
    "Inventory rules. Finding owners who want to sell or rent before the agency next door does, and buyers with a clear profile, is what decides how many deals you close in a year.",
    "AI helps you spot those opportunities in your areas and write first, with a message about each person's property or search rather than about your agency.",
  ]},
  {"id": "confianza", "h2": "3. Trust before the first showing", "bloques": [
    "In a large purchase people choose someone they know. Consistently showing closed deals, your knowledge of each neighborhood and your judgment in choosing a property means the buyer arrives at the showing already trusting you.",
    "With AI that content goes out every week in your voice, based on what your team already knows and sees on the street.",
  ]},
  {"id": "presencia", "h2": "4. Every inquiry answered within minutes", "bloques": [
    "Inquiries arrive at night and on weekends, exactly when the office is closed. An AI assistant replies right away with the listing your team approved, asks the questions the agent needs and books the showing.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "WhatsApp · Sunday 20:05", "lineas": [
        ("yo", "Hi, I saw the 3 bedroom house for rent. Is it still available?"),
        ("bot", "Hi. I'm the agency's AI assistant. Yes, it is still available. When are you looking to move and how many people would live there?"),
        ("yo", "In December, there are 4 of us."),
        ("bot", "Great. Here is the listing with the requirements. Shall I book a showing with an agent? There is an opening Tuesday at 5 pm."),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. Follow-up without losing anyone between chats", "bloques": [
    "Screening inquiries, booking showings, remembering the next touch after a showing, asking for documents: work that repeats in every deal and stops whenever the agent is busy. When it runs on its own, every contact has an owner and a dated next step.",
    "The sales team stays free for what closes deals: the showing, the negotiation and the relationship with the client.",
  ]},
  nohace("AI does not sell properties on its own. The showing, the negotiation and the buyer's trust stay in your agents' hands. What it does is make sure no contact goes cold for lack of a reply and that every agent arrives at the showing with complete information."),
  cuidar("<strong>Information on each property.</strong> The assistant answers only with the approved listing. For pre-construction sales the law requires specific information for the buyer; the real estate CRM guide explains it in depth."),
  medir(["Time to first contact with each lead.",
         "Leads with no owner or no dated next step.",
         "Showings booked and showings held.",
         "Past contacts who replied again.",
         "Leads by source: listing sites, social media, referrals, ads."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for in a real estate agency?", "To reactivate contacts who did not buy, find owners and buyers before another agency, build trust with consistent content, answer every inquiry within minutes and lose no one in follow-up."),
  ("Can AI book showings?", "Yes. It replies with the approved listing, asks the questions the agent needs and books the showing in an available slot. Whatever it cannot solve goes to a person."),
  ("Can I message leads from listing sites on WhatsApp?", "To write first on WhatsApp you need an approved template and the person's consent to receive your messages. If the lead writes to you, you have 24 hours to reply with free-form messages.{{meta}}"),
  ("Does it work for a small agency or an independent broker?", "Yes. With fewer agents, every lost contact weighs more; organizing follow-up is usually the first step."),
  ("Where do I start?", "By looking at how many contacts have no follow-up and how long the first reply takes today. El Tío's free Audit maps that out and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how your agency works today: where contacts come from, how long they wait for a reply, who handles them and where follow-up breaks down.",
},
# ---------------------------------------------------------------- FITNESS
{
 "es": "como-usar-ia-en-un-gimnasio", "slug": "how-to-use-ai-in-a-gym", "rubro": "fitness", "rubro_nombre": "Fitness",
 "wa": "gimnasios", "about": "Artificial intelligence for gyms and studios",
 "title": "How to use AI in a gym in 2026: 5 advantages · El Tío",
 "h1": "How to use AI in a gym in 2026: 5 advantages your competitors already use",
 "desc": "The 5 advantages of artificial intelligence for gyms and studios in Mexico: members who come back, companies and neighbors, community on social media, instant replies and sign-ups and renewals that run themselves.",
 "bajada": "A gym or a studio lives on people coming back. This guide explains the five advantages AI gives fitness businesses today, from winning back members who left to renewals that run themselves, with examples of what they look like and what to measure.",
 "img": {"src": "fi-clase-vacia", "wh": (1536, 1024), "alt": "Empty class studio with mats neatly lined up"},
 "rel": rel_en("/en/fitness/", "Fitness", "como-usar-ia-en-un-gimnasio", "Cómo usar IA en un gimnasio en 2026",
               [("/en/guides/gym-member-retention-class-bookings/", "Member retention for gyms and studios: cancellations and class bookings")],
               ["ciudad-de-mexico", "monterrey", "guadalajara"], "fitness"),
 "secciones": [
  hoy("gyms and studios",
      "In fitness the underlying problem is habit. Stefano DellaVigna and Ulrike Malmendier followed 7,752 members of three US gyms for three years: many went less often than they expected when they signed up and took a long time to cancel even after they stopped going.{{della}} Whoever supports members at the right time keeps them."),
  {"id": "datos", "h2": "1. Members who left can come back", "bloques": [
    "Every gym has a long list of members who canceled, students who took a trial class and never returned and people who asked and never signed up. These are people who already wanted to train with you.",
    "The advantage is writing to them at the right moment: the start of the year, the end of vacation, the new class that matches what they were looking for. A timely invitation brings back more people than an ad aimed at strangers.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Members to invite this week", "filas": [
        ("Paola S.", "Canceled in August · did spinning", "New 7 am class"),
        ("Ricardo M.", "Trial class, never returned", "Invite to a second class"),
        ("Fernanda L.", "No check-in for 3 weeks", "Message from her coach"),
        ("North office team", "Asked about a corporate plan", "Send proposal")]},
  ]},
  {"id": "prospectar", "h2": "2. Companies and neighbors who do not know you yet", "bloques": [
    "Companies in your area are looking for wellness options for their teams, and neighbors who recently moved in have not chosen where to train yet. Both end up at the gym that reaches them first.",
    "AI helps you find those companies and write to them with a proposal made for their team, before the gym on the next block does.",
  ]},
  {"id": "confianza", "h2": "3. A community people can see on social media", "bloques": [
    "People train where they feel they belong. Showing classes, coaches and members' progress every week means that someone who has not signed up yet already feels they know the place.",
    "With AI the content is planned and written every week in your tone, and your team only contributes what happens on the floor.",
  ]},
  {"id": "presencia", "h2": "4. Schedules and trial classes answered instantly", "bloques": [
    "Questions arrive at any hour: which classes are on tomorrow, whether there is room, how the trial class works. If nobody answers, the person keeps looking. An AI assistant replies right away and saves the spot.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "Instagram · 23:18", "lineas": [
        ("yo", "Hi, do you have a functional training trial class?"),
        ("bot", "Hi. I'm the studio's AI assistant. Yes, the trial class is for new students. There are spots tomorrow at 7 am and 7 pm. Which one should I save for you?"),
        ("yo", "The 7 pm one."),
        ("bot", "Done, it's under your name. Bring comfortable clothes and water, and arrive ten minutes early to meet the coach."),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. Sign-ups, renewals and reminders that run themselves", "bloques": [
    "Signing up a member, reminding them of the renewal date, announcing a schedule change, confirming today's class: work that repeats every month and gets forgotten in the busiest week. When it runs on its own, the front desk and the coaches are free to train and support people.",
    "The warning signs also show up in time: who stopped coming, which class is emptying out and which time slot is worth opening.",
  ]},
  nohace("AI does not train anyone or create a community from scratch. A bad class or a cold atmosphere is not fixed with reminders. What it does is bring more people in to try and make sure nobody leaves without you noticing."),
  cuidar("<strong>Membership terms.</strong> The assistant explains the terms exactly as they appear in your contract and passes any cancellation or exception request to a person."),
  medir(["Time to first reply to each inquiry.",
         "Trial classes booked and students who signed up afterwards.",
         "Members with no check-in in the last three weeks.",
         "Members who came back after an invitation.",
         "On-time renewals versus late renewals."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for in a gym?", "To bring back members who left, find companies and neighbors, show your community on social media, answer schedules and trial classes instantly and let sign-ups, renewals and reminders run themselves."),
  ("Does AI help keep members from canceling?", "It helps you spot in time who stopped coming and reach them before they leave. What keeps members is the gym; AI makes sure nobody slips away without you noticing."),
  ("Can I message former members on WhatsApp?", "Yes, if they agreed to receive your messages and you use an approved template to write first. If someone asks to stop receiving messages, that is respected.{{wapol}}"),
  ("Does it work for a small yoga or pilates studio?", "Yes. The five advantages are the same; in a small studio it usually makes sense to start with trial students who did not come back."),
  ("Where do I start?", "By looking at how many members left this year and how long the first reply takes. El Tío's free Audit maps that out and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how your gym works today: how many inquiries come in, what happens with trial classes, how many members left and where front desk time goes.",
},
# ---------------------------------------------------------------- EVENTS
{
 "es": "como-usar-ia-en-eventos", "slug": "how-to-use-ai-in-an-events-business", "rubro": "eventos", "rubro_nombre": "Events",
 "wa": "eventos", "about": "Artificial intelligence for event companies",
 "title": "How to use AI in events in 2026: 5 advantages · El Tío",
 "h1": "How to use AI in an events business in 2026: 5 advantages your competitors already use",
 "desc": "The 5 advantages of artificial intelligence for production companies, venues, promoters and wedding planners in Mexico: repeat clients, companies and agencies, trust, same-day quotes and everything in one place.",
 "bajada": "Production companies, venues, promoters and planners work with dates that do not move and clients who decide fast. This guide explains the five advantages AI gives events businesses today, with examples of what they look like and what to measure.",
 "img": {"src": "ev-consulta-noche", "wh": (1536, 1024), "alt": "Event inquiry open on a phone at night"},
 "rel": rel_en("/en/events/", "Events", "como-usar-ia-en-eventos", "Cómo usar IA en una empresa de eventos en 2026",
               [], ["ciudad-de-mexico", "monterrey", "guadalajara", "cancun"], "eventos"),
 "secciones": [
  hoy("production companies, venues and planners",
      "In events, whoever quotes first usually gets the date. A study published in Harvard Business Review found that companies that replied to a prospect within the first hour were nearly seven times more likely to make something happen with them than those that waited one hour longer.{{hbr}} When someone asks for three quotes for the same date, the one that arrives the next morning starts at a disadvantage."),
  {"id": "datos", "h2": "1. Clients from past events come back", "bloques": [
    "Birthdays, company anniversaries, year-end parties, annual conferences: many dates come around every year. Every client who already worked with you left a date, a type of event and a contact. That list is the most direct way to fill next year's calendar.",
    "The advantage is writing to them before they start asking for quotes elsewhere, with a proposal for the event they already know.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Dates that come back · next 90 days", "filas": [
        ("Logistics company N.", "2025 holiday party · 180 people", "Propose a date"),
        ("Herrera family", "Younger sister's quinceañera", "Write in January"),
        ("Dental conference", "Annual edition in March", "Send proposal"),
        ("Agency R.", "3 launches in 2025", "Ask for 2027 calendar")]},
  ]},
  {"id": "prospectar", "h2": "2. Companies, agencies and planners with several dates a year", "bloques": [
    "A single client who organizes several events a year is worth more than ten one-off events. Companies with large teams, marketing agencies and wedding planners look for suppliers they can trust and stay with whoever gets it right the first time.",
    "AI helps you find those clients in your city and write to them first, with a proposal about what they organize.",
  ]},
  {"id": "confianza", "h2": "3. Nobody hires an event blind", "bloques": [
    "Before hiring, clients want to see: real setups, details, testimonials, how something unexpected was handled. Showing that consistently means they arrive at the quote already convinced.",
    "With AI the content from each event becomes this week's posts, without your team having to stop producing.",
  ]},
  {"id": "presencia", "h2": "4. Quotes answered the same day", "bloques": [
    "Inquiries arrive while you are in the middle of a setup. An AI assistant replies right away, asks the questions you need to quote (date, guests, type of event, venue) and leaves the request ready for you to answer.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "WhatsApp · Saturday 18:30", "lineas": [
        ("yo", "Hi, I'd like a quote for a wedding for 150 people in April."),
        ("bot", "Hi. I'm the production company's AI assistant. Happy to help. Do you already have a date and venue, or are you also looking for a venue?"),
        ("yo", "April 18, and we're looking for a venue in the south of the city."),
        ("bot", "Noted. The team will send you the quote with venue options on Monday before 1 pm. Shall I send it here?"),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. Quoting, confirming and collecting from one place", "bloques": [
    "Quotes in one chat, suppliers in another, deposits in a spreadsheet: that is how dates and payments get lost. When quoting, confirming suppliers and tracking payments happen in one place, the team stops hunting for information and focuses on producing.",
    "Deposit and balance reminders go out on their own, and every event keeps its history for next time.",
  ]},
  nohace("AI does not produce the event. The setup, the suppliers and the operation on the day are still your team's work. What it does is make sure no request slips by while you are mid-setup and that every client thinks of you again as their date approaches."),
  cuidar("<strong>What gets promised.</strong> The assistant does not confirm dates or terms your team has not approved; it takes the details and hands the quote to a person."),
  medir(["Time to first reply to each request.",
         "Quotes sent the same day.",
         "Quotes that turned into events.",
         "Past clients who hired again.",
         "Deposits and balances collected on time."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for in an events business?", "To bring back clients from past events, find companies and planners with several dates a year, show your work consistently, answer requests the same day and organize quotes, suppliers and payments."),
  ("Can AI quote an event?", "It can collect all the details you need to quote and leave the request ready for you. The final quote and the terms are set by your team."),
  ("Does it work for a venue or a small promoter?", "Yes. The five advantages are the same; in a small business it usually makes sense to start with replying on time and with the clients you already have."),
  ("Can I message clients from previous years?", "Yes, if they agreed to receive your messages and you use an approved template to write first on WhatsApp.{{meta}}"),
  ("Where do I start?", "By looking at how many requests come in, how long you take to quote and how many clients come back. El Tío's free Audit maps that out and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how your events business works today: how many requests come in, how long you take to quote, what happens with clients from previous years and where payments and dates get lost.",
},
# ---------------------------------------------------------------- ARTISTS
{
 "es": "como-usar-ia-siendo-artista", "slug": "how-to-use-ai-as-an-artist", "rubro": "artistas", "rubro_nombre": "Artists",
 "wa": "artistas", "about": "Artificial intelligence for artists, DJs and managers",
 "title": "How to use AI as an artist in 2026: 5 advantages · El Tío",
 "h1": "How to use AI as an artist in 2026: 5 advantages other artists already use",
 "desc": "The 5 advantages of artificial intelligence for artists, musicians, DJs and managers in Mexico: an audience that comes back, venues and brands, consistency on social media and an organized calendar without giving up time to create.",
 "bajada": "An artist, a DJ or a manager lives on their audience and their calendar, and almost never has time to organize either. This guide explains the five advantages AI gives creators today, with examples of what they look like and what to measure.",
 "img": {"src": "ar-fichas-fans", "wh": (1024, 1024), "alt": "Audience cards arranged on a studio table"},
 "rel": rel_en("/en/artists/", "Artists", "como-usar-ia-siendo-artista", "Cómo usar IA siendo artista en 2026",
               [("/en/guides/show-up-in-chatgpt-and-google-small-business/", "How to show up on ChatGPT and Google if you run a small business")],
               ["ciudad-de-mexico", "guadalajara", "monterrey", "tulum"], "artistas"),
 "secciones": [
  hoy("artists, studios and independent projects",
      "For artists, consistency makes the difference. Venues, festivals and brands pick whoever they see active, and audiences follow whoever talks to them often. Whoever organizes their audience and calendar today gets to the dates that matter first."),
  {"id": "datos", "h2": "1. Your audience hears it first", "bloques": [
    "Anyone who already bought a ticket, a piece, a record or a class from you is your most valuable audience. Those contacts usually end up scattered between the ticketing platform, direct messages and an old list.",
    "The advantage is organizing them and telling them first about what comes next: the new date in their city, the presale, the piece that just left the studio. An audience that hears first fills the front row.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Audience to notify · Guadalajara date", "filas": [
        ("312 people", "Bought tickets in GDL in 2025", "Presale notice"),
        ("48 people", "Asked about the tour when there was no date", "Tell them first"),
        ("Collectors", "Bought work at the last show", "Private invitation"),
        ("Workshop students", "Summer workshop", "New date")]},
  ]},
  {"id": "prospectar", "h2": "2. Venues, brands and festivals looking for profiles like yours", "bloques": [
    "Venues plan their programming months ahead, festivals look for names for every edition and brands look for artists for their activations. Many of those opportunities close before you hear about them.",
    "AI helps you find those programmers and producers and write to them in time, with a proposal showing why your profile fits what they do.",
  ]},
  {"id": "confianza", "h2": "3. Audiences follow people", "bloques": [
    "People get hooked on the process: the rehearsal, the sketch, the sound check, the trip to the next date. Sharing it consistently builds an audience that picks you when something new comes out.",
    "With AI, what already happens in your day becomes this week's posts in your voice, without you having to sit down and write each one.",
  ]},
  {"id": "presencia", "h2": "4. Posting often without stopping creating", "bloques": [
    "Every artist runs the risk of disappearing from social media while creating. Planning and preparing content ahead of time keeps you present while you are in the studio, and an AI assistant answers the usual questions: dates, where to buy, how to book you.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "Instagram · 01:47", "lineas": [
        ("yo", "When are you coming to Monterrey?"),
        ("bot", "Hi. I'm the team's AI assistant. There is no Monterrey date yet. Would you like us to tell you first when it is announced?"),
        ("yo", "Yes please"),
        ("bot", "Done, you're on the Monterrey list. We'll write to you here as soon as there is a date and a presale."),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. Calendar and bookings in order", "bloques": [
    "Booking requests through five channels, technical riders asked for again and again, overlapping dates: a messy calendar takes hours away from the work. When requests come into one place with complete details, you or your manager decide quickly and well.",
    "The time you free up goes back to what only you do: creating.",
  ]},
  nohace("AI does not create your work or replace your voice. What you post and what you tell your audience has to sound like you, and you decide that. What it does is organize everything around the work so you have time left to make it."),
  cuidar("<strong>Your voice is yours.</strong> The assistant introduces itself as the team's assistant, never as the artist, and everything that gets posted goes through your approval."),
  medir(["People on your audience list, by city.",
         "Tickets or pieces sold in the presale to your list.",
         "Proposals sent to venues, festivals and brands, and replies.",
         "Posts this week.",
         "Booking requests answered the same day."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for as an artist?", "To organize your audience and tell them first, find venues, brands and festivals, share your process consistently, post often without stopping creating and keep your calendar and bookings in order."),
  ("Will AI create my work?", "No. This guide is about the business around your work: audience, calendar, bookings and social media. What you create is still yours."),
  ("Does it work for a DJ or an independent musician?", "Yes. With a small team or no team at all, organizing your audience and calendar is what frees up the most time."),
  ("Can I message people who bought tickets?", "Yes, if they agreed to receive your messages. To write first on WhatsApp you need an approved template.{{meta}}"),
  ("Where do I start?", "By looking at where your audience is today and how bookings come in. El Tío's free Audit maps that out and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how you work today: where your audience is, how bookings come in, what you post and where the time that should go to creating ends up.",
},
# ---------------------------------------------------------------- DISTRIBUTION
{
 "es": "como-usar-ia-en-una-distribuidora", "slug": "how-to-use-ai-in-a-distribution-business", "rubro": "distribucion", "rubro_nombre": "Distribution",
 "wa": "distribuidoras", "about": "Artificial intelligence for distributors and wholesalers",
 "title": "How to use AI in a distribution business in 2026: 5 advantages · El Tío",
 "h1": "How to use AI in a distribution business in 2026: 5 advantages your competitors already use",
 "desc": "The 5 advantages of artificial intelligence for distributors, wholesalers, hardware stores and importers in Mexico: customers who stopped ordering, new accounts, trust, an instant catalog and orders in order.",
 "bajada": "A distributor lives on customers who order often, and loses money every time one stops ordering without anyone noticing. This guide explains the five advantages AI gives distribution today, with examples of what they look like and what to measure.",
 "img": {"src": "di-mostrador-pedidos", "wh": (1536, 1024), "alt": "Order counter at a distributor with sheets and boxes"},
 "rel": rel_en("/en/distribution/", "Distribution", "como-usar-ia-en-una-distribuidora", "Cómo usar IA en una distribuidora en 2026",
               [("/en/guides/whatsapp-orders-quotes-distributors/", "WhatsApp orders to quotes for distributors and hardware stores")],
               ["monterrey", "guadalajara", "ciudad-de-mexico"], "distribucion"),
 "secciones": [
  hoy("distributors, wholesalers and hardware stores",
      "In distribution the buyer compares fast. A study published in Harvard Business Review found that companies that replied to a prospect within the first hour were nearly seven times more likely to make something happen with them than those that waited one hour longer.{{hbr}} When a store asks three suppliers for availability, it usually buys from the one that answers first with the right information."),
  {"id": "datos", "h2": "1. Customers who stopped ordering, caught in time", "bloques": [
    "A store that ordered every week and has not ordered in a month is almost always buying somewhere else. In most distributors nobody notices until it is too late, because orders are scattered between sales reps, messages and notes.",
    "The advantage is spotting that silence in time and writing before you lose the customer, with something concrete: the product they always ordered, the restock that is due, the new item that fits their business.",
    {"h3": "What it looks like"},
    {"tipo": "panel", "titulo": "Customers who cut back their orders", "filas": [
        ("El Puente hardware", "Ordered weekly · 34 days without an order", "Write today"),
        ("Abarrotes Sofi", "Order cut in half", "Ask what happened"),
        ("La Loma restaurant", "Stopped ordering oil", "Offer a restock"),
        ("Centro paint store", "Orders every 15 days · up to date", "No action")]},
  ]},
  {"id": "prospectar", "h2": "2. Stores and businesses that do not buy from you yet", "bloques": [
    "In your delivery area there are stores, restaurants and businesses that buy from another supplier today or opened recently. Each one is a fuller route with the same truck.",
    "AI helps you find them and write first, with a proposal about what they sell rather than your whole catalog.",
  ]},
  {"id": "confianza", "h2": "3. Trust to switch suppliers", "bloques": [
    "Buyers switch suppliers when they trust you will not let them down. Consistently showing your catalog, your deliveries and the support you give when something goes wrong makes that decision easier.",
    "With AI that content goes out every week without taking time from the warehouse or the sales reps.",
  ]},
  {"id": "presencia", "h2": "4. Catalog and availability instantly", "bloques": [
    "The usual questions arrive at all hours: is it in stock, how long does it take, do you deliver to this neighborhood. An AI assistant replies right away with the catalog and availability you approved, puts the order together and passes it to your team to confirm.",
    {"h3": "What it looks like"},
    {"tipo": "chat", "titulo": "WhatsApp · 06:50", "lineas": [
        ("yo", "Good morning, do you have gray cement and 3/8 rebar?"),
        ("bot", "Good morning. I'm the distributor's AI assistant. Yes, we have both. How many of each and to what address?"),
        ("yo", "20 bags and 50 bars, Industrial neighborhood."),
        ("bot", "Noted. Here is the order to confirm and the delivery window for your area. A sales rep will confirm before 9 am."),
        ("nota", "Example conversation.")]},
  ]},
  {"id": "optimizar", "h2": "5. Orders, inventory and routes without manual entry", "bloques": [
    "Copying orders from messages into a spreadsheet, checking stock, planning the day's route and telling the customer it is on the way: work that repeats every day and where errors appear. When it runs on its own, the team focuses on selling and solving.",
    "And with orders organized you see what you could not see before: which customers are growing, which products move and which route needs adjusting.",
  ]},
  nohace("AI does not deliver or negotiate prices. On-time delivery and the relationship with each buyer stay with your team. What it does is make sure no order gets lost between messages and that you find out before a customer goes to another supplier."),
  cuidar("<strong>Real prices and stock.</strong> The assistant answers only with the catalog and availability your team approved, and any unusual order goes to a sales rep."),
  medir(["Time to first reply to each inquiry.",
         "Customers who cut back how often they order.",
         "Customers won back after a message.",
         "New accounts opened this month.",
         "Orders entered without errors."]),
 ],
 "faq": [
  ("What is artificial intelligence useful for in a distribution business?", "To spot in time the customers who stop ordering, open new accounts in your area, build trust, answer catalog and availability questions instantly and organize orders, inventory and routes."),
  ("Can AI take orders on WhatsApp?", "Yes. It replies with the approved catalog, puts the order together and passes it to your team to confirm. The guide on WhatsApp orders for distributors explains it in depth."),
  ("Does it work for a hardware store or a small wholesaler?", "Yes. With fewer sales reps, every customer who stops ordering weighs more; spotting it in time is usually the first step."),
  ("Can I message my customers on WhatsApp to offer products?", "Yes, if they agreed to receive your messages and you use an approved template to write first. If the customer writes to you, you have 24 hours to reply with free-form messages.{{meta}}"),
  ("Where do I start?", "By looking at how many customers cut back their orders this year and how long the first reply takes. El Tío's free Audit maps that out and tells you which advantage to take first."),
 ],
 "cierre": "Before installing anything, El Tío looks at how your distribution business works today: how orders come in, how long they wait for a reply, which customers cut back their orders and where data entry time goes.",
},
]
