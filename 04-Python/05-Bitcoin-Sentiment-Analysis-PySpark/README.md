# ₿ Bitcoin Sentiment & Social Engagement Analytics with PySpark

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-Big_Data_Analytics-E25A1C?style=flat&logo=apachespark&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Sentiment_Analysis-green?style=flat)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto di Big Data Analytics realizzato durante il **Master in Data Analytics di ProfessionAI**, come capstone del modulo su Big Data e PySpark. Lo scenario di business — una società di ricerche di mercato che monitora il sentiment sul Bitcoin — è uno scenario simulato ideato per applicare le tecniche in un contesto realistico.

L'obiettivo è stimare il consenso pubblico e il sentiment degli utenti nei confronti del Bitcoin elaborando milioni di tweet raccolti nel tempo, sfruttando la potenza di calcolo distribuito di PySpark su Google Colab. La pipeline pulisce il testo, filtra la lingua inglese, classifica il sentiment giornaliero (positivo, negativo, neutro) tramite TextBlob, misura le metriche di engagement degli utenti (likes e replies) ed esplora la correlazione con lo storico dei prezzi di mercato del Bitcoin (BTC/USD).

**Dataset:** TODO-inserisci-fonte-dataset (es. Kaggle, materiale del corso)

---

## 💡 Cosa dimostra questo progetto
* **Elaborazione distribuita su larga scala**, non solo su un singolo notebook Pandas.
* **Sentiment analysis vettorizzata** con Pandas UDF per performance su grandi volumi.
* **Analisi critica dei risultati**: il progetto non si limita a mostrare correlazioni, ma le interpreta correttamente quando risultano deboli o assenti.

---

## ⚙️ Pipeline Big Data & Metodologia

1. **Configurazione dell'Ambiente PySpark:** inizializzazione di una SparkSession con Apache Arrow attivato e tuning delle partizioni di shuffle.
2. **Data Ingestion & Data Cleaning:** lettura di due dataset (tweet su Bitcoin e storico prezzi BTC/USD), filtro sui timestamp validi, cast dei campi numerici e pulizia del testo con regex (rimozione URL, entità HTML, caratteri speciali).
3. **Rilevamento della lingua** tramite Pandas UDF (`langdetect`) per mantenere solo i tweet in inglese.
4. **Sentiment Analysis con TextBlob:** applicazione vettorizzata tramite Pandas UDF per la polarità del testo, classificando ogni tweet come positivo, negativo o neutro.
5. **Analisi dell'Engagement:** calcolo della media di likes e replies per ogni categoria di sentiment.
6. **Join Temporale & Correlazione:** aggregazione giornaliera dei volumi di tweet per sentiment, join con lo storico prezzi Bitcoin, calcolo della correlazione di Pearson tra tweet positivi/negativi e prezzo di chiusura.
7. **Data Visualization:** grafici temporali con Seaborn e Matplotlib (scala logaritmica sul trend storico, focus lineare sul 2019).

---

## 📊 Risultati ed Insight Principali

* **Engagement sui social media:** i tweet con sentiment negativo ricevono in media più like (8,62) rispetto a quelli positivi (8,28) e neutri (7,85). I tweet positivi generano invece più risposte in media (1,11) rispetto ai negativi (0,91), a indicare che i messaggi positivi stimolano più interazione diretta.
* **Correlazione tra sentiment e prezzo BTC/USD:** l'indice di correlazione di Pearson tra i tweet giornalieri e il prezzo di chiusura del Bitcoin risulta prossimo a zero (circa 0,01 sia per i tweet positivi che per i negativi).
* **Conclusione:** non emerge una correlazione lineare diretta tra il volume giornaliero di tweet e il prezzo del Bitcoin. Le variazioni di prezzo sono guidate da dinamiche macroeconomiche e finanziarie più complesse rispetto al solo volume di post sui social.

---

## 💻 Codice Principale (Core Logic in PySpark)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, avg, count, pandas_udf
from pyspark.sql.types import StringType
import pandas as pd
from textblob import TextBlob

# 1. Inizializzazione Sessione PySpark
spark = SparkSession.builder \
    .appName("Bitcoin_Sentiment_Analysis") \
    .config("spark.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

# 2. Pandas UDF per Sentiment Analysis Vettorizzata
@pandas_udf(StringType())
def sentiment_pandas_udf(texts: pd.Series) -> pd.Series:
    def get_sentiment(text):
        if not text: return "neutro"
        pol = TextBlob(str(text)).sentiment.polarity
        return "positivo" if pol > 0 else ("negativo" if pol < 0 else "neutro")
    return texts.apply(get_sentiment)

df_con_sentiment = df_pulito.withColumn("sentiment", sentiment_pandas_udf(col("testo_pulito"))).cache()

# 3. Analisi dell'Engagement Medio
df_engagement = df_con_sentiment.groupBy("sentiment").agg(
    avg("likes_num").alias("media_likes"),
    avg("replies_num").alias("media_risposte")
)
df_engagement.show()

# 4. Calcolo della Correlazione di Pearson con il Prezzo BTC
corr_positivi = df_output_correlazione.stat.corr("tweet_positivi", "Close")
corr_negativi = df_output_correlazione.stat.corr("tweet_negativi", "Close")
```

---

## 🧰 Competenze Tecniche Utilizzate
- **Big Data Processing:** PySpark SQL & DataFrames, integrazione Apache Arrow, caching, esecuzione distribuita su Google Colab.
- **Natural Language Processing & Feature Engineering:** text cleaning con regex, language detection con `langdetect`, sentiment analysis con TextBlob.
- **High-Performance Execution:** Pandas UDF ottimizzate per elaborazioni vettorizzate.
- **Data Integration & Statistical Analysis:** pivot temporale, join di dataset eterogenei, correlazione di Pearson.
- **Data Visualization:** Matplotlib e Seaborn per subplot temporali (scala logaritmica e lineare).

---

## 🚀 Come Eseguire il Progetto
1. Apri Google Colab e carica il notebook `Bitcoin_Sentiment_Analysis_PySpark.ipynb`.
2. Esegui la prima cella per installare le dipendenze Big Data (`pyspark`, `langdetect`, `pyarrow`).
3. Esegui le celle in sequenza: il codice scaricherà automaticamente i dataset dei tweet e dello storico prezzi BTC/USD.
4. Consulta i dataframe aggregati, la tabella di engagement e i grafici temporali del sentiment generati.

---

## 👤 Autore
**Alessandro Gravagna**
*Junior Data Analyst* | Monza (MB), Italia
