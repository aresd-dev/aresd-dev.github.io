"""Coloca ?v=<hash do conteúdo> nos links de CSS/JS do index.html.

O GitHub Pages deixa o navegador guardar cada arquivo por 10 min. Sem versão,
quem já visitou o site pode juntar o HTML novo com o JS/CSS antigo. Com a versão
na URL, mudou o arquivo, mudou a URL, e o navegador baixa o novo na hora.

Rode antes de cada commit que mexer em css/ ou js/:
    python tools/versionar.py
(tests/check_site.py falha se a versão estiver desatualizada.)
"""
import hashlib
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
ASSET_RE = re.compile(r'(href|src)="((?:css|js)/[^"?]+\.(?:css|js))(?:\?v=[0-9a-f]*)?"')


def content_hash(path):
    # normaliza fim de linha: o Git no Windows pode trocar LF por CRLF na cópia local
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()[:8]


def main():
    index = ROOT / "index.html"
    html = index.read_text(encoding="utf-8")
    changed = []

    def repl(m):
        attr, rel = m.group(1), m.group(2)
        new = f'{attr}="{rel}?v={content_hash(ROOT / rel)}"'
        if new != m.group(0):
            changed.append(rel)
        return new

    out = ASSET_RE.sub(repl, html)
    if out != html:
        index.write_text(out, encoding="utf-8", newline="\n")
    print("atualizados: " + (", ".join(changed) if changed else "nenhum (já em dia)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
