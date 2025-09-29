"""Servicio para interactuar con los datos públicos de la NASA (CNEOS / SBDB).

Este módulo actúa como proxy entre el backend de MeteorMadness y la
Small-Body Database API de JPL, entregando la información ya normalizada
para su uso en la simulación.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


AU_IN_KM = 149_597_870.7


@dataclass
class NeoLookupResult:
    """Representa la respuesta procesada para un objeto NEO."""

    success: bool
    status_code: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class NasaNeoService:
    """Cliente simple para la Small-Body Database API (sbdb.api)."""

    BASE_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"

    def __init__(self, session: Optional[requests.Session] = None, timeout: int = 15):
        self.session = session or requests.Session()
        self.timeout = timeout

    def fetch_object(self, identifier: str) -> NeoLookupResult:
        """Obtiene la información de un objeto a partir de su identificador.

        La API acepta designaciones, números MPC, SPK-ID o nombres comunes.
        """

        if not identifier:
            return NeoLookupResult(
                success=False,
                status_code=400,
                error="Identifier is required to query NASA SBDB",
            )

        try:
            response = self.session.get(
                self.BASE_URL,
                params={"sstr": identifier, "full-prec": "true"},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            return NeoLookupResult(
                success=False,
                status_code=503,
                error=f"Failed to contact NASA SBDB service: {exc}",
            )

        if response.status_code == 404:
            return NeoLookupResult(
                success=False,
                status_code=404,
                error="Object not found in NASA SBDB",
            )

        if not response.ok:
            return NeoLookupResult(
                success=False,
                status_code=response.status_code,
                error=f"NASA SBDB responded with status {response.status_code}",
            )

        payload: Dict[str, Any] = response.json()

        if "object" not in payload:
            # La API puede devolver un estado con mensaje de error.
            error_message = payload.get("message") or payload.get("error") or "Invalid response from NASA SBDB"
            return NeoLookupResult(
                success=False,
                status_code=502,
                error=error_message,
            )

        processed = self._build_response(payload)
        return NeoLookupResult(success=True, status_code=200, data=processed)

    # ------------------------------------------------------------------
    # Helpers privados

    def _build_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        object_info = payload.get("object", {})
        orbit_section = payload.get("orbit", {}) or {}
        physical_section = payload.get("phys_par", {}) or {}

        elements_dict = self._element_list_to_dict(orbit_section.get("elements"))
        physical_dict = self._element_list_to_dict(physical_section.get("parameters"))

        simulation_ready, missing = self._extract_simulation_elements(elements_dict)

        return {
            "source": {
                "service": "NASA/JPL Small-Body Database API",
                "endpoint": self.BASE_URL,
                "citation": "https://ssd-api.jpl.nasa.gov/doc/sbdb.html",
            },
            "object": {
                "designation": object_info.get("des"),
                "full_name": object_info.get("fullname"),
                "neo": object_info.get("neo"),
                "pha": object_info.get("pha"),
                "orbit_class": object_info.get("orbit_class"),
                "alternate_designations": object_info.get("alts"),
            },
            "orbit": {
                "epoch": self._normalize_epoch(orbit_section.get("epoch")),
                "elements": elements_dict,
                "residuals": orbit_section.get("residuals"),
            },
            "physical": physical_dict or None,
            "simulation_elements": simulation_ready,
            "missing_for_simulation": missing or None,
        }

    @staticmethod
    def _element_list_to_dict(elements: Optional[Any]) -> Dict[str, Any]:
        if not elements:
            return {}

        if isinstance(elements, dict):
            iterator = elements.values()
        else:
            iterator = elements

        parsed: Dict[str, Any] = {}
        for entry in iterator:
            if not isinstance(entry, dict):
                continue

            key = entry.get("name") or entry.get("label")
            if not key:
                continue

            value = entry.get("value")
            if isinstance(value, str):
                value = value.strip()

            parsed[key] = NasaNeoService._coerce_number(value)

            if "uncertainty" in entry:
                uncertainty_key = f"{key}_unc"
                parsed[uncertainty_key] = NasaNeoService._coerce_number(entry["uncertainty"])

        return parsed

    @staticmethod
    def _coerce_number(value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return value

        try:
            return float(value)
        except (TypeError, ValueError):
            return value

    @staticmethod
    def _normalize_epoch(epoch_section: Optional[Any]) -> Optional[Dict[str, Any]]:
        if not epoch_section:
            return None

        if isinstance(epoch_section, dict):
            value = epoch_section.get("value") or epoch_section.get("julian_date")
            as_float = NasaNeoService._coerce_number(value)
            return {
                "jd": as_float,
                "time_scale": epoch_section.get("time_scale"),
                "calendar_date": epoch_section.get("calendar_date"),
            }

        as_float = NasaNeoService._coerce_number(epoch_section)
        return {
            "jd": as_float,
            "time_scale": None,
            "calendar_date": None,
        }

    def _extract_simulation_elements(self, elements: Dict[str, Any]) -> Tuple[Optional[Dict[str, float]], List[str]]:
        required_keys = {
            "a": "a",
            "e": "e",
            "i": "i",
            "w": "omega",
            "om": "Omega",
            "ma": "M0",
        }

        missing = [original for original, mapped in required_keys.items() if elements.get(original) is None]

        if missing:
            return None, missing

        semi_major_axis_km = float(elements["a"]) * AU_IN_KM

        simulation_elements = {
            "a": semi_major_axis_km,
            "e": float(elements["e"]),
            "i": float(elements["i"]),
            "omega": float(elements["w"]),
            "Omega": float(elements["om"]),
            "M0": float(elements["ma"]),
        }

        return simulation_elements, []


__all__ = ["NasaNeoService", "NeoLookupResult"]
