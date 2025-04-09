import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# @st.cache_data
# def load_data(csv_path):
#     df = pd.read_csv(csv_path, delimiter=',', encoding='iso-8859-1')
#     return df

# csv_id = "1KaISva3CENPIY7hdxRQPAkj7FoquVzLM"  # substitua pelo seu ID real
# csv_url = f"https://drive.google.com/uc?id={csv_id}"

# # Caminho local para salvar temporariamente
# output = "dados.csv"

# # Faz o download direto ignorando a tela de verificação de vírus
# gdown.download(csv_url, output, quiet=False)

# df = load_data(csv_url)


# csv_url = f'https://drive.google.com/file/d/1KaISva3CENPIY7hdxRQPAkj7FoquVzLM/view?usp=sharing'

# df = load_data('Cad_BEC_top10_corrigido.csv')
df = pd.read_parquet("Cad_BEC_compactado_brotli.parquet")

col1, col2 = st.columns([1, 2])  # Coluna esquerda menor, direita maior

with col1:
    st.title("Consulta de Itens")
    # Campo CODBEC
    cod_bec_input = st.text_input("Digite o CODBEC para pesquisa:", "")

    # Já definimos um text_area desativado (disabled=True).
    # Inicia vazio e preenchemos só depois de clicar em Pesquisar.
    descricao_item = ""

    # Botão de pesquisa
    if st.button("Pesquisar"):
        try:
            # Tentar converter input para int (caso seja numérico)
            cod_bec_int = int(cod_bec_input)
        except ValueError:
            st.warning("Digite um valor numérico para CODBEC.")
            st.stop()

        filtered_df = df[df['CODBEC'] == cod_bec_int]
        if filtered_df.empty:
            st.warning("Nenhuma linha encontrada para esse CODBEC.")
        else:
            # Pega a 1ª linha achada
            row = filtered_df.iloc[0]
            # Passa o descritivo das CARACTERISTICAS para a variável
            descricao_item = row["CARACTERISTICAS"]

            # Monta tabela (Cód GOV, Descritivo)
            table_data = []
            for n in range(1, 11):
                matched_id_col = f"Matched_ID_{n}"
                matched_desc_col = f"Matched_Description_{n}"

                if pd.notna(row[matched_id_col]):
                    table_data.append([
                        row[matched_id_col],
                        row[matched_desc_col]
                    ])
                else:
                    table_data.append(["", ""])

            global_result_df = pd.DataFrame(table_data, columns=["Cód GOV", "Descritivo"])

            # Exibe a tabela na coluna da direita
            with col2:
                st.title("Itens correspondentes")

                # 1) Resetar o índice e descartar a coluna antiga
                global_result_df = global_result_df.reset_index(drop=True)

                # 3) Formatar a coluna "Descritivo" para quebrar linhas e ter altura maior
                df_styled = (
                    global_result_df.style
                    .set_properties(
                        subset=['Descritivo'],
                        **{
                            'white-space': 'pre-wrap',
                            'word-wrap': 'break-word',
                            'overflow-wrap': 'break-word',
                            'line-height': '1.5',
                        }
                    )
                )

                # 4) Exibir a versão estilizada
                st.dataframe(df_styled, use_container_width=True, hide_index=True)
              
    else:
        st.info("Digite o CODBEC e clique em 'Pesquisar' para visualizar os itens.")

    # Aqui exibimos o text_area final com o descritivo,
    # já que se não foi encontrado nada ele fica vazio.
    st.text_area("Descrição Item", value=descricao_item, disabled=True, height=200)
