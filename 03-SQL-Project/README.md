# 🗄️ Behavioral Feature Store for Predictive Banking Analytics

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQL Engineering](https://img.shields.io/badge/SQL-Feature_Engineering-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progettazione e implementazione in SQL di un **Behavioral Feature Store denormalizzato** (`feature_clienti`) per l'istituto finanziario *Banking Intelligence*. 
L'algoritmo trasforma il database transazionale relazionale della banca in un dataset analitico a riga singola per cliente (riferito univocamente all'ID cliente), pronto per alimentare modelli di **Machine Learning supervisionato** (predizione del *Churn Rate*, propensione d'acquisto e rilevamento anomalie).

---

## 🏛️ Architettura del Database Relazionale (Schema ER)

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
💡 Valore Aggiunto Aziendale
Dataset Ready-to-Use per Machine Learning: Trasformazione di un database transazionale complesso in una matrice di feature denormalizzata per modelli predittivi di Churn Reduction, Credit Risk e Fraud Detection.

Segmentazione & Behavioral Analytics: Estrazione di pattern di spesa (volumi uscite/entrate e distribuzione del portafoglio) per campagne di marketing mirate e personalizzate.

Integrità dei Dati & Coerenza Contabile: Architettura basata su LEFT JOIN a cascata e funzioni aggregate condizionali per evitare la perdita di informazioni sui clienti silenti o privi di transazioni.

⚙️ Feature Ingegnerizzate
Per ciascun id_cliente sono stati calcolati in modo dinamico i seguenti indicatori comportamentali:

Indicatori Demografici: eta_cliente (calcolata in modo dinamico).

Indicatori Transazionali Totali: Volume e frequenza di transazioni in entrata (+) e in uscita (-).

Indicatori di Portafoglio: Conteggio univoco dei conti posseduti e segmentazione per categoria (Base, Business, Privati, Famiglie).

Matrix Features (Pivoting): Scomposizione incrociata di volumi monetari e numero di movimenti per ogni combinazione di conto ed entrata/uscita.

🛠️ Codice SQL e Logica di Implementazione
-- Creazione della Tabella/Feature Store Denormalizzato
CREATE TABLE feature_clienti AS
SELECT 
    c.id_cliente,
    
    -- Feature Demografica
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

    -- Feature Pivotate per Categoria Conto (Esempio: Conto Base)
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '-' THEN 1 ELSE 0 END) AS num_trans_uscita_base,
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '+' THEN 1 ELSE 0 END) AS num_trans_entrata_base,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_uscita_base,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_base,

    -- Feature Pivotate (Esempio: Conto Famiglie)
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_famiglie

FROM cliente c
LEFT JOIN conto co 
    ON c.id_cliente = co.id_cliente
LEFT JOIN tipo_conto tc 
    ON co.id_tipo_conto = tc.id_tipo_conto
LEFT JOIN transazioni t 
    ON co.id_conto = t.id_conto
LEFT JOIN tipo_transazione tt 
    ON t.id_tipo_trans = tt.id_tipo_transazione
GROUP BY 
    c.id_cliente,
    c.data_nascita;

🧰 Competenze Tecniche SQL
DDL & DML Advanced: CREATE TABLE ... AS SELECT per la persistenza dei dati aggregati.

Conditional Aggregation & Pivoting: Utilizzo avanzato di SUM(CASE WHEN ...) e COUNT(DISTINCT ...).

Multi-Table Joins: Relazioni a cascata tramite LEFT JOIN per preservare l'integrità del campione.

Date & Math Functions: TIMESTAMPDIFF(), CURRENT_DATE, ROUND().

👤 Autore
Alessandro Gravagna

Junior Data Analyst | Monza (MB), Italia
