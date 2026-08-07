# 🏎️ Formula 1 2008 Season Performance Analytics

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📌 Panoramica del Progetto
Il progetto, commissionato dall'agenzia specializzata **F1 Analytics**, si occupa dell'analisi algoritmica dei dati prestazionali relativi al **Campionamento Mondiale di Formula 1 della stagione 2008**. 

L'obiettivo è elaborare i dataset di gara in formato `.csv` attraverso script e algoritmi **Python nativi** (data parsing, dizionari dinamici e cicli di aggregazione), permettendo di interrogare le performance dei singoli piloti, calcolare le metriche di punteggio del regolamento FIA 2008, generare la classifica piloti con export di report di testo e determinare il Campionato Costruttori.

---

## 💡 Valore Aggiunto Aziendale

1. **Automation & Reporting Ingestion:** Automazione del calcolo dei punteggi per ciascuna gara senza dipendere da calcoli manuali o fogli di calcolo esterni.
2. **Interactive CLI Search Engine:** Sistema interattivo con validazione condizionale dell'input per consentire ad analisti e giornalisti la ricerca immediata dei KPI prestazionali di qualsiasi pilota (Punti, Vittorie, Podi).
3. **Data Exporting Standardizzato:** Generazione automatica di file di testo strutturati (`Drivers_Standings_2008.txt`) pronti per la pubblicazione e l'integrazione nei sistemi di reporting editoriale.

---

## ⚙️ Regolamento Punteggi FIA 2008 Implementato

L'algoritmo applica la mappatura ufficiale dei punti assegnati ai primi 8 piazzamenti di ogni Gran Premio:

| Posizione | Punti Assegnati |
| :---: | :---: |
| **1° Posto** | 10 pt |
| **2° Posto** | 8 pt |
| **3° Posto** | 6 pt |
| **4° Posto** | 5 pt |
| **5° Posto** | 4 pt |
| **6° Posto** | 3 pt |
| **7° Posto** | 2 pt |
| **8° Posto** | 1 pt |
| **> 8° Posto** | 0 pt |

---

## 🛠️ Architettura del Codice e Logica di Implementazione

```python
import csv

# 1. Caricamento e parsing del dataset CSV
with open("formula1_data.csv", encoding="utf-8") as file:
    dataset_f1 = list(csv.DictReader(file))

punti_2008 = {"1": 10, "2": 8, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1}

# 2. Funzione per la Performance Individuale del Pilota
def analizza_performance_pilota(dati, nome_pilota):
    punti_totali, vittorie, podi = 0, 0, 0
    for riga in dati:
        if riga['Driver'].lower() == nome_pilota.lower():
            pos = riga['Position']
            if pos in punti_2008:
                punti_totali += punti_2008[pos]
            if pos == "1":
                vittorie += 1
            if pos in ["1", "2", "3"]:
                podi += 1
    return [punti_totali, vittorie, podi]

# 3. Funzione Generazione Classifica Piloti & Export Report
def genera_classifica_piloti(dati):
    classifica = {}
    for riga in dati:
        pilota, pos = riga['Driver'], riga['Position']
        punti = punti_2008.get(pos, 0)
        classifica[pilota] = classifica.get(pilota, 0) + punti

    classifica_ordinata = dict(sorted(classifica.items(), key=lambda x: x[1], reverse=True))

    with open("Drivers_Standings_2008.txt", "w", encoding="utf-8") as f:
        f.write("Drivers Standings 2008 Formula 1\n")
        for pilota, punteggio in classifica_ordinata.items():
            f.write(f"{pilota}: {punteggio}\n")

    return classifica_ordinata
```

---

## 🧰 Competenze Tecniche Python Utilizzate

* **File I/O & CSV Parsing:** Utilizzo del modulo nativo `csv.DictReader` per la manipolazione di dataset eterogenei.
* **Algoritmi di Ordinamento:** Utilizzo di `sorted()` accoppiato a funzioni lambda (`key=lambda x: x[1]`) per l'ordinamento decrescente dei dizionari.
* **Control Flow & Input Validation:** Cicli `while` per la gestione difensiva degli errori di input dell'utente e normalizzazione delle stringhe con `.lower()` e `.strip()`.
* **Data Persistence:** Scrittura ed esportazione automatizzata di file di testo (`.txt`) tramite context manager (`with open(...)`).

---

## 👤 Autore
**Alessandro Gravagna**  
*Junior Data Specialist | Data Analytics Portfolio*  
📍 Monza (MB), Italia
