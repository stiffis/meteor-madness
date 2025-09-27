#!/usr/bin/env python3
"""
Simulación de Órbita de Dos Elementos
Basado en: https://nasa.github.io/mission-viz/RMarkdown/Elliptical_Orbit_Design.html

Implementa las ecuaciones de Kepler para simular órbitas elípticas
y visualizar el movimiento orbital de dos cuerpos.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from typing import Tuple, List, Dict
import argparse


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


class OrbitalSimulation:
    """Simulador de órbitas elípticas"""
    
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
            'times': times,
            'body': np.array(body_positions)
        }


class OrbitalVisualizer:
    """Visualizador de órbitas en 3D"""
    
    def __init__(self, simulation_data: Dict):
        self.data = simulation_data
        
    def plot_orbits_3d(self, show_animation: bool = False):
        """Visualiza la órbita en 3D"""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Datos de la trayectoria
        body_pos = self.data['body']
        
        # Plotear la trayectoria completa
        ax.plot(body_pos[:, 0], body_pos[:, 1], body_pos[:, 2], 
               'b-', label='Satélite', alpha=0.8, linewidth=2)
        
        # Marcar posición inicial
        ax.scatter(body_pos[0, 0], body_pos[0, 1], body_pos[0, 2], 
                  c='blue', s=150, marker='o', label='Posición Inicial')
        
        # Marcar posición actual (final)
        ax.scatter(body_pos[-1, 0], body_pos[-1, 1], body_pos[-1, 2], 
                  c='red', s=150, marker='s', label='Posición Final')
        
        # Marcar el centro (foco)
        ax.scatter([0], [0], [0], c='gold', s=300, marker='*', 
                  label='Centro Gravitacional', edgecolors='orange')
        
        # Configurar ejes
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')
        ax.set_title('Simulación de Órbita Elíptica')
        ax.legend()
        
        # Hacer los ejes proporcionales
        max_range = np.max(np.abs(body_pos))
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range/2, max_range/2])
        
        plt.tight_layout()
        
        if show_animation:
            print("🎬 Iniciando animación... (Presiona Ctrl+C para detener)")
            self._create_animation(fig, ax)
        
        plt.show()
    
    def _create_animation(self, fig, ax):
        """Crea una animación del movimiento orbital"""
        body_pos = self.data['body']
        
        # Punto para la animación
        point, = ax.plot([], [], [], 'ro', markersize=10, label='Satélite')
        
        def animate(frame):
            if frame < len(body_pos):
                point.set_data([body_pos[frame, 0]], [body_pos[frame, 1]])
                point.set_3d_properties([body_pos[frame, 2]])
            
            return point,
        
        anim = FuncAnimation(fig, animate, frames=len(body_pos), 
                           interval=33, blit=False, repeat=True)  # ~30 FPS
        return anim
    
    def plot_orbital_elements_evolution(self):
        """Plotea la evolución de algunos parámetros orbitales"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        times = self.data['times'] / 3600  # Convertir a horas
        body_pos = self.data['body']
        
        # Calcular distancias al centro
        body_distances = np.sqrt(np.sum(body_pos**2, axis=1))
        
        # Distancia al centro vs tiempo
        ax1.plot(times, body_distances, 'b-', label='Satélite', linewidth=2)
        ax1.set_xlabel('Tiempo (horas)')
        ax1.set_ylabel('Distancia al Centro (km)')
        ax1.set_title('Evolución de la Distancia Radial')
        ax1.legend()
        ax1.grid(True)
        
        # Velocidad orbital (aproximada)
        dt = times[1] - times[0] if len(times) > 1 else 1
        body_velocities = np.sqrt(np.sum(np.diff(body_pos, axis=0)**2, axis=1)) / (dt * 3600)
        
        ax2.plot(times[1:], body_velocities, 'b-', label='Satélite', linewidth=2)
        ax2.set_xlabel('Tiempo (horas)')
        ax2.set_ylabel('Velocidad (km/s)')
        ax2.set_title('Velocidad Orbital')
        ax2.legend()
        ax2.grid(True)
        
        # Proyecciones XY
        ax3.plot(body_pos[:, 0], body_pos[:, 1], 'b-', label='Satélite', alpha=0.8, linewidth=2)
        ax3.scatter(body_pos[0, 0], body_pos[0, 1], c='blue', s=100, marker='o', label='Inicio')
        ax3.scatter(body_pos[-1, 0], body_pos[-1, 1], c='red', s=100, marker='s', label='Final')
        ax3.scatter([0], [0], c='gold', s=200, marker='*', label='Centro', edgecolors='orange')
        ax3.set_xlabel('X (km)')
        ax3.set_ylabel('Y (km)')
        ax3.set_title('Proyección en el Plano XY')
        ax3.legend()
        ax3.grid(True)
        ax3.axis('equal')
        
        # Altitud vs tiempo (altura sobre la superficie terrestre)
        altitude = body_distances - 6371  # Restamos el radio terrestre
        ax4.plot(times, altitude, 'g-', linewidth=2)
        ax4.set_xlabel('Tiempo (horas)')
        ax4.set_ylabel('Altitud (km)')
        ax4.set_title('Altitud sobre la Superficie Terrestre')
        ax4.grid(True)
        
        plt.tight_layout()
        plt.show()


def main():
    """Función principal para ejecutar la simulación"""
    parser = argparse.ArgumentParser(description='Simulador de Órbitas Elípticas')
    parser.add_argument('--duration', type=float, default=7200, 
                       help='Duración de la simulación en segundos (default: 2 horas)')
    parser.add_argument('--timestep', type=float, default=60, 
                       help='Paso de tiempo en segundos (default: 60s)')
    parser.add_argument('--animate', action='store_true', 
                       help='Mostrar animación del movimiento')
    
    args = parser.parse_args()
    
    print("🚀 Iniciando Simulación de Órbita Elíptica")
    print("=" * 45)
    
    # Definir elementos orbitales para el satélite
    # Órbita tipo ISS con algo de excentricidad
    body_elements = OrbitalElements(
        a=7000,      # Semi-eje mayor (km)
        e=0.2,       # Excentricidad moderada
        i=28.5,      # Inclinación (grados) - similar a la ISS
        omega=0,     # Argumento del periapsis (grados)
        Omega=0,     # Longitud del nodo ascendente (grados)
        M0=0         # Anomalía media inicial (grados)
    )
    
    print(f"Satélite - Órbita: a={body_elements.a}km, e={body_elements.e}, i={math.degrees(body_elements.i):.1f}°")
    print(f"Período orbital: {body_elements.T/3600:.2f} horas")
    print(f"Altitud periapsis: {body_elements.a*(1-body_elements.e)-6371:.0f} km")
    print(f"Altitud apoapsis: {body_elements.a*(1+body_elements.e)-6371:.0f} km")
    print()
    
    # Crear simulación
    simulation = OrbitalSimulation(body_elements)
    
    print(f"Simulando durante {args.duration/3600:.2f} horas con pasos de {args.timestep}s...")
    
    # Ejecutar simulación
    results = simulation.simulate(args.duration, args.timestep)
    
    print("✅ Simulación completada!")
    print(f"Puntos calculados: {len(results['times'])}")
    print()
    
    # Crear visualización
    visualizer = OrbitalVisualizer(results)
    
    print("📊 Generando visualizaciones...")
    
    # Mostrar órbitas en 3D
    visualizer.plot_orbits_3d(show_animation=args.animate)
    
    # Mostrar evolución de parámetros orbitales
    visualizer.plot_orbital_elements_evolution()
    
    print("🎯 Visualización completada!")


if __name__ == "__main__":
    main()