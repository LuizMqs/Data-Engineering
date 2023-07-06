# **Fonte dos dados:**

**DATASUS - Sistema de Informação sobre Mortalidade (SIM)**

As classificações de raça e sexo estão de acordo com o IBGE (Instituto Brasileiro de Geografia e Estatística). Divididas entre: Parda, Preta, Branca, Amarela e Indígena para as raças e Masculino ou Feminino para o sexo

**DATASUS - Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde (CID-10).**

Os casos de suicídios (lesões autoprovocadas) são classificados de acordo(CID) entre os códigos X600 e X850.

# **Dicionário das variáveis:**

**Sistema de Informação sobre Mortalidade (SIM):**

As variáveis gender e race seguem as classificações de acordo com o Instituto Brasileiro de Geografia e Estatística (IBGE).

**state**: Sigla de todos estados da federação brasileira (27).

**year**: ano dos dados registrados (2010 - 2019).

**month**: mês dos óbitos registrados. (1 - 12).

**date_of_death**: Data registrada do óbito. (year-month-day).

**gender**: Classificação do sexo. (Masculino ou Feminino).

**race**: Classificação de raça. (Parda, Branca, Preta, Indígena e Amarela).

**death_cause**: Causa básica da morte de acordo com a Classificação Internacional de Doenças (CID-10)

**place_of_death**: Local de ocorrência do óbito. (Via pública, Domicílio, Hospital, Outros, Outro estabelecimento de saúde).

**Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde - CID 10:**

**id**: Códigos da subcategoria do CID-10.

**description**: Descrição da doença ou do problema relacionado à saúde.


**Coleta e limpeza dos dados.**

Fonte: DATASUS - Sistema de Informação sobre Mortalidade (SIM)

Para a limpeza de dados iniciamos uma análise exploratória a procura de inconsistências e dados faltantes.

Na tabela de idade (age) encontramos 10800 valores nulos, representando 9.74% da nossa base total. Decidimos renomear os valores nulos com N/A.

Em relação aos valores nulos da coluna gênero (gender) calculamos a proporção de cada gênero na tabela e preenchemos os valores faltantes. Aplicamos o mesmo princípio na coluna raça (race).

Fonte: DATASUS - Classificação Estatística Internacional de Doenças e Problemas Relacionados à Saúde (CID-10).

Selecionamos apenas os casos de suicídios (lesões autoprovocadas) classificados de acordo (CID) entre os códigos X600 e X850.

**Banco de dados:**

Tabela "suicides":

-   Esta tabela armazena informações sobre suicídios.
-   Possui as seguintes colunas:
    -   "id": Um UUID gerado automaticamente que serve como identificador único para cada registro.
    -   "state": Uma sigla de dois caracteres representando o estado em que o suicídio ocorreu.
    -   "year": O ano em que o suicídio ocorreu, representado como uma sequência de quatro caracteres.
    -   "month": O mês em que o suicídio ocorreu, representado como uma sequência de dois caracteres.
    -   "date_of_death": A data em que o suicídio ocorreu, representada como uma sequência de dez caracteres.
    -   "gender": O gênero da pessoa que cometeu o suicídio, representado como uma sequência de nove caracteres.
    -   "race": A raça da pessoa que cometeu o suicídio, representada como uma sequência de dez caracteres.
    -   "death_cause": A causa da morte, representada como uma sequência de quatro caracteres.
    -   "place_of_death": O local onde ocorreu o suicídio, representado como um texto.
    -   "age": A idade da pessoa que cometeu o suicídio, representada como uma sequência de cinco caracteres.

Tabela "death_causes":

-   Esta tabela armazena informações sobre as causas de morte.
-   Possui as seguintes colunas:
    -   "id": Uma sequência de quatro caracteres que representa a causa de morte.
    -   "description": Uma descrição textual da causa de morte.

Tabela "macro_regions_populations":

-   Esta tabela armazena informações sobre as populações das macro-regiões.
-   Possui as seguintes colunas:
    -   "macro_region": O nome da macro-região.
    -   As colunas restantes representam a população total para cada ano de 2010 a 2022.

Tabela "idh":

-   Esta tabela armazena informações sobre o Índice de Desenvolvimento Humano (IDH).
-   Possui as seguintes colunas:
    -   "id": Um UUID gerado automaticamente que serve como identificador único para cada registro.
    -   "reference_year": O ano de referência do IDH.
    -   "idh": O valor do IDH.
    -   "female_idh": O valor do IDH para mulheres.
    -   "male_idh": O valor do IDH para homens.
    -   "life_expectancy": A expectativa de vida.
    -   "female_life_expectancy": A expectativa de vida para mulheres.
    -   "male_life_expectancy": A expectativa de vida para homens.

Tabela "states":

-   Esta tabela armazena informações sobre os estados.
-   Possui as seguintes colunas:
    -   "id": Um UUID gerado automaticamente que serve como identificador único para cada registro.
    -   "state_abbreviation": A sigla do estado.
    -   "state": O nome do estado.
    -   "region": A região a que o estado pertence.
    -   "year": O ano dos dados.
    -   "number_of_deaths": O número de mortes.

Todas as tabelas possuem chave primária para garantir a unicidade do registro no banco de dados.

Além disso, a tabela "suicides" tem uma restrição de chave estrangeira ("fk_suicides_death_causes") na coluna "death_cause", que faz referência à tabela "death_causes" na coluna "id", garantindo que as causas de morte existam na tabela "death_causes".

**Análise de dados:**

Distribuição dos suicídios por idade:

-   Foram criados intervalos de idades para categorizar os dados de suicídios de acordo com faixas etárias. Isso permite uma análise da distribuição dos suicídios em relação à idade.

Tabela de população total:

-   Foi criada uma tabela contendo os valores da população total entre 2011 e 2016. Esses valores foram estimados com base na taxa de crescimento da população brasileira e nos dados do censo de 2010 e 2022. Isso permite analisar a relação entre a população e os suicídios ao longo do tempo.

Taxa de suicídio da população brasileira:

-   Foi calculada a taxa de suicídio da população brasileira em relação ao tempo. Isso envolveu a análise do número de suicídios em relação à população total para determinar a incidência de suicídios na população.

Total de suicídios por gênero, raça e idade:

-   Foram calculados os totais de suicídios com base nos dados de gênero, raça e idade. Isso permite examinar a distribuição dos suicídios nessas categorias específicas.

Principais lesões autoinfligidas:

-   Foram identificadas as principais lesões autoinfligidas com base nos dados disponíveis. Isso ajuda a compreender os métodos mais comuns utilizados em casos de suicídio.

Quantidade de suicídios ao longo do tempo nas macrorregiões:

-   Foi calculada a quantidade de suicídios ao longo do tempo em cada macrorregião. Isso permite identificar possíveis variações regionais nos números de suicídios.

Taxa de suicídio e IDH ao longo do tempo na população brasileira:

-   Foi realizada uma análise da taxa de suicídio em relação ao Índice de Desenvolvimento Humano (IDH) ao longo do tempo na população brasileira. Isso permite investigar possíveis correlações entre indicadores socioeconômicos e suicídios.