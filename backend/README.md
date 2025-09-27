# Backend - MeteorMadness

API REST en Flask para simulación orbital basada en las ecuaciones de Kepler.

## 🚀 Características

- **API REST completa** para simulación orbital
- **Validación de elementos orbitales** keplerianos
- **Presets predefinidos** (ISS, órbitas geoestacionarias, etc.)
- **Análisis orbital completo** (periapsis, apoapsis, detección de impactos)
- **Integración con simulación existente** de `simultion_trajectory/`

## Estructura

```
backend/
├── README.md              # Este archivo
├── app.py                 # Aplicación Flask principal
├── run.py                 # Script de arranque
├── requirements.txt       # Dependencias Python
├── .env.example          # Variables de entorno de ejemplo
├── models/               # Modelos de datos
│   ├── __init__.py
│   └── orbital_elements.py  # Modelo de elementos orbitales
├── services/             # Lógica de negocio
│   ├── __init__.py
│   ├── orbital_service.py   # Validación y presets
│   └── simulation_service.py # Simulación orbital
└── utils/                # Utilidades compartidas
    └── __init__.py
```

## Tecnologías

- **Framework**: Flask 2.3.3
- **CORS**: Flask-CORS para frontend
- **Simulación**: NumPy, SciPy, Matplotlib
- **Variables de entorno**: python-dotenv

## 📦 Instalación

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env
```

## 🎯 Uso

### Desarrollo

```bash
# Modo desarrollo
python app.py

# O usando el script de desarrollo
chmod +x start_dev.sh
./start_dev.sh
```

### Producción

```bash
# Con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 API Endpoints

### Información General

- `GET /` - Página de bienvenida con lista de endpoints
- `GET /health` - Health check del servidor

### API Orbital

- `POST /api/orbital/simulate` - Ejecutar simulación orbital
- `POST /api/orbital/elements` - Validar elementos orbitales
- `GET /api/orbital/presets` - Obtener presets predefinidos

### Ejemplo de Uso

```bash
# Simular órbita ISS
curl -X POST http://localhost:5000/api/orbital/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "elements": {
      "a": 6778,
      "e": 0.0003,
      "i": 51.6,
      "omega": 0,
      "Omega": 0,
      "M0": 0
    },
    "duration": 3600,
    "timestep": 60
  }'
```

## 🔧 Configuración

Variables de entorno disponibles en `.env`:

- `FLASK_HOST` - Host del servidor (default: 0.0.0.0)
- `FLASK_PORT` - Puerto del servidor (default: 5000)
- `FLASK_DEBUG` - Modo debug (default: false)

## 📊 Datos de Respuesta

La API devuelve datos de simulación que incluyen:

- **Trayectoria completa**: Posiciones, velocidades, altitudes
- **Análisis orbital**: Periapsis, apoapsis, velocidades
- **Detección de impactos**: Si la órbita chocará con la Tierra
- **Información orbital**: Período, excentricidad, etc.

## 🧪 Testing

```bash
# Ejecutar health check
curl http://localhost:5000/health

# Obtener presets
curl http://localhost:5000/api/orbital/presets
```