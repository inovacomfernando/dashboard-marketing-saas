import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Dashboard Marketing - SaaS ERP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #073763;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #073763;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1e7dd;
        border-left: 4px solid #198754;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados

# Função para carregar dados do Google Sheets
@st.cache_data
def load_data():
    # Integração Google Sheets (standby)
    # SHEET_ID = "1k4s7OlIBJHLl9BjUJYC2mgbXDUI-RRXyDQTLIwiXWwo"
    # SHEET_NAME = "Indicadores" # Altere para o nome correto da aba se necessário
    # CREDENTIALS = st.secrets["gcp_service_account"] if "gcp_service_account" in st.secrets else None
    # if CREDENTIALS:
    #     creds = Credentials.from_service_account_info(CREDENTIALS, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    #     gc = gspread.authorize(creds)
    #     sh = gc.open_by_key(SHEET_ID)
    #     worksheet = sh.worksheet(SHEET_NAME)
    #     data = worksheet.get_all_records()
    #     return pd.DataFrame(data)
    # else:
    # Dados fixos locais
    data = {
        'Mês': ['Mai/25', 'Jun/25', 'Jul/25', 'Ago/25', 'Set/25'],
        'Sessões': [5218, 5600, 5717, 7654, 8028],
        'Primeira Visita': [2900, 3562, 3500, 5400, 5548],
        'Leads': [270, 290, 401, 600, 604],
        'TC Usuários (%)': [9.32, 8.79, 11.46, 11.11, 10.89],
        'Clientes Web': [16, 15, 18, 20, 22],
        'TC Leads (%)': [5.93, 5.50, 4.50, 3.33, 3.64],
        'Receita Web': [2114.56, 1991.31, 2591.91, 2728.92, 3001.90],
        'Ticket Médio': [132.16, 132.75, 149.99, 136.45, 136.45],
        'Custo Meta': [2238.52, 2328.16, 2731.39, 3476.39, 3807.17],
        'Custo Google': [2934.49, 3083.29, 3194.67, 4932.45, 6127.84],
        'Total Ads': [5173.01, 5411.32, 5926.06, 8408.84, 9935.01],
        'CAC': [323.31, 360.75, 329.23, 420.44, 451.59],
        'LTV': [1585.92, 1593.00, 1799.88, 1637.40, 1637.40],
        'CAC:LTV': [4.9, 4.4, 5.5, 3.9, 3.6],
        'ROI (%)': [390.52, 341.57, 446.70, 289.45, 262.58]
    }
    return pd.DataFrame(data)

df = load_data()

# Benchmarks
benchmarks = {
    'TC Usuários (%)': {'min': 8, 'max': 15, 'ideal': 10.5},
    'TC Leads (%)': {'min': 4.5, 'max': 6, 'ideal': 5.25},
    'CAC': {'min': 250, 'max': 500, 'ideal': 350},
    'CAC:LTV': {'min': 3, 'max': 7, 'ideal': 4, 'critico': 3},
    'ROI (%)': {'min': 300, 'max': 500, 'ideal': 400},
    'Ticket Médio': {'min': 120, 'max': 200, 'ideal': 150}
}

# Header
st.markdown('<div class="main-header">📊 Dashboard de Marketing - SaaS ERP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Análise de Performance: Maio - Setembro 2025</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/073763/ffffff?text=SaaS+ERP", use_container_width=True)
    st.markdown("---")
    
    st.subheader("Filtros")
    meses_selecionados = st.multiselect(
        "Selecione os meses:",
        options=df['Mês'].tolist(),
        default=df['Mês'].tolist()
    )
    
    st.markdown("---")
    st.subheader("Sobre")
    st.info("""
    Dashboard interativo para análise de KPIs de marketing digital com benchmarks do setor de SaaS ERP.
    """)
    
    st.markdown("---")
    st.caption("Desenvolvido para análise estratégica de marketing")

# Filtrar dados
df_filtered = df[df['Mês'].isin(meses_selecionados)]

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    cac_medio = df_filtered['CAC'].mean()
    cac_variacao = ((df_filtered['CAC'].iloc[-1] - df_filtered['CAC'].iloc[0]) / df_filtered['CAC'].iloc[0] * 100)
    st.metric(
        "CAC Médio",
        f"R$ {cac_medio:.2f}",
        f"{cac_variacao:+.1f}%",
        delta_color="inverse"
    )

with col2:
    ltv_medio = df_filtered['LTV'].mean()
    ltv_variacao = ((df_filtered['LTV'].iloc[-1] - df_filtered['LTV'].iloc[0]) / df_filtered['LTV'].iloc[0] * 100)
    st.metric(
        "LTV Médio",
        f"R$ {ltv_medio:.2f}",
        f"{ltv_variacao:+.1f}%"
    )

with col3:
    roi_medio = df_filtered['ROI (%)'].mean()
    roi_variacao = ((df_filtered['ROI (%)'].iloc[-1] - df_filtered['ROI (%)'].iloc[0]) / df_filtered['ROI (%)'].iloc[0] * 100)
    st.metric(
        "ROI Médio",
        f"{roi_medio:.1f}%",
        f"{roi_variacao:+.1f}%",
        delta_color="inverse"
    )

with col4:
    tc_leads_medio = df_filtered['TC Leads (%)'].mean()
    tc_variacao = ((df_filtered['TC Leads (%)'].iloc[-1] - df_filtered['TC Leads (%)'].iloc[0]) / df_filtered['TC Leads (%)'].iloc[0] * 100)
    st.metric(
        "TC Leads → Vendas",
        f"{tc_leads_medio:.2f}%",
        f"{tc_variacao:+.1f}%",
        delta_color="inverse"
    )

# Alertas
st.markdown("""
<div class="alert-box">
    <h4>⚠️ Pontos de Atenção</h4>
    <ul>
        <li><strong>CAC crescente:</strong> Aumentou 36% de Mai para Set (R$ 323 → R$ 441)</li>
        <li><strong>ROI em queda:</strong> Redução de 31% no período (390% → 271%)</li>
        <li><strong>Relação CAC:LTV em declínio:</strong> Caiu de 4.9:1 para 3.7:1 (tendência preocupante, aproximando do mínimo de 3:1)</li>
        <li><strong>TC Leads baixa:</strong> Tendência de queda (5.93% → 3.77%)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Tabs
import numpy as np
from sklearn.linear_model import LinearRegression

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["� Evolução", "💰 Financeiro", "🎯 Conversão", "📊 Benchmarks", "📋 Recomendações", "🔮 Forecast"])

with tab1:
    st.subheader("Evolução de Leads e Clientes")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_filtered['Mês'], 
        y=df_filtered['Leads'],
        mode='lines+markers',
        name='Leads',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=10)
    ))
    fig1.add_trace(go.Scatter(
        x=df_filtered['Mês'], 
        y=df_filtered['Clientes Web'],
        mode='lines+markers',
        name='Clientes',
        line=dict(color='#10b981', width=3),
        marker=dict(size=10)
    ))
    fig1.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tráfego do Site")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['Sessões'],
            name='Total Sessões',
            marker_color='#073763'
        ))
        fig2.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['Primeira Visita'],
            name='Primeira Visita',
            marker_color='#3b82f6'
        ))
        fig2.update_layout(height=350, barmode='group')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("Receita Web Mensal")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['Receita Web'],
            marker_color='#10b981',
            text=df_filtered['Receita Web'].apply(lambda x: f'R$ {x:.0f}'),
            textposition='outside'
        ))
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("Análise Financeira")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### CAC vs LTV")
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['CAC'],
            name='CAC',
            marker_color='#ef4444'
        ))
        fig4.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['LTV'],
            name='LTV',
            marker_color='#10b981'
        ))
        fig4.update_layout(height=350, barmode='group')
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.markdown("### Investimento em Ads")
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['Custo Meta'],
            name='Meta Ads',
            marker_color='#1877f2'
        ))
        fig5.add_trace(go.Bar(
            x=df_filtered['Mês'],
            y=df_filtered['Custo Google'],
            name='Google Ads',
            marker_color='#ea4335'
        ))
        fig5.update_layout(height=350, barmode='stack')
        st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("### Evolução do ROI")
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=df_filtered['Mês'],
        y=df_filtered['ROI (%)'],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=12)
    ))
    fig6.add_hline(y=benchmarks['ROI (%)']['ideal'], line_dash="dash", 
                   line_color="green", annotation_text="Benchmark Ideal")
    fig6.update_layout(height=350)
    st.plotly_chart(fig6, use_container_width=True)
    
    # Alerta crítico sobre CAC:LTV
    st.markdown("### ⚠️ Alerta Crítico: CAC:LTV em Declínio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_cac_ltv = go.Figure()
        fig_cac_ltv.add_trace(go.Scatter(
            x=df_filtered['Mês'],
            y=df_filtered['CAC:LTV'],
            mode='lines+markers',
            line=dict(color='#ef4444', width=3),
            marker=dict(size=12),
            name='CAC:LTV'
        ))
        fig_cac_ltv.add_hline(y=3, line_dash="dash", line_color="red", 
                             annotation_text="Mínimo Aceitável (3:1)", annotation_position="bottom right")
        fig_cac_ltv.add_hline(y=4, line_dash="dot", line_color="orange",
                             annotation_text="Ideal (4:1)", annotation_position="top right")
        fig_cac_ltv.add_hrect(y0=4, y1=7, fillcolor="green", opacity=0.1,
                             annotation_text="Zona Saudável", annotation_position="top left")
        fig_cac_ltv.update_layout(
            height=350,
            yaxis_title="Relação CAC:LTV",
            showlegend=False
        )
        st.plotly_chart(fig_cac_ltv, use_container_width=True)
    
    with col2:
        variacao_cac_ltv = ((df_filtered['CAC:LTV'].iloc[-1] - df_filtered['CAC:LTV'].iloc[0]) / df_filtered['CAC:LTV'].iloc[0] * 100)
        
        st.metric(
            "CAC:LTV Atual",
            f"{df_filtered['CAC:LTV'].iloc[-1]:.1f}:1",
            f"{variacao_cac_ltv:.1f}%",
            delta_color="inverse"
        )
        
        st.metric(
            "Distância do Mínimo",
            f"{(df_filtered['CAC:LTV'].iloc[-1] - 3):.1f}",
            "pontos acima de 3:1"
        )
        
        st.markdown("""
        <div style="background-color: #fee; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ef4444; margin-top: 1rem;">
            <strong>⚠️ Situação Crítica</strong><br>
            <small>Se continuar nesta tendência, em 2-3 meses você estará abaixo do mínimo aceitável de 3:1</small>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("Funil de Conversão")
    
    # Métricas do último mês
    ultimo_mes = df_filtered.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sessões", f"{ultimo_mes['Sessões']:,.0f}")
    with col2:
        st.metric("Leads", f"{ultimo_mes['Leads']:,.0f}")
    with col3:
        st.metric("Clientes", f"{ultimo_mes['Clientes Web']:,.0f}")
    with col4:
        st.metric("Receita", f"R$ {ultimo_mes['Receita Web']:,.2f}")
    
    # Gráfico de funil
    fig7 = go.Figure(go.Funnel(
        y=['Sessões', 'Primeira Visita', 'Leads', 'Clientes'],
        x=[ultimo_mes['Sessões'], ultimo_mes['Primeira Visita'], 
           ultimo_mes['Leads'], ultimo_mes['Clientes Web']],
        textinfo="value+percent initial",
        marker=dict(color=['#073763', '#3b82f6', '#8b5cf6', '#10b981'])
    ))
    fig7.update_layout(height=400)
    st.plotly_chart(fig7, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Taxa de Conversão: Usuários → Leads")
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=df_filtered['Mês'],
            y=df_filtered['TC Usuários (%)'],
            mode='lines+markers',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=10)
        ))
        fig8.add_hrect(y0=benchmarks['TC Usuários (%)']['min'], 
                       y1=benchmarks['TC Usuários (%)']['max'],
                       fillcolor="green", opacity=0.1,
                       annotation_text="Benchmark", annotation_position="top left")
        fig8.update_layout(height=300)
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.markdown("### Taxa de Conversão: Leads → Vendas")
        fig9 = go.Figure()
        fig9.add_trace(go.Scatter(
            x=df_filtered['Mês'],
            y=df_filtered['TC Leads (%)'],
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=10)
        ))
        fig9.add_hrect(y0=benchmarks['TC Leads (%)']['min'], 
                       y1=benchmarks['TC Leads (%)']['max'],
                       fillcolor="green", opacity=0.1,
                       annotation_text="Benchmark", annotation_position="top left")
        fig9.update_layout(height=300)
        st.plotly_chart(fig9, use_container_width=True)

with tab4:
    st.subheader("Comparação com Benchmarks SaaS ERP")
    
    # Tabela de benchmarks
    benchmark_data = {
        'Métrica': ['TC Usuários → Leads', 'TC Leads → Vendas', 'CAC', 'CAC:LTV', 'ROI', 'Ticket Médio'],
        'Sua Média': [
            f"{df_filtered['TC Usuários (%)'].mean():.2f}%",
            f"{df_filtered['TC Leads (%)'].mean():.2f}%",
            f"R$ {df_filtered['CAC'].mean():.2f}",
            f"{df_filtered['CAC:LTV'].mean():.1f}:1",
            f"{df_filtered['ROI (%)'].mean():.1f}%",
            f"R$ {df_filtered['Ticket Médio'].mean():.2f}"
        ],
        'Benchmark': ['8-15%', '4.5-6%', 'R$ 250-500', '≥3:1 (ideal 4-7:1)', '300-500%', 'R$ 120-200'],
        'Status': ['✅ Na meta', '⚠️ Limítrofe', '✅ Aceitável', '⚠️ Declínio', '✅ Bom', '✅ Normal']
    }
    
    st.dataframe(
        pd.DataFrame(benchmark_data),
        use_container_width=True,
        hide_index=True
    )
    
    # Gráfico radar
    st.markdown("### Radar de Performance vs Benchmark")
    
    categories = ['TC Usuários', 'TC Leads', 'CAC/100', 'CAC:LTV', 'ROI/100']
    
    seu_desempenho = [
        df_filtered['TC Usuários (%)'].mean(),
        df_filtered['TC Leads (%)'].mean(),
        df_filtered['CAC'].mean() / 100,
        df_filtered['CAC:LTV'].mean(),
        df_filtered['ROI (%)'].mean() / 100
    ]
    
    benchmark_valores = [
        benchmarks['TC Usuários (%)']['ideal'],
        benchmarks['TC Leads (%)']['ideal'],
        benchmarks['CAC']['ideal'] / 100,
        benchmarks['CAC:LTV']['ideal'],
        benchmarks['ROI (%)']['ideal'] / 100
    ]
    
    fig10 = go.Figure()
    fig10.add_trace(go.Scatterpolar(
        r=seu_desempenho,
        theta=categories,
        fill='toself',
        name='Seu Desempenho',
        line_color='#3b82f6'
    ))
    fig10.add_trace(go.Scatterpolar(
        r=benchmark_valores,
        theta=categories,
        fill='toself',
        name='Benchmark',
        line_color='#10b981',
        opacity=0.6
    ))
    fig10.update_layout(height=500, polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig10, use_container_width=True)

with tab5:
    st.subheader("Recomendações Estratégicas Atualizadas")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="alert-box">
            <h4>🎯 Prioridade Alta</h4>
            <ol>
                <li><strong>Monitorar CAC:LTV:</strong> Relação caiu de 4.9:1 para 3.6:1. Atenção máxima para não romper o mínimo de 3:1. Ações:
                    <ul>
                        <li>Reduzir CAC: Otimizar campanhas, pausar keywords caras, investir em canais orgânicos</li>
                        <li>Aumentar LTV: Upsell, cross-sell, retenção e customer success</li>
                    </ul>
                </li>
                <li><strong>Otimizar CAC:</strong> Google Ads subiu +109% em 5 meses. Auditar campanhas e priorizar SEO/conteúdo.</li>
                <li><strong>Melhorar conversão Leads→Vendas:</strong> TC caiu de 5.93% para 3.64%. Implementar lead scoring e revisar funil comercial.</li>
                <li><strong>Qualificar leads:</strong> Foco em qualidade para elevar conversão e ticket médio.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>📈 Oportunidades Recentes</h4>
            <ul>
                <li><strong>Crescimento de leads:</strong> Volume subiu 124% (270→604)</li>
                <li><strong>Tráfego qualificado:</strong> Conversão usuários→leads está dentro do benchmark</li>
                <li><strong>Infraestrutura escalável:</strong> Suporta aumento de 50% sem perda de qualidade</li>
                <li><strong>ROI positivo:</strong> Mantido acima de 260%, modelo sustentável</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📅 Plano de Ação Atualizado")
    plano = pd.DataFrame({
        'Prazo': ['Curto (30 dias)', 'Curto (30 dias)', 'Curto (30 dias)', 
                  'Médio (90 dias)', 'Médio (90 dias)', 'Médio (90 dias)',
                  'Longo (6 meses)', 'Longo (6 meses)', 'Longo (6 meses)'],
        'Ação': [
            'Auditar campanhas Google Ads - pausar palavras com CPC alto',
            'Implementar qualificação de leads (lead scoring)',
            'A/B test em landing pages focando em conversão',
            'Desenvolver estratégia de conteúdo (SEO)',
            'Criar programa de onboarding para aumentar LTV',
            'Implementar automação de marketing',
            'Diversificar canais de aquisição (parcerias, marketplace)',
            'Desenvolver estratégia de customer success',
            'Criar ofertas de upsell/cross-sell'
        ],
        'Impacto Esperado': [
            'Redução CAC em 15-20%',
            'Aumento TC em 10-15%',
            'Aumento conversão em 5-10%',
            'Redução CAC em 25-30%',
            'Aumento LTV em 20-30%',
            'Aumento TC em 15-20%',
            'Redução CAC em 30-40%',
            'Redução churn em 15-25%',
            'Aumento LTV em 40-60%'
        ],
        'Responsável': [
            'Marketing', 'Vendas/Marketing', 'Marketing',
            'Marketing', 'CS/Produto', 'Marketing',
            'Comercial', 'Customer Success', 'Produto/Vendas'
        ]
    })
    st.dataframe(plano, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("Dashboard de Marketing - SaaS ERP | Atualizado em Setembro 2025")
    
# Forecast Tab
with tab6:
    st.subheader("🔮 Forecast: Cenários para Projeção e Estratégia")
    meses = df['Mês'].tolist()
    meses_num = np.arange(len(meses)).reshape(-1, 1)
    previsao_meses = ["Out/25", "Nov/25", "Dez/25"]
    meses_num_forecast = np.arange(len(meses), len(meses)+len(previsao_meses)).reshape(-1, 1)

    def prever_cenarios(col):
        modelo = LinearRegression()
        modelo.fit(meses_num, df[col].values)
        base = modelo.predict(meses_num_forecast)
        # Cenário otimista: +10% de crescimento sobre a tendência
        otimista = base * 1.10
        # Cenário conservador: -10% sobre a tendência
        conservador = base * 0.90
        # Cenário realista: tendência linear
        realista = base
        return otimista, realista, conservador

    kpis = ["Leads", "Clientes Web", "Receita Web", "CAC", "LTV", "ROI (%)"]
    resultados_otimista, resultados_realista, resultados_conservador = {}, {}, {}
    for kpi in kpis:
        ot, rl, cv = prever_cenarios(kpi)
        resultados_otimista[kpi] = ot
        resultados_realista[kpi] = rl
        resultados_conservador[kpi] = cv

    df_otimista = pd.DataFrame({
        "Mês": previsao_meses,
        **{k: resultados_otimista[k].round(2) for k in kpis}
    })
    df_realista = pd.DataFrame({
        "Mês": previsao_meses,
        **{k: resultados_realista[k].round(2) for k in kpis}
    })
    df_conservador = pd.DataFrame({
        "Mês": previsao_meses,
        **{k: resultados_conservador[k].round(2) for k in kpis}
    })

    st.markdown("### Tabela de Projeções por Cenário")
    st.markdown("**Cenário Otimista**")
    st.dataframe(df_otimista, use_container_width=True, hide_index=True)
    st.markdown("**Cenário Realista**")
    st.dataframe(df_realista, use_container_width=True, hide_index=True)
    st.markdown("**Cenário Conservador**")
    st.dataframe(df_conservador, use_container_width=True, hide_index=True)

    st.markdown("### Gráficos de Projeção por Cenário")
    col1, col2, col3 = st.columns(3)
    with col1:
        fig_leads = go.Figure()
        fig_leads.add_trace(go.Scatter(x=meses, y=df["Leads"], mode="lines+markers", name="Histórico"))
        fig_leads.add_trace(go.Scatter(x=previsao_meses, y=df_otimista["Leads"], mode="lines+markers", name="Otimista"))
        fig_leads.add_trace(go.Scatter(x=previsao_meses, y=df_realista["Leads"], mode="lines+markers", name="Realista"))
        fig_leads.add_trace(go.Scatter(x=previsao_meses, y=df_conservador["Leads"], mode="lines+markers", name="Conservador"))
        fig_leads.update_layout(title="Leads - Cenários", height=350)
        st.plotly_chart(fig_leads, use_container_width=True)
    with col2:
        fig_receita = go.Figure()
        fig_receita.add_trace(go.Scatter(x=meses, y=df["Receita Web"], mode="lines+markers", name="Histórico"))
        fig_receita.add_trace(go.Scatter(x=previsao_meses, y=df_otimista["Receita Web"], mode="lines+markers", name="Otimista"))
        fig_receita.add_trace(go.Scatter(x=previsao_meses, y=df_realista["Receita Web"], mode="lines+markers", name="Realista"))
        fig_receita.add_trace(go.Scatter(x=previsao_meses, y=df_conservador["Receita Web"], mode="lines+markers", name="Conservador"))
        fig_receita.update_layout(title="Receita Web - Cenários", height=350)
        st.plotly_chart(fig_receita, use_container_width=True)
    with col3:
        fig_cac = go.Figure()
        fig_cac.add_trace(go.Scatter(x=meses, y=df["CAC"], mode="lines+markers", name="Histórico"))
        fig_cac.add_trace(go.Scatter(x=previsao_meses, y=df_otimista["CAC"], mode="lines+markers", name="Otimista"))
        fig_cac.add_trace(go.Scatter(x=previsao_meses, y=df_realista["CAC"], mode="lines+markers", name="Realista"))
        fig_cac.add_trace(go.Scatter(x=previsao_meses, y=df_conservador["CAC"], mode="lines+markers", name="Conservador"))
        fig_cac.update_layout(title="CAC - Cenários", height=350)
        st.plotly_chart(fig_cac, use_container_width=True)

    st.markdown("### Estratégias e Insumos para Decisão por Cenário")
    st.info(f"""
    **Otimista:**
    - Aproveitar o crescimento acelerado para investir em expansão e novos canais.
    - Reforçar ações de retenção e upsell para maximizar receita.
    - Monitorar custos para não perder margem.

    **Realista:**
    - Manter investimentos atuais, focar em eficiência operacional.
    - Revisar funil comercial e ajustar campanhas conforme performance.
    - Priorizar ações de baixo custo e alto impacto.

    **Conservador:**
    - Reduzir gastos em canais pagos, priorizar orgânico e relacionamento.
    - Foco total em retenção e redução de churn.
    - Revisar metas e preparar plano de contingência.
    """)

    st.markdown("#### Insumos para Decisão Assertiva:")
    st.markdown("""
    - Relatórios detalhados de campanhas (Google Ads, Meta)
    - Análise de churn e satisfação dos clientes
    - Dados de funil comercial e taxas de conversão
    - Projeção de custos e receitas por canal
    - Benchmark do setor atualizado
    """)

    st.success("Compare os cenários para definir metas, ajustar investimentos e priorizar ações conforme o contexto do negócio.")

    st.markdown("---")
    st.caption("Forecast com cenários para apoiar decisões estratégicas de marketing e vendas.")
