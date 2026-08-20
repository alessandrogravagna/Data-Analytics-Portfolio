# 🗄️ Behavioral Feature Store for Predictive Banking Analytics

![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Engineering-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto realizzato durante il **Master in Data Analytics di ProfessionAI**, come capstone del modulo su SQL avanzato. Lo scenario di business — un istituto finanziario che vuole predire il churn dei clienti — è uno scenario simulato ideato per applicare le tecniche in un contesto realistico.

L'obiettivo è la progettazione e implementazione in SQL di un **Behavioral Feature Store** denormalizzato (`feature_clienti`), che trasforma il database transazionale relazionale della banca in un dataset analitico a riga singola per cliente, pronto per alimentare modelli di Machine Learning supervisionato (predizione del churn rate, propensione d'acquisto, rilevamento anomalie).

**Dataset:** Fornito dal materiale didattico del Master in Data Analytics di ProfessionAI.

---

## 🏛️ Architettura del Database Relazionale (Schema ER)

```
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

## 💡 Cosa dimostra questo progetto
* **Dataset ready-to-use per Machine Learning:** trasformazione di un database transazionale complesso in una matrice di feature denormalizzata, utilizzabile per modelli predittivi di churn reduction, credit risk e fraud detection.
* **Segmentazione & behavioral analytics:** estrazione di pattern di spesa (volumi uscite/entrate e distribuzione del portafoglio) utili per campagne di marketing mirate.
* **Integrità dei dati & coerenza contabile:** architettura basata su LEFT JOIN a cascata e funzioni aggregate condizionali per evitare la perdita di informazioni sui clienti silenti o privi di transazioni.

---

## ⚙️ Feature Ingegnerizzate

Per ciascun `id_cliente` sono stati calcolati in modo dinamico i seguenti indicatori comportamentali:

- **Indicatori demografici:** `eta_cliente` (calcolata dinamicamente).
- **Indicatori transazionali totali:** volume e frequenza di transazioni in entrata (+) e in uscita (-).
- **Indicatori di portafoglio:** conteggio univoco dei conti posseduti e segmentazione per categoria (Base, Business, Privati, Famiglie).
- **Matrix features (pivoting):** scomposizione incrociata di volumi monetari e numero di movimenti per ogni combinazione di conto ed entrata/uscita.

---

## 🛠️ Codice SQL e Logica di Implementazione

```sql
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
LEFT JOIN conto co ON c.id_cliente = co.id_cliente
LEFT JOIN tipo_conto tc ON co.id_tipo_conto = tc.id_tipo_conto
LEFT JOIN transazioni t ON co.id_conto = t.id_conto
LEFT JOIN tipo_transazione tt ON t.id_tipo_trans = tt.id_tipo_transazione
GROUP BY c.id_cliente, c.data_nascita;
```

---

## 🧰 Competenze Tecniche SQL
- **DDL & DML Advanced:** `CREATE TABLE ... AS SELECT` per la persistenza dei dati aggregati.
- **Conditional Aggregation & Pivoting:** utilizzo avanzato di `SUM(CASE WHEN ...)` e `COUNT(DISTINCT ...)`.
- **Multi-Table Joins:** relazioni a cascata tramite `LEFT JOIN` per preservare l'integrità del campione.
- **Date & Math Functions:** `TIMESTAMPDIFF()`, `CURRENT_DATE`, `ROUND()`.

---

## 👤 Autore
**Alessandro Gravagna**
*Junior Data Analyst* | Monza (MB), Italia
