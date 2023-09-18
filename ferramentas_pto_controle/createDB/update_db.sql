BEGIN;

ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_imagem_lateral_1 VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_imagem_lateral_2 VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_imagem_lateral_3 VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_imagem_lateral_4 VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_imagem_aerea VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_croqui VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_monografia VARCHAR(255);
ALTER TABLE bpc.ponto_controle_p ADD COLUMN endereco_rinex VARCHAR(255);

COMMIT;