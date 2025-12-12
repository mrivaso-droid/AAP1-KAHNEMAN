import streamlit as st
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# CONFIGURACIÓN Y MODO OSCURO AUTOMÁTICO
# ---------------------------------------------------------
st.set_page_config(
    page_title="Analizador de Decisiones - Kahneman",
    page_icon="🧠",
    layout="centered",
)

dark_mode_css = """
<script>
const observer = new MutationObserver((mutations) => {
    const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
});
observer.observe(document.documentElement, { attributes: true });
</script>

<style>
:root {
    --bg: #ffffff;
    --text: #000000;
    --card: #f0f2f6;
    --border: #4A90E2;
}

[data-theme="dark"] {
    --bg: #121212;
    --text: #f2f2f2;
    --card: #1e1e1e;
    --border: #888;
}

body, .main, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.card {
    background: var(--card) !important;
    color: var(--text) !important;
    border-left: 4px solid var(--border) !important;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}

h1, h2, h3, p, label, div, span {
    color: var(--text) !important;
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# MANIFEST Y SERVICE WORKER (PWA)
# ---------------------------------------------------------
manifest_code = """
<link rel="manifest" href="manifest.json">
<script>
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("service-worker.js")
}
</script>
"""
st.markdown(manifest_code, unsafe_allow_html=True)

# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------
st.title("🧠 Analizador de Decisiones — Modelo de Kahneman")

st.markdown(
"""
Bienvenido al analizador interactivo de decisiones. 
Aquí podrás comparar una **opción segura** vs una **opción riesgosa**, 
evaluar su **valor esperado**, identificar el **cuadrante psicológico** y recibir una **recomendación racional** junto al **sesgo cognitivo probable**.
"""
)

# ---------------------------------------------------------
# ENTRADAS DEL USUARIO
# ---------------------------------------------------------
st.header("📊 Ingreso de Datos")

escenario = st.radio("¿El escenario corresponde a una GANANCIA o a una PÉRDIDA?",
                     ["Ganancia", "Pérdida"])

p = st.slider("Probabilidad del evento riesgoso (0 = imposible, 1 = seguro)", 0.0, 1.0, 0.5, 0.01)

valor_seguro = st.number_input("Valor de la opción segura ($)", min_value=0.0, step=1000.0)

valor_riesgoso = st.number_input("Valor potencial si eliges la opción riesgosa ($)", 
                                 min_value=0.0, step=1000.0)

if st.button("➡ Analizar decisión"):
    # -----------------------------------------------------
    # CÁLCULOS PRINCIPALES
    # -----------------------------------------------------
    VE_riesgo = p * valor_riesgoso
    p_segura = 1 - p
    # El Valor Esperado (VE) de la opción segura es el premio total,
    # ya que se asume que su probabilidad de ocurrir es 1 (segura)
    # Para el modelo, usamos el valor de la opción segura directamente como su VE:
    VE_segura = valor_seguro 

    # -----------------------------------------------------
    # DETERMINAR CUADRANTE PSICOLÓGICO
    # -----------------------------------------------------
    if escenario == "Ganancia":
        if p >= 0.5:
            cuadrante = 1
            sesgo = "Aversión al riesgo moderada"
            descripcion = "Ganancia probable. La mayoría prefiere asegurar."
        else:
            cuadrante = 2
            sesgo = "Búsqueda del riesgo"
            descripcion = "Ganancia improbable. Se sobrevaloran las pequeñas probabilidades."
    else:
        if p >= 0.5:
            cuadrante = 3
            sesgo = "Búsqueda del riesgo"
            descripcion = "Pérdida probable. Las personas arriesgan más para evitar perder."
        else:
            cuadrante = 4
            sesgo = "Aversión al riesgo extrema"
            descripcion = "Pérdida improbable. Se prefiere asegurar incluso pequeñas pérdidas."

    # -----------------------------------------------------
    # RECOMENDACIÓN FINAL
    # -----------------------------------------------------
    if VE_riesgo > VE_segura:
        recomendación = "CONVIENE EL RIESGO"
        color_r = "🟩"
    else:
        recomendación = "CONVIENE LA OPCIÓN SEGURA"
        color_r = "🟥"

    # -----------------------------------------------------
    # RESULTADOS TEXTUALES
    # -----------------------------------------------------
    st.header("📘 Resultados del Análisis")

    st.markdown(f"""
    ### **🧩 Cuadrante psicológico**
    **CUADRANTE {cuadrante} — {descripcion}**

    **Sesgo cognitivo probable:** 👉 *{sesgo}*

    ---

    ### **💵 Valor Esperado**
    - VE opción segura: **${VE_segura:,.0f}**
    - VE opción riesgosa: **${VE_riesgo:,.0f}**

    ---

    ### **🔍 Recomendación Final**
    {color_r} **{recomendación}**
    """)
    
    # -----------------------------------------------------
    # GRÁFICO VALOR ESPERADO VS PROBABILIDAD (CORREGIDO)
    # -----------------------------------------------------
    fig, ax = plt.subplots(figsize=(6,4))

    # Puntos
    ax.scatter(p_segura, VE_segura, color="green", s=120)
    # 🟢 Texto corregido
    ax.text(p_segura, VE_segura, f" Segura (VE: ${VE_segura:,.0f})", fontsize=10) 

    ax.scatter(p, VE_riesgo, color="red", s=120)
    # 🔴 Texto corregido
    ax.text(p, VE_riesgo, f" Riesgo (VE: ${VE_riesgo:,.0f})", fontsize=10)

    # Estética
    ax.set_xlabel("Probabilidad")
    ax.set_ylabel("Valor Esperado")
    ax.set_title("Comparación de Valor Esperado")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)

# FIN DEL SCRIPT