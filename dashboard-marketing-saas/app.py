# Importações principais
try:
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from scipy import stats
    import sklearn.metrics as metrics
except Exception as e:
    st.error(f"""
    ❌ Erro ao importar as bibliotecas necessárias.
    
    Por favor, instale todas as dependências usando:
    ```
    pip install -r requirements.txt
    ```
    
    Erro original: {str(e)}
    """)
    st.stop()

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
    .info-box {
        background-color: #cfe2ff;
        border-left: 4px solid #0d6efd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Evolução", 
    "💰 Financeiro", 
    "🎯 Conversão", 
    "📊 Benchmarks", 
    "📋 Recomendações", 
    "🔮 Forecast",
    "🤝 Parceria Contador"
])

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
    
    benchmark_data = pd.DataFrame({
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
    })
    
    st.dataframe(benchmark_data, use_container_width=True, hide_index=True)

with tab5:
    st.subheader("Recomendações Estratégicas")
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
            <h4>📈 Oportunidades</h4>
            <ul>
                <li><strong>Crescimento de leads:</strong> Volume subiu 124% (270→604)</li>
                <li><strong>Tráfego qualificado:</strong> Conversão usuários→leads está dentro do benchmark</li>
                <li><strong>Infraestrutura escalável:</strong> Suporta aumento de 50% sem perda de qualidade</li>
                <li><strong>ROI positivo:</strong> Mantido acima de 260%, modelo sustentável</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.subheader("🔮 Forecast: Cenários para Projeção e Estratégia")
    
    try:
        # Preparação dos dados para forecast
        meses = df['Mês'].tolist()
        meses_num = np.arange(len(meses)).reshape(-1, 1)
        previsao_meses = ["Out/25", "Nov/25", "Dez/25"]
        meses_num_forecast = np.arange(len(meses), len(meses)+len(previsao_meses)).reshape(-1, 1)

        def prever_cenarios(col):
            try:
                # Modelo de regressão linear
                modelo = LinearRegression()
                modelo.fit(meses_num, df[col].values)
                
                # Previsão base
                y_pred = modelo.predict(meses_num)
                previsao_base = modelo.predict(meses_num_forecast)
                
                # Cálculo de resíduos e erro padrão
                residuos = df[col].values - y_pred
                erro_padrao = np.std(residuos)
                
                # Intervalo de confiança (95%)
                z_score = 1.96
                margem_erro = z_score * erro_padrao
                
                # Métricas de qualidade
                r2 = metrics.r2_score(df[col].values, y_pred)
                rmse = np.sqrt(metrics.mean_squared_error(df[col].values, y_pred))
                mape = np.mean(np.abs((df[col].values - y_pred) / df[col].values)) * 100
                
                # Teste de tendência (Mann-Kendall)
                tau, p_valor = stats.kendalltau(range(len(df[col].values)), df[col].values)
                
                # Cálculo dos cenários
                otimista = previsao_base + margem_erro
                conservador = previsao_base - margem_erro
                
                return {
                    'previsao': previsao_base,
                    'otimista': otimista,
                    'conservador': conservador,
                    'metricas': {
                        'R²': r2,
                        'RMSE': rmse,
                        'MAPE': mape,
                        'Erro Padrão': erro_padrao,
                        'Tendência (tau)': tau,
                        'P-valor tendência': p_valor
                    }
                }
            except Exception as e:
                st.error(f"Erro ao calcular previsões para {col}: {str(e)}")
                return None

        # KPIs para previsão
        kpis = ["Leads", "Clientes Web", "Receita Web", "CAC", "LTV", "ROI (%)"]
        
        # Calcular previsões
        resultados = {}
        for kpi in kpis:
            resultados[kpi] = prever_cenarios(kpi)

        # Exibir resultados
        st.markdown("### Previsões com Validação Estatística")
        
        for kpi in kpis:
            if resultados[kpi]:
                st.markdown(f"#### {kpi}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Gráfico com previsões e intervalos de confiança
                    fig = go.Figure()
                    
                    # Dados históricos
                    fig.add_trace(go.Scatter(
                        x=meses,
                        y=df[kpi],
                        name="Histórico",
                        mode="lines+markers",
                        line=dict(color='#3b82f6', width=3)
                    ))
                    
                    # Previsão
                    fig.add_trace(go.Scatter(
                        x=previsao_meses,
                        y=resultados[kpi]['previsao'],
                        name="Previsão",
                        mode="lines+markers",
                        line=dict(color='#10b981', width=3, dash='dot')
                    ))
                    
                    # Intervalos de confiança
                    fig.add_trace(go.Scatter(
                        x=previsao_meses,
                        y=resultados[kpi]['otimista'],
                        name="IC Superior (95%)",
                        mode="lines",
                        line=dict(color='rgba(16, 185, 129, 0.3)', dash='dash')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=previsao_meses,
                        y=resultados[kpi]['conservador'],
                        name="IC Inferior (95%)",
                        mode="lines",
                        line=dict(color='rgba(239, 68, 68, 0.3)', dash='dash'),
                        fill='tonexty'
                    ))
                    
                    fig.update_layout(
                        title=f"Previsão: {kpi}",
                        xaxis_title="Mês",
                        yaxis_title=kpi,
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Métricas de qualidade
                    st.markdown("**Métricas de Qualidade**")
                    metricas = resultados[kpi]['metricas']
                    
                    # Avaliação da qualidade
                    if metricas['R²'] > 0.8:
                        r2_status = "✅ Excelente"
                    elif metricas['R²'] > 0.6:
                        r2_status = "⚠️ Moderado"
                    else:
                        r2_status = "❌ Baixo"
                        
                    if metricas['MAPE'] < 10:
                        mape_status = "✅ Baixo"
                    elif metricas['MAPE'] < 20:
                        mape_status = "⚠️ Moderado"
                    else:
                        mape_status = "❌ Alto"
                        
                    if metricas['P-valor tendência'] < 0.05:
                        tend_status = "📈 Significativa" if metricas['Tendência (tau)'] > 0 else "📉 Significativa"
                    else:
                        tend_status = "➖ Não significativa"
                    
                    st.metric("R² (Ajuste do Modelo)", f"{metricas['R²']:.3f}", r2_status)
                    st.metric("MAPE (Erro %)", f"{metricas['MAPE']:.1f}%", mape_status)
                    st.metric("Tendência", f"{metricas['Tendência (tau)']:.3f}", tend_status)
                
                st.markdown("---")

        # Análise de correlação entre KPIs
        st.markdown("### Análise de Correlação entre KPIs")
        corr_matrix = df[kpis].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            labels=dict(color="Correlação"),
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig_corr.update_layout(
            title="Matriz de Correlação",
            height=500
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Insights baseados nas correlações
        st.markdown("### Insights das Análises")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Qualidade das Previsões:**
            - Modelos com R² > 0.8 são altamente confiáveis
            - MAPE < 10% indica previsões precisas
            - Tendências significativas sugerem padrões consistentes
            """)
            
            st.markdown("""
            **Recomendações para Uso:**
            1. Priorize KPIs com maior R² e menor MAPE
            2. Use intervalos de confiança para planejamento
            3. Considere tendências significativas nas decisões
            """)
        
        with col2:
            st.markdown("""
            **Limitações do Modelo:**
            - Assume tendência linear
            - Sensível a mudanças bruscas
            - Requer monitoramento contínuo
            """)
            
            st.markdown("""
            **Próximos Passos:**
            1. Atualizar dados mensalmente
            2. Validar previsões vs. realizado
            3. Ajustar modelos conforme necessário
            """)

    except Exception as e:
        st.error(f"""
        ❌ Erro ao gerar previsões e análises estatísticas.
        
        Erro: {str(e)}
        
        Verifique:
        1. Formato dos dados
        2. Quantidade de dados históricos
        3. Dependências instaladas
        """)

with tab7:
    st.subheader("🤝 Parceria Contador: Simulação de Indicadores")
    
    # Configurações da parceria
    meses_comissao = 6
    percentual_comissao = 0.15
    
    # Valores médios baseados nos dados filtrados
    ticket_medio = df_filtered['Ticket Médio'].mean()
    roi_medio = df_filtered['ROI (%)'].mean()
    ltv_medio = df_filtered['LTV'].mean()
    cac_medio = df_filtered['CAC'].mean()
    
    # Cálculo do custo por lead
    custo_por_lead_min = 25
    custo_por_lead_max = 50
    custo_por_lead_medio = (custo_por_lead_min + custo_por_lead_max) / 2
    
    # Comissão mensal (não acumulada)
    comissao_mensal = ticket_medio * percentual_comissao
    
    # Informações do modelo de parceria
    st.markdown(f"""
    <div class="metric-card">
        <h4>📋 Modelo de Parceria</h4>
        <ul>
            <li>Comissão: <strong>{percentual_comissao*100:.0f}%</strong> sobre o ticket mensal por <strong>{meses_comissao} meses</strong></li>
            <li>Comissão mensal por cliente: <strong>R$ {comissao_mensal:.2f}</strong></li>
            <li>Ticket Médio atual: <strong>R$ {ticket_medio:.2f}</strong></li>
            <li>ROI médio: <strong>{roi_medio:.1f}%</strong></li>
            <li>LTV médio: <strong>R$ {ltv_medio:.2f}</strong></li>
            <li>CAC médio (via ads): <strong>R$ {cac_medio:.2f}</strong></li>
            <li>Custo por Lead atual: <strong>R$ {custo_por_lead_min:.2f} - R$ {custo_por_lead_max:.2f}</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Análise: Comissão vs Custo por Lead
    st.markdown("### 💡 Análise: Comissão vs Custo por Lead")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Comparativo visual
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=['Custo Lead Mín', 'Custo Lead Máx', 'Custo Lead Médio', 'Comissão Mensal'],
            y=[custo_por_lead_min, custo_por_lead_max, custo_por_lead_medio, comissao_mensal],
            marker_color=['#fbbf24', '#f59e0b', '#d97706', '#10b981'],
            text=[f'R$ {custo_por_lead_min:.2f}', f'R$ {custo_por_lead_max:.2f}', 
                  f'R$ {custo_por_lead_medio:.2f}', f'R$ {comissao_mensal:.2f}'],
            textposition='outside'
        ))
        fig_comp.update_layout(
            title="Comparação: Custo Lead vs Comissão Contador",
            height=350,
            showlegend=False,
            yaxis_title="Valor (R$)"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        # Análise do percentual
        ratio_min = (comissao_mensal / custo_por_lead_max) * 100
        ratio_max = (comissao_mensal / custo_por_lead_min) * 100
        ratio_medio = (comissao_mensal / custo_por_lead_medio) * 100
        
        st.markdown("**Análise do Percentual de 15%:**")
        st.metric("Comissão vs Custo Lead Mín", f"{ratio_max:.0f}%", 
                  "✅ Saudável" if ratio_max <= 100 else "⚠️ Alto")
        st.metric("Comissão vs Custo Lead Máx", f"{ratio_min:.0f}%", 
                  "✅ Saudável" if ratio_min <= 100 else "⚠️ Alto")
        st.metric("Comissão vs Custo Lead Médio", f"{ratio_medio:.0f}%", 
                  "✅ Saudável" if ratio_medio <= 100 else "⚠️ Alto")
        
        if ratio_medio <= 100:
            status_comissao = "success-box"
            icone = "✅"
            mensagem = f"O percentual de <strong>{percentual_comissao*100:.0f}%</strong> é <strong>saudável</strong>! A comissão mensal (R$ {comissao_mensal:.2f}) representa apenas <strong>{ratio_medio:.0f}%</strong> do custo médio por lead."
        else:
            status_comissao = "alert-box"
            icone = "⚠️"
            mensagem = f"O percentual de <strong>{percentual_comissao*100:.0f}%</strong> está <strong>alto</strong>. A comissão mensal (R$ {comissao_mensal:.2f}) representa <strong>{ratio_medio:.0f}%</strong> do custo médio por lead."
        
        st.markdown(f"""
        <div class="{status_comissao}">
            <h4>{icone} Conclusão</h4>
            <p>{mensagem}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Simulação de receita do contador - MÊS A MÊS
    st.markdown("### 💰 Simulação: Receita Mensal por Cliente Indicado")
    
    # Cálculos mensais (não acumulados)
    comissao_total_6m = comissao_mensal * meses_comissao  # Total que o contador recebe em 6 meses
    receita_mensal_empresa = ticket_medio  # Receita mensal da empresa por cliente
    receita_6m_empresa = receita_mensal_empresa * meses_comissao  # Receita empresa em 6 meses
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Comissão Mensal", f"R$ {comissao_mensal:,.2f}")
    
    with col2:
        st.metric("Comissão Total (6m)", f"R$ {comissao_total_6m:,.2f}")
    
    with col3:
        st.metric("Receita Empresa/Mês", f"R$ {receita_mensal_empresa:,.2f}")
    
    with col4:
        st.metric("LTV Estimado", f"R$ {ltv_medio:,.2f}")
    
    # Tabela detalhada mês a mês
    st.markdown("#### 📅 Detalhamento Mês a Mês (Por Cliente)")
    
    meses_detalhe = [f"Mês {i+1}" for i in range(meses_comissao)]
    dados_mensais = {
        'Mês': meses_detalhe,
        'Receita Empresa': [receita_mensal_empresa] * meses_comissao,
        'Comissão Contador': [comissao_mensal] * meses_comissao,
        '% Comissão': [f"{percentual_comissao*100:.0f}%"] * meses_comissao,
        'Lucro Empresa': [receita_mensal_empresa - comissao_mensal] * meses_comissao
    }
    
    df_mensal = pd.DataFrame(dados_mensais)
    st.dataframe(df_mensal, use_container_width=True, hide_index=True)
    
    # Gráfico mês a mês
    fig_mensal = go.Figure()
    
    fig_mensal.add_trace(go.Bar(
        x=meses_detalhe,
        y=[receita_mensal_empresa] * meses_comissao,
        name='Receita Empresa',
        marker_color='#10b981'
    ))
    
    fig_mensal.add_trace(go.Bar(
        x=meses_detalhe,
        y=[comissao_mensal] * meses_comissao,
        name='Comissão Contador',
        marker_color='#3b82f6'
    ))
    
    fig_mensal.update_layout(
        title="Distribuição Mensal: Receita vs Comissão (por cliente)",
        xaxis_title="Período",
        yaxis_title="Valor (R$)",
        height=400,
        barmode='group'
    )
    
    st.plotly_chart(fig_mensal, use_container_width=True)
    
    st.markdown("---")
    
    # Comparativo CAC
    st.markdown("### 📊 Comparativo: CAC Ads vs CAC Indicação")
    
    # CAC da indicação = total de comissões pagas
    cac_indicacao = comissao_total_6m
    economia_vs_ads = cac_medio - cac_indicacao
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cac = go.Figure()
        fig_cac.add_trace(go.Bar(
            x=['CAC Google Ads', 'CAC Indicação'],
            y=[cac_medio, cac_indicacao],
            marker_color=['#ea4335', '#10b981'],
            text=[f'R$ {cac_medio:.2f}', f'R$ {cac_indicacao:.2f}'],
            textposition='outside'
        ))
        fig_cac.update_layout(
            title="Comparação de CAC",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_cac, use_container_width=True)
        
        # Métricas de economia
        st.metric(
            "Economia vs Ads", 
            f"R$ {economia_vs_ads:,.2f}",
            f"{(economia_vs_ads/cac_medio)*100:.1f}%"
        )
    
    with col2:
        # Relação CAC:LTV para indicação
        cac_ltv_indicacao = ltv_medio / cac_indicacao
        cac_ltv_ads = ltv_medio / cac_medio
        
        fig_ratio = go.Figure()
        fig_ratio.add_trace(go.Bar(
            x=['CAC:LTV Ads', 'CAC:LTV Indicação'],
            y=[cac_ltv_ads, cac_ltv_indicacao],
            marker_color=['#ea4335', '#10b981'],
            text=[f'{cac_ltv_ads:.1f}:1', f'{cac_ltv_indicacao:.1f}:1'],
            textposition='outside'
        ))
        fig_ratio.add_hline(
            y=4, 
            line_dash="dash", 
            line_color="orange",
            annotation_text="Benchmark Ideal (4:1)"
        )
        fig_ratio.update_layout(
            title="Relação CAC:LTV",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    st.markdown("---")
    
    # Simulador interativo
    st.markdown("### 🎯 Simulador de Impacto")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Parâmetros da Simulação**")
        num_clientes = st.slider(
            "Número de clientes indicados/mês:",
            min_value=1,
            max_value=50,
            value=10,
            step=1
        )
        
        meses_simulacao = st.slider(
            "Período de simulação (meses):",
            min_value=1,
            max_value=12,
            value=6,
            step=1
        )
    
    with col2:
        # Cálculos da simulação - MÊS A MÊS
        total_clientes = num_clientes * meses_simulacao
        
        # Comissão mensal = num_clientes * comissão_mensal
        comissao_mensal_total = num_clientes * comissao_mensal
        comissao_total_periodo = comissao_mensal_total * meses_simulacao
        
        # Receita mensal da empresa
        receita_mensal_total = num_clientes * receita_mensal_empresa
        receita_total_periodo = receita_mensal_total * meses_simulacao
        
        # Economia total
        economia_total = economia_vs_ads * total_clientes
        
        st.markdown("**Resultados da Simulação**")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Total Clientes", f"{total_clientes}")
            st.metric("Comissão/Mês", f"R$ {comissao_mensal_total:,.2f}")
        
        with col_b:
            st.metric("Comissão Total", f"R$ {comissao_total_periodo:,.2f}")
            st.metric("Receita/Mês", f"R$ {receita_mensal_total:,.2f}")
        
        with col_c:
            roi_indicacao = ((receita_total_periodo - comissao_total_periodo) / comissao_total_periodo) * 100
            st.metric("ROI Indicação", f"{roi_indicacao:.1f}%")
            st.metric("Economia Total", f"R$ {economia_total:,.2f}")
    
    st.markdown("---")
    
    # Projeção mensal
    st.markdown("### 📈 Projeção Mensal de Crescimento")
    
    meses_proj = [f"Mês {i+1}" for i in range(meses_simulacao)]
    
    # Novos clientes a cada mês
    novos_clientes_mes = [num_clientes] * meses_simulacao
    
    # Receita e comissão MENSAL (não acumulada)
    # A cada mês entra num_clientes novos, mas os antigos continuam pagando
    receita_mensal_proj = []
    comissao_mensal_proj = []
    
    for i in range(meses_simulacao):
        # Clientes ativos no mês = todos que entraram nos últimos 6 meses
        # (após 6 meses, não há mais comissão)
        clientes_ativos = min((i + 1) * num_clientes, num_clientes * min(i + 1, meses_comissao))
        
        # Receita mensal
        receita_mes = clientes_ativos * receita_mensal_empresa
        receita_mensal_proj.append(receita_mes)
        
        # Comissão mensal: apenas clientes nos primeiros 6 meses
        if i < meses_comissao:
            comissao_mes = (i + 1) * num_clientes * comissao_mensal
        else:
            # Após o 6º mês, sempre haverá 6 meses de clientes pagando comissão
            comissao_mes = num_clientes * meses_comissao * comissao_mensal
        
        comissao_mensal_proj.append(comissao_mes)
    
    fig_proj = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Receita Mensal da Empresa', 'Comissão Mensal aos Contadores'),
        vertical_spacing=0.15
    )
    
    # Gráfico 1: Receita
    fig_proj.add_trace(
        go.Bar(
            x=meses_proj,
            y=receita_mensal_proj,
            name='Receita Mensal',
            marker_color='#10b981',
            text=[f'R$ {v:,.0f}' for v in receita_mensal_proj],
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Gráfico 2: Comissão
    fig_proj.add_trace(
        go.Bar(
            x=meses_proj,
            y=comissao_mensal_proj,
            name='Comissão Mensal',
            marker_color='#3b82f6',
            text=[f'R$ {v:,.0f}' for v in comissao_mensal_proj],
            textposition='outside'
        ),
        row=2, col=1
    )
    
    fig_proj.update_layout(
        title=f"Projeção com {num_clientes} novas indicações/mês",
        height=600,
        showlegend=False
    )
    
    fig_proj.update_xaxes(title_text="Período", row=2, col=1)
    fig_proj.update_yaxes(title_text="Receita (R$)", row=1, col=1)
    fig_proj.update_yaxes(title_text="Comissão (R$)", row=2, col=1)
    
    st.plotly_chart(fig_proj, use_container_width=True)
    
    # Resumo da projeção
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Receita Mensal (último mês)", f"R$ {receita_mensal_proj[-1]:,.2f}")
    
    with col2:
        st.metric("Comissão Mensal (último mês)", f"R$ {comissao_mensal_proj[-1]:,.2f}")
    
    with col3:
        margem_ultimo_mes = ((receita_mensal_proj[-1] - comissao_mensal_proj[-1]) / receita_mensal_proj[-1]) * 100
        st.metric("Margem Líquida", f"{margem_ultimo_mes:.1f}%")
    
    st.markdown("---")
    
    # Análise de benefícios
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4>✅ Vantagens da Parceria</h4>
            <ul>
                <li><strong>Menor CAC:</strong> Economia de R$ {:.2f} por cliente (redução de {:.1f}%)</li>
                <li><strong>Comissão competitiva:</strong> R$ {:.2f}/mês representa {:.0f}% do custo médio por lead</li>
                <li><strong>Maior qualidade:</strong> Indicações geralmente têm melhor fit e maior taxa de conversão</li>
                <li><strong>Relação CAC:LTV melhor:</strong> {:.1f}:1 vs {:.1f}:1 (ads)</li>
                <li><strong>Sem risco:</strong> Pagamento apenas após conversão em cliente</li>
                <li><strong>Escalável:</strong> Rede de contadores pode crescer exponencialmente</li>
                <li><strong>Confiança:</strong> Indicação de profissional de confiança aumenta credibilidade</li>
                <li><strong>Modelo recorrente:</strong> Comissão mensal incentiva acompanhamento contínuo</li>
            </ul>
        </div>
        """.format(
            economia_vs_ads, 
            (economia_vs_ads/cac_medio)*100, 
            comissao_mensal,
            ratio_medio,
            cac_ltv_indicacao, 
            cac_ltv_ads
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📌 Pontos de Atenção</h4>
            <ul>
                <li><strong>Gestão de parceiros:</strong> Necessário sistema de acompanhamento de indicações</li>
                <li><strong>Treinamento:</strong> Contadores precisam conhecer o produto</li>
                <li><strong>SLA de pagamento:</strong> Definir prazos claros para comissões</li>
                <li><strong>Qualificação:</strong> Estabelecer critérios para indicações válidas</li>
                <li><strong>Suporte:</strong> Canal dedicado para dúvidas dos parceiros</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recomendações estratégicas
    st.markdown("### 🎯 Recomendações Estratégicas")
    
    st.markdown("""
    <div class="alert-box">
        <h4>📋 Plano de Ação Sugerido</h4>
        <ol>
            <li><strong>Fase 1 - Piloto (Mês 1-2):</strong>
                <ul>
                    <li>Selecionar 5-10 contadores parceiros</li>
                    <li>Criar material de apoio e treinamento</li>
                    <li>Definir processo de indicação e tracking</li>
                    <li>Meta: 3-5 clientes indicados</li>
                </ul>
            </li>
            <li><strong>Fase 2 - Expansão (Mês 3-6):</strong>
                <ul>
                    <li>Recrutar mais 20-30 contadores</li>
                    <li>Implementar sistema de gamificação</li>
                    <li>Criar programa de benefícios por performance</li>
                    <li>Meta: 10-15 clientes/mês</li>
                </ul>
            </li>
            <li><strong>Fase 3 - Escala (Mês 7+):</strong>
                <ul>
                    <li>Automatizar onboarding de parceiros</li>
                    <li>Criar comunidade de parceiros</li>
                    <li>Desenvolver co-marketing</li>
                    <li>Meta: 20+ clientes/mês</li>
                </ul>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs para monitoramento
    st.markdown("### 📊 KPIs para Monitoramento do Programa")
    
    kpis_parceria = pd.DataFrame({
        'KPI': [
            'Número de Parceiros Ativos',
            'Indicações Qualificadas/Mês',
            'Taxa de Conversão Indicações',
            'CAC Médio por Indicação',
            'LTV Médio Clientes Indicados',
            'Tempo Médio de Conversão',
            'NPS dos Parceiros',
            'Receita via Parceria (%)'
        ],
        'Meta Mês 3': ['15', '10', '40%', f'R$ {cac_indicacao:.2f}', f'R$ {ltv_medio:.2f}', '30 dias', '8+', '10%'],
        'Meta Mês 6': ['30', '20', '45%', f'R$ {cac_indicacao*0.9:.2f}', f'R$ {ltv_medio*1.1:.2f}', '25 dias', '9+', '20%'],
        'Meta Mês 12': ['50+', '30+', '50%', f'R$ {cac_indicacao*0.8:.2f}', f'R$ {ltv_medio*1.2:.2f}', '20 dias', '9+', '30%']
    })
    
    st.dataframe(kpis_parceria, use_container_width=True, hide_index=True)
    
    st.info("""
    💡 **Nota:** Os cálculos utilizam os valores médios dos dados históricos. 
    Para análises mais precisas, recomenda-se criar uma coluna de origem do lead 
    para rastrear especificamente os clientes vindos de indicações de contadores.
    """)

# Footer
st.markdown("---")
st.caption("Dashboard de Marketing - SaaS ERP | Atualizado em Setembro 2025")
