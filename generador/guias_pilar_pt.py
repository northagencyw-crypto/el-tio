"""Versão em português do Brasil dos guias pilar. Ver guias_pilar.py.
Regras: só dados com fonte, exemplos marcados, sem preços, sem ligações, sem travessões."""

FUENTES_PT = {
 "mck": "McKinsey &amp; Company, «The State of AI in 2025», pesquisa global publicada em novembro de 2025: 88% das organizações usam IA regularmente em pelo menos uma função do negócio.",
 "ind": "El Tío, «Índice El Tío», edição 1, novembro de 2026: 83.714 empresas de até 50 pessoas em quatro estados do México, com base no Diretório Estatístico Nacional de Unidades Econômicas (DENUE) do INEGI.",
 "hbr": "James B. Oldroyd, Kristina McElheran e David Elkington, «The Short Life of Online Sales Leads», Harvard Business Review, março de 2011.",
 "asur": "ASUR, «ASUR Announces Total Passenger Traffic for December 2025», comunicado de 6 de janeiro de 2026 com o tráfego de janeiro a dezembro de 2025 do aeroporto de Cancún, reproduzido no Stock Titan.",
 "della": "Stefano DellaVigna e Ulrike Malmendier, «Paying Not to Go to the Gym», American Economic Review, vol. 96, n. 3, junho de 2006, p. 694 a 719.",
 "meta": "Meta, «Pricing on the WhatsApp Business Platform», documentação para desenvolvedores: janela de atendimento de 24 horas, mensagens com e sem modelo e permissão do usuário.",
 "wapol": "WhatsApp, «Política de mensagens do WhatsApp Business», atualizada em 23 de setembro de 2026.",
 "lgpd": "Lei n. 13.709, de 14 de agosto de 2018, Lei Geral de Proteção de Dados Pessoais (LGPD), Diário Oficial da União. Texto compilado no Planalto.",
 "lfpd": "Lei Federal de Proteção de Dados Pessoais em Posse de Particulares do México, Diario Oficial de la Federación, 20 de março de 2025. Texto vigente na Câmara dos Deputados.",
}

CIDADE = {"sao-paulo": "São Paulo", "rio-de-janeiro": "Rio de Janeiro", "belo-horizonte": "Belo Horizonte", "curitiba": "Curitiba",
          "florianopolis": "Florianópolis", "salvador": "Salvador", "natal": "Natal", "brasilia": "Brasília",
          "porto-alegre": "Porto Alegre", "campinas": "Campinas", "goiania": "Goiânia", "recife": "Recife",
          "ribeirao-preto": "Ribeirão Preto"}


def rel_pt(setor, nome, plural, es_slug, es_titulo, guias, cidades, rubro):
    r = [f'<li><a href="/pt/{setor}/">{nome}</a>: a página do setor</li>',
         f'<li><a href="/guias/{es_slug}/">{es_titulo}</a>: este guia em espanhol</li>']
    r += [f'<li><a href="{u}">{t}</a></li>' for u, t in guias]
    r += [f'<li><a href="/pt/negocios/{c}/{setor}/">{plural} em {CIDADE[c]}</a></li>' for c in cidades]
    r += ['<li><a href="/pt/negocios/">Cidades e setores no Brasil</a></li>',
          f'<li><a data-cta="audit" href="https://app.eltio.net/auditoria/{rubro}">Audit gratuito da sua empresa</a></li>']
    return r


def hoy(rubro_txt, extra):
    return {"id": "hoy", "h2": "Por que a vantagem é hoje", "bloques": [
        "As grandes empresas já se mexeram. Na pesquisa global da McKinsey publicada em novembro de 2025, 88% das organizações disseram usar inteligência artificial regularmente em pelo menos uma função do negócio.{{mck}}",
        f"Já as pequenas empresas, em sua maioria, ainda não começaram. No Índice El Tío contamos 83.714 empresas de até 50 pessoas em quatro estados do México com o diretório do INEGI, e 94 de cada 100 não têm um site registrado.{{{{ind}}}} É um retrato do México, mas a lógica vale para qualquer mercado: se muitos {rubro_txt} ainda não têm o básico, quem soma IA ao jeito de trabalhar hoje sai na frente na sua região.",
        extra,
        "Essa distância é a janela. Hoje basta dar um passo. Quando a maior parte da concorrência tiver começado, você vai precisar dar dez para chegar ao mesmo lugar. As cinco vantagens a seguir são as que mais se repetem no seu setor, do que você já tem ao que ainda falta.",
    ]}


def nohace(txt):
    return {"id": "no-hace", "h2": "O que a IA não faz por você", "bloques": [
        "Vale deixar isso claro desde o início, porque evita expectativas que depois decepcionam.",
        txt,
        "Ela também não substitui a sua equipe. O que ela faz é tirar das mãos dela o trabalho que se repete e avisar a tempo o que precisa de uma pessoa. As empresas que mais aproveitam a IA decidem primeiro o que querem alcançar e só depois o que automatizar, não o contrário.",
        "E nada disso se instala de um dia para o outro. Você começa por uma vantagem, mede por algumas semanas e soma a próxima. O importante é dar o primeiro passo enquanto a maioria ainda não deu.",
    ]}


def cuidar(extra, quem="clientes"):
    return {"id": "cuidar", "h2": "O que merece cuidado", "bloques": [
        "A IA trabalha com os seus clientes, e as regras são as mesmas que valem para a sua equipe.",
        {"lista": [
            "<strong>Permissão para escrever primeiro.</strong> Se o cliente manda mensagem, você tem 24 horas para responder com mensagens livres. Para escrever primeiro pelo WhatsApp, é preciso um modelo de mensagem aprovado e que a pessoa tenha aceitado receber as suas mensagens.{{meta}}",
            "<strong>Respeitar quem diz não.</strong> A política do WhatsApp Business exige parar de escrever para quem pede, e mandar mensagem fria para uma lista comprada coloca o seu número em risco.{{wapol}}",
            f"<strong>Dados pessoais.</strong> Os nomes, telefones e históricos dos seus {quem} são protegidos por lei. No Brasil vale a LGPD, a Lei 13.709/2018, que pede uma base legal e transparência sobre o que você guarda e para quê.{{{{lgpd}}}} Se você também atende no México, vale a lei mexicana de 2025, com regras parecidas para o aviso de privacidade.{{{{lfpd}}}}",
            "<strong>Dizer que é um assistente.</strong> Quem escreve sabe que está falando com um assistente de IA e que uma pessoa pode assumir a conversa quando for preciso.",
            extra,
        ]},
    ]}


def medir(items):
    return {"id": "medir", "h2": "Como saber se funciona", "bloques": ["Cinco números, toda semana:", {"ol": items}]}


GUIAS_PT = [
# ---------------------------------------------------------------- GASTRONOMIA
{
 "es": "como-usar-ia-en-un-restaurante", "slug": "como-usar-ia-em-um-restaurante", "rubro": "gastronomia", "rubro_nombre": "Gastronomia", "setor": "gastronomia",
 "wa": "restaurantes", "about": "Inteligência artificial para restaurantes",
 "title": "Como usar IA em um restaurante em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA em um restaurante em 2026: 5 vantagens que a sua concorrência já aproveita",
 "desc": "As 5 vantagens da inteligência artificial para restaurantes, bares e cafeterias: clientes que voltam, eventos de empresa, redes sociais, resposta em pleno serviço e menos trabalho repetido.",
 "bajada": "Um restaurante já tem o que mais vale para a IA: centenas de clientes que mandaram mensagem, reservaram ou pediram delivery. Este guia explica as cinco vantagens que hoje separam os restaurantes que se mexem dos que esperam, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "gas-ent-telefono-noche", "wh": (1024, 1536), "alt": "Telefone aceso no balcão da recepção com o restaurante já fechado"},
 "rel": rel_pt("gastronomia", "Gastronomia", "Restaurantes e cafeterias", "como-usar-ia-en-un-restaurante", "Cómo usar IA en un restaurante en 2026",
               [("/pt/guias/chatbot-whatsapp-restaurantes-cidade-do-mexico/", "Chatbot de WhatsApp para restaurantes na Cidade do México")],
               ["sao-paulo", "rio-de-janeiro", "belo-horizonte", "curitiba"], "gastronomia"),
 "secciones": [
  hoy("restaurantes, bares e cafeterias",
      "Em um restaurante a diferença aparece rápido. O cliente que pergunta por uma mesa às nove da noite reserva onde respondem primeiro, e o grupo que procura onde comemorar escolhe o lugar que vê sempre nas redes."),
  {"id": "datos", "h2": "1. Os clientes que já mandaram mensagem voltam", "bloques": [
    "Cada reserva, cada pedido de delivery e cada pergunta pelo WhatsApp deixa um nome, uma data e o que aquela pessoa pediu. Na maioria dos restaurantes essa informação fica parada no celular do gerente. Organizada, é a lista de clientes mais valiosa que você tem, porque são pessoas que já conhecem a casa.",
    "A vantagem está em convidá-las a voltar no momento certo: o aniversário, um ano da primeira visita, a volta do prato da estação que pediram no ano passado. É mais fácil trazer de volta quem já comeu com você do que convencer um desconhecido.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Clientes para convidar esta semana", "filas": [
        ("Mariana R.", "Aniversário na quinta · 4 visitas", "Convite pronto"),
        ("Grupo do escritório", "Almoço de fim de mês · 12 pessoas", "Lembrar na segunda"),
        ("Jorge T.", "Pediu o prato de inverno em 2025", "Avisar a volta"),
        ("Lúcia M.", "Sem visita desde julho", "Convite de retorno")]},
  ]},
  {"id": "prospectar", "h2": "2. Empresas e grupos antes da concorrência", "bloques": [
    "Jantares de equipe, cafés da manhã de trabalho, festas de fim de ano e pedidos grandes para escritórios são mesas cheias em dias fracos. Quase nunca chegam sozinhos: alguém da empresa procura opções, pergunta em dois ou três lugares e reserva onde respondem primeiro e melhor.",
    "A IA ajuda a encontrar essas empresas na sua região e a escrever para elas com uma proposta pensada para elas antes que o restaurante da frente faça isso. Quem chega primeiro com uma opção clara costuma ficar com o evento.",
  ]},
  {"id": "confianza", "h2": "3. Confiança nas redes, semana após semana", "bloques": [
    "Antes de experimentar um lugar, as pessoas olham. Veem as suas fotos, os seus stories e como você responde os comentários. Mostrar a cozinha, a equipe e os pratos toda semana faz com que escolham você antes de provar qualquer coisa, porque você já parece conhecido.",
    "O problema de sempre é o tempo: na alta temporada ninguém lembra de postar. Com IA o conteúdo é planejado, escrito e organizado com a sua voz, e a sua equipe só contribui com o que acontece na cozinha.",
  ]},
  {"id": "presencia", "h2": "4. Responder em pleno serviço", "bloques": [
    "As mensagens chegam justamente quando ninguém pode olhar o celular: no almoço, no pico do jantar, no fechamento. Um estudo publicado na Harvard Business Review mostrou que as empresas que respondiam a um interessado na primeira hora tinham quase sete vezes mais chance de fechar algo com ele do que as que esperavam uma hora a mais.{{hbr}} O estudo não é sobre restaurantes, mas a lógica vale do mesmo jeito para quem pergunta por uma mesa para hoje.",
    "Um assistente de IA responde horários, cardápio, endereço e disponibilidade na hora, faz a reserva e passa para uma pessoa o que não sabe resolver.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "WhatsApp · 21:40", "lineas": [
        ("yo", "Oi, tem mesa para 6 hoje às 22h?"),
        ("bot", "Oi. Sou o assistente de IA do restaurante. Tenho mesa para 6 às 22h15 no terraço. Reservo em nome de quem?"),
        ("yo", "Daniel. Vocês têm opções sem glúten?"),
        ("bot", "Pronto, Daniel, mesa para 6 às 22h15. Sim, os pratos sem glúten estão marcados no cardápio; já te mando. Se alguém tiver alergia, avise o garçom ao chegar."),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Menos trabalho repetido, mais equipe no salão", "bloques": [
    "Confirmar reservas, lembrar a mesa do dia, responder dez vezes se tem estacionamento, passar o pedido para a cozinha: tudo isso consome horas da melhor equipe que você tem. Quando acontece sozinho, a equipe fica livre para o que só uma pessoa faz: atender a mesa, recomendar um vinho, resolver um problema na hora.",
    "O trabalho repetido também gera números. Você sabe quantas reservas chegaram por mensagem, a que horas mais perguntam e em que dias vale reforçar o turno.",
  ]},
  nohace("A IA não cozinha nem atende a mesa. Um prato fraco ou um serviço ruim não se resolvem com mensagens rápidas: a experiência no salão continua sendo o que faz alguém voltar. O que ela faz é levar mais gente para experimentar e fazer quem já veio lembrar de você."),
  cuidar("<strong>Informação sobre alérgenos.</strong> O assistente responde só com o cardápio que a sua cozinha aprovou e passa para uma pessoa qualquer pergunta sobre alergias que não esteja nele."),
  medir(["Tempo até a primeira resposta a cada mensagem, também durante o serviço.",
         "Reservas que chegaram por mensagem e quantas compareceram.",
         "Clientes que voltaram depois de um convite.",
         "Eventos e pedidos de empresas orçados e fechados.",
         "Posts da semana e mensagens que chegaram pelas redes."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial em um restaurante?", "Para trazer de volta os clientes que você já tem, encontrar empresas e grupos que enchem os dias fracos, aparecer com constância nas redes, responder mensagens em pleno serviço e tirar da equipe o trabalho repetido, como confirmar reservas."),
  ("Um chatbot de WhatsApp substitui a minha equipe de recepção?", "Não. Ele responde o que se repete e faz reservas, e passa para uma pessoa o que não sabe resolver. A equipe fica livre para atender os clientes no salão."),
  ("Posso escrever para clientes antigos pelo WhatsApp?", "Sim, se eles aceitaram receber as suas mensagens e você usa um modelo aprovado para escrever primeiro. Se o cliente manda mensagem, você tem 24 horas para responder com mensagens livres.{{meta}}"),
  ("Serve para uma cafeteria ou um bar pequeno?", "Sim. As cinco vantagens são as mesmas; muda o volume. Em um negócio pequeno costuma valer a pena começar pelos clientes que você já tem e por responder a tempo."),
  ("Por onde eu começo?", "Vendo onde as reservas e os clientes se perdem hoje. O Audit gratuito do El Tío monta esse mapa para o seu restaurante e diz qual vantagem vale pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como o seu restaurante trabalha hoje: quantas mensagens chegam, quanto tempo esperam resposta, o que acontece com os clientes que já vieram e onde as reservas se perdem.",
},
# ---------------------------------------------------------------- HOTELARIA
{
 "es": "como-usar-ia-en-un-hotel", "slug": "como-usar-ia-em-um-hotel", "rubro": "hospitality", "rubro_nombre": "Hotelaria", "setor": "hotelaria",
 "wa": "hoteles", "about": "Inteligência artificial para hotéis e turismo",
 "title": "Como usar IA em um hotel em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA em um hotel em 2026: 5 vantagens que a sua concorrência já aproveita",
 "desc": "As 5 vantagens da inteligência artificial para hotéis boutique, pousadas, aluguel por temporada e passeios: hóspedes que voltam, grupos, avaliações, resposta em outro idioma e menos trabalho na recepção.",
 "bajada": "Um hotel boutique, uma pousada ou um operador de passeios disputa com as grandes plataformas a atenção do viajante. Este guia explica as cinco vantagens que a IA dá hoje na hotelaria, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "ho-libro-novedades", "wh": (1024, 1024), "alt": "Livro de ocorrências aberto sobre o balcão da recepção"},
 "rel": rel_pt("hotelaria", "Hotelaria", "Hotéis e pousadas", "como-usar-ia-en-un-hotel", "Cómo usar IA en un hotel en 2026",
               [("/pt/guias/reservas-diretas-whatsapp-hoteis/", "Reservas diretas pelo WhatsApp para hotéis e aluguel por temporada"),
                ("/pt/guias/chatbot-whatsapp-passeios-riviera-maya/", "Chatbot de WhatsApp para passeios em Tulum e na Riviera Maya")],
               ["rio-de-janeiro", "florianopolis", "salvador", "natal"], "hospitality"),
 "secciones": [
  hoy("hotéis, pousadas e operadores de passeios",
      "Na hotelaria o viajante vem de longe. O aeroporto de Cancún movimentou 29.345.538 passageiros em 2025, e 19.464.554 eram internacionais.{{asur}} São passageiros que chegam e saem, não pessoas diferentes, mas o recado é claro: boa parte dos seus hóspedes escreve em outro idioma e de outro fuso horário."),
  {"id": "datos", "h2": "1. Os hóspedes de temporadas passadas voltam", "bloques": [
    "Cada hóspede que ficou com você deixou um nome, uma data e às vezes um motivo: lua de mel, viagem com amigos, trabalho remoto. Essa lista é o caminho mais direto para encher a próxima temporada, porque eles já conhecem o lugar e já confiam.",
    "A vantagem está em convidá-los antes que reservem em outro lugar: algumas semanas antes da data em que vieram no ano passado, ou quando abre a temporada que escolheram. Um hóspede que volta direto não passa por uma plataforma.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Hóspedes para convidar · dezembro", "filas": [
        ("Família Oliveira", "Veio no Natal de 2025 · 3 noites", "Convite pronto"),
        ("Emma e Paul", "Aniversário de casamento em janeiro · escrevem em inglês", "Enviar em inglês"),
        ("Retiro de yoga A.", "Grupo de 14 em março", "Propor datas"),
        ("Carlos V.", "Trabalho remoto · 2 semanas", "Avisar a baixa temporada")]},
  ]},
  {"id": "prospectar", "h2": "2. Grupos que enchem semanas inteiras", "bloques": [
    "Agências, empresas com viagens de incentivo, cerimonialistas de casamento e organizadores de retiros trazem grupos que ocupam vários quartos de uma vez. Eles procuram opções com meses de antecedência e escolhem quem responde com uma proposta clara.",
    "A IA ajuda a encontrar esses organizadores e a escrever para eles antes da concorrência, com uma proposta que fala do que eles precisam: capacidade, áreas comuns, traslados e datas.",
  ]},
  {"id": "confianza", "h2": "3. Avaliações e dia a dia que geram confiança", "bloques": [
    "O viajante reserva onde confia, e confia no que vê: avaliações recentes, fotos reais, respostas aos comentários. Mostrar o dia a dia do lugar com constância, responder cada avaliação e pedi-las no momento certo faz com que escolham você e não um hotel que só tem fotos de catálogo.",
    "Com IA o conteúdo e as respostas saem toda semana, no seu tom e nos idiomas dos seus hóspedes.",
  ]},
  {"id": "presencia", "h2": "4. Responder no idioma e no horário do hóspede", "bloques": [
    "Quem planeja uma viagem de outro país escreve quando para você é madrugada, e escreve no idioma dele. Se a resposta demora, ele reserva na plataforma que responde. Um assistente de IA responde na hora, no idioma do hóspede, com a informação que você aprovou: disponibilidade, como chegar, o que está incluído.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "WhatsApp · 03:12", "lineas": [
        ("yo", "Hi! Do you have a room for 2 adults from Jan 14 to 18?"),
        ("bot", "Hi! I'm the hotel's AI assistant. Yes, we have a garden suite for those dates. Would you like me to send the details and how to book directly?"),
        ("yo", "Yes please. Is there airport transfer?"),
        ("bot", "We can arrange a transfer from the airport. I'll include it in the details, and our team will confirm the time with you in the morning."),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Recepção livre para receber bem", "bloques": [
    "Instruções de chegada, a senha do wifi, o horário do café da manhã, o lembrete do check-out: as mesmas perguntas, todos os dias. Quando saem sozinhas, a recepção fica livre para receber bem quem chega e resolver o que de fato precisa de uma pessoa.",
    "Também se organiza o que acontece entre os turnos: qual hóspede pediu o quê, o que ficou pendente e qual avaliação falta responder.",
  ]},
  nohace("A IA não substitui a hospitalidade. Um quarto diferente das fotos ou uma chegada mal resolvida não se compensam com respostas em outro idioma. O que ela faz é ajudar mais viajantes a encontrar você, reservar direto e chegar bem informados."),
  cuidar("<strong>Regras de cada plataforma.</strong> Se o hóspede reservou por uma plataforma, confira as condições dela antes de levar a conversa ou o pagamento para outro canal.", "hóspedes"),
  medir(["Tempo até a primeira resposta, de dia e de noite.",
         "Reservas diretas comparadas com reservas por plataforma.",
         "Hóspedes que voltaram depois de um convite.",
         "Orçamentos de grupos enviados e fechados.",
         "Avaliações novas e avaliações respondidas."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial em um hotel boutique?", "Para trazer de volta os hóspedes de temporadas passadas, encontrar grupos, cuidar das avaliações, responder no idioma e no horário do hóspede e tirar da recepção as perguntas repetidas."),
  ("O assistente responde em inglês e em outros idiomas?", "Sim. Ele responde no idioma em que o hóspede escreve, com a informação que você aprovou, e passa para a sua equipe o que não sabe resolver."),
  ("Ajuda a depender menos das plataformas de reserva?", "Ajuda mais reservas a chegarem direto, sobretudo de hóspedes que já conhecem você. As plataformas continuam sendo um canal; vale conferir as condições delas antes de levar conversas para outro lugar."),
  ("Serve para aluguel por temporada e passeios?", "Sim. As cinco vantagens são as mesmas para um hotel, um aluguel ou um operador de passeios; mudam os detalhes de cada conversa."),
  ("Por onde eu começo?", "Vendo quantas mensagens chegam fora do horário e o que acontece com os seus hóspedes anteriores. O Audit gratuito do El Tío monta esse mapa e diz qual vantagem pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como o seu hotel trabalha hoje: de onde chegam as reservas, quanto tempo as mensagens da noite esperam resposta, o que acontece com os seus hóspedes anteriores e para onde vai o tempo da recepção.",
},
# ---------------------------------------------------------------- IMOBILIARIO
{
 "es": "como-usar-ia-en-una-inmobiliaria", "slug": "como-usar-ia-em-uma-imobiliaria", "rubro": "real-estate", "rubro_nombre": "Imobiliário", "setor": "imobiliario",
 "wa": "inmobiliarias", "about": "Inteligência artificial para imobiliárias",
 "title": "Como usar IA em uma imobiliária em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA em uma imobiliária em 2026: 5 vantagens que a sua concorrência já aproveita",
 "desc": "As 5 vantagens da inteligência artificial para imobiliárias, incorporadoras e corretores: leads parados, novos proprietários, confiança, resposta em minutos e acompanhamento sem perder ninguém.",
 "bajada": "Em uma imobiliária cada contato pode virar um negócio grande, e a maioria se perde por falta de acompanhamento, não por falta de interesse. Este guia explica as cinco vantagens que a IA dá hoje no mercado imobiliário, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "re-activo-archivo", "wh": (1536, 1024), "alt": "Arquivo com pastas de imóveis sobre uma mesa"},
 "rel": rel_pt("imobiliario", "Imobiliário", "Imobiliárias", "como-usar-ia-en-una-inmobiliaria", "Cómo usar IA en una inmobiliaria en 2026",
               [("/pt/guias/crm-imobiliaria-acompanhamento-de-leads/", "CRM para imobiliárias: acompanhamento de leads de lançamento e aluguel")],
               ["sao-paulo", "curitiba", "brasilia", "porto-alegre"], "real-estate"),
 "secciones": [
  hoy("imobiliárias e corretores",
      "No mercado imobiliário a velocidade pesa. Um estudo publicado na Harvard Business Review mostrou que as empresas que contatavam um interessado na primeira hora tinham quase sete vezes mais chance de qualificá-lo do que as que esperavam uma hora a mais.{{hbr}} O estudo não é sobre imobiliárias, mas quem deixa os dados em três portais num domingo costuma visitar com o primeiro que responde."),
  {"id": "datos", "h2": "1. Os contatos que não compraram continuam procurando", "bloques": [
    "Toda imobiliária tem centenas de pessoas que perguntaram por um imóvel há meses e não compraram. Muitas só não compraram ainda: o orçamento mudou, esperavam um financiamento ou não acharam o que buscavam. Essa lista fica espalhada no WhatsApp de cada corretor e em planilhas que ninguém abre.",
    "Organizada, vale mais do que qualquer campanha nova. A vantagem está em voltar a escrever com algo que combine com o que elas buscavam: o novo lançamento no bairro que pediram, a baixa de um aluguel, a unidade que vagou.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Contatos para reativar", "filas": [
        ("Andrea P.", "Buscava 2 quartos em Pinheiros · março", "Nova unidade no bairro"),
        ("Investidor R.", "Perguntou por lançamento · junho", "Avisar nova torre"),
        ("Família Gomes", "Esperava financiamento · agosto", "Perguntar como está"),
        ("Diego L.", "Aluguel até um teto · setembro", "Duas opções novas")]},
  ]},
  {"id": "prospectar", "h2": "2. Proprietários e compradores antes de outra imobiliária", "bloques": [
    "Quem manda é o estoque. Encontrar proprietários que querem vender ou alugar antes da imobiliária ao lado, e compradores com um perfil claro, é o que define quantos negócios você fecha no ano.",
    "A IA ajuda a localizar essas oportunidades nos seus bairros e a escrever primeiro, com uma mensagem que fala do imóvel ou da busca de cada pessoa e não da sua imobiliária.",
  ]},
  {"id": "confianza", "h2": "3. Confiança antes da primeira visita", "bloques": [
    "Em uma compra grande, a pessoa escolhe quem ela conhece. Mostrar com constância negócios fechados, o conhecimento de cada bairro e o critério para escolher um imóvel faz o comprador chegar à visita já confiando em você.",
    "Com IA esse conteúdo sai toda semana com a sua voz, a partir do que a sua equipe já sabe e já vive na rua.",
  ]},
  {"id": "presencia", "h2": "4. Cada consulta respondida em minutos", "bloques": [
    "As consultas chegam à noite e no fim de semana, justamente quando o escritório está fechado. Um assistente de IA responde na hora com a ficha que a sua equipe aprovou, faz as perguntas de que o corretor precisa e agenda a visita.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "WhatsApp · domingo 20:05", "lineas": [
        ("yo", "Oi, vi a casa de 3 quartos para alugar. Ainda está disponível?"),
        ("bot", "Oi. Sou o assistente de IA da imobiliária. Sim, ainda está disponível. Para quando você pensa em se mudar e quantas pessoas morariam?"),
        ("yo", "Em dezembro, somos 4."),
        ("bot", "Perfeito. Te mando a ficha com os requisitos. Quer que eu agende uma visita com um corretor? Tenho horário na terça às 17h."),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Acompanhamento sem perder ninguém entre conversas", "bloques": [
    "Filtrar consultas, agendar visitas, lembrar o próximo contato depois da visita, pedir documentos: é trabalho que se repete em cada negócio e que para quando o corretor está ocupado. Quando acontece sozinho, cada contato tem um responsável e um próximo passo com data.",
    "A equipe comercial fica livre para o que fecha negócios: a visita, a negociação e a relação com o cliente.",
  ]},
  nohace("A IA não vende imóveis sozinha. A visita, a negociação e a confiança do comprador continuam nas mãos dos seus corretores. O que ela faz é garantir que nenhum contato esfrie por falta de resposta e que cada corretor chegue à visita com a informação completa."),
  cuidar("<strong>Informação de cada imóvel.</strong> O assistente responde só com a ficha aprovada. Em vendas na planta, a lei exige informações específicas para o comprador; o guia de CRM para imobiliárias explica isso a fundo."),
  medir(["Tempo até o primeiro contato com cada lead.",
         "Leads sem responsável ou sem próximo passo com data.",
         "Visitas agendadas e visitas feitas.",
         "Contatos antigos que voltaram a responder.",
         "Leads por origem: portais, redes, indicações, anúncios."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial em uma imobiliária?", "Para reativar contatos que não compraram, encontrar proprietários e compradores antes de outra imobiliária, gerar confiança com conteúdo constante, responder cada consulta em minutos e não perder ninguém no acompanhamento."),
  ("A IA consegue agendar visitas?", "Sim. Ela responde com a ficha aprovada, faz as perguntas de que o corretor precisa e agenda a visita no horário disponível. O que não sabe resolver ela passa para uma pessoa."),
  ("Posso escrever pelo WhatsApp para leads de portais?", "Para escrever primeiro pelo WhatsApp é preciso um modelo aprovado e que a pessoa tenha aceitado receber as suas mensagens. Se o lead manda mensagem, você tem 24 horas para responder com mensagens livres.{{meta}}"),
  ("Serve para uma imobiliária pequena ou um corretor autônomo?", "Sim. Com menos corretores, cada contato perdido pesa mais; organizar o acompanhamento costuma ser o primeiro passo."),
  ("Por onde eu começo?", "Vendo quantos contatos estão sem acompanhamento e quanto demora hoje a primeira resposta. O Audit gratuito do El Tío monta esse mapa e diz qual vantagem pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como a sua imobiliária trabalha hoje: de onde chegam os contatos, quanto tempo esperam resposta, quem atende e onde o acompanhamento se perde.",
},
# ---------------------------------------------------------------- FITNESS
{
 "es": "como-usar-ia-en-un-gimnasio", "slug": "como-usar-ia-em-uma-academia", "rubro": "fitness", "rubro_nombre": "Fitness", "setor": "fitness",
 "wa": "gimnasios", "about": "Inteligência artificial para academias e estúdios",
 "title": "Como usar IA em uma academia em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA em uma academia em 2026: 5 vantagens que a sua concorrência já aproveita",
 "desc": "As 5 vantagens da inteligência artificial para academias e estúdios: alunos que voltam, empresas e vizinhos, comunidade nas redes, resposta imediata e matrículas e renovações automáticas.",
 "bajada": "Uma academia ou um estúdio vive de as pessoas voltarem. Este guia explica as cinco vantagens que a IA dá hoje no fitness, de recuperar alunos que saíram até renovações que acontecem sozinhas, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "fi-clase-vacia", "wh": (1536, 1024), "alt": "Sala de aula vazia com colchonetes arrumados"},
 "rel": rel_pt("fitness", "Fitness", "Academias e estúdios", "como-usar-ia-en-un-gimnasio", "Cómo usar IA en un gimnasio en 2026",
               [("/pt/guias/retencao-alunos-academia-reservas-aulas/", "Retenção de alunos em academias e estúdios: cancelamentos e reservas de aula")],
               ["sao-paulo", "belo-horizonte", "campinas", "goiania"], "fitness"),
 "secciones": [
  hoy("academias e estúdios",
      "No fitness o problema de fundo é o hábito. Stefano DellaVigna e Ulrike Malmendier acompanharam 7.752 alunos de três academias dos Estados Unidos durante três anos: muitos iam menos do que esperavam ao se matricular e demoravam a cancelar mesmo sem frequentar.{{della}} Quem acompanha os alunos na hora certa fica com eles."),
  {"id": "datos", "h2": "1. Os alunos que saíram podem voltar", "bloques": [
    "Toda academia tem uma lista longa de alunos que cancelaram, de pessoas que fizeram a aula experimental e não voltaram e de quem perguntou e nunca se matriculou. São pessoas que já quiseram treinar com você.",
    "A vantagem está em escrever para elas no momento certo: o começo do ano, a volta das férias, a aula nova que combina com o que buscavam. Um convite na hora certa traz de volta mais gente do que um anúncio para desconhecidos.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Alunos para convidar esta semana", "filas": [
        ("Paola S.", "Cancelou em agosto · fazia spinning", "Nova aula das 7h"),
        ("Ricardo M.", "Aula experimental sem voltar", "Convite para segunda aula"),
        ("Fernanda L.", "Sem treinar há 3 semanas", "Mensagem do professor"),
        ("Equipe escritório Norte", "Perguntou por plano empresarial", "Enviar proposta")]},
  ]},
  {"id": "prospectar", "h2": "2. Empresas e vizinhos que ainda não conhecem você", "bloques": [
    "As empresas da sua região procuram opções de bem-estar para as equipes, e os vizinhos que se mudaram há pouco ainda não escolheram onde treinar. Os dois vão parar na academia que fala com eles primeiro.",
    "A IA ajuda a encontrar essas empresas e a escrever para elas com uma proposta pensada para a equipe, antes da academia do outro quarteirão.",
  ]},
  {"id": "confianza", "h2": "3. Uma comunidade que aparece nas redes", "bloques": [
    "A gente treina onde se sente parte. Mostrar as aulas, os professores e a evolução dos alunos toda semana faz quem ainda não se matriculou sentir que já conhece o lugar.",
    "Com IA o conteúdo é planejado e escrito toda semana no seu tom, e a sua equipe só contribui com o que acontece no salão.",
  ]},
  {"id": "presencia", "h2": "4. Horários e aulas experimentais respondidos na hora", "bloques": [
    "As perguntas chegam a qualquer hora: que aulas tem amanhã, se tem vaga, como é a aula experimental. Se ninguém responde, a pessoa continua procurando. Um assistente de IA responde na hora e reserva a vaga.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "Instagram · 23:18", "lineas": [
        ("yo", "Oi, vocês têm aula experimental de funcional?"),
        ("bot", "Oi. Sou o assistente de IA do estúdio. Sim, a aula experimental é para novos alunos. Tem vaga amanhã às 7h e às 19h. Qual eu reservo para você?"),
        ("yo", "A das 19h."),
        ("bot", "Pronto, ficou no seu nome. Traga roupa confortável e água, e chegue dez minutos antes para conhecer o professor."),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Matrículas, renovações e lembretes automáticos", "bloques": [
    "Matricular um aluno, lembrar o vencimento, avisar a mudança de horário, confirmar a aula do dia: trabalho que se repete todo mês e que se esquece na semana mais corrida. Quando acontece sozinho, recepção e professores ficam livres para treinar e acompanhar.",
    "Os sinais também aparecem a tempo: quem deixou de vir, que aula está esvaziando e que horário vale abrir.",
  ]},
  nohace("A IA não treina ninguém nem cria comunidade do zero. Uma aula ruim ou um ambiente frio não se resolvem com lembretes. O que ela faz é levar mais gente para experimentar e garantir que ninguém vá embora sem você perceber."),
  cuidar("<strong>Condições do plano.</strong> O assistente explica as condições exatamente como estão no seu contrato e passa para uma pessoa qualquer pedido de cancelamento ou de exceção.", "alunos"),
  medir(["Tempo até a primeira resposta a cada consulta.",
         "Aulas experimentais agendadas e alunos que se matricularam depois.",
         "Alunos sem treinar nas últimas três semanas.",
         "Alunos que voltaram depois de um convite.",
         "Renovações em dia comparadas com renovações atrasadas."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial em uma academia?", "Para trazer de volta os alunos que saíram, encontrar empresas e vizinhos, mostrar a comunidade nas redes, responder horários e aulas experimentais na hora e fazer matrículas, renovações e lembretes acontecerem sozinhos."),
  ("A IA ajuda a evitar cancelamentos?", "Ajuda a perceber a tempo quem deixou de vir e a escrever antes que a pessoa vá embora. O que retém é a academia; a IA garante que ninguém se perca sem você saber."),
  ("Posso escrever pelo WhatsApp para alunos que cancelaram?", "Sim, se eles aceitaram receber as suas mensagens e você usa um modelo aprovado para escrever primeiro. Se alguém pede para não receber mais mensagens, isso é respeitado.{{wapol}}"),
  ("Serve para um estúdio pequeno de yoga ou pilates?", "Sim. As cinco vantagens são as mesmas; em um estúdio pequeno costuma valer a pena começar pelos alunos da aula experimental que não voltaram."),
  ("Por onde eu começo?", "Vendo quantos alunos saíram este ano e quanto demora a primeira resposta. O Audit gratuito do El Tío monta esse mapa e diz qual vantagem pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como a sua academia trabalha hoje: quantas consultas chegam, o que acontece com as aulas experimentais, quantos alunos saíram e para onde vai o tempo da recepção.",
},
# ---------------------------------------------------------------- EVENTOS
{
 "es": "como-usar-ia-en-eventos", "slug": "como-usar-ia-em-eventos", "rubro": "eventos", "rubro_nombre": "Eventos", "setor": "eventos",
 "wa": "eventos", "about": "Inteligência artificial para empresas de eventos",
 "title": "Como usar IA em eventos em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA em uma empresa de eventos em 2026: 5 vantagens que a sua concorrência já aproveita",
 "desc": "As 5 vantagens da inteligência artificial para produtoras, espaços de eventos, promotores e cerimonialistas: clientes que voltam, empresas e agências, confiança, orçamentos no mesmo dia e tudo em um só lugar.",
 "bajada": "Produtoras, espaços de eventos, promotores e cerimonialistas trabalham com datas que não mudam e clientes que decidem rápido. Este guia explica as cinco vantagens que a IA dá hoje em eventos, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "ev-consulta-noche", "wh": (1536, 1024), "alt": "Consulta de evento aberta no celular à noite"},
 "rel": rel_pt("eventos", "Eventos", "Eventos", "como-usar-ia-en-eventos", "Cómo usar IA en una empresa de eventos en 2026",
               [], ["sao-paulo", "rio-de-janeiro", "brasilia", "recife"], "eventos"),
 "secciones": [
  hoy("produtoras, espaços de eventos e organizadores",
      "Em eventos, quem orça primeiro costuma ficar com a data. Um estudo publicado na Harvard Business Review mostrou que as empresas que respondiam a um interessado na primeira hora tinham quase sete vezes mais chance de fechar algo com ele do que as que esperavam uma hora a mais.{{hbr}} Quando alguém pede três orçamentos para a mesma data, o que chega na manhã seguinte já larga em desvantagem."),
  {"id": "datos", "h2": "1. Os clientes de eventos passados voltam", "bloques": [
    "Aniversários, datas de empresa, festas de fim de ano, congressos anuais: muitas datas voltam todo ano. Cada cliente que já trabalhou com você deixou uma data, um tipo de evento e um contato. Essa lista é o caminho mais direto para encher a agenda do ano que vem.",
    "A vantagem está em escrever para eles antes que comecem a pedir orçamento em outro lugar, com a proposta do evento que eles já conhecem.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Datas que voltam · próximos 90 dias", "filas": [
        ("Empresa de logística N.", "Festa de fim de ano 2025 · 180 pessoas", "Propor data"),
        ("Família Ferreira", "Festa de 15 anos da irmã mais nova", "Escrever em janeiro"),
        ("Congresso odontológico", "Edição anual em março", "Enviar proposta"),
        ("Agência R.", "3 lançamentos em 2025", "Pedir calendário 2027")]},
  ]},
  {"id": "prospectar", "h2": "2. Empresas, agências e cerimonialistas com várias datas por ano", "bloques": [
    "Um único cliente que organiza vários eventos por ano vale mais do que dez eventos avulsos. Empresas com equipes grandes, agências de marketing e cerimonialistas procuram fornecedores de confiança e ficam com quem resolve bem da primeira vez.",
    "A IA ajuda a encontrar esses clientes na sua cidade e a escrever primeiro, com uma proposta que fala do que eles organizam.",
  ]},
  {"id": "confianza", "h2": "3. Ninguém contrata um evento no escuro", "bloques": [
    "Antes de contratar, o cliente quer ver: montagens reais, detalhes, depoimentos, como um imprevisto foi resolvido. Mostrar isso com constância faz com que ele chegue ao orçamento já convencido.",
    "Com IA o conteúdo de cada evento vira os posts da semana, sem a sua equipe parar de produzir.",
  ]},
  {"id": "presencia", "h2": "4. Orçamentos respondidos no mesmo dia", "bloques": [
    "As consultas chegam enquanto você está no meio de uma montagem. Um assistente de IA responde na hora, faz as perguntas de que você precisa para orçar (data, número de pessoas, tipo de evento, local) e deixa o pedido pronto para você responder.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "WhatsApp · sábado 18:30", "lineas": [
        ("yo", "Oi, quero um orçamento de casamento para 150 pessoas em abril."),
        ("bot", "Oi. Sou o assistente de IA da produtora. Com prazer. Vocês já têm data e local, ou procuram também o espaço?"),
        ("yo", "Dia 18 de abril, procuramos espaço na zona sul."),
        ("bot", "Anotado. A equipe manda o orçamento com opções de espaço na segunda antes das 13h. Posso enviar por aqui?"),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Orçar, confirmar e cobrar de um só lugar", "bloques": [
    "Orçamentos em uma conversa, fornecedores em outra, sinais de pagamento em uma planilha: é assim que se perdem datas e pagamentos. Quando orçar, confirmar fornecedores e acompanhar os pagamentos fica em um só lugar, a equipe para de procurar informação e se dedica a produzir.",
    "Os lembretes de sinal e de saldo saem sozinhos, e cada evento guarda o seu histórico para a próxima vez.",
  ]},
  nohace("A IA não produz o evento. A montagem, os fornecedores e a operação do dia continuam sendo trabalho da sua equipe. O que ela faz é garantir que nenhum pedido escape enquanto você está no meio de uma montagem e que cada cliente volte a pensar em você quando a data dele se aproximar."),
  cuidar("<strong>O que se promete.</strong> O assistente não confirma datas nem condições que a sua equipe não aprovou; ele anota os dados e passa o orçamento para uma pessoa."),
  medir(["Tempo até a primeira resposta a cada pedido.",
         "Orçamentos enviados no mesmo dia.",
         "Orçamentos que viraram evento.",
         "Clientes antigos que voltaram a contratar.",
         "Sinais e saldos recebidos em dia."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial em uma empresa de eventos?", "Para trazer de volta os clientes de eventos passados, encontrar empresas e cerimonialistas com várias datas por ano, mostrar o seu trabalho com constância, responder pedidos no mesmo dia e organizar orçamentos, fornecedores e pagamentos."),
  ("A IA consegue orçar um evento?", "Ela consegue reunir todos os dados de que você precisa para orçar e deixar o pedido pronto. O orçamento final e as condições são definidos pela sua equipe."),
  ("Serve para um espaço de eventos ou um promotor pequeno?", "Sim. As cinco vantagens são as mesmas; em um negócio pequeno costuma valer a pena começar por responder a tempo e pelos clientes que você já tem."),
  ("Posso escrever para clientes de anos anteriores?", "Sim, se eles aceitaram receber as suas mensagens e você usa um modelo aprovado para escrever primeiro pelo WhatsApp.{{meta}}"),
  ("Por onde eu começo?", "Vendo quantos pedidos chegam, quanto você demora para orçar e quantos clientes voltam. O Audit gratuito do El Tío monta esse mapa e diz qual vantagem pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como a sua empresa de eventos trabalha hoje: quantos pedidos chegam, quanto você demora para orçar, o que acontece com os clientes de anos anteriores e onde se perdem pagamentos e datas.",
},
# ---------------------------------------------------------------- ARTISTAS
{
 "es": "como-usar-ia-siendo-artista", "slug": "como-usar-ia-sendo-artista", "rubro": "artistas", "rubro_nombre": "Artistas", "setor": "artistas",
 "wa": "artistas", "about": "Inteligência artificial para artistas, DJs e empresários artísticos",
 "title": "Como usar IA sendo artista em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA sendo artista em 2026: 5 vantagens que outros artistas já aproveitam",
 "desc": "As 5 vantagens da inteligência artificial para artistas, músicos, DJs e empresários artísticos: público que volta, casas de show e marcas, constância nas redes e a agenda em ordem sem deixar de criar.",
 "bajada": "Um artista, um DJ ou um empresário artístico vive do seu público e da sua agenda, e quase nunca tem tempo para organizar nenhum dos dois. Este guia explica as cinco vantagens que a IA dá hoje a quem cria, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "ar-fichas-fans", "wh": (1024, 1024), "alt": "Fichas de público organizadas sobre uma mesa de estúdio"},
 "rel": rel_pt("artistas", "Artistas", "Artistas", "como-usar-ia-siendo-artista", "Cómo usar IA siendo artista en 2026",
               [("/pt/guias/como-aparecer-no-chatgpt-e-no-google-pequeno-negocio/", "Como aparecer no ChatGPT e no Google se você tem uma empresa pequena")],
               ["sao-paulo", "rio-de-janeiro", "salvador", "recife"], "artistas"),
 "secciones": [
  hoy("artistas, estúdios e projetos independentes",
      "No mundo dos artistas, quem faz a diferença é a constância. Casas de show, festivais e marcas escolhem quem veem ativo, e o público segue quem fala com ele com frequência. Quem organiza hoje o público e a agenda chega antes às datas que importam."),
  {"id": "datos", "h2": "1. O seu público fica sabendo primeiro", "bloques": [
    "Quem já comprou um ingresso, uma obra, um disco ou uma aula sua é o seu público mais valioso. Esses contatos costumam ficar espalhados entre a plataforma de ingressos, as mensagens diretas e uma lista antiga.",
    "A vantagem está em organizá-los e avisar primeiro sobre o que vem: a data nova na cidade deles, a pré-venda, a obra que acabou de sair do ateliê. Um público avisado lota a primeira fila.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Público para avisar · data em Belo Horizonte", "filas": [
        ("312 pessoas", "Compraram ingresso em BH em 2025", "Aviso de pré-venda"),
        ("48 pessoas", "Perguntaram pela turnê quando não havia data", "Avisar primeiro"),
        ("Colecionadores", "Compraram obra na última exposição", "Convite exclusivo"),
        ("Alunos da oficina", "Oficina de verão", "Nova data")]},
  ]},
  {"id": "prospectar", "h2": "2. Casas de show, marcas e festivais que procuram perfis como o seu", "bloques": [
    "As casas de show montam a programação com meses de antecedência, os festivais procuram nomes para cada edição e as marcas procuram artistas para as suas ativações. Muitas dessas oportunidades se fecham antes de você ficar sabendo.",
    "A IA ajuda a encontrar esses programadores e produtores e a escrever para eles a tempo, com uma proposta que mostra por que o seu perfil combina com o que eles fazem.",
  ]},
  {"id": "confianza", "h2": "3. O público segue pessoas", "bloques": [
    "As pessoas se envolvem com o processo: o ensaio, o esboço, a passagem de som, a viagem para a próxima data. Contar isso com constância constrói um público que escolhe você quando sai algo novo.",
    "Com IA o que já acontece no seu dia vira os posts da semana com a sua voz, sem você ter que sentar para escrever cada um.",
  ]},
  {"id": "presencia", "h2": "4. Postar com frequência sem deixar de criar", "bloques": [
    "O risco de qualquer artista é sumir das redes enquanto está criando. Planejar e preparar o conteúdo com antecedência mantém você presente enquanto está no estúdio, e um assistente de IA responde as perguntas de sempre: datas, onde comprar, como contratar você.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "Instagram · 01:47", "lineas": [
        ("yo", "Quando você vem para Curitiba?"),
        ("bot", "Oi. Sou o assistente de IA da equipe. Ainda não há data em Curitiba. Quer que a gente te avise primeiro quando for anunciada?"),
        ("yo", "Quero sim"),
        ("bot", "Pronto, você entrou na lista de Curitiba. A gente te escreve por aqui assim que tiver data e pré-venda."),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Agenda e contratações em ordem", "bloques": [
    "Pedidos de contratação por cinco canais, rider técnico pedido várias vezes, datas que se cruzam: a bagunça da agenda tira horas da obra. Quando os pedidos entram em um só lugar com os dados completos, você ou o seu empresário decidem rápido e bem.",
    "O tempo que sobra volta para o que só você faz: criar.",
  ]},
  nohace("A IA não cria a sua obra nem substitui a sua voz. O que você publica e o que diz ao seu público precisa soar como você, e isso quem decide é você. O que ela faz é organizar tudo o que está em volta da obra para sobrar tempo para criá-la."),
  cuidar("<strong>A sua voz é sua.</strong> O assistente se apresenta como assistente da equipe, nunca como o artista, e tudo o que é publicado passa pela sua aprovação.", "fãs e contratantes"),
  medir(["Pessoas na sua lista de público, por cidade.",
         "Ingressos ou obras vendidos na pré-venda para a sua lista.",
         "Propostas enviadas a casas de show, festivais e marcas, e respostas.",
         "Posts da semana.",
         "Pedidos de contratação respondidos no mesmo dia."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial para um artista?", "Para organizar o seu público e avisá-lo primeiro, encontrar casas de show, marcas e festivais, contar o seu processo com constância, postar com frequência sem deixar de criar e manter a agenda e as contratações em ordem."),
  ("A IA vai criar a minha obra?", "Não. Este guia é sobre o negócio em volta da sua obra: público, agenda, contratações e redes. O que você cria continua sendo seu."),
  ("Serve para um DJ ou um músico independente?", "Sim. Com uma equipe pequena ou sem equipe, organizar o público e a agenda é o que mais libera tempo."),
  ("Posso escrever para quem comprou ingressos?", "Sim, se a pessoa aceitou receber as suas mensagens. Para escrever primeiro pelo WhatsApp é preciso um modelo aprovado.{{meta}}"),
  ("Por onde eu começo?", "Vendo onde está o seu público hoje e como chegam as contratações. O Audit gratuito do El Tío monta esse mapa e diz qual vantagem pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como você trabalha hoje: onde está o seu público, como chegam as contratações, o que você publica e para onde vai o tempo que deveria ser para criar.",
},
# ---------------------------------------------------------------- DISTRIBUICAO
{
 "es": "como-usar-ia-en-una-distribuidora", "slug": "como-usar-ia-em-uma-distribuidora", "rubro": "distribucion", "rubro_nombre": "Distribuição", "setor": "distribuicao",
 "wa": "distribuidoras", "about": "Inteligência artificial para distribuidoras e atacadistas",
 "title": "Como usar IA em uma distribuidora em 2026: 5 vantagens · El Tío",
 "h1": "Como usar IA em uma distribuidora em 2026: 5 vantagens que a sua concorrência já aproveita",
 "desc": "As 5 vantagens da inteligência artificial para distribuidoras, atacadistas, lojas de material de construção e importadoras: clientes que pararam de comprar, contas novas, confiança, catálogo na hora e pedidos em ordem.",
 "bajada": "Uma distribuidora vive de clientes que compram com frequência, e perde dinheiro cada vez que um deles para de comprar sem que ninguém perceba. Este guia explica as cinco vantagens que a IA dá hoje na distribuição, com exemplos de como ficam na prática e o que vale medir.",
 "img": {"src": "di-mostrador-pedidos", "wh": (1536, 1024), "alt": "Balcão de pedidos de uma distribuidora com folhas e caixas"},
 "rel": rel_pt("distribuicao", "Distribuição", "Distribuidoras", "como-usar-ia-en-una-distribuidora", "Cómo usar IA en una distribuidora en 2026",
               [("/pt/guias/pedidos-whatsapp-orcamentos-distribuidoras/", "De pedidos pelo WhatsApp a orçamentos para distribuidoras e lojas de material")],
               ["sao-paulo", "campinas", "ribeirao-preto", "goiania"], "distribucion"),
 "secciones": [
  hoy("distribuidoras, atacadistas e lojas de material",
      "Na distribuição o comprador compara rápido. Um estudo publicado na Harvard Business Review mostrou que as empresas que respondiam a um interessado na primeira hora tinham quase sete vezes mais chance de fechar algo com ele do que as que esperavam uma hora a mais.{{hbr}} Quando uma loja pergunta disponibilidade para três fornecedores, costuma comprar de quem responde primeiro com a informação certa."),
  {"id": "datos", "h2": "1. Os clientes que pararam de comprar, a tempo", "bloques": [
    "Uma loja que comprava toda semana e está há um mês sem pedir quase sempre está comprando em outro lugar. Na maioria das distribuidoras ninguém percebe até ser tarde, porque os pedidos estão espalhados entre vendedores, mensagens e anotações.",
    "A vantagem está em perceber esse silêncio a tempo e escrever antes de perder o cliente, com algo concreto: o produto que ele sempre pedia, a reposição que está na hora, a novidade que combina com o negócio dele.",
    {"h3": "Como fica na prática"},
    {"tipo": "panel", "titulo": "Clientes que reduziram o pedido", "filas": [
        ("Material de Construção Ponte", "Pedia toda semana · 34 dias sem pedir", "Escrever hoje"),
        ("Mercadinho Sofia", "Pedido caiu pela metade", "Perguntar o que houve"),
        ("Restaurante da Colina", "Parou de pedir óleo", "Oferecer reposição"),
        ("Loja de tintas Centro", "Pede a cada 15 dias · em dia", "Sem ação")]},
  ]},
  {"id": "prospectar", "h2": "2. Lojas e empresas que ainda não compram de você", "bloques": [
    "Na sua área de entrega existem lojas, restaurantes e empresas que hoje compram de outro fornecedor ou que abriram há pouco. Cada um é uma rota mais cheia com o mesmo caminhão.",
    "A IA ajuda a encontrá-los e a escrever primeiro, com uma proposta que fala do que eles vendem e não do seu catálogo inteiro.",
  ]},
  {"id": "confianza", "h2": "3. Confiança para trocar de fornecedor", "bloques": [
    "O comprador troca de fornecedor quando confia que você não vai falhar. Mostrar com constância o seu catálogo, as suas entregas e o respaldo que você dá quando algo dá errado torna essa decisão mais fácil.",
    "Com IA esse conteúdo sai toda semana sem tirar tempo do estoque nem dos vendedores.",
  ]},
  {"id": "presencia", "h2": "4. Catálogo e disponibilidade na hora", "bloques": [
    "As perguntas de sempre chegam a qualquer hora: se tem, quanto demora, se entrega em tal bairro. Um assistente de IA responde na hora com o catálogo e a disponibilidade que você aprovou, monta o pedido e passa para a sua equipe confirmar.",
    {"h3": "Como fica na prática"},
    {"tipo": "chat", "titulo": "WhatsApp · 06:50", "lineas": [
        ("yo", "Bom dia, vocês têm cimento e vergalhão de 3/8?"),
        ("bot", "Bom dia. Sou o assistente de IA da distribuidora. Sim, temos os dois. Quantas unidades de cada e para qual endereço?"),
        ("yo", "20 sacos e 50 barras, Distrito Industrial."),
        ("bot", "Anotado. Te mando o pedido para confirmar e o horário de entrega na sua região. Um vendedor confirma antes das 9h."),
        ("nota", "Conversa de exemplo.")]},
  ]},
  {"id": "optimizar", "h2": "5. Pedidos, estoque e rotas sem digitação manual", "bloques": [
    "Passar pedidos das mensagens para uma planilha, conferir o estoque, montar a rota do dia e avisar o cliente que está a caminho: trabalho que se repete todo dia e onde aparecem os erros. Quando acontece sozinho, a equipe se dedica a vender e a resolver.",
    "E com os pedidos organizados você enxerga o que antes não via: quais clientes crescem, quais produtos giram e qual rota vale ajustar.",
  ]},
  nohace("A IA não faz entregas nem negocia preços. A entrega no prazo e a relação com cada comprador continuam com a sua equipe. O que ela faz é garantir que nenhum pedido se perca entre mensagens e que você saiba antes de um cliente ir para outro fornecedor."),
  cuidar("<strong>Preços e estoque reais.</strong> O assistente responde só com o catálogo e a disponibilidade que a sua equipe aprovou, e qualquer pedido fora do normal vai para um vendedor."),
  medir(["Tempo até a primeira resposta a cada consulta.",
         "Clientes que reduziram a frequência de pedidos.",
         "Clientes recuperados depois de uma mensagem.",
         "Contas novas abertas no mês.",
         "Pedidos registrados sem erros."]),
 ],
 "faq": [
  ("Para que serve a inteligência artificial em uma distribuidora?", "Para perceber a tempo os clientes que param de comprar, abrir contas novas na sua região, gerar confiança, responder catálogo e disponibilidade na hora e organizar pedidos, estoque e rotas."),
  ("A IA consegue receber pedidos pelo WhatsApp?", "Sim. Ela responde com o catálogo aprovado, monta o pedido e passa para a sua equipe confirmar. O guia de pedidos pelo WhatsApp para distribuidoras explica isso a fundo."),
  ("Serve para uma loja de material ou um atacadista pequeno?", "Sim. Com menos vendedores, cada cliente que para de comprar pesa mais; perceber isso a tempo costuma ser o primeiro passo."),
  ("Posso escrever para os meus clientes pelo WhatsApp para oferecer produtos?", "Sim, se eles aceitaram receber as suas mensagens e você usa um modelo aprovado para escrever primeiro. Se o cliente manda mensagem, você tem 24 horas para responder com mensagens livres.{{meta}}"),
  ("Por onde eu começo?", "Vendo quantos clientes reduziram o pedido este ano e quanto demora a primeira resposta. O Audit gratuito do El Tío monta esse mapa e diz qual vantagem pegar primeiro."),
 ],
 "cierre": "Antes de instalar qualquer coisa, El Tío olha como a sua distribuidora trabalha hoje: como chegam os pedidos, quanto tempo esperam resposta, quais clientes reduziram o pedido e para onde vai o tempo de digitação.",
},
]
