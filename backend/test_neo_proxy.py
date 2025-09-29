#!/usr/bin/env python3
"""Probar el endpoint proxy /api/neo/object del backend."""

import argparse
import sys
from typing import Any, Dict

import requests


def fetch_neo(base_url: str, identifier: str) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/neo/object"
    response = requests.get(url, params={"designation": identifier}, timeout=20)
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Test proxy NASA NEO endpoint")
    parser.add_argument(
        "identifier",
        nargs="?",
        default="99942",
        help="Designación o nombre del objeto NEO (default: 99942 Apophis)",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:5000",
        help="URL base del backend (default: http://localhost:5000)",
    )
    args = parser.parse_args()

    print(f"➡️  Consultando {args.identifier} en {args.base_url}...")

    try:
        payload = fetch_neo(args.base_url, args.identifier)
    except requests.exceptions.RequestException as exc:
        print(f"❌ Error al contactar al backend: {exc}")
        print("💡 ¿Está corriendo python app.py y tienes conexión a internet?")
        return 1

    if not payload.get("success"):
        print("⚠️  El backend respondió sin éxito:")
        print(payload)
        return 2

    data = payload.get("data", {})
    sim_elements = data.get("simulation_elements")
    missing = data.get("missing_for_simulation")

    print("✅ Respuesta recibida");
    if sim_elements:
        print("   Elementos listos para simulación (km / grados):")
        for key, value in sim_elements.items():
            print(f"     - {key}: {value}")
    else:
        print("   No se pudieron extraer elementos completos para simulación.")
        if missing:
            print(f"   Faltan campos en la respuesta NASA: {missing}")

    orbit_epoch = data.get("orbit", {}).get("epoch")
    if orbit_epoch:
        print("   Época (JD):", orbit_epoch.get("jd"))

    physical = data.get("physical")
    if physical:
        diameter = physical.get("diameter")
        if diameter:
            print("   Diámetro estimado (km):", diameter)

    return 0


if __name__ == "__main__":
    sys.exit(main())
