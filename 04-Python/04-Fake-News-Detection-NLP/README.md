# 📰 Fake News Detection & Threat Analysis Engine for US Government

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-TF--IDF_%26_Text_Processing-green?style=flat)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Classification-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto sviluppato per una divisione speciale del **Governo degli Stati Uniti** focalizzata sulla prevenzione e mitigazione della disinformazione digitale. L'obiettivo strategico è realizzare un motore di **Natural Language Processing (NLP)** e **Machine Learning** in grado di classificare in tempo reale se un articolo di notizia è reale o falso (*Fake vs True News*).

Il modello finale è stato ottimizzato e serializzato in formato `.pkl` per consentirne l'integrazione immediata da parte del team dev all'interno di un'**estensione browser per Google Chrome**, fornendo agli utenti un feedback istantaneo sulla veridicità delle notizie lette online.

---

## 💡 Valore Aggiunto Aziendale e Sociale
* **Riduzione della Disinformazione:** Identificazione tempestiva di articoli inaffidabili e protezione degli utenti da contenuti ingannevoli.
* **Supporto Decisionale ed Istituzionale:** Analisi dei trend e identificazione prioritaria dei temi maggiormente soggetti a manipolazione informativa (es. politica e notizie governative).
* **Integrazione MLOps End-to-End:** Esportazione dell'intera pipeline (`TF-IDF + Logistic Regression`) tramite serializzazione `pickle` pronta per il deployment in ambiente produzione/web extension.

---

## ⚙️ Pipeline NLP e Metodologia di Modellazione

1. **Analisi Esplorativa dei Dati (EDA):**
   * Unione dei dataset ufficiali *True* (21.417 articoli) e *Fake* (23.481 articoli) con bilanciamento del target (`is_fake`: 0 per vere, 1 per fake).
   * Analisi delle distribuzioni per categoria (`subject`) per individuare quali temi sono più esposti alla disinformazione.
   * Feature Extraction dai titoli (*Title Length*, *Uppercase Letter Count*, *Exclamation Marks*).
2. **Preprocessing e Pulizia del Testo:**
   * Normalizzazione in minuscolo e rimozione della punteggiatura/caratteri speciali tramite espressioni regolari (`re`).
   * Eliminazione delle Stopwords inglesi tramite la libreria `nltk` per ridurre il rumore semantico.
3. **Feature Engineering Ibrido (Testo + Struttura):**
   * Vettorizzazione del testo dei titoli tramite **TF-IDF Vectorizer** (limitato a 5.000 unigrammi/bigrammi più rilevanti).
   * Combinazione della matrice sparsa TF-IDF con le metriche numeriche strutturali dei titoli tramite `scipy.sparse.hstack`.
4. **Modellazione e Validazione:**
   * Divisione del dataset in Training Set (80%) e Test Set (20%) stratificato.
   * Addestramento del classificatore di **Regressione Logistica** (`LogisticRegression`).
   * Valutazione delle performance sul test set mediante **Accuracy, Precision, Recall, F1-Score** e **Matrice di Confusione**.
5. **Esportazione per il Plug-in Chrome:**
   * Serializzazione del modello addestrato e del vettorizzatore TF-IDF in file `.pkl`.

---

## 📊 Key Insights e Risultati Analitici

* **Pattern Stilistici dei Titoli (Clickbait):**
  * I titoli delle **Fake News** sono sensibilmente più lunghi (media di **94.2 caratteri** contro i **64.7** delle notizie vere).
  * Le Fake News mostrano un uso massiccio di maiuscole nel titolo (media di **27.8 lettere maiuscole** contro **3.55**) e una frequenza nettamente superiore di punti esclamativi.
* **Analisi dei Temi:**
  * I temi maggiormente soggetti a Fake News risultano essere *News Generali*, *Politica* e *Left News*.
  * Le categorie *politicsNews* e *worldnews* contengono esclusivamente notizie verificate.
* **Performance del Modello:**
  * **Accuracy Globale:** **99%** sul test set di 8.980 articoli.
  * **Precision & Recall:** 0.99 sia per la classe Notizie Vere che per le Fake News, riducendo al minimo il rischio di falsi positivi (falsa censura).

---

## 💻 Codice Principale (Core Logic)

```python
import scipy.sparse as sp
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# 1. Vettorizzazione TF-IDF dei titoli puliti
tfidf = TfidfVectorizer(max_features=5000)
X_tfidf = tfidf.fit_transform(df['title_clean'])

# 2. Estrazione e Unione delle Feature Strutturali (Lunghezza, Maiuscole, Esclamativi)
X_numeric = df[['title_len', 'title_uppercase', 'title_exclamations']].values
X = sp.hstack((X_tfidf, X_numeric), format='csr')
y = df['is_fake'].values

# 3. Train/Test Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Addestramento Classificatore
modello = LogisticRegression(max_iter=1000)
modello.fit(X_train, y_train)

# 5. Valutazione
y_pred = modello.predict(X_test)
print(classification_report(y_test, y_pred))

# 6. Esportazione Modello e Vettorizzatore per Plug-in Chrome
with open('fake_news_model.pkl', 'wb') as f:
    pickle.dump(modello, f)

with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
```
## 🧰 Competenze Tecniche Utilizzate

* **Natural Language Processing (NLP):**
  * NLTK Stopwords Removal
  * Regular Expressions (`re`)
  * TF-IDF Vectorization
  * Text Cleaning
* **Feature Engineering:**
  * Combinazione di matrici sparse PNV (NLP) e variabili dense numeriche tramite SciPy
* **Supervised Machine Learning:**
  * Classification con `LogisticRegression`
  * Train/Test Split con stratificazione
* **Model Evaluation & MLOps:**
  * Precision, Recall, F1-Score, Confusion Matrix
  * Model Serialization con `pickle`
* **Data Visualization:**
  * Seaborn Countplots e Cross-Tabulation per l'analisi dei temi e delle metriche stilistiche

---

## 🚀 Come Eseguire il Progetto

1. Clona la repository o scarica la cartella `04-Fake-News-Detection-NLP`.
2. Assicurati di avere installato le librerie necessarie (`pandas`, `scikit-learn`, `nltk`, `seaborn`, `scipy`).
3. Apri ed esegui il notebook `Fake_News_Detection_NLP.ipynb` su Google Colab o Jupyter Notebook.
4. I file `fake_news_model.pkl` e `tfidf_vectorizer.pkl` verranno generati nella directory di lavoro, pronti per l'integrazione nell'estensione Chrome.

---

## 👤 Autore

**Alessandro Gravagna**  
*Junior Data Analyst | Monza (MB), Italia*
