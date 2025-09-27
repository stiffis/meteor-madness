# 🚀 SIAER - Simulador de Impactos de Asteroides y Evaluación de Riesgos

Proyecto **EN DESARROLLO**. Herramienta web interactiva que simula impactos de asteroides en la Tierra y evalúa las consecuencias medioambientales, integrando datos reales de NASA y USGS.

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

## 🎯 Estado Actual del Desarrollo

### ✅ **Completado (Fase 1 - Simulación Orbital)**

1. **Simulación de Trayectorias Orbitales**
   - ✅ Implementación completa de ecuaciones de Kepler
   - ✅ Propagación orbital con elementos keplerianos
   - ✅ Visualización 3D interactiva con Three.js
   - ✅ 6 presets educativos (ISS, Geoestacionaria, Molniya, etc.)
   - ✅ Detección de impactos con la Tierra

2. **Backend Flask Funcional**
   - ✅ API REST para simulación orbital
   - ✅ Validación de elementos orbitales
   - ✅ Integración con simulación Python existente
   - ✅ Análisis orbital (periapsis, apoapsis, períodos)

3. **Frontend React + Three.js**
   - ✅ Interfaz web moderna y responsive
   - ✅ Panel de control para elementos orbitales
   - ✅ Animación en tiempo real de satélites
   - ✅ Controles de velocidad y navegación temporal

### 🔄 **En Desarrollo (Fase 2 - Efectos de Impacto)**

1. **Simulación de Efectos de Impacto** ⚠️ **PENDIENTE**
   - ❌ Cálculo de formación de cráteres
   - ❌ Simulación de ondas expansivas
   - ❌ Modelado de tsunamis (impactos oceánicos)
   - ❌ Efectos sísmicos y geológicos
   - ❌ Evaluación de daños por zonas

2. **Integración con APIs Externas** ⚠️ **PENDIENTE**
   - ❌ NASA Near-Earth Object (NEO) API
   - ❌ USGS Earthquake Catalog API
   - ❌ Datos reales de asteroides cercanos
   - ❌ Información sísmica histórica

3. **Funcionalidades Avanzadas** ⚠️ **PENDIENTE**
   - ❌ Mapas 2D de zonas afectadas
   - ❌ Cálculo de energía cinética y equivalente TNT
   - ❌ Simulación de estrategias de mitigación
   - ❌ Sección educativa sobre impactos de asteroides

### 📋 **Próximas Prioridades (Basadas en Anteproyecto)**

#### **Objetivo 1: Efectos Medioambientales del Impacto**
- [ ] Implementar modelos de formación de cráteres (Collins et al., 2005)
- [ ] Calcular ondas expansivas usando escalado Kingery-Bulmash
- [ ] Simular tsunamis con modelos Ward y Asphaug (2000)
- [ ] Evaluar efectos térmicos y sísmicos

#### **Objetivo 2: Integración de Datos Reales**
- [ ] Conectar con NASA NEO API para asteroides cercanos
- [ ] Integrar USGS Earthquake Catalog para efectos sísmicos
- [ ] Implementar validación con casos históricos (Tunguska, Chelyabinsk)

#### **Objetivo 3: Interfaz Interactiva Avanzada**
- [ ] Mapas 2D con D3.js para visualizar zonas afectadas
- [ ] Sliders para parámetros de asteroide (tamaño, velocidad, ángulo)
- [ ] Visualización de estrategias de mitigación
- [ ] Exportación de datos (GeoJSON, CSV)

#### **Objetivo 4: Componente Educativo**
- [ ] Sección explicativa sobre fundamentos científicos
- [ ] Casos de estudio históricos interactivos
- [ ] Glosario y referencias científicas
- [ ] Medidas de protección planetaria

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

## 🏗️ Arquitectura y Metodología (Según Anteproyecto)

### **Enfoque Científico**
El proyecto implementa metodologías científicas validadas para la simulación de impactos de asteroides:

1. **Modelos Físicos Validados**
   - Ecuaciones de Kepler para propagación orbital
   - Earth Impact Effects Program (Collins et al., 2005)
   - Escalado Kingery-Bulmash para ondas expansivas
   - Modelos Ward-Asphaug para tsunamis

2. **Integración de Datos Reales**
   - NASA Near-Earth Object (NEO) API
   - USGS Earthquake Catalog
   - Validación con casos históricos

3. **Arquitectura Cliente-Servidor**
   - **Frontend**: React + Vite + Three.js + D3.js
   - **Backend**: Flask + Python (NumPy, SciPy, AstroPy)
   - **APIs**: RESTful con datos en tiempo real

### **Fase de Desarrollo Actual vs Objetivo Final**

| Componente | Estado Actual | Objetivo Final |
|------------|---------------|----------------|
| **Trayectoria Orbital** | ✅ Completo | ✅ Ecuaciones de Kepler |
| **Efectos de Impacto** | ❌ No iniciado | 🎯 Cráteres, ondas, tsunamis |
| **APIs Externas** | ❌ No integradas | 🎯 NASA NEO + USGS |
| **Mapas 2D** | ❌ No implementado | 🎯 D3.js + GeoJSON |
| **Sección Educativa** | ❌ No iniciado | 🎯 Fundamentos científicos |

## 🤝 Contribución

El proyecto está completamente estructurado para contribuciones:

- **Backend**: API REST extensible en Flask
- **Frontend**: Componentes React modulares
- **Simulación**: Algoritmos modulares
- **Documentación**: Completa y actualizada

## 📚 Referencias Científicas

### **Validación con Casos Históricos**
- **Tunguska (1908)**: Evento de estallido atmosférico en Siberia
- **Chelyabinsk (2013)**: Meteorito y onda expansiva documentados
- **Chicxulub**: Impacto asociado con extinción masiva K-Pg

### **APIs y Datos Reales**
- **NASA NEO API**: Near-Earth Object database para asteroides cercanos
- **USGS Earthquake Catalog**: Datos sísmicos globales para modelado
- **NASA Mission Visualization**: Metodología de diseño orbital

### **Frameworks y Tecnologías**
- [NASA Mission Visualization - Elliptical Orbit Design](https://nasa.github.io/mission-viz/RMarkdown/Elliptical_Orbit_Design.html)
- [Three.js Documentation](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [D3.js](https://d3js.org/) - Visualización de datos y mapas 2D

## 📄 Licencia

Proyecto de código abierto bajo licencia MIT.

---

## ⚡ Estado del Proyecto

### 🏆 **Fase 1 Completada: Simulación Orbital**
✅ **Trayectorias de Asteroides** - Ecuaciones de Kepler implementadas  
✅ **Visualización 3D** - Three.js con animación en tiempo real  
✅ **Backend Flask** - API REST funcional  
✅ **Frontend React** - Interfaz moderna e interactiva  

### 🚧 **Fase 2 En Desarrollo: Efectos de Impacto**
⚠️ **Modelos de Impacto** - Cráteres, ondas expansivas, tsunamis  
⚠️ **APIs NASA/USGS** - Datos reales de asteroides y efectos sísmicos  
⚠️ **Mapas de Daño** - Visualización 2D de zonas afectadas  
⚠️ **Componente Educativo** - Fundamentos científicos  

**SIAER** está en desarrollo activo. La simulación orbital está completa y funcional, mientras que los efectos de impacto y la integración con datos reales están en fase de implementación.

### 📈 **Progreso Actual: ~40% Completado**
- ✅ Simulación orbital y visualización 3D
- 🔄 Efectos de impacto (próxima prioridad)
- 📋 APIs externas y datos reales
- 📋 Sección educativa y documentación científica
