-- Criando a tabela dim_alimento
CREATE TABLE dim_alimento (
    id_alimento SERIAL PRIMARY KEY,
    nome_alimento VARCHAR(200)
);
SELECT * FROM dim_alimento;

-- Criando a tabela dim_nutriente;
CREATE TABLE dim_nutriente (
    id_nutriente SERIAL PRIMARY KEY,
    nome_nutriente VARCHAR(100)
);
SELECT * FROM dim_nutriente;

-- Criando a tabela fato_nutricao

CREATE TABLE fato_nutricao (
    id_fato SERIAL PRIMARY KEY,
    id_alimento INTEGER REFERENCES dim_alimento(id_alimento),
    id_nutriente INTEGER REFERENCES dim_nutriente(id_nutriente),
    quantidade NUMERIC,
    nutrition_density NUMERIC,
    health_score NUMERIC
);
SELECT * FROM fato_nutricao;

-- Select de consulta por alimento com score mais baixo
SELECT
    a.nome_alimento AS alimento,
    n.nome_nutriente AS nutriente,
    f.quantidade,
    f.nutrition_density,
    f.health_score
FROM
    fato_nutricao f
JOIN dim_alimento a ON f.id_alimento = a.id_alimento
JOIN dim_nutriente n ON f.id_nutriente = n.id_nutriente
WHERE
    f.health_score < 80
ORDER BY
    f.health_score DESC,
    a.nome_alimento,
    n.nome_nutriente;

-- Tabela auxiliar para poder rodar as triggers não faz parte do Data Warehouse
CREATE TABLE log_insercao_fato (
    log_id SERIAL PRIMARY KEY,
    id_fato INTEGER,
    nome_alimento VARCHAR(200),
    data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acao VARCHAR(50)
);

SELECT
    a.nome_alimento AS alimento,
    n.nome_nutriente AS nutriente,
    ROUND(AVG(f.quantidade), 2) AS media_quantidade
FROM
    fato_nutricao f
JOIN dim_alimento a ON f.id_alimento = a.id_alimento
JOIN dim_nutriente n ON f.id_nutriente = n.id_nutriente
GROUP BY
    a.nome_alimento,
    n.nome_nutriente
ORDER BY
    a.nome_alimento,
    n.nome_nutriente;
