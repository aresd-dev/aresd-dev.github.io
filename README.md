# Portfólio de (Ares) Guilherme Dantas — Desenvolvedor Back-end

Site estático (HTML, CSS e JavaScript puro, sem build) em **PT e EN**, pensado para o GitHub Pages
do repositório `aresd-dev.github.io`. Estrutura inspirada no site de Yudi Ganeko: hero, timeline com
bullets de impacto e carrossel de imagens, mas com **projetos** no lugar de empregos.

## Rodar localmente

```bash
python -m http.server 8000
# abra http://localhost:8000
```

## Verificar

```bash
python tests/check_site.py
tools/versionar.py  # versão (?v=hash) dos links de CSS/JS
```

Falha se: uma chave `data-i18n*` não existir em `js/i18n.js` ou faltar `pt`/`en`; houver chave
do dicionário sem uso; um `src`/`href` local não resolver; um link externo estiver fora da lista
esperada; ou uma imagem estiver sem `width`/`height`, `loading="lazy"` ou alt traduzido.

**Antes de commitar mudanças em `css/` ou `js/`:**

```bash
python tools/versionar.py
```

Ele coloca `?v=<hash do conteúdo>` nos links de CSS/JS do `index.html`. O GitHub Pages deixa o
navegador guardar cada arquivo por 10 min; com a versão na URL, quem volta ao site recebe o
arquivo novo na hora, em vez de misturar HTML novo com JS antigo. O checker falha se a versão
estiver desatualizada.

## Estrutura

```
index.html        # marcação; todo texto traduzível tem data-i18n="chave"
css/style.css     # tokens (claro/escuro automático), timeline, carrossel, responsivo
js/i18n.js        # dicionário { chave: { pt, en } }
js/main.js        # troca de idioma, carrossel, fallback da foto
img/projetos/     # prints copiados das vitrines
tests/check_site.py
```

## Como editar

- **Foto:** coloque `img/foto.jpg` (proporção 4:5). Sem o arquivo, aparece um avatar com a inicial.
- **Textos:** edite `js/i18n.js` (PT e EN juntos). O texto em PT dentro do HTML é só o padrão sem JavaScript.
- **Idioma inicial:** o salvo no navegador; senão, `navigator.language` (pt → PT, o resto → EN).
- **Números dos projetos** vêm das vitrines que o site linka (zone-portfolio, postador, shiori,
  washi-vitrine). Ao mudar um número lá, mude aqui também, para um bater com o outro.

## Publicar

Quando quiser: crie o repositório `aresd-dev/aresd-dev.github.io` no GitHub e envie esta pasta;
o GitHub Pages serve a raiz da branch principal.

© 2026 (Ares) Guilherme Dantas. Imagens e textos dos projetos: todos os direitos reservados.
