"""
Automatický test modules/copilot
Spuštění: python test_copilot.py
"""
import sys
from pathlib import Path

# Přidej složku modulu na sys.path
sys.path.insert(0, str(Path(__file__).parent))

import traceback

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"

results = []

def test(name, fn):
    try:
        fn()
        print(f"  {PASS}  {name}")
        results.append((name, True, None))
    except Exception as e:
        print(f"  {FAIL}  {name}: {e}")
        results.append((name, False, e))


# ── Test 1: import ────────────────────────────────────────────────────────────
def t_import():
    from copilot_api import ask, ask_json, is_available, RateLimitError
    assert callable(ask)
    assert callable(ask_json)
    assert callable(is_available)

test("import copilot_api", t_import)


# ── Test 2: is_available ──────────────────────────────────────────────────────
def t_available():
    from copilot_api import is_available
    from copilot_auth import _find_oauth_token, _read_vscode_github_token
    tok = _find_oauth_token()
    vsc = _read_vscode_github_token()
    print(f"\n     token zdroj: {'VSCode DB' if vsc else 'Credential Manager'}")
    print(f"     token prefix: {tok[:8]}..." if tok else "     token: NENALEZEN")
    result = is_available()
    assert isinstance(result, bool), f"is_available() vrátilo {type(result)}"
    if not result:
        raise AssertionError(
            "Copilot API odmítlo token (pravděpodobně chybí scope 'copilot').\n"
            "     Řešení: vytvoř ~/.writerroom/.env s GITHUB_OAUTH_TOKEN=ghp_..."
        )

test("is_available() == True", t_available)


# ── Test 3: ask – jednoduchý dotaz ────────────────────────────────────────────
def t_ask():
    from copilot_api import is_available, ask
    if not is_available():
        raise AssertionError("Přeskočeno – Copilot nedostupný")
    resp = ask("Odpověz pouze slovem: ahoj", max_tokens=10)
    assert isinstance(resp, str) and len(resp) > 0, f"Prázdná odpověď: {resp!r}"

test("ask() vrátí neprázdný string", t_ask)


# ── Test 4: ask_json ──────────────────────────────────────────────────────────
def t_ask_json():
    from copilot_api import is_available, ask_json
    if not is_available():
        raise AssertionError("Přeskočeno – Copilot nedostupný")
    data = ask_json('Vrať JSON objekt s klíčem "ok" a hodnotou true.')
    assert isinstance(data, dict), f"Očekáván dict, dostali jsme {type(data)}"

test("ask_json() vrátí dict", t_ask_json)


# ── Výsledky ──────────────────────────────────────────────────────────────────
passed = sum(1 for _, ok, _ in results if ok)
total = len(results)
print(f"\n{'='*40}")
print(f"  Výsledek: {passed}/{total} testů prošlo")
if passed < total:
    sys.exit(1)
