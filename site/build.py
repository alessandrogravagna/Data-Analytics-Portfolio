#!/usr/bin/env python3
"""
Generatore del sito GitHub Pages del portfolio.

Legge i README.md dei progetti (unica fonte di verita') e produce il sito
statico dentro la cartella docs/, pubblicabile con GitHub Pages.

Uso:
    python3 site/build.py

Nessuna dipendenza esterna: solo libreria standard.
"""

import html
import os
import re
import shutil
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "docs")

REPO = "alessandrogravagna/Data-Analytics-Portfolio"
REPO_URL = f"https://github.com/{REPO}"
SITE_URL = "https://alessandrogravagna.github.io/Data-Analytics-Portfolio/"
OG_IMAGE = SITE_URL + "assets/img/powerbi-techmarket-powerbi_dashboard_preview.png"
LINKEDIN = "https://www.linkedin.com/in/alessandro-gravagna-3a3050201/"
EMAIL = "alegrava8@gmail.com"

AUTHOR = "Alessandro Gravagna"
PLACE = "Monza (MB)"

# --------------------------------------------------------------------------
# Metadati dei progetti (l'ordine e' quello di pubblicazione in homepage)
# --------------------------------------------------------------------------

PROJECTS = [
    {
        "slug": "behavioral-feature-store",
        "dir": "03-SQL-Project",
        "emoji": "\U0001F5C4\uFE0F",
        "title": "Behavioral Feature Store",
        "tagline": "Feature engineering bancario in SQL puro",
        "domain": "Banking",
        "cat": "SQL",
        "tools": ["SQL", "MySQL", "PostgreSQL"],
        "featured": True,
        "metric": "1 riga per cliente",
        "metric_label": "dataset ML-ready",
        "summary": "Trasformazione di un database transazionale relazionale in un feature store "
                   "denormalizzato: join a cascata, aggregazione condizionale e pivoting per "
                   "alimentare modelli di churn prediction.",
    },
    {
        "slug": "credit-card-segmentation",
        "dir": "04-Python/03-Credit-Card-Customer-Segmentation",
        "emoji": "\U0001F4B3",
        "title": "Credit Card Customer Segmentation",
        "tagline": "Clustering K-Means e strategie di marketing mirate",
        "domain": "Banking",
        "cat": "Python",
        "tools": ["Python", "Scikit-learn", "K-Means", "PCA"],
        "featured": True,
        "metric": "4 cluster",
        "metric_label": "profili cliente azionabili",
        "summary": "Segmentazione comportamentale della base clienti su 17 feature transazionali, "
                   "con log-transform, standardizzazione, validazione via Elbow/Silhouette e "
                   "proiezione PCA. Ogni cluster ha una strategia promozionale dedicata.",
    },
    {
        "slug": "powerbi-techmarket",
        "dir": "02-Business Intelligence/01-PowerBI-TechMarket",
        "emoji": "\U0001F3EC",
        "title": "TechMarket Sales & Returns Analytics",
        "tagline": "Dashboard Power BI con star schema e misure DAX",
        "domain": "Retail BI",
        "cat": "Power BI",
        "tools": ["Power BI", "DAX", "Power Query"],
        "featured": True,
        "metric": "5 aree",
        "metric_label": "di report navigabili a bookmark",
        "thumb": "02-Business Intelligence/images/powerbi_dashboard_preview.png",
        "summary": "Report su una catena di elettronica di consumo: pipeline ETL in Power Query, "
                   "modello a stella, calcolo delle vendite nette al netto dei resi e "
                   "geolocalizzazione delle performance per citta'.",
    },
    {
        "slug": "tableau-superstore-europa",
        "dir": "02-Business Intelligence/02-Tableau-Superstore-Europa",
        "emoji": "\U0001F1EA\U0001F1FA",
        "title": "Superstore Europa",
        "tagline": "Data storytelling e riallocazione del budget marketing",
        "domain": "E-Commerce",
        "cat": "Tableau",
        "tools": ["Tableau", "Storytelling", "Geo-analytics"],
        "featured": True,
        "metric": "Live",
        "metric_label": "pubblicato su Tableau Public",
        "thumb": "02-Business Intelligence/images/tableau_story_preview.png",
        "live": ("Apri su Tableau Public",
                 "https://public.tableau.com/app/profile/alessandro.gravagna/viz/Progettotableaumaster/Storia1"),
        "summary": "Tableau Story costruita sul framework 3C (Contesto, Conflitto, Conclusione) per "
                   "individuare i prodotti ad alto margine da spingere e quelli in perdita da "
                   "razionalizzare nel mercato europeo.",
    },
    {
        "slug": "fake-news-detection",
        "dir": "04-Python/04-Fake-News-Detection-NLP",
        "emoji": "\U0001F4F0",
        "title": "Fake News Detection",
        "tagline": "Classificazione NLP di titoli veri vs. disinformazione",
        "domain": "Media / NLP",
        "cat": "Python",
        "tools": ["Python", "NLP", "TF-IDF", "Scikit-learn"],
        "metric": "99%",
        "metric_label": "accuracy su 8.980 articoli",
        "summary": "Pipeline NLP con TF-IDF su unigrammi e bigrammi, arricchita con feature "
                   "strutturali del titolo (lunghezza, maiuscole, punti esclamativi) e modello di "
                   "regressione logistica serializzato per il riuso.",
    },
    {
        "slug": "bitcoin-sentiment-pyspark",
        "dir": "04-Python/05-Bitcoin-Sentiment-Analysis-PySpark",
        "emoji": "\u20BF",
        "title": "Bitcoin Sentiment Analysis",
        "tagline": "Sentiment su larga scala con calcolo distribuito",
        "domain": "Finance / Crypto",
        "cat": "Python",
        "tools": ["PySpark", "Big Data", "TextBlob", "Pandas UDF"],
        "metric": "r \u2248 0,01",
        "metric_label": "correlazione sentiment / prezzo BTC",
        "summary": "Pipeline PySpark su milioni di tweet: pulizia regex, language detection e "
                   "sentiment analysis vettorizzata via Pandas UDF, join temporale con lo storico "
                   "BTC/USD e lettura critica di una correlazione che risulta assente.",
    },
    {
        "slug": "aviation-accidents",
        "dir": "04-Python/02-Aviation-Accidents-Analytics",
        "emoji": "\u2708\uFE0F",
        "title": "Aviation Accidents Analytics",
        "tagline": "Un secolo di incidenti aerei, 1919-2023",
        "domain": "Aviation Safety",
        "cat": "Python",
        "tools": ["Python", "Pandas", "Plotly", "Matplotlib"],
        "metric": "23.967",
        "metric_label": "record analizzati",
        "summary": "Data wrangling su dati storici sporchi, costruzione di un safety index per "
                   "operatore su campioni significativi, analisi del trend post 11 settembre e "
                   "mappa coropletica interattiva.",
    },
    {
        "slug": "formula1-2008",
        "dir": "04-Python/01-Formula1-2008-Analytics",
        "emoji": "\U0001F3CE\uFE0F",
        "title": "Formula 1 2008 Analytics",
        "tagline": "Classifiche e KPI piloti in Python puro",
        "domain": "Motorsport",
        "cat": "Python",
        "tools": ["Python", "Standard Library", "File I/O"],
        "metric": "0 librerie",
        "metric_label": "solo standard library",
        "summary": "Motore di calcolo che applica il regolamento punti F1 2008 ai risultati di gara "
                   "per generare classifiche piloti e costruttori, senza Pandas: la logica sotto il "
                   "cofano, scritta a mano.",
    },
    {
        "slug": "consumer-complaints",
        "dir": "01-Excel-Projects/01-Consumer-Complaints",
        "emoji": "\U0001F3E6",
        "title": "Consumer Complaints Analysis",
        "tagline": "Analisi geografica dei reclami e monitoraggio SLA",
        "domain": "Financial Services",
        "cat": "Excel",
        "tools": ["Excel", "Formattazione condizionale", "Statistica"],
        "metric": "3 tab",
        "metric_label": "dataset, geografia, statistica",
        "thumb": "01-Excel-Projects/images/complaints_geographical_insights.png",
        "summary": "Ristrutturazione di un dataset complesso di reclami: calcolo automatico dei "
                   "tempi di gestione, incidenze percentuali per Stato USA con soglie visive e "
                   "identificazione della problematica piu' frequente.",
    },
    {
        "slug": "retail-sales-reporting",
        "dir": "01-Excel-Projects/02-Retail-Sales-Reporting",
        "emoji": "\U0001F460",
        "title": "Retail Sales Analysis",
        "tagline": "Margini, promozioni e stagionalita' in un unico report",
        "domain": "Retail",
        "cat": "Excel",
        "tools": ["Excel", "Power Query", "Pivot", "Slicer"],
        "metric": "MoM / YoY",
        "metric_label": "medie mobili e stagionalita'",
        "thumb": "01-Excel-Projects/images/trendyshoes_dashboard.png",
        "summary": "Sistema di BI costruito interamente su Excel: impatto degli sconti sulla "
                   "marginalita' reale, medie mobili a 3 e 6 mesi per la pianificazione scorte e "
                   "dashboard interattiva con slicer.",
    },
    {
        "slug": "luggnagg-population-study",
        "dir": "01-Excel-Projects/03-Statistical-Simulation",
        "emoji": "\U0001F4C8",
        "title": "Luggnagg Population Study",
        "tagline": "Simulazione demografica e regressione lineare",
        "domain": "Statistics",
        "cat": "Excel",
        "tools": ["Excel", "Statistica", "Regressione"],
        "metric": "250",
        "metric_label": "individui simulati",
        "thumb": "01-Excel-Projects/images/luggnagg_regression_preview.png",
        "summary": "Generazione di un campione sintetico su distribuzione normale, campionamento "
                   "condizionale, intervalli di confidenza, matrice di correlazione e modello di "
                   "regressione con estrapolazione predittiva.",
    },
]

CATEGORIES = ["Tutti", "SQL", "Python", "Power BI", "Tableau", "Excel"]

INTRO = (
    "Il mio percorso nella Data Analytics parte da un luogo diverso dal solito: il campo da "
    "pallavolo. Per 6 anni ho lavorato come allenatore e scoutman in settori giovanili di alto "
    "livello (Vero Volley Monza, PowerVolley Milano), raccogliendo dati in tempo reale e "
    "costruendo fogli gara in Excel per l'analisi post-partita e lo studio degli avversari. La "
    "curiosit\u00e0 andava oltre il richiesto: ogni weekend studiavo per interesse personale gli "
    "scout di tutte le partite pubblicati dalla Lega Serie A Volley."
)
INTRO2 = (
    "Quella parte del lavoro \u2014 raccogliere dati, pulirli e trasformare numeri in decisioni "
    "\u2014 \u00e8 diventata la mia passione, da qui la scelta di specializzarmi con un master in "
    "Data Analytics (ProfessionAI). Raccolgo qui i progetti pratici svolti durante il percorso."
)

STACK = [
    ("Python", "Pandas, NumPy, Scikit-learn, Matplotlib, Plotly, Seaborn"),
    ("SQL", "MySQL, PostgreSQL, join multipli, aggregazione condizionale, pivoting"),
    ("Big Data", "PySpark, Pandas UDF, Apache Arrow, elaborazione distribuita"),
    ("Machine Learning", "Clustering K-Means, PCA, regressione logistica, validazione modelli"),
    ("NLP", "TF-IDF, stopwords, sentiment analysis, text classification"),
    ("Business Intelligence", "Power BI, DAX, Power Query, Tableau, data storytelling"),
    ("Excel avanzato", "Power Query, pivot, slicer, statistica descrittiva, regressione"),
    ("Data Viz", "Dashboard interattive, mappe coropletiche, executive reporting"),
]

# --------------------------------------------------------------------------
# Convertitore Markdown -> HTML (sottoinsieme usato nei README del progetto)
# --------------------------------------------------------------------------

BADGE_RE = re.compile(r"^\s*(!\[[^\]]*\]\(https://img\.shields\.io/[^)]*\)\s*)+$")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ULI_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
OLI_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-") or "sezione"


class MarkdownRenderer:
    """Converte il markdown dei README in HTML, risolvendo le immagini locali."""

    def __init__(self, base_dir, asset_hook):
        self.base_dir = base_dir          # cartella del README (per i path relativi)
        self.asset_hook = asset_hook      # callback: path assoluto -> url nel sito
        self.headings = []                # [(livello, testo, id)]

    # ---- inline -------------------------------------------------------
    def inline(self, text):
        placeholders = []

        def stash(markup):
            placeholders.append(markup)
            return "\x00%d\x00" % (len(placeholders) - 1)

        # 1. code span (protetti da ogni altra trasformazione)
        def code_sub(m):
            return stash("<code>%s</code>" % html.escape(m.group(1)))

        text = CODE_SPAN_RE.sub(code_sub, text)

        # 2. immagini
        def img_sub(m):
            alt, src = m.group(1), m.group(2)
            if src.startswith("http"):
                url = src
            else:
                url = self.asset_hook(os.path.normpath(os.path.join(self.base_dir, src)))
                if url is None:
                    return ""
            return stash('<img src="%s" alt="%s" loading="lazy">'
                         % (html.escape(url, quote=True), html.escape(alt, quote=True)))

        text = IMG_RE.sub(img_sub, text)

        # 3. link
        def link_sub(m):
            label, href = m.group(1), m.group(2)
            ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            return stash('<a href="%s"%s>%s</a>'
                         % (html.escape(href, quote=True), ext, self.inline_lite(label)))

        text = LINK_RE.sub(link_sub, text)

        text = html.escape(text)
        text = BOLD_RE.sub(r"<strong>\1</strong>", text)
        text = ITALIC_RE.sub(r"<em>\1</em>", text)

        for i, markup in enumerate(placeholders):
            text = text.replace("\x00%d\x00" % i, markup)
        return text

    def inline_lite(self, text):
        """Testo dentro un link: niente link annidati."""
        if "\x00" in text:
            return text
        return BOLD_RE.sub(r"<strong>\1</strong>", html.escape(text))

    # ---- blocchi ------------------------------------------------------
    def render(self, md):
        lines = md.split("\n")
        out = []
        stack = []          # liste aperte: {tag, indent, li}
        para = []

        def flush_para():
            if not para:
                return
            text = " ".join(para).strip()
            para.clear()
            if not text:
                return
            cls = ""
            if text.startswith("*(") and text.endswith(")*"):
                cls = ' class="caption"'
            out.append("<p%s>%s</p>" % (cls, self.inline(text)))

        def close_lists(to_indent=-1):
            while stack and stack[-1]["indent"] > to_indent:
                node = stack.pop()
                if node["li"]:
                    out.append("</li>")
                out.append("</%s>" % node["tag"])
                if stack:
                    stack[-1]["li"] = True

        def open_item(indent, tag, content):
            while stack and indent < stack[-1]["indent"]:
                node = stack.pop()
                if node["li"]:
                    out.append("</li>")
                out.append("</%s>" % node["tag"])
            if not stack or indent > stack[-1]["indent"]:
                out.append("<%s>" % tag)
                stack.append({"tag": tag, "indent": indent, "li": False})
            else:
                if stack[-1]["li"]:
                    out.append("</li>")
                    stack[-1]["li"] = False
                if stack[-1]["tag"] != tag:
                    out.append("</%s>" % stack.pop()["tag"])
                    out.append("<%s>" % tag)
                    stack.append({"tag": tag, "indent": indent, "li": False})
            out.append("<li>%s" % self.inline(content))
            stack[-1]["li"] = True

        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            stripped = line.strip()

            # --- code fence
            if stripped.startswith("```"):
                flush_para()
                close_lists()
                lang = stripped[3:].strip() or "text"
                buf = []
                i += 1
                while i < n and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                i += 1
                out.append('<div class="code-block" data-lang="%s"><pre><code>%s</code></pre></div>'
                           % (html.escape(lang, quote=True),
                              html.escape("\n".join(buf))))
                continue

            # --- riga vuota
            if not stripped:
                flush_para()
                i += 1
                continue

            # --- badge shields.io: scartati (sul sito ci sono i chip)
            if BADGE_RE.match(line):
                flush_para()
                i += 1
                continue

            # --- separatore orizzontale
            if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
                flush_para()
                close_lists()
                out.append("<hr>")
                i += 1
                continue

            # --- titolo
            m = HEADING_RE.match(stripped)
            if m:
                flush_para()
                close_lists()
                level = len(m.group(1))
                text = m.group(2).strip()
                hid = slugify(text)
                self.headings.append((level, text, hid))
                out.append('<h%d id="%s">%s</h%d>' % (level, hid, self.inline(text), level))
                i += 1
                continue

            # --- tabella
            if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
                flush_para()
                close_lists()
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    rows.append(lines[i].strip())
                    i += 1
                out.append(self.render_table(rows))
                continue

            # --- elenchi
            m = OLI_RE.match(line)
            if m:
                flush_para()
                open_item(len(m.group(1)), "ol", m.group(3))
                i += 1
                continue
            m = ULI_RE.match(line)
            if m:
                flush_para()
                open_item(len(m.group(1)), "ul", m.group(2))
                i += 1
                continue

            # --- continuazione di una voce di elenco
            if stack and line.startswith("  "):
                out.append(" " + self.inline(stripped))
                i += 1
                continue

            # --- paragrafo
            close_lists()
            para.append(stripped)
            i += 1

        flush_para()
        close_lists()
        return "\n".join(out)

    def render_table(self, rows):
        def cells(row):
            return [c.strip() for c in row.strip().strip("|").split("|")]

        header = cells(rows[0])
        aligns = []
        for spec in cells(rows[1]):
            if spec.startswith(":") and spec.endswith(":"):
                aligns.append("center")
            elif spec.endswith(":"):
                aligns.append("right")
            else:
                aligns.append("left")
        body = [cells(r) for r in rows[2:]]

        def style(idx):
            a = aligns[idx] if idx < len(aligns) else "left"
            return ' style="text-align:%s"' % a if a != "left" else ""

        parts = ['<div class="table-wrap"><table><thead><tr>']
        for idx, cell in enumerate(header):
            parts.append("<th%s>%s</th>" % (style(idx), self.inline(cell)))
        parts.append("</tr></thead><tbody>")
        for row in body:
            parts.append("<tr>")
            for idx, cell in enumerate(row):
                parts.append("<td%s>%s</td>" % (style(idx), self.inline(cell)))
            parts.append("</tr>")
        parts.append("</tbody></table></div>")
        return "".join(parts)


# --------------------------------------------------------------------------
# Gestione asset
# --------------------------------------------------------------------------

copied_assets = {}


def copy_asset(abs_path, prefix=""):
    """Copia un file in docs/assets/img/ e restituisce l'URL relativo alla root del sito."""
    if abs_path in copied_assets:
        return copied_assets[abs_path]
    if not os.path.isfile(abs_path):
        print("  ! immagine mancante: %s" % os.path.relpath(abs_path, ROOT), file=sys.stderr)
        copied_assets[abs_path] = None
        return None
    name = os.path.basename(abs_path).replace(" ", "-")
    if prefix:
        name = "%s-%s" % (prefix, name)
    dest_dir = os.path.join(OUT, "assets", "img")
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(abs_path, os.path.join(dest_dir, name))
    url = "assets/img/" + quote(name)
    copied_assets[abs_path] = url
    return url


def gh_tree(rel_dir):
    return "%s/tree/main/%s" % (REPO_URL, quote(rel_dir))


def gh_blob(rel_path):
    """Pagina di GitHub che mostra il contenuto del file."""
    return "%s/blob/main/%s" % (REPO_URL, quote(rel_path))


def gh_raw(rel_path):
    """URL che scarica il file invece di aprirne la pagina."""
    return "%s/raw/main/%s" % (REPO_URL, quote(rel_path))


# Per notebook e script la pagina di GitHub e' utile: mostra il contenuto.
# Un .pbix invece GitHub non sa visualizzarlo, e la sua pagina sembra vuota:
# per quel formato serve il link che scarica direttamente il file.
ARTIFACTS = (
    (".ipynb", "Apri il notebook", gh_blob),
    (".sql", "Apri lo script SQL", gh_blob),
    (".pbix", "Scarica il file .pbix", gh_raw),
    (".xlsx", "Scarica il file Excel", gh_raw),
    (".xlsm", "Scarica il file Excel", gh_raw),
)


def main_artifact(rel_dir):
    """Individua il file principale del progetto (notebook, script SQL, report Power BI)."""
    abs_dir = os.path.join(ROOT, rel_dir)
    for ext, label, url_for in ARTIFACTS:
        for f in sorted(os.listdir(abs_dir)):
            if f.endswith(ext):
                return label, url_for(os.path.join(rel_dir, f))
    return None


# --------------------------------------------------------------------------
# Template HTML
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Tema chiaro / scuro
# --------------------------------------------------------------------------

# Va eseguito nell'<head>, prima che la pagina venga disegnata: cosi' chi ha
# gia' scelto un tema non vede il lampo del tema sbagliato al caricamento.
THEME_INIT = """<script>
(function () {
  try {
    var t = localStorage.getItem('tema');
    if (t === 'light' || t === 'dark') {
      document.documentElement.setAttribute('data-theme', t);
    }
  } catch (e) { /* localStorage non disponibile: si usa il tema di sistema */ }
})();
</script>"""

# Senza scelta salvata si segue il sistema operativo; il primo clic decide.
THEME_BUTTON = """<button class="theme-toggle" type="button" id="theme-toggle"
        aria-label="Cambia tema chiaro o scuro" title="Cambia tema chiaro o scuro">
        <svg class="icon-sun" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <circle cx="12" cy="12" r="4.2"/>
          <path d="M12 2.4v2.6M12 19v2.6M4.2 4.2l1.9 1.9M17.9 17.9l1.9 1.9M2.4 12h2.6M19 12h2.6M4.2 19.8l1.9-1.9M17.9 6.1l1.9-1.9"/>
        </svg>
        <svg class="icon-moon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path d="M20.5 14.6A8.6 8.6 0 0 1 9.4 3.5a8.6 8.6 0 1 0 11.1 11.1z"/>
        </svg>
      </button>"""

THEME_SCRIPT = """<script>
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;
  var scuroDiSistema = window.matchMedia('(prefers-color-scheme: dark)');

  function temaAttuale() {
    return root.getAttribute('data-theme') || (scuroDiSistema.matches ? 'dark' : 'light');
  }
  function aggiornaEtichetta() {
    var prossimo = temaAttuale() === 'dark' ? 'chiaro' : 'scuro';
    btn.setAttribute('aria-label', 'Passa al tema ' + prossimo);
    btn.setAttribute('title', 'Passa al tema ' + prossimo);
  }

  btn.addEventListener('click', function () {
    var nuovo = temaAttuale() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', nuovo);
    try { localStorage.setItem('tema', nuovo); } catch (e) {}
    aggiornaEtichetta();
  });

  // Se non c'e' una scelta esplicita, si segue il sistema anche a caldo.
  scuroDiSistema.addEventListener('change', function () {
    if (!root.hasAttribute('data-theme')) aggiornaEtichetta();
  });

  aggiornaEtichetta();
})();
</script>"""


def page(title, description, body, depth=0, extra_head="", body_class=""):
    base = "../" * depth
    return """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{author}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{site_url}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="it_IT">
<meta name="twitter:card" content="summary_large_image">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#128202;</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
{theme_init}
{extra_head}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Vai al contenuto</a>
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="{base}index.html">
      <span class="brand-mark">AG</span>
      <span class="brand-text">{author}</span>
    </a>
    <nav class="topnav">
      <a href="{base}index.html#progetti">Progetti</a>
      <a href="{base}index.html#stack">Stack</a>
      <a href="{base}index.html#contatti">Contatti</a>
      <a class="btn btn-ghost" href="{repo}" target="_blank" rel="noopener">GitHub</a>
      {theme_button}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap footer-inner">
    <div>
      <strong>{author}</strong><br>
      <span class="muted">{place}</span>
    </div>
    <div class="footer-links">
      <a href="{linkedin}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="mailto:{email}">{email}</a>
      <a href="{repo}" target="_blank" rel="noopener">Repository</a>
    </div>
  </div>
</footer>
{theme_script}
</body>
</html>
""".format(title=html.escape(title), description=html.escape(description, quote=True),
           author=AUTHOR, place=PLACE, base=base, repo=REPO_URL,
           site_url=SITE_URL, og_image=OG_IMAGE,
           theme_init=THEME_INIT, theme_button=THEME_BUTTON, theme_script=THEME_SCRIPT,
           linkedin=LINKEDIN, email=EMAIL, body=body, extra_head=extra_head,
           body_class=body_class)


def chips(items, cls="chip"):
    return "".join('<span class="%s">%s</span>' % (cls, html.escape(t)) for t in items)


def build_card(p):
    href = "projects/%s.html" % p["slug"]
    if p.get("thumb"):
        url = copy_asset(os.path.join(ROOT, p["thumb"]), prefix=p["slug"])
        media = ('<div class="card-media"><img src="%s" alt="Anteprima di %s" loading="lazy"></div>'
                 % (url, html.escape(p["title"], quote=True))) if url else ""
    else:
        media = ('<div class="card-media card-media--glyph"><span>%s</span></div>' % p["emoji"])

    star = '<span class="star" title="Progetto in evidenza">\u2605</span>' if p.get("featured") else ""
    metric = ""
    if p.get("metric"):
        metric = ('<div class="card-metric"><b>%s</b><span>%s</span></div>'
                  % (html.escape(p["metric"]), html.escape(p["metric_label"])))

    return """
<article class="card" data-cat="{cat}" data-featured="{feat}">
  <a class="card-link" href="{href}">
    {media}
    <div class="card-body">
      <div class="card-top"><span class="domain">{domain}</span>{star}</div>
      <h3>{emoji} {title}</h3>
      <p class="card-tagline">{tagline}</p>
      <p class="card-summary">{summary}</p>
      {metric}
      <div class="chips">{tools}</div>
      <span class="card-cta">Apri il progetto <span aria-hidden="true">&rarr;</span></span>
    </div>
  </a>
</article>""".format(
        cat=html.escape(p["cat"], quote=True), feat="1" if p.get("featured") else "0",
        href=href, media=media, domain=html.escape(p["domain"]), star=star,
        emoji=p["emoji"], title=html.escape(p["title"]),
        tagline=html.escape(p["tagline"]), summary=html.escape(p["summary"]),
        metric=metric, tools=chips(p["tools"]))


def build_index():
    n_python = sum(1 for p in PROJECTS if p["cat"] == "Python")
    n_bi = sum(1 for p in PROJECTS if p["cat"] in ("Power BI", "Tableau"))
    n_excel = sum(1 for p in PROJECTS if p["cat"] == "Excel")

    filters = "".join(
        '<button class="filter%s" data-filter="%s">%s</button>'
        % (" is-active" if c == "Tutti" else "", html.escape(c, quote=True), html.escape(c))
        for c in CATEGORIES
    )
    cards = "\n".join(build_card(p) for p in PROJECTS)
    stack = "".join(
        '<div class="stack-item"><h3>%s</h3><p>%s</p></div>' % (html.escape(k), html.escape(v))
        for k, v in STACK
    )

    body = """
<section class="hero">
  <div class="wrap hero-inner">
    <p class="pill"><span class="dot"></span> Disponibile per un ruolo in ambito Data</p>
    <h1>Dai fogli gara di pallavolo<br><span class="grad">ai dati che guidano le decisioni</span></h1>
    <p class="lead">{intro}</p>
    <p class="lead">{intro2}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#progetti">Guarda gli {total} progetti</a>
      <a class="btn" href="{linkedin}" target="_blank" rel="noopener">LinkedIn</a>
      <a class="btn" href="mailto:{email}">Scrivimi</a>
    </div>
    <dl class="stats">
      <div><dt>{total}</dt><dd>progetti end-to-end</dd></div>
      <div><dt>{n_python}</dt><dd>progetti Python &amp; ML</dd></div>
      <div><dt>{n_bi}</dt><dd>dashboard BI</dd></div>
      <div><dt>{n_excel}</dt><dd>modelli Excel avanzati</dd></div>
    </dl>
  </div>
</section>

<section class="section" id="progetti">
  <div class="wrap">
    <div class="section-head">
      <h2>Progetti</h2>
      <p class="muted">Ogni progetto ha una pagina dedicata con problema di business, dati, approccio e risultati. Le <span class="star">&#9733;</span> segnalano quelli in evidenza.</p>
    </div>
    <div class="filters" role="group" aria-label="Filtra i progetti per strumento">{filters}</div>
    <div class="grid" id="grid">
{cards}
    </div>
    <p class="empty" id="empty" hidden>Nessun progetto per questo filtro.</p>
  </div>
</section>

<section class="section section-alt" id="stack">
  <div class="wrap">
    <div class="section-head"><h2>Competenze tecniche</h2>
    <p class="muted">Strumenti e metodi usati concretamente nei progetti qui sopra.</p></div>
    <div class="stack-grid">{stack}</div>
  </div>
</section>

<section class="section" id="contatti">
  <div class="wrap contact">
    <h2>Parliamone</h2>
    <p class="lead">Cerco un ruolo in ambito Data (Data Analyst, Data Engineer, BI Specialist),
    con la possibilit&agrave; di crescere e specializzarmi nel tempo.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="mailto:{email}">{email}</a>
      <a class="btn" href="{linkedin}" target="_blank" rel="noopener">Profilo LinkedIn</a>
      <a class="btn" href="{repo}" target="_blank" rel="noopener">Codice su GitHub</a>
    </div>
  </div>
</section>

<script>
(function () {{
  var filters = document.querySelectorAll('.filter');
  var cards = document.querySelectorAll('.card');
  var empty = document.getElementById('empty');
  filters.forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var value = btn.dataset.filter;
      filters.forEach(function (b) {{ b.classList.toggle('is-active', b === btn); }});
      var shown = 0;
      cards.forEach(function (card) {{
        var match = value === 'Tutti' || card.dataset.cat === value;
        card.hidden = !match;
        if (match) shown++;
      }});
      empty.hidden = shown > 0;
    }});
  }});
}})();
</script>
""".format(intro=html.escape(INTRO), intro2=html.escape(INTRO2), total=len(PROJECTS),
           n_python=n_python, n_bi=n_bi, n_excel=n_excel, linkedin=LINKEDIN, email=EMAIL,
           filters=filters, cards=cards, stack=stack, repo=REPO_URL)

    description = ("Portfolio di %s: %d progetti end-to-end su SQL, Python, Machine Learning, "
                   "NLP, PySpark, Power BI, Tableau ed Excel." % (AUTHOR, len(PROJECTS)))
    return page("%s \u2014 Data Analytics Portfolio" % AUTHOR, description, body,
                depth=0, body_class="home")


def clean_readme(md):
    """Rimuove titolo H1, badge e sezione Autore: sul sito sono gia' nel layout."""
    lines = md.split("\n")
    # via il primo H1
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            lines = lines[idx + 1:]
            break
    # via la sezione finale "Autore"
    for idx, line in enumerate(lines):
        if re.match(r"^##+\s+.*Autore", line):
            lines = lines[:idx]
            break
    # via i separatori finali orfani
    while lines and (not lines[-1].strip() or re.fullmatch(r"-{3,}", lines[-1].strip())):
        lines.pop()
    return "\n".join(lines)


def build_project(p, prev_p, next_p):
    rel_dir = p["dir"]
    readme = os.path.join(ROOT, rel_dir, "README.md")
    with open(readme, encoding="utf-8") as fh:
        md = clean_readme(fh.read())

    def asset_hook(path):
        url = copy_asset(path, prefix=p["slug"])
        return "../" + url if url else None

    renderer = MarkdownRenderer(base_dir=os.path.join(ROOT, rel_dir), asset_hook=asset_hook)
    content = renderer.render(md)

    toc_items = "".join(
        '<a href="#%s">%s</a>' % (hid, html.escape(text))
        for level, text, hid in renderer.headings if level == 2
    )
    toc = ('<aside class="toc"><p class="toc-title">In questa pagina</p><nav>%s</nav></aside>'
           % toc_items) if toc_items else ""

    actions = ['<a class="btn btn-primary" href="%s" target="_blank" rel="noopener">Vedi la cartella su GitHub</a>'
               % gh_tree(rel_dir)]
    artifact = main_artifact(rel_dir)
    if artifact:
        actions.append('<a class="btn" href="%s" target="_blank" rel="noopener">%s</a>'
                       % (artifact[1], html.escape(artifact[0])))
    if p.get("live"):
        actions.append('<a class="btn btn-accent" href="%s" target="_blank" rel="noopener">%s</a>'
                       % (p["live"][1], html.escape(p["live"][0])))

    nav = []
    if prev_p:
        nav.append('<a class="pager prev" href="%s.html"><span>Progetto precedente</span><b>%s</b></a>'
                   % (prev_p["slug"], html.escape(prev_p["title"])))
    if next_p:
        nav.append('<a class="pager next" href="%s.html"><span>Progetto successivo</span><b>%s</b></a>'
                   % (next_p["slug"], html.escape(next_p["title"])))

    metric = ""
    if p.get("metric"):
        metric = ('<div class="head-metric"><b>%s</b><span>%s</span></div>'
                  % (html.escape(p["metric"]), html.escape(p["metric_label"])))

    body = """
<section class="project-head">
  <div class="wrap">
    <a class="back" href="../index.html#progetti"><span aria-hidden="true">&larr;</span> Tutti i progetti</a>
    <span class="domain">{domain}</span>
    <h1>{emoji} {title}</h1>
    <p class="lead">{tagline}</p>
    <div class="chips">{tools}</div>
    {metric}
    <div class="hero-actions">{actions}</div>
  </div>
</section>
<div class="wrap project-layout">
  {toc}
  <article class="prose">
{content}
  </article>
</div>
<div class="wrap pager-row">{nav}</div>
""".format(domain=html.escape(p["domain"]), emoji=p["emoji"], title=html.escape(p["title"]),
           tagline=html.escape(p["tagline"]), tools=chips(p["tools"]), metric=metric,
           actions="".join(actions), toc=toc, content=content, nav="".join(nav))

    return page("%s \u2014 %s" % (p["title"], AUTHOR), p["summary"], body,
                depth=1, body_class="project")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

    shutil.copy2(os.path.join(SITE, "style.css"), os.path.join(OUT, "assets", "style.css"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    for i, p in enumerate(PROJECTS):
        prev_p = PROJECTS[i - 1] if i > 0 else None
        next_p = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None
        target = os.path.join(OUT, "projects", "%s.html" % p["slug"])
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(build_project(p, prev_p, next_p))
        print("  pagina  docs/projects/%s.html" % p["slug"])

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_index())
    print("  pagina  docs/index.html")
    print("\nSito generato in docs/ (%d progetti)." % len(PROJECTS))


if __name__ == "__main__":
    main()
