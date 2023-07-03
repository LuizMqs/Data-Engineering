# Data-Engineering


# **Fonte dos dados:**

**DATASUS - Sistema de Informação sobre Mortalidade (SIM)**

As classificações de raça e sexo estão de acordo com o IBGE (Instituto Brasileiro de Geografia e Estatística). Divididas entre: Parda, Preta, Branca, Amarela e Indígena para as raças e Masculino ou Feminino para o sexo

**DATASUS - Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde (CID-10).**

Os casos de suicídios (lesões autoprovocadas) são classificados de acordo(CID) entre os códigos X600 e X850.

# **Dicionário das variáveis:**

**Sistema de Informação sobre Mortalidade (SIM):**

As variáveis SEXO e RACACOR seguem as classificações de acordo com o Instituto Brasileiro de Geografia e Estatística (IBGE).

**estados**: Sigla de todos estados da federação brasileira (27).

**ano**: ano dos dados registrados (2010 - 2019).

**mes**: mês dos óbitos registrados. (1 - 12).

**DTOBITO**: Data registrada do óbito. (year-month-day).

**SEXO**: Classificação do sexo. (Masculino ou Feminino).

**RACACOR**: Classificação de raça. (Parda, Branca, Preta, Indígena e Amarela).

**CAUSASBAS**: Causa básica da morte de acordo com a Classificação Internacional de Doenças (CID-10)

**LOCOCOR**: Local de ocorrência do óbito. (Via pública, Domicílio, Hospital, Outros, Outro estabelecimento de saúde).

* Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde - CID 10:

**SUBCAT**: Códigos da subcategoria do CID-10.

**DESCRICAO**: Descrição da doença ou do problema relacionado à saúde.



**Coleta e Limpeza dos dados:**

**Banco de Dados:**

**Análise Exploratória:**