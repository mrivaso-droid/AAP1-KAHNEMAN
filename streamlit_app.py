import streamlit as st
import matplotlib.pyplot as plt

# -------------------------
# Sesgo cognitivo Kahneman
# -------------------------
def sesgo_kahneman(escenario, p):
    if escenario == "Ganancia":
        if p >= 0.5:
            return (
                "CUADRANTE 1 — GANANCIA PROBABLE",
                "Aversión al riesgo.\nSe prefiere asegurar la ganancia."
            )
        else:
            return (
                "CUADRANTE 2 — GANANCIA IMPROBABLE",
                "Búsqueda del riesgo.\nSe sobrevaloran pequeñas probabilidades."
            )
    else:
        if p >= 0.5:
            return (
                "CUADRANTE 3 — PÉRDIDA PROBABLE",
                "Búsqueda del riesgo.\nSe arriesga para evitar una pérdida segura."
            )
        else:
            return (
                "CUADRANTE 4 — PÉRDIDA IMPROBABLE",
                "Aversión al riesgo.\nSe paga demasiado por eliminar riesgos pequeños."
            )

# -------------------------
# Configuración Streamlit
# -------------------------
st.set_page_config(
    page_title="Analizador de Decisiones",
    layout="centered"
)

st.title("🧠 Analizador de Decisiones")
st.caption("Modelo de Valor Esperado + Sesgos Cognitivos (Kahneman)")

st.markdown("""
Este analizador compara una **opción segura** y una **opción riesgosa**
usando **valor esperado**, permitiendo elegir el modelo de probabilidad.
""")

# -------------------------
# Entradas del usuario
# -------------------------
st.header("1️⃣ Contexto de la decisión")

escenario = st.selectbox(
    "Tipo de escenario",
    ["Ganancia", "Pérdida"]
)

p = st.slider(
    "Probabilidad del evento riesgoso (p)",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.01
)

modelo = st.radio(
    "Modelo de comparación",
    [
        "Modelo A — Opción segura con probabilidad (1 − p)",
        "Modelo B — Opción segura con probabilidad 1"
    ]
)

st.header("2️⃣ Valores de las opciones")

valor_seguro = st.number_input(
    "Valor opción segura ($)",
    step=1,
    format="%d"
)

valor_riesgo = st.number_input(
    "Valor opción riesgosa ($)",
    step=1,
    format="%d"
)

# -------------------------
# Botón de análisis
# -------------------------
if st.button("📊 Analizar decisión"):

    # Probabilidades
    prob_riesgo = p
    if modelo.startswith("Modelo A"):
        prob_segura = 1 - p
        modelo_texto = "Modelo A: Probabilidades complementarias"
    else:
        prob_segura = 1
        modelo_texto = "Modelo B: Opción segura cierta"

    # Valores esperados
    VE_segura = prob_segura * valor_seguro
    VE_riesgo = prob_riesgo * valor_riesgo

    # Recomendación
    if VE_segura > VE_riesgo:
        recomendacion = "CONVIENE LA OPCIÓN SEGURA"
    elif VE_riesgo > VE_segura:
        recomendacion = "CONVIENE TOMAR EL RIESGO"
    else:
        recomendacion = "AMBAS OPCIONES SON EQUIVALENTES"

    # Sesgo cognitivo
    cuadrante, sesgo_texto = sesgo_kahneman(escenario, p)

    # -------------------------
    # Resultados numéricos
    # -------------------------
    st.header("3️⃣ Resultados")

    st.markdown(f"**{modelo_texto}**")

    col1, col2 = st.columns(2)
    col1.metric("Probabilidad opción segura", f"{prob_segura:.2f}")
    col2.metric("Probabilidad opción riesgosa", f"{prob_riesgo:.2f}")

    col1.metric("Valor esperado opción segura", f"${VE_segura:,.0f}")
    col2.metric("Valor esperado opción riesgosa", f"${VE_riesgo:,.0f}")

    # -------------------------
    # Sesgo cognitivo
    # -------------------------
    st.subheader("🧠 Sesgo cognitivo posible (Kahneman)")
    st.markdown(f"**{cuadrante}**")
    st.write(sesgo_texto)

    # -------------------------
    # Recomendación final
    # -------------------------
    st.subheader("✅ Recomendación final")
    st.success(f"📌 {recomendacion}")

    # -------------------------
    # Gráfico
    # -------------------------
    st.subheader("📈 Visualización — Valor Esperado vs Probabilidad")

    fig, ax = plt.subplots(figsize=(8, 5))

    if prob_segura >= prob_riesgo:
        color_segura = "green"
        color_riesgo = "red"
    else:
        color_segura = "red"
        color_riesgo = "green"

    ax.scatter(prob_segura, VE_segura, s=300, c=color_segura, edgecolors="black")
    ax.scatter(prob_riesgo, VE_riesgo, s=300, c=color_riesgo, edgecolors="black")

    ax.text(prob_segura, VE_segura, "S", ha="center", va="center", fontsize=14, weight="bold")
    ax.text(prob_riesgo, VE_riesgo, "R", ha="center", va="center", fontsize=14, weight="bold")

    ax.text(prob_segura + 0.02, VE_segura, f"${VE_segura:,.0f}", fontsize=11)
    ax.text(prob_riesgo + 0.02, VE_riesgo, f"${VE_riesgo:,.0f}", fontsize=11)

    ax.set_xlabel("Probabilidad")
    ax.set_ylabel("Valor Esperado")
    ax.set_xlim(-0.05, 1.05)
    ax.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)
