# ✈️ Aviation Accidents Analytics & Historical Safety Engine (1919 - 2023)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Wrangling-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Geo_Analytics-3F4F75?style=flat&logo=plotly&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Data_Viz-11557c?style=flat&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto realizzato durante il **Master in Data Analytics di ProfessionAI**, come capstone del modulo su Pandas e Data Visualization. Lo scenario di business — un'organizzazione internazionale per la sicurezza aerea — è uno scenario simulato ideato per applicare le tecniche in un contesto realistico.

L'analisi elabora un dataset di **23.967 record** di incidenti aerei registrati a livello globale tra il 1919 e il 2023, applicando pipeline di data wrangling, feature engineering e geo-analytics per isolare pattern di rischio, valutare la sicurezza degli operatori commerciali/militari e tracciare la curva di sicurezza aeronavale prima e dopo l'11 settembre 2001.

**Dataset:** Fornito dal materiale didattico del Master in Data Analytics di ProfessionAI.

---

## 💡 Cosa dimostra questo progetto
* **Data cleaning avanzato di dati storici:** trattamento dinamico di stringhe complesse nella colonna `fatalities` tramite parsing condizionale, estrazione regex degli anni e normalizzazione dei valori mancanti/ignoti.
* **Indice di sicurezza operatori (Safety Index):** normalizzazione del rapporto di mortalità per singolo incidente, applicata a operatori con un campione statisticamente significativo (almeno 20 incidenti).
* **Analisi temporale & milestone 9/11:** monitoraggio del trend annuale degli incidenti nel periodo 1990–2023 con evidenza visiva dell'impatto delle normative di sicurezza introdotte dopo il 2001.
* **Choropleth geo-analytics:** mappatura geospaziale interattiva mediante Plotly Express con allineamento ISO dei nomi geografici (es. Russian Federation, United States, D.R. Congo).

---

## 📊 Insight e Risultati Chiave dell'Analisi

* **Geografia del rischio:** Stati Uniti e Russia guidano la classifica globale per volume assoluto di incidenti storici, riflettendo la densità di traffico aereo e flotte operative gestite nell'ultimo secolo.
* **Distribuzione settimanale:** il giorno con più incidenti registrati è il venerdì (3.563 eventi), seguito dal giovedì (3.382), mentre la domenica risulta il giorno più tranquillo (2.656).
* **Operatori più sicuri (almeno 20 incidenti):**
  1. Southwest Airlines: 0,0769 morti/incidente (26 incidenti, 2 decessi).
  2. ZUA: 0,1250 morti/incidente (32 incidenti, 4 decessi).
* **Velivoli a maggiore impatto:** il Douglas C-47A (DC-3) è il velivolo con il maggior numero cumulativo di fatalità storiche (5.770 decessi), seguito dalle varianti Douglas C-47 (2.636) e Douglas C-47B (1.992).

---

## 💻 Codice Principale (Core Logic)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# 1. Cleaning della colonna fatalities tramite eval() e parsing temporale
def pulisci_morti(valore):
    if pd.isna(valore): return 0
    try: return eval(str(valore))
    except: return np.nan

df['fatalities'] = df['fatalities'].apply(pulisci_morti)
df['fatalities'] = pd.to_numeric(df['fatalities'], errors='coerce').fillna(0)

df['year_extracted'] = pd.to_numeric(df['date'].str.extract(r'(\d{4})')[0], errors='coerce')
df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')

# Rimozione record non definiti
df = df[df['operator'].str.lower() != 'unknown']
df = df[~df['country'].str.lower().str.contains('unknown', na=False)]

# 2. Ranking Operatori più Sicuri (minimo 20 incidenti)
analisi_operatori = df.groupby('operator').agg(
    totale_incidenti=('date', 'count'),
    totale_morti=('fatalities', 'sum')
)
op_rilevanti = analisi_operatori[analisi_operatori['totale_incidenti'] >= 20].copy()
op_rilevanti['morti_per_incidente'] = op_rilevanti['totale_morti'] / op_rilevanti['totale_incidenti']
operatori_sicuri = op_rilevanti.sort_values('morti_per_incidente', ascending=True)

# 3. Geo-Analytics Interattiva con Plotly
dati_mappa = df['country'].value_counts().reset_index()
dati_mappa.columns = ['nazione', 'incidenti']

mappa_correzioni = {
    'USA': 'United States',
    'U.K.': 'United Kingdom',
    'Russia': 'Russian Federation',
    'S. Africa': 'South Africa',
    'Korea, South': 'South Korea',
    'Korea, North': 'North Korea',
    'Democratic Republic of Congo': 'Democratic Republic of the Congo'
}
dati_mappa['nazione'] = dati_mappa['nazione'].replace(mappa_correzioni)

fig = px.choropleth(
    dati_mappa,
    locations="nazione",
    locationmode="country names",
    color="incidenti",
    title="Mappa Globale degli Incidenti Aerei per Nazione",
    color_continuous_scale="Reds"
)
```

---

## 🧰 Competenze Tecniche Utilizzate
- **Data Cleansing & Wrangling:** uso di Pandas per la manipolazione di tipi dato eterogenei, valutazioni condizionali dinamiche (`eval()`) ed estrazioni con espressioni regolari.
- **Statistical Analysis & Filtering:** aggregazioni di gruppo, calcolo di indici di mortalità ponderati e filtri su campioni statisticamente significativi.
- **Data Visualization:** bar chart con gradienti cromatici personalizzati in Matplotlib e mappe coropletiche geografiche interattive con Plotly Express.

---

## 🚀 Come Eseguire il Progetto
1. Clona il repository o scarica la cartella `02-Aviation-Accidents-Analytics`.
2. Apri il notebook `Incidenti_aerei.ipynb` su Google Colab o Jupyter Notebook.
3. Assicurati che l'URL del dataset o il file `aviation-accidents.csv` sia raggiungibile.
4. Esegui le celle per riprodurre le analisi statistiche e la mappa interattiva.

---

## 👤 Autore
**Alessandro Gravagna**
Monza (MB), Italia
