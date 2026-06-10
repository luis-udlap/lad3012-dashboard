"""
Dashboard Superstore — Plantilla LAD3012 D09
============================================
Solo tienes que cambiar TU_NOMBRE y TU_ID antes de subir.
El INSIGHT lo escribes DESPUES de explorar tu dashboard publicado.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIGURACION DE PAGINA
# ============================================================
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="🏪",
    layout="wide"
)

# ============================================================
# PASO 1 — CAMBIA ESTAS DOS LINEAS ANTES DE SUBIR A GITHUB
# ============================================================
TU_NOMBRE = "Luis Barragan Ortiz"
TU_ID     = "178061"

# ============================================================
# PASO 2 — DEJA ESTO COMO ESTA. NO LO CAMBIES TODAVIA.
# Lo llenaras DESPUES de:
#    a) Subir el dashboard
#    b) Abrir tu URL .streamlit.app
#    c) Jugar con los filtros y observar los KPIs y graficos
#    d) Sacar UNA conclusion de negocio en TUS palabras
# Despues vuelves a GitHub, editas esta linea, y haces commit.
# Streamlit Cloud actualiza tu dashboard solo en 30 segundos.
# ============================================================
TU_INSIGHT = """
1. Descubri que la categoria Furniture genero ventas por $579,900, pero tuvo una perdida de $34,742 y un margen negativo de -6.0%.
Recomiendo revisar y limitar los descuentos o costos de envio en Furniture para dejar de perder dinero y acercar el margen al benchmark de 12%.

2. Descubri que Technology vendio $547,025 y genero $51,593 de ganancia, siendo la categoria con mejor rentabilidad del dashboard con un margen de 9.4%.
Recomiendo impulsar mas los productos de Technology con campanas y prioridad comercial para aumentar la ganancia total sin depender solo del volumen de ventas.

3. Descubri que Office Supplies vendio aproximadamente $649,568, mas que Technology, pero genero solo $38,155 de ganancia, menos que los $51,593 de Technology.
Recomiendo revisar precios y descuentos en Office Supplies para mejorar su margen y convertir su alto volumen de ventas en mayor utilidad.

4. Descubri que el negocio completo vendio $1,776,494, pero solo genero $55,006 de ganancia, dejando un margen general de apenas 3.1%, muy por debajo del benchmark de 12%.
Recomiendo priorizar las categorias mas rentables y corregir las perdidas de Furniture para elevar el margen general del negocio.
"""


# ============================================================
# CARGAR DATOS (con cache para velocidad)
# ============================================================
@st.cache_data
def cargar_datos():
    df = pd.read_csv("superstore.csv", encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"]  = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

df = cargar_datos()

# ============================================================
# TITULO Y AUTOR
# ============================================================
st.title("🏪 Superstore — Dashboard Ejecutivo")
st.caption(f"Por **{TU_NOMBRE}** · ID {TU_ID} · LAD3012 · UDLAP Verano I 2026")
st.markdown("---")

# ============================================================
# FILTROS (sidebar)
# ============================================================
st.sidebar.header("🔎 Filtros")
regiones = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)
categorias = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)
anios = st.sidebar.multiselect(
    "Anio",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

# Aplicar filtros
df_f = df[
    df["Region"].isin(regiones) &
    df["Category"].isin(categorias) &
    df["Year"].isin(anios)
]

if len(df_f) == 0:
    st.warning("No hay datos con esos filtros. Selecciona al menos una opcion en cada filtro.")
    st.stop()

# ============================================================
# KPIs (3 metricas grandes)
# ============================================================
col1, col2, col3 = st.columns(3)
col1.metric(
    "Ventas totales",
    f"${df_f['Sales'].sum():,.0f}",
    help="Suma de Sales con los filtros aplicados"
)
col2.metric(
    "Ganancia total",
    f"${df_f['Profit'].sum():,.0f}"
)
margen = 100 * df_f["Profit"].sum() / df_f["Sales"].sum() if df_f["Sales"].sum() else 0
col3.metric(
    "Margen %",
    f"{margen:.1f}%",
    delta=f"{margen - 12:.1f} pp vs benchmark 12%"
)

st.markdown("---")

# ============================================================
# GRAFICOS (2 lado a lado)
# ============================================================
g1, g2 = st.columns(2)

with g1:
    st.subheader("Ventas por categoria")
    datos = df_f.groupby("Category")["Sales"].sum().reset_index()
    fig1 = px.bar(
        datos, x="Category", y="Sales",
        color="Category",
        color_discrete_sequence=["#1E2761", "#F96167", "#21A179"]
    )
    fig1.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig1, use_container_width=True)

with g2:
    st.subheader("Ventas mensuales")
    mensual = df_f.groupby("Month")["Sales"].sum().reset_index()
    fig2 = px.line(mensual, x="Month", y="Sales", markers=True)
    fig2.update_traces(line_color="#1E2761")
    fig2.update_layout(height=380)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# TABLA: top 10 ordenes
# ============================================================
st.subheader("Top 10 ordenes por venta")
top10 = (
    df_f.sort_values("Sales", ascending=False)
        .head(10)
        [["Order ID", "Order Date", "Category", "Region", "Sales", "Profit"]]
)
st.dataframe(top10, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================
# PREGUNTAS GUIA PARA INVESTIGAR (panel desplegable)
# Usalas como inspiracion para escribir tu insight.
# Tu insight personal sera mas valioso que solo responder estas.
# ============================================================
with st.expander("🔍 Preguntas guia para encontrar tu insight"):
    st.markdown("""
**Juega con los filtros del sidebar mientras te haces estas preguntas:**

1. **Region menos rentable.** Deja solo una region a la vez en el filtro. 
¿Cual tiene el margen mas bajo? ¿Por que crees que sea?


2. **Categoria problema.** ¿Hay alguna categoria cuyo margen sea sospechosamente bajo
incluso cuando todas las regiones estan activas? ¿Que decision tomarias como gerente?

3. **Patron temporal.** En el grafico de "Ventas mensuales", ¿hay meses donde claramente
vendemos mas o menos? ¿Que implicaria eso para inventario, contratacion o promociones?

4. **Reto extra.** Si fueras CEO y tuvieras 10 segundos para tomar UNA decision basada
en este dashboard, ¿que decision tomarias y por que?

---

**Tu insight ideal:**
una frase con TU hallazgo + una frase con TU recomendacion.

Ejemplo de la estructura (no copies el contenido, escribe el tuyo):
*"Descubri que [HALLAZGO con un dato concreto]. Recomiendo
[ACCION concreta] para [RESULTADO esperado]."*
    """)

# ============================================================
# INSIGHT DE NEGOCIO
# ============================================================
st.subheader("💡 Insight de negocio")
st.info(TU_INSIGHT)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Dashboard preparado con pandas + plotly + Streamlit · LAD3012 D09")
