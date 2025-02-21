import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
import pygsheets
import os
from dotenv import load_dotenv

# Configuração da página
st.set_page_config(
    page_title="Dashboard Salas do Empreendedor", layout="wide")

# credenciais_json = os.environ.get("API_KEY")
load_dotenv()

api_key =st.secrets["api_key"]
#api_key = os.getenv("api_key")
# API GOOGLE SHEETS
credenciais = pygsheets.authorize(service_account_file=(
    api_key))  # leitura da credencial
paginaplanilha = "https://docs.google.com/spreadsheets/d/1q-gDA5KEcZLds_gnk5eXjjKcF9LbGbK9mhCD4QEZYdk/"  # link da planilha
arquivo = credenciais.open_by_url(paginaplanilha)  # abrindo arquivo pela url
# titulo da aba da planilha, caso tenha mais de uma
aba = arquivo.worksheet_by_title("dashboard")
file = aba.get_all_values()  # pegando todos os dados da aba
# Definindo os nomes das colunas
colunas = [
    "Seq.", "Municípios", "LG Nº", "LG Impl.", "Sala", "Situação",
    "Atendimentos 2024", "Atendimentos 2025", "Endereço",
    "Responsável", "Telefone", "Nome", "CPF", "Telefone AD",
    "E-mail", "Rede Simples"
]

# criando data frame para o pandas poder ler
df = pd.DataFrame(file, columns=colunas)


# Se o arquivo for carregado
if file is not None:

    # Carregar apenas a planilha "dashboard" do df
    # df = pd.read_excel(file, sheet_name="dashboard")

    # Removendo a primeira coluna
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(index=0)

    cidade = st.sidebar.selectbox("Escolha uma cidade:", [
        "Todas as cidades"] + df["Municípios"].unique().tolist())

    if cidade == "Todas as cidades":
        # Título centralizado do dashboard
        st.markdown('<h1 style="text-align: center;">Dashboard Salas do Empreendedor ARJP</h1>',
                    unsafe_allow_html=True)

    elif cidade != "Todas as cidades":
        # Título centralizado do dashboard para uma cidade específica
        st.markdown(
            f'<h1 style="text-align: center;">Dashboard Sala do Empreendedor {cidade}</h1>', unsafe_allow_html=True)

    # criando colunas
    col1, col2 = st.columns(2)
    # Botão de upload na coluna 1
    with col1:

        # mostrar os dados com base na cidade escolhida
        if cidade == "Todas as cidades":
            df_table = pd.DataFrame(df)
            st.dataframe(df_table, hide_index=True)

            # df_filtrado = df
            # df_filtrado  # Se "Todas as cidades" for selecionada, não filtra
        else:
            # Caso contrário, filtra pela cidade selecionada
            # df_filtrado = df[df["Municípios"] == cidade]
            # df_filtrado

            slot1, slot2 = st.columns(2)
            slot3, slot4 = st.columns(2)

            with slot1:
                st.write("")
                # Exemplo: pegar o valor da coluna 'LG Nº' na linha onde 'Municípios' é a cidade escolhida na selectbox
                lg = df.loc[df['Municípios'] == cidade, 'LG Nº'].iloc[0]

                st.markdown(
                    f'<p style="font-size: 30px;"><b><u>Lei Geral Nº:</b></u><br> {lg}</p>',
                    unsafe_allow_html=True
                )
            with slot2:
                st.write("")
                sala = df.loc[df['Municípios'] == cidade, 'Sala'].iloc[0]
                st.markdown(
                    f'<p style="font-size: 30px;"><b><u>Sala Aberta?</b></u><br>{sala}</p>',
                    unsafe_allow_html=True
                )
            with slot3:
                impl = df.loc[df['Municípios'] == cidade, 'LG Impl.'].iloc[0]
                st.markdown(
                    f'<p style="font-size: 30px;"><b><u>Atualizar LG?</b></u><br>{impl}</p>',
                    unsafe_allow_html=True
                )
            with slot4:
                situacao = df.loc[df['Municípios']
                                  == cidade, 'Situação'].iloc[0]
                st.markdown(
                    f'<p style="font-size: 30px;"><b><u>Situação:</b></u><br>{situacao}</p>',
                    unsafe_allow_html=True
                )

    with col2:
        # criando mapa da paraíba e seus municipios
        # lendo arquivo shapefil
        path_shp = r'PB_Municipios_2023.shp'
        paraiba = gpd.read_file(path_shp)

        # Se a cidade selecionada for 'Todas as cidades', vamos filtrar os municípios que queremos destacar
        cidades_destacadas = [
            "Baía da Traição", "Bayeux", "Cabedelo", "Caldas Brandão", "Capim",
            "Cruz do Espírito Santo", "Cuité de Mamanguape", "Curral de Cima",
            "Gurinhém", "Ingá", "Itabaiana", "Itapororoca", "Jacaraú",
            "João Pessoa", "Juripiranga", "Lucena", "Mamanguape", "Marcação",
            "Mataraca", "Mogeiro", "Pedras de Fogo", "Pedro Régis", "Pilar",
            "Riachão do Poço", "Rio Tinto", "Salgado de São Félix", "Santa Rita",
            "São José dos Ramos", "São Miguel de Taipu", "Sobrado"
        ]

        # Seleciona o município ou todos os municípios
        if cidade == "Todas as cidades":
            municipios = paraiba[paraiba['NM_MUN'].isin(cidades_destacadas)]
        else:
            municipios = paraiba[paraiba['NM_MUN'] == cidade]

            # Plotar todos os municípios
        figmap, ax = plt.subplots(figsize=(8, 8))

        # Todos os municípios em cinza
        paraiba.plot(ax=ax, color='lightgrey',
                     edgecolor='black', linewidth=0.5)

        # Plotar os municípios em destaque
        municipios.plot(ax=ax, color='blue', edgecolor='black', linewidth=0.5)

        # Ajustar os limites do gráfico (se necessário)
        minx, miny, maxx, maxy = municipios.total_bounds
        ax.set_xlim(minx - 2, maxx + 0.5)
        ax.set_ylim(miny - 0.5, maxy + 0.5)

        # Exibir o gráfico
        ax.set_axis_off()
        figmap.patch.set_visible(False)
        st.pyplot(figmap)

    # with col2:
     #   slot1, slot2, slot3 = st.columns(3)
#
 #       with slot1:
  #          st.markdown(
   #             f'<p style="font-size: 15px;"><b><u>População em 2022</b></u><br>12560 habitantes</p>',
    #            unsafe_allow_html=True
     #       )

    col3, col4, col5 = st.columns(3)
    # col3, col4 = st.columns(2)

    # GRÁFICO 1 (SALAS ABERTAS E FECHADAS)
    # modificando "sim" e "não" da coluna sala para "abertas" e "fechadas"
    df["Sala"] = df["Sala"].replace({'sim': 'Abertas', 'não': 'Fechadas'})

    # contagem de valores na coluna "Sala"
    sala_counts = df["Sala"].value_counts()

    # Criar o gráfico de pizza para salas abertas e fechadas(ou que não abriram)
    fig = px.pie(
        names=sala_counts.index,
        values=sala_counts.values,
        title="Proporção das salas em todas as cidades",
        color=sala_counts.index,
        color_discrete_map={'Abertas': 'blue', 'Fechadas': 'red '},
        hole=0  # Faz o gráfico de pizza parecer um gráfico de rosquinha
    )
    # Exibe o gráfico na `col3`
    col3.plotly_chart(fig)

    # CRIANDO GRÁFICO DA COLUNA SITUAÇÃO
    # Contagem das ocorrências para situação
    situação_counts = df["Situação"].value_counts()

    # Criar o gráfico de pizza para a quantidade de "situação"
    fig_situação = px.pie(
        names=situação_counts.index,
        values=situação_counts.values,
        title="Situação das Salas em todas as cidades",
        color=situação_counts.index,
        color_discrete_map={'em revoção': 'blue',
                            'Não': 'lightred', 'renovar': 'lightyellow'},
        hole=0.3   # Faz o gráfico de pizza parecer um gráfico de rosquinha
    )

    # Exibe o gráfico na `col4`
    col4.plotly_chart(fig_situação)

    # CRIANDO GRÁFICO DA COLUNA LG impl.
    # Contagem das ocorrências para situação
    LGimpl_counts = df["LG Impl."].value_counts()

    # Criar o gráfico de pizza para a quantidade de "situação"
    fig_LGimpl = px.pie(
        names=LGimpl_counts.index,
        values=LGimpl_counts.values,
        title="Situação da LG implementada",
        color=LGimpl_counts.index,
        color_discrete_map={'atualizar': 'orange',
                            'não': 'red', 'sim': 'green'},
        hole=0.3   # Faz o gráfico de pizza parecer um gráfico de rosquinha
    )

    # Exibe o gráfico na `col5`
    col5.plotly_chart(fig_LGimpl)

    col6, col7, col8 = st.columns(3)

    # criando grafico de barra
    sala_qtd = df['Sala'].value_counts().reset_index()
    sala_qtd.columns = ['Salas', 'Quantidade']

    fig6 = px.bar(
        data_frame=sala_qtd,
        x='Salas',
        y="Quantidade",
        title="Quantidade de salas abertas e fechadas"
    )
    # Configura a posição do texto
    # Texto acima das barras
    fig6.update_traces(text=sala_qtd['Quantidade'], textposition='outside')

    col6.plotly_chart(fig6)

    # criando grafico de barra
    situacao_qtd = df['Situação'].value_counts().reset_index()
    situacao_qtd.columns = ['Situação', 'Quantidade']

    fig7 = px.bar(
        data_frame=situacao_qtd,
        x='Situação',
        y="Quantidade",
        title="Quantidade de salas em cada situação"
    )
    # Configura a posição do texto
    # Texto acima das barras
    fig7.update_traces(
        text=situacao_qtd['Quantidade'], textposition='outside')

    col7.plotly_chart(fig7)

    # criando grafico de barra
    LGimpl_qtd = df['LG Impl.'].value_counts().reset_index()
    LGimpl_qtd.columns = ['LG implementada', 'Quantidade']

    fig8 = px.bar(
        data_frame=LGimpl_qtd,
        x='LG implementada',
        y="Quantidade",
        title="LG implementada"
    )
    # Configura a posição do texto
    # Texto acima das barras
    fig8.update_traces(
        text=LGimpl_qtd['Quantidade'], textposition='outside')

    col8.plotly_chart(fig8)

else:
    # Caso o arquivo ainda não tenha sido carregado
    st.write("Nenhum arquivo carregado ainda.")
