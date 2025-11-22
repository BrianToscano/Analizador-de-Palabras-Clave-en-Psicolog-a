# logica
🧠 Analizador de Palabras Clave en Psicología

Descripción del Proyecto

Esta aplicación web, construida con Streamlit y Python, permite a los usuarios buscar y analizar la relevancia psicológica de una palabra o raíz (ej., 'emo', 'estrés', 'terapia').



⚙️ Características

Conexión a Base de Datos: Los datos se cargan automáticamente desde una base de datos SQLite interna (psicologia_data.db).

Análisis Simulado: Calcula un porcentaje de relación basado en la coincidencia exacta o de raíz con las palabras clave de la base de datos.

Visualización: Muestra el resultado del análisis en un gráfico de indicador interactivo (Plotly).

Diseño Web: Interfaz amigable desarrollada con Streamlit.

🚀 Cómo Ejecutar la Aplicación

1. Requisitos Previos

Asegúrate de tener Python instalado (versión 3.8 o superior).

2. Instalación de Dependencias

Instala las librerías necesarias utilizando el archivo requirements.txt:

pip install -r requirements.txt


3. Ejecución

Ejecuta el script principal de Streamlit desde tu terminal:

streamlit run Buscale.py


La aplicación se abrirá automáticamente en tu navegador predeterminado (normalmente en http://localhost:8501).

📁 Estructura del Proyecto

Buscale.py: Contiene toda la lógica de la aplicación Streamlit, la conexión a SQLite, la lógica de análisis y la visualización de los gráficos.

requirements.txt: Lista las librerías necesarias para ejecutar la aplicación (Streamlit, Pandas, Plotly, NumPy).

psicologia_data.db: El archivo de base de datos SQLite que se crea automáticamente al ejecutar Buscale.py por primera vez si no existe.

🛠️ Notas sobre la Base de Datos

La aplicación utiliza SQLite y crea un archivo llamado psicologia_data.db en el mismo directorio.

La función setup_db() inicializa la tabla palabras_psicologicas y carga datos de ejemplo si la tabla está vacía.

Si deseas usar una base de datos diferente (PostgreSQL, MySQL, etc.), deberás modificar las funciones setup_db() y load_data_from_db() en Buscale.py para usar el conector de base de datos apropiado (como psycopg2 o mysql-connector-python) y actualizar el archivo requirements.txt.