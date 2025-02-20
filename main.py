import os
import streamlit as st
import pandas as pd
import random
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del cliente de Groq
qclient = Groq()

# Colores de la bandera ecuatoriana
COLORS = {
    'amarillo': '#FFD700',  # Amarillo de la bandera
    'azul': '#0047AB',  # Azul de la bandera
    'rojo': '#EF3340',  # Rojo de la bandera
    'neutral': '#808080'  # Gris para votos nulos
}


def analyze_voting_intention(text):
    """Analiza el texto para determinar la intención de voto en el contexto ecuatoriano"""
    text = str(text).lower()
    if 'noboa' in text or 'daniel' in text:
        return 'Voto Noboa'
    elif 'luisa' in text or 'gonzález' in text or 'gonzalez' in text:
        return 'Voto González'
    else:
        return 'Voto Nulo'


def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Elecciones Ecuador 2024",
        page_icon="🇪🇨",
        layout="wide"
    )

    # Encabezado con colores ecuatorianos estilos de la pagina
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(90deg, #FFD700 33%, #0047AB 33% 66%, #EF3340 66%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Título principal
    st.markdown("""
        <div class='main-header'>
            <h1>Análisis Electoral Ecuador 2024 🗳️</h1>
            <h3 style='color: white;'>Segunda Vuelta Presidencial</h3>
        </div>
        """, unsafe_allow_html=True)

    # Carga de archivo
    uploaded_file = st.file_uploader('📊 Cargar archivo de datos (XLSX)', type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if 'text' not in df.columns:
            st.error("⚠️ El archivo debe contener una columna 'text' con las respuestas de los votantes")
            return

        # Sección de muestreo
        st.markdown("### 📌 Selección de Muestra")
        sample_size = st.slider(
            "Tamaño de muestra a analizar",
            min_value=1,
            max_value=len(df),
            value=min(10, len(df))
        )

        sample_df = df.sample(n=sample_size)

        # Mostrar muestra con estilo
        st.markdown("#### 📝 Muestra de Respuestas Ciudadanas")
        st.dataframe(sample_df[['text']], use_container_width=True)

        # Análisis de votos
        df['intencion_voto'] = df['text'].apply(analyze_voting_intention)
        vote_counts = df['intencion_voto'].value_counts()

        # Visualización con colores ecuatorianos
        fig = px.bar(
            x=vote_counts.index,
            y=vote_counts.values,
            title="📊 Tendencia Electoral Ecuador 2024",
            labels={'x': 'Candidato', 'y': 'Número de Menciones'},
            color=vote_counts.index,
            color_discrete_map={
                'Voto Noboa': COLORS['amarillo'],
                'Voto González': COLORS['azul'],
                'Voto Nulo': COLORS['neutral']
            }
        )

        # Personalizar gráfico
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Arial",
            title_font_size=24
        )
        st.plotly_chart(fig, use_container_width=True)

        # Métricas electorales
        votos_nulos = vote_counts.get('Voto Nulo', 0)
        total_votos = len(df)
        porcentaje_nulos = (votos_nulos / total_votos) * 100

        st.markdown("### 📈 Resultados del Análisis")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🗳️ Total de Respuestas",
                f"{total_votos:,}",
                delta="Muestra Nacional"
            )
        with col2:
            st.metric(
                "❌ Votos Nulos/Blancos",
                f"{votos_nulos:,}",
                delta=f"{porcentaje_nulos:.1f}% del total"
            )
        with col3:
            votos_validos = total_votos - votos_nulos
            st.metric(
                "✅ Votos Válidos",
                f"{votos_validos:,}",
                delta=f"{(votos_validos / total_votos * 100):.1f}% del total"
            )

        # Conclusiones
        st.markdown("### 📋 Análisis Final")
        ganador = vote_counts.index[0] if not vote_counts.empty else "Datos insuficientes"

        st.markdown(f"""
        #### Resultados del Análisis Electoral:
        - 🏆 Candidato con mayor intención de voto: **{ganador}**
        - 📊 Participación total analizada: **{total_votos:,} respuestas**
        - ❌ Votos nulos/blancos: **{porcentaje_nulos:.1f}%**
        """)

        # Sección de consultas
        st.markdown("### 💬 Consultas Electorales")
        st.markdown("_Realiza preguntas sobre los resultados del análisis electoral_")

        user_question = st.text_input("🤔 ¿Qué deseas saber sobre los resultados?")

        if user_question:
            with st.spinner("⏳ Analizando resultados..."):
                data_summary = f"""
                Resumen Electoral Ecuador 2024:
                - Total de respuestas: {total_votos:,}
                - Distribución de votos:
                {vote_counts.to_string()}
                - Porcentaje votos nulos: {porcentaje_nulos:.1f}%
                """

                response = qclient.chat.completions.create(
                    messages=[
                        {"role": "system",
                         "content": "Eres un analista experto en elecciones ecuatorianas 2024. Responde preguntas sobre la segunda vuelta presidencial basándote en los datos proporcionados."},
                        {"role": "user",
                         "content": f"Datos electorales:\n{data_summary}\n\nPregunta: {user_question}"},
                    ],
                    model="llama3-8B-8192",
                    stream=False
                )

                st.markdown("#### 📌 Respuesta del Analista:")
                st.write(response.choices[0].message.content)


if __name__ == "__main__":
    main()