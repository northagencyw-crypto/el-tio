"""English versions of the 2027 guides for Tulum, Cancún and Playa del Carmen: /en/guides/2027/{slug}/.

Called from guias_2027.py (main), which writes the files, the sitemap and llms.txt.
Audience: foreign owners and managers in the Riviera Maya (hotels, villas, tour operators, real estate).
Rules: only sourced data (FUENTES), no prices, no dashes, no invented figures.
"""
from build import documento, migas, e, BASE, HOY, CABECERA, PIE
from guias_2027 import R, CARIBE, IMG, slug, slug_en, refs, wa, hero, ajustes
from guias_pilar_datos import FUENTES
from guias_pilar_en import FUENTES_EN

CITY = {"tulum": "Tulum", "cancun": "Cancún", "playa-del-carmen": "Playa del Carmen"}

RE = {
 "gastronomia": dict(name="Restaurants", plural="restaurants", one="a restaurant", your="your restaurant", customer="diners",
    asks="reservations, takeout orders and menu questions", pillar="how-to-use-ai-in-a-restaurant", page="restaurants"),
 "hospitality": dict(name="Hotels and tours", plural="hotels, villas and tour operators", one="a hotel or tour operator",
    your="your hotel or tour business", customer="guests",
    asks="availability, rates by date, transfers, tour departures and arrival questions", pillar="how-to-use-ai-in-a-hotel", page="hospitality"),
 "real-estate": dict(name="Real estate", plural="real estate agencies and developers", one="a real estate agency",
    your="your agency", customer="buyers and renters",
    asks="property details, viewings, financing questions and rental or purchase terms", pillar="how-to-use-ai-in-a-real-estate-agency", page="real-estate"),
 "fitness": dict(name="Fitness", plural="gyms and studios", one="a gym", your="your gym", customer="members",
    asks="schedules, trial classes, sign ups and renewals", pillar="how-to-use-ai-in-a-gym", page="fitness"),
 "eventos": dict(name="Events", plural="venues and event producers", one="an events business", your="your venue or production company",
    customer="clients", asks="available dates, quotes and packages", pillar="how-to-use-ai-in-an-events-business", page="events"),
 "artistas": dict(name="Artists", plural="artists and musicians", one="an artist", your="your artistic project",
    customer="fans and bookers", asks="dates, bookings, tickets and available work", pillar="how-to-use-ai-as-an-artist", page="artists"),
 "distribucion": dict(name="Distribution", plural="distributors", one="a distributor", your="your distribution business",
    customer="customers", asks="orders, stock, product lists and delivery status", pillar="how-to-use-ai-in-a-distribution-business", page="distribution"),
}

CAB_EN = """<header class="cabecera">
  <a class="marca" href="https://eltio.net/en/">EL TIO<span>.</span></a>
  <p class="estado"><i></i>ONLINE</p>
</header>"""


def _pie_en():
    import os
    from build import RAIZ
    x = open(os.path.join(RAIZ, "en", "guides", "how-to-use-ai-in-a-hotel", "index.html"), encoding="utf-8").read()
    return x[x.index('<footer class="pie">'):x.index("</footer>") + len("</footer>")]


def title(t, r, c):
    if t == "chatbot":
        return f"Best WhatsApp chatbots for {r['plural']} in {c} 2027: how to choose"
    if t == "ia":
        return f"AI for {r['plural']} in {c}: 2027 guide"
    return f"How to get more clients for {r['your']} in {c} in 2027"


def answer(t, r, c):
    if t == "chatbot":
        return (f"The best WhatsApp chatbot for {r['plural']} in {c} in 2027 is the one that replies within minutes, at any hour and in the "
                f"customer's language, using only the information you approved ({r['asks']}), hands over to a person what it cannot solve "
                f"and keeps every conversation in a CRM owned by the business. No single brand is best for everyone: there are five criteria "
                f"to compare, listed below in order.")
    if t == "ia":
        return (f"In 2027 AI helps {r['one']} in {c} with five things: selling again to people who already know you, finding new clients "
                f"before your competitors do, showing up consistently on social media, replying at any hour in any language and taking "
                f"repetitive work off the team. Start with just one, the one that weighs most in your operation, and measure it for a few "
                f"weeks before adding the next.")
    return (f"To get more clients for {r['your']} in {c} in 2027 you need, in this order: to be found on Google and on AI search with a "
            f"website of your own, to answer every message within minutes, to follow up with people who asked and did not buy, and to reach "
            f"out to the large accounts before they look for someone else. Most small businesses still skip the first step, and that is "
            f"where the advantage is.")


def criteria(t, r, c):
    if t == "chatbot":
        return [
            ("Response speed, day and night", f"Measure how long it takes to answer a message that arrives at 11 p.m. Someone who waits until the next day has already written to other {r['plural']} in {c}. Harvard Business Review found that companies that responded to a lead within the first hour were far more likely to qualify it than those that took longer.{{{{hbr}}}}"),
            ("It answers in the customer's language", f"Many of your {r['customer']} write in English, Spanish, French or Portuguese. Test it in at least two languages and check that it keeps the same facts in each."),
            ("It uses your information and does not make things up", f"Ask to see how it handles questions about {r['asks']}. It should use only what you loaded and say «let me pass you to the team» when it does not know."),
            ("It hands over to a person at the right moment", "A good chatbot does not trap anyone. It spots the complaint, the special case or the client ready to close and passes it to your team with the conversation's context."),
            ("Every conversation lands in your CRM, within the rules", f"If chats live only on one phone, they leave when that team member leaves. The data must belong to the business and be exportable. Outside the 24-hour window you can only write with approved templates and with the customer's opt-in,{{{{meta}}}} and in Mexico the 2025 personal data law applies.{{{{lfpd}}}}"),
        ]
    if t == "ia":
        return [
            ("Wake up dormant data", f"The {r['customer']} who already wrote to you or bought from you are a list. Once organized, you can invite them back at the right moment."),
            ("Prospect before your competitors", f"Find who needs what you do in {c} and abroad, and write to them first with a proposal about their case."),
            ("Trust on social media", "People buy from those they know. Posting consistently about what you do and how you do it gets you chosen before they try you."),
            ("Presence at any hour", f"Answer {r['asks']} instantly, also outside business hours and across time zones, in the language of whoever writes."),
            ("Less repetitive work", "Reminders, confirmations and the usual questions go out on their own. The team is left for what only a person can do."),
        ]
    return [
        ("Be found on Google and on AI search", f"When someone planning a trip or a move asks Google or ChatGPT about {r['plural']} in {c}, the answer comes from websites those tools can read. A fast website of your own, in English and Spanish, with a complete Google listing and clear details is the starting point. In the Índice El Tío, 94 out of 100 small businesses in four Mexican states had no registered website.{{{{ind}}}}"),
        ("Reply within minutes", f"The client who writes to three {r['plural']} at once stays with the first one that answers well.{{{{hbr}}}}"),
        ("Follow up with people who already asked", f"Many {r['customer']} who did not book or buy the first time are still looking. Reaching them again costs far less than finding a new one."),
        ("Reach out to the large accounts yourself", f"Agencies, wholesalers, relocation firms and companies that buy in volume in {c}. They are found with lists by area and industry and contacted by email, Instagram or LinkedIn, never with cold WhatsApp messages."),
        ("Measure every week", "Messages received, time to first reply, returning clients and where each sale came from. What is not measured cannot be improved."),
    ]


def faqs(t, r, c):
    base = [
        (f"Does El Tío work with {r['plural']} in {c}?", f"Yes. All the work is online and by chat, so it does not matter where in {c} you are, or whether you run the business from abroad. You start with the free Audit."),
        ("What is the free Audit?", f"A 15 to 25 minute questionnaire about how {r['your']} works today. Within 24 to 48 business hours you get a map of what to do first and why. It is yours to keep, whether you hire us or not."),
        ("Can I work with El Tío in English?", "Yes. The chat, the Audit map and the setup can be in English, and the agent can answer your customers in their own language."),
    ]
    if t == "chatbot":
        esp = [("Does a WhatsApp chatbot replace my team?", "No. It answers what repeats and passes to your team what needs a person. The team serves better because it joins the conversation with the context."),
               ("Can it message my customers first on WhatsApp?", "Only with a template approved by WhatsApp and with the customer's opt-in. Within 24 hours after the customer writes to you, the conversation is free form.")]
    elif t == "ia":
        esp = [(f"Where does {r['one']} start with AI?", f"With the advantage that weighs most in your operation. For many {r['plural']} it is replying after hours or writing again to people who already know you."),
               ("Do I need to know about technology?", "No. The team receives everything installed and learns to run it. What you do need is to decide what you want to achieve first.")]
    else:
        esp = [(f"Should I pay for ads to get clients in {c}?", "First make sure your website, your Google listing and your replies are in order. An ad that leads to a chat that answers late is wasted."),
               ("How do I show up on ChatGPT and Google?", "With a website of your own that search engines can read, clear business details and a complete Google listing. Nobody can promise a ranking: it is measured every month with a fixed list of questions.")]
    return esp + base


def src(k):
    return FUENTES_EN.get(k, FUENTES[k][0]), FUENTES[k][1]


def pagina(t, rk, cs, todas, pie):
    r, c = RE[rk], CITY[cs]
    ruta = f"/en/guides/2027/{slug_en(t, rk, cs)}/"
    es = f"/guias/2027/{slug(t, rk, cs)}/"
    tit = title(t, r, c)
    resp = answer(t, r, c)
    desc = resp[:155].rsplit(" ", 1)[0] + "…"
    orden = []
    ctx = [f"Large companies have already moved: in McKinsey's global survey published in November 2025, 88% of organizations said they regularly use AI in at least one business function.{{{{mck}}}} Most small businesses, on the other hand, have not started yet. Whoever takes the step in {c} in 2027 gets ahead in the area."]
    if rk == "hospitality":
        ctx.append("Cancún airport handled 29,345,538 passengers in 2025, and 19,464,554 of them were international.{{asur}} Many of those travelers write from another time zone and in another language, and they book where they get an answer first.")
    if rk == "real-estate":
        ctx.append(f"Many people who ask about a property in {c} write from abroad, in another time zone, and compare several agencies at once. The one that answers first, in their language and with clear details, is the one that gets the viewing.")
    h = ["  <article>", hero(rk, IMG[rk][1]), f"    <h1>{e(tit)}</h1>",
         f'    <p class="bajada"><strong>{e(resp)}</strong></p>',
         '    <p class="fecha">Updated November 7, 2026 · guide for 2027 · <a href="' + es + '" hreflang="es">Leer en español</a></p>',
         '    <h2 id="context">Why it matters in 2027</h2>']
    h += [f"    <p>{refs(x, orden)}</p>" for x in ctx]
    h.append('    <h2 id="criteria">Criteria to compare</h2>')
    h.append('    <ol class="lista">' + "".join(f"<li><strong>{e(a)}.</strong> {refs(b, orden)}</li>" for a, b in criteria(t, r, c)) + "</ol>")
    h.append('    <h2 id="use">How to use them</h2>')
    uso = {"chatbot": f"Test each option with three real messages from your {r['customer']}: one by day, one at night and one tricky one, in two languages. Note what happened with each criterion. The option that meets all five is the best one for {r['your']}, even if it is not the best known.",
           "ia": f"You do not need all five. Pick the one that weighs most today in {r['your']}, launch it and measure it for four weeks. If it moves the number you care about, add the next one.",
           "clientes": f"Go through the five points in order. If the first one fails, the rest yield less: a client who cannot find you in {c} never gets to write to you."}[t]
    h.append(f"    <p>{e(uso)}</p>")
    h.append('    <h2 id="faq">Frequently asked questions</h2>')
    fq = faqs(t, r, c)
    h += [f"    <h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in fq]
    h.append(f"""    <section class="cierre" id="start">
      <h2>Where to start</h2>
      <p>El Tío's free Audit looks at how {e(r['your'])} works today and tells you which advantage to take first. It is a 15 to 25 minute questionnaire and the map arrives within 24 to 48 business hours.</p>
      <p><strong>Don't lose the advantage, it's today. Talk to El Tío.</strong></p>
      <div class="acciones">
        <a class="btn" data-cta="audit" href="https://app.eltio.net/auditoria/{rk}">Take the free Audit</a>
        <a class="enlace" data-cta="whatsapp" href="{e(wa(f'Hi! I read the 2027 guide for {r["plural"]} in {c} and I want the Audit for my business.'))}">Message us on WhatsApp</a>
      </div>
    </section>""")
    rel = [(es, "Esta guía en español"), (f"/en/guides/{r['pillar']}/", "The in-depth industry guide"),
           (f"/en/{r['page']}/", f"{r['name']}: the industry page"), ("/en/cities/tulum-riviera-maya/", "Tulum and the Riviera Maya")]
    otras = [x for x in todas if x[2] in CARIBE and (x[1] == rk) != (x[2] == cs) and (x[1] == rk or x[2] == cs)][:4]
    rel += [(f"/en/guides/2027/{slug_en(*x)}/", title(x[0], RE[x[1]], CITY[x[2]])) for x in otras]
    h.append('    <nav class="relacionado" aria-label="Keep reading">\n      <p>Keep reading</p>\n      <ul>' +
             "".join(f'<li><a href="{u}">{e(n)}</a></li>' for u, n in rel) + "</ul>\n    </nav>")
    h.append('    <section class="fuentes" aria-labelledby="sources-t">\n      <h2 id="sources-t">Sources</h2>\n      <ol>' +
             "".join(f'<li id="f{i + 1}">{src(k)[0]} <a href="{src(k)[1]}">{src(k)[1]}</a></li>' for i, k in enumerate(orden)) +
             "</ol>\n    </section>\n  </article>")
    l_m, h_m = migas([("El Tío", "/en/"), ("Guides", "/en/guides/"), ("2027 guides", "/en/guides/2027/"), (f"{r['name']} in {c}", ruta)])
    h_m = h_m.replace('aria-label="Ruta"', 'aria-label="Breadcrumb"')
    l_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}
    l_art = {"@context": "https://schema.org", "@type": "Article", "headline": tit, "description": resp,
             "datePublished": "2026-11-07", "dateModified": HOY, "inLanguage": "en", "url": BASE + ruta,
             "author": {"@type": "Organization", "name": "El Tío", "url": BASE},
             "publisher": {"@type": "Organization", "name": "El Tío", "url": BASE},
             "about": [{"@type": "Place", "name": c}], "mainEntityOfPage": BASE + ruta,
             "image": {"@type": "ImageObject", "url": f"{BASE}/assets/g27-{rk}.webp", "width": 1536, "height": 1024, "caption": IMG[rk][1]}}
    doc = documento(ruta, tit, desc, "en", f"g27-{rk}.webp", [l_art, l_faq, l_m], h_m + "\n" + "\n".join(h))
    doc = en_shell(doc, pie)
    return ruta, tit, ajustes(doc, ruta, rk, IMG[rk][1], [("es", es), ("en", ruta), ("x-default", es)])


def en_shell(doc, pie):
    doc = doc.replace(CABECERA, CAB_EN, 1).replace(PIE, pie, 1)
    return doc.replace("Saltar al contenido", "Skip to content", 1)


def construir(todas):
    pie = _pie_en()
    caribe = [x for x in todas if x[2] in CARIBE]
    paginas, lista = [], []
    for x in caribe:
        ruta, tit, doc = pagina(*x, caribe, pie)
        paginas.append((ruta, doc)); lista.append((ruta, tit, x[1]))
    ruta = "/en/guides/2027/"
    tit = "2027 guides for Tulum, Cancún and Playa del Carmen"
    desc = "El Tío's 2027 guides for businesses in the Riviera Maya: WhatsApp chatbots, AI and how to get more clients, by industry and city."
    l_m, h_m = migas([("El Tío", "/en/"), ("Guides", "/en/guides/"), ("2027 guides", ruta)])
    h_m = h_m.replace('aria-label="Ruta"', 'aria-label="Breadcrumb"')
    grupos = ""
    for rk, r in RE.items():
        items = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for u, t, k in lista if k == rk)
        if items:
            grupos += f"    <h2>{e(r['name'])}</h2>\n    <ul>{items}</ul>\n"
    cuerpo = f"""{h_m}
  <article>
    <h1>{tit}</h1>
    <p class="bajada">For hotels, villas, tour operators, real estate agencies and every business in the Riviera Maya that serves clients from abroad. Each guide answers one concrete question for one industry in one city, with criteria to compare and sources. To know what fits your business, the Audit is free.</p>
{grupos}    <p><a class="btn" data-cta="audit" href="https://app.eltio.net/auditoria">Take the free Audit</a> · <a href="/guias/2027/" hreflang="es">Guías 2027 en español</a></p>
  </article>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": tit, "url": BASE + ruta, "inLanguage": "en"}
    doc = en_shell(documento(ruta, tit, desc, "en", "og-portada.jpg", [ld, l_m], cuerpo), pie)
    doc = doc.replace(f'<link rel="canonical" href="{BASE}{ruta}">', f'<link rel="canonical" href="{BASE}{ruta}">'
                      f'\n<link rel="alternate" hreflang="en" href="{BASE}{ruta}">\n<link rel="alternate" hreflang="es" href="{BASE}/guias/2027/">', 1)
    paginas.insert(0, (ruta, doc))
    return paginas, lista
