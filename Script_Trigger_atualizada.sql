-- Função de UPSERT 
CREATE OR REPLACE FUNCTION fn_upsert_fato_nutricao()
RETURNS TRIGGER AS $$
DECLARE
    nome_alimento_log VARCHAR(200);
BEGIN
    SELECT nome_alimento INTO nome_alimento_log
    FROM dim_alimento
    WHERE id_alimento = NEW.id_alimento;

    IF EXISTS (
        SELECT 1 FROM fato_nutricao
        WHERE id_alimento = NEW.id_alimento
          AND id_nutriente = NEW.id_nutriente
    ) THEN
        UPDATE fato_nutricao
        SET quantidade = NEW.quantidade,
            nutrition_density = NEW.nutrition_density,
            health_score = NEW.health_score
        WHERE id_alimento = NEW.id_alimento
          AND id_nutriente = NEW.id_nutriente;

        INSERT INTO log_insercao_fato (id_fato, nome_alimento, acao)
        VALUES (
            (SELECT id_fato FROM fato_nutricao
             WHERE id_alimento = NEW.id_alimento
               AND id_nutriente = NEW.id_nutriente),
            nome_alimento_log,
            'UPDATE'
        );

        RETURN NULL;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Trigger de UPSERT
CREATE TRIGGER tr_upsert_fato_nutricao
BEFORE INSERT ON fato_nutricao
FOR EACH ROW
EXECUTE FUNCTION fn_upsert_fato_nutricao();

-- Função de UPDATE
CREATE OR REPLACE FUNCTION fn_log_update_fato()
RETURNS TRIGGER AS $$
DECLARE
    nome_alimento_log VARCHAR(200);
BEGIN
    SELECT nome_alimento INTO nome_alimento_log
    FROM dim_alimento
    WHERE id_alimento = NEW.id_alimento;

    INSERT INTO log_insercao_fato (id_fato, nome_alimento, acao)
    VALUES (NEW.id_fato, nome_alimento_log, 'UPDATE');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger de UPDATE
CREATE TRIGGER tr_log_update_fato
AFTER UPDATE ON fato_nutricao
FOR EACH ROW
EXECUTE FUNCTION fn_log_update_fato();

-- Função de DELETE
CREATE OR REPLACE FUNCTION fn_log_delete_fato()
RETURNS TRIGGER AS $$
DECLARE
    nome_alimento_log VARCHAR(200);
BEGIN
    SELECT nome_alimento INTO nome_alimento_log
    FROM dim_alimento
    WHERE id_alimento = OLD.id_alimento;

    INSERT INTO log_insercao_fato (id_fato, nome_alimento, acao)
    VALUES (OLD.id_fato, nome_alimento_log, 'DELETE');

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger de DELETE
CREATE TRIGGER tr_log_delete_fato
AFTER DELETE ON fato_nutricao
FOR EACH ROW
EXECUTE FUNCTION fn_log_delete_fato();

INSERT INTO fato_nutricao (id_alimento, id_nutriente, quantidade, nutrition_density, health_score)
VALUES (2, 3, 150, 7.5, 65.3);

UPDATE fato_nutricao
SET quantidade = 135.2
WHERE id_fato = 2;

DELETE FROM fato_nutricao
WHERE id_fato = 1;

SELECT * FROM log_insercao_fato ORDER BY data_insercao DESC;
