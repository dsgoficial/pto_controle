CREATE EXTENSION postgis;
CREATE SCHEMA dominios;

CREATE TABLE dominios.tipo_situacao(
	code SMALLINT NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL
);
ALTER TABLE dominios.tipo_situacao OWNER TO postgres;

INSERT INTO dominios.tipo_situacao (code, nome) VALUES (1, 'Não medido');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (2, 'Aguardando revisão');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (3, 'Aprovado');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (4, 'Reprovado');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (9999, 'A SER PREENCHIDO');

CREATE TABLE dominios.classificacao_ponto(
	code SMALLINT NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL
);
ALTER TABLE dominios.classificacao_ponto OWNER TO postgres;

INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (0, 'Desconhecido');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (1, 'Canto de edificação');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (2, 'Entroncamento de estrada');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (3, 'Cerca ou muro');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (4, 'Elemento identificável no solo');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (5, 'Elemento não identificável no solo');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (6, 'Topo de vegetação');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (7, 'Abaixo de vegetação');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (9999, 'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_ref (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ref_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_ref OWNER TO postgres;

INSERT INTO dominios.tipo_ref (code,code_name) VALUES (1,'Altimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (2,'Planimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (3,'Planialtimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (4,'Gravimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.sistema_geodesico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT sistema_geodesico_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.sistema_geodesico OWNER TO postgres;

INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (1,'SAD-69');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (2,'SIRGAS2000');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (3,'WGS-84');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (4,'Córrego Alegre');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (5,'Astro Chuá');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (6,'SAD-69 (96)');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (99,'Outra referência');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.referencial_altim (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencial_altim_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.referencial_altim OWNER TO postgres;

INSERT INTO dominios.referencial_altim (code,code_name) VALUES (1,'Torres');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (2,'Imbituba');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (3,'Santana');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (99,'Outra referência');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.metodo_posicionamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT metodo_posicionamento_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.metodo_posicionamento OWNER TO postgres;

INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (1,'Posicionamento por ponto preciso (PPP)');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (2,'Real Time Kinematic (RTK)');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (3,'Semi-cinemático');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (4,'Relativo Estático');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (5,'Relativo Cinemático');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (6,'Absoluto');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_medicao_altura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_medicao_altura_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_medicao_altura OWNER TO postgres;

INSERT INTO dominios.tipo_medicao_altura (code,code_name) VALUES (1,'Base de montagem');
INSERT INTO dominios.tipo_medicao_altura (code,code_name) VALUES (2,'Altura inclinada');
INSERT INTO dominios.tipo_medicao_altura (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.referencia_medicao_altura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencia_medicao_altura_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.referencia_medicao_altura OWNER TO postgres;

INSERT INTO dominios.referencia_medicao_altura (code,code_name) VALUES (1,'Nível do solo');
INSERT INTO dominios.referencia_medicao_altura (code,code_name) VALUES (2,'Nível do objeto');
INSERT INTO dominios.referencia_medicao_altura (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.orbita (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT orbita_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.orbita OWNER TO postgres;

INSERT INTO dominios.orbita (code,code_name) VALUES (1,'Ultra Rápida (predita)');
INSERT INTO dominios.orbita (code,code_name) VALUES (2,'Ultra Rápida (observada)');
INSERT INTO dominios.orbita (code,code_name) VALUES (3,'Rápida');
INSERT INTO dominios.orbita (code,code_name) VALUES (4,'Final');
INSERT INTO dominios.orbita (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.orbita (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_pto_ref_geod_topo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pto_ref_geod_topo_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_pto_ref_geod_topo OWNER TO postgres;

INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (0,'Desconhecido');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (1,'Vértice de triangulação - VT');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (2,'Referência de nível - RN');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (3,'Estação gravimétrica - EG');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (4,'Estação de poligonal - EP');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (5,'Ponto astronômico - PA');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (6,'Ponto barométrico - B');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (7,'Ponto trigonométrico - RV');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (8,'Ponto de satélite - SAT');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (99,'Outros');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_marco_limite (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_marco_limite_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_marco_limite OWNER TO postgres;

INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (3,'Municipal');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (23,'Estadual');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (24,'Internacional secundário');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (25,'Internacional de referência');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (26,'Internacional principal');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (99,'Outros');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.rede_referencia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT rede_referencia_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.rede_referencia OWNER TO postgres;

INSERT INTO dominios.rede_referencia (code,code_name) VALUES (0,'Desconhecida');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (2,'Estadual');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (3,'Municipal');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (14,'Nacional');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (15,'Privada');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.referencial_grav (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencial_grav_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.referencial_grav OWNER TO postgres;

INSERT INTO dominios.referencial_grav (code,code_name) VALUES (0,'Desconhecido');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (1,'Potsdam 1930');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (2,'IGSN71');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (3,'Absoluto');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (4,'Local');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (5,'RGFB');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.situacao_marco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_marco_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.situacao_marco OWNER TO postgres;

INSERT INTO dominios.situacao_marco (code,code_name) VALUES (0,'Desconhecida');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (1,'Bom');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (2,'Destruído');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (3,'Destruído sem chapa');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (4,'Destruí­do com chapa danificada');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (5,'Não encontrado');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (6,'Não visitado');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (7,'Não construí­do');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.insumo_medicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT insumo_medicao_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.insumo_medicao OWNER TO postgres;

INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (1,'Fototriangulação');
INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (2,'Carta Topográfica');
INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (3,'Ortoimagem');
INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (9999,'A SER PREENCHIDO');


CREATE SCHEMA bpc;

CREATE TABLE bpc.controle_medicao_a(
  id SERIAL NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL,
  total_pontos_aprovados smallint NOT NULL DEFAULT 0,
  total_pontos_em_avaliacao smallint NOT NULL DEFAULT 0,
  total_pontos_previstos smallint NOT NULL DEFAULT 0,
  lote VARCHAR(255),
  geom geometry(Polygon,4674) NOT NULL
);
CREATE INDEX controle_medicao_a_geom ON bpc.controle_medicao_a USING gist (geom);
ALTER TABLE bpc.controle_medicao_a OWNER TO postgres;

CREATE TABLE bpc.ponto_controle_p(
  id SERIAL NOT NULL PRIMARY KEY,
  cod_ponto VARCHAR(255) UNIQUE NOT NULL,
  data_rastreio DATE NOT NULL,
  tipo_ref SMALLINT NOT NULL REFERENCES dominios.tipo_ref(code) DEFAULT 9999,
  latitude REAL, --graus decimais
  longitude REAL, --graus decimais
  norte FLOAT,
  leste FLOAT,
  altitude_ortometrica REAL, --metros
  altitude_geometrica REAL,  --metros
  sistema_geodesico SMALLINT NOT NULL REFERENCES  dominios.sistema_geodesico(code) DEFAULT 9999,
  outra_ref_plan VARCHAR(255),
  referencial_altim SMALLINT NOT NULL REFERENCES  dominios.referencial_altim(code) DEFAULT 9999,
  outro_ref_alt VARCHAR(255),
  fuso VARCHAR(255),
  meridiano_central VARCHAR(255),
  tipo_situacao SMALLINT NOT NULL REFERENCES dominios.tipo_situacao(code) DEFAULT 9999,
  reserva BOOLEAN NOT NULL DEFAULT FALSE,
  lote VARCHAR(255),
  latitude_planejada REAL, --graus decimais
  longitude_planejada REAL, --graus decimais
  medidor VARCHAR(255),
  inicio_rastreio TIMESTAMP WITH TIME ZONE,
  fim_rastreio TIMESTAMP WITH TIME ZONE,
  classificacao_ponto SMALLINT NOT NULL REFERENCES dominios.classificacao_ponto(code) DEFAULT 9999,
  observacao VARCHAR(255),
  metodo_posicionamento SMALLINT NOT NULL REFERENCES dominios.metodo_posicionamento(code) DEFAULT 9999,
  ponto_base VARCHAR(255),
  materializado BOOLEAN NOT NULL DEFAULT FALSE,
  altura_antena REAL, --metros
  tipo_medicao_altura SMALLINT NOT NULL REFERENCES dominios.tipo_medicao_altura(code) DEFAULT 9999,
  referencia_medicao_altura SMALLINT NOT NULL REFERENCES dominios.referencia_medicao_altura(code) DEFAULT 9999,
  altura_objeto REAL, --metros
  mascara_elevacao REAL, --graus decimais
  taxa_gravacao REAL, --segundos
  modelo_gps VARCHAR(255),
  modelo_antena VARCHAR(255),
  numero_serie_gps VARCHAR(255),
  numero_serie_antena VARCHAR(255),
  modelo_geoidal VARCHAR(255),
  precisao_horizontal_esperada REAL, --metros
  precisao_vertical_esperada REAL, --metros
  freq_processada VARCHAR(255),
  data_processamento DATE,
  orbita SMALLINT NOT NULL REFERENCES dominios.orbita(code) DEFAULT 9999,
  orgao_executante VARCHAR(255),
  projeto VARCHAR(255),
  engenheiro_responsavel VARCHAR(255),
  crea_engenheiro_responsavel VARCHAR(255),
  cpf_engenheiro_responsavel VARCHAR(255),
  geometria_aproximada BOOLEAN NOT NULL DEFAULT FALSE,
  tipo_pto_ref_geod_topo SMALLINT NOT NULL REFERENCES dominios.tipo_pto_ref_geod_topo(code) DEFAULT 9999,
  tipo_marco_limite SMALLINT NOT NULL REFERENCES dominios.tipo_marco_limite(code) DEFAULT 9999,
  rede_referencia SMALLINT NOT NULL REFERENCES dominios.rede_referencia(code) DEFAULT 9999,
  referencial_grav SMALLINT NOT NULL REFERENCES dominios.referencial_grav(code) DEFAULT 9999,
  situacao_marco SMALLINT NOT NULL REFERENCES dominios.situacao_marco(code) DEFAULT 9999,
  data_visita DATE,
  valor_gravidade REAL,
  possui_monografia BOOLEAN NOT NULL DEFAULT FALSE,
  numero_fotos SMALLINT,
  possui_croqui BOOLEAN NOT NULL DEFAULT FALSE,
  possui_arquivo_rastreio BOOLEAN NOT NULL DEFAULT FALSE,
  endereco_imagem_lateral_1 VARCHAR(255),
  endereco_imagem_lateral_2 VARCHAR(255),
  endereco_imagem_lateral_3 VARCHAR(255),
  endereco_imagem_lateral_4 VARCHAR(255),
  endereco_imagem_aerea VARCHAR(255),
  endereco_monografia VARCHAR(255),
  endereco_croqui VARCHAR(255),
  endereco_rinex VARCHAR(255),
  geom geometry(POINT,4674) NOT NULL
);
CREATE INDEX ponto_controle_p_geom ON bpc.ponto_controle_p USING gist (geom);
ALTER TABLE bpc.ponto_controle_p OWNER TO postgres;

CREATE TABLE bpc.ponto_controle_virtual_p(
  id SERIAL NOT NULL PRIMARY KEY,
  cod_ponto VARCHAR(255) UNIQUE NOT NULL,
  tipo_ref SMALLINT NOT NULL REFERENCES dominios.tipo_ref(code) DEFAULT 9999,
  latitude REAL, --graus decimais
  longitude REAL, --graus decimais
  altitude_ortometrica REAL, --metros
  sistema_geodesico SMALLINT NOT NULL REFERENCES  dominios.sistema_geodesico(code) DEFAULT 9999,
  outra_ref_plan VARCHAR(255),
  referencial_altim SMALLINT NOT NULL REFERENCES  dominios.referencial_altim(code) DEFAULT 9999,
  outro_ref_alt VARCHAR(255),
  lote VARCHAR(255),
  medidor VARCHAR(255),
  classificacao_ponto SMALLINT NOT NULL REFERENCES dominios.classificacao_ponto(code) DEFAULT 9999,
  observacao VARCHAR(255),
  insumo_medicao SMALLINT NOT NULL REFERENCES dominios.insumo_medicao(code) DEFAULT 9999,
  software VARCHAR(255),
  identificacao_insumo VARCHAR(255),
  acuracia_planimetrica_insumo REAL, --metros
  acuracia_altimetrica_insumo REAL, --metros
  descricao_insumo VARCHAR(255),
  orgao_executante VARCHAR(255),
  projeto VARCHAR(255),
  engenheiro_responsavel VARCHAR(255),
  crea_engenheiro_responsavel VARCHAR(255),
  geom geometry(POINTZ,4674) NOT NULL
);
CREATE INDEX ponto_controle_virtual_p_geom ON bpc.ponto_controle_virtual_p USING gist (geom);
ALTER TABLE bpc.ponto_controle_virtual_p OWNER TO postgres;

CREATE TABLE public.layer_styles
(
  id serial NOT NULL,
  f_table_catalog character varying,
  f_table_schema character varying,
  f_table_name character varying,
  f_geometry_column character varying,
  stylename character varying(255),
  styleqml text,
  stylesld xml,
  useasdefault boolean,
  description text,
  owner character varying(30),
  ui xml,
  update_time timestamp without time zone DEFAULT now(),
  CONSTRAINT layer_styles_pkey PRIMARY KEY (id)
);

ALTER TABLE public.layer_styles OWNER TO postgres;
