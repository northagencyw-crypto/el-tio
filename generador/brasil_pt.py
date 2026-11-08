"""Brasil pt-BR: páginas de cidade (São Paulo, Rio de Janeiro) e /pt/vantagem/.
Usa cabeçalho e rodapé de pt/cidades/monterrey como molde. Rodar: python generador/brasil_pt.py"""
import os, re, json, urllib.parse
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
molde = open(os.path.join(RAIZ, "pt/cidades/monterrey/index.html"), encoding="utf-8").read()
pre_main, resto = molde.split('<main id="contenido">', 1)
rodape = resto.split("</main>", 1)[1]
cab = pre_main[pre_main.index("<body>"):]
cab = re.sub(r'\s*<details class="idioma">.*?</details>', "", cab, flags=re.S)
cab = cab.replace('href="#audit" data-cta="audit">Audit gratuito', 'href="/pt/vantagem/" data-cta="audit">Teste grátis')
WA = "https://wa.me/525568976898?text="
def wa(t): return WA + urllib.parse.quote(t)
ICON = molde[molde.index('<link rel="icon"'):molde.index('<link rel="stylesheet" href="/paginas.css">')]

def head(titulo, desc, url, ld, extra=""):
    lds = "".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>\n' for x in ld)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · El Tío</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-BR" href="{url}">
<meta name="theme-color" content="#04070B">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="El Tío">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://eltio.net/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
{ICON}<link rel="stylesheet" href="/paginas.css">
{lds}<script src="/medicion.js" defer></script>
{extra}</head>
"""

def migas(*itens):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": "https://eltio.net" + u} for i, (n, u) in enumerate(itens)]}
    html = " / ".join(f'<a href="{u}">{n}</a>' for n, u in itens[:-1]) + " / " + itens[-1][0]
    return ld, f'<nav class="migas franja" aria-label="Caminho" style="padding-bottom:0">{html}</nav>'

AUDIT = [("gastronomia", "Gastronomia", "Restaurantes, bares, cafeterias e padarias"), ("hospitality", "Hotelaria", "Hotéis, pousadas, aluguel por temporada e passeios"),
         ("real-estate", "Imobiliário", "Imobiliárias, incorporadoras e corretores"), ("fitness", "Fitness", "Academias, boxes e estúdios"),
         ("eventos", "Eventos", "Produtoras, promotores e casas de show"), ("artistas", "Artistas", "Artistas, DJs e empresários"), ("distribucion", "Distribuição", "Atacadistas, distribuidoras e importadores")]
RUB_PT = {"gastronomia": "gastronomia", "hospitality": "hotelaria", "real-estate": "imobiliario", "fitness": "fitness", "eventos": "eventos", "artistas": "artistas", "distribucion": "distribuicao"}

FAQ = [
    ("Vocês atendem empresas no Brasil?", "Sim. Todo o trabalho é online: o teste e o Audit são feitos pela internet, as dúvidas são resolvidas por chat e a instalação é testada de ponta a ponta a distância. Não precisamos ir até a sua empresa."),
    ("Funciona em português?", "Sim. O site, o agente de WhatsApp e Instagram e as mensagens para os seus clientes ficam em português. O questionário do Audit por enquanto está em espanhol, por isso o primeiro passo em português é o teste de 5 perguntas."),
    ("Quanto custa?", "O teste e o Audit são gratuitos. Depois existem duas formas de começar: Site e posicionamento (a partir de USD 399 de implantação e USD 49 por mês) ou Instagram que vende (USD 399 de implantação e USD 149 por mês). Os extras, como o chatbot ou a prospecção, são acrescentados quando você quiser, e o plano completo custa USD 1.000 de implantação e USD 300 por mês. Tudo é mês a mês, sem contrato longo."),
]

CIDADES = [
    dict(slug="sao-paulo", nome="São Paulo", no="em São Paulo", estado="São Paulo",
         titulo="IA para empresas em São Paulo: a vantagem é de quem começa hoje",
         desc="Agentes de IA no WhatsApp e no Instagram, site com posicionamento no Google e nos assistentes de IA, CRM e automações para negócios de São Paulo. Faça o teste grátis de 5 perguntas.",
         h1="Em São Paulo, quem responde primeiro leva o cliente",
         bajada="A IA já é vantagem no seu setor, e a janela é hoje. Enquanto a maioria dos negócios ainda responde à mão, quem automatiza atende na hora, aparece quando alguém pergunta ao ChatGPT e não perde o cliente para o concorrente da mesma rua.",
         contexto=["São Paulo é a maior cidade do Brasil. Em bairros como Pinheiros, Vila Madalena, Moema, Itaim Bibi e a região da Faria Lima, um mesmo quarteirão tem vários restaurantes, academias, imobiliárias e prestadores de serviço disputando o mesmo cliente.",
                   "Nesse mercado, o cliente pergunta para vários lugares ao mesmo tempo pelo WhatsApp e fecha com quem responde primeiro e melhor. Quando a resposta depende de alguém estar livre, ela chega tarde.",
                   "Por isso, em São Paulo, El Tío começa pela resposta: um agente que atende no WhatsApp e no Instagram em segundos, a qualquer hora, e um site que aparece no Google e nos assistentes de IA quando alguém procura o que você faz."],
         setores=["gastronomia", "fitness", "real-estate", "eventos", "distribucion"]),
    dict(slug="rio-de-janeiro", nome="Rio de Janeiro", no="no Rio de Janeiro", estado="Rio de Janeiro",
         titulo="IA para empresas no Rio de Janeiro: a vantagem é de quem começa hoje",
         desc="Agentes de IA que respondem em português, inglês e espanhol, reservas diretas, site com posicionamento no Google e nos assistentes de IA e CRM para negócios do Rio de Janeiro. Faça o teste grátis de 5 perguntas.",
         h1="No Rio, o turista reserva com quem responde no idioma dele",
         bajada="A IA já é vantagem no seu setor, e a janela é hoje. Um agente que responde em português, inglês e espanhol a qualquer hora transforma a mensagem das 2 da manhã em reserva, em vez de deixar para o concorrente que respondeu antes.",
         contexto=["O Rio de Janeiro recebe turistas do Brasil e do exterior o ano inteiro. Em Copacabana, Ipanema, Leblon, Botafogo, Santa Teresa e na Barra da Tijuca, hotéis, pousadas, passeios, restaurantes e produtoras de eventos vivem de mensagens que chegam em vários idiomas e em qualquer horário.",
                   "Quando essas mensagens esperam até o dia seguinte, a reserva vai para quem respondeu primeiro ou para a plataforma que cobra comissão.",
                   "Por isso, no Rio, El Tío começa pelo atendimento e pelas reservas: um agente de WhatsApp e Instagram que responde em português, inglês e espanhol, reservas que passam para o seu canal direto e um CRM com o histórico de cada cliente."],
         setores=["hospitality", "gastronomia", "eventos", "real-estate", "fitness"]),
]
TXT_SETOR = {
    "gastronomia": ("Gastronomia", "Restaurantes, bares, cafeterias e padarias", "Reservas e pedidos pelo WhatsApp e pelo Instagram, confirmação na véspera e avaliações no Google depois de cada visita."),
    "hospitality": ("Hotelaria", "Hotéis, pousadas, aluguel por temporada e passeios", "Resposta em vários idiomas, reserva direta sem comissão e o histórico de cada hóspede."),
    "real-estate": ("Imobiliário", "Imobiliárias, incorporadoras e corretores", "Resposta imediata a cada contato, visita agendada e a base de compradores organizada por região e orçamento."),
    "fitness": ("Fitness", "Academias, boxes e estúdios", "Aula experimental agendada sozinha, follow-up de quem não se matriculou e aviso antes de um aluno cancelar."),
    "eventos": ("Eventos", "Produtoras, promotores e casas de show", "Atendimento de cada data e a lista de compradores para a próxima."),
    "distribucion": ("Distribuição", "Atacadistas, distribuidoras e importadores", "O pedido chega pelo WhatsApp e sai como orçamento pronto para revisar, com follow-up até ser aprovado."),
}


def bloco_audit(c):
    lis = "\n".join(f'        <li><a class="fuerte" data-cta="audit" href="https://app.eltio.net/auditoria/{k}">{n}<span>{d}</span></a></li>' for k, n, d in AUDIT)
    return f"""  <section class="franja">
    <div class="audit" id="audit">
      <p class="ojo">Primeiro passo</p>
      <h2>Descubra a vantagem que a sua empresa {c['no']} está deixando passar</h2>
      <p>O teste tem 5 perguntas, leva um minuto e está em português. Mostra a sua pontuação e as 3 vantagens de IA que convém colocar em prática primeiro.</p>
      <p><a class="btn" data-cta="audit" href="/pt/vantagem/">Fazer o teste grátis</a></p>
      <p>Quer o mapa completo, revisado por uma pessoa? O Audit gratuito é um questionário guiado de 15 a 25 minutos, e em 24 a 48 horas úteis você recebe o que vale a pena fazer primeiro. O mapa é seu, contratando ou não.</p>
      <ul class="rubros">
{lis}
      </ul>
      <p class="nota nota-idioma">O questionário do Audit por enquanto está em espanhol. Se preferir em português, escreva para a gente pelo <a data-cta="whatsapp" href="{wa('Olá! Tenho um negócio ' + c['no'] + ' e quero o Audit gratuito em português.')}">WhatsApp</a> ou para hola@eltio.net.</p>
    </div>
  </section>
"""


def oferta(nome, impl, mes, minimo=False):
    return {"@type": "Offer", "name": nome, "priceCurrency": "USD", "url": "https://eltio.net/pt/planos-e-precos/", "priceSpecification": [
        {"@type": "UnitPriceSpecification", "name": "Implantação", ("minPrice" if minimo else "price"): impl, "priceCurrency": "USD"},
        {"@type": "UnitPriceSpecification", "name": "Mensal", "price": mes, "priceCurrency": "USD", "unitCode": "MON", "unitText": "mês"}]}


def pagina_cidade(c):
    url = f"https://eltio.net/pt/cidades/{c['slug']}/"
    ld_m, nav = migas(("El Tío", "/pt/"), ("Cidades", "/pt/cidades/"), (c["nome"], f"/pt/cidades/{c['slug']}/"))
    serv = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": f"El Tío · IA para empresas {c['no']}", "description": c["desc"], "url": url, "email": "hola@eltio.net",
            "areaServed": [{"@type": "City", "name": c["nome"], "containedInPlace": {"@type": "State", "name": c["estado"]}}],
            "parentOrganization": {"@type": "Organization", "name": "El Tío", "url": "https://eltio.net/pt/"},
            "makesOffer": [{"@type": "Offer", "name": "Audit", "price": 0, "priceCurrency": "USD", "url": "https://eltio.net/pt/planos-e-precos/"},
                           oferta("Site e posicionamento", 399, 49, True), oferta("Instagram que vende", 399, 149), oferta("Plano completo", 1000, 300)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "pt-BR", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    cards = "\n".join(f'      <a class="tarjeta" href="/pt/negocios/{c["slug"]}/{RUB_PT[k]}/"><span class="tag">{TXT_SETOR[k][0]}</span><h3>{TXT_SETOR[k][1]}</h3><p>{TXT_SETOR[k][2]}</p></a>' for k in c["setores"])
    ctx = "\n".join(f"    <p>{p}</p>" for p in c["contexto"])
    faqs = "\n".join(f"      <details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in FAQ)
    corpo = f"""<main id="contenido">
  {nav}
  <section class="franja" style="padding-top:8px">
    <p class="ojo">{c['estado']} · Brasil</p>
    <h1>{c['h1']}</h1>
    <p class="bajada">{c['bajada']}</p>
    <div class="acciones">
      <a class="btn" data-cta="audit" href="/pt/vantagem/">Fazer o teste grátis</a>
      <a class="enlace" data-cta="whatsapp" href="{wa('Olá! Tenho um negócio ' + c['no'] + ' e quero falar com o El Tío.')}">Chamar no WhatsApp</a>
    </div>
  </section>
  <section class="franja">
    <h2>Por que a janela é hoje</h2>
{ctx}
    <p>A IA já resolve sozinha boa parte do que hoje toma o seu dia: responder, agendar, pedir avaliação, fazer follow-up. Quem começa agora aprende antes e chega primeiro. Quem espera vai competir com negócios que já fazem isso.</p>
  </section>
  <section class="franja">
    <h2>Setores {c['no']}</h2>
    <div class="grilla">
{cards}
    </div>
    <p style="margin-top:20px"><a href="/pt/negocios/{c['slug']}/">Ver todos os setores {c['no']}</a></p>
  </section>
  <section class="franja">
    <h2>O que El Tío instala</h2>
    <div class="grilla">
      <a class="tarjeta" href="/pt/servicos/agente-whatsapp-instagram/"><span class="tag">Atendimento</span><h3>Agente de WhatsApp e Instagram</h3><p>Responde em segundos, agenda e guarda cada contato.</p></a>
      <a class="tarjeta" href="/pt/sites/"><span class="tag">Site</span><h3>Site com domínio próprio</h3><p>Em 8 idiomas, pronto para o Google, o ChatGPT, o Perplexity e o Gemini.</p></a>
      <a class="tarjeta" href="/pt/servicos/crm-e-acompanhamento/"><span class="tag">Operação</span><h3>CRM e follow-up</h3><p>Contatos em um só lugar, lembretes e cobrança.</p></a>
      <a class="tarjeta" href="/pt/servicos/automacoes-e-relatorios/"><span class="tag">Operação</span><h3>Automações e relatórios</h3><p>Tarefas repetitivas em fluxos e o relatório de segunda-feira.</p></a>
    </div>
    <p style="margin-top:20px">Para começar: Site e posicionamento a partir de USD 399 e USD 49 por mês, ou Instagram que vende por USD 399 e USD 149 por mês. <a href="/pt/planos-e-precos/">Ver pacotes e preços</a></p>
  </section>
  <section class="franja" id="preguntas">
    <h2>Perguntas frequentes</h2>
    <div class="preguntas">
{faqs}
    </div>
  </section>
{bloco_audit(c)}</main>"""
    return head(c["titulo"], c["desc"], url, [serv, faq, ld_m]) + cab + corpo + rodape


def pagina_vantagem():
    src = open(os.path.join(RAIZ, "ventaja/index.html"), encoding="utf-8").read()
    style = src[src.index("<style>"):src.index("</style>") + 8] + "\n"
    script = src[src.index("<script>\n(function"):src.index("</script>\n</main>") + 9]
    T = [("'Un sitio que vende por ti', 'Un sitio propio, rápido y en varios idiomas, que aparece en Google y en las respuestas de ChatGPT cuando alguien busca lo que haces.'",
          "'Um site que vende por você', 'Um site próprio, rápido e em vários idiomas, que aparece no Google e nas respostas do ChatGPT quando alguém procura o que você faz.'"),
         ("'Contestar al instante, a cualquier hora', 'Un asistente en WhatsApp e Instagram que responde en segundos, resuelve las preguntas de siempre y te pasa solo las conversaciones que necesitan a una persona.'",
          "'Responder na hora, a qualquer hora', 'Um assistente no WhatsApp e no Instagram que responde em segundos, resolve as perguntas de sempre e passa para você só as conversas que precisam de uma pessoa.'"),
         ("'Reseñas que llegan solas', 'Un mensaje automático después de cada visita o venta que pide la reseña en Google y te avisa si alguien quedó molesto antes de que la publique.'",
          "'Avaliações que chegam sozinhas', 'Uma mensagem automática depois de cada visita ou venda que pede a avaliação no Google e avisa você se alguém ficou insatisfeito antes que publique.'"),
         ("'Redes con constancia', 'Un calendario de publicaciones hecho con lo que ya pasa en tu negocio, para que tus redes no dependan de que te sobre tiempo.'",
          "'Redes com constância', 'Um calendário de publicações feito com o que já acontece no seu negócio, para que as suas redes não dependam de sobrar tempo.'"),
         ("'Reservas y pedidos sin escribir', 'Que el cliente reserve o pida solo, con confirmación y recordatorio automáticos, y que todo quede en un mismo lugar.'",
          "'Reservas e pedidos sem precisar escrever', 'O cliente reserva ou pede sozinho, com confirmação e lembrete automáticos, e tudo fica em um só lugar.'"),
         ("'Ya aprovechas buena parte. Lo que queda es afinar.'", "'Você já aproveita boa parte. O que falta é ajustar.'"),
         ("'Vas a medias: hay ventajas claras que todavía haces a mano o no haces.'", "'Você está no meio do caminho: há vantagens claras que ainda faz à mão ou não faz.'"),
         ("'Estás dejando pasar casi todo lo que hoy se puede resolver solo. Es el mejor momento para empezar.'", "'Você está deixando passar quase tudo o que hoje já se resolve sozinho. A janela é agora.'"),
         ("'Hola, El Tío. Hice la calculadora de ventaja.\\nRubro: '", "'Olá, El Tío. Fiz o teste de vantagem em português.\\nSetor: '"),
         ("'\\nPuntos: '", "'\\nPontos: '"),
         ("'\\nMi contacto: '", "'\\nMeu contato: '"), ("'\\nQuiero el detalle.'", "'\\nQuero o detalhe.'"),
         ("content_name: 'ventaja'", "content_name: 'vantagem-pt'"), ("{ rubro: rubro, puntos: tot }", "{ rubro: rubro, puntos: tot, idioma: 'pt' }")]
    for a, b in T:
        assert a in script, a
        script = script.replace(a, b)
    url = "https://eltio.net/pt/vantagem/"
    tit = "Descubra a vantagem que você está deixando passar"
    desc = "Teste grátis do El Tío: escolha o seu setor, responda 5 perguntas e descubra a sua pontuação e as 3 vantagens de IA que convém colocar em prática primeiro."
    ld_m, nav = migas(("El Tío", "/pt/"), ("Teste de vantagem", "/pt/vantagem/"))
    wp = {"@context": "https://schema.org", "@type": "WebPage", "name": tit, "url": url, "inLanguage": "pt-BR", "description": desc}

    def q(n, nome, ops):
        return f'      <fieldset class="preg"><legend>{n}</legend>\n' + "\n".join(
            f'        <label><input type="radio" name="{nome}" value="{v}"{" required" if i == 0 else ""}> {t}</label>' for i, (v, t) in enumerate(ops)) + "</fieldset>"
    corpo = f"""<main id="contenido">
  {nav}
  <section class="franja" style="padding-top:8px">
    <p class="ojo">Ferramenta grátis</p>
    <h1>{tit}</h1>
    <p class="bajada">Cinco perguntas, um minuto. Mostra quanto você aproveita hoje do que a IA já resolve em negócios do seu setor e por onde convém começar. A IA já é vantagem, e a janela é hoje.</p>
  </section>
  <section class="franja">
    <form class="form-el" id="calc" style="max-width:680px">
      <label>Seu setor<select name="rubro" required>
        <option value="">Escolha o seu setor</option>
        <option value="gastronomia">Gastronomia</option><option value="hospitality">Hotelaria</option><option value="real-estate">Imobiliário</option><option value="fitness">Fitness</option><option value="eventos">Eventos</option><option value="artistas">Artistas</option><option value="distribucion">Distribuição</option>
      </select></label>
{q("1. O seu negócio tem site próprio?", "web", [(20, "Sim, e mantenho atualizado"), (10, "Sim, mas está velho ou quase não uso"), (0, "Não")])}
{q("2. Como você responde no WhatsApp?", "wa", [(20, "Um assistente responde na hora, a qualquer hora"), (10, "Uma pessoa, em horário comercial"), (0, "Quando alguém pode, às vezes horas depois")])}
{q("3. Você pede avaliações no Google aos seus clientes?", "resenas", [(20, "Sim, de forma automática depois de cada visita ou venda"), (10, "Às vezes, à mão"), (0, "Não")])}
{q("4. Com que frequência você publica nas redes?", "redes", [(20, "Várias vezes por semana"), (10, "Uma vez por semana ou menos"), (0, "Quase nunca")])}
{q("5. Os seus clientes conseguem reservar ou pedir sozinhos?", "reserva", [(20, "Sim, online e com confirmação automática"), (10, "Só mandando mensagem"), (0, "Não temos isso organizado")])}
      <button type="submit">Ver meu resultado</button>
    </form>
  </section>
  <section class="franja oculto" id="resultado" aria-live="polite">
    <p class="ojo">Seu resultado</p>
    <p class="marcador"><span id="puntos">0</span><small style="font-size:.35em"> / 100</small></p>
    <p id="lectura"></p>
    <h2>Suas 3 vantagens prioritárias</h2>
    <ol id="ventajas"></ol>
    <div id="candado">
      <h3>Receba o detalhe de cada vantagem</h3>
      <p>O que muda no seu dia e o que é preciso para colocar em prática. Deixe o seu WhatsApp ou o seu e-mail e a gente manda.</p>
      <form class="form-el" id="pedir">
        <label>Seu WhatsApp ou seu e-mail<input name="dato" required placeholder="+55 11 90000 0000 ou voce@negocio.com.br"></label>
        <button type="submit">Quero o detalhe</button>
      </form>
    </div>
    <div id="detalle" class="oculto"><ol id="det"></ol></div>
    <p style="margin-top:22px">Quer o mapa completo, revisado por uma pessoa? <a class="boton" id="ir-audit" data-cta="audit" href="https://app.eltio.net/auditoria/gastronomia">Fazer o Audit gratuito</a></p>
    <p class="nota">O questionário do Audit por enquanto está em espanhol. Se preferir em português, responda pelo WhatsApp que seguimos por lá.</p>
  </section>
  <section class="franja">
    <h2>Como é calculado</h2>
    <p>É uma escala própria do El Tío, não uma estatística de mercado. Cada pergunta vale de 0 a 20 pontos: 20 se você já resolve isso com ferramentas que trabalham sozinhas, 10 se faz pela metade ou à mão e 0 se não faz. A soma vai de 0 a 100.</p>
    <p>As suas três vantagens prioritárias são as perguntas em que você fez menos pontos. Se houver empate, vale a ordem que usamos para cada setor: em gastronomia vem primeiro o WhatsApp, em hotelaria as reservas e em artistas as redes, por exemplo.</p>
    <p>A página não guarda as suas respostas. Só chega até nós o que você decidir mandar.</p>
    <p>Veja também: <a href="/pt/cidades/sao-paulo/">El Tío em São Paulo</a> · <a href="/pt/cidades/rio-de-janeiro/">El Tío no Rio de Janeiro</a> · <a href="/pt/planos-e-precos/">Pacotes e preços</a></p>
  </section>
{script}
</main>"""
    return head(tit, desc, url, [wp, ld_m], style) + cab + corpo + rodape


def escrever(rota, d):
    for bad in ("—", "ligação", "ligando", "chamada"):
        assert bad not in d, (rota, bad)
    p = os.path.join(RAIZ, rota)
    os.makedirs(p, exist_ok=True)
    open(os.path.join(p, "index.html"), "w", encoding="utf-8", newline="\n").write(d)
    print("ok", rota)


if __name__ == "__main__":
    for c in CIDADES:
        escrever(f"pt/cidades/{c['slug']}", pagina_cidade(c))
    escrever("pt/vantagem", pagina_vantagem())
