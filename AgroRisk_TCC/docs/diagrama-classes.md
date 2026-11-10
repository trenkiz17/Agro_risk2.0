# Diagrama de classes — AgroRisk

Este diagrama apresenta as **Models de domínio** da versão Flask analisada: `Usuario`, `Propriedade`, `Safra` e `SafraParametros`. As relações representam **chaves estrangeiras**, não composição de objetos implementada explicitamente no código. O GitHub renderiza o gráfico abaixo com Mermaid.

```mermaid
classDiagram
    direction LR

    class Usuario {
        +int id
        +string nome
        +string email
        +string senha
        +string telefone
        +string cpf
        +date data_nascimento
        +string estado
        +string cidade
        +string idioma
        +salvar()
        +atualizar()
        +deletar()
        +listar_todos()
        +buscar_por_id(id)
        +buscar_por_email(email)
    }

    class Propriedade {
        +int id
        +int usuario_id
        +string nome
        +string cidade
        +string estado
        +string observacao
        +float area
        +float perimetro
        +float latitude
        +float longitude
        +text geojson
        +salvar()
        +atualizar()
        +deletar()
        +listar_todos()
        +buscar_por_id(id)
    }

    class Safra {
        +int id
        +int propriedade_id
        +string nome
        +string cultura
        +string ano_safra
        +decimal area_plantada
        +date data_plantio
        +date data_colheita
        +decimal produtividade
        +decimal custo_total
        +text observacoes
        +string status
        +datetime created_at
        +salvar()
        +atualizar()
        +deletar()
        +listar_todos()
        +buscar_por_id(id)
    }

    class SafraParametros {
        +int safra_id PK/FK
        +string cultivar
        +float idade_lavoura_anos
        +float altitude_m
        +string irrigacao
        +float area_util_percentual
        +date data_emergencia
        +date data_florada
        +date data_frutificacao
        +int ciclo_min_dias
        +int ciclo_max_dias
        +float produtividade_baixa_sc_ha
        +float produtividade_media_sc_ha
        +float produtividade_alta_sc_ha
        +datetime atualizado_em
        +to_dict()
    }

    Usuario "1" --> "0..*" Propriedade : usuario_id (FK)
    Propriedade "1" --> "0..*" Safra : propriedade_id (FK)
    Safra "1" --> "0..1" SafraParametros : safra_id (FK)
```

## Correspondência no código

| Classe | Arquivo | Tabela MySQL | Relação |
| --- | --- | --- | --- |
| `Usuario` | `backend/models/usuario.py` | `usuarios` | Identificado por `id` |
| `Propriedade` | `backend/models/propriedade.py` | `propriedades` | `usuario_id` referencia `usuarios.id` |
| `Safra` | `backend/models/safra.py` | `safras` | `propriedade_id` referencia `propriedades.id` |
| `SafraParametros` | `backend/models/safra_parametros.py` | `safra_parametros` | `safra_id` é PK e FK para `safras.id` |

A herança de `db.Model` está presente nas quatro classes, embora não esteja desenhada como uma entidade de domínio, porque faz parte da infraestrutura do SQLAlchemy.

**Nota de coerência:** os campos `produtividade` e `custo_total` permanecem na Model por compatibilidade com o banco, mesmo que previsões de produtividade e lucro tenham sido retiradas das telas e relatórios.
