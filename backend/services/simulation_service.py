"""
Servicio de simulación orbital
Integra la lógica de simulación existente para uso en API
"""

import numpy as np
import math
from typing import Dict, List, Any, Tuple
from models.orbital_elements import OrbitalElements


class OrbitalSimulation:
    """Simulador de órbitas elípticas adaptado para API"""
    
    def __init__(self, body_elements: OrbitalElements):
        self.body = body_elements
        
    def solve_kepler_equation(self, M: float, e: float, tolerance: float = 1e-8) -> float:
        """
        Resuelve la ecuación de Kepler: M = E - e*sin(E)
        usando el método de Newton-Raphson
        """
        E = M  # Aproximación inicial
        
        for _ in range(50):  # Máximo 50 iteraciones
            f = E - e * math.sin(E) - M
            df = 1 - e * math.cos(E)
            
            E_new = E - f / df
            
            if abs(E_new - E) < tolerance:
                return E_new
            
            E = E_new
        
        return E
    
    def mean_to_true_anomaly(self, M: float, e: float) -> float:
        """Convierte anomalía media a anomalía verdadera"""
        E = self.solve_kepler_equation(M, e)  # Anomalía excéntrica
        
        # Anomalía verdadera
        nu = 2 * math.atan2(
            math.sqrt(1 + e) * math.sin(E/2),
            math.sqrt(1 - e) * math.cos(E/2)
        )
        
        return nu
    
    def orbital_to_cartesian(self, elements: OrbitalElements, t: float) -> Tuple[float, float, float]:
        """
        Convierte elementos orbitales a coordenadas cartesianas
        en el tiempo t (segundos)
        """
        # Anomalía media en el tiempo t
        M = elements.M0 + elements.n * t
        
        # Anomalía verdadera
        nu = self.mean_to_true_anomaly(M, elements.e)
        
        # Radio orbital
        r = elements.a * (1 - elements.e**2) / (1 + elements.e * math.cos(nu))
        
        # Coordenadas en el plano orbital
        x_orbital = r * math.cos(nu)
        y_orbital = r * math.sin(nu)
        z_orbital = 0
        
        # Matrices de rotación para transformar al sistema inercial
        # Rotación por argumento del periapsis
        cos_omega = math.cos(elements.omega)
        sin_omega = math.sin(elements.omega)
        
        # Rotación por inclinación
        cos_i = math.cos(elements.i)
        sin_i = math.sin(elements.i)
        
        # Rotación por longitud del nodo ascendente
        cos_Omega = math.cos(elements.Omega)
        sin_Omega = math.sin(elements.Omega)
        
        # Aplicar rotaciones
        x1 = x_orbital * cos_omega - y_orbital * sin_omega
        y1 = x_orbital * sin_omega + y_orbital * cos_omega
        z1 = z_orbital
        
        x2 = x1
        y2 = y1 * cos_i - z1 * sin_i
        z2 = y1 * sin_i + z1 * cos_i
        
        x = x2 * cos_Omega - y2 * sin_Omega
        y = x2 * sin_Omega + y2 * cos_Omega
        z = z2
        
        return x, y, z
    
    def simulate(self, duration: float, time_step: float) -> Dict:
        """
        Simula la órbita durante un período de tiempo dado
        
        Args:
            duration: Duración de la simulación en segundos
            time_step: Paso de tiempo en segundos
        
        Returns:
            Diccionario con la trayectoria del cuerpo
        """
        times = np.arange(0, duration, time_step)
        
        body_positions = []
        
        for t in times:
            # Calcular posición
            pos = self.orbital_to_cartesian(self.body, t)
            body_positions.append(pos)
        
        return {
            'times': times.tolist(),  # Convertir a lista para JSON
            'positions': np.array(body_positions).tolist()  # Convertir a lista para JSON
        }


class SimulationService:
    """Servicio principal para ejecutar simulaciones orbitales"""
    
    def __init__(self):
        self.earth_radius = 6371  # km
    
    def run_simulation(self, elements_dict: Dict[str, float], 
                      duration: float, timestep: float) -> Dict[str, Any]:
        """
        Ejecuta una simulación orbital completa
        
        Args:
            elements_dict: Diccionario con elementos orbitales
            duration: Duración en segundos
            timestep: Paso de tiempo en segundos
            
        Returns:
            Resultado de la simulación con datos y metadatos
        """
        try:
            # Crear elementos orbitales
            elements = OrbitalElements.from_dict(elements_dict)
            
            # Crear simulador
            simulation = OrbitalSimulation(elements)
            
            # Ejecutar simulación
            raw_results = simulation.simulate(duration, timestep)
            
            # Procesar resultados para incluir análisis adicional
            processed_results = self._process_simulation_results(
                raw_results, elements
            )
            
            return {
                "success": True,
                "data": processed_results,
                "total_points": len(raw_results['times']),
                "orbital_period": elements.T
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _process_simulation_results(self, raw_results: Dict, 
                                  elements: OrbitalElements) -> Dict[str, Any]:
        """
        Procesa los resultados de la simulación para añadir análisis
        
        Args:
            raw_results: Resultados crudos de la simulación
            elements: Elementos orbitales usados
            
        Returns:
            Resultados procesados con análisis adicional
        """
        positions = np.array(raw_results['positions'])
        times = np.array(raw_results['times'])
        
        # Calcular distancias al centro
        distances = np.sqrt(np.sum(positions**2, axis=1))
        
        # Calcular velocidades (aproximadas)
        if len(positions) > 1:
            dt = times[1] - times[0]  # segundos
            velocities = np.sqrt(np.sum(np.diff(positions, axis=0)**2, axis=1)) / dt
        else:
            velocities = [0]
        
        # Calcular altitudes (altura sobre superficie terrestre)
        altitudes = distances - self.earth_radius
        
        # Detectar puntos de impacto
        impact_points = np.where(distances <= self.earth_radius)[0]
        first_impact_index = impact_points[0] if len(impact_points) > 0 else None
        
        # Encontrar periapsis y apoapsis
        min_distance_idx = np.argmin(distances)
        max_distance_idx = np.argmax(distances)
        
        return {
            "trajectory": {
                "times": raw_results['times'],
                "positions": raw_results['positions'],
                "distances": distances.tolist(),
                "velocities": velocities.tolist() if len(velocities) > 1 else [],
                "altitudes": altitudes.tolist()
            },
            "analysis": {
                "min_altitude": float(np.min(altitudes)),
                "max_altitude": float(np.max(altitudes)),
                "min_distance": float(np.min(distances)),
                "max_distance": float(np.max(distances)),
                "avg_velocity": float(np.mean(velocities)) if len(velocities) > 1 else 0,
                "periapsis": {
                    "time": float(times[min_distance_idx]),
                    "position": positions[min_distance_idx].tolist(),
                    "distance": float(distances[min_distance_idx]),
                    "altitude": float(altitudes[min_distance_idx])
                },
                "apoapsis": {
                    "time": float(times[max_distance_idx]),
                    "position": positions[max_distance_idx].tolist(),
                    "distance": float(distances[max_distance_idx]),
                    "altitude": float(altitudes[max_distance_idx])
                },
                "impact": {
                    "will_impact": first_impact_index is not None,
                    "impact_time": float(times[first_impact_index]) if first_impact_index is not None else None,
                    "impact_position": positions[first_impact_index].tolist() if first_impact_index is not None else None,
                    "impact_index": int(first_impact_index) if first_impact_index is not None else None
                }
            },
            "orbital_info": elements.get_orbital_info()
        }