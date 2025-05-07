INSERT INTO estabelecimentos(
        cnpj_basico,
        cnpj_ordem,
        cnpj_dv,nome_fantasia,
        situacao_cadastral,
        tipo_logradouro,
        logradouro,
        numero,
        complemento,
        bairro,
        cep,
        uf,municipio,
        ddd_1,
        telefone_1,
        ddd_2,
        telefone_2,
        correio_eletronico
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
