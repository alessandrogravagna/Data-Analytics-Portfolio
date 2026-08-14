# 💳 Credit Card Customer Segmentation & Targeted Marketing Strategy

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Unsupervised_ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Clustering](https://img.shields.io/badge/Algorithm-K--Means_%26_PCA-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto di Machine Learning non supervisionato realizzato durante il **Master in Data Analytics di ProfessionAI**, come capstone del modulo su Machine Learning. Lo scenario di business — una società finanziaria che vuole segmentare la propria clientela — è uno scenario simulato ideato per applicare le tecniche in un contesto realistico.

L'obiettivo è segmentare la base clienti in gruppi comportamentali omogenei basati su saldo residuo, frequenza d'uso, volumi d'acquisto e abitudini di pagamento con carta di credito, per poter progettare strategie promozionali personalizzate per ciascun profilo.

**Dataset:** TODO-inserisci-fonte-dataset (es. Kaggle, materiale del corso) — circa 9.000 titolari di carta

---

## 💡 Cosa dimostra questo progetto
* **Segmentazione comportamentale data-driven:** superamento delle logiche di segmentazione meramente demografiche tramite l'estrazione di pattern transazionali reali.
* **Ottimizzazione del budget marketing:** identificazione dei cluster ad alta redditività ("Big Spenders") per azioni di fidelizzazione e dei cluster inattivi per campagne di re-ingaggio.
* **Personalizzazione dell'offerta creditizia:** individuazione dei clienti con alta propensione agli acquisti rateali o all'anticipo contanti.

---

## ⚙️ Pipeline di Machine Learning e Metodologia

1. **Analisi Esplorativa (EDA) & Data Cleaning:**
   - Ispezione della struttura dei dati e analisi della matrice di correlazione tra le variabili.
   - Imputazione dei valori mancanti con la mediana per `MINIMUM_PAYMENTS` e `CREDIT_LIMIT`.
   - Rimozione dell'identificativo categorico non informativo (`CUST_ID`).
2. **Preprocessing & Feature Engineering:**
   - Applicazione della trasformazione logaritmica log(1+x) su tutte le variabili monetarie (`BALANCE`, `PURCHASES`, `CASH_ADVANCE`, `PAYMENTS`, ecc.) per attenuare l'asimmetria positiva e l'impatto dei valori estremi.
   - Standardizzazione delle feature tramite `StandardScaler()` per uniformare la scala prima del calcolo delle distanze euclidee.
3. **Clustering Non Supervisionato (K-Means):**
   - Valutazione del numero ottimale di cluster (k=4) tramite Elbow Method e Silhouette Score.
4. **Riduzione Dimensionale & Visualizzazione (PCA):**
   - Proiezione delle 17 feature su 2 componenti principali per l'ispezione visiva e la verifica della separazione tra i cluster.

---

## 📊 Profilazione dei Cluster (Business Personas)

| Cluster | Archetipo | Caratteristiche Finanziarie | Strategia di Marketing Mirata |
| :--- | :--- | :--- | :--- |
| **Cluster 0** | Low Engagement / Inattivi | Saldo e limite di credito contenuti, frequenza d'acquisto molto bassa. | Re-ingaggio con bonus cashback o incentivi all'attivazione. |
| **Cluster 1** | Cash Advance Dependent | Elevato saldo residuo, frequenza e importi d'anticipo contante alti. | Consolidamento debito: prestiti personali a tassi agevolati. |
| **Cluster 2** | Big Spenders / VIP | Elevata capacità di spesa, alto limite di credito, alta % di pagamento completo. | Retention premium: upgrade Gold/Platinum, cashback su acquisti luxury. |
| **Cluster 3** | Installment Lovers | Forte prevalenza di acquisti rateali ed elevata frequenza transazionale. | Partnership a tasso zero con e-commerce ed esercenti convenzionati. |

---

## 💻 Codice Principale (Core Logic)

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# 1. Imputazione Valori Mancanti e Trasformazione Logaritmica
df['MINIMUM_PAYMENTS'] = df['MINIMUM_PAYMENTS'].fillna(df['MINIMUM_PAYMENTS'].median())
df['CREDIT_LIMIT'] = df['CREDIT_LIMIT'].fillna(df['CREDIT_LIMIT'].median())

df_model = df.drop(columns=['CUST_ID'])
colonne_monetarie = ['BALANCE', 'PURCHASES', 'CASH_ADVANCE', 'CREDIT_LIMIT',
                     'PAYMENTS', 'MINIMUM_PAYMENTS', 'ONEOFF_PURCHASES', 'INSTALLMENTS_PURCHASES']

for col in colonne_monetarie:
    df_model[col] = np.log1p(df_model[col])

# 2. Standardizzazione delle Feature
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_model)

# 3. Clustering K-Means con k=4
final_k = 4
kmeans_final = KMeans(n_clusters=final_k, init='k-means++', n_init=10, random_state=42)
clusters = kmeans_final.fit_predict(df_scaled)
df['Cluster'] = clusters

# 4. Riduzione Dimensionale per Visualizzazione 2D
pca = PCA(n_components=2)
pca_data = pca.fit_transform(df_scaled)
```

---

## 🧰 Competenze Tecniche Utilizzate
- **Unsupervised Machine Learning:** K-Means Clustering, Elbow Method, Silhouette Score.
- **Dimensionality Reduction:** Principal Component Analysis (PCA) per proiezioni vettoriali 2D.
- **Data Preprocessing & Cleaning:** imputazione della mediana, log transformation per correzione della skewness, feature scaling (`StandardScaler`).
- **Exploratory Data Analysis:** istogrammi distributivi, heatmap di correlazione con Seaborn/Matplotlib.

---

## 🚀 Come Eseguire il Progetto
1. Clona la repository o scarica la cartella del progetto.
2. Apri il notebook `Credit_Card_Customer_Segmentation.ipynb` su Google Colab o Jupyter Notebook.
3. Esegui le celle per riprodurre le analisi di EDA, la validazione di Silhouette/Elbow e la profilazione dei cluster.

---

## 👤 Autore
**Alessandro Gravagna**
*Junior Data Analyst* | Monza (MB), Italia
