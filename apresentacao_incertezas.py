import streamlit as st

# Título da apresentação
st.header("Medição do volume no streamlit")

# Declaração das bibliotecas utilizadas
st.subheader("Declaração das bibliotecas utilizadas")

code1 = '''import streamlit as st
import pandas as pd
import time'''
st.code(code1, language='python')

st.write("Neste trecho, importamos as bibliotecas necessárias para o funcionamento do código. `streamlit` é utilizado para a criação da interface web, `pandas` para manipulação de dados e `time` para controlar o tempo de atualização dos dados.")

# Função para carregar os dados do CSV
st.subheader("Função para Carregar os Dados do CSV")

code2 = \
'''
def load_csv_data():
    # Ler o arquivo CSV e selecionar apenas a última linha
    df = pd.read_csv("data.csv").tail(1)
    return df
'''
st.code(code2, language='python')

st.write("A função `load_csv_data()` é responsável por carregar os dados do arquivo CSV. Neste caso, estamos lendo o arquivo e selecionando apenas a última linha, que contém os dados mais recentes.")

# Configuração inicial do Streamlit
st.subheader("Configuração Inicial do Streamlit")

code3 = \
'''
# Configurar o Streamlit
st.title("Medição de Volume")
col1, col2, col3 = st.columns(3)

# Inicializar placeholders com valores iniciais
placeholder_hora = col1.metric("Hora", "...")
placeholder_volume_percent = col2.metric("Volume (%)", "...")
placeholder_volume_ml = col3.metric("Volume (ml)", "...")
'''
st.code(code3, language='python')

st.write("Neste trecho, configuramos a interface do Streamlit. Criamos três colunas para exibir os dados de hora, volume em percentagem e volume em mililitros. Os valores iniciais dos placeholders são definidos como '...'.")

# Loop principal para atualizar os dados
st.subheader("Loop Principal para Atualizar os Dados")

code4 = \
'''
# Loop principal para atualizar os dados
while True:
    # Carregar os dados do CSV
    df = load_csv_data()
    
    for index, row in df.iterrows():
        # Extrair apenas a parte da hora do timestamp
        hora = pd.to_datetime(row['Timestamp']).strftime('%H:%M:%S')  # Formato de hora: HH:MM:SS

        # Calcular o volume em porcentagem em relação aos 2 litros
        volume_ml = row['Volume (ml)']
        volume_percent = (volume_ml / 2000) * 100  # 2 litros = 2000 ml

        # Atualizar os valores na mesma linha
        placeholder_hora.metric("Hora", hora)
        placeholder_volume_percent.metric("Volume (%)", f"{volume_percent:.1f}%")
        placeholder_volume_ml.metric("Volume (ml)", volume_ml)

        # Aguardar 1 segundo antes de atualizar novamente
        time.sleep(1)
'''
st.code(code4, language='python')

st.write("Neste trecho, implementamos o loop principal responsável por atualizar os dados em tempo real. Primeiro, carregamos os dados do arquivo CSV utilizando a função `load_csv_data()`. Em seguida, iteramos sobre o DataFrame para extrair os valores de hora e volume. Finalmente, atualizamos os valores nos placeholders e aguardamos 1 segundo antes da próxima atualização.")

