import os
import json
import requests
from typing import List, Dict, Any


OPENROUTER_ENV_VAR = "OPENROUTER_API_KEY"
SECRETS_FILE = "secrets.json"  
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"

def _split_components(components: str) -> list[str]:
    parts = [c.strip() for c in components.replace("\n", ",").split(',') if c.strip()]
    return parts

def _build_prompt(products: List[Dict[str, Any]], components: str) -> str:
    comp_list = _split_components(components)
    lines = [
        "You are an assistant that determines if each product is COMPATIBLE with all of the user's listed components.",
        "Return ONLY JSON with the structure: {\"compatibility\": [{\"index\": <int>, \"compatible\": true/false}, ...] }.",
        "Decide true only if the product plausibly matches or supports ALL key components; be conservative.",
        f"Components: {', '.join(comp_list) if comp_list else '(none provided)'}",
        "Products:" 
    ]
    for i, p in enumerate(products):
        title = p.get('title','').strip().replace('\n',' ')[:160]
        lines.append(f"{i}. title={title}")
    return "\n".join(lines)

def _load_api_key() -> str:
    """Load API key from env first, then secrets.json; return empty string if absent."""
    key = os.getenv(OPENROUTER_ENV_VAR, "").strip()
    if key:
        return key
    # fallback to secrets file (local only, user-managed)
    try:
        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return str(data.get(OPENROUTER_ENV_VAR, "")).strip()
    except Exception:
        pass
    return ""

def _call_model(prompt: str) -> dict | None:
    api_key = _load_api_key()
    if not api_key:
        return None
    try:
        resp = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "response_format": {"type": "json_object"}
            },
            timeout=60,
        )
    except Exception:
        return None
    if resp.status_code != 200:
        return None
    try:
        data = resp.json()
    except Exception:
        return None
    # Standard OpenRouter shape: choices[0].message.content
    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        return None
    try:
        parsed = json.loads(content)
        return parsed
    except Exception:
        return None

def _fallback_heuristic(products: List[Dict[str, Any]], components: str) -> list[bool]:
    comp_tokens = [c.lower() for c in _split_components(components)]
    flags = []
    for p in products:
        title = (p.get('title') or '').lower()
        if not comp_tokens:
            flags.append(False)
            continue
        # basic AND matching: all component tokens must appear somewhere
        ok = all(token in title for token in comp_tokens)
        flags.append(ok)
    return flags

def flag_items(products: List[Dict[str, Any]], components: str) -> List[Dict[str, Any]]:
    if not isinstance(products, list):
        return []
    for p in products:
        if isinstance(p, dict) and 'compatible' not in p:
            p['compatible'] = False
    if not products:
        return products
    prompt = _build_prompt(products, components or '')
    model_result = _call_model(prompt)
    if isinstance(model_result, dict) and 'compatibility' in model_result:
        print("from model")
    if model_result and isinstance(model_result, dict) and 'compatibility' in model_result:
        compat_map = {}
        for entry in model_result.get('compatibility', []):
            try:
                idx = int(entry.get('index'))
                comp_flag = bool(entry.get('compatible'))
                compat_map[idx] = comp_flag
            except Exception:
                continue
        for i, p in enumerate(products):
            if i in compat_map:
                p['compatible'] = compat_map[i]
            else:
                p['compatible'] = False
        return products
    # fallback heuristics
    heuristics = _fallback_heuristic(products, components or '')
    for p, h in zip(products, heuristics):
        p['compatible'] = h
    print("from heuristic")
    return products

if __name__ == "__main__":  # simple manual smoke test (will use heuristic if no key)
    sample_products = [
        {"title": "Arduino UNO R3 Board", "price": "BDT 1200", "link": "#"},
        {"title": "Raspberry Pi 4 8GB", "price": "BDT 8500", "link": "#"},
        {"title": "Jumper Wires Set", "price": "BDT 150", "link": "#"},
    ]
    comps = "arduino, board"
    flagged = flag_items(sample_products, comps)
    print(json.dumps(flagged, indent=2))