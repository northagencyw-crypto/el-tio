"""SEO local do Brasil em português: /pt/negocios/, /pt/negocios/{cidade}/, /pt/negocios/{cidade}/{setor}/.

Uso: python generador/pseo/build_pt.py   (depois de build.py; acrescenta as URLs ao sitemap-negocios.xml)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build import RAIZ, BASE, HOY, e, semilla, rota, wa
from datos_pt import CIDADES_BR, RUBROS_PT, SLUG_PT, VENTAGEM_TITULOS, PERFIS

LEI = "a Lei Geral de Proteção de Dados (LGPD, Lei 13.709/2018)"

CAB = """<header class="cabecera">
  <a class="marca" href="https://eltio.net/pt/">EL TIO<span>.</span></a>
  <p class="estado"><i></i>ONLINE</p>
</header>"""

PIE = """<footer class="pie">
  <div class="inner">
    <div class="pie-cols">
      <div><p>Serviços</p><ul>
        <li><a href="/pt/sites/">Sites</a></li>
        <li><a href="/pt/servicos/agente-whatsapp-instagram/">Agente de WhatsApp e Instagram</a></li>
        <li><a href="/pt/servicos/crm-e-acompanhamento/">CRM e acompanhamento</a></li>
        <li><a href="/pt/posicionamento-em-ia/">Posicionamento em IA</a></li>
      </ul></div>
      <div><p>Setores</p><ul>
""" + "".join(f'        <li><a href="{r["pag"]}">{r["nome"]}</a></li>\n' for r in RUBROS_PT.values()) + """      </ul></div>
      <div><p>El Tío</p><ul>
        <li><a href="/pt/negocios/">Cidades e setores no Brasil</a></li>
        <li><a href="/pt/como-trabalhamos/">Como trabalhamos</a></li>
        <li><a href="/pt/perguntas-frequentes/">Perguntas frequentes</a></li>
        <li><a href="/pt/guias/">Guias</a></li>
        <li><a href="/pt/contato/">Contato</a></li>
      </ul></div>
    </div>
    <div class="pie-base">
      <p>El Tío · Inteligência artificial aplicada a empresas</p>
      <p><a href="mailto:hola@eltio.net">hola@eltio.net</a> · <a href="https://wa.me/525568976898?text=Ol%C3%A1%21%20Quero%20falar%20com%20El%20T%C3%ADo." data-cta="whatsapp">WhatsApp</a></p>
    </div>
  </div>
</footer>"""


def doc(ruta, titulo, desc, ld, corpo, alt=None):
    url = BASE + ruta
    lds = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>' for x in ld)
    hl = f'<link rel="alternate" hreflang="pt-BR" href="{url}">'
    if alt:
        hl += "\n" + "\n".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{v}">' for k, v in alt.items())
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)} · El Tío</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{hl}
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{BASE}/assets/og-portada.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-var.woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/guias/guias.css">
{lds}
<script src="/medicion.js" defer></script>
</head>
<body>
<a class="saltar" href="#contenido">Pular para o conteúdo</a>
{CAB}
<main id="contenido" class="guia">
{corpo}
</main>
{PIE}
</body>
</html>
"""


def migas(items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}
    vis = " / ".join(f'<a href="{u}">{e(n)}</a>' for n, u in items[:-1]) + " / " + e(items[-1][0])
    return ld, f'  <nav class="migas" aria-label="Caminho">{vis}</nav>'


def cid(t):
    return dict(zip(("slug", "nome", "estado", "perfil", "nota", "zonas", "motor"), t))


def vizinhas(c, todas, n=4):
    m = [x for x in todas if x["perfil"] == c["perfil"] and x["slug"] != c["slug"]]
    o = [x for x in todas if x["estado"] == c["estado"] and x["slug"] != c["slug"] and x not in m]
    return (o + m)[:n]


def pagina(c, rk, todas):
    r, p, nom = RUBROS_PT[rk], PERFIS[c["perfil"]], c["nome"]
    sl = SLUG_PT[rk]
    s = semilla("br", c["slug"], rk)
    ruta = f"/pt/negocios/{c['slug']}/{sl}/"
    titulo = f"Site e chatbot para {r['plural']} em {nom}"
    desc = f"Os problemas mais comuns de {r['plural']} em {nom}, como resolvê-los com um site próprio e um chatbot de WhatsApp, e um Audit gratuito para saber por onde começar."
    faqs = rota(r["faq"], 3, s // 3) + [
        (f"Vocês atendem {r['plural']} em {nom}?", f"Sim. Todo o trabalho é online, então tanto faz se você está em {nom} ou em outra cidade de {c['estado']}. Você começa pelo Audit gratuito e seguimos pelo chat."),
        ("O que é o Audit gratuito?", f"Um questionário de 15 a 25 minutos sobre como {r['um']} trabalha hoje. Em 24 a 48 horas úteis você recebe um mapa do que convém organizar primeiro. Se um site ou um chatbot não for o que mais ajuda, a gente diz."),
        ("E os meus dados e os dos meus clientes?", f"São seus. No Brasil o tratamento de dados pessoais segue {LEI}: é preciso ter uma base legal para cada uso, informar a cada pessoa quais dados você guarda e para quê, e atender quem pede acesso, correção ou exclusão. As mensagens de marketing pelo WhatsApp vão só para quem aceitou recebê-las."),
    ]
    audit = f"https://app.eltio.net/auditoria/{r['es']}"
    wt = wa(f"Olá! Tenho {'um projeto artístico' if rk == 'artistas' else 'um negócio de ' + r['nome'].lower()} em {nom} e quero o Audit gratuito.")
    l_m, h_m = migas([("El Tío", "/pt/"), ("Cidades e setores", "/pt/negocios/"), (nom, f"/pt/negocios/{c['slug']}/"), (r["nome"], ruta)])
    l_s = {"@context": "https://schema.org", "@type": "Service", "name": titulo, "description": desc, "inLanguage": "pt-BR",
           "serviceType": "Site e chatbot de WhatsApp", "url": BASE + ruta,
           "provider": {"@type": "Organization", "name": "El Tío", "url": BASE + "/pt/"},
           "areaServed": {"@type": "City", "name": nom, "containedInPlace": {"@type": "State", "name": c["estado"], "containedInPlace": {"@type": "Country", "name": "Brasil"}}},
           "audience": {"@type": "BusinessAudience", "audienceType": r["plural"]}}
    l_f = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    h = [h_m, "  <article>", f"    <h1>{e(titulo)}</h1>",
         f'    <p class="bajada">{e(c["nota"])} Esta página reúne os problemas que mais se repetem em {e(r["plural"])} e como organizá-los com um site próprio e um chatbot de WhatsApp e Instagram.</p>',
         f'    <p class="fecha">Atualizada em {HOY[8:10]}/{HOY[5:7]}/{HOY[:4]}</p>',
         '    <h2 id="problemas">O que mais se repete</h2>']
    for t, d in rota(r["problemas"], 4, s):
        h += [f"    <h3>{e(t)}</h3>", f"    <p>{e(d)}</p>"]
    h += [f'    <h2 id="cidade">O que muda em {e(nom)}</h2>', f"    <p>{e(p['geral'])}</p>", f"    <p>{e(p[rk])}</p>",
          f"    <p>{e(r['local'].format(nom=nom, zonas=c['zonas'], motor=c['motor']))}</p>",
          f'    <div class="aviso">Um teste simples: procure no Google «{e(r["plural"].split(" e ")[0])} em {e(nom)}» pelo celular e veja se você aparece, o que se vê do seu negócio e quanto tempo levaria para responder se alguém escrevesse agora.</div>',
          f'    <h2 id="vantagem">Sua vantagem em {e(r["nome"].lower())} em {e(nom)}</h2>',
          f"    <p>A IA já é uma vantagem diante do mercado e a janela é hoje: quem não dá um passo agora, amanhã precisa dar dez para chegar ao mesmo lugar. Estas são as cinco que mais pesam em {e(r['plural'])}.</p>",
          '    <ol class="lista">']
    h += [f"      <li><strong>{e(t)}.</strong> {e(x)}</li>" for t, x in zip(VENTAGEM_TITULOS, r["ventagens"])]
    h += ["    </ol>", f'    <p><a data-cta="ventaja" href="{e(wt)}">Não perca a vantagem, é hoje. Fale com El Tío.</a></p>',
          '    <h2 id="como">Como se resolve</h2>', '    <ol class="lista">']
    h += [f"      <li>{e(x)}</li>" for x in [r["passos"][0]] + rota(r["passos"][1:], 3, s)]
    h += ["    </ol>", "    <p>O site sai em 8 idiomas, com domínio próprio e preparado para aparecer no Google e em assistentes de IA como o ChatGPT. O que não se usa não se instala: a ordem é definida pelo Audit.</p>",
          '    <h2 id="perguntas">Perguntas frequentes</h2>']
    for q, a in faqs:
        h += [f"    <h3>{e(q)}</h3>", f"    <p>{e(a)}</p>"]
    h += ['    <section class="cierre" id="comecar">', "      <h2>Por onde começar</h2>",
          f"      <p>O Audit é gratuito: um questionário de 15 a 25 minutos sobre {e(r['um'])} e, em 24 a 48 horas úteis, o mapa do que convém fazer primeiro. Tudo segue pelo chat.</p>",
          '      <div class="acciones">', f'        <a class="btn" data-cta="audit" href="{audit}">Fazer o Audit gratuito</a>',
          f'        <a class="enlace" data-cta="whatsapp" href="{e(wt)}">Escrever pelo WhatsApp</a>', "      </div>", "    </section>",
          '    <nav class="relacionado" aria-label="Para continuar">', "      <p>Para continuar</p>", "      <ul>",
          f'        <li><a href="{r["pag"]}">{e(r["nome"])}</a>: a página do setor</li>', '        <li><a href="/pt/sites/">Sites do El Tío</a></li>']
    for v in vizinhas(c, todas):
        h.append(f'        <li><a href="/pt/negocios/{v["slug"]}/{sl}/">{e(r["plural"].capitalize())} em {e(v["nome"])}</a></li>')
    for k in rota([k for k in RUBROS_PT if k != rk], 3, s):
        h.append(f'        <li><a href="/pt/negocios/{c["slug"]}/{SLUG_PT[k]}/">{e(RUBROS_PT[k]["plural"].capitalize())} em {e(nom)}</a></li>')
    h += [f'        <li><a href="/pt/negocios/{c["slug"]}/">Todos os setores em {e(nom)}</a></li>', "      </ul>", "    </nav>", "  </article>"]
    return ruta, doc(ruta, titulo, desc, [l_s, l_f, l_m], "\n".join(h), {"x-default": ruta})


def hub_cidade(c, todas):
    ruta = f"/pt/negocios/{c['slug']}/"
    titulo = f"Sites e chatbots para negócios em {c['nome']}"
    desc = f"Site próprio e chatbot de WhatsApp para restaurantes, hotéis, imobiliárias, academias, eventos, artistas e distribuidoras de {c['nome']}. Audit gratuito."
    l_m, h_m = migas([("El Tío", "/pt/"), ("Cidades e setores", "/pt/negocios/"), (c["nome"], ruta)])
    p = PERFIS[c["perfil"]]
    h = [h_m, "  <article>", f"    <h1>{e(titulo)}</h1>", f'    <p class="bajada">{e(c["nota"])} {e(p["geral"])}</p>', "    <h2>Escolha o seu setor</h2>", "    <ul>"]
    for k, r in RUBROS_PT.items():
        h.append(f'      <li><a href="/pt/negocios/{c["slug"]}/{SLUG_PT[k]}/"><strong>{e(r["plural"].capitalize())}</strong></a>: {e(p[k])}</li>')
    h += ["    </ul>", '    <section class="cierre"><h2>Por onde começar</h2><p>O Audit é gratuito e em 24 a 48 horas úteis você tem o mapa do que convém fazer primeiro.</p>',
          '      <div class="acciones"><a class="btn" data-cta="audit" href="https://app.eltio.net/">Fazer o Audit gratuito</a>',
          f'      <a class="enlace" data-cta="whatsapp" href="{e(wa("Olá! Tenho um negócio em " + c["nome"] + " e quero o Audit gratuito."))}">Escrever pelo WhatsApp</a></div></section>',
          '    <nav class="relacionado" aria-label="Para continuar"><p>Outras cidades</p><ul>']
    h += [f'      <li><a href="/pt/negocios/{v["slug"]}/">{e(v["nome"])}</a></li>' for v in vizinhas(c, todas, 6)]
    h += ["    </ul></nav>", "  </article>"]
    return ruta, doc(ruta, titulo, desc, [l_m], "\n".join(h), {"x-default": ruta})


def hub_indice(todas):
    ruta = "/pt/negocios/"
    titulo = "Sites e chatbots por cidade e setor no Brasil"
    desc = "El Tío nas principais cidades do Brasil: site próprio e chatbot de WhatsApp por setor, com os problemas típicos de cada negócio e um Audit gratuito."
    l_m, h_m = migas([("El Tío", "/pt/"), ("Cidades e setores", ruta)])
    h = [h_m, "  <article>", f"    <h1>{e(titulo)}</h1>",
         '    <p class="bajada">Cada página explica o que mais se repete num setor, o que muda naquela cidade e como organizar tudo com um site próprio e um chatbot. Escolha a sua cidade.</p>',
         "    <h2>Brasil</h2>", "    <ul>"]
    h += [f'      <li><a href="/pt/negocios/{x["slug"]}/">{e(x["nome"])}</a>, {e(x["estado"])}</li>' for x in sorted(todas, key=lambda x: x["nome"])]
    h += ["    </ul>", "  </article>"]
    return ruta, doc(ruta, titulo, desc, [l_m], "\n".join(h), {"es": "/negocios/", "x-default": "/negocios/"})


def main():
    todas = [cid(t) for t in CIDADES_BR]
    pags = [hub_indice(todas)]
    for c in todas:
        pags.append(hub_cidade(c, todas))
        pags += [pagina(c, rk, todas) for rk in RUBROS_PT]
    for ruta, d in pags:
        if "—" in d:
            raise SystemExit(f"travessão em {ruta}")
        p = os.path.join(RAIZ, ruta.strip("/"))
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "index.html"), "w", encoding="utf-8", newline="\n").write(d)
    sm = os.path.join(RAIZ, "sitemap-negocios.xml")
    x = open(sm, encoding="utf-8").read()
    x = "\n".join(l for l in x.split("\n") if "/pt/negocios/" not in l)
    linhas = "\n".join(f"  <url><loc>{BASE}{r}</loc><lastmod>{HOY}</lastmod><changefreq>monthly</changefreq><priority>{'0.6' if r.count('/') > 4 else '0.7'}</priority></url>" for r, _ in pags)
    x = x.replace("</urlset>", linhas + "\n</urlset>")
    open(sm, "w", encoding="utf-8", newline="\n").write(x)
    n = sum(1 for r, _ in pags if r.count("/") == 5)
    print(f"{len(pags)} páginas ({n} cidade x setor, {len(todas)} cidades)")


if __name__ == "__main__":
    main()
