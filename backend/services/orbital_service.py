"""
Servicio para validación y cálculos de elementos orbitales
"""

from typing import Dict, List, Any
from models.orbital_elements import OrbitalElements


class OrbitalService:
    """Servicio para operaciones relacionadas con elementos orbitales"""
    
    def __init__(self):
        self.earth_radius = 6371  # km
        self.earth_mu = 3.986004418e5  # km³/s²
    
    def validate_orbital_elements(self, elements: Dict[str, float]) -> Dict[str, Any]:
        """
        Valida un diccionario de elementos orbitales
        
        Args:
            elements: Diccionario con elementos orbitales
            
        Returns:
            Dict con 'valid' (bool) y 'errors' (list) si hay errores
        """
        errors = []
        required_fields = ['a', 'e', 'i', 'omega', 'Omega', 'M0']
        
        # Verificar campos requeridos
        for field in required_fields:
            if field not in elements:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return {"valid": False, "errors": errors}
        
        # Validar rangos de valores
        a = elements['a']
        e = elements['e']
        i = elements['i']
        omega = elements['omega']
        Omega = elements['Omega']
        M0 = elements['M0']
        
        # Semi-eje mayor debe ser positivo y razonable
        if a <= 0:
            errors.append("Semi-major axis (a) must be positive")
        elif a < self.earth_radius:
            errors.append(f"Semi-major axis (a) must be greater than Earth radius ({self.earth_radius} km)")
        elif a > 1e9:  # Límite práctico para este simulador (~6.7 AU)
            errors.append("Semi-major axis (a) is too large (max 1e9 km)")
        
        # Excentricidad debe estar entre 0 y 1 (órbitas elípticas)
        if e < 0 or e >= 1:
            errors.append("Eccentricity (e) must be between 0 and 1 (exclusive)")
        
        # Inclinación debe estar entre 0 y 180 grados
        if i < 0 or i > 180:
            errors.append("Inclination (i) must be between 0 and 180 degrees")
        
        # Argumentos angulares deben estar entre 0 y 360 grados
        if omega < 0 or omega > 360:
            errors.append("Argument of periapsis (omega) must be between 0 and 360 degrees")
        
        if Omega < 0 or Omega > 360:
            errors.append("Longitude of ascending node (Omega) must be between 0 and 360 degrees")
        
        if M0 < 0 or M0 > 360:
            errors.append("Mean anomaly at epoch (M0) must be between 0 and 360 degrees")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def calculate_orbital_info(self, elements: Dict[str, float]) -> Dict[str, Any]:
        """
        Calcula información adicional de una órbita
        
        Args:
            elements: Elementos orbitales validados
            
        Returns:
            Información calculada de la órbita
        """
        orbital_elements = OrbitalElements.from_dict(elements)
        return orbital_elements.get_orbital_info()
    
    def get_orbital_presets(self) -> Dict[str, Any]:
        """
        Obtiene presets predefinidos de órbitas famosas
        
        Returns:
            Diccionario con presets de órbitas
        """
        return {
            "default": {
                "name": "Órbita por Defecto",
                "description": "Órbita LEO con excentricidad moderada",
                "elements": {
                    "a": 7000,
                    "e": 0.2,
                    "i": 28.5,
                    "omega": 0,
                    "Omega": 0,
                    "M0": 0
                }
            },
            "iss": {
                "name": "Estación Espacial Internacional",
                "description": "Órbita real de la ISS",
                "elements": {
                    "a": 6778,
                    "e": 0.0003,
                    "i": 51.6,
                    "omega": 0,
                    "Omega": 0,
                    "M0": 0
                }
            },
            "geostationary": {
                "name": "Órbita Geostacionaria",
                "description": "Satélite geoestacionario sobre el ecuador",
                "elements": {
                    "a": 42164,
                    "e": 0.0,
                    "i": 0,
                    "omega": 0,
                    "Omega": 0,
                    "M0": 0
                }
            },
            "molniya": {
                "name": "Órbita Molniya",
                "description": "Órbita elíptica de comunicaciones rusas",
                "elements": {
                    "a": 26600,
                    "e": 0.74,
                    "i": 63.4,
                    "omega": 270,
                    "Omega": 0,
                    "M0": 0
                }
            },
            "polar": {
                "name": "Órbita Polar",
                "description": "Órbita polar de observación terrestre",
                "elements": {
                    "a": 8000,
                    "e": 0.1,
                    "i": 90,
                    "omega": 0,
                    "Omega": 0,
                    "M0": 0
                }
            },
            "crash": {
                "name": "Órbita de Impacto (Educativa)",
                "description": "⚠️ Órbita que impactará con la Tierra",
                "elements": {
                    "a": 6000,
                    "e": 0.6,
                    "i": 45,
                    "omega": 0,
                    "Omega": 0,
                    "M0": 0
                },
                "warning": "Esta órbita resultará en impacto con la superficie terrestre"
            }
        }
