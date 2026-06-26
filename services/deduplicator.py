from __future__ import annotations
from datetime import datetime
import streamlit as st


def _init():
    if "seen_codes" not in st.session_state:
        st.session_state.seen_codes = set()
    if "code_list" not in st.session_state:
        st.session_state.code_list = []
    if "last_processed_scan_id" not in st.session_state:
        st.session_state.last_processed_scan_id = None


def add_code(code: str, code_type: str, session_name: str) -> bool:
    """Returns True if code is new and was added, False if duplicate."""
    _init()
    if code in st.session_state.seen_codes:
        return False
    st.session_state.seen_codes.add(code)
    st.session_state.code_list.append({
        "order": len(st.session_state.code_list) + 1,
        "code": code,
        "type": code_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session": session_name,
    })
    return True


def clear_session():
    st.session_state.seen_codes = set()
    st.session_state.code_list = []
    st.session_state.last_processed_scan_id = None
    st.session_state.last_scan_result = None
