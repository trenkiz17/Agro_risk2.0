-- Estrutura para instalações NOVAS. Não altera tabelas que já existem.
-- Não contém usuários de exemplo nem senhas em texto simples.
-- Para instalações existentes, verifique as colunas e faça migrações com backup.
CREATE DATABASE IF NOT EXISTS agrorisk
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agrorisk;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  telefone VARCHAR(20) NULL,
  cpf VARCHAR(14) NULL,
  data_nascimento DATE NULL,
  estado VARCHAR(100) NULL,
  cidade VARCHAR(100) NULL,
  idioma VARCHAR(50) NULL DEFAULT 'Português'
);

CREATE TABLE IF NOT EXISTS propriedades (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  estado VARCHAR(100) NOT NULL,
  observacao TEXT NULL,
  area FLOAT NOT NULL,
  perimetro FLOAT NOT NULL DEFAULT 0,
  latitude FLOAT NULL,
  longitude FLOAT NULL,
  geojson TEXT NULL,
  CONSTRAINT fk_prop_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS safras (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  propriedade_id INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  cultura VARCHAR(100) NOT NULL,
  ano_safra VARCHAR(20) NOT NULL,
  area_plantada DECIMAL(10,2) NOT NULL,
  data_plantio DATE NULL,
  data_colheita DATE NULL,
  produtividade DECIMAL(10,2) NULL,
  custo_total DECIMAL(10,2) NULL,
  observacoes TEXT NULL,
  status VARCHAR(50) NULL DEFAULT 'Planejamento',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_safra_prop FOREIGN KEY (propriedade_id) REFERENCES propriedades(id)
);

-- Extensão opcional da Estimativa Agrícola Avançada (2026).
-- Tabela própria; não modifica as colunas de safras existentes.
CREATE TABLE IF NOT EXISTS safra_parametros (
  safra_id INT NOT NULL PRIMARY KEY,
  cultivar VARCHAR(100) NULL,
  idade_lavoura_anos FLOAT NULL,
  altitude_m FLOAT NULL,
  irrigacao VARCHAR(20) NULL,
  area_util_percentual FLOAT NULL,
  data_emergencia DATE NULL,
  data_florada DATE NULL,
  data_frutificacao DATE NULL,
  ciclo_min_dias INT NULL,
  ciclo_max_dias INT NULL,
  florada_colheita_min_dias INT NULL,
  florada_colheita_max_dias INT NULL,
  produtividade_baixa_sc_ha FLOAT NULL,
  produtividade_media_sc_ha FLOAT NULL,
  produtividade_alta_sc_ha FLOAT NULL,
  fonte_parametros VARCHAR(350) NULL,
  atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_parametros_safra FOREIGN KEY (safra_id)
      REFERENCES safras(id) ON DELETE CASCADE
);
