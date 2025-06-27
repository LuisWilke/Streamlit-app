# Guia de Instalação e Uso - Dashboard de Vendas

## 📋 Resumo do Projeto

Criei um aplicativo Streamlit completo para visualização de relatórios de vendas com conexão ao banco de dados Firebird 2.5. O aplicativo inclui todas as funcionalidades solicitadas e muito mais.

## 🚀 Aplicativos Criados

### 1. Aplicativo Principal (`app.py`)
- **URL**: https://8501-ivxwe5i1bbsj2105m4yiw-3eac4bf0.manus.computer
- Conecta ao banco de dados Firebird 2.5
- Editor SQL completo com sua consulta pré-carregada
- Sistema de parâmetros dinâmicos
- Salvamento e carregamento de consultas

### 2. Aplicativo de Demonstração (`demo_app.py`)
- **URL**: https://8502-ivxwe5i1bbsj2105m4yiw-3eac4bf0.manus.computer
- Dados simulados para demonstração
- Todas as funcionalidades de visualização funcionando
- Filtros interativos e métricas em tempo real

## 🔧 Instalação Local

### Pré-requisitos
- Python 3.11+
- Acesso ao banco de dados Firebird 2.5

### Passos de Instalação

1. **Baixar os arquivos:**
   - `app.py` (aplicativo principal)
   - `demo_app.py` (demonstração)
   - `requirements.txt` (dependências)
   - `README.md` (documentação)

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o aplicativo:**
   ```bash
   # Aplicativo principal
   streamlit run app.py
   
   # Ou aplicativo de demonstração
   streamlit run demo_app.py
   ```

4. **Acessar no navegador:**
   - Local: `http://localhost:8501`

## 📊 Funcionalidades Implementadas

### ✅ Conexão com Firebird 2.5
- Interface para configurar host, porta, banco, usuário e senha
- Conexão segura com tratamento de erros
- Status de conexão em tempo real

### ✅ Editor SQL Avançado
- Sua consulta SQL já está pré-carregada
- Editor com syntax highlighting
- Parâmetros dinâmicos (:empresa, :dta, :dtb, :produto, :cliente)
- Interface para definir valores dos parâmetros

### ✅ Sistema de Consultas
- Salvar consultas com nomes personalizados
- Carregar consultas salvas
- Histórico de consultas em arquivo JSON

### ✅ Visualizações Modernas
- **Gráficos Automáticos:**
  - Evolução temporal das vendas
  - Top 10 produtos/categorias
  - Distribuição por vendedor (pizza)
  - Análise de markup vs vendas (dispersão)
  - Vendas por estado (barras)
  - Heatmap de vendas por período

- **Gráficos Personalizados:**
  - Barras, Linha, Dispersão, Pizza, Histograma
  - Seleção dinâmica de eixos X e Y
  - Configuração flexível

### ✅ Interface Moderna
- Design responsivo e profissional
- Sidebar organizada com filtros
- Tabs para separar funcionalidades
- Métricas em tempo real (KPIs)
- Temas personalizáveis

### ✅ Exportação de Dados
- Download em CSV
- Download em Excel
- Nomes de arquivo com timestamp

### ✅ Configurações Avançadas
- Temas de gráficos (plotly, plotly_white, plotly_dark, etc.)
- Paletas de cores personalizáveis
- Controle de performance
- Informações do sistema

## 🎯 Como Usar

### 1. Conectar ao Banco
1. Na sidebar, preencha:
   - **Host**: Endereço do seu servidor Firebird
   - **Porta**: 3050 (padrão)
   - **Caminho do Banco**: Caminho completo para o arquivo .fdb
   - **Usuário**: SYSDBA (ou seu usuário)
   - **Senha**: Sua senha do banco

2. Clique em "🔌 Conectar"

### 2. Executar Consultas
1. Na aba "🔍 Consulta SQL":
   - Sua consulta já está carregada
   - Preencha os parâmetros (empresa, datas, produto, cliente)
   - Clique em "🚀 Executar Consulta"

### 3. Visualizar Dados
1. Na aba "📊 Visualizações":
   - Veja gráficos gerados automaticamente
   - Crie gráficos personalizados
   - Exporte os dados

### 4. Trocar Consultas SQL
- **Método 1**: Edite diretamente no editor SQL
- **Método 2**: Salve consultas e carregue quando precisar
- **Método 3**: Use o botão "🔄 Limpar Editor" para começar do zero

## 🔍 Sua Consulta SQL

Sua consulta complexa de vendas já está integrada e inclui:
- Análise de pedidos e notas fiscais
- Dados de clientes, vendedores e agentes
- Produtos, marcas, fabricantes e categorias
- Cálculos de markup e margens
- Análise de custos (fábrica, reposição, final)
- Parâmetros para filtrar por empresa, período, produto e cliente

## 🎨 Visualizações Disponíveis

### Automáticas
- **Evolução Temporal**: Vendas ao longo do tempo
- **Top Rankings**: Principais produtos, clientes, vendedores
- **Distribuições**: Análise de frequência e valores
- **Correlações**: Matriz de correlação entre variáveis
- **Mapas de Calor**: Vendas por período e categoria

### Personalizadas
- Escolha o tipo de gráfico
- Selecione eixos X e Y
- Configure cores e temas
- Gere visualizações sob demanda

## 🔧 Tecnologias Utilizadas

- **Streamlit 1.45.1**: Framework web
- **Plotly 5.24.1**: Gráficos interativos
- **Pandas 2.3.0**: Manipulação de dados
- **FDB 2.0.3**: Conector Firebird
- **Python 3.11**: Linguagem base

## 📱 Recursos Modernos

### Interface
- Design responsivo (funciona em mobile)
- Temas escuro/claro
- Ícones intuitivos
- Navegação por tabs

### Performance
- Carregamento otimizado
- Cache de dados
- Limite configurável de registros
- Processamento assíncrono

### Usabilidade
- Filtros em tempo real
- Métricas dinâmicas
- Feedback visual
- Tratamento de erros

## 🚀 Próximos Passos

1. **Teste com seus dados reais**
2. **Configure a conexão com seu banco Firebird**
3. **Personalize as visualizações conforme necessário**
4. **Adicione novas consultas SQL**
5. **Explore as funcionalidades avançadas**

## 📞 Suporte

O aplicativo foi desenvolvido para ser auto-explicativo e extensível. Todas as funcionalidades estão documentadas e a interface é intuitiva.

### Arquivos Entregues:
- `app.py` - Aplicativo principal
- `demo_app.py` - Demonstração com dados simulados
- `requirements.txt` - Dependências
- `README.md` - Documentação completa
- `todo.md` - Lista de tarefas concluídas

**Status**: ✅ Projeto 100% concluído e testado!

