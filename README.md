# Dashboard de Vendas de Veículos Elétricos

## Sobre o Projeto

### Título e Tema
Dashboard Interativo de Análise de Vendas Globais de Veículos Elétricos (2010-2023)

### Justificativa da Escolha do Tema
A escolha deste tema se justifica pela crescente relevância da mobilidade elétrica no contexto global de sustentabilidade e transição energética. Com a intensificação das políticas climáticas e o aumento dos investimentos em tecnologias limpas, o mercado de veículos elétricos tem apresentado crescimento exponencial nos últimos anos.

Este dashboard permite visualizar e analisar a evolução do mercado de VEs ao longo de 13 anos, o papel de diferentes países na adoção dessa tecnologia, tendências e padrões de crescimento, além da concentração de mercado e identificação dos líderes globais.

O tema é relevante tanto do ponto de vista ambiental quanto econômico, permitindo compreender como diferentes nações estão respondendo aos desafios da descarbonização do transporte.

---

## Fonte de Dados

### API Utilizada
Our World in Data (OWID) - Electric Car Sales Dataset

URL: https://github.com/owid/owid-datasets/raw/master/datasets/Electric%20car%20sales%20-%20by%20country/

Formato: CSV

Atualização: Dados atualizados automaticamente a cada 7 dias via cache inteligente

### Descrição dos Dados
O dataset contém informações sobre vendas de veículos elétricos em nível global e por país:

- Período coberto: 2010 a 2023
- Países/Entidades: 35 países mais agregações regionais (World, Europe, etc.)
- Total de registros: aproximadamente 418 entradas
- Variável principal: Electric cars sold (número de carros elétricos vendidos anualmente)

Os dados são coletados pela Our World in Data, organização de pesquisa sem fins lucrativos focada em problemas globais, e representam vendas anuais de veículos elétricos puros (BEV) e híbridos plug-in (PHEV).

---

## Perguntas-Chave

Este dashboard foi desenvolvido para responder às seguintes questões:

1. Qual foi a evolução global das vendas de veículos elétricos nos últimos 13 anos?
   - Análise de crescimento exponencial e identificação de pontos de inflexão

2. Quais são os principais mercados de veículos elétricos no mundo?
   - Identificação dos top 10 países e sua participação no mercado global

3. Como diferentes países se comparam em termos de adoção de VEs?
   - Comparação temporal entre países selecionados
   - Análise de market share e trajetórias de crescimento

4. Qual é a taxa de crescimento anual do mercado?
   - Crescimento ano a ano
   - Períodos de aceleração e desaceleração

5. Como o mercado se concentra geograficamente?
   - Análise de concentração de mercado
   - Papel da China, EUA e Europa na transição elétrica

6. Quais padrões e tendências podem ser identificados nos dados históricos?
   - Impacto de eventos globais
   - Aceleração recente versus crescimento histórico

---

## Como Rodar o Projeto Localmente

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instruções

1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Dashboard
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install streamlit pandas plotly requests
```

3. Execute o dashboard
```bash
streamlit run src/app.py
```

Ou alternativamente:
```bash
python -m streamlit run src/app.py
```

4. Acesse no navegador
O dashboard abrirá automaticamente em http://localhost:8501

### Estrutura do Projeto
```
Dashboard/
├── src/
│   └── app.py              # Aplicação principal
├── data/
│   └── ev_sales_global.csv # Cache local dos dados da API
├── requirements.txt        # Dependências do projeto
└── README.md              # Documentação
```

---

## Capturas de Tela do Dashboard

### 1. Visão Geral Global
![Visão Geral](screenshots/visao_geral.png)

Contexto: Esta tela fornece um panorama completo do mercado global de VEs, destacando as métricas mais importantes através de quatro indicadores principais: Total de Vendas Globais, Vendas em 2023, Número de Países com dados disponíveis, e Crescimento Médio Anual. O gráfico de barras horizontal apresenta os Top 10 mercados, com a China em destaque como líder absoluto. As métricas permitem aos usuários compreender rapidamente a magnitude do mercado e a concentração geográfica das vendas.

---

### 2. Tendências Temporais
![Tendências](screenshots/tendencias.png)

Contexto: A aba de tendências permite identificar padrões temporais através de um gráfico de linha mostrando a evolução exponencial das vendas globais de 2010 a 2023. A visualização inclui uma anotação destacando a aceleração pós-pandemia em 2020. A seção também apresenta uma tabela detalhada com crescimento ano a ano e um gráfico de barras comparando vendas por período (2010-2015, 2016-2020, 2021-2023), evidenciando como o mercado acelerou dramaticamente nos últimos anos, com crescimento de mais de 100x desde 2010.

---

### 3. Comparação Entre Países
![Comparação](screenshots/comparacao.png)

Contexto: Esta é a seção mais interativa do dashboard, onde usuários podem comparar até 5 países simultaneamente através de um gráfico de linhas multicolorido. Os filtros na sidebar (multiselect de países e slider de anos) permitem análises personalizadas do período de interesse. A visualização inclui uma tabela detalhada com dados ano a ano e um gráfico de pizza mostrando participação de mercado, revelando a dominância chinesa no setor. Métricas individuais por país são exibidas lateralmente, mostrando totais e crescimento percentual no período selecionado.

---

### 4. Explorador de Dados
![Dados](screenshots/dados.png)

Contexto: Esta aba permite exploração granular dos dados brutos através de três opções de visualização selecionáveis via botões de rádio. A primeira opção (Dados Globais) apresenta uma tabela com vendas mundiais anuais e crescimento percentual. A segunda opção (Dados por País) oferece um seletor dropdown para escolher um país específico e visualizar sua evolução detalhada com métricas calculadas incluindo crescimento percentual e variação absoluta. A terceira opção (Download Completo) exibe um preview do dataset com informações resumidas sobre sua estrutura, período coberto, número de registros e fonte dos dados.

---

### 5. Sidebar com Filtros
![Sidebar](screenshots/sidebar.png)

Contexto: A sidebar centraliza todos os controles interativos do dashboard em um painel lateral com fundo escuro. O título "Filtros" separa visualmente a área de controles do conteúdo principal. O multiselect de países permite selecionar múltiplas nações para comparação (padrão: China, United States, Germany). O slider de período possibilita ajustar o intervalo temporal de análise (padrão: 2015 até o ano mais recente). O botão "Atualizar Dados da API" permite forçar nova busca de dados, limpando o cache local. Os filtros aplicam-se globalmente, afetando principalmente a aba de Comparação.

---

## Tecnologias Utilizadas

- Streamlit: Framework para criação de dashboards interativos
- Pandas: Manipulação e análise de dados
- Plotly: Visualizações interativas e gráficos
- Requests: Cliente HTTP para consumo da API
- Python 3.12: Linguagem de programação

---

## Requisitos Funcionais Atendidos

### Conceitos de Ciência de Dados
- Coleta via API: Busca automatizada de dados do Our World in Data
- Armazenamento local: Cache de dados em arquivo CSV (data/ev_sales_global.csv)
- Processamento e limpeza: Remoção de valores nulos, conversão de tipos, criação de colunas derivadas
- Análise exploratória: Múltiplas visualizações, KPIs, insights e métricas calculadas

### Interface e Dashboard
- Streamlit: 100% construído com Streamlit
- Interatividade: 5 elementos interativos (multiselect, slider, radio, selectbox, button)
- Layout organizado: 4 tabs temáticas, títulos claros, KPIs destacados, explicações contextuais

---

## Funcionalidades

- Visualização de métricas principais (KPIs)
- Análise geográfica com top 10 países
- Gráficos de tendências temporais
- Comparação interativa entre países
- Filtros dinâmicos (países e período)
- Exploração de dados brutos
- Atualização automática via API (cache de 7 dias)
- Interface em modo escuro
- Layout responsivo

---

## Equipe

[Adicione aqui os nomes dos membros da equipe]

---

## Licença

[Adicione informações sobre licença, se aplicável]

---

## Contato

[Adicione informações de contato]

---

Nota: Para adicionar as capturas de tela, crie uma pasta "screenshots" na raiz do projeto e salve as imagens com os nomes: visao_geral.png, tendencias.png, comparacao.png, dados.png, sidebar.png
