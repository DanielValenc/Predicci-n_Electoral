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
    'amarillo': '#FFD700',
    'azul': '#0047AB',
    'rojo': '#EF3340',
    'neutral': '#808080'
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

    # Estilos y animaciones mejoradas
    st.markdown(
        """
        <style>
        /* Animaciones generales */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Estilos del encabezado */
        .main-header {
            background: linear-gradient(
                90deg, 
                #FFD700 0%, 
                #0047AB 50%, 
                #EF3340 100%
            );
            background-size: 200% 200%;
            animation: gradientFlow 15s ease infinite;
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .main-header:hover {
            transform: translateY(-5px);
        }

        /* Animación para elementos de datos */
        .metric-card {
            animation: fadeIn 0.8s ease-out;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Estilo para el gráfico */
        .plot-container {
            animation: fadeIn 1s ease-out;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .plot-container:hover {
            transform: scale(1.01);
        }

        /* Animación para la sección de análisis */
        .analysis-section {
            animation: slideIn 0.8s ease-out;
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
            margin: 20px 0;
        }

        /* Estilo para botones y controles */
        .stButton>button {
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #0047AB 0%, #003380 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Estilo para el slider */
        .stSlider {
            animation: fadeIn 0.8s ease-out;
            color: white;
        }

        /* Animación para las métricas */
        div[data-testid="stMetric"] {
            animation: fadeIn 0.8s ease-out;
            background: #34495e;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Estilo para el DataFrame */
        .dataframe {
            animation: fadeIn 1s ease-out;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        /* Estilo para mensajes de error */
        .stAlert {
            animation: pulse 2s infinite;
        }

        /* Estilo para el spinner de carga */
        .stSpinner {
            animation: pulse 1s infinite;
        }

        /* Responsive design ajustes */
        @media (max-width: 768px) {
            .main-header {
                padding: 15px;
                margin-bottom: 20px;
            }

            .metric-card {
                padding: 15px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Título principal con clase actualizada
    st.markdown("""
        <div class='main-header'>
            <h1>Análisis Electoral Ecuador 2024-2025🗳️</h1>
            <h3 style='color: white;'>Segunda Vuelta Presidencial</h3>
        </div>
        """, unsafe_allow_html=True)

    # Carga de archivo con estilo mejorado
    uploaded_file = st.file_uploader('📊 Cargar archivo de datos (XLSX)', type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if 'text' not in df.columns:
            st.error("⚠️ El archivo debe contener una columna 'text' con las respuestas de los votantes")
            return

        # Sección de muestreo con animación
        st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
        st.markdown("### 📌 Selección de Muestra")
        sample_size = st.slider(
            "Tamaño de muestra a analizar",
            min_value=1,
            max_value=len(df),
            value=min(10, len(df))
        )
        st.markdown("</div>", unsafe_allow_html=True)

        sample_df = df.sample(n=sample_size)

        # Mostrar muestra con estilo
        st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
        st.markdown("#### 📝 Muestra de Respuestas Ciudadanas")
        st.dataframe(sample_df[['text']], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Análisis de votos y visualización
        df['intencion_voto'] = df['text'].apply(analyze_voting_intention)
        vote_counts = df['intencion_voto'].value_counts()

        # Gráfico con estilo mejorado
        st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
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

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Arial",
            title_font_size=24,
            showlegend=False,
            hovermode='x',
            margin=dict(t=50, l=20, r=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Métricas con animación
        votos_nulos = vote_counts.get('Voto Nulo', 0)
        total_votos = len(df)
        porcentaje_nulos = (votos_nulos / total_votos) * 100

        st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

        # Conclusiones con animación
        st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
        st.markdown("### 📋 Análisis Final")
        ganador = vote_counts.index[0] if not vote_counts.empty else "Datos insuficientes"

        st.markdown(f"""
        #### Resultados del Análisis Electoral:
        - 🏆 Candidato con mayor intención de voto: **{ganador}**
        - 📊 Participación total analizada: **{total_votos:,} respuestas**
        - ❌ Votos nulos/blancos: **{porcentaje_nulos:.1f}%**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        # Sección de consultas con animación
        st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()