## Guida all'Utilizzo dell'Applicazione
Per utilizzare questa applicazione, è necessario disporre di un dataset in formato CSV. Normalmente, questi dataset hanno la seguente struttura:
- **3 colonne**:
  - Una per la data di inizio della validità dei dati.
  - Una per la data di fine della validità dei dati.
  - Una per il valore utile per l'analisi.
Per standardizzare l'applicazione e renderla il più flessibile possibile, ho determinato un formato specifico del dataset che funziona per i dataset provenienti da tutti i siti da cui vengono scaricati.

### Nomi delle Colonne Richieste
- **Data di Inizio Validità**: `date_start`
- **Data di Fine Validità**: `date_end`
- **Valore Utile**:
  - **Dataset Pioggia**: `rain`
  - **Dataset Temperatura**: `temperature`
  - **Dataset Velocità del Vento**: `speed`
  - **Dataset Direzione del Vento**: `direction`

### Struttura di Esempio del Dataset
| date_start | date_end   | rain  |
|------------|------------|-------|
| 2023-01-01 | 2023-01-02 | 5.6   |

| date_start | date_end   | temperature |
|------------|------------|-------------|
| 2023-01-01 | 2023-01-02 | 18.3        |

| date_start | date_end   | speed |
|------------|------------|-------|
| 2023-01-01 | 2023-01-02 | 12.4  |

| date_start | date_end   | direction |
|------------|------------|-----------|
| 2023-01-01 | 2023-01-02 | 150        |
