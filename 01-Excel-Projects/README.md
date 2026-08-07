# 📊 01. Excel Analytics Projects Portfolio

In questa sezione sono raccolti i 3 progetti pratici sviluppati su Microsoft Excel per la risoluzione di problemi aziendali reali: dall'ottimizzazione del servizio clienti fino all'analisi delle vendite e alla simulazione di scenari tramite modellazione statistica e regressione lineare.

---

## Progetto 1: Analisi dei Reclami dei Consumatori (FinServ Solutions)

![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📌 Panoramica del Progetto
Questo progetto è stato commissionato da **FinServ Solutions**, una società specializzata in soluzioni software per la gestione del servizio clienti nel settore finanziario. L'obiettivo principale è stato **ristrutturare, ottimizzare e riorganizzare graficamente e funzionalmente** il dataset aziendale dei reclami dei consumatori per migliorare l'analisi geografica, velocizzare il processo decisionale e monitorare l'efficienza aziendale nei tempi di risposta.

### 💡 Valore Aggiunto Aziendale
1. **Ottimizzazione delle Performance e Tempistiche:** Calcolo automatico dei giorni di gestione tra la ricezione del reclamo e l'invio alla compagnia per monitorare la tempestività del servizio.
2. **Analisi Geografica Mirata:** Creazione di una dashboard per individuare la concentrazione dei reclami per ciascuno stato USA con indicatori visivi (Formattazione Condizionale).
3. **Analisi Statistica delle Problematiche:** Identificazione univoca di tutte le tipologie di reclamo e calcolo automatico della problematica più frequente (*Valore Moda*).

### 🛠️ Architettura e Struttura del Foglio Excel
Il foglio di calcolo è stato riorganizzato in **3 Tab principali**:
* **Consumer complaints:** Dataset principale ordinato per `Complaint ID`, con calcolo automatico dei tempi di risposta, standardizzazione date (`dd/mm/yy`) e filtri temporali.
* **Geographical insights:** Analisi aggregata per Stato USA tramite la formula `=CONTA.SE()`, calcolo delle incidenze percentuali e formattazione condizionale (Verde < 2%, Rosso >= 2%).
* **Statistical insights:** Estrazione di tutti i motivi di reclamo distinti e calcolo del valore moda tramite la funzione `=MODA()`.

---

## Progetto 2: Analisi delle Vendite & Reporting Interattivo (TrendyShoes S.r.l.)

![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📌 Panoramica del Progetto
**TrendyShoes S.r.l.** è un'azienda italiana operante nel settore retail e e-commerce di calzature fashion. A seguito della forte espansione aziendale, la direzione ha richiesto la progettazione di un **sistema di reporting e data analytics su Excel** basato sul dataset *Global Superstore*. L'obiettivo è supportare la transizione verso un approccio *Data-Driven*, ottimizzando le vendite, migliorando i margini sulle promozioni, analizzando i trend stagionali e identificando i segmenti di clientela più profittevoli.

### 💡 Valore Aggiunto Aziendale
1. **Ottimizzazione Promozioni & Margini:** Analisi dell'impatto degli sconti sui profitti effettivi per identificare i prodotti ad alta marginalità e ridurre promozioni infruttuose.
2. **Pianificazione Scorte & Stagionalità:** Calcolo di medie mobili e tassi di crescita mensili per prevedere i picchi di domanda e ottimizzare il riassortimento.
3. **Data-Driven Decision Making:** Integrazione di Tabelle Pivot dinamiche e Dashboard interattive con filtri visivi per consentire al management decisioni tempestive.

### 🛠️ Architettura e Struttura del Foglio Excel
Il modello è organizzato nei seguenti Tab:
* **Statistica descrittiva:** Calcolo delle Medie Mobili a 3 e 6 mesi, Tassi di Crescita (MoM/YoY), Deviazione Standard e Indici di Stagionalità.
* **Tabelle pivot:** Aggregazioni dinamiche di fatturato e profitti per Area Geografica, Categoria Prodotto e Canale Distributivo.
* **Dashboard:** Report visivo con KPI principali (Fatturato, Profitto Netto, Margine %), Grafici Dinamici e Slicers interattivi per filtro anno e regione.

---

## Progetto 3: Simulazione Dati Casuali & Modellazione Statistica (Luggnagg Population Study)

![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

### 📌 Panoramica del Progetto
In un contesto aziendale data-driven, la capacità di **simulare scenari reali e generare dataset sintetici verosimili** è fondamentale per testare modelli predittivi e supportare decisioni strategiche in assenza di dati storici completi. Il progetto simula le caratteristiche demografiche di un campione di 250 individui della popolazione di *Luggnagg*, applicando tecniche di **generazione di distribuzioni normali, campionamento condizionale, analisi di correlazione e regressione lineare**.

### 💡 Valore Aggiunto Aziendale
1. **Simulazione di Scenari & Risk Management:** Creazione di ambienti simulati sicuri per testare ipotesi di mercato e modelli di machine learning/statistici senza costi di raccolta dati.
2. **Campionamento e Segmentazione:** Capacità di isolare sotto-campioni specifici per analisi di gruppo e stime parametriche di confidenza.
3. **Analisi Relazionale e Predittiva:** Valutazione della correlazione tra variabili e costruzione di modelli di regressione lineare per identificare trend e relazioni causa-effetto.

### 🛠️ Architettura e Struttura del Foglio Excel
Il modello è strutturato su **6 Tab specializzati**:
* **Parameters:** Interfaccia utente per l'impostazione dei parametri probabilistici di input (Probabilità, Media $\mu$, Deviazione Standard $\sigma$).
* **Data:** Generazione stocastica dell'età della popolazione (distribuzione normale di 250 individui) e assegnazione casuale a 4 gruppi distinti tramite funzioni casuali.
* **Sample:** Estrazione dinamica e filtraggio condizionale del sotto-campione di analisi relativo a uno specifico gruppo tramite la funzione `=SE()`.
* **Statistical Insight:** Calcolo degli indicatori statistici chiave del campione (Deviazione Standard, Valore Atteso, Dimensione Campionaria, Tasso di Confidenza, Intervallo di Confidenza e stima del parametro $p$).
* **(Un)correlated Variables:** Verifica delle relazioni statistiche ed elaborazione della matrice di correlazione tra l'età e variabili indipendenti (es. numero di gatti posseduti, età del partner).
* **Linear Regression:** Modellazione di regressione lineare tra l'età ($Y$) e l'ordine di censimento/rank ($X$), completa di scatterplot, equazione della retta di regressione ed stima predittiva per specifici partecipanti.

---

### 👤 Autore
**Alessandro Gravagna**  
*Junior Data Specialist | Data Analytics Portfolio*  
📍 Monza (MB), Italia
