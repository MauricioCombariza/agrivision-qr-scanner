import os
import streamlit.components.v1 as components

_FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "scanner_frontend")
_scanner_component = components.declare_component("qr_scanner", path=_FRONTEND_DIR)


def qr_scanner(key: str = "qr_scanner") -> dict | None:
    return _scanner_component(key=key, default=None, height=560)
