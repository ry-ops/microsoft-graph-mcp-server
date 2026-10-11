import importlib
import os

import msal


def test_module_loads(monkeypatch):
    monkeypatch.setenv("MICROSOFT_TENANT_ID", "tenant")
    monkeypatch.setenv("MICROSOFT_CLIENT_ID", "client")
    monkeypatch.setenv("MICROSOFT_CLIENT_SECRET", "secret")
    monkeypatch.setattr(msal, "ConfidentialClientApplication", lambda *a, **k: object())
    module = importlib.import_module("mcp_graph_server")
    assert callable(module.main)
    assert os.path.basename(module.__file__) == "mcp_graph_server.py"
