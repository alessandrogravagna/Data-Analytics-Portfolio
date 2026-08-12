# ₿ Bitcoin Sentiment & Social Engagement Analytics with PySpark

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-Big_Data_Analytics-E25A1C?style=flat&logo=apachespark&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Sentiment_Analysis-green?style=flat)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto di Big Data Analytics sviluppato per la società di ricerche di mercato **MarketPulse Analytics**. L'obiettivo è stimare il consenso pubblico e il sentiment degli utenti nei confronti del Bitcoin elaborando e analizzando milioni di tweet raccolti nel tempo.

Sfruttando la potenza di calcolo distribuito di **PySpark** su architettura Cloud (Google Colab), la pipeline pulisce il testo, filtra la lingua inglese tramite Pandas UDF, classifica il sentiment giornaliero (positivo, negativo, neutro) tramite TextBlob, misura le metriche di engagement degli utenti (*likes* e *replies*) ed esplora la correlazione con lo storico dei prezzi di mercato del Bitcoin (BTC/USD).

---

## 💡 Valore Aggiunto Aziendale
* **Monitoraggio del Consenso in Tempo Reale:** Tracciamento della percezione pubblica sul Bitcoin per guidare le scelte di investitori e professionisti finanziari.
* **Engagement Behavior Analysis:** Comprensione delle dinamiche social, valutando se i messaggi con tono negativo generano maggiore attenzione (*likes*) o discussioni più accese (*replies*).
* **Correlation Insights:** Analisi empirica della relazione tra la frequenza dei tweet (positivi/negativi) e le quotazioni di chiusura di BTC/USD per individuare eventuali pattern di mercato.

---

## ⚙️ Pipeline Big Data & Metodologia

1. **Configurazione dell'Ambiente PySpark:**
   * Inizializzazione di una `SparkSession` ottimizzata con l'attivazione di **Apache Arrow** (`spark.execution.arrow.pyspark.enabled`) e tuning delle partizioni di shuffle.
2. **Data Ingestion & Data Cleaning:**
   * Download e lettura di due dataset: tweet su Bitcoin e storico prezzi BTC/USD.
   * Filtro sui timestamp validi, cast dei campi numerici e pulizia avanzata del testo con Regex (rimozione URL, entità HTML e caratteri speciali).
   * Rilevamento della lingua tramite **Pandas UDF** (`langdetect`) per mantenere solo i tweet in inglese, memorizzando il risultato in cache RAM.
3. **Sentiment Analysis con TextBlob:**
   * Applicazione vettorizzata di **TextBlob** tramite Pandas UDF per la polarità del testo, classificando ogni tweet come `positivo` (polarità > 0), `negativo` (polarità < 0) o `neutro` (polarità = 0).
4. **Analisi dell'Engagement (Likes vs Replies):**
   * Calcolo della media delle interazioni (`likes_num` e `replies_num`) filtrate per ogni categoria di sentiment.
5. **Join Temporale & Calcolo della Correlazione:**
   * Aggregazione giornaliera (*Pivot*) dei volumi di tweet per ciascun sentiment.
   * Inner Join con lo storico prezzi del Bitcoin basato sulla data (`data_pulita`).
   * Calcolo dell'indice di correlazione di Pearson tra tweet positivi/negativi e il prezzo di chiusura (*Close*).
6. **Data Visualization:**
   * Generazione di grafici temporali a linee con Seaborn e Matplotlib (trend storico globale su scala logaritmica e focus lineare sul 2019).

---

## 📊 Risultati ed Insight Principali

* **Engagement sui Social Media:**
  * **Likes:** I tweet con sentiment **negativo** ricevono una media di like leggermente superiore (**8.62**) rispetto a quelli positivi (**8.28**) e neutri (**7.85**).
  * **Replies (Discussioni):** I tweet **positivi** generano in media più risposte (**1.11**) rispetto a quelli negativi (**0.91**), dimostrando che i messaggi positivi stimolano maggiormente l'interazione diretta e il dibattito.
* **Correlazione tra Sentiment e Prezzo BTC/USD:**
  * Il calcolo dell'indice di correlazione di Pearson tra i tweet giornalieri e il prezzo di chiusura del Bitcoin restituisce un valore prossimo a zero (~**0.01** sia per i tweet positivi che per i negativi).
  * **Conclusione:** Non emerge una correlazione lineare diretta tra il volume giornaliero di tweet e il prezzo del Bitcoin. Le variazioni di prezzo sono guidate da dinamiche macroeconomiche e finanziarie più complesse rispetto al solo volume di post sui social.

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
    .appName("MarketPulse_Bitcoin_Sentiment") \
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
## 🧰 Competenze Tecniche Utilizzate

* **Big Data Processing:**
  * PySpark SQL & PySpark DataFrames
  * Apache Arrow Integration & Spark Caching
  * Distributed Execution su Google Colab
* **Natural Language Processing (NLP) & Feature Engineering:**
  * Text Cleaning con Regex
  * Language Detection con `langdetect`
  * Sentiment Analysis & Polarity Scoring con `TextBlob`
* **High-Performance Execution:**
  * Optimised Pandas UDFs (`pyspark.sql.functions.pandas_udf`) per elaborazioni vettorizzate veloci
* **Data Integration & Statistical Analysis:**
  * Reshaping temporale (Pivot)
  * Inner Join di dataset eterogenei (Tweet Data + BTC/USD Financial Price Data)
  * Calcolo della Correlazione di Pearson (`stat.corr`)
* **Data Visualization:**
  * Matplotlib e Seaborn per la creazione di subplot temporali (scala logaritmica e lineare)

---

## 🚀 Come Eseguire il Progetto

1. Apri **Google Colab** e carica il notebook `Bitcoin_Sentiment_Analysis_PySpark.ipynb`.
2. Esegui la prima cella per installare le dipendenze Big Data (`pyspark`, `langdetect`, `pyarrow`).
3. Esegui le celle in sequenza: il codice scaricherà automaticamente i dataset dei tweet e dello storico prezzi BTC/USD.
4. Consulta i dataframe aggregati, la tabella di engagement e i grafici temporali del sentiment generati.

---

## 👤 Autore

**Alessandro Gravagna**  
*Junior Data Analyst | Monza (MB), Italia*
