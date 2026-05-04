"""
modules/copilot – sdílený Copilot API modul
Importuj: from copilot_api import ask, ask_json, is_available
"""
from .copilot_api import ask, ask_json, is_available, RateLimitError

__all__ = ["ask", "ask_json", "is_available", "RateLimitError"]
