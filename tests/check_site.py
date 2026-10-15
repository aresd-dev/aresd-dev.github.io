"""Verificação estática do site (sem dependências).

Falha (exit 1) se:
  - uma chave data-i18n* usada no HTML não existe em js/i18n.js, ou falta pt/en;
  - uma chave do dicionário não é usada em lugar nenhum (HTML ou main.js);
  - um src/href local não resolve para um arquivo existente;
  - um link externo está fora da lista esperada;
  - um <img> não tem width/height ou loading=lazy (exceto a foto do hero).
Uso: python tests/check_site.py
"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPTIONAL = {"img/foto.jpg"}  # placeholder: o usuário coloca depois; o site tem fallback
ALLOWED_EXTERNAL_PREFIXES = (
    "https://github.com/aresd-dev",
    "https://www.linkedin.com/in/aresd-dev",
    "mailto:aresd.dev@gmail.com",
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
)
I18N_ATTRS = ("data-i18n", "data-i18n-alt", "data-i18n-aria")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys = []      # (attr, key)
        self.refs = []      # (tag, attr, value)
        self.imgs = []      # atributos de cada <img>

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for name in I18N_ATTRS:
            if name in a:
                self.keys.append((name, a[name]))
        for name in ("src", "href"):
            if name in a:
                self.refs.append((tag, name, a[name]))
        if tag == "img":
            self.imgs.append(a)


def load_dictionary(js_text):
    """Lê as chaves de window.I18N sem executar JS: pega "chave": { pt: ..., en: ... }."""
    entries = {}
    for m in re.finditer(r'^\s*"([^"]+)":\s*\{(.*?)\n?\s*\}\s*,?\s*$', js_text, re.S | re.M):
        entries[m.group(1)] = m.group(2)
    return entries


def main():
    errors = []
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    js_i18n = (ROOT / "js" / "i18n.js").read_text(encoding="utf-8")
    js_main = (ROOT / "js" / "main.js").read_text(encoding="utf-8")

    col = Collector()
    col.feed(html)
    entries = load_dictionary(js_i18n)

    # 1) chaves usadas existem e têm pt e en
    used = {key for _, key in col.keys}
    for key in sorted(used):
        body = entries.get(key)
        if body is None:
            errors.append(f"chave i18n ausente no dicionário: {key}")
            continue
        for lang in ("pt", "en"):
            if not re.search(rf'\b{lang}:\s*"', body):
                errors.append(f"chave '{key}' sem texto em '{lang}'")

    # 2) chaves do dicionário não usadas (meta.* são usadas por main.js)
    for key in sorted(entries):
        if key not in used and f'"{key}"' not in js_main and not key.startswith("meta."):
            errors.append(f"chave do dicionário não usada: {key}")

    # 3) refs locais resolvem; externas são permitidas
    for tag, attr, value in col.refs:
        if value.startswith("#"):
            target = value[1:]
            if target and f'id="{target}"' not in html:
                errors.append(f"âncora sem destino: {value}")
        elif value.startswith(("http://", "https://", "mailto:")):
            if not value.startswith(ALLOWED_EXTERNAL_PREFIXES):
                errors.append(f"link externo inesperado: {value}")
        else:
            if value not in OPTIONAL and not (ROOT / value).exists():
                errors.append(f"arquivo local não existe: {value}")

    # 4) imagens com dimensões e lazy-load (exceto foto do hero)
    for a in col.imgs:
        src = a.get("src", "")
        if src in OPTIONAL:
            continue
        if not (a.get("width") and a.get("height")):
            errors.append(f"<img> sem width/height: {src}")
        if a.get("loading") != "lazy":
            errors.append(f"<img> sem loading=lazy: {src}")
        if not a.get("data-i18n-alt"):
            errors.append(f"<img> sem alt traduzido: {src}")

    if errors:
        print(f"FALHOU: {len(errors)} problema(s)")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(used)} chaves i18n usadas, {len(entries)} no dicionário, "
          f"{len(col.refs)} refs, {len(col.imgs)} imagens.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
