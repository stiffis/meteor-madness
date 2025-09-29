#!/usr/bin/env python3
"""Probar el endpoint /api/neo/search del backend."""

import argparse
import sys
from typing import Any, Dict

import requests


def search(base_url: str, query: str, limit: int) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/neo/search"
    response = requests.get(
        url,
        params={"q": query, "limit": limit},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Test NEO search endpoint")
    parser.add_argument("query", nargs="?", default="Apophis", help="Texto a buscar (default: Apophis)")
    parser.add_argument("--limit", type=int, default=5, help="Límite de resultados (default: 5)")
    parser.add_argument(
        "--base-url",
        default="http://localhost:5000",
        help="URL base del backend (default: http://localhost:5000)",
    )
    args = parser.parse_args()

    print(f"➡️  Buscando '{args.query}' en {args.base_url} (limit={args.limit})...")

    try:
        payload = search(args.base_url, args.query, args.limit)
    except requests.exceptions.RequestException as exc:
        print(f"❌ Error al contactar al backend: {exc}")
        print("💡 ¿Está corriendo python app.py y tienes conexión a internet?")
        return 1

    if not payload.get("success"):
        print("⚠️  Búsqueda sin éxito:")
        print(payload)
        return 2

    data = payload.get("data", {})
    results = data.get("results", [])
    print(f"✅ {len(results)} resultados (count reportado: {data.get('count')})")

    for item in results:
        name = item.get("full_name") or item.get("designation")
        moid = item.get("moid_au")
        h = item.get("absolute_magnitude_h")
        pha = item.get("pha")
        print(f"   • {name} | MOID: {moid} au | H: {h} | PHA: {pha}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
