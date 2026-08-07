# 🗄️ 03. SQL & Relational Database Engineering Portfolio

In questa sezione sono raccolti i progetti pratici sviluppati in **SQL (MySQL/PostgreSQL)** dedicati alla gestione dei database relazionali, alla progettazione di pipeline di Business Intelligence, all'estrazione di KPI avanzati e alla creazione di dataset denormalizzati per modelli di Machine Learning (*Feature Engineering*).

---

## 🏦 Progetto 1: Behavioral Feature Store per Predictive Banking Analytics (Banking Intelligence)

![SQL](https://img.shields.io/badge/SQL-MySQL%20%2F%20Relational-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📌 Panoramica del Progetto
L'istituto finanziario **Banking Intelligence** intende sviluppare modelli di **Machine Learning supervisionato** per prevedere il comportamento futuro dei clienti (es. prevenzione dell'abbandono/Churn, propensione all'acquisto di nuovi prodotti finanziari e rilevamento delle anomalie). 

Il progetto ha visto la progettazione e l'implementazione in **SQL** di un **Feature Store denormalizzato** (`feature_clienti`). L'algoritmo aggrega e trasforma il database transazionale relazionale della banca in un unico dataset analitico riferito univocamente all'ID cliente.

---

### 💡 Valore Aggiunto Aziendale

1. **Abilitazione di Modelli Predittivi di Machine Learning:** Trasformazione di un database transazionale complesso in un dataset a riga singola per cliente ready-to-use per modelli di *Churn Rate Reduction*, *Credit Risk* e *Fraud Detection*.
2. **Segmentazione e Personalizzazione:** Estrazione di pattern comportamentali (volumi di uscite/entrate e tipologie di conto preferite) per campagne marketing mirate.
3. **Integrità dei Dati e Coerenza Contabile:** Utilizzo di logiche di `LEFT JOIN` e funzioni aggregate condizionali per garantire che anche i clienti silenti o privi di transazioni siano inclusi senza perdita di informazione.

---

### 🏛️ Architettura del Database Relazionale

Il dataset sorgente si compone di 5 tabelle collegate tramite chiavi primarie ed esterne:

```text
 ┌─────────────┐       ┌─────────────┐       ┌─────────────────┐
 │   CLIENTE   │───1:N─│    CONTO    │───N:1─│   TIPO_CONTO    │
 └─────────────┘       └─────────────┘       └─────────────────┘
                              │
                             1:N
                              │
                       ┌─────────────┐       ┌─────────────────┐
                       │ TRANSAZIONI │───N:1─│ TIPO_TRANSAZIONE│
                       └─────────────┘       └─────────────────┘
```

---

### ⚙️ Feature Ingegnerizzate e Calcolate

Per ciascun cliente (`id_cliente`) sono stati calcolati in modo dinamico i seguenti indicatori comportamentali:

* **Indicatori Demografici:**
  * `eta_cliente`: Calcolata in modo dinamico tramite `TIMESTAMPDIFF(YEAR, data_nascita, CURRENT_DATE)`.
* **Indicatori Transazionali Totali:**
  * `num_transazioni_uscita` / `num_transazioni_entrata`: Conteggio aggregato per segno (`-` o `+`).
  * `importo_tot_uscita` / `importo_tot_entrata`: Somma dei volumi monetari gestiti.
* **Indicatori di Portafoglio (Conti):**
  * `num_totale_conti`: Conteggio univoco tramite `COUNT(DISTINCT id_conto)`.
  * `num_conti_base`, `num_conti_business`, `num_conti_privati`, `num_conti_famiglie`: Segmentazione per tipologia.
* **Matrix Feature (Transazioni per Tipologia di Conto):**
  * Scomposizione incrociata di volumi monetari e numero di movimenti per ciascuna combinazione di conto (Base, Business, Privati, Famiglie) ed entrata/uscita.

---

### 🛠️ Codice SQL e Logica di Implementazione

```sql
-- Creazione della Tabella delle Feature
CREATE TABLE feature_clienti AS
SELECT 
    c.id_cliente,
    
    -- Demografica
    TIMESTAMPDIFF(YEAR, c.data_nascita, CURRENT_DATE) AS eta_cliente,

    -- Transazioni Totali
    SUM(CASE WHEN tt.segno = '-' THEN 1 ELSE 0 END) AS num_transazioni_uscita,
    SUM(CASE WHEN tt.segno = '+' THEN 1 ELSE 0 END) AS num_transazioni_entrata,
    ROUND(SUM(CASE WHEN tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_tot_uscita,
    ROUND(SUM(CASE WHEN tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_tot_entrata,

    -- Portafoglio Conti
    COUNT(DISTINCT co.id_conto) AS num_totale_conti,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Base' THEN co.id_conto END) AS num_conti_base,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Business' THEN co.id_conto END) AS num_conti_business,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Privati' THEN co.id_conto END) AS num_conti_privati,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' THEN co.id_conto END) AS num_conti_famiglie,

    -- Feature Pivotate per Categoria Conto (Base, Business, Privati, Famiglie)
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '-' THEN 1 ELSE 0 END) AS num_trans_uscita_base,
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '+' THEN 1 ELSE 0 END) AS num_trans_entrata_base,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_uscita_base,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_base,
    
    -- [... Categorie Business, Privati, Famiglie ...]
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_famiglie

FROM cliente c
LEFT JOIN conto co ON c.id_cliente = co.id_cliente
LEFT JOIN tipo_conto tc ON co.id_tipo_conto = tc.id_tipo_conto
LEFT JOIN transazioni t ON co.id_conto = t.id_conto
LEFT JOIN tipo_transazione tt ON t.id_tipo_trans = tt.id_tipo_transazione

GROUP BY 
    c.id_cliente,
    c.data_nascita;
```

---

### 🧰 Competenze Tecniche SQL Utilizzate

* **DDL & DML Advanced:** `CREATE TABLE ... AS SELECT` per persistenza dei dati aggregati.
* **Conditional Aggregation:** Utilizzo combinato di `SUM(CASE WHEN ...)` e `COUNT(DISTINCT ...)` per pivoting dinamico.
* **Multi-Table Joins:** Relazioni a cascata tramite `LEFT JOIN` per preservare la completezza del campione.
* **Date & Math Functions:** `TIMESTAMPDIFF()`, `CURRENT_DATE`, `ROUND()`.

---

### 👤 Autore
**Alessandro Gravagna**  
*Junior Data Specialist | Data Analytics Portfolio*  
📍 Monza (MB), Italia
