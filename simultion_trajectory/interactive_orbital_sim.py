#!/usr/bin/env python3
"""
Interfaz Interactiva para la Simulación Orbital
Permite modificar parámetros orbitales en tiempo real
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
import math
from orbital_simulation import OrbitalElements, OrbitalSimulation, OrbitalVisualizer


class InteractiveOrbitalSimulation:
    """Simulador orbital interactivo con controles deslizantes"""
    
    def __init__(self):
        # Parámetros iniciales
        self.initial_params = {
            'a': 7000, 'e': 0.2, 'i': 28.5, 'omega': 0, 'Omega': 0, 'M0': 0
        }
        
        self.duration = 7200  # 2 horas
        self.timestep = 60    # 1 minuto
        
        # Variables para la animación
        self.animation = None
        self.is_playing = False
        self.current_frame = 0
        self.animation_speed = 30  # frames por segundo
        
        # Datos de la simulación actual
        self.current_results = None
        self.current_elements = None
        
        self.setup_interactive_plot()
    
    def setup_interactive_plot(self):
        """Configura la interfaz interactiva"""
        # Crear figura principal
        self.fig = plt.figure(figsize=(14, 10))
        
        # Solo subplot para la órbita 3D (ocupa toda la parte superior)
        self.ax_3d = self.fig.add_subplot(111, projection='3d')
        
        # Espacio para los controles deslizantes
        plt.subplots_adjust(bottom=0.4)
        
        self.create_sliders()
        self.create_buttons()
        
        # Simulación inicial
        self.update_simulation()
        
        # Conectar eventos
        for slider in self.sliders.values():
            slider.on_changed(self.on_slider_change)
        
        self.reset_button.on_clicked(self.reset_parameters)
        self.preset_iss_button.on_clicked(self.load_preset_iss)
        self.preset_crash_button.on_clicked(self.load_preset_crash)
        self.play_button.on_clicked(self.start_animation)
        self.pause_button.on_clicked(self.pause_animation)
        self.reset_anim_button.on_clicked(self.reset_animation)
        self.speed_slider.on_changed(self.change_speed)
    
    def create_sliders(self):
        """Crea los controles deslizantes para los parámetros orbitales"""
        self.sliders = {}
        
        # Definir posiciones y rangos de los sliders
        slider_configs = [
            ('a', 'Semi-eje mayor (km)', 6000, 20000, self.initial_params['a']),
            ('e', 'Excentricidad', 0.0, 0.8, self.initial_params['e']),
            ('i', 'Inclinación (°)', 0, 90, self.initial_params['i']),
            ('omega', 'Arg. Periapsis (°)', 0, 360, self.initial_params['omega']),
            ('Omega', 'Long. Nodo Asc. (°)', 0, 360, self.initial_params['Omega']),
            ('M0', 'Anomalía Media (°)', 0, 360, self.initial_params['M0']),
        ]
        
        # Crear sliders en dos columnas para usar mejor el espacio
        for i, (param, label, min_val, max_val, init_val) in enumerate(slider_configs):
            row = i % 3  # 3 sliders por columna
            col = i // 3
            
            ax_slider = plt.axes([0.1 + col * 0.4, 0.32 - row * 0.06, 0.3, 0.03])
            
            self.sliders[param] = Slider(
                ax_slider, label, min_val, max_val, 
                valinit=init_val, valfmt='%.1f'
            )
    
    def create_buttons(self):
        """Crea botones de control"""
        # Botón de reset
        ax_reset = plt.axes([0.1, 0.02, 0.1, 0.04])
        self.reset_button = Button(ax_reset, 'Reset')
        
        # Botón de preset ISS
        ax_preset_iss = plt.axes([0.22, 0.02, 0.08, 0.04])
        self.preset_iss_button = Button(ax_preset_iss, 'ISS')
        
        # Botón de preset CRASH
        ax_preset_crash = plt.axes([0.31, 0.02, 0.08, 0.04])
        self.preset_crash_button = Button(ax_preset_crash, 'CRASH')
        
        # Botón de Play
        ax_play = plt.axes([0.40, 0.02, 0.06, 0.04])
        self.play_button = Button(ax_play, 'Play')
        
        # Botón de Pause
        ax_pause = plt.axes([0.47, 0.02, 0.06, 0.04])
        self.pause_button = Button(ax_pause, 'Pause')
        
        # Botón de Reset animación
        ax_reset_anim = plt.axes([0.54, 0.02, 0.06, 0.04])
        self.reset_anim_button = Button(ax_reset_anim, 'Reset')
        
        # Slider de velocidad de animación
        ax_speed = plt.axes([0.65, 0.02, 0.25, 0.02])
        self.speed_slider = Slider(ax_speed, 'Velocidad', 1, 60, valinit=30, valfmt='%.0f FPS')
    
    def on_slider_change(self, val):
        """Callback cuando cambia un slider"""
        self.update_simulation()
    
    def reset_parameters(self, event):
        """Resetea todos los parámetros a valores iniciales"""
        for param, slider in self.sliders.items():
            slider.reset()
    
    def load_preset_iss(self, event):
        """Carga un preset con órbita ISS"""
        # Preset: ISS real
        presets = {
            'a': 6778, 'e': 0.0003, 'i': 51.6, 'omega': 0, 'Omega': 0, 'M0': 0  # ISS
        }
        
        for param, value in presets.items():
            self.sliders[param].set_val(value)
    
    def load_preset_crash(self, event):
        """Carga un preset que chocará con la Tierra"""
        # Preset: Órbita de impacto - perigeo muy bajo que atraviesa la superficie terrestre
        presets = {
            'a': 6000,    # Semi-eje mayor pequeño (menor que el radio terrestre!)
            'e': 0.6,     # Alta excentricidad
            'i': 45,      # Inclinación moderada
            'omega': 0,   # Argumento del periapsis
            'Omega': 0,   # Longitud del nodo ascendente
            'M0': 0       # Anomalía media inicial
        }
        
        for param, value in presets.items():
            self.sliders[param].set_val(value)
    
    def get_current_parameters(self):
        """Obtiene los parámetros actuales de los sliders"""
        return {param: slider.val for param, slider in self.sliders.items()}
    
    def update_simulation(self):
        """Actualiza la simulación con los parámetros actuales"""
        params = self.get_current_parameters()
        
        # Crear elementos orbitales
        body_elements = OrbitalElements(
            a=params['a'],
            e=params['e'],
            i=params['i'],
            omega=params['omega'],
            Omega=params['Omega'],
            M0=params['M0']
        )
        
        # Ejecutar simulación
        simulation = OrbitalSimulation(body_elements)
        results = simulation.simulate(self.duration, self.timestep)
        
        # Guardar datos actuales
        self.current_results = results
        self.current_elements = body_elements
        
        # Actualizar gráficos
        self.update_plots(results, body_elements)
    
    def update_plots(self, results, body_elements):
        """Actualiza el gráfico 3D"""
        # Limpiar eje 3D
        self.ax_3d.clear()
        
        times = results['times'] / 3600  # Convertir a horas
        body_pos = results['body']
        
        # Detectar puntos de impacto con la Tierra (radio = 6371 km)
        distances = np.sqrt(np.sum(body_pos**2, axis=1))
        impact_indices = np.where(distances <= 6371)[0]
        
        # Encontrar el primer impacto
        first_impact = impact_indices[0] if len(impact_indices) > 0 else None
        
        # Gráfico 3D - solo si no hay impacto (si hay impacto se dibuja arriba)
        if first_impact is None:
            self.ax_3d.plot(body_pos[:, 0], body_pos[:, 1], body_pos[:, 2], 
                           'b-', label='Satélite', alpha=0.8, linewidth=2)
        
        # Marcar posición inicial
        self.ax_3d.scatter(body_pos[0, 0], body_pos[0, 1], body_pos[0, 2], 
                          c='blue', s=120, marker='o', label='Inicio')
        
        # Marcar posición final o punto de impacto
        if first_impact is not None:
            # Marcar punto de impacto
            self.ax_3d.scatter(body_pos[first_impact, 0], body_pos[first_impact, 1], body_pos[first_impact, 2], 
                              c='red', s=200, marker='X', label='IMPACTO!', edgecolors='darkred', linewidth=2)
            # Solo mostrar órbita hasta el impacto
            self.ax_3d.plot(body_pos[:first_impact+1, 0], body_pos[:first_impact+1, 1], body_pos[:first_impact+1, 2], 
                           'r-', alpha=0.8, linewidth=3, label='Trayectoria de Impacto')
        else:
            # Marcar posición actual (final)
            self.ax_3d.scatter(body_pos[-1, 0], body_pos[-1, 1], body_pos[-1, 2], 
                              c='red', s=120, marker='s', label='Actual')
        
        # Dibujar la Tierra como una esfera
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        earth_radius = 6371
        x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
        y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
        z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax_3d.plot_surface(x_earth, y_earth, z_earth, alpha=0.3, color='blue', label='Tierra')
        
        # Centro gravitacional
        self.ax_3d.scatter([0], [0], [0], c='gold', s=250, marker='*', 
                          edgecolors='orange', label='Centro')
        
        # Configurar ejes 3D
        max_range = np.max(np.abs(body_pos))
        self.ax_3d.set_xlim([-max_range, max_range])
        self.ax_3d.set_ylim([-max_range, max_range])
        self.ax_3d.set_zlim([-max_range/2, max_range/2])
        self.ax_3d.set_xlabel('X (km)')
        self.ax_3d.set_ylabel('Y (km)')
        self.ax_3d.set_zlabel('Z (km)')
        
        # Título con información orbital
        altitude_perigee = body_elements.a*(1-body_elements.e) - 6371
        altitude_apogee = body_elements.a*(1+body_elements.e) - 6371
        will_impact = altitude_perigee < 0
        
        if will_impact:
            impact_depth = abs(altitude_perigee)
            title = f'⚠️ ÓRBITA DE IMPACTO - Perigeo: {impact_depth:.0f}km BAJO superficie | Período: {body_elements.T/3600:.2f}h'
            self.ax_3d.set_title(title, color='red', fontsize=12, weight='bold')
        else:
            title = f'Órbita Estable - Perigeo: {altitude_perigee:.0f}km | Apogeo: {altitude_apogee:.0f}km | Período: {body_elements.T/3600:.2f}h'
            self.ax_3d.set_title(title, color='blue', fontsize=12)
        
        self.ax_3d.legend(loc='upper right')
        
        # Actualizar gráficos
        self.fig.canvas.draw()
    
    def start_animation(self, event):
        """Inicia la animación del satélite"""
        if self.current_results is None:
            return
            
        if not self.is_playing:
            self.is_playing = True
            
            # Crear la animación si no existe
            if self.animation is None:
                fps = int(self.speed_slider.val)
                interval = max(1, int(1000 / fps))
                self.animation = FuncAnimation(
                    self.fig, self.animate_satellite, 
                    frames=len(self.current_results['times']),
                    interval=interval,
                    repeat=True,
                    blit=False
                )
            else:
                # Reanudar la animación
                self.animation.resume()
    
    def pause_animation(self, event):
        """Pausa la animación del satélite"""
        if self.animation is not None and self.is_playing:
            self.is_playing = False
            self.animation.pause()
    
    def reset_animation(self, event):
        """Reinicia la animación desde el principio"""
        if self.animation is not None:
            self.animation.pause()
        self.is_playing = False
        self.current_frame = 0
        
        # Actualizar gráficos al estado inicial
        if self.current_results is not None:
            self.animate_satellite(0)
    
    def change_speed(self, val):
        """Cambia la velocidad de la animación"""
        new_fps = int(val)
        new_interval = max(1, int(1000 / new_fps))  # ms entre frames
        
        if self.animation is not None:
            # Pausar la animación actual
            was_playing = self.is_playing
            if was_playing:
                self.animation.pause()
            
            # Crear nueva animación con la nueva velocidad
            self.animation = FuncAnimation(
                self.fig, self.animate_satellite, 
                frames=len(self.current_results['times']) if self.current_results else 100,
                interval=new_interval,
                repeat=True,
                blit=False
            )
            
            # Reanudar si estaba reproduciéndose
            if was_playing:
                self.is_playing = True
                # No necesitamos llamar resume() aquí, la nueva animación ya está corriendo
    
    def animate_satellite(self, frame):
        """Función de animación que actualiza la posición del satélite"""
        if self.current_results is None:
            return
        
        self.current_frame = frame
        body_pos = self.current_results['body']
        
        # Limpiar solo el gráfico 3D y mantener las trayectorias
        self.ax_3d.clear()
        
        # Redibujar la órbita completa
        self.ax_3d.plot(body_pos[:, 0], body_pos[:, 1], body_pos[:, 2], 
                       'b-', label='Órbita', alpha=0.3, linewidth=1)
        
        # Dibujar la trayectoria hasta el punto actual
        self.ax_3d.plot(body_pos[:frame+1, 0], body_pos[:frame+1, 1], body_pos[:frame+1, 2], 
                       'b-', alpha=0.8, linewidth=2)
        
        # Detectar si el frame actual está en impacto
        current_distance = np.sqrt(np.sum(body_pos[frame]**2))
        is_impacting = current_distance <= 6371
        
        # Posición actual del satélite (animada)
        if is_impacting:
            # Satélite impactando - mostrar como explosión
            self.ax_3d.scatter(body_pos[frame, 0], body_pos[frame, 1], body_pos[frame, 2], 
                              c='red', s=300, marker='*', label='IMPACTO!', edgecolors='darkred', linewidth=3)
        else:
            self.ax_3d.scatter(body_pos[frame, 0], body_pos[frame, 1], body_pos[frame, 2], 
                              c='red', s=150, marker='o', label='Satélite')
        
        # Posición inicial
        self.ax_3d.scatter(body_pos[0, 0], body_pos[0, 1], body_pos[0, 2], 
                          c='blue', s=100, marker='o', alpha=0.6, label='Inicio')
        
        # Centro gravitacional (Tierra)
        self.ax_3d.scatter([0], [0], [0], c='gold', s=250, marker='*', 
                          edgecolors='orange', label='Tierra')
        
        # Configurar ejes 3D
        max_range = np.max(np.abs(body_pos))
        self.ax_3d.set_xlim([-max_range, max_range])
        self.ax_3d.set_ylim([-max_range, max_range])
        self.ax_3d.set_zlim([-max_range/2, max_range/2])
        self.ax_3d.set_xlabel('X (km)')
        self.ax_3d.set_ylabel('Y (km)')
        self.ax_3d.set_zlabel('Z (km)')
        self.ax_3d.set_title(f'Órbita 3D - Tiempo: {self.current_results["times"][frame]/3600:.2f}h')
        self.ax_3d.legend()
        
        # Solo actualizar el título con el tiempo actual
        if self.current_elements:
            altitude_perigee = self.current_elements.a*(1-self.current_elements.e) - 6371
            will_impact = altitude_perigee < 0
            
            time_str = f' - Tiempo: {self.current_results["times"][frame]/3600:.2f}h'
            
            if will_impact:
                impact_depth = abs(altitude_perigee)
                title = f'⚠️ ÓRBITA DE IMPACTO - Perigeo: {impact_depth:.0f}km BAJO superficie{time_str}'
                self.ax_3d.set_title(title, color='red', fontsize=12, weight='bold')
            else:
                altitude_apogee = self.current_elements.a*(1+self.current_elements.e) - 6371
                title = f'Órbita Estable - Perigeo: {altitude_perigee:.0f}km | Apogeo: {altitude_apogee:.0f}km{time_str}'
                self.ax_3d.set_title(title, color='blue', fontsize=12)
        
        return []
    
    def show(self):
        """Muestra la interfaz interactiva"""
        plt.show()


def main():
    """Función principal para la interfaz interactiva"""
    print("🎮 Iniciando Simulador Orbital Interactivo")
    print("=" * 50)
    print("Controles:")
    print("- Usa los deslizadores para modificar los parámetros orbitales")
    print("- 'Reset': Vuelve a los valores iniciales")
    print("- 'ISS': Carga la órbita real de la ISS")
    print("- 'CRASH': Carga una órbita que CHOCARÁ con la Tierra! ⚠️")
    print("- 'Play': Inicia la animación del satélite orbitando")
    print("- 'Pause': Pausa la animación")
    print("- 'Reset' (animación): Reinicia la animación desde el principio")
    print("- 'Velocidad': Ajusta los FPS de la animación (1-60 FPS)")
    print("- Los gráficos se actualizan automáticamente")
    print()
    
    # Crear y mostrar la interfaz interactiva
    interactive_sim = InteractiveOrbitalSimulation()
    interactive_sim.show()


if __name__ == "__main__":
    main()