import streamlit as st
import pandas as pd

from components.scanner import qr_scanner
from services.deduplicator import add_code, clear_session
from services.exporter import build_excel

st.set_page_config(
    page_title="QR / Barcode Scanner",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Session state defaults ────────────────────────────────────────────────────
for key, default in [
    ("seen_codes", set()),
    ("code_list", []),
    ("last_processed_scan_id", None),
    ("last_scan_result", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Configuración")

    session_name = st.text_input(
        "Sesión / Lote / Operario",
        placeholder="Ej: Operario Juan — Lote A3",
        key="session_name_input",
    )

    st.divider()
    st.metric("Códigos únicos escaneados", len(st.session_state.code_list))

    if st.button("Limpiar sesión", type="secondary", use_container_width=True):
        clear_session()
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("Scanner QR / Barcode")

if not session_name:
    st.info("Ingresa el nombre de sesión en el panel lateral para comenzar.")
    st.stop()

# Scanner component
scan_result = qr_scanner(key="qr_scanner")

# Process incoming scan — only when scan_id is new
if scan_result and isinstance(scan_result, dict):
    scan_id = scan_result.get("scan_id")
    code = scan_result.get("code", "").strip()
    code_type = scan_result.get("type", "UNKNOWN")

    if code and scan_id != st.session_state.last_processed_scan_id:
        st.session_state.last_processed_scan_id = scan_id
        is_new = add_code(code, code_type, session_name)
        st.session_state.last_scan_result = {"code": code, "is_new": is_new}

# Feedback message
if st.session_state.last_scan_result:
    result = st.session_state.last_scan_result
    if result["is_new"]:
        st.success(f"Nuevo código agregado: `{result['code']}`")
    else:
        st.warning(f"Duplicado ignorado: `{result['code']}`")

# Code list + export
if st.session_state.code_list:
    st.divider()
    st.subheader(f"{len(st.session_state.code_list)} código(s) único(s)")

    df = pd.DataFrame(st.session_state.code_list)
    df.columns = ["#", "Código", "Tipo", "Fecha/Hora", "Sesión"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    safe_name = session_name.replace(" ", "_").replace("/", "-")
    excel_bytes = build_excel(st.session_state.code_list)
    st.download_button(
        label="Exportar a Excel",
        data=excel_bytes,
        file_name=f"codigos_{safe_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True,
    )
