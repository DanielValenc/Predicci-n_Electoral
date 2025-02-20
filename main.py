import streamlit as st
import pandas as pd
import numpy as np


def generate_random_sample(data, sample_size):
    """Genera una muestra aleatoria de los datos."""
    return data.sample(n=sample_size, random_state=42)


def main():
    st.title("Predicción Electoral 2025")

    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Vista previa de los datos:")
        st.write(df.head())

        if 'text' in df.columns:
            # Control para definir el tamaño de la muestra
            sample_size = st.slider("Selecciona el tamaño de la muestra", min_value=10, max_value=1000, value=50)

            if st.button("Generar Muestra"):
                sample = generate_random_sample(df, sample_size)

                # Contar los votos en la muestra
                vote_counts = sample['text'].value_counts()

                # Mostrar resultados de la muestra
                st.write("Resultados de la muestra:")
                st.write(vote_counts)

                # Gráfico de barras en cuanto a los votos de Luisa, Noboa y Nulo en la muestra
                st.bar_chart(vote_counts)

            # Contar los votos en todo el conjunto de datos
            total_vote_counts = df['text'].value_counts()

            # Mostrar resumen de votos totales
            st.write("Resumen general de los votos:")
            st.bar_chart(total_vote_counts)

            # Mostrar los votos específicos de Noboa, Luisa y Nulo
            noboa_votes = total_vote_counts.get("Noboa", 0)
            luisa_votes = total_vote_counts.get("Luisa", 0)
            nulo_votes = total_vote_counts.get("Nulo", 0)

            st.write(f"Votos Totales -> Noboa: {noboa_votes}, Luisa: {luisa_votes}, Nulo: {nulo_votes}")
        else:
            st.error("El archivo debe contener una columna llamada 'text' con las opciones: Noboa, Luisa, Nulo.")


if __name__ == "__main__":
    main()