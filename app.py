
import streamlit as st
 
ARCHIVO_ESTADO = "estado.csv"
 
VALORES_INICIALES = {
    "saldo": 500000,
    "total_consignado": 0,
    "total_retirado": 0,
    "num_consignaciones": 0,
    "num_retiros": 0,
    "meta_ahorro": 0,
}
 
 
# ----------------------------- Persistencia -----------------------------
 
def cargar_estado():
    # Modo "a": crea el archivo si no existe, no borra nada si ya existe.
    with open(ARCHIVO_ESTADO, "a") as f:
        pass
 
    estado = {}
    with open(ARCHIVO_ESTADO, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea == "":
                continue
            partes = linea.split(",")
            # Si la línea no tiene el formato clave,valor, la ignoramos
            # en vez de dejar que el programa se caiga.
            if len(partes) < 2:
                continue
            clave = partes[0]
            valor = int(partes[1])
            estado[clave] = valor
 
    if len(estado) == 0:
        estado = dict(VALORES_INICIALES)
        guardar_estado(estado)
    elif "meta_ahorro" not in estado:
        # Compatibilidad con un estado.csv del laboratorio anterior,
        # que no tenía esta clave.
        estado["meta_ahorro"] = 0
        guardar_estado(estado)
 
    return estado
 
 
def guardar_estado(estado):
    with open(ARCHIVO_ESTADO, "w") as f:
        for clave in estado:
            f.write(clave + "," + str(estado[clave]) + "\n")
 
 
# ------------------------------ Operaciones ------------------------------
 
def consignar(estado, monto):
    estado["saldo"] = estado["saldo"] + monto
    estado["total_consignado"] = estado["total_consignado"] + monto
    estado["num_consignaciones"] = estado["num_consignaciones"] + 1
    return estado
 
 
def retira(estado, monto):
    estado["saldo"] = estado["saldo"] - monto
    estado["total_retirado"] = estado["total_retirado"] + monto
    estado["num_retiros"] = estado["num_retiros"] + 1
    return estado
 
 
def fijar_meta(estado, monto):
    estado["meta_ahorro"] = monto
    return estado
 
 
# --------------------------------- UI ------------------------------------
 
st.set_page_config(page_title="Cajero UNAL", page_icon="🏦", layout="centered")
 
st.markdown(
    """
    <style>
    .stApp { background-color: #F7F8F5; }
    .cajero-header {
        background: linear-gradient(135deg, #2E5339 0%, #1F3864 100%);
        padding: 1.4rem 1.6rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.2rem;
    }
    .cajero-header h1 { margin: 0; font-size: 1.6rem; }
    .cajero-header p { margin: 0.2rem 0 0 0; opacity: 0.85; font-size: 0.9rem; }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E3E3E3;
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
 
if "estado" not in st.session_state:
    st.session_state.estado = cargar_estado()
 
estado = st.session_state.estado
 
st.markdown(
    """
    <div class="cajero-header">
        <h1>🏦 Cajero UNAL</h1>
        <p>Programación de Computadores con Python — Universidad Nacional de Colombia</p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
st.metric("Saldo actual", f"$ {estado['saldo']:,}")
 
tab_consultar, tab_consignar, tab_retirar, tab_simular, tab_stats, tab_meta = st.tabs(
    ["Consultar", "Consignar", "Retirar", "Simular ahorro", "Estadísticas", "Meta de ahorro"]
)
 
# --- Consultar saldo ---
with tab_consultar:
    st.write("Su saldo actual es de:")
    st.subheader(f"$ {estado['saldo']:,}")
    st.caption("Esta operación no modifica el estado ni el archivo.")
 
# --- Consignar ---
with tab_consignar:
    st.subheader("Consignar")
    monto = st.number_input(
        "Monto a consignar", min_value=0, step=10000, format="%d", key="monto_consignar"
    )
    if st.button("Consignar", type="primary"):
        if monto <= 0:
            st.error("Monto inválido. No se puede consignar ese valor.")
        else:
            estado = consignar(estado, int(monto))
            guardar_estado(estado)
            st.session_state.estado = estado
            st.success(f"Consignación exitosa. Su nuevo saldo es: $ {estado['saldo']:,}")
            st.rerun()
 
# --- Retirar ---
with tab_retirar:
    st.subheader("Retirar")
    monto_retiro = st.number_input(
        "Monto a retirar", min_value=0, step=10000, format="%d", key="monto_retirar"
    )
    if st.button("Retirar", type="primary"):
        if monto_retiro <= 0:
            st.error("El monto debe ser positivo.")
        elif monto_retiro % 10000 != 0:
            st.error("El monto debe ser múltiplo de $10.000.")
        elif monto_retiro > estado["saldo"]:
            st.error(f"Fondos insuficientes. Su saldo es de $ {estado['saldo']:,}")
        else:
            estado = retira(estado, int(monto_retiro))
            guardar_estado(estado)
            st.session_state.estado = estado
            st.success(
                f"Retiro exitoso. Retiró $ {int(monto_retiro):,}. "
                f"Su nuevo saldo es: $ {estado['saldo']:,}"
            )
            st.rerun()
 
# --- Simular ahorro ---
with tab_simular:
    st.subheader("Simulador de ahorro")
    st.caption("Proyecta mes a mes desde el saldo actual. No modifica el saldo real ni guarda nada.")
    col1, col2 = st.columns(2)
    with col1:
        ahorro = st.number_input("¿Cuánto va a ahorrar cada mes?", min_value=0, step=10000, format="%d")
    with col2:
        meses = st.number_input("¿Por cuántos meses?", min_value=0, step=1, format="%d")
 
    if st.button("Simular"):
        if ahorro <= 0:
            st.error("El monto debe ser positivo.")
        elif meses <= 0:
            st.error("Los meses deben ser positivos.")
        else:
            total = estado["saldo"]
            proyeccion = []
            for mes in range(1, int(meses) + 1):
                total += ahorro
                proyeccion.append(total)
 
            st.line_chart({"Saldo proyectado": proyeccion})
            st.success(f"En {int(meses)} meses tendría un total de $ {total:,}")
 
# --- Ver estadísticas ---
with tab_stats:
    st.subheader("Estadísticas")
    st.caption("Estos totales vienen del archivo, así que incluyen ejecuciones anteriores, no solo esta sesión.")
 
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total consignado", f"$ {estado['total_consignado']:,}")
        st.metric("Consignaciones realizadas", estado["num_consignaciones"])
        if estado["num_consignaciones"] > 0:
            promedio_c = estado["total_consignado"] / estado["num_consignaciones"]
            st.metric("Promedio por consignación", f"$ {promedio_c:,.0f}")
        else:
            st.caption("No se registraron consignaciones.")
 
    with c2:
        st.metric("Total retirado", f"$ {estado['total_retirado']:,}")
        st.metric("Retiros realizados", estado["num_retiros"])
        if estado["num_retiros"] > 0:
            promedio_r = estado["total_retirado"] / estado["num_retiros"]
            st.metric("Promedio por retiro", f"$ {promedio_r:,.0f}")
        else:
            st.caption("No se registraron retiros.")
 
# --- Meta de ahorro ---
with tab_meta:
    st.subheader("Meta de ahorro")
 
    nueva_meta = st.number_input(
        "Fijar o cambiar meta de ahorro", min_value=0, step=10000, format="%d", key="nueva_meta"
    )
    if st.button("Guardar meta", type="primary"):
        estado = fijar_meta(estado, int(nueva_meta))
        guardar_estado(estado)
        st.session_state.estado = estado
        st.success(f"Meta actualizada a $ {estado['meta_ahorro']:,}")
        st.rerun()
 
    st.divider()
 
    meta = estado["meta_ahorro"]
    saldo = estado["saldo"]
 
    if meta == 0:
        # Caso especial 1: no hay meta fijada todavía -> no se puede dividir entre 0
        st.info("Todavía no has fijado una meta de ahorro. Usa el campo de arriba para fijar una.")
    elif saldo >= meta:
        # Caso especial 2: el saldo ya alcanzó o superó la meta -> progreso tope en 1.0
        st.success(f"¡Meta alcanzada! Tu saldo (${saldo:,}) ya llegó a tu meta de ${meta:,}.")
        st.progress(1.0)
    else:
        progreso = saldo / meta
        faltante = meta - saldo
        st.write(f"Llevas $ {saldo:,} de tu meta de $ {meta:,}")
        st.write(f"Te faltan $ {faltante:,} — {progreso * 100:.1f}% alcanzado")
        st.progress(progreso)
 
st.divider()
st.caption(f"Estado persistido en `{ARCHIVO_ESTADO}` — cierra y vuelve a abrir la app para comprobar que el saldo continúa.")