-- Procedure calc_media_nutriente
CREATE OR REPLACE PROCEDURE calc_media_nutriente(nutriente_nome TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    quantidade_total NUMERIC := 0;
    contador INTEGER := 0;
    media NUMERIC := 0;
    registro RECORD;
BEGIN
    FOR registro IN
        SELECT f.quantidade
        FROM fato_nutricao f
        JOIN dim_nutriente n ON f.id_nutriente = n.id_nutriente
        WHERE n.nome_nutriente = nutriente_nome
    LOOP
        quantidade_total := quantidade_total + registro.quantidade;
        contador := contador + 1;
    END LOOP;

    IF contador > 0 THEN
        media := quantidade_total / contador;
        RAISE NOTICE 'Média de %: %', nutriente_nome, ROUND(media, 2);
    ELSE
        RAISE NOTICE 'Nenhum dado encontrado para o nutriente: %', nutriente_nome;
    END IF;
END;
$$;

-- Como usar
CALL calc_media_nutriente('Caloric_Value');
CALL calc_media_nutriente('Protein');