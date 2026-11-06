"""Genera llms-full.txt: llms.txt mas el texto completo de las paginas clave en espanol.
Uso: python generador/llms_full.py  (desde la raiz del repo o desde cualquier lado)."""
import html, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINAS = ["", "paginas-web/", "posicionamiento-en-ia/", "prospeccion-y-email/", "como-trabajamos/",
           "servicios/", "gastronomia/", "hospitality/", "real-estate/", "fitness/", "eventos/",
           "artistas/", "distribucion/", "ciudades/", "preguntas-frecuentes/", "sobre-el-tio/",
           "indice/", "cronometro/", "glosario/"]
for d in ("servicios", "guias", "ciudades"):
    base = os.path.join(RAIZ, d)
    for s in sorted(os.listdir(base)):
        if os.path.isfile(os.path.join(base, s, "index.html")):
            PAGINAS.append(f"{d}/{s}/")
PRECIO = re.compile(r"(USD|MXN|US\$|\$\s?\d|\d+\s?(pesos|dolares|dólares))", re.I)


def texto(ruta):
    h = open(os.path.join(RAIZ, ruta, "index.html"), encoding="utf-8").read()
    titulo = html.unescape(re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip())
    m = re.search(r"<main.*?</main>", h, re.S) or re.search(r"<body.*?</body>", h, re.S)
    c = re.sub(r"<(script|style|svg|nav|header|footer|form)\b.*?</\1>", " ", m.group(0), flags=re.S)
    c = re.sub(r"</(p|h[1-6]|li|dt|dd|tr|div|section|article)>", "\n", c)
    c = html.unescape(re.sub(r"<[^>]+>", " ", c))
    lineas = [re.sub(r"\s+", " ", l).strip() for l in c.splitlines()]
    lineas = [l for l in lineas if len(l) > 2 and not PRECIO.search(l)]
    salida, prev = [], None
    for l in lineas:
        if l != prev:
            salida.append(l)
        prev = l
    return titulo, "\n".join(salida)


partes = [open(os.path.join(RAIZ, "llms.txt"), encoding="utf-8").read().rstrip(), "\n\n# Texto completo de las paginas\n"]
for p in PAGINAS:
    t, cuerpo = texto(p)
    partes.append(f"\n## {t}\nURL: https://eltio.net/{p}\n\n{cuerpo}\n")
salida = "".join(partes).replace("—", ",")
open(os.path.join(RAIZ, "llms-full.txt"), "w", encoding="utf-8", newline="\n").write(salida)
print("llms-full.txt:", len(PAGINAS), "paginas,", len(salida), "caracteres")
