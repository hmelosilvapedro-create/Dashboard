# ⚡ Dashboard de Vendas de Carros Elétricos

Dashboard interativo para análise de vendas globais de carros elétricos (2010-2023).

## Como usar

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

Acesse em: http://localhost:8501

## Requisitos Atendidos

### ✅ Conceitos de Ciência de Dados
- **Coleta via API**: Busca dados da API do Our World in Data
- **Armazenamento local**: Dados salvos em CSV após coleta
- **Processamento/Limpeza**: Filtragem de valores nulos, conversão de tipos
- **Análise exploratória**: Múltiplas visualizações e métricas

### ✅ Interface e Dashboard
- **Streamlit**: 100% construído com Streamlit
- **Interatividade**: 4+ elementos interativos (multiselect, slider, radio, selectbox)
- **Layout organizado**: 4 tabs com títulos claros, KPIs e explicações

## Dados

- **Fonte**: Our World in Data API
- **Período**: 2010-2023
- **Países**: 35 entidades
- **Atualização**: Automática a cada 7 dias

## Funcionalidades

- Visão geral com métricas principais
- Análise de tendências temporais
- Comparação entre países
- Download de dados em CSV
- Coleta automática via API
- Cache inteligente de dados

## Tecnologias

- Streamlit
- Pandas
- Plotly
