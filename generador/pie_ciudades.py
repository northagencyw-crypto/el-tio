# Suma las ciudades de Colombia, Argentina, Chile y Perú a la columna «Ciudades» del pie en español.
# Una línea por país para no recargar el pie. Solo páginas en español (no toca /pt/ ni otros idiomas).
# Uso: python generador/pie_ciudades.py (desde el-tio). Idempotente.
import pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
IDIOMAS = {"en", "pt", "de", "fr", "it", "ja", "zh"}
ANCLA = '        <li><a href="/ciudades/tulum-riviera-maya/">Tulum y Riviera Maya</a></li>\n'
GRUPOS = [
    [("bogota", "Bogotá"), ("medellin", "Medellín"), ("cali", "Cali")],
    [("buenos-aires", "Buenos Aires"), ("cordoba", "Córdoba"), ("rosario", "Rosario")],
    [("santiago", "Santiago"), ("valparaiso", "Valparaíso")],
    [("lima", "Lima"), ("arequipa", "Arequipa")],
]
BLOQUE = "".join(
    "        <li>" + " · ".join(f'<a href="/ciudades/{s}/">{n}</a>' for s, n in g) + "</li>\n" for g in GRUPOS)
MARCA = re.compile(r'        <li><a href="/ciudades/bogota/">.*?\n(?:        <li><a href="/ciudades/[a-z-]+/">[^\n]*· [^\n]*\n)*')

n = 0
for f in R.rglob("*.html"):
    rel = f.relative_to(R).parts
    if rel[0] in IDIOMAS or rel[0] == "generador":
        continue
    s = f.read_text(encoding="utf-8")
    if ANCLA not in s:
        continue
    t = MARCA.sub("", s)
    t = t.replace(ANCLA, ANCLA + BLOQUE, 1)
    if t != s:
        f.write_bytes(t.encode("utf-8"))
        n += 1
print("pie actualizado en", n, "páginas")
