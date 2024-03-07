# Webscraping utilizando Python e Selenium
###### Como extrair dados da Secretaria de Segurança Pública do Estado de São Paulo de forma dinâmica.

**Tecnologias utilizadas:**
- Python
- Selenium
- VS Code

**Dados disponíveis em:** 
**https://www.ssp.sp.gov.br/estatistica/dados-mensais**

*Todos os scripts, logs, ambiente virtual e pacotes estão separados por pastas.*

#### Resultado Final - Código em execução - Extração de Dados Automática
[![Script](https://s9.gifyu.com/images/SF56c.gif "Script")](https://s9.gifyu.com/images/SF56c.gif "Script")

#### Objetivo 
- Criar um processo automatizado para extração de dados de forma dinâmica da SSP, sem a necessidade de interação humana.

Automação em Python extraindo todos os dados para cada Ano, Região, Município e DP:


#### Perguntas válidas para o projeto
- Por qual motivo optou por **Selenium** em vez de utilizar **Beautiful Soup**?
R: Os elementos gerados pela página foram feitos utilizando JavaScript, parte desses elementos não conseguem ser processados diretamente com a biblioteca Beatiful Soup, por esse motivo, optou-se por Selenium (obs: uma alternativa válida, seria utilizar o Selenium apenas para carregar as páginas e interagir com os elementos, e em seguida, coletar os dados utilizando Beautiful Soup).

#### Principais desafios durante o desenvolvimento:
- Criar uma lógica para seleção de todos os itens do menu de opções de forma dependente. Conforme exemplo abaixo:

1. Script seleciona 1 região (Grande SP, por exemplo)
2. Seleciona 1 município (Diadema, por exemplo)
3. Seleciona 1 delegacia (DP01 Diadema)
4. Os dados apresentados na tabela são coletados. 

A lógica para solucionar o problema foi:
- Criar um for loop aninhado para que seja escolhido cada uma das possibilidades de seleção. Os dados são coletados e armazenados em formato .csv localmente. (Futuramente, essa solução será adaptada para a AWS).

Conforme exemplo anterior, tabela é apresentada após a escolha de ao menos 1 item.
[![Lista de rolagem dependente](https://s9.gifyu.com/images/SF5uE.gif "Lista de rolagem dependente")]("Lista de rolagem dependente")
