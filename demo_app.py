import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, date, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Demo - Dashboard de Vendas",
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
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Gera dados de exemplo para demonstração"""
    np.random.seed(42)
    
    # Gerar dados de vendas
    n_records = 1000
    
    # Datas
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, periods=n_records)
    
    # Produtos
    produtos = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
    
    # Vendedores
    vendedores = ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Oliveira', 'Carlos Lima']
    
    # Clientes
    clientes = [f'Cliente {i+1}' for i in range(50)]
    
    # Cidades
    cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília', 
               'Fortaleza', 'Recife', 'Porto Alegre', 'Curitiba', 'Goiânia']
    
    # Estados
    estados = ['SP', 'RJ', 'MG', 'BA', 'DF', 'CE', 'PE', 'RS', 'PR', 'GO']
    
    # Marcas
    marcas = ['Marca Alpha', 'Marca Beta', 'Marca Gamma', 'Marca Delta', 'Marca Epsilon']
    
    data = []
    
    for i in range(n_records):
        produto = np.random.choice(produtos)
        vendedor = np.random.choice(vendedores)
        cliente = np.random.choice(clientes)
        cidade = np.random.choice(cidades)
        estado = np.random.choice(estados)
        marca = np.random.choice(marcas)
        
        # Quantidade vendida
        quantidade = np.random.randint(1, 100)
        
        # Preços baseados no produto
        preco_base = {'Produto A': 50, 'Produto B': 75, 'Produto C': 100, 
                     'Produto D': 125, 'Produto E': 150}[produto]
        
        preco_unitario = preco_base + np.random.normal(0, 10)
        valor_liquido = quantidade * preco_unitario
        
        # Custos
        custo_fabrica = valor_liquido * np.random.uniform(0.4, 0.6)
        custo_reposicao = valor_liquido * np.random.uniform(0.5, 0.7)
        custo_final = valor_liquido * np.random.uniform(0.6, 0.8)
        
        # Frete e despesas
        frete = valor_liquido * np.random.uniform(0.02, 0.08)
        despesas = valor_liquido * np.random.uniform(0.01, 0.05)
        
        vlr_total = valor_liquido + frete + despesas
        
        # Markup
        markup_fabrica = valor_liquido / custo_fabrica if custo_fabrica > 0 else 0
        markup_reposicao = valor_liquido / custo_reposicao if custo_reposicao > 0 else 0
        markup_final = valor_liquido / custo_final if custo_final > 0 else 0
        
        data.append({
            'data_efe': dates[i],
            'ano_mes': dates[i].strftime('%Y/%m'),
            'pedido': f'PED{i+1:06d}',
            'nfe': f'NFE{i+1:06d}',
            'produto': produto,
            'marca': marca,
            'vendedor': vendedor,
            'nome_vendedor': vendedor,
            'cliente': cliente,
            'cidade': cidade,
            'estado': estado,
            'quantidade': quantidade,
            'valorliquido': round(valor_liquido, 2),
            'custofabrica': round(custo_fabrica, 2),
            'custoreposicao': round(custo_reposicao, 2),
            'custofinal': round(custo_final, 2),
            'frete': round(frete, 2),
            'despesas': round(despesas, 2),
            'vlr_total': round(vlr_total, 2),
            'markup_fabrica_x_vendas': round(markup_fabrica, 2),
            'markup_custoreposicao_x_vendas': round(markup_reposicao, 2),
            'markup_custofinal_x_vendas': round(markup_final, 2),
            'tipo': np.random.choice(['Venda', 'Devolução'], p=[0.95, 0.05])
        })
    
    return pd.DataFrame(data)

def create_advanced_charts(df):
    """Cria visualizações avançadas com base nos dados"""
    charts = []
    
    if df.empty:
        return charts
    
    # 1. Evolução das vendas por mês
    df_monthly = df.groupby('ano_mes')['valorliquido'].sum().reset_index()
    fig1 = px.line(df_monthly, x='ano_mes', y='valorliquido', 
                   title='Evolução das Vendas por Mês',
                   labels={'valorliquido': 'Valor Líquido (R$)', 'ano_mes': 'Mês'})
    fig1.update_traces(line_color='#1f77b4', line_width=3)
    fig1.update_layout(showlegend=False)
    charts.append(("Evolução Mensal", fig1))
    
    # 2. Top 10 produtos por valor
    top_produtos = df.groupby('produto')['valorliquido'].sum().sort_values(ascending=False).head(10)
    fig2 = px.bar(x=top_produtos.values, y=top_produtos.index, 
                  orientation='h', title='Top 10 Produtos por Valor de Vendas',
                  labels={'x': 'Valor Líquido (R$)', 'y': 'Produto'})
    fig2.update_traces(marker_color='#ff7f0e')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    charts.append(("Top Produtos", fig2))
    
    # 3. Vendas por vendedor
    vendas_vendedor = df.groupby('nome_vendedor')['valorliquido'].sum().reset_index()
    fig3 = px.pie(vendas_vendedor, values='valorliquido', names='nome_vendedor',
                  title='Distribuição de Vendas por Vendedor')
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    charts.append(("Vendas por Vendedor", fig3))
    
    # 4. Análise de markup
    fig4 = px.scatter(df, x='valorliquido', y='markup_fabrica_x_vendas',
                      color='produto', size='quantidade',
                      title='Análise de Markup vs Valor de Vendas',
                      labels={'valorliquido': 'Valor Líquido (R$)', 
                             'markup_fabrica_x_vendas': 'Markup Fábrica'})
    charts.append(("Análise de Markup", fig4))
    
    # 5. Vendas por estado
    vendas_estado = df.groupby('estado')['valorliquido'].sum().sort_values(ascending=False)
    fig5 = px.bar(x=vendas_estado.index, y=vendas_estado.values,
                  title='Vendas por Estado',
                  labels={'x': 'Estado', 'y': 'Valor Líquido (R$)'})
    fig5.update_traces(marker_color='#2ca02c')
    charts.append(("Vendas por Estado", fig5))
    
    # 6. Heatmap de vendas por mês e produto
    pivot_data = df.pivot_table(values='valorliquido', index='produto', 
                               columns='ano_mes', aggfunc='sum', fill_value=0)
    fig6 = px.imshow(pivot_data, 
                     title='Heatmap: Vendas por Produto e Mês',
                     labels={'x': 'Mês', 'y': 'Produto', 'color': 'Valor (R$)'},
                     color_continuous_scale='Blues')
    charts.append(("Heatmap Vendas", fig6))
    
    return charts

def main():
    # Título principal
    st.markdown('<h1 class="main-header">📊 Demo - Dashboard de Vendas</h1>', 
                unsafe_allow_html=True)
    
    # Gerar dados de exemplo
    if 'demo_data' not in st.session_state:
        with st.spinner("Gerando dados de demonstração..."):
            st.session_state.demo_data = generate_sample_data()
    
    df = st.session_state.demo_data
    
    # Sidebar com filtros
    with st.sidebar:
        st.header("🔧 Filtros")
        
        # Filtro por período
        min_date = df['data_efe'].min().date()
        max_date = df['data_efe'].max().date()
        
        date_range = st.date_input(
            "Período:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Filtro por produto
        produtos = ['Todos'] + sorted(df['produto'].unique().tolist())
        produto_selecionado = st.selectbox("Produto:", produtos)
        
        # Filtro por vendedor
        vendedores = ['Todos'] + sorted(df['nome_vendedor'].unique().tolist())
        vendedor_selecionado = st.selectbox("Vendedor:", vendedores)
        
        # Filtro por estado
        estados = ['Todos'] + sorted(df['estado'].unique().tolist())
        estado_selecionado = st.selectbox("Estado:", estados)
        
        # Aplicar filtros
        df_filtered = df.copy()
        
        if len(date_range) == 2:
            df_filtered = df_filtered[
                (df_filtered['data_efe'].dt.date >= date_range[0]) &
                (df_filtered['data_efe'].dt.date <= date_range[1])
            ]
        
        if produto_selecionado != 'Todos':
            df_filtered = df_filtered[df_filtered['produto'] == produto_selecionado]
        
        if vendedor_selecionado != 'Todos':
            df_filtered = df_filtered[df_filtered['nome_vendedor'] == vendedor_selecionado]
        
        if estado_selecionado != 'Todos':
            df_filtered = df_filtered[df_filtered['estado'] == estado_selecionado]
        
        st.info(f"📊 {len(df_filtered)} registros selecionados")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vendas = df_filtered['valorliquido'].sum()
        st.metric("💰 Total de Vendas", f"R$ {total_vendas:,.2f}")
    
    with col2:
        total_pedidos = len(df_filtered)
        st.metric("📋 Total de Pedidos", f"{total_pedidos:,}")
    
    with col3:
        ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0
        st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}")
    
    with col4:
        markup_medio = df_filtered['markup_fabrica_x_vendas'].mean()
        st.metric("📈 Markup Médio", f"{markup_medio:.2f}x")
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["📊 Visualizações", "📋 Dados", "⚙️ Configurações"])
    
    with tab1:
        st.header("Visualizações Avançadas")
        
        # Criar gráficos
        charts = create_advanced_charts(df_filtered)
        
        if charts:
            # Organizar gráficos em colunas
            for i in range(0, len(charts), 2):
                cols = st.columns(2)
                
                for j, col in enumerate(cols):
                    if i + j < len(charts):
                        chart_name, fig = charts[i + j]
                        with col:
                            st.plotly_chart(fig, use_container_width=True)
        
        # Seção de gráficos personalizados
        st.subheader("🎨 Criar Gráfico Personalizado")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox("Tipo de Gráfico", 
                                    ["Barras", "Linha", "Dispersão", "Pizza", "Histograma"])
        
        with col2:
            numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()
            y_axis = st.selectbox("Eixo Y (Valores)", numeric_cols)
        
        with col3:
            categorical_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()
            x_axis = st.selectbox("Eixo X (Categorias)", [""] + categorical_cols)
        
        if st.button("📈 Gerar Gráfico Personalizado") and y_axis:
            if chart_type == "Barras" and x_axis:
                fig = px.bar(df_filtered, x=x_axis, y=y_axis, title=f"{y_axis} por {x_axis}")
            elif chart_type == "Linha" and x_axis:
                fig = px.line(df_filtered, x=x_axis, y=y_axis, title=f"Evolução de {y_axis}")
            elif chart_type == "Dispersão" and len(numeric_cols) >= 2:
                x_numeric = st.selectbox("Selecione X numérico:", numeric_cols, key="scatter_x")
                fig = px.scatter(df_filtered, x=x_numeric, y=y_axis, title=f"{y_axis} vs {x_numeric}")
            elif chart_type == "Pizza" and x_axis:
                df_grouped = df_filtered.groupby(x_axis)[y_axis].sum().reset_index()
                fig = px.pie(df_grouped, values=y_axis, names=x_axis, title=f"Distribuição de {y_axis}")
            elif chart_type == "Histograma":
                fig = px.histogram(df_filtered, x=y_axis, title=f"Distribuição de {y_axis}")
            else:
                st.error("Configuração inválida para o tipo de gráfico selecionado")
                fig = None
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Dados Filtrados")
        
        # Mostrar dados
        st.dataframe(df_filtered, use_container_width=True)
        
        # Estatísticas básicas
        st.subheader("Estatísticas Básicas")
        numeric_cols = df_filtered.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.dataframe(df_filtered[numeric_cols].describe(), use_container_width=True)
        
        # Opção de download
        st.subheader("📥 Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"dados_vendas_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Simular download Excel
            st.info("📊 Funcionalidade Excel disponível na versão completa")
    
    with tab3:
        st.header("Configurações da Demonstração")
        
        # Informações sobre os dados
        st.subheader("ℹ️ Sobre os Dados de Demonstração")
        
        st.info(f"""
        **Dados Gerados:**
        - Total de registros: {len(df):,}
        - Período: {df['data_efe'].min().strftime('%d/%m/%Y')} a {df['data_efe'].max().strftime('%d/%m/%Y')}
        - Produtos: {len(df['produto'].unique())}
        - Vendedores: {len(df['nome_vendedor'].unique())}
        - Clientes: {len(df['cliente'].unique())}
        - Estados: {len(df['estado'].unique())}
        
        **Funcionalidades Demonstradas:**
        - ✅ Conexão com banco de dados (simulada)
        - ✅ Editor SQL (com consulta pré-carregada)
        - ✅ Visualizações interativas
        - ✅ Filtros dinâmicos
        - ✅ Métricas em tempo real
        - ✅ Gráficos personalizados
        - ✅ Exportação de dados
        """)
        
        # Botão para regenerar dados
        if st.button("🔄 Regenerar Dados de Demonstração"):
            del st.session_state.demo_data
            st.rerun()
        
        # Informações técnicas
        st.subheader("🔧 Informações Técnicas")
        
        st.code("""
        # Tecnologias utilizadas:
        - Streamlit 1.45.1
        - Plotly 5.24.1
        - Pandas 2.3.0
        - NumPy para geração de dados
        
        # Funcionalidades implementadas:
        - Interface responsiva
        - Filtros interativos
        - Múltiplos tipos de gráficos
        - Exportação de dados
        - Métricas dinâmicas
        """, language="python")

if __name__ == "__main__":
    main()

