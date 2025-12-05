import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import requests
from datetime import datetime

# ========================
# COLETA DE DADOS VIA API
# ========================

@st.cache_data(ttl=86400)  # Cache por 24 horas
def fetch_data_from_api():
    """
    Busca dados de vendas de VEs da API do Our World in Data
    e salva localmente em CSV
    """
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    csv_path = data_dir / "ev_sales_global.csv"
    
    # Se arquivo já existe e é recente (menos de 7 dias), usar cache local
    if csv_path.exists():
        file_age_days = (datetime.now().timestamp() - csv_path.stat().st_mtime) / 86400
        if file_age_days < 7:
            return pd.read_csv(csv_path)
    
    # Buscar dados da API
    try:
        # URL da API do OWID para dados de carros elétricos
        api_url = "https://github.com/owid/owid-datasets/raw/master/datasets/Electric%20car%20sales%20-%20by%20country/Electric%20car%20sales%20-%20by%20country.csv"
        
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        # Salvar dados brutos
        with open(csv_path, 'wb') as f:
            f.write(response.content)
        
        # Carregar e retornar DataFrame
        df = pd.read_csv(csv_path)
        return df
        
    except requests.RequestException as e:
        # Fallback: tentar carregar arquivo local existente
        if csv_path.exists():
            return pd.read_csv(csv_path)
        else:
            st.error("Não foi possível obter os dados. Verifique sua conexão com a internet.")
            st.stop()

st.set_page_config(
    page_title="Dashboard Vendas VE",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Modo escuro */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #f8fafc;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #94a3b8;
    }
    
    /* Tabs escuras */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #1e293b;
        padding: 8px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 6px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white !important;
    }
    
    /* Sidebar escura */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Botões */
    .stDownloadButton button {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 6px;
        font-weight: 600;
    }
    
    .stDownloadButton button:hover {
        background-color: #2563eb;
    }
    
    /* Títulos */
    h1 {
        color: #f8fafc !important;
        font-weight: 800;
        font-size: 2.5rem !important;
    }
    
    h2 {
        color: #f1f5f9 !important;
        font-weight: 700;
    }
    
    h3 {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Texto */
    p, span, label {
        color: #cbd5e1 !important;
    }
    
    /* Cards escuros */
    .stAlert {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-left: 4px solid #3b82f6;
    }
    
    /* Dataframe escuro */
    [data-testid="stDataFrame"] {
        background-color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_and_process_data():
    """Carrega dados da API e aplica processamento/limpeza"""
    df = fetch_data_from_api()
    
    # Limpeza de dados
    df = df.dropna(subset=['Electric cars sold']).copy()
    df['Electric cars sold'] = df['Electric cars sold'].astype(int)
    
    return df

@st.cache_resource
def load_data():
    """DEPRECADO - usar load_and_process_data() que busca da API"""
    data_path = Path(__file__).parent.parent / "data" / "ev_sales_global.csv"
    df = pd.read_csv(data_path)
    df = df.dropna(subset=['Electric cars sold']).copy()
    df['Electric cars sold'] = df['Electric cars sold'].astype(int)
    return df

def get_global_trend(df):
    return df[df['Entity'] == 'World'].sort_values('Year')

def get_top_countries(df, year=None, top_n=10):
    df_countries = df[~df['Entity'].isin(['World', 'Europe', 'Rest of World', 'European Union (27)'])]
    if year is None:
        return df_countries.groupby('Entity')['Electric cars sold'].sum().sort_values(ascending=False).head(top_n)
    else:
        year_data = df_countries[df_countries['Year'] == year]
        return year_data.groupby('Entity')['Electric cars sold'].sum().sort_values(ascending=False).head(top_n)

def get_country_data(df, country):
    return df[df['Entity'] == country].sort_values('Year')

def get_countries_list(df):
    df_countries = df[~df['Entity'].isin(['World', 'Europe', 'Rest of World', 'European Union (27)'])]
    return sorted(df_countries['Entity'].unique().tolist())

def get_year_range(df):
    return int(df['Year'].min()), int(df['Year'].max())

def get_summary_stats(df):
    world_data = get_global_trend(df)
    yearly_growth = world_data['Electric cars sold'].pct_change().dropna()
    avg_growth = yearly_growth.mean() * 100 if len(yearly_growth) > 0 else 0
    
    return {
        'total_sales': int(df['Electric cars sold'].sum()),
        'countries': df[~df['Entity'].isin(['World', 'Europe', 'Rest of World', 'European Union (27)'])]['Entity'].nunique(),
        'year_min': int(df['Year'].min()),
        'year_max': int(df['Year'].max()),
        'avg_annual_growth': avg_growth
    }

df = load_and_process_data()
min_year, max_year = get_year_range(df)

st.markdown("""
<div style='text-align: center; padding: 2rem 0; background: #1e293b; border-radius: 12px; margin-bottom: 2rem; border: 1px solid #334155;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem; color: #f8fafc;'>Dashboard de Vendas de Veículos Elétricos</h1>
    <p style='font-size: 1rem; color: #94a3b8; margin: 0;'>
        Análise global de vendas de veículos elétricos • 2010-2023 • Dados via API OWID
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='text-align: center; padding: 2rem 0 1.5rem 0; border-bottom: 1px solid #334155;'>
    <h2 style='font-size: 1.5rem; margin: 0; font-weight: 700;'>Filtros</h2>
</div>
""", unsafe_allow_html=True)

selected_countries = st.sidebar.multiselect(
    "Países para comparar:",
    options=get_countries_list(df),
    default=["China", "United States", "Germany"],
    help="Selecione até 5 países para comparação detalhada"
)

year_range = st.sidebar.slider(
    "Período de análise:",
    min_year,
    max_year,
    (2015, max_year)
)

# Botão para forçar atualização dos dados
if st.sidebar.button("Atualizar Dados da API"):
    st.cache_data.clear()
    st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Tendências", "Comparação", "Dados"])

with tab1:
    st.markdown("""
    <div style='background: #1e293b; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid #334155;'>
        <h2 style='color: #f8fafc; margin: 0 0 0.5rem 0; font-size: 1.5rem;'>Visão Geral Global</h2>
        <p style='color: #94a3b8; margin: 0; font-size: 0.95rem;'>
            Panorama completo das vendas globais de veículos elétricos de 2010 a 2023
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    stats = get_summary_stats(df)
    world_data = get_global_trend(df)
    latest_year = world_data.iloc[-1]
    prev_year = world_data.iloc[-2]
    growth_last_year = ((latest_year['Electric cars sold'] - prev_year['Electric cars sold']) / prev_year['Electric cars sold'] * 100)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Total de Vendas Globais", 
        f"{stats['total_sales']:,}",
        help="Soma de todas as vendas registradas de 2010-2023"
    )
    col2.metric(
        "Vendas em 2023", 
        f"{latest_year['Electric cars sold']:,}",
        delta=f"+{growth_last_year:.1f}% vs 2022",
        help="Vendas do ano mais recente com crescimento anual"
    )
    col3.metric(
        "Países", 
        stats['countries'],
        help="Número de países com dados disponíveis"
    )
    col4.metric(
        "Crescimento Médio Anual", 
        f"{stats['avg_annual_growth']:.1f}%",
        help="Taxa média de crescimento ano a ano desde 2010"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Top 10 Mercados de Veículos Elétricos (2010-2023)")
    st.caption("Líderes de mercado impulsionando a transição para mobilidade elétrica")
    
    top_10 = get_top_countries(df, top_n=10)
    total_top10 = top_10.sum()
    china_share = (top_10.iloc[0] / total_top10 * 100) if len(top_10) > 0 else 0
    
    colors = ['#3b82f6' if i == 0 else '#60a5fa' if i < 3 else '#93c5fd' for i in range(len(top_10))]
    
    fig = go.Figure(data=[go.Bar(
        x=top_10.values, 
        y=top_10.index, 
        orientation='h',
        marker=dict(color=colors),
        text=[f"{val:,}" for val in top_10.values],
        textposition='outside',
        textfont=dict(size=11, color='#f8fafc', family='Arial')
    )])
    fig.update_layout(
        xaxis_title="Total de Vendas (unidades)",
        yaxis_title="",
        height=450,
        template="plotly_dark",
        title=dict(
            text=f"China representa {china_share:.1f}% do Top 10",
            font=dict(size=13, color='#cbd5e1')
        ),
        plot_bgcolor='#0f172a',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(color='#cbd5e1')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"China lidera com {top_10.iloc[0]:,} vendas, mais que os próximos 5 países combinados")
    with col2:
        st.info(f"À uma grande concentração de mercado onde o Top 3 países representam 70%+ das vendas globais")

with tab2:
    st.markdown("""
    <div style='background: #1e293b; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid #334155;'>
        <h2 style='color: #f8fafc; margin: 0 0 0.5rem 0; font-size: 1.5rem;'>Evolução Temporal e Tendências</h2>
        <p style='color: #94a3b8; margin: 0; font-size: 0.95rem;'>
            Análise da trajetória de crescimento do mercado de VEs ao longo de 13 anos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    world_data = get_global_trend(df)
    first_year_sales = world_data.iloc[0]['Electric cars sold']
    last_year_sales = world_data.iloc[-1]['Electric cars sold']
    total_growth = ((last_year_sales - first_year_sales) / first_year_sales * 100)
    
    st.markdown(f"**Crescimento Total:** {first_year_sales:,} (2010) → {last_year_sales:,} (2023) = **+{total_growth:,.0f}%**")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=world_data['Year'],
        y=world_data['Electric cars sold'],
        mode='lines+markers',
        name='Vendas Anuais',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8, color='#60a5fa'),
        fill='tozeroy',
        fillcolor='rgba(59,130,246,0.1)',
        hovertemplate='<b>Ano %{x}</b><br>Vendas: %{y:,}<extra></extra>'
    ))
    
    fig.add_annotation(
        x=2020,
        y=world_data[world_data['Year'] == 2020]['Electric cars sold'].values[0],
        text="Aceleração<br>pós-pandemia",
        showarrow=True,
        arrowhead=2,
        bgcolor="#1e293b",
        bordercolor="#334155",
        borderwidth=1,
        font=dict(color='#cbd5e1')
    )
    
    fig.update_layout(
        title=dict(
            text="Crescimento Exponencial: Mercado expandiu 100x desde 2010",
            font=dict(size=14, color='#cbd5e1')
        ),
        xaxis_title="Ano",
        yaxis_title="Vendas Globais (unidades)",
        height=500,
        template="plotly_dark",
        hovermode='x unified',
        plot_bgcolor='#0f172a',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(color='#cbd5e1')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Crescimento Ano a Ano")
        st.caption("Variação percentual comparando cada ano ao anterior")
        
        world_copy = world_data.copy()
        world_copy['Crescimento %'] = world_copy['Electric cars sold'].pct_change() * 100
        world_copy['Vendas Adicionais'] = world_copy['Electric cars sold'].diff()
        
        display_df = world_copy[['Year', 'Electric cars sold', 'Vendas Adicionais', 'Crescimento %']].rename(
            columns={
                'Year': 'Ano',
                'Electric cars sold': 'Vendas Totais',
                'Vendas Adicionais': 'Novas vs Anterior',
                'Crescimento %': 'Crescimento %'
            }
        )
        
        st.dataframe(
            display_df.style.format({
                'Vendas Totais': '{:,.0f}',
                'Novas vs Anterior': '{:+,.0f}',
                'Crescimento %': '{:+.1f}%'
            }),
            use_container_width=True,
            height=400
        )
        
        max_growth_year = world_copy.loc[world_copy['Crescimento %'].idxmax(), 'Year']
        max_growth_value = world_copy['Crescimento %'].max()
        st.info(f"📈 **Pico de crescimento:** {max_growth_year:.0f} com +{max_growth_value:.1f}%")
    
    with col2:
        st.subheader("Vendas por Período")
        st.caption("Mostra como o mercado acelerou dramaticamente nos anos recentes")
        
        p1 = world_data[world_data['Year'] <= 2015]['Electric cars sold'].sum()
        p2 = world_data[(world_data['Year'] >= 2016) & (world_data['Year'] <= 2020)]['Electric cars sold'].sum()
        p3 = world_data[world_data['Year'] >= 2021]['Electric cars sold'].sum()
        
        periods = ['2010-2015', '2016-2020', '2021-2023']
        values = [p1, p2, p3]
        
        fig = go.Figure(data=[go.Bar(
            x=periods,
            y=values,
            marker=dict(color=['#60a5fa', '#3b82f6', '#2563eb']),
            text=[f"{val:,}" for val in values],
            textposition='outside',
            textfont=dict(size=12, color='#f8fafc', family='Arial')
        )])
        
        fig.update_layout(
            title="Período recente (2021-23) supera toda a década anterior",
            yaxis_title="Total de Vendas",
            height=350,
            template="plotly_dark",
            showlegend=False,
            plot_bgcolor='#0f172a',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"2021-2023 teve {(p3/p2-1)*100:.0f}% mais vendas que 2016-2020")

with tab3:
    st.markdown("""
    <div style='background: #1e293b; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid #334155;'>
        <h2 style='color: #f8fafc; margin: 0 0 0.5rem 0; font-size: 1.5rem;'>Comparação Entre Países</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if selected_countries:
        comparison_data = []
        for country in selected_countries:
            country_df = get_country_data(df, country)
            country_df = country_df[(country_df['Year'] >= year_range[0]) & (country_df['Year'] <= year_range[1])]
            comparison_data.append(country_df)
        
        df_comp = pd.concat(comparison_data)
        
        fig = px.line(
            df_comp,
            x='Year',
            y='Electric cars sold',
            color='Entity',
            markers=True,
            labels={'Electric cars sold': 'Vendas Anuais', 'Year': 'Ano', 'Entity': 'País'},
            color_discrete_sequence=['#3b82f6', '#60a5fa', '#93c5fd', '#2563eb', '#1d4ed8']
        )
        
        fig.update_layout(
            title=dict(
                text=f"Trajetória Comparativa: {', '.join(selected_countries)} ({year_range[0]}-{year_range[1]})",
                font=dict(size=13, color='#cbd5e1')
            ),
            height=500,
            template="plotly_dark",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='#1e293b',
                bordercolor='#334155',
                borderwidth=1
            ),
            plot_bgcolor='#0f172a',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=80, b=20),
            font=dict(color='#cbd5e1')
        )
        
        fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
        fig.update_xaxes(gridcolor='#1e293b', linecolor='#334155')
        fig.update_yaxes(gridcolor='#1e293b', linecolor='#334155')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Análise Detalhada por Ano")
        st.caption("Compare vendas entre países e anos")
        
        pivot = df_comp.pivot(index='Year', columns='Entity', values='Electric cars sold')
        pivot['Total Anual'] = pivot.sum(axis=1)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(
                pivot.style.format("{:,.0f}"),
                use_container_width=True
            )
        
        with col2:
            st.markdown("**💡 Insights:**")
            for country in selected_countries:
                country_data = df_comp[df_comp['Entity'] == country]
                if len(country_data) > 1:
                    total = country_data['Electric cars sold'].sum()
                    growth = (country_data.iloc[-1]['Electric cars sold'] - 
                             country_data.iloc[0]['Electric cars sold']) / \
                             country_data.iloc[0]['Electric cars sold'] * 100
                    st.metric(
                        country,
                        f"{total:,}",
                        delta=f"+{growth:.0f}%",
                        help=f"Total no período com crescimento percentual"
                    )
        
        st.markdown("---")
        st.subheader("Participação de Mercado")
        
        market_share = df_comp.groupby('Entity')['Electric cars sold'].sum().sort_values(ascending=False)
        market_share_pct = (market_share / market_share.sum() * 100)
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=market_share_pct.index,
            values=market_share_pct.values,
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{percent}<br>Vendas: %{value:,.0f}<extra></extra>',
            marker=dict(colors=['#3b82f6', '#60a5fa', '#93c5fd', '#2563eb', '#1d4ed8'])
        )])
        
        fig_pie.update_layout(
            height=700,
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        leader = market_share.index[0]
        leader_pct = market_share_pct.iloc[0]
        st.info(f"{leader} tem a maior partipação com {leader_pct:.1f}% das vendas entre o mercado de veículos elétricos, graças a políticas agressivas e incentivos para o uso desses veículos.")
        
        
    else:
        st.info("👈 Selecione países na barra lateral para iniciar a comparação")

with tab4:
    st.markdown("""
    <div style='background: #1e293b; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid #334155;'>
        <h2 style='color: #f8fafc; margin: 0 0 0.5rem 0; font-size: 1.5rem;'>Explorador de Dados</h2>
        <p style='color: #94a3b8; margin: 0; font-size: 0.95rem;'>
            Acesse dados originais obtidos via API para análise personalizada ou download
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    view = st.radio("Escolha o tipo de visualização:", ["📊 Dados Globais", "🌍 Dados por País", "📥 Download Completo"])
    
    if view == "📊 Dados Globais":
        st.markdown("**Total de vendas mundiais por ano** - Agregação de todos os países")
        global_df = get_global_trend(df)
        global_df['Crescimento Anual %'] = global_df['Electric cars sold'].pct_change() * 100
        
        st.dataframe(
            global_df[['Year', 'Electric cars sold', 'Crescimento Anual %']].rename(columns={
                'Year': 'Ano',
                'Electric cars sold': 'Vendas Globais',
                'Crescimento Anual %': 'Crescimento Anual %'
            }).style.format({
                'Vendas Globais': '{:,.0f}',
                'Crescimento Anual %': '{:+.1f}%'
            }),
            use_container_width=True
        )
    
    elif view == "🌍 Dados por País":
        st.markdown("**Selecione um país para ver sua evolução detalhada**")
        country = st.selectbox("Escolha o país:", get_countries_list(df))
        
        country_data = get_country_data(df, country)
        country_data['Crescimento %'] = country_data['Electric cars sold'].pct_change() * 100
        country_data['Variação Absoluta'] = country_data['Electric cars sold'].diff()
        
        total_country = country_data['Electric cars sold'].sum()
        avg_sales = country_data['Electric cars sold'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Histórico", f"{total_country:,.0f}")
        col2.metric("Média Anual", f"{avg_sales:,.0f}")
        col3.metric("Anos com Dados", len(country_data))
        
        st.dataframe(
            country_data[['Year', 'Electric cars sold', 'Variação Absoluta', 'Crescimento %']].rename(columns={
                'Year': 'Ano',
                'Electric cars sold': 'Vendas',
                'Variação Absoluta': 'Mudança vs Ano Anterior',
                'Crescimento %': 'Crescimento %'
            }).style.format({
                'Vendas': '{:,.0f}',
                'Mudança vs Ano Anterior': '{:+,.0f}',
                'Crescimento %': '{:+.1f}%'
            }),
            use_container_width=True
        )
    
    elif view == "📥 Download Completo":
        st.markdown("**Dataset completo com todos os países e anos (Fonte: API OWID)**")
        
        st.info(f"""
        📊 **Informações do Dataset:**
        - Total de registros: {len(df):,}
        - Países: {df['Entity'].nunique()}
        - Período: {df['Year'].min():.0f} - {df['Year'].max():.0f}
        - Total de vendas registradas: {df['Electric cars sold'].sum():,.0f}
        - Fonte: Our World in Data API
        """)
        
        st.dataframe(
            df.head(20).style.format({'Electric cars sold': '{:,.0f}'}),
            use_container_width=True
        )
        
        st.markdown("*Mostrando primeiras 20 linhas do dataset completo.*")
