-- ANÁLISE 1: KPI - Taxa de Conclusão do Acervo (Formatado)
SELECT
    -- Contagem total de livros no acervo
    COUNT(l.ID) AS total_livros,

    -- Contagem de livros que estão no status 'Lido'
    SUM(CASE WHEN s.Nome_do_status = 'Lido' THEN 1 ELSE 0 END) AS livros_concluidos,

    -- Cálculo do KPI: Percentual de conclusão (Arredondado para 1 casa decimal)
    ROUND(
        CAST(SUM(CASE WHEN s.Nome_do_status = 'Lido' THEN 1 ELSE 0 END) AS NUMERIC) * 100 / COUNT(l.ID),
        1 -- 1 casa decimal de precisão
    ) AS percentual_conclusao
FROM
    Livros l
JOIN
    Status_leitores s ON l.ID_status = s.ID_status;

-- ANÁLISE 2: Tempo Médio de Leitura por Gênero (em dias) - FORMATADO
SELECT
    genero,
    -- Usa ROUND para arredondar o resultado da média para zero casas decimais
    ROUND(AVG(data_fim_leitura - data_inicio_leitura)) AS tempo_medio_leitura_dias_arredondado
FROM
    Livros
WHERE
    data_inicio_leitura IS NOT NULL AND data_fim_leitura IS NOT NULL
GROUP BY
    genero
ORDER BY
    tempo_medio_leitura_dias_arredondado ASC;


-- ANÁLISE 3: Top 5 Autores por Livros no Acervo e Status Pendente
SELECT
    a.Nome_do_autor,
    COUNT(l.ID) AS total_livros_no_acervo,
    -- Contagem de livros com status 'Pendente' (usando CASE WHEN para filtrar)
    SUM(CASE WHEN s.Nome_do_status = 'Pendente' THEN 1 ELSE 0 END) AS livros_pendentes
FROM
    Livros l
JOIN
    Autores a ON l.ID_autor = a.ID_autor
JOIN
    Status_leitores s ON l.ID_status = s.ID_status
GROUP BY
    a.Nome_do_autor
ORDER BY
    total_livros_no_acervo DESC
LIMIT 5;