"""Taller–Bitácora 2 · Cálculo Diferencial 2026-2S
Ejecutar con:  streamlit run app.py
"""
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Taller–Bitácora 2", page_icon="📐", layout="centered")

BASE = Path(__file__).parent
IMG = BASE / "imagenes"
EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# ─────────────────────────── DATOS PERSONALES ───────────────────────────
NOMBRE = "Jhoan Stiven Muñoz Barbosa"
GRUPO = "27"
FECHA = "16/11/2026"

# ─────────────────────────── ESTRUCTURA DEL CORTE ───────────────────────
SEMANAS = {
    6: "Continuidad y funciones definidas por tramos",
    7: "Derivada por definición, tangentes y velocidad",
    8: "Reglas de derivación",
    9: "Regla de la cadena y derivación implícita",
    10: "Funciones inversas, logaritmos y derivación logarítmica",
}
MINIMO_SEMANA = 3

ESPECIALES = {
    6: "Gráfica sencilla marcando qué debe coincidir para que haya continuidad. "
       "Cierra con: «El valor del parámetro sale porque...»",
    7: "De secante a tangente: muestra qué representa el cociente incremental antes del límite.",
    8: "Antes de derivar, leo la función: señala la estructura (producto, cociente, potencia...) "
       "y cómo supiste qué regla usar.",
    9: "Capas de una composición: separa función exterior e interior (esquema con flechas o colores).",
    10: "Elegir la técnica: explica en 2–3 líneas por qué esa técnica y qué habría sido más incómodo.",
}

CODIGOS_ERROR = {
    "C": "Continuidad: no revisé límites laterales o el valor de la función",
    "A": "Álgebra: signo, simplificación, factorización",
    "R": "Regla: elegí mal producto, cociente o potencia",
    "Cad": "Cadena: olvidé derivar la función interior",
    "I": "Implícita: olvidé multiplicar por y′ o despejé mal",
    "L": "Logaritmos / inversas: fórmula incompleta o dominio ignorado",
}


# ─────────────────────────── ENTRADAS ───────────────────────────────────
# Cada entrada tiene un id (e01, e02...). Las imágenes se buscan por id:
#   imagenes/e01_intento.jpg
#   imagenes/e01_procedimiento.jpg   (o e01_procedimiento_2.jpg, _3... para varias páginas)
#   imagenes/e01_especial.jpg        (solo entradas especiales ⭐)
#   imagenes/e01_error.jpg           (solo si registras un error: tu intento con el error marcado)
#   imagenes/e01_correccion.jpg      (solo si registras un error: tu segundo intento)
#
# Campos de texto (puedes usar LaTeX con $...$ o $$...$$):
#   proc       -> procedimiento escrito (opcional si pones foto)
#   respuesta  -> respuesta final simplificada
#   regla      -> «¿Qué regla usé y por qué?» en una línea
#   error_codigo / error_nota -> si te equivocaste (ver CODIGOS_ERROR); varios códigos separados por coma: "Cad, A"
def E(id, semana, subtema, ref, especial=False):
    return dict(
        id=id, semana=semana, subtema=subtema, ref=ref, especial=especial,
        proc="", respuesta="", regla="", error_codigo="", error_nota="",
    )


ENTRADAS = [
    # ── Semana 6 ──
    E("e01", 6, "Continuidad en un punto", "Stewart · Sec. 2.5 · ej. 20"),
    E("e02", 6, "Discontinuidades removibles y funciones por tramos", "Stewart · Sec. 2.5 · ej. 42"),
    E("e03", 6, "Parámetros y continuidad", "Stewart · Sec. 2.5 · ej. 45", especial=True),
    # ── Semana 7 ──
    E("e04", 7, "Rectas tangentes y razón de cambio", "Stewart · Sec. 2.7 · ej. 5", especial=True),
    E("e05", 7, "Derivada por definición", "Stewart · Sec. 2.8 · ej. 24"),
    E("e06", 7, "Movimiento rectilíneo", "Dueñas–Rubio · Sec. 5.2 · ej. 5.10, num. 3"),
    # ── Semana 8 ──
    E("e07", 8, "Potencias y funciones exponenciales", "Stewart · Sec. 3.1 · ej. 19"),
    E("e08", 8, "Producto y cociente", "Stewart · Sec. 3.2 · ej. 18", especial=True),
    E("e09", 8, "Funciones trigonométricas", "Stewart · Sec. 3.3 · ej. 3"),
    E("e10", 8, "Adicional · Producto y cociente", "Dueñas–Rubio · Sec. 5.3 · ej. 5.18, num. 6(d)"),
    # ── Semana 9 ──
    E("e11", 9, "Regla de la cadena", "Stewart · Sec. 3.4 · ej. 23", especial=True),
    E("e12", 9, "Composiciones con varias reglas", "Dueñas–Rubio · Sec. 5.8 · ej. 5.32, num. 7"),
    E("e13", 9, "Derivación implícita", "Stewart · Sec. 3.5 · ej. 14"),
    E("e14", 9, "Adicional · Regla de la cadena", "Stewart · Sec. 3.4 · ej. 35"),
    # ── Semana 10 ──
    E("e15", 10, "Funciones trigonométricas inversas", "Stewart · Sec. 3.5 · ej. 51"),
    E("e16", 10, "Funciones logarítmicas", "Stewart · Sec. 3.6 · ej. 13"),
    E("e17", 10, "Derivación logarítmica", "Stewart · Sec. 3.6 · ej. 43", especial=True),
    E("e18", 10, "Adicional · Derivación logarítmica", "Dueñas–Rubio · Sec. 5.11 · ej. 5.39, num. 2(d)"),
]

# Enunciados (solo el texto; las funciones se consultan en el libro).
# Transcritos de lo que pegó Stiven; verifícalos contra la página del libro.
ENUNCIADOS = {
    "e01": r"Explique por qué la función siguiente es discontinua en el número dado $a$. "
           r"Trace la gráfica de la función. Dato: $a=1$.",
    "e02": r"Encuentre los números en los que $f$ es discontinua. ¿En cuáles de estos números $f$ es continua "
           r"por la derecha, por la izquierda o por ninguna de las dos? Trace la gráfica de $f$.",
    "e03": r"¿Para qué valor de la constante $c$ la función $f$ es continua en $(-\infty,\infty)$?",
    "e04": r"Encuentre la ecuación de la recta tangente a cada una de las curvas siguientes en el punto dado. "
           r"Punto: $(2,-4)$.",
    "e05": r"Encuentre la derivada de cada una de las funciones siguientes usando la definición de derivada. "
           r"Indique los dominios de la función y de su derivada.",
    "e06": r"La función dada describe la posición (en metros) de un objeto que se mueve en línea recta, "
           r"con respecto al tiempo (en segundos). Halle, en el numeral 3: la velocidad y la aceleración "
           r"en el instante $t=4$ segundos.",
    "e07": "Derive cada una de las funciones siguientes.",
    "e08": "Derive cada una de las funciones siguientes.",
    "e09": "Derive cada una de las funciones siguientes.",
    "e10": "Use las propiedades para hallar la derivada de cada una de las siguientes funciones.",
    "e11": "Obtenga la derivada de cada una de las funciones siguientes.",
    "e12": "Hallar la derivada de cada una de las siguientes funciones.",
    "e13": "",  # pendiente: Stewart, Sec. 3.5, ej. 14 (no se encontró la página)
    "e14": "Obtenga la derivada de cada una de las funciones siguientes.",
    "e15": "Determine la derivada de cada una de las funciones siguientes. Simplifique donde sea posible.",
    "e16": "Derive la función.",
    "e17": "Utilice la derivación logarítmica para determinar la derivada de la función.",
    "e18": "Calcular la derivada de las siguientes funciones.",
}
for _e in ENTRADAS:
    _e["enunciado"] = ENUNCIADOS.get(_e["id"], "")

# Ejemplo de cómo se llena una entrada (bórralo cuando hagas la tuya):
# ENTRADAS[0].update(
#     ref="[S] Sec. 2.5, ej. 19",
#     proc=r"Calculo los límites laterales en $x=2$: $$\lim_{x\to2^-}f(x)=3$$",
#     respuesta=r"$f$ no es continua en $x=2$ porque los límites laterales difieren.",
#     regla="Revisé las tres condiciones de continuidad una por una.",
#     error_codigo="C",
#     error_nota="Olvidé calcular el valor f(2) en el primer intento.",
# )

# ─────────────────────────── PAUSAS Y CIERRE ────────────────────────────
PREGUNTAS_PAUSA = [
    "¿Qué regla reconozco mejor? (un ejemplo concreto)",
    "¿Qué error sigo repitiendo? (la señal que debo vigilar)",
    "¿Qué ejercicio debo repetir y por qué?",
    "¿Qué ya puedo explicar sin mirar?",
]
PAUSAS = {  # escribe tus respuestas en el mismo orden de PREGUNTAS_PAUSA
    6: ["", "", "", ""],
    12: ["", "", "", ""],
    18: ["", "", "", ""],
}
PREGUNTAS_CIERRE = [
    "La regla que mejor manejo ahora es...",
    "El error que debo vigilar en el parcial es...",
    "El ejercicio que volveré a resolver antes del parcial es...",
    "Cuando veo una función nueva, lo primero que miro es...",
]
CIERRE = ["", "", "", ""]
CITA = ("Resolver bien no es hacer muchos ejercicios. Es aprender a reconocer qué hacer, "
        "revisar lo que salió mal y poder intentarlo de nuevo.")


# ─────────────────────────── ESTILO (inspirado en Apple) ────────────────
CSS = """
<style>
:root {
    color-scheme: light !important;
    --background-color: #ffffff;
    --text-color: #1f2937;
}

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    color: #1f2937 !important;
}

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #1f2937;
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root{--azul:#0071e3;--texto:#1d1d1f;--gris:#6e6e73;--fondo:#f5f5f7;--tarjeta:#ffffff;--hueco:#fafafc;
--linea:rgba(0,0,0,.08);--seg:rgba(0,0,0,.055);--seg-sel:#ffffff;--seg-sombra:0 1px 3px rgba(0,0,0,.14);
--barra:rgba(0,0,0,.08);--codigo:rgba(0,0,0,.06);--borde-drop:rgba(0,0,0,.18);--pend:#a1a1a6;
--sombra:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.06);--sombra-img:0 2px 12px rgba(0,0,0,.10);
--chip-azul-bg:rgba(0,113,227,.12);--chip-azul:#0071e3;--chip-verde-bg:rgba(52,199,89,.16);--chip-verde:#1f8a3b;
--chip-gris-bg:rgba(0,0,0,.06);--chip-naranja-bg:rgba(255,149,0,.16);--chip-naranja:#b35c00;color-scheme:light;}
@media (prefers-color-scheme: dark){:root{--azul:#0a84ff;--texto:#f5f5f7;--gris:#98989d;--fondo:#000000;--tarjeta:#1c1c1e;--hueco:#111113;
--linea:rgba(255,255,255,.12);--seg:rgba(255,255,255,.10);--seg-sel:#3a3a3c;--seg-sombra:0 1px 3px rgba(0,0,0,.5);
--barra:rgba(255,255,255,.14);--codigo:rgba(255,255,255,.12);--borde-drop:rgba(255,255,255,.22);--pend:#6e6e73;
--sombra:0 0 0 1px rgba(255,255,255,.06),0 8px 24px rgba(0,0,0,.5);--sombra-img:0 2px 12px rgba(0,0,0,.6);
--chip-azul-bg:rgba(10,132,255,.22);--chip-azul:#64a9ff;--chip-verde-bg:rgba(48,209,88,.22);--chip-verde:#30d158;
--chip-gris-bg:rgba(255,255,255,.10);--chip-naranja-bg:rgba(255,159,10,.22);--chip-naranja:#ff9f0a;color-scheme:dark;}}
.stApp{background:var(--fondo);color:var(--texto);}
.stApp,.stApp p,.stApp li,.stApp label,.stApp button,.stApp h1,.stApp h2,.stApp h3,.stApp h4{
font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Inter","Helvetica Neue",Arial,sans-serif;
-webkit-font-smoothing:antialiased;}
.stApp p,.stApp li,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp [data-testid="stMarkdownContainer"]{color:var(--texto);}
.stApp code{background:var(--codigo);color:var(--texto);}
header[data-testid="stHeader"]{display:none;}
footer,#MainMenu{visibility:hidden;}
.block-container{max-width:880px;padding-top:2rem;padding-bottom:5rem;}
hr{border-color:var(--linea);}


/* tipografía */
.eyebrow{font-size:.74rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--gris);}
.hero{padding:2.6rem 0 1rem;text-align:center;}
.hero .grande{font-size:clamp(2.6rem,8vw,4.6rem);font-weight:700;letter-spacing:-.035em;line-height:1.05;margin:.4rem 0;
background:linear-gradient(90deg,#0a84ff 0%,#7a5af8 50%,#ff375f 100%);-webkit-background-clip:text;background-clip:text;color:transparent;}
.hero .sub{font-size:clamp(1.15rem,3vw,1.6rem);color:var(--gris);font-weight:500;}
.semana{margin:.8rem 0 1.4rem;}
.semana .t{font-size:clamp(1.7rem,5vw,2.5rem);font-weight:700;letter-spacing:-.03em;line-height:1.1;color:var(--texto);margin-top:.25rem;}
.semana .s{color:var(--gris);margin-top:.5rem;}

/* tarjetas */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:1rem 0;}
.card{background:var(--tarjeta);border-radius:20px;padding:1.1rem 1.25rem;box-shadow:var(--sombra);}
.card .k{font-size:.7rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--gris);}
.card .v{font-size:1.2rem;font-weight:600;color:var(--texto);margin-top:.25rem;}
.card .big{font-size:2.3rem;font-weight:700;letter-spacing:-.03em;}
.card .big small{font-size:1.1rem;color:var(--gris);font-weight:500;}
.card .n{font-size:.82rem;color:var(--gris);margin-top:.35rem;}
.card .n.txt{font-size:.95rem;color:var(--texto);}
.quote{background:var(--tarjeta);border-radius:22px;padding:1.6rem 1.9rem;box-shadow:var(--sombra);font-size:1.12rem;line-height:1.55;
color:var(--texto);margin:1.4rem 0;font-weight:500;letter-spacing:-.01em;}
.bar{height:6px;background:var(--barra);border-radius:99px;overflow:hidden;margin-top:.8rem;}
.bar>div{height:100%;background:var(--azul);border-radius:99px;}
.bar.verde>div{background:#34c759;}

/* chips */
.chip{display:inline-block;font-size:.74rem;font-weight:600;padding:.22rem .7rem;border-radius:99px;margin:0 .4rem .4rem 0;}
.chip.azul{background:var(--chip-azul-bg);color:var(--chip-azul);}
.chip.verde{background:var(--chip-verde-bg);color:var(--chip-verde);}
.chip.gris{background:var(--chip-gris-bg);color:var(--gris);}
.chip.naranja{background:var(--chip-naranja-bg);color:var(--chip-naranja);}

/* entradas */
[data-testid="stExpander"]{background:var(--tarjeta);border:none;border-radius:20px;box-shadow:var(--sombra);margin-bottom:14px;overflow:hidden;}
[data-testid="stExpander"] details{background:var(--tarjeta);border:none;border-radius:20px;}
[data-testid="stExpander"] summary{padding:1rem 1.3rem;font-weight:600;}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary p,[data-testid="stExpander"] summary span{color:var(--texto);}
[data-testid="stExpander"] summary:hover,[data-testid="stExpander"] summary:hover p,[data-testid="stExpander"] summary:hover span{color:var(--azul);}
.paso{display:flex;align-items:center;gap:.6rem;margin:1.4rem 0 .55rem;font-weight:600;font-size:1rem;color:var(--texto);}
.paso .n{width:24px;height:24px;border-radius:50%;background:var(--azul);color:#fff;font-size:.78rem;
display:inline-flex;align-items:center;justify-content:center;flex:none;}
.paso .s{font-weight:400;color:var(--gris);font-size:.88rem;}
.drop{border:1.5px dashed var(--borde-drop);border-radius:16px;padding:1.4rem;text-align:center;color:var(--gris);background:var(--hueco);font-size:.92rem;}
.drop code{background:var(--codigo);color:var(--texto);padding:.1rem .45rem;border-radius:6px;word-break:break-all;}
.pend{color:var(--pend);font-style:italic;}
[data-testid="stImage"] img{border-radius:14px;box-shadow:var(--sombra-img);}
/* navegación fija arriba */
div[data-testid="stElementContainer"]:has([data-testid="stButtonGroup"]){position:sticky;top:0;z-index:100;background:var(--fondo);
padding:.7rem 0 .6rem;border-bottom:1px solid var(--linea);margin-bottom:1rem;}
.element-container:has([data-testid="stButtonGroup"]){position:sticky;top:0;z-index:100;background:var(--fondo);
padding:.7rem 0 .6rem;border-bottom:1px solid var(--linea);margin-bottom:1rem;}

/* botones de página */
.stApp [data-testid="stBaseButton-secondary"]{border-radius:99px;background:var(--tarjeta);border:1px solid var(--linea);box-shadow:var(--sombra);}
.stApp [data-testid="stBaseButton-secondary"] p{color:var(--texto);font-weight:500;}
.stApp [data-testid="stBaseButton-secondary"]:hover{border-color:var(--azul);}
.stApp [data-testid="stBaseButton-secondary"]:hover p{color:var(--azul);}

/* lista de requisitos */
.fila{display:flex;gap:.7rem;align-items:flex-start;padding:.6rem 0;border-top:1px solid var(--linea);}
.fila .ok{font-size:1.1rem;line-height:1.3;}
.fila .d{color:var(--gris);font-size:.85rem;}
.fila b{color:var(--texto);font-weight:600;}
/* pills de navegación: colores propios para que se lean en cualquier modo */
.stApp [data-testid="stBaseButton-pills"]{background:var(--tarjeta);border:1px solid var(--linea);border-radius:99px;box-shadow:none;}
.stApp [data-testid="stBaseButton-pills"],.stApp [data-testid="stBaseButton-pills"] p,.stApp [data-testid="stBaseButton-pills"] span,
.stApp [data-testid="stBaseButton-pills"] div{color:var(--texto) !important;}
.stApp [data-testid="stBaseButton-pills"]:hover{border-color:var(--azul);}
.stApp [data-testid="stBaseButton-pillsActive"]{background:var(--azul);border:1px solid var(--azul);border-radius:99px;}
.stApp [data-testid="stBaseButton-pillsActive"],.stApp [data-testid="stBaseButton-pillsActive"] p,.stApp [data-testid="stBaseButton-pillsActive"] span,
.stApp [data-testid="stBaseButton-pillsActive"] div{color:#ffffff !important;}
</style>
"""


def html(s):
    """Renderiza HTML en una sola línea (evita que Markdown lo rompa)."""
    st.markdown(" ".join(l.strip() for l in s.strip().splitlines()), unsafe_allow_html=True)


# ─────────────────────────── FUNCIONES AUXILIARES ───────────────────────
def imagenes(prefijo):
    if not IMG.exists():
        return []
    return sorted(p for p in IMG.glob(f"{prefijo}*") if p.suffix.lower() in EXT)


def mostrar_imagenes(prefijo, descripcion):
    fotos = imagenes(prefijo)
    if fotos:
        for f in fotos:
            st.image(str(f), use_container_width=True)
    else:
        html(f'<div class="drop">📷 {descripcion}<br>Sube la foto como <code>imagenes/{prefijo}.jpg</code></div>')


def texto_o_pendiente(texto):
    if texto:
        st.markdown(texto)
    else:
        html('<span class="pend">Pendiente</span>')


def paso(n, titulo, sub=""):
    extra = f' <span class="s">{sub}</span>' if sub else ""
    html(f'<div class="paso"><span class="n">{n}</span>{titulo}{extra}</div>')


def barra(valor, total, clase=""):
    pct = 0 if total == 0 else round(100 * valor / total)
    return f'<div class="bar {clase}"><div style="width:{pct}%"></div></div>'


# ─────────────────────────── NAVEGACIÓN: ORDEN Y ETIQUETAS ──────────────
SLUGS = ["inicio", "tablero"] + [f"s{s}" for s in SEMANAS] + ["pausas", "cierre"]
ETIQUETAS = {"inicio": "Inicio", "tablero": "Tablero", "pausas": "Pausas", "cierre": "Cierre"}
ETIQUETAS.update({f"s{s}": f"Sem. {s}" for s in SEMANAS})


def ir(slug):
    st.session_state["pagina"] = slug
    st.session_state["_subir"] = True


def navegacion(ant=None, sig=None, etiqueta_sig=None):
    st.write("")
    c1, c2 = st.columns(2)
    if ant:
        c1.button(f"← {ETIQUETAS[ant]}", on_click=ir, args=(ant,), key=f"ant_{ant}", use_container_width=True)
    if sig:
        texto = etiqueta_sig or f"Siguiente · {ETIQUETAS[sig]}"
        c2.button(f"{texto} →", on_click=ir, args=(sig,), key=f"sig_{sig}", use_container_width=True)


def entrada_completa(e):
    tiene_proc = bool(e["proc"]) or bool(imagenes(f"{e['id']}_procedimiento"))
    return tiene_proc and bool(e["respuesta"])


def codigos(e):
    return [c.strip() for c in e["error_codigo"].split(",") if c.strip()]


def respondida(respuestas):
    return all(r.strip() for r in respuestas)


def conteo_errores():
    cuenta = {k: 0 for k in CODIGOS_ERROR}
    for e in ENTRADAS:
        for c in codigos(e):
            if c in cuenta:
                cuenta[c] += 1
    return cuenta


def requisitos():
    hechas = sum(entrada_completa(e) for e in ENTRADAS)
    faltan = [f"Sem. {s}" for s in SEMANAS
              if sum(entrada_completa(e) for e in ENTRADAS if e["semana"] == s) < MINIMO_SEMANA]
    n_esp = sum(any(e["especial"] and entrada_completa(e) for e in ENTRADAS if e["semana"] == s)
                for s in SEMANAS)
    n_pausas = sum(respondida(r) for r in PAUSAS.values())
    con_error = sum(1 for e in ENTRADAS if codigos(e))
    return [
        (15 <= len(ENTRADAS) <= 20, "Entre 15 y 20 ejercicios en la bitácora", f"{len(ENTRADAS)} en la lista"),
        (hechas >= 15, "Al menos 15 entradas completas", f"{hechas} de 15"),
        (not faltan, "Las cinco semanas cubiertas (mínimo 3 entradas completas por semana)",
         "Todas listas" if not faltan else "Faltan: " + ", ".join(faltan)),
        (n_esp == 5, "Una entrada especial completa por semana", f"{n_esp} de 5"),
        (n_pausas == len(PAUSAS), "Pausas de aprendizaje respondidas (6, 12 y 18)", f"{n_pausas} de {len(PAUSAS)}"),
        (respondida(CIERRE), "Última página respondida", "Completa" if respondida(CIERRE) else "Pendiente"),
        (con_error >= 1, "Correcciones visibles (al menos un error registrado)", f"{con_error} entrada(s) con error"),
    ]


def mostrar_entrada(e):
    completa = entrada_completa(e)
    estado = "✅" if completa else "⏳"
    estrella = "⭐ " if e["especial"] else ""
    cods = codigos(e)
    with st.expander(f"{estado}  {estrella}{e['id'].upper()} · {e['subtema']}"):
        chips = f'<span class="chip gris">Semana {e["semana"]}</span>'
        if e["especial"]:
            chips += '<span class="chip azul">⭐ Entrada especial</span>'
        chips += ('<span class="chip verde">Completa</span>' if completa
                  else '<span class="chip naranja">En progreso</span>')
        chips += "".join(f'<span class="chip gris">Error {c}</span>' for c in cods)
        html(chips)

        paso(1, "Referencia")
        st.markdown(e["ref"])
        if e.get("enunciado"):
            html('<div class="eyebrow" style="margin:.8rem 0 .3rem">Enunciado</div>')
            st.markdown(e["enunciado"])

        paso(2, "Intento", "antes de mirar ayuda")
        mostrar_imagenes(f"{e['id']}_intento", "Foto de tu primer intento")

        paso(3, "Procedimiento")
        if e["proc"]:
            st.markdown(e["proc"])
        mostrar_imagenes(f"{e['id']}_procedimiento", "Foto del procedimiento")

        paso(4, "Respuesta")
        texto_o_pendiente(e["respuesta"])

        paso(5, "Nota breve", "¿qué regla usé y por qué?")
        texto_o_pendiente(e["regla"])

        if e["especial"]:
            st.divider()
            html(f'<div class="card"><div class="k">⭐ Parte especial de la semana {e["semana"]}</div>'
                 f'<div class="n txt">{ESPECIALES[e["semana"]]}</div></div>')
            mostrar_imagenes(f"{e['id']}_especial", "Gráfica o esquema de la entrada especial")

        if cods:
            st.divider()
            paso("!", f"Error registrado [{', '.join(cods)}]")
            html("".join(f'<div class="n">{c} · {CODIGOS_ERROR.get(c, "")}</div>' for c in cods))
            texto_o_pendiente(e["error_nota"])
            antes, despues = st.columns(2)
            with antes:
                html('<div class="eyebrow" style="margin:.8rem 0 .4rem">Antes · error marcado</div>')
                mostrar_imagenes(f"{e['id']}_error", "Primer intento con el error marcado")
            with despues:
                html('<div class="eyebrow" style="margin:.8rem 0 .4rem">Después · corrección</div>')
                mostrar_imagenes(f"{e['id']}_correccion", "Segundo intento, sin mirar la solución")


# ─────────────────────────── PÁGINAS ────────────────────────────────────
def pagina_portada():
    html(f"""
    <div class="hero">
      <div class="eyebrow">Cálculo Diferencial · Segundo corte · 2026-2S</div>
      <div class="grande">Taller–Bitácora 2</div>
      <div class="sub">Continuidad y derivadas</div>
    </div>
    <div class="quote">“{CITA}”</div>
    <div class="grid">
      <div class="card"><div class="k">Estudiante</div><div class="v">{NOMBRE}</div></div>
      <div class="card"><div class="k">Grupo</div><div class="v">{GRUPO}</div></div>
      <div class="card"><div class="k">Entrega</div><div class="v">{FECHA}</div></div>
      <div class="card"><div class="k">Docente</div><div class="v">Jhoan Sebastián Tenjo García</div></div>
    </div>
    <div class="eyebrow" style="text-align:center;margin-top:1.6rem">
      Universidad Nacional de Colombia · Departamento de Matemáticas
    </div>
    """)
    if imagenes("portada"):
        mostrar_imagenes("portada", "Imagen de portada")
    navegacion(sig="s6", etiqueta_sig="Empezar · Sem. 6")


def pagina_tablero():
    total = len(ENTRADAS)
    hechas = sum(entrada_completa(e) for e in ENTRADAS)
    especiales = sum(
        any(e["especial"] and entrada_completa(e) for e in ENTRADAS if e["semana"] == s)
        for s in SEMANAS
    )
    n_img = len([p for p in IMG.glob("*") if p.suffix.lower() in EXT]) if IMG.exists() else 0

    html(f"""
    <div class="semana"><div class="eyebrow">Resumen</div><div class="t">Tablero de progreso</div>
    <div class="s">Meta: 18 entradas (mínimo 15, máximo 20). Las marcadas ⭐ son las especiales.</div></div>
    <div class="grid">
      <div class="card"><div class="k">Entradas completas</div>
        <div class="v big">{hechas}<small> / {total}</small></div>{barra(hechas, total)}</div>
      <div class="card"><div class="k">Entradas especiales</div>
        <div class="v big">{especiales}<small> / 5</small></div>{barra(especiales, 5, "verde")}</div>
      <div class="card"><div class="k">Imágenes subidas</div>
        <div class="v big">{n_img}</div></div>
    </div>
    <div class="eyebrow" style="margin:1.6rem 0 .4rem">Por semana</div>
    """)

    tarjetas = ""
    for s in SEMANAS:
        es = [e for e in ENTRADAS if e["semana"] == s]
        ok = sum(entrada_completa(e) for e in es)
        esp = "✅" if any(e["especial"] and entrada_completa(e) for e in es) else "⏳"
        tarjetas += (f'<div class="card"><div class="k">Semana {s}</div>'
                     f'<div class="v big">{ok}<small> / {len(es)}</small></div>'
                     f'{barra(ok, len(es))}<div class="n">Mínimo {MINIMO_SEMANA} · Especial {esp}</div></div>')
    html(f'<div class="grid">{tarjetas}</div>')

    # 1 · Requisitos del bono
    reqs = requisitos()
    cumplidos = sum(1 for ok, _, _ in reqs if ok)
    filas = "".join(
        f'<div class="fila"><span class="ok">{"✅" if ok else "⏳"}</span>'
        f'<div><b>{titulo}</b><br><span class="d">{detalle}</span></div></div>'
        for ok, titulo, detalle in reqs
    )
    html(f"""
    <div class="eyebrow" style="margin:1.6rem 0 .4rem">Requisitos para activar el bono</div>
    <div class="card"><div class="v">{cumplidos} de {len(reqs)} cumplidos</div>
    {barra(cumplidos, len(reqs), "verde")}<div style="margin-top:.6rem">{filas}</div></div>
    """)

    # 3 · Resumen de errores
    cuenta = conteo_errores()
    total_err = sum(cuenta.values())
    html('<div class="eyebrow" style="margin:1.6rem 0 .4rem">Mis errores por tipo</div>')
    if total_err == 0:
        html('<div class="card"><div class="n txt">Aún no hay errores registrados. '
             'Cuando pongas <code>error_codigo</code> en una entrada, el conteo aparece aquí.</div></div>')
    else:
        mx = max(cuenta.values())
        top = ", ".join(k for k, v in cuenta.items() if v == mx)
        html(f'<div class="n txt" style="margin-bottom:.6rem">El que más se repite: <b>{top}</b> '
             f'({mx} {"vez" if mx == 1 else "veces"}). Vigílalo en el parcial.</div>')
        tarjetas = "".join(
            f'<div class="card"><div class="k">{k}</div><div class="v big">{v}</div>'
            f'{barra(v, mx)}<div class="n">{CODIGOS_ERROR[k]}</div></div>'
            for k, v in cuenta.items()
        )
        html(f'<div class="grid">{tarjetas}</div>')
    navegacion(ant="inicio", sig="s6")


def pagina_semana(s):
    es = [x for x in ENTRADAS if x["semana"] == s]
    ok = sum(entrada_completa(e) for e in es)
    html(f"""
    <div class="semana"><div class="eyebrow">Semana {s}</div>
    <div class="t">{SEMANAS[s]}</div>
    <div class="s">{ok} de {len(es)} entradas completas</div></div>
    """)
    for e in es:
        mostrar_entrada(e)
    i = SLUGS.index(f"s{s}")
    navegacion(ant=SLUGS[i - 1], sig=SLUGS[i + 1])


def pagina_pausas():
    html("""
    <div class="semana"><div class="eyebrow">Aprendizaje</div><div class="t">Pausas</div>
    <div class="s">Cuatro preguntas cortas después de los ejercicios 6, 12 y 18.</div></div>
    """)
    cuenta = conteo_errores()
    if sum(cuenta.values()) > 0:
        mx = max(cuenta.values())
        top = ", ".join(k for k, v in cuenta.items() if v == mx)
        html(f'<div class="n txt" style="margin-bottom:1rem">Tu error más frecuente hasta ahora: <b>{top}</b> '
             '(detalle en el Tablero).</div>')
    for n, resp in PAUSAS.items():
        with st.expander(f"⏸️  Pausa después del ejercicio {n}"):
            for i, (preg, r) in enumerate(zip(PREGUNTAS_PAUSA, resp), start=1):
                paso(i, preg)
                texto_o_pendiente(r)
    navegacion(ant="s10", sig="cierre")


def pagina_cierre():
    html("""
    <div class="semana"><div class="eyebrow">Para terminar</div><div class="t">Última página</div></div>
    """)
    for i, (preg, r) in enumerate(zip(PREGUNTAS_CIERRE, CIERRE), start=1):
        paso(i, preg)
        texto_o_pendiente(r)
    html('<div class="hero" style="padding-top:2.5rem"><div class="sub">Resolver. Revisar. Volver a intentar.</div></div>')
    navegacion(ant="pausas")


# ─────────────────────────── NAVEGACIÓN (fija arriba) ───────────────────
html(CSS)

if "pagina" not in st.session_state:
    p = st.query_params.get("p", "inicio")
    st.session_state["pagina"] = p if p in SLUGS else "inicio"

st.pills("Navegación", SLUGS, format_func=lambda s: ETIQUETAS[s], key="pagina",
         label_visibility="collapsed")
actual = st.session_state.get("pagina") or "inicio"
st.query_params["p"] = actual  # el enlace conserva la página abierta

if actual == "inicio":
    pagina_portada()
elif actual == "tablero":
    pagina_tablero()
elif actual == "pausas":
    pagina_pausas()
elif actual == "cierre":
    pagina_cierre()
else:
    pagina_semana(int(actual[1:]))

# al cambiar de página con los botones, vuelve arriba
if st.session_state.pop("_subir", False):
    try:
        st.html(
            "<script>const m=document.querySelector('[data-testid=\"stMain\"]')"
            "||document.querySelector('section.main');if(m){m.scrollTo({top:0});}</script>",
            unsafe_allow_javascript=True,
        )
    except Exception:
        pass
