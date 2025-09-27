"""
Modelo de datos para elementos orbitales keplerianos
Adaptado de la simulación orbital existente
"""

import math
from typing import Dict, Any


class OrbitalElements:
    """Clase para manejar los elementos orbitales keplerianos"""
    
    def __init__(self, 
                 a: float,           # Semi-eje mayor (km)
                 e: float,           # Excentricidad
                 i: float,           # Inclinación (grados)
                 omega: float,       # Argumento del periapsis (grados)
                 Omega: float,       # Longitud del nodo ascendente (grados)
                 M0: float,          # Anomalía media en t=0 (grados)
                 mu: float = 3.986004418e5):  # Parámetro gravitacional estándar de la Tierra (km³/s²)
        
        self.a = a
        self.e = e
        self.i = math.radians(i)
        self.omega = math.radians(omega)
        self.Omega = math.radians(Omega)
        self.M0 = math.radians(M0)
        self.mu = mu
        
        # Calcular el movimiento medio (n)
        self.n = math.sqrt(mu / (a**3))  # rad/s
        
        # Periodo orbital
        self.T = 2 * math.pi / self.n  # segundos
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte los elementos orbitales a diccionario"""
        return {
            'a': self.a,
            'e': self.e,
            'i': math.degrees(self.i),
            'omega': math.degrees(self.omega),
            'Omega': math.degrees(self.Omega),
            'M0': math.degrees(self.M0),
            'mu': self.mu,
            'n': self.n,
            'T': self.T
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrbitalElements':
        """Crea elementos orbitales desde un diccionario"""
        return cls(
            a=data['a'],
            e=data['e'],
            i=data['i'],
            omega=data['omega'],
            Omega=data['Omega'],
            M0=data['M0'],
            mu=data.get('mu', 3.986004418e5)
        )
    
    def get_orbital_info(self) -> Dict[str, Any]:
        """Obtiene información calculada de la órbita"""
        # Radio terrestre
        earth_radius = 6371  # km
        
        # Calcular altitudes
        perigee_altitude = self.a * (1 - self.e) - earth_radius
        apogee_altitude = self.a * (1 + self.e) - earth_radius
        
        # Verificar si la órbita es válida (no choca con la Tierra)
        will_impact = perigee_altitude < 0
        
        return {
            'semi_major_axis': self.a,
            'eccentricity': self.e,
            'inclination': math.degrees(self.i),
            'argument_of_periapsis': math.degrees(self.omega),
            'longitude_of_ascending_node': math.degrees(self.Omega),
            'mean_anomaly_at_epoch': math.degrees(self.M0),
            'orbital_period_hours': self.T / 3600,
            'orbital_period_minutes': self.T / 60,
            'mean_motion': self.n,
            'perigee_altitude': perigee_altitude,
            'apogee_altitude': apogee_altitude,
            'will_impact_earth': will_impact,
            'impact_depth': abs(perigee_altitude) if will_impact else 0
        }