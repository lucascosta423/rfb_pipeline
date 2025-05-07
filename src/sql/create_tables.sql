-- Tabela empresas
CREATE TABLE IF NOT EXISTS empresas (
    cnpj_basico TEXT,
    razao_social_nome_empresarial TEXT
);

-- Tabela socios
CREATE TABLE IF NOT EXISTS socios (
    cnpj_basico TEXT,
    identificador_de_socio TEXT,
    nome_socio_ou_razao_social TEXT,
    cpf_socio TEXT,
    representante_legal TEXT,
    nome_representante TEXT
);

-- Tabela estabelecimentos
CREATE TABLE IF NOT EXISTS estabelecimentos (
    cnpj_basico TEXT,
    cnpj_ordem TEXT,
    cnpj_dv TEXT,
    nome_fantasia TEXT,
    situacao_cadastral TEXT,
    data_situacao_cadastral TEXT,
    motivo_situacao_cadastral TEXT,
    nome_cidade_exterior TEXT,
    pais TEXT,
    data_inicio_atividade TEXT,
    cnae_principal TEXT,
    cnae_secundaria TEXT,
    tipo_logradouro TEXT,
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cep TEXT,
    uf TEXT,
    municipio TEXT,
    ddd_1 TEXT,
    telefone_1 TEXT,
    ddd_2 TEXT,
    telefone_2 TEXT,
    correio_eletronico TEXT
);

-- Tabela municipio
CREATE TABLE IF NOT EXISTS municipio (
    codigo TEXT,
    descricao TEXT
);