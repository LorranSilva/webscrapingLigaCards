# WebScraping Liga Cards

Web scraping das coleções de cartas da **LigaPokemon**, **LigaYuGiOh** e **LigaMagic**, extraindo nome, sigla, quantidade de cartas e faixas de preço de cada coleção.

## Tecnologias

- Python 3
- [Scrapy 2.15](https://scrapy.org/) — framework de web scraping
- [Scrapy-Splash](https://github.com/scrapy-plugins/scrapy-splash) — renderização de páginas com JavaScript
- [Docker](https://www.docker.com/) — execução do servidor Splash
- Jupyter Notebook — orquestração dos spiders

## Estrutura do projeto

```
webscrapingLigaCards/
├── scrapcards/
│   ├── scrapcards/
│   │   ├── spiders/
│   │   │   ├── ligamagic.py   # Spider para LigaMagic (Magic: The Gathering)
│   │   │   ├── ligapoke.py    # Spider para LigaPokemon
│   │   │   └── ligaygo.py     # Spider para LigaYuGiOh
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   └── settings.py
│   └── datasets/
│       ├── mtg.json           # Dados de Magic: The Gathering
│       ├── ptcg.json          # Dados de Pokémon TCG
│       └── ygo.json           # Dados de Yu-Gi-Oh!
├── notebooks/
│   └── executer.ipynb         # Notebook para executar os spiders
├── images/
├── requirements.txt
└── README.md
```

## Dados coletados

Para cada coleção são extraídos:

| Campo | Descrição |
|---|---|
| `name` | Nome da coleção |
| `acronym` | Sigla da coleção |
| `cards_quantity` | Quantidade de cartas |
| `lowest_price` | Soma dos menores preços (R$) |
| `averege_price` | Preço médio da coleção (R$) |
| `highest_price` | Soma dos maiores preços (R$) |
| `cards` | Lista detalhada de todas as cartas |

## Como funciona

As páginas dos sites renderizam conteúdo dinamicamente via JavaScript. Para confirmar isso, desabilite o JS no navegador via DevTools (`Ctrl+Shift+P` → "Disable JavaScript") e recarregue a página — os dados das cartas desaparecem.

Para contornar isso, o projeto usa **Scrapy-Splash** (via Docker) que renderiza o JavaScript antes de fazer o scraping. Os dados das cartas ficam em uma variável JavaScript `cardsjson` embutida no HTML, extraída via regex após a renderização.

## Pré-requisitos

- Python 3.x
- Docker instalado e em execução

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/LorranSilva/webscrapingLigaCards.git
cd webscrapingLigaCards

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Suba o servidor Splash
docker pull scrapinghub/splash
docker run -it -p 8050:8050 --rm docker.io/scrapinghub/splash
```

## Executando

### Via Notebook

Abra e execute o notebook `notebooks/executer.ipynb`. Os resultados serão salvos em `scrapcards/datasets/`.

### Via linha de comando

```bash
cd scrapcards

# Pokémon TCG
scrapy crawl ligapoke -O datasets/ptcg.json

# Magic: The Gathering
scrapy crawl ligamagic -O datasets/mtg.json

# Yu-Gi-Oh!
scrapy crawl ligaygo -O datasets/ygo.json
```

> `-O` sobrescreve o arquivo; `-o` acrescenta ao arquivo existente.

## Comandos úteis do Scrapy

```bash
# Shell interativo para testar seletores
scrapy shell

# Testar conexão com o site
fetch('https://www.ligapokemon.com.br/?view=cards/home')

# Testar seletores CSS
response.css('.edc-nm-2').get()
```
