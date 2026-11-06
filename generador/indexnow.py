"""Envia las URL de los sitemaps de eltio.net a IndexNow (Bing, Yandex, Seznam, Naver;
Bing alimenta la busqueda de ChatGPT).

Uso despues de cada deploy (cuando el push ya esta en vivo):
    python generador/indexnow.py            # todas las URL de los sitemaps
    python generador/indexnow.py URL [URL]  # solo las URL indicadas
La clave es el archivo <clave>.txt de la raiz del repo, servido en https://eltio.net/<clave>.txt.
"""
import glob, json, os, re, sys, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "eltio.net"
LOTE = 10000
ENDPOINT = os.environ.get("INDEXNOW_ENDPOINT", "https://api.indexnow.org/indexnow")


def clave():
    for f in glob.glob(os.path.join(RAIZ, "*.txt")):
        n = os.path.basename(f)[:-4]
        if re.fullmatch(r"[a-f0-9]{32}", n) and open(f).read().strip() == n:
            return n
    sys.exit("No hay archivo de clave IndexNow en la raiz")


def urls_sitemaps():
    urls = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "sitemap*.xml"))):
        x = open(f, encoding="utf-8").read()
        if "<sitemapindex" in x:
            continue
        urls += re.findall(r"<loc>\s*(.*?)\s*</loc>", x)
    return list(dict.fromkeys(urls))


def enviar(urls, k):
    for i in range(0, len(urls), LOTE):
        lote = urls[i:i + LOTE]
        cuerpo = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt", "urlList": lote}).encode()
        req = urllib.request.Request(ENDPOINT, data=cuerpo,
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print(f"lote {i // LOTE + 1}: {len(lote)} URL -> HTTP {r.status}")
        except urllib.error.HTTPError as e:
            print(f"lote {i // LOTE + 1}: {len(lote)} URL -> HTTP {e.code} {e.read()[:300]!r}")


if __name__ == "__main__":
    k = clave()
    lista = sys.argv[1:] or urls_sitemaps()
    print(f"{len(lista)} URL, clave {k}")
    enviar(lista, k)
