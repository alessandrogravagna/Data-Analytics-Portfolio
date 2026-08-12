# 💳 Credit Card Customer Segmentation & Targeted Marketing Strategy

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Unsupervised_ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Clustering](https://img.shields.io/badge/Algorithm-K--Means_%26_PCA-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto di Machine Learning Non Supervisionato sviluppato per la società finanziaria **FinTech Solutions S.p.A.** con l'obiettivo di segmentare la base clienti in gruppi comportamentali omogenei basati su saldo residuo, frequenza d'uso, volumi d'acquisto e abitudini di pagamento con carta di credito.
La soluzione consente all'azienda di ottimizzare il budget pubblicitario, aumentare il tasso di conversione delle campagne e progettare strategie promozionali fortemente personalizzate per ciascun profilo di utente.

---

## 💡 Valore Aggiunto Aziendale
* **Segmentazione Comportamentale Data-Driven:** Superamento delle tradizionali logiche di segmentazione meramente demografiche tramite l'estrazione di pattern transazionali reali da un campione di circa 9.000 titolari di carta.
* **Ottimizzazione del ROI di Marketing:** Identificazione dei cluster ad alta redditività (*Big Spenders*) per azioni di fidelizzazione e dei cluster inattivi per campagne promozionali di re-ingaggio.
* **Personalizzazione dell'Offerta Creditizia:** Progettazione di prodotti mirati per i clienti con alta propensione agli acquisti rateali (`INSTALLMENTS_PURCHASES`) o all'anticipo contanti (`CASH_ADVANCE`).

---

## ⚙️ Pipeline di Machine Learning e Metodologia

1. **Analisi Esplorativa (EDA) & Data Cleaning:**
   * Ispezione della struttura dei dati e analisi della matrice di correlazione tra le variabili.
   * Imputazione dei valori mancanti con la mediana per `MINIMUM_PAYMENTS` e `CREDIT_LIMIT` per garantire la massima robustezza agli outlier.
   * Rimozione dell'identificativo categorico non informativo (`CUST_ID`).
2. **Preprocessing & Feature Engineering:**
   * Applicazione della trasformazione logaritmica $\log(1 + x)$ su tutte le variabili monetarie (`BALANCE`, `PURCHASES`, `CASH_ADVANCE`, `PAYMENTS`, ecc.) per attenuare la forte asimmetria positiva (skewness) e l'impatto dei valori estremi.
   * Standardizzazione completa delle feature tramite `StandardScaler()` per uniformare la scala operativa prima del calcolo delle distanze euclidee.
3. **Clustering Non Supervisionato (K-Means):**
   * Valutazione del numero ottimale di cluster ($k=4$) tramite analisi combinata dell'Inerzia/WCSS (**Elbow Method**) e del **Silhouette Score**.
4. **Riduzione Dimensionale & Visualizzazione (PCA):**
   * Proiezione delle 17 feature su 2 componenti principali (PCA) per l'ispezione visiva 2D e la verifica della separazione spaziale tra i cluster.

---

## 📊 Profilazione dei Cluster (Business Personas)

Calcolando il profilo medio di ciascun gruppo sulle variabili originali, sono emersi 4 segmenti di clientela nettamente distinti:

| Cluster | Archetipo | Caratteristiche Finanziarie | Strategia di Marketing Mirata |
| :--- | :--- | :--- | :--- |
| **Cluster 0** | **Low Engagement / Inattivi** | Saldo e limite di credito contenuti, frequenza d'acquisto molto bassa, utilizzo sporadico. | **Re-Ingaggio:** Promozioni con bonus cashback o incentivi all'attivazione al raggiungimento di una soglia minima di transazioni. |
| **Cluster 1** | **Cash Advance Dependent** | Elevato saldo residuo, frequenza e importi d'anticipo contante (`CASH_ADVANCE`) alti. | **Consolidamento Debito:** Proposta di prestiti personali a tassi agevolati per convertire l'anticipo contanti in credito al consumo a minor rischio. |
| **Cluster 2** | **Big Spenders / VIP** | Elevata capacità di spesa (`PURCHASES`), alto limite di credito e alta percentuale di pagamento completo (`PRC_FULL_PAYMENT`). | **Retention Premium:** Upgrade a carte Gold/Platinum, cashback su acquisti luxury e vantaggi esclusivi. |
| **Cluster 3** | **Installment Lovers** | Forte prevalenza di acquisti rateali (`INSTALLMENTS_PURCHASES`) ed elevata frequenza transazionale. | **Partnership & Tasso Zero:** Promozioni di finanziamento a tasso zero presso e-commerce ed esercenti convenzionati. |

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
## 🧰 Competenze Tecniche Utilizzate
Unsupervised Machine Learning: K-Means Clustering, Elbow Method, Silhouette Score.
Dimensionality Reduction: Principal Component Analysis (PCA) per proiezioni vettoriali 2D.
Data Preprocessing & Cleaning: Imputazione della mediana, Log Transformation ($\log(1+x)$) per correzione della skewness, Feature Scaling (StandardScaler).
Exploratory Data Analysis: Istogrammi distributivi, Heatmap di correlazione con Seaborn/Matplotlib.
## 🚀 Come Eseguire il Progetto
Scarica la cartella 03-Credit-Card-Customer-Segmentation.
Apri il notebook Credit_Card_Customer_Segmentation.ipynb su Google Colab o Jupyter Notebook.
Esegui le celle per riprodurre le analisi di EDA, la validazione di Silhouette/Elbow e la profilazione dei cluster.
##👤 Autore
##Alessandro Gravagna##
Junior Data Analyst | Monza (MB), Italia
