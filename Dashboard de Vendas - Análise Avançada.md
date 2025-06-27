# Dashboard de Vendas - Análise Avançada

Este é um aplicativo Streamlit moderno para visualização de relatórios de vendas, conectado ao banco de dados Firebird 2.5.

## Características Principais

### 🔧 Funcionalidades Técnicas
- **Conexão Firebird 2.5**: Conecta-se diretamente ao banco de dados Firebird
- **Editor SQL Avançado**: Interface para escrever e executar consultas SQL personalizadas
- **Parâmetros Dinâmicos**: Suporte a parâmetros SQL (:empresa, :dta, :dtb, etc.)
- **Salvamento de Consultas**: Sistema para salvar e carregar consultas frequentes

### 📊 Visualizações Modernas
- **Gráficos Interativos**: Usando Plotly para visualizações avançadas
- **Dashboards Automáticos**: Geração automática de gráficos baseados nos dados
- **Gráficos Personalizados**: Interface para criar visualizações específicas
- **Análise Temporal**: Gráficos de evolução ao longo do tempo
- **Top Rankings**: Visualização dos principais itens por categoria
- **Matriz de Correlação**: Análise de correlações entre variáveis

### 🎨 Interface Moderna
- **Design Responsivo**: Interface adaptável para diferentes tamanhos de tela
- **Tema Customizável**: Múltiplas opções de temas e paletas de cores
- **Sidebar Organizada**: Configurações e controles bem organizados
- **Tabs Intuitivas**: Separação clara entre consulta, visualização e configurações

### 📥 Exportação de Dados
- **CSV Export**: Download dos dados em formato CSV
- **Excel Export**: Exportação para planilhas Excel
- **Nomes Automáticos**: Arquivos com timestamp automático

## Como Usar

### 1. Configuração da Conexão
1. Na sidebar, preencha os dados de conexão:
   - **Host**: Endereço do servidor Firebird
   - **Porta**: Porta do servidor (padrão: 3050)
   - **Caminho do Banco**: Caminho completo para o arquivo .fdb
   - **Usuário**: Nome de usuário (padrão: SYSDBA)
   - **Senha**: Senha do banco de dados

2. Clique em "🔌 Conectar"

### 2. Executando Consultas
1. Na aba "🔍 Consulta SQL":
   - Use o editor para escrever ou modificar consultas SQL
   - Preencha os parâmetros necessários (empresa, datas, produto, cliente)
   - Clique em "🚀 Executar Consulta"

2. A consulta padrão já está carregada com a query fornecida

### 3. Visualizando Dados
1. Na aba "📊 Visualizações":
   - Visualize gráficos gerados automaticamente
   - Crie gráficos personalizados
   - Exporte os dados em CSV ou Excel

### 4. Salvando Consultas
1. Digite um nome para a consulta
2. Clique em "💾 Salvar Consulta"
3. Use a sidebar para carregar consultas salvas

## Tecnologias Utilizadas

- **Streamlit**: Framework para aplicações web em Python
- **Plotly**: Biblioteca para gráficos interativos
- **Pandas**: Manipulação e análise de dados
- **FDB**: Conector para banco de dados Firebird
- **Python 3.11**: Linguagem de programação

## Estrutura do Projeto

```
├── app.py                 # Aplicação principal
├── saved_queries.json     # Consultas salvas (criado automaticamente)
├── requirements.txt       # Dependências (opcional)
└── README.md             # Este arquivo
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Acesso ao banco de dados Firebird 2.5

### Passos para Execução
1. Instale as dependências:
   ```bash
   pip install streamlit fdb pandas plotly
   ```

2. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

3. Acesse no navegador: `http://localhost:8501`

## Consulta SQL Padrão

O aplicativo vem com uma consulta SQL pré-configurada que analisa dados de vendas, incluindo:

- Informações de pedidos e notas fiscais
- Dados de clientes, vendedores e agentes
- Produtos, marcas, fabricantes e categorias
- Cálculos de markup e valores
- Análise de custos e margens

A consulta utiliza parâmetros para filtrar por:
- Empresa
- Período (data início e fim)
- Produto específico
- Cliente específico

## Funcionalidades Avançadas

### Gráficos Automáticos
- **Distribuição**: Histogramas de valores numéricos
- **Evolução Temporal**: Gráficos de linha para análise temporal
- **Top 10**: Rankings das principais categorias
- **Correlação**: Matriz de correlação entre variáveis

### Gráficos Personalizados
- Barras, Linha, Dispersão, Pizza, Histograma
- Seleção dinâmica de eixos X e Y
- Configuração flexível de dados

### Configurações
- Temas de gráficos (plotly, plotly_white, plotly_dark, etc.)
- Paletas de cores personalizáveis
- Controle de performance (máximo de linhas)
- Informações do sistema

## Suporte e Manutenção

Este aplicativo foi desenvolvido para ser facilmente extensível. Para adicionar novas funcionalidades:

1. **Novas Visualizações**: Modifique a função `create_advanced_charts()`
2. **Novos Tipos de Gráfico**: Adicione opções na seção de gráficos personalizados
3. **Configurações Adicionais**: Expanda a aba "Configurações Avançadas"
4. **Novos Conectores**: Adicione suporte a outros bancos de dados na classe `DatabaseConnection`

## Segurança

- As senhas são inseridas usando campos de senha (não visíveis)
- As consultas SQL são executadas com parâmetros para evitar SQL injection
- Não há armazenamento permanente de credenciais

## Performance

- Limite configurável de linhas para visualização
- Carregamento otimizado de dados
- Cache de consultas salvas
- Interface responsiva para grandes datasets

