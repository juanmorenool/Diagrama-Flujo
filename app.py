import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(
    page_title="Framework IRRBB — Flujo del Modelo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS para ocultar el menú de Streamlit y el footer ──
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.block-container {padding-top: 1rem; padding-bottom: 0rem;}
</style>
""", unsafe_allow_html=True)

# ── Barra superior con controles mínimos ──
col_title, col_controls = st.columns([4, 1])
with col_title:
    st.markdown("## 📊 Framework Interbank — IRRBB · Tarjetas de crédito")
    st.caption("Flujo del modelo: segmentación → utilización → amortización → ∆EVE")
with col_controls:
    st.markdown("<br>", unsafe_allow_html=True)
    # Botón para abrir en pantalla completa (nueva pestaña)
    with open("diagrama.html", "r", encoding="utf-8") as f:
        html_b64 = base64.b64encode(f.read().encode()).decode()
    st.link_button(
        label="⛶ Abrir pantalla completa",
        url=f"data:text/html;base64,{html_b64}",
        use_container_width=True
    )

# ── Render del diagrama ──
with open("diagrama.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=950, scrolling=False)
