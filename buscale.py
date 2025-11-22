import pandas as pd
import streamlit as st
import sqlite3
import plotly.graph_objects as go
import numpy as np

# --- Configuración de la Base de Datos (SQLite) ---
DATABASE_FILE = "psicologia_data.db"
TABLE_NAME = "palabras_psicologicas"

# --- 1. Inicialización de la Base de Datos ---
def setup_db():
    """
    Crea la tabla y carga datos de ejemplo si no existen.
    Esto hace que la aplicación sea runnable de inmediato.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Crear la tabla si no existe
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                palabra TEXT PRIMARY KEY,
                categoria TEXT
            )
        """)
        
        # Datos de ejemplo para la tabla
        data = [
            ("ansiedad", "Trastorno Emocional"), 
            ("estrés", "Respuesta Fisiológica"), 
            ("autoestima", "Auto-concepto"), 
            ("motivación", "Procesos Cognitivos"), 
            ("depresión", "Trastorno Emocional"), 
            ("empatía", "Habilidad Social"),
            ("atención", "Procesos Cognitivos"), 
            ("memoria", "Procesos Cognitivos"), 
            ("percepción", "Procesos Cognitivos"), 
            ("conducta", "Comportamiento"), 
            ("emoción", "Afectividad"), 
            ("aprendizaje", "Desarrollo"),
            ("terapia", "Intervención"), 
            ("trauma", "Trastorno Psicológico"), 
            ("bienestar", "Salud Mental"), 
            ("personalidad", "Rasgos Estables"), 
            ("autoconcepto", "Auto-concepto"), 
            ("neurociencia", "Biología"),
            ("resiliencia", "Fuerza Personal"), 
            ("trastorno", "Clínico"), 
            ("psicoterapia", "Intervención"),
            ("bipolaridad", "Clínico"),
            ("freud", "Teórico"),
        ]
        
        # Insertar los datos. ON CONFLICT IGNORE evita duplicados al recargar
        cursor.executemany(f"INSERT OR IGNORE INTO {TABLE_NAME} (palabra, categoria) VALUES (?, ?)", data)
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error al configurar la base de datos: {e}")

# Ejecutar la configuración inicial de la DB
setup_db()


# --- 2. Carga de Datos desde la DB (Reemplaza la carga de archivos) ---
@st.cache_data
def load_data_from_db():
    """Carga todos los datos de la base de datos a un DataFrame de Pandas."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        query = f"SELECT palabra, categoria FROM {TABLE_NAME}" 
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error al conectar o cargar datos de la base de datos: {e}")
        # Retorna un DataFrame vacío en caso de error
        return pd.DataFrame({'palabra': [], 'categoria': []})

df_palabras_clave = load_data_from_db()


# --- 3. Lógica de Análisis para el Porcentaje ---
def analyze_psychology_relation(search_term, df):
    """
    Simula el cálculo del porcentaje de relación con la psicología 
    basado en coincidencias en la base de datos.
    """
    search_term = search_term.lower().strip()
    
    # 1. Búsqueda de coincidencia exacta
    exact_match = df[df['palabra'] == search_term]
    
    # 2. Búsqueda de coincidencia de raíz (usando 'startswith' como simplificación)
    root_match = df[df['palabra'].str.startswith(search_term)]

    relation_percentage = 0
    category = "No encontrada o Genérica"
    resultados = pd.DataFrame() # Para mantener la tabla de resultados

    if not exact_match.empty:
        # Coincidencia exacta: Relación muy alta
        relation_percentage = 95
        category = exact_match['categoria'].mode()[0]
        resultados = exact_match
    elif not root_match.empty:
        # Coincidencia de raíz: Relación alta
        relation_percentage = 70
        category = root_match['categoria'].mode()[0]
        resultados = root_match
    else:
        # Sin coincidencia directa: Relación asumida como baja
        relation_percentage = 15
        category = "Relación Mínima/Contextual"
        
    return relation_percentage, category, resultados


# --- Configuración de la aplicación Streamlit ---
st.set_page_config(page_title="Analizador de Palabras Psicológicas", layout="centered", page_icon="🧠")

st.title("🧠 Analizador de Palabras Clave en Psicología")

st.write("""
Esta aplicación **se conecta directamente a tu base de datos** para buscar y analizar 
palabras clave relacionadas con el dominio de la psicología.
""")

# Mensaje de éxito de la DB (Reemplazo del file_uploader)
st.success(f"✅ Conexión exitosa a la Base de Datos. Se cargaron {len(df_palabras_clave)} palabras clave.")

# Formulario de búsqueda
with st.form(key="buscar"):
    query = st.text_input("🔍 Escribe una palabra o raíz para buscar (ej. 'emo', 'estrés', 'terapia')")
    boton = st.form_submit_button("Buscar")

# Si el usuario presiona buscar
if boton and query:
    # 1. Obtener los resultados del análisis
    percentage, category, resultados_df = analyze_psychology_relation(query, df_palabras_clave)

    st.subheader(f"📊 Análisis de Relación Psicológica para: **{query}**")
    
    # --- 4. Desplegar la Gráfica de Porcentaje ---
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Porcentaje de Relación Psicológica"},
        gauge = {'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                 'bar': {'color': "#66bb6a"}, # Barra de color verde
                 'bgcolor': "white",
                 'borderwidth': 2,
                 'bordercolor': "gray",
                 'steps': [
                     {'range': [0, 30], 'color': "red"},
                     {'range': [30, 60], 'color': "yellow"},
                     {'range': [60, 100], 'color': "lightgreen"}],
                 'threshold': {'line': {'color': "darkblue", 'width': 4}, 'thickness': 0.8, 'value': percentage}}
    ))

    # Ajustar el diseño del gráfico para que sea más claro
    fig.update_layout(height=250)
    
    st.plotly_chart(fig, use_container_width=True)

    # 5. Mostrar la Conclusión y la Tabla
    if percentage > 20:
        st.info(f"""
            La palabra **{query}** tiene un **{percentage}% de relación** con la psicología, 
            siendo la categoría más relevante: **{category}**.
        """)
    else:
        st.warning(f"""
            La palabra **{query}** solo tiene un **{percentage}% de relación** con el dominio, 
            sugiriendo una conexión mínima o contextual.
        """)
    
    st.markdown("---")
    