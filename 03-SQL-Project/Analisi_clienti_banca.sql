
-- PROGETTO SQL: ANALISI DEI CLIENTI DI UNA BANCA


-- 1. SELEZIONE DEL DATABASE
USE banca;

-- 2. CREAZIONE DELLA TABELLA DELLE FEATURE
-- Uso la struttura CREATE TABLE ... AS per salvare fisicamente i dati nel database.
-- Applico il GROUP BY per ottenere esattamente una riga per ogni singolo cliente.

CREATE TABLE feature_clienti AS
SELECT 
    c.id_cliente,
    
    -- Indicatori di base: Età del cliente calcolata a oggi
    TIMESTAMPDIFF(YEAR, c.data_nascita, CURRENT_DATE) AS eta_cliente,

    -- Indicatori sulle transazioni totali (Uscite ed Entrate)
    SUM(CASE WHEN tt.segno = '-' THEN 1 ELSE 0 END) AS num_transazioni_uscita,
    SUM(CASE WHEN tt.segno = '+' THEN 1 ELSE 0 END) AS num_transazioni_entrata,
    ROUND(SUM(CASE WHEN tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_tot_uscita,
    ROUND(SUM(CASE WHEN tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_tot_entrata,

    -- Indicatori sui conti posseduti (Uso DISTINCT per evitare doppioni causati dalle JOIN)
    COUNT(DISTINCT co.id_conto) AS num_totale_conti,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Base' THEN co.id_conto END) AS num_conti_base,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Business' THEN co.id_conto END) AS num_conti_business,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Privati' THEN co.id_conto END) AS num_conti_privati,
    COUNT(DISTINCT CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' THEN co.id_conto END) AS num_conti_famiglie,

    -- Indicatori sulle transazioni per tipologia di conto: CONTO BASE
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '-' THEN 1 ELSE 0 END) AS num_trans_uscita_base,
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '+' THEN 1 ELSE 0 END) AS num_trans_entrata_base,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_uscita_base,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Base' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_base,

    -- Indicatori sulle transazioni per tipologia di conto: CONTO BUSINESS
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Business' AND tt.segno = '-' THEN 1 ELSE 0 END) AS num_trans_uscita_business,
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Business' AND tt.segno = '+' THEN 1 ELSE 0 END) AS num_trans_entrata_business,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Business' AND tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_uscita_business,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Business' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_business,

    -- Indicatori sulle transazioni per tipologia di conto: CONTO PRIVATI
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Privati' AND tt.segno = '-' THEN 1 ELSE 0 END) AS num_trans_uscita_privati,
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Privati' AND tt.segno = '+' THEN 1 ELSE 0 END) AS num_trans_entrata_privati,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Privati' AND tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_uscita_privati,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Privati' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_privati,

    -- Indicatori sulle transazioni per tipologia di conto: CONTO FAMIGLIE
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' AND tt.segno = '-' THEN 1 ELSE 0 END) AS num_trans_uscita_famiglie,
    SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' AND tt.segno = '+' THEN 1 ELSE 0 END) AS num_trans_entrata_famiglie,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' AND tt.segno = '-' THEN t.importo ELSE 0 END), 2) AS importo_uscita_famiglie,
    ROUND(SUM(CASE WHEN tc.desc_tipo_conto = 'Conto Famiglie' AND tt.segno = '+' THEN t.importo ELSE 0 END), 2) AS importo_entrata_famiglie

-- 3. RELAZIONI TRA LE TABELLE (Uso LEFT JOIN per non escludere clienti senza movimenti)
FROM cliente c
LEFT JOIN conto co ON c.id_cliente = co.id_cliente
LEFT JOIN tipo_conto tc ON co.id_tipo_conto = tc.id_tipo_conto
LEFT JOIN transazioni t ON co.id_conto = t.id_conto
LEFT JOIN tipo_transazione tt ON t.id_tipo_trans = tt.id_tipo_transazione

-- 4. AGGREGAZIONE FINALE
GROUP BY 
    c.id_cliente,
    c.data_nascita;

-- 5. VERIFICA DEL RISULTATO (Opzionale per il professore)
-- SELECT * FROM feature_clienti LIMIT 10;