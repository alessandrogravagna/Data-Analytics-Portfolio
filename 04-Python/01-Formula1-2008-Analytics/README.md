# 🏎️ Formula 1 2008 Season Analytics & Performance Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white)
![Data Analysis](https://img.shields.io/badge/Data_Analysis-Pure_Python-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Panoramica del Progetto
Progetto realizzato durante il **Master in Data Analytics di ProfessionAI**, come capstone del modulo introduttivo su Python puro (senza librerie esterne). Lo scenario di business — una società di F1 Analytics che elabora dati prestazionali e contabili — è uno scenario simulato ideato per applicare le tecniche in un contesto realistico.

Il sistema processa i dati grezzi delle gare (`formula1_data.csv`) applicando il regolamento ufficiale di punteggio F1 2008 per calcolare le metriche di performance individuali dei piloti e generare le classifiche mondiali (Piloti e Costruttori).

**Dataset:** Fornito dal materiale didattico del Master in Data Analytics di ProfessionAI.

---

## ⚙️ Regolamento Punteggi F1 2008 Implementato
Il sistema calcola i punti assegnati al termine di ogni Gran Premio in base alla posizione di arrivo:
* **1° Posto:** 10 pt | **2° Posto:** 8 pt | **3° Posto:** 6 pt | **4° Posto:** 5 pt
* **5° Posto:** 4 pt | **6° Posto:** 3 pt | **7° Posto:** 2 pt | **8° Posto:** 1 pt
* **9° Posto o oltre:** 0 pt

---

## 💡 Cosa dimostra questo progetto
* **Elaborazione nativa senza dipendenze:** elaborazione dei dati basata sulla libreria standard di Python, senza librerie esterne — utile per capire la logica sotto il cofano prima di affidarsi a Pandas.
* **Automazione del reporting:** generazione ed esportazione automatica delle classifiche su file di testo (`Drivers_Standings_2008.txt`).
* **Consultazione dinamica:** interfaccia interattiva da riga di comando per estrarre KPI individuali (punti, vittorie, podi) per qualsiasi pilota della stagione.

---

## 💻 Codice Principale (Core Logic)

```python
import csv

# Sistema di punteggio ufficiale F1 2008
PUNTEGGI_2008 = {"1": 10, "2": 8, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1}

def ottieni_punti(posizione):
    return PUNTEGGI_2008.get(posizione, 0)

# 1. Performance individuali pilota
def analizza_performance_pilota(dati, nome_pilota):
    punti_totali, vittorie, podi = 0, 0, 0
    for riga in dati:
        if riga['Driver'].lower() == nome_pilota.lower():
            pos = riga['Position']
            punti_totali += ottieni_punti(pos)
            if pos == "1": vittorie += 1
            if pos in ["1", "2", "3"]: podi += 1
    return [punti_totali, vittorie, podi]

# 2. Generazione Classifica Piloti ed Export File
def genera_classifica_piloti(dati):
    classifica = {}
    for riga in dati:
        pilota = riga['Driver']
        classifica[pilota] = classifica.get(pilota, 0) + ottieni_punti(riga['Position'])

    classifica_ordinata = dict(sorted(classifica.items(), key=lambda item: item[1], reverse=True))

    with open("Drivers_Standings_2008.txt", "w", encoding="utf-8") as file:
        file.write("Drivers Standings 2008 Formula 1\n")
        for pilota, punteggio in classifica_ordinata.items():
            file.write(f"{pilota}: {punteggio}\n")

    return classifica_ordinata
```

**Esempio di output:**
```
RISULTATI PER HAMILTON
Punti Totali : 98
Vittorie     : 5
Podi Totali  : 10

CLASSIFICA PILOTI 2008
1º - Hamilton        98 pt
2º - Massa           97 pt
3º - Raikkonen       75 pt
```

---

## 🧰 Competenze Tecniche Utilizzate
- **File I/O & Parsing:** lettura/scrittura file con gestione sicura dei contesti (`with open`), codifica UTF-8 e `csv.DictReader`.
- **Data Structures:** manipolazione di dizionari, liste e insiemi (`set`) per deduplicazione e aggregazione in memoria.
- **Functional Sorting & Lambdas:** ordinamento dinamico per valore con `sorted(..., key=lambda item: item[1], reverse=True)`.
- **String Formatting & CLI:** formattazione dell'output con f-string e `ljust()`.

---

## 🚀 Come Eseguire il Progetto
1. Scarica la cartella `01-Formula1-2008-Analytics`.
2. Apri il notebook `F1_2008_Performance_Analysis.ipynb` su Google Colab o Jupyter Notebook.
3. Assicurati che il dataset `formula1_data.csv` si trovi nella stessa directory del file `.ipynb`.
4. Esegui le celle in sequenza per avviare l'analisi interattiva.

---

## 👤 Autore
**Alessandro Gravagna**
*Junior Data Analyst* | Monza (MB), Italia
