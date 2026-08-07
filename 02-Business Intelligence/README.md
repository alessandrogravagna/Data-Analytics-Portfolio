# 📊 02. Business Intelligence & Dashboarding Portfolio

In questa sezione sono raccolti i progetti di Business Intelligence sviluppati con **Microsoft Power BI** e **Tableau** per la trasformazione di dataset complessi ed eterogenei in dashboard interattive, report navigabili e Data Storytelling a supporto delle decisioni strategiche aziendali.

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

## 🇪🇺 Progetto 2: Ottimizzazione Data-Driven & Marketing Strategy (Superstore Europa)

![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📌 Panoramica del Progetto
**Superstore Europa** ha avviato un processo di trasformazione data-driven per sostituire la reportistica statica con sistemi dinamici di Business Intelligence. Il progetto risponde a due esigenze chiave della direzione aziendale:
1. Il **monitoraggio continuo e globale delle operazioni europee** (andamento vendite, profitti per nazione, efficienza delle classi di spedizione).
2. La definizione di una **strategia di allocazione del budget marketing** basata sull'analisi del potenziale dei prodotti.

🔗 **[Visualizza il Progetto Interattivo su Tableau Public](https://public.tableau.com/views/Progettotableaumaster/Storia1?:language=it-IT&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

---

### 💡 Valore Aggiunto Aziendale

1. **Ottimizzazione del Budget Marketing:** Identificazione analitica dei prodotti ad alto margine ma sottovalutati in termini di vendite (da spingere), dei prodotti saturi/a basso margine (da ridurre) e dei prodotti in perdita da eliminare dal catalogo.
2. **Data Storytelling Strategico (Regola delle 3C):** Presentazione visiva strutturata in formato *Tableau Story* (Contesto, Conflitto, Conclusione) per guidare l'executive board verso decisioni chiare e direttamente applicabili.
3. **Ottimizzazione Logistica & Geo-Analytics:** Analisi combinata della marginalità per nazione/città e dell'impatto dei costi di spedizione per classe di servizio per ridurre le inefficienze operative.

---

### 🖥️ Architettura della Tableau Story & Dashboard

La soluzione è articolata in una **Tableau Story** e in **Dashboard di monitoraggio operativo**:

* 📊 **Executive Operations Dashboard:** Visualizzazione dinamica del trend delle vendite nel tempo, mappa coropletica del profitto per nazione europea e scomposizione dei volumi per classe di spedizione (Standard, Express, Same Day).
* 📖 **Tableau Marketing Story (3C Framework):**
  * **Contesto:** Panoramica generale delle vendite e della profittabilità del mercato europeo.
  * **Conflitto:** Evidenza delle inefficienze nel catalogo (prodotti ad alta marginalità non valorizzati vs. prodotti ad alta vendita ma in perdita).
  * **Conclusione & Raccomandazioni:** Piano d'azione per il riallocamento del budget pubblicitario e la razionalizzazione del catalogo.
* 📍 **Bonus Geo & Logistic Insights:** Mappatura dei profitti per città chiave e analisi di efficienza delle opzioni logistiche.

---

### 🧰 Competenze e Strumenti Tableau Utilizzati

* **Visual Analytics & Storytelling:** Tableau Stories, Tableau Dashboard Layouts, 3C Storytelling Framework.
* **Calculated Fields & Metrics:** Creazione di campi calcolati per margini %, indici di costo logistico e segmentazione di prodotto.
* **Interactive Features:** Filtri dinamici cross-sheet, azioni di evidenziazione (Highlight Actions), mappe geografiche e Slicers interattivi.
* **Cloud Publishing:** Deployment e condivisione su **Tableau Public Cloud**.

---

### 👤 Autore
**Alessandro Gravagna**  
*Junior Data Specialist | Data Analytics Portfolio*  
📍 Monza (MB), Italia
