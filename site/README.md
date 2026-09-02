# Generatore del sito

Questa cartella contiene tutto il necessario per costruire il sito pubblicato su
GitHub Pages. **Il contenuto delle pagine dei progetti non si scrive qui**: viene
letto direttamente dai `README.md` di ciascun progetto, che restano l'unica fonte
di verità.

| File | A cosa serve |
| :--- | :--- |
| `build.py` | Legge i README, li converte in HTML e genera il sito dentro `docs/`. Solo libreria standard di Python, nessuna dipendenza da installare. |
| `style.css` | Foglio di stile unico del sito (viene copiato in `docs/assets/style.css`). |

## Rigenerare il sito

```bash
python3 site/build.py
```

Il comando ricrea da zero la cartella `docs/`. Dopo averlo eseguito basta fare
commit di `docs/`.

> Se modifichi un README direttamente da GitHub e non lanci lo script, ci pensa
> comunque la GitHub Action `.github/workflows/build-site.yml`: rigenera `docs/`
> e committa il risultato automaticamente.

## Vedere il sito in locale

```bash
python3 -m http.server 4321 --directory docs
```

Poi apri <http://localhost:4321>.

## Aggiungere un nuovo progetto

1. Crea la cartella del progetto con dentro il suo `README.md`.
2. Apri `site/build.py` e aggiungi una voce alla lista `PROJECTS`:

```python
{
    "slug": "nome-nell-url",              # -> docs/projects/nome-nell-url.html
    "dir": "04-Python/06-Nuovo-Progetto", # cartella che contiene il README
    "emoji": "\U0001F4C8",
    "title": "Titolo del progetto",
    "tagline": "Una riga che dice perche' vale la pena guardarlo",
    "domain": "Retail",                   # etichetta mostrata sulla card
    "cat": "Python",                      # filtro: SQL | Python | Power BI | Tableau | Excel
    "tools": ["Python", "Pandas"],
    "featured": True,                     # opzionale: mette la stella
    "metric": "99%",                      # opzionale: numero in evidenza
    "metric_label": "accuracy sul test set",
    "thumb": "cartella/images/preview.png",  # opzionale: anteprima sulla card
    "summary": "Due o tre righe di sintesi.",
},
```

3. Rilancia `python3 site/build.py`.

Il file principale del progetto (`.ipynb`, `.sql` o `.pbix`) viene individuato da
solo e linkato in cima alla pagina.
