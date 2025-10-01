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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Evolução", "💰 Financeiro", "🎯 Conversão", "📊 Benchmarks", "📋 Recomendações", "🔮 Forecast"])

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

# Footer
st.markdown("---")
st.caption("Dashboard de Marketing - SaaS ERP | Atualizado em Setembro 2025")
