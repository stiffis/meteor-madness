"""Servicio para generar estados orbitales aproximados del sistema solar."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List
import math

AU_IN_KM = 149_597_870.7
SUN_RADIUS_KM = 695_700
J2000_EPOCH = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class PlanetElement:
    name: str
    color: str
    orbit_color: str
    radius_km: float
    semi_major_axis_au: float
    eccentricity: float
    inclination_deg: float
    longitude_of_ascending_node_deg: float
    argument_of_periapsis_deg: float
    mean_anomaly_deg: float
    orbital_period_days: float


PLANETARY_ELEMENTS: List[PlanetElement] = [
    PlanetElement('Mercurio', '#d0a169', '#ffb347', 2439.7, 0.38709927, 0.205630, 7.00487, 48.331, 29.124, 174.796, 87.969),
    PlanetElement('Venus', '#f5d36b', '#f9e27d', 6051.8, 0.72333566, 0.006773, 3.39471, 76.680, 54.884, 50.115, 224.701),
    PlanetElement('Tierra', '#6ba4ff', '#3fa9f5', 6371.0, 1.00000011, 0.016710, 0.00005, -11.26064, 114.20783, 358.617, 365.256),
    PlanetElement('Marte', '#ff6f5c', '#ff896b', 3389.5, 1.52371034, 0.093394, 1.850, 49.558, 286.502, 19.356, 686.980),
    PlanetElement('Júpiter', '#f7c492', '#f4a259', 69911.0, 5.20288700, 0.048386, 1.303, 100.464, 273.867, 20.020, 4332.589),
    PlanetElement('Saturno', '#f4deaa', '#f1c27d', 58232.0, 9.53667594, 0.054150, 2.485, 113.665, 339.392, 317.020, 10759.22),
    PlanetElement('Urano', '#9bdaf1', '#68c3d4', 25362.0, 19.18916464, 0.047167, 0.773, 74.006, 96.998, 142.2386, 30685.4),
    PlanetElement('Neptuno', '#4c6fff', '#5a63ff', 24622.0, 30.06992276, 0.008585, 1.770, 131.784, 273.188, 256.228, 60190.0),
]


class SolarSystemService:
    """Genera elementos orbitales actualizados a partir de una época base."""

    def __init__(self, reference_epoch: datetime = J2000_EPOCH) -> None:
        self.reference_epoch = reference_epoch

    def get_planet_states(self, moment: datetime | None = None) -> Dict[str, Any]:
        now = moment.astimezone(timezone.utc) if moment else datetime.now(timezone.utc)
        delta_seconds = (now - self.reference_epoch).total_seconds()

        planets = []
        for planet in PLANETARY_ELEMENTS:
            mean_motion = 2 * math.pi / (planet.orbital_period_days * 86400.0)
            mean_anomaly_rad = math.radians(planet.mean_anomaly_deg)
            mean_anomaly_now = (mean_anomaly_rad + mean_motion * delta_seconds) % (2 * math.pi)
            mean_anomaly_deg_now = math.degrees(mean_anomaly_now)

            planets.append({
                'name': planet.name,
                'color': planet.color,
                'orbitColor': planet.orbit_color,
                'radiusKm': planet.radius_km,
                'semiMajorAxisKm': planet.semi_major_axis_au * AU_IN_KM,
                'eccentricity': planet.eccentricity,
                'inclinationDeg': planet.inclination_deg,
                'longitudeOfAscendingNodeDeg': planet.longitude_of_ascending_node_deg,
                'argumentOfPeriapsisDeg': planet.argument_of_periapsis_deg,
                'meanAnomalyDeg': mean_anomaly_deg_now,
                'orbitalPeriodDays': planet.orbital_period_days,
            })

        return {
            'generatedAt': now.isoformat(),
            'referenceEpoch': self.reference_epoch.isoformat(),
            'sunRadiusKm': SUN_RADIUS_KM,
            'planets': planets,
        }


__all__ = ['SolarSystemService', 'SUN_RADIUS_KM']
