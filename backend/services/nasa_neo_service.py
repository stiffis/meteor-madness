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


@dataclass
class NeoSearchResult:
    """Salida de la búsqueda de objetos NEO."""

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

    def search_objects(self, query: str, limit: int = 10) -> NeoSearchResult:
        """Busca objetos NEO usando el endpoint genérico sbdb.api."""

        sanitized = (query or "").strip()
        if not sanitized:
            return NeoSearchResult(
                success=False,
                status_code=400,
                error="Query parameter 'q' is required",
            )

        safe_limit = max(1, min(int(limit), 25)) if isinstance(limit, (int, float)) else 10

        search_term = sanitized
        if "*" not in search_term:
            search_term = f"*{search_term}*"

        params = {
            "sstr": search_term,
            "neo": "1",
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            return NeoSearchResult(
                success=False,
                status_code=503,
                error=f"Failed to contact NASA SBDB service: {exc}",
            )

        payload = self._safe_json(response)

        if response.status_code == 404:
            return NeoSearchResult(
                success=True,
                status_code=200,
                data={"count": 0, "results": []},
            )

        if response.status_code not in (200, 300):
            return NeoSearchResult(
                success=False,
                status_code=response.status_code,
                error=payload.get("message") or f"NASA SBDB responded with status {response.status_code}",
            )

        if "object" in payload:
            processed = self._build_response(payload)
            object_info = processed.get("object", {})
            if not self._coerce_bool(object_info.get("neo")):
                return NeoSearchResult(
                    success=True,
                    status_code=200,
                    data={"count": 0, "results": []},
                )

            entry = self._search_entry_from_processed(processed)
            return NeoSearchResult(
                success=True,
                status_code=200,
                data={"count": 1, "results": [entry]},
            )

        matches = payload.get("list", [])
        if matches:
            results = []
            for item in matches[:safe_limit]:
                designation = item.get("pdes")
                entry = {
                    "designation": designation,
                    "full_name": item.get("name"),
                    "moid_au": self._coerce_number(item.get("moid")),
                    "orbit_class": item.get("class"),
                }

                detail = self.fetch_object(designation) if designation else None
                if detail and detail.success and detail.data:
                    entry.update(self._search_entry_from_processed(detail.data))
                else:
                    entry["pha"] = None
                    entry["absolute_magnitude_h"] = None

                results.append(entry)

            return NeoSearchResult(
                success=True,
                status_code=200,
                data={
                    "count": payload.get("count", len(matches)),
                    "results": results,
                },
            )

        if payload.get("message"):
            return NeoSearchResult(
                success=False,
                status_code=400,
                error=payload.get("message"),
            )

        return NeoSearchResult(
            success=False,
            status_code=500,
            error="Unexpected response from NASA SBDB",
        )

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
                "spkid": object_info.get("spkid"),
            },
            "orbit": {
                "epoch": self._normalize_epoch(orbit_section.get("epoch")),
                "elements": elements_dict,
                "residuals": orbit_section.get("residuals"),
                "moid": self._coerce_number(orbit_section.get("moid")),
                "moid_jup": self._coerce_number(orbit_section.get("moid_jup")),
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
    def _coerce_bool(value: Any) -> Optional[bool]:
        if value in (None, "", "null"):
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return bool(value)

        value_str = str(value).strip().lower()
        if value_str in {"y", "yes", "true", "1"}:
            return True
        if value_str in {"n", "no", "false", "0"}:
            return False
        return None

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
            "mu": 1.32712440018e11,  # Constante gravitacional solar (km^3/s^2)
        }

        return simulation_elements, []

    @staticmethod
    def _safe_json(response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
            return data if isinstance(data, dict) else {}
        except ValueError:
            return {}

    def _search_entry_from_processed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        object_info = data.get("object", {}) or {}
        orbit_info = data.get("orbit", {}) or {}
        physical_info = data.get("physical") or {}

        if isinstance(physical_info, dict):
            absolute_magnitude = physical_info.get("H")
        else:
            absolute_magnitude = None

        entry = {
            "designation": object_info.get("designation"),
            "full_name": object_info.get("full_name") or object_info.get("designation"),
            "spkid": object_info.get("spkid"),
            "neo": self._coerce_bool(object_info.get("neo")),
            "pha": self._coerce_bool(object_info.get("pha")),
            "absolute_magnitude_h": self._coerce_number(absolute_magnitude),
            "orbit_class": object_info.get("orbit_class"),
            "moid_au": self._coerce_number(orbit_info.get("moid")),
        }

        return entry


__all__ = ["NasaNeoService", "NeoLookupResult", "NeoSearchResult"]
