CREATE OR REPLACE FUNCTION atualizar_controle_medicao()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE bpc.controle_medicao_a a
    SET total_pontos_aprovados = (
        SELECT COUNT(*)
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom) AND p.tipo_situacao = 3
    )
    WHERE EXISTS (
        SELECT 1
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom)
    );
    UPDATE bpc.controle_medicao_a a
    SET total_pontos_em_avaliacao = (
        SELECT COUNT(*)
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom) AND p.tipo_situacao = 2
    )
    WHERE EXISTS (
        SELECT 1
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insert_controle_medicao
AFTER INSERT ON bpc.ponto_controle_p
FOR EACH ROW
EXECUTE FUNCTION atualizar_controle_medicao();

CREATE TRIGGER trigger_update_controle_medicao
AFTER UPDATE ON bpc.ponto_controle_p
FOR EACH ROW
EXECUTE FUNCTION atualizar_controle_medicao();

CREATE TRIGGER trigger_delete_controle_medicao
AFTER DELETE ON bpc.ponto_controle_p
FOR EACH ROW
EXECUTE FUNCTION atualizar_controle_medicao();