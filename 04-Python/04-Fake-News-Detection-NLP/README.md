# 📰 Fake News Detection & Text Classification Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-TF--IDF_%26_Text_Processing-green?style=flat)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Classification-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto realizzato durante il **Master in Data Analytics di ProfessionAI**, come capstone del modulo su Natural Language Processing. Lo scenario di business — un motore di classificazione integrabile in un'estensione browser — è uno scenario simulato ideato per applicare le tecniche in un contesto realistico.

L'obiettivo è realizzare un modello di NLP e Machine Learning in grado di classificare se un articolo di notizia è reale o falso (fake vs true news), a partire dal titolo. Il modello finale è stato serializzato in formato `.pkl` per un ipotetico utilizzo in un'estensione browser che dia un feedback immediato sull'affidabilità della fonte.

**Dataset:** Fornito dal materiale didattico del Master in Data Analytics di ProfessionAI.

---

## 💡 Cosa dimostra questo progetto
* **Riconoscimento di pattern stilistici legati alla disinformazione**, non solo classificazione a scatola chiusa.
* **Feature engineering ibrido**, combinando testo e metriche numeriche strutturali.
* **Pipeline riproducibile ed esportabile**, dal training alla serializzazione del modello.

---

## ⚙️ Pipeline NLP e Metodologia di Modellazione

1. **Analisi Esplorativa dei Dati (EDA):**
   - Unione dei dataset True e Fake con bilanciamento del target (`is_fake`: 0 per vere, 1 per fake).
   - Analisi delle distribuzioni per categoria (`subject`) per individuare quali temi sono più esposti alla disinformazione.
   - Feature extraction dai titoli (lunghezza, conteggio lettere maiuscole, punti esclamativi).
2. **Preprocessing e Pulizia del Testo:**
   - Normalizzazione in minuscolo e rimozione della punteggiatura/caratteri speciali tramite espressioni regolari.
   - Eliminazione delle stopwords inglesi tramite la libreria `nltk`.
3. **Feature Engineering Ibrido (Testo + Struttura):**
   - Vettorizzazione del testo dei titoli tramite TF-IDF Vectorizer (limitato a 5.000 unigrammi/bigrammi più rilevanti).
   - Combinazione della matrice sparsa TF-IDF con le metriche numeriche strutturali dei titoli tramite `scipy.sparse.hstack`.
4. **Modellazione e Validazione:**
   - Divisione del dataset in training set (80%) e test set (20%) stratificato.
   - Addestramento di un classificatore di Regressione Logistica.
   - Valutazione delle performance tramite accuracy, precision, recall, F1-score e matrice di confusione.
5. **Esportazione del Modello:**
   - Serializzazione del modello addestrato e del vettorizzatore TF-IDF in file `.pkl`.

---

## 📊 Key Insights e Risultati Analitici

* **Pattern stilistici dei titoli (clickbait):** i titoli delle fake news sono sensibilmente più lunghi (media di 94,2 caratteri contro 64,7 delle notizie vere) e mostrano un uso massiccio di maiuscole (27,8 lettere maiuscole medie contro 3,55) e più punti esclamativi.
* **Analisi dei temi:** i temi maggiormente soggetti a fake news risultano essere News Generali, Politica e Left News. Le categorie politicsNews e worldnews contengono esclusivamente notizie verificate.
* **Performance del modello:** accuracy globale del 99% sul test set di 8.980 articoli, con precision e recall di 0,99 per entrambe le classi.

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

# 6. Esportazione Modello e Vettorizzatore
with open('fake_news_model.pkl', 'wb') as f:
    pickle.dump(modello, f)

with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
```

---

## 🧰 Competenze Tecniche Utilizzate
- **Natural Language Processing:** rimozione stopwords con NLTK, espressioni regolari, TF-IDF vectorization, text cleaning.
- **Feature Engineering:** combinazione di matrici sparse (NLP) e variabili numeriche dense tramite SciPy.
- **Supervised Machine Learning:** classificazione con Regressione Logistica, train/test split stratificato.
- **Model Evaluation:** precision, recall, F1-score, matrice di confusione, serializzazione del modello con pickle.
- **Data Visualization:** countplot e cross-tabulation con Seaborn per l'analisi dei temi e delle metriche stilistiche.

---

## 🚀 Come Eseguire il Progetto
1. Clona la repository o scarica la cartella `04-Fake-News-Detection-NLP`.
2. Assicurati di avere installato le librerie necessarie (`pandas`, `scikit-learn`, `nltk`, `seaborn`, `scipy`).
3. Apri ed esegui il notebook `Fake_News_Detection_NLP.ipynb` su Google Colab o Jupyter Notebook.
4. I file `fake_news_model.pkl` e `tfidf_vectorizer.pkl` verranno generati nella directory di lavoro.

---

## 👤 Autore
**Alessandro Gravagna**
Monza (MB), Italia
