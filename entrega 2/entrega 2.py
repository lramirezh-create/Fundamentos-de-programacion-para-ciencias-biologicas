# ANÁLISIS EPIDEMIOLÓGICO DEL DENGUE 
# ===========================================================

# Importar librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuración del estilo de las graficas.
plt.style.use('default')
sns.set_palette("husl")
print(" ANÁLISIS DESCRIPTIVO: PATRONES EPIDEMIOLÓGICOS DEL DENGUE")

# 1. CARGA Y PREPARACIÓN DE DATOS
# ===============================
print("\n1.  CARGANDO DATOS...")
df = pd.read_csv('C:/Users/BGinvestments/Documents/Luis/UN/2025-2/programacion/parciales/entrega 2/dengue grabe/13._Dengue,_Dengue_grave_y_mortalidad_por_dengue_municipio_de_Bucaramanga_20251028.csv ', encoding='utf-8', low_memory=False)

# Limpieza básica y preparación de las variables epidemiologicas importantes.
#conversion de las fechas para hacer el analisis temporal
df['fec_not'] = pd.to_datetime(df['fec_not'], errors='coerce')
#conversion de semana epidemiologica a numerica
df['semana'] = pd.to_numeric(df['semana'], errors='coerce')
#Extracion de edad numerica desde variable categorica grupo_etario.
df['edad_numerica'] = df['grupo_etario'].str.extract('(\d+)').astype(float)

print(f"Dataset cargado: {df.shape[0]} casos de dengue")

# 2. GRÁFICO 1: BOXPLOT (Numérico vs Categórico)
# ==============================================
print("\n2.GRÁFICO 1: Boxplot - Distribución de edad por tipo de dengue")
plt.figure(figsize=(10, 6))


# Filtrar y preparar datos para analisis de distribucion etaria
#se excluyen valores nulos y se filtran solo registros de dengue
datos_boxplot = df[df['clasfinal'].notna() & df['edad_numerica'].notna()]
datos_boxplot = datos_boxplot[datos_boxplot['clasfinal'].str.contains('DENGUE', na=False)]

# Crear boxplot para comparar distribucion de edad entre categorias de dengue
# Boxplot seleccionado porque muestra percentiles, mediana y outliers de manera efectiva.
sns.boxplot(data=datos_boxplot, x='clasfinal', y='edad_numerica')
plt.title('Distribución de Edad por Tipo de Dengue', fontsize=14, fontweight='bold')
plt.xlabel('Clasificación del Dengue')
plt.ylabel('Edad (años)')
plt.xticks(rotation=45)
plt.tight_layout()

# Justificación: El boxplot muestra la distribución, mediana y outliers de edad para cada categoría de dengue
# permitiendo identificar diferencias en el perfil etario entre tipos de la enfermedad.
print("Boxplot generado: Compara variable numérica (edad) con categórica (tipo de dengue)")

# 3. GRÁFICO 2: COUNTPLOT (Categórico vs Categórico)
# ==================================================
print("\n3.GRÁFICO 2: Countplot - Distribución por sexo y clasificación")
plt.figure(figsize=(12, 6))

# Preparar datos para analisis de distribucion por sexo
#se filtran solo valores validos de sexo (M,F) y clasificaciones no nulas.
datos_count = df[df['sexo_'].isin(['M', 'F']) & df['clasfinal'].notna()]
datos_count = datos_count[datos_count['clasfinal'].str.contains('DENGUE', na=False)]

# Crear countplot para visualizar frecuencia cruzada de dos variables categoricas
#countplot ideal para compara frecuencias entre categorias con desglose por subcategorias.
sns.countplot(data=datos_count, x='clasfinal', hue='sexo_')
plt.title('Distribución de Casos por Sexo y Tipo de Dengue', fontsize=14, fontweight='bold')
plt.xlabel('Clasificación del Dengue')
plt.ylabel('Número de Casos')
plt.legend(title='Sexo', labels=['Masculino', 'Femenino'])
plt.xticks(rotation=45)
plt.tight_layout()

# Justificación: El countplot permite visualizar la frecuencia de casos cruzando dos variables categóricas
# mostrando diferencias en la distribución por sexo para cada tipo de dengue.
print("Countplot generado: Compara dos variables categóricas (sexo y tipo de dengue)")

# 4. GRÁFICO 3: LINEPLOT (Numérico vs Numérico)
# =============================================
print("\n4. GRÁFICO 3: Lineplot - Evolución temporal de casos")
plt.figure(figsize=(12, 6))

# Preparar datos temporales
#agrupar por semana epidemiolgocia y contar casos
casos_semana = df.groupby('semana').size().reset_index(name='casos')
casos_semana = casos_semana[casos_semana['semana'] <= 52]  # Filtrar semanas válidas

# Crear lineplot para mostrar tendencia temporal de casos
#lineplot seleccionado por su efectividad para visulizar serie temporales
sns.lineplot(data=casos_semana, x='semana', y='casos', marker='o')
plt.title('Evolución Semanal de Casos de Dengue', fontsize=14, fontweight='bold')
plt.xlabel('Semana Epidemiológica')
plt.ylabel('Número de Casos')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Justificación: El lineplot muestra la tendencia temporal de casos, ideal para variables numéricas continuas
# como el tiempo (semanas) vs frecuencia de casos.
print("Lineplot generado: Compara dos variables numéricas (semana vs número de casos)")

# 5. GRÁFICO 4: BARPLOT (Numérico vs Categórico)
# ==============================================
print("\n5. GRÁFICO 4: Barplot - Casos por grupo etario")
plt.figure(figsize=(10, 6))

# Preparar datos por grupo etario
#luego cuenta casos por cada grupo etario
casos_edad = df['grupo_etario'].value_counts().reset_index()
casos_edad.columns = ['grupo_etario', 'casos']

# Ordenar por edad
orden_edad = ['MENOR DE 1', '1 A 4', '5 A 9', '10 A 14', '15 A 19',
              '20 A 29', '30 A 39', '40 A 49', '50 A 59', '60 A 69', '70 Y MAS']
#convierte de forma categorica ordenando para mantener secuencia logica en la grafica.
casos_edad['grupo_etario'] = pd.Categorical(casos_edad['grupo_etario'], categories=orden_edad, ordered=True)
casos_edad = casos_edad.sort_values('grupo_etario')

# Crear barplot
sns.barplot(data=casos_edad, x='grupo_etario', y='casos')
plt.title('Distribución de Casos por Grupo Etario', fontsize=14, fontweight='bold')
plt.xlabel('Grupo Etario')
plt.ylabel('Número de Casos')
plt.xticks(rotation=45)
plt.tight_layout()

# Justificación: El barplot es ideal para comparar magnitudes (casos) entre categorías (grupos etarios)
# mostrando claramente qué grupos de edad son más afectados.
print("Barplot generado: Compara variable numérica (casos) con categórica (grupo etario)")

# 6. GRÁFICO 5: HEATMAP (Numérico vs Categórico)
# ==============================================
print("\n6. GRÁFICO 5: Heatmap - Casos por comuna y mes")
plt.figure(figsize=(12, 8))

# Preparar datos para heatmap
df['mes'] = df['fec_not'].dt.month
top_comunas = df['COMUNA shp'].value_counts().head(10).index  # Top 10 comunas

datos_heatmap = df[df['COMUNA shp'].isin(top_comunas)]
heatmap_data = datos_heatmap.groupby(['COMUNA shp', 'mes']).size().unstack(fill_value=0)

# Crear heatmap
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5)
plt.title('Casos de Dengue por Comuna y Mes (Top 10 Comunas)', fontsize=14, fontweight='bold')
plt.xlabel('Mes')
plt.ylabel('Comuna')
plt.tight_layout()

# Justificación: El heatmap permite visualizar patrones espaciotemporales, mostrando intensidad de casos
# por comuna (categórica) a lo largo de los meses (numérico transformado a categórico para visualización).
print(" Heatmap generado: Compara datos numéricos (casos) organizados por dos dimensiones categóricas")

# 7. RESUMEN Y EXPORTACIÓN
# ========================


# Mostrar todos los gráficos

plt.show()
