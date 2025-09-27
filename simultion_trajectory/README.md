# Simulación de Órbita Elíptica

Esta simulación implementa las ecuaciones de Kepler para modelar y visualizar órbitas elípticas de un satélite, basándose en la documentación de la NASA sobre diseño de órbitas elípticas.

## 🚀 Características

- **Simulación precisa**: Implementa las ecuaciones de Kepler con el método de Newton-Raphson
- **Elementos orbitales completos**: Semi-eje mayor, excentricidad, inclinación, argumentos de periapsis y nodo ascendente
- **Visualización 3D**: Gráficos interactivos de las trayectorias orbitales
- **Análisis orbital**: Evolución de distancia, velocidad y parámetros orbitales
- **Interfaz interactiva**: Modificación de parámetros en tiempo real
- **Animación en tiempo real**: Botones Play/Pause para ver el satélite orbitando

## 📋 Requisitos

```bash
pip install -r requirements.txt
```

### Dependencias:
- `numpy >= 1.21.0`
- `matplotlib >= 3.5.0`
- `scipy >= 1.7.0`

## 🎯 Uso

### Simulación Básica

```bash
# Ejecutar simulación con parámetros por defecto
python3 orbital_simulation.py

# Simulación de 4 horas con pasos de 30 segundos
python3 orbital_simulation.py --duration 14400 --timestep 30

# Incluir animación del movimiento
python3 orbital_simulation.py --animate
```

### Simulación Interactiva

```bash
# Lanzar interfaz interactiva con controles deslizantes
python3 interactive_orbital_sim.py
```

## 📊 Parámetros Orbitales

La simulación utiliza los siguientes elementos orbitales keplerianos:

- **a**: Semi-eje mayor (km)
- **e**: Excentricidad (0-1)
- **i**: Inclinación orbital (grados)
- **ω (omega)**: Argumento del periapsis (grados)
- **Ω (Omega)**: Longitud del nodo ascendente (grados)
- **M₀**: Anomalía media en t=0 (grados)

### Configuración por Defecto

**Satélite** (Órbita tipo ISS con excentricidad):
- Semi-eje mayor: 7,000 km
- Excentricidad: 0.2
- Inclinación: 28.5°
- Periapsis: ~628 km de altitud
- Apoapsis: ~1,258 km de altitud

## 🎮 Interfaz Interactiva

La interfaz interactiva (`interactive_orbital_sim.py`) permite:

- **Controles deslizantes**: Modificar todos los parámetros orbitales en tiempo real
- **Visualización 3D enfocada**: Órbita 3D grande y clara con información orbital integrada
- **Animación interactiva**: Botones Play/Pause para ver el satélite en movimiento
- **Presets educativos**: ISS (órbita estable) y CRASH (impacto con la Tierra)
- **Control de velocidad**: Ajustar FPS de la animación en tiempo real

### Controles:
- Desliza los controles para modificar parámetros
- **Reset**: Vuelve a valores iniciales
- **ISS**: Carga la órbita real de la Estación Espacial Internacional
- **CRASH**: ⚠️ Carga una órbita que chocará con la Tierra (educativo)
- **Play**: Inicia la animación del satélite orbitando en tiempo real
- **Pause**: Pausa la animación en cualquier momento
- **Reset** (animación): Reinicia la animación desde el principio
- **Velocidad**: Control deslizante para ajustar los FPS (1-60 FPS) en tiempo real

## 🔬 Teoría Implementada

### Ecuación de Kepler
La simulación resuelve la ecuación de Kepler:
```
M = E - e·sin(E)
```

Donde:
- M: Anomalía media
- E: Anomalía excéntrica
- e: Excentricidad

### Transformaciones de Coordenadas
1. **Plano orbital → Sistema inercial**
2. **Rotaciones secuenciales**:
   - Argumento del periapsis (ω)
   - Inclinación orbital (i)
   - Longitud del nodo ascendente (Ω)

### Parámetros Calculados
- **Movimiento medio**: n = √(μ/a³)
- **Período orbital**: T = 2π/n
- **Radio orbital**: r = a(1-e²)/(1+e·cos(ν))

## 📈 Visualizaciones

### Visualización 3D Simplificada y Enfocada

- **Órbita 3D grande y clara**: Ocupa toda la pantalla para mejor visualización
- **Animación fluida**: Controles Play/Pause con velocidad ajustable (1-60 FPS)
- **Información integrada**: Título dinámico con datos orbitales clave
- **Alertas visuales**: Detección automática de órbitas de impacto
- **Tierra en 3D**: Esfera terrestre visible para referencia de escala
- **Marcadores claros**: Posiciones inicial, actual e impacto bien diferenciadas
- **Interfaz limpia**: Solo lo esencial - sin distracciones

## 🌍 Ejemplos de Órbitas

### Órbita por Defecto (LEO con excentricidad)
```python
OrbitalElements(a=7000, e=0.2, i=28.5, omega=0, Omega=0, M0=0)
```

### Órbita ISS Real
```python
OrbitalElements(a=6778, e=0.0003, i=51.6, omega=0, Omega=0, M0=0)
```

### ⚠️ Órbita de Impacto (Educativa)
```python
OrbitalElements(a=6000, e=0.6, i=45, omega=0, Omega=0, M0=0)
# Perigeo: ~1,429 km BAJO la superficie terrestre!
```

### Órbita Geosíncrona
```python
OrbitalElements(a=42164, e=0.0, i=0, omega=0, Omega=0, M0=0)
```

### Órbita Molniya
```python
OrbitalElements(a=26600, e=0.74, i=63.4, omega=270, Omega=0, M0=0)
```

## 🔧 Personalización

### Modificar Parámetros Gravitacionales
```python
# Cambiar el cuerpo central (ej: Luna)
elements = OrbitalElements(a=1000, e=0.1, i=0, omega=0, Omega=0, M0=0, 
                          mu=4.9048695e3)  # μ lunar
```

### Órbitas Interesantes para Probar
```python
# Órbita muy elíptica
elements = OrbitalElements(a=15000, e=0.6, i=0, omega=0, Omega=0, M0=0)

# Órbita polar
elements = OrbitalElements(a=8000, e=0.1, i=90, omega=0, Omega=0, M0=0)

# Órbitas de impacto (experimenta con estos valores):
# Semi-eje menor al radio terrestre (6371 km)
elements = OrbitalElements(a=5000, e=0.4, i=0, omega=0, Omega=0, M0=0)
elements = OrbitalElements(a=6200, e=0.8, i=30, omega=0, Omega=0, M0=0)
```

### Ajustar Duración y Resolución
```python
results = simulation.simulate(
    duration=86400,  # 24 horas
    time_step=30     # 30 segundos
)
```

## 📚 Referencias

- [NASA Mission Visualization - Elliptical Orbit Design](https://nasa.github.io/mission-viz/RMarkdown/Elliptical_Orbit_Design.html)
- Elementos orbitales keplerianos
- Mecánica orbital clásica

## 🐛 Solución de Problemas

### Error de Importación
```bash
# Verificar instalación de dependencias
pip install numpy matplotlib scipy
```

### Problemas de Visualización en Hyprland
```bash
# Configurar backend de matplotlib si es necesario
export MPLBACKEND=Qt5Agg
```

### Rendimiento en Simulaciones Largas
- Reducir la resolución temporal (`--timestep`)
- Limitar la duración (`--duration`)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Especialmente:
- Nuevos tipos de órbitas
- Mejoras en la visualización
- Optimizaciones de rendimiento
- Documentación adicional

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.