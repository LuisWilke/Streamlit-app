import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import fdb
import json
import os
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas - Análise Avançada",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
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
    .sql-editor {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        padding: 0.75rem;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        
    def connect(self, host, database, user, password, port=3050):
        """Conecta ao banco de dados Firebird"""
        try:
            dsn = f"{host}/{port}:{database}"
            self.connection = fdb.connect(
                dsn=dsn,
                user=user,
                password=password,
                charset='NONE'
            )
            return True, "Conexão estabelecida com sucesso!"
        except Exception as e:
            return False, f"Erro na conexão: {str(e)}"
    
    def execute_query(self, query, params=None):
        """Executa uma consulta SQL e retorna um DataFrame"""
        if not self.connection:
            return None, "Não há conexão ativa com o banco de dados"
        
        try:
            cursor = self.connection.cursor()
            if params:
                # Agora params é uma tupla/lista para parâmetros posicionais
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obter nomes das colunas
            columns = [desc[0] for desc in cursor.description]
            
            # Obter dados
            data = cursor.fetchall()
            cursor.close()
            
            # Criar DataFrame
            df = pd.DataFrame(data, columns=columns)
            return df, "Consulta executada com sucesso!"
        except Exception as e:
            return None, f"Erro na execução da consulta: {str(e)}"
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None

def save_query(name, query):
    """Salva uma consulta SQL em arquivo JSON"""
    queries_file = "saved_queries.json"
    
    if os.path.exists(queries_file):
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries = json.load(f)
    else:
        queries = {}
    
    queries[name] = {
        "query": query,
        "created_at": datetime.now().isoformat()
    }
    
    with open(queries_file, 'w', encoding='utf-8') as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)

def load_queries():
    """Carrega consultas salvas do arquivo JSON"""
    queries_file = "saved_queries.json"
    
    if os.path.exists(queries_file):
        with open(queries_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def create_advanced_charts(df):
    """Cria visualizações avançadas com base nos dados"""
    charts = []
    
    if df.empty:
        return charts
    
    # Detectar colunas numéricas e categóricas
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Gráfico 1: Distribuição de valores (se houver colunas numéricas)
    if numeric_cols:
        col = numeric_cols[0]
        fig = px.histogram(df, x=col, title=f"Distribuição de {col}", 
                          color_discrete_sequence=['#1f77b4'])
        fig.update_layout(showlegend=False)
        charts.append(("Distribuição", fig))
    
    # Gráfico 2: Análise temporal (se houver colunas de data)
    if date_cols and numeric_cols:
        date_col = date_cols[0]
        value_col = numeric_cols[0]
        df_temp = df.copy()
        df_temp[date_col] = pd.to_datetime(df_temp[date_col])
        df_grouped = df_temp.groupby(df_temp[date_col].dt.date)[value_col].sum().reset_index()
        
        fig = px.line(df_grouped, x=date_col, y=value_col, 
                     title=f"Evolução Temporal de {value_col}",
                     color_discrete_sequence=['#ff7f0e'])
        charts.append(("Evolução Temporal", fig))
    
    # Gráfico 3: Top 10 categorias (se houver colunas categóricas e numéricas)
    if categorical_cols and numeric_cols:
        cat_col = categorical_cols[0]
        value_col = numeric_cols[0]
        
        top_categories = df.groupby(cat_col)[value_col].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(x=top_categories.values, y=top_categories.index, 
                    orientation='h', title=f"Top 10 {cat_col} por {value_col}",
                    color_discrete_sequence=['#2ca02c'])
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        charts.append(("Top 10", fig))
    
    # Gráfico 4: Correlação entre variáveis numéricas
    if len(numeric_cols) >= 2:
        correlation_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(correlation_matrix, 
                       title="Matriz de Correlação",
                       color_continuous_scale='RdBu_r',
                       aspect="auto")
        fig.update_layout(width=600, height=500)
        charts.append(("Correlação", fig))
    
    return charts

def main():
    # Título principal
    st.markdown('<h1 class="main-header">📊 Dashboard de Vendas - Análise Avançada</h1>', 
                unsafe_allow_html=True)
    
    # Inicializar conexão de banco de dados na sessão
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = DatabaseConnection()
    
    # Sidebar para configurações
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🔧 Configurações")
        
        # Configurações de conexão
        st.subheader("Conexão com Banco de Dados")
        
        host = st.text_input("Host", value="localhost", help="Endereço do servidor Firebird")
        port = st.number_input("Porta", value=3050, min_value=1, max_value=65535)
        database = st.text_input("Caminho do Banco", help="Caminho completo para o arquivo .fdb", value="c:/ecosis/dados/ecodados.eco")
        user = st.text_input("Usuário", value="SYSDBA")
        password = st.text_input("Senha", type="password")
        
        if st.button("🔌 Conectar", type="primary"):
            success, message = st.session_state.db_connection.connect(host, database, user, password, port)
            if success:
                st.success(message)
                st.session_state.connected = True
            else:
                st.error(message)
                st.session_state.connected = False
        
        # Status da conexão
        if hasattr(st.session_state, 'connected') and st.session_state.connected:
            st.success("✅ Conectado")
        else:
            st.warning("⚠️ Não conectado")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Seção de consultas salvas
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("💾 Consultas Salvas")
        
        saved_queries = load_queries()
        if saved_queries:
            selected_query = st.selectbox("Selecionar consulta:", 
                                        [""] + list(saved_queries.keys()))
            if selected_query and st.button("📥 Carregar Consulta"):
                st.session_state.current_query = saved_queries[selected_query]["query"]
                st.rerun()
        else:
            st.info("Nenhuma consulta salva")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Área principal
    tab1, tab2, tab3 = st.tabs(["🔍 Consulta SQL", "📊 Visualizações", "⚙️ Configurações Avançadas"])
    
    with tab1:
        st.header("Editor de Consulta SQL")
        
        # Query padrão (a consulta fornecida pelo usuário, com parâmetros posicionais)
        default_query = """WITH vendas AS (
    SELECT
        ped.nfeletronica AS emitiu_nfe,
        ped.empresa AS empresa,
        ped.codigo AS pedido,
        extract(year FROM ped.dataefe) || '/' || lpad(extract(month FROM ped.dataefe),2,'0') AS ano_mes,
        ped.dataefe AS data_efe,
        ped.notanfe AS nfe,
        ped.numeronfce AS nfce,    
        ped.agente,
        age.nome AS nome_agente,
        ven.codigo AS vendedor,    
        ven.nome AS nome_vendedor,     
        clg.nome || ' (' || clg.codigo || ')' AS cliente,
        cid.nome || ' (' || cid.codigo || ')' AS cidade,
        cid.estado,
        reg.nome || ' (' || reg.codigo || ')' AS regiao,
        atv.descricao || ' (' || atv.codigo || ')' AS atividade,
        clg.cep,
        CASE nat.tipoentrada
            WHEN 'D' THEN 'Devolução'
            ELSE 'Venda'
        END AS tipo,
        pdt.produto AS cod_produto,
        pdg.descricaograde || ' - ' || pdg.embalagem || '/' || cast(pdg.qtdeembalagem AS integer) AS produto,
        mar.descricao || ' (' || mar.codigo || ')' AS marca,
        fab.descricao || ' (' || fab.codigo || ')' AS fabricante,
        str.descricao || ' (' || str.codigo || ')' AS setor,
        grp.descricao || ' (' || grp.codigo || ')' AS grupo,
        grp.descricao || '-' || sgr.descricao || ' (' || sgr.subgrupo || ')' AS subgrupo,
        coalesce((tab.descricao || ' (' || pdt.idtabelapreco || ')'), pdt.idtabelapreco, 'sem-tabela') AS tabela,
        CASE tab.tipopreco
            WHEN 'V' THEN 'Varejo'
            WHEN 'A' THEN 'Atacado'
            WHEN 'P' THEN 'Promocao'
            ELSE 'Sem-tabela'
        END AS tipo_tabela,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN pdt.qtde * -1
            ELSE pdt.qtde
        END) AS quantidade,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN (pdt.custofabrica * pdt.qtde) * -1
            ELSE (pdt.custofabrica * pdt.qtde)
        END) AS custofabrica,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN (pdt.custoreposicao * pdt.qtde) * -1
            ELSE (pdt.custoreposicao * pdt.qtde)
        END) AS custoreposicao,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN (pdt.custofinal * pdt.qtde) * -1
            ELSE (pdt.custofinal * pdt.qtde)
        END) AS custofinal,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN pdt.vlrliquido * -1
            ELSE pdt.vlrliquido
        END) AS valorliquido,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN pdt.frete * -1
            ELSE pdt.frete
        END) AS frete,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN pdt.despesas * -1
            ELSE pdt.despesas
        END) AS despesas,
        SUM(CASE nat.tipoentrada
            WHEN 'D' THEN (pdt.vlrliquido + pdt.frete + pdt.despesas) * -1
            ELSE (pdt.vlrliquido + pdt.frete + pdt.despesas)
        END) AS vlr_total
    FROM tvenpedido ped
    LEFT JOIN tvenproduto pdt ON (pdt.empresa = ped.empresa AND pdt.pedido = ped.codigo)
    LEFT JOIN testnatureza nat ON (nat.codigo = ped.tipooperacao)
    LEFT JOIN tvenvendedor ven ON (ven.empresa = ped.empresa AND ven.codigo = ped.vendedor)
    LEFT JOIN tvenvendedor age ON (age.empresa = ped.empresa AND age.codigo = ped.agente)
    LEFT JOIN testprodutogeral pdg ON (pdg.codigo = pdt.produto)
    LEFT JOIN testmarca mar ON (mar.codigo = pdg.marca)
    LEFT JOIN testfabricante fab ON (fab.codigo = pdg.fabricante)
    LEFT JOIN testproduto pro ON (pro.empresa = pdt.empresa AND pro.produto = pdt.produto)
    LEFT JOIN testgrupo grp ON (grp.empresa = pro.empresa AND grp.codigo = pro.grupo)
    LEFT JOIN testsubgrupo sgr ON (sgr.empresa = pro.empresa AND sgr.grupo = pro.grupo AND sgr.subgrupo = pro.subgrupo)
    LEFT JOIN testsetor str ON (str.empresa = pro.empresa AND str.codigo = pro.setor)
    LEFT JOIN testtabelapreco tab ON (tab.empresa = pdt.empresa AND tab.idtabelapreco = pdt.idtabelapreco)
    LEFT JOIN trecclientegeral clg ON (clg.codigo = ped.cliente)
    LEFT JOIN tgercidade cid ON (cid.codigo = clg.cidade)
    LEFT JOIN trecregiao reg ON (reg.gid = clg.gidregiao)
    LEFT JOIN trecatividade atv ON (atv.codigo = clg.atividade)
    WHERE ped.empresa = ?
      AND nat.geraestatistica = 'S'
      AND nat.gerafinanceiro = 'S'
      AND nat.tiposaida <> 'T'    
      AND ped.status = 'EFE'
      AND ped.dataefe BETWEEN ? AND ?
      AND (? IS NULL OR pdt.produto = ?) -- Condição para produto opcional
      AND (? IS NULL OR ped.cliente = ?) -- Condição para cliente opcional
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27
)

SELECT 
    ven.*,
    CASE ven.custofabrica
        WHEN 0 THEN 0
        ELSE CAST((ven.valorliquido / ven.custofabrica) AS numeric(15,2))
    END AS markup_fabrica_x_vendas,
    CASE ven.custoreposicao
        WHEN 0 THEN 0
        ELSE CAST((ven.valorliquido / ven.custoreposicao) AS numeric(15,2))
    END AS markup_custoreposicao_x_vendas,
    CASE ven.custofinal
        WHEN 0 THEN 0
        ELSE CAST((ven.valorliquido / ven.custofinal) AS numeric(15,2))
    END AS markup_custofinal_x_vendas,
    COALESCE(p.valoresespecificos, 'N') AS tem_valor_especifico
FROM vendas ven
LEFT JOIN (
    SELECT p1.empresa, p1.produto, 'S' AS valoresespecificos
    FROM testtabelaprecoprodutos p1
    WHERE p1.valoresespecificos = 'S'
    GROUP BY p1.empresa, p1.produto
) p ON p.empresa = ven.empresa AND p.produto = ven.cod_produto;
"""
        
        # Editor de SQL
        current_query = st.session_state.get('current_query', default_query)
        query = st.text_area("Consulta SQL:", value=current_query, height=400, 
                           help="Digite sua consulta SQL aqui. Use parâmetros posicionais '?' para os valores dinâmicos.")
        
        # Parâmetros da consulta
        st.subheader("Parâmetros da Consulta")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            empresa = st.text_input("Empresa", value="01")
        with col2:
            data_inicio = st.date_input("Data Início", value=date(2024, 1, 1))
        with col3:
            data_fim = st.date_input("Data Fim", value=date.today())
        with col4:
            produto = st.text_input("Produto (opcional)", value="")
        
        cliente = st.text_input("Cliente (opcional)", value="")
        
        # Botões de ação
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Executar Consulta", type="primary"):
                if hasattr(st.session_state, 'connected') and st.session_state.connected:
                    # Construir a tupla de parâmetros na ordem correta
                    # Para parâmetros opcionais, passamos o valor e o valor novamente
                    # para a condição `(? IS NULL OR coluna = ?)`.
                    # Se o campo estiver vazio, passamos None para que `? IS NULL` seja verdadeiro.
                    
                    params = (
                        empresa,
                        data_inicio,
                        data_fim,
                        None if not produto else produto, # Primeiro ? para o IS NULL
                        produto, # Segundo ? para a comparação
                        None if not cliente else cliente, # Primeiro ? para o IS NULL
                        cliente # Segundo ? para a comparação
                    )
                    
                    with st.spinner("Executando consulta..."):
                        df, message = st.session_state.db_connection.execute_query(query, params)
                        
                    if df is not None:
                        st.success(message)
                        st.session_state.current_data = df
                        
                        # Mostrar informações básicas
                        st.info(f"📊 Consulta retornou {len(df)} registros com {len(df.columns)} colunas")
                        
                        # Mostrar preview dos dados
                        st.subheader("Preview dos Dados")
                        st.dataframe(df.head(100), use_container_width=True)
                        
                        # Estatísticas básicas
                        if not df.empty:
                            st.subheader("Estatísticas Básicas")
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            if len(numeric_cols) > 0:
                                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                    else:
                        st.error(message)
                else:
                    st.error("❌ Conecte-se ao banco de dados primeiro!")
        
        with col2:
            query_name = st.text_input("Nome da consulta", placeholder="Ex: Vendas Mensais")
            if st.button("💾 Salvar Consulta"):
                if query_name:
                    save_query(query_name, query)
                    st.success(f"Consulta '{query_name}' salva!")
                    st.rerun()
                else:
                    st.error("Digite um nome para a consulta")
        
        with col3:
            if st.button("🔄 Limpar Editor"):
                st.session_state.current_query = ""
                st.rerun()
    
    with tab2:
        st.header("Visualizações Avançadas")
        
        if 'current_data' in st.session_state and not st.session_state.current_data.empty:
            df = st.session_state.current_data
            
            # Criar gráficos automaticamente
            charts = create_advanced_charts(df)
            
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
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                chart_type = st.selectbox("Tipo de Gráfico", 
                                        ["Barras", "Linha", "Dispersão", "Pizza", "Histograma"])
            
            with col2:
                if numeric_cols:
                    y_axis = st.selectbox("Eixo Y (Valores)", numeric_cols)
                else:
                    st.warning("Nenhuma coluna numérica encontrada")
                    y_axis = None
            
            with col3:
                if categorical_cols:
                    x_axis = st.selectbox("Eixo X (Categorias)", [""] + categorical_cols)
                else:
                    x_axis = ""
            
            if st.button("📈 Gerar Gráfico Personalizado") and y_axis:
                if chart_type == "Barras" and x_axis:
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} por {x_axis}")
                elif chart_type == "Linha" and x_axis:
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"Evolução de {y_axis}")
                elif chart_type == "Dispersão" and len(numeric_cols) >= 2:
                    x_numeric = st.selectbox("Selecione X numérico:", numeric_cols)
                    fig = px.scatter(df, x=x_numeric, y=y_axis, title=f"{y_axis} vs {x_numeric}")
                elif chart_type == "Pizza" and x_axis:
                    df_grouped = df.groupby(x_axis)[y_axis].sum().reset_index()
                    fig = px.pie(df_grouped, values=y_axis, names=x_axis, title=f"Distribuição de {y_axis}")
                elif chart_type == "Histograma":
                    fig = px.histogram(df, x=y_axis, title=f"Distribuição de {y_axis}")
                else:
                    st.error("Configuração inválida para o tipo de gráfico selecionado")
                    fig = None
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Opção de download dos dados
            st.subheader("📥 Exportar Dados")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name=f"dados_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Usar BytesIO para criar o arquivo Excel em memória
                from io import BytesIO
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Dados')
                excel_buffer.seek(0) # Voltar ao início do buffer
                
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_buffer,
                    file_name=f"dados_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.info("🔍 Execute uma consulta na aba 'Consulta SQL' para visualizar os dados aqui.")
    
    with tab3:
        st.header("Configurações Avançadas")
        
        # Configurações de visualização
        st.subheader("🎨 Configurações de Visualização")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox("Tema dos Gráficos", 
                               ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"])
            
        with col2:
            color_palette = st.selectbox("Paleta de Cores", 
                                       ["Default", "Viridis", "Plasma", "Set1", "Set2", "Pastel1"])
        
        # Configurações de performance
        st.subheader("⚡ Configurações de Performance")
        
        max_rows = st.number_input("Máximo de linhas para visualização", 
                                 min_value=100, max_value=10000, value=1000)
        
        auto_refresh = st.checkbox("Atualização automática dos gráficos")
        
        # Informações do sistema
        st.subheader("ℹ️ Informações do Sistema")
        
        st.info(f"""
        **Versões das Bibliotecas:**
        - Streamlit: {st.__version__}
        - Pandas: {pd.__version__}
        - Plotly: {px.__version__ if hasattr(px, '__version__') else 'N/A'}
        
        **Status da Conexão:**
        - Banco: {'✅ Conectado' if hasattr(st.session_state, 'connected') and st.session_state.connected else '❌ Desconectado'}
        
        **Dados Carregados:**
        - Registros: {len(st.session_state.current_data) if 'current_data' in st.session_state else 0}
        - Colunas: {len(st.session_state.current_data.columns) if 'current_data' in st.session_state else 0}
        """)

if __name__ == "__main__":
    main()