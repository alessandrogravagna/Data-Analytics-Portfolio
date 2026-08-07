# 📊 02. Business Intelligence & Dashboarding Portfolio

In questa sezione sono raccolti i progetti di Business Intelligence sviluppati con **Microsoft Power BI** per la trasformazione di dataset complessi ed eterogenei in dashboard interattive, navigabili e data-driven a supporto dei decision-maker aziendali.

---

## 🏬 Progetto 1: Gestione Vendite & Performance Punti Vendita (TechMarket S.p.A.)

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📌 Panoramica del Progetto
**TechMarket S.p.A.** è una delle principali catene italiane di distribuzione al dettaglio di elettronica di consumo. Per gestire ed elaborare l'enorme mole di dati provenienti dai punti vendita distribuiti sul territorio nazionale, è stata progettata una **soluzione avanzata di BI e reportistica su Power BI**. 

Il report integra le transazioni di vendita del 2014, i dati anagrafici dei negozi e dei prodotti e la gestione analitica dei resi per fornire al management un quadro veritiero e navigabile delle vendite nette e della redditività territoriale.

---

### 💡 Valore Aggiunto Aziendale

1. **Monitoraggio Nette vs. Lorde (Gestione Resi):** Integrazione del modulo dei resi (gennaio/febbraio) per il calcolo dinamico del fatturato netto effettivo per punto vendita.
2. **Geolocalizzazione delle Performance:** Mappatura geografica interattiva per identificare immediatamente i cluster regionali e le città top-performer (es. Roma e Verona).
3. **UX/UI Navigabile & Interattiva:** Implementazione di un menu superiore con pulsanti e segnalibri (*Bookmarks*) per consentire un passaggio rapido tra 5 aree di analisi senza sovraccaricare la schermata.

---

### 🖥️ Struttura della Dashboard Interattiva

Il report si compone di **5 pagine/sezioni principali** interconnesse tramite pulsanti d'azione:

* 📍 **Vendite per città:** Istogrammi Unità Vendute e Mappatura Geografica Territoriale.
* 📅 **Vendite per mese:** Analisi temporale dell'andamento delle vendite, prezzi e sconti.
* 📦 **Dettaglio Prodotto:** Donut Chart quote di mercato, Slicers condizionali e tabelle di performance.
* 🏪 **Info Negozi:** Ranking Responsabili Store, fatturato totale e volumi per indirizzo.
* 🔄 **Gestione Resi:** Focus contabile sulle vendite nette escludendo i resi.

---

### 📐 Modello Dati e Pipeline ETL (Power Query)

* **Data Ingestion & Merge:** Importazione ed elaborazione di file multipli mensili e tabelle anagrafiche (Negozi, Prodotti, Province). Unione delle fonti tramite operazioni di *Merge* in Power Query per associare `Prezzo Unitario`, `Descrizione Prodotto` e `Responsabile` tramite chiavi relazionali (`Prodotto_ID`, `Store_ID`).
* **Relazioni del Modello (Star Schema):** Definizione delle relazioni 1-a-molti tra le tabelle di dimensione (`Dim_Prodotti`, `Dim_Negozi`) e la tabella dei fatti (`Fact_Vendite`, `Fact_Resi`).
* **Misure & Calcoli DAX:** Calcolo di metriche di Business tra cui:
  $$\text{Vendite Totali} = \sum (\text{Unità Vendute} \times \text{Prezzo Unitario} \times (1 - \text{Sconto}))$$
  $$\text{Vendite Nette} = \text{Vendite Totali} - \text{Valore Resi}$$

---

### 🧰 Competenze e Strumenti Power BI Utilizzati

* **Data Preparation:** Power Query (Merge, Append, Pulizia tipi dato, Trasformazione colonne).
* **Data Modeling:** Modello relazionale a stella, relazioni direzionali, ottimizzazione delle chiavi esterne.
* **Data Visualization:** Map Visuals, Donut Charts, Clustered Bar Charts, Matrix Tables con KPI.
* **Interactive Features:** Page Navigation Buttons, Bookmarks, Cross-filtering, Slicers condizionali per città e prodotti.

---

### 👤 Autore
**Alessandro Gravagna**  
*Junior Data Specialist | Data Analytics Portfolio*  
📍 Monza (MB), Italia
