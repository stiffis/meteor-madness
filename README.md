# 🚀 MeteorMadness

Proyecto de simulación orbital avanzada con backend Flask, frontend React + Three.js y simulación basada en las ecuaciones de Kepler.

## 📁 Estructura del Proyecto

```
MeteorMadness/
├── README.md                    # Este archivo
├── backend/                     # API REST en Flask
│   ├── app.py                   # Aplicación principal
│   ├── requirements.txt         # Dependencias Python
│   ├── start_dev.sh            # Script de desarrollo
│   ├── test_setup.py           # Test de configuración
│   ├── test_api.py             # Test de endpoints
│   ├── models/                 # Modelos de datos
│   │   └── orbital_elements.py # Elementos orbitales keplerianos
│   └── services/               # Lógica de negocio
│       ├── orbital_service.py  # Validación y presets
│       └── simulation_service.py # Simulación orbital
├── frontend/                   # Frontend React + Three.js
│   ├── src/                   # Código fuente React
│   │   ├── components/        # Componentes React
│   │   └── services/          # Servicios API
│   ├── README.md              # Documentación del frontend
│   └── start_dev.sh          # Script de desarrollo
└── simultion_trajectory/      # Simulación orbital original
    ├── orbital_simulation.py  # Simulación base
    ├── interactive_orbital_sim.py # Interfaz interactiva
    └── README.md              # Documentación detallada
```

## 🎯 Estado Actual

### ✅ Completado

1. **Backend Flask Completo**
   - API REST con endpoints para simulación orbital
   - Validación de elementos orbitales keplerianos
   - 6 presets predefinidos (ISS, Geoestacionaria, Molniya, etc.)
   - Análisis orbital completo (periapsis, apoapsis, detección de impactos)
   - Integración con simulación existente

2. **Frontend React + Three.js Completo**
   - Interfaz web moderna con React 18 + Vite
   - Visualización 3D interactiva con Three.js
   - Panel de control completo para elementos orbitales
   - Animación en tiempo real de satélites
   - Integración total con API del backend

3. **Simulación Orbital Avanzada**
   - Implementación de las ecuaciones de Kepler
   - Visualización 3D interactiva (Python + Web)
   - Animación en tiempo real
   - Múltiples presets educativos

4. **Estructura de Proyecto Completa**
   - Separación clara backend/frontend
   - Documentación completa
   - Scripts de desarrollo y testing

### 🔧 Tecnologías

- **Backend**: Flask, NumPy, SciPy, Matplotlib
- **Frontend**: React 18, Vite, Three.js, Tailwind CSS
- **3D Graphics**: React Three Fiber, Three.js
- **Simulación**: Ecuaciones de Kepler, Newton-Raphson
- **API**: REST con validación y presets
- **Testing**: Scripts automatizados de prueba

## 🚀 Inicio Rápido

### Backend

```bash
# Navegar al backend
cd backend

# Activar entorno virtual
source venv/bin/activate

# Probar configuración
python test_setup.py

# Iniciar servidor de desarrollo
python app.py
# o usar: ./start_dev.sh
```

### Frontend

```bash
# Navegar al frontend
cd frontend

# Iniciar servidor de desarrollo
npm run dev
# o usar: ./start_dev.sh
```

### Simulación Original

```bash
# Navegar a simulación
cd simultion_trajectory

# Activar entorno virtual
source orbital_env/bin/activate

# Simulación interactiva
python interactive_orbital_sim.py

# Simulación básica
python orbital_simulation.py
```

## 📡 API Endpoints

- `GET /` - Página de bienvenida
- `GET /health` - Health check
- `GET /api/orbital/presets` - Obtener presets
- `POST /api/orbital/elements` - Validar elementos orbitales
- `POST /api/orbital/simulate` - Ejecutar simulación

### Ejemplo de Uso

```bash
# Simular órbita ISS
curl -X POST http://localhost:5000/api/orbital/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "elements": {
      "a": 6778, "e": 0.0003, "i": 51.6,
      "omega": 0, "Omega": 0, "M0": 0
    },
    "duration": 3600,
    "timestep": 60
  }'
```

## 🎮 Características

### Frontend Web (React + Three.js)

- **Visualización 3D**: Tierra, trayectorias orbitales, satélites animados
- **Panel de Control**: Modificación en tiempo real de elementos orbitales
- **Presets Integrados**: ISS, Geoestacionaria, Molniya, Crash
- **Animación Fluida**: Play/Pause/Reset de simulaciones
- **Interfaz Moderna**: Tailwind CSS con tema espacial
- **Responsive**: Adaptable a diferentes tamaños de pantalla

### Simulación Orbital

- **Ecuaciones de Kepler**: Implementación precisa
- **6 Elementos Orbitales**: a, e, i, ω, Ω, M₀
- **Análisis Completo**: Periapsis, apoapsis, período
- **Detección de Impactos**: Alertas automáticas
- **Presets Educativos**: ISS, Geoestacionaria, Molniya, etc.

### API Backend

- **REST Completa**: Validación y simulación
- **CORS Habilitado**: Listo para frontend
- **Error Handling**: Respuestas consistentes
- **Documentación**: Endpoints autodocumentados

## 📊 Presets Disponibles

1. **default**: Órbita LEO con excentricidad (7,000 km)
2. **iss**: Estación Espacial Internacional (6,778 km)
3. **geostationary**: Satélite geoestacionario (42,164 km)
4. **molniya**: Órbita elíptica rusa (26,600 km, e=0.74)
5. **polar**: Órbita polar de observación (8,000 km)
6. **crash**: ⚠️ Órbita de impacto educativa

## 🌐 Aplicación Web Completa

### Cómo Usar la Interfaz Web

1. **Iniciar Backend**: `cd backend && python app.py`
2. **Iniciar Frontend**: `cd frontend && npm run dev`
3. **Abrir**: http://localhost:5173

### Características Web

- **Panel Lateral**: Controles para elementos orbitales
- **Visualizador 3D**: Tierra, órbitas y satélites en Three.js
- **Controles de Cámara**: Zoom, rotación, desplazamiento
- **Información en Tiempo Real**: Período, altitudes, tiempo transcurrido
- **Presets Rápidos**: Carga instantánea de órbitas famosas

## 🔬 Próximos Pasos

### Posibles Mejoras
1. **Base de Datos**: Almacenar simulaciones históricas
2. **Autenticación**: Sistema de usuarios
3. **Más Cuerpos**: Luna, planetas, asteroides
4. **Perturbaciones**: Efectos gravitatorios adicionales
5. **Exportación**: Datos en CSV, JSON, KML
6. **Mobile App**: Versión móvil nativa

## 🤝 Contribución

El proyecto está completamente estructurado para contribuciones:

- **Backend**: API REST extensible en Flask
- **Frontend**: Componentes React modulares
- **Simulación**: Algoritmos modulares
- **Documentación**: Completa y actualizada

## 📚 Referencias

- [NASA Mission Visualization - Elliptical Orbit Design](https://nasa.github.io/mission-viz/RMarkdown/Elliptical_Orbit_Design.html)
- [Three.js Documentation](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- Mecánica orbital clásica
- Elementos orbitales keplerianos

## 📄 Licencia

Proyecto de código abierto bajo licencia MIT.

---

## 🎉 ¡Proyecto Completado!

✅ **Backend Flask** - API REST completa  
✅ **Frontend React + Three.js** - Interfaz web moderna  
✅ **Simulación Orbital** - Ecuaciones de Kepler implementadas  
✅ **Visualización 3D** - Tanto en Python como en Web  
✅ **Documentación** - Completa para todos los componentes

**MeteorMadness** es ahora un simulador orbital completo listo para uso educativo y desarrollo posterior.