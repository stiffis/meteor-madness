#!/usr/bin/env python3
"""
Backend Flask para MeteorMadness
API REST para simulación orbital
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Importar nuestros servicios
from services.orbital_service import OrbitalService
from services.simulation_service import SimulationService
from services.solar_system_service import SolarSystemService
from services.nasa_neo_service import NasaNeoService

# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)

# Configurar CORS para permitir requests desde el frontend
CORS(app)

# Configuración
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.getenv('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.getenv('FLASK_PORT', 5000))

# Inicializar servicios
orbital_service = OrbitalService()
simulation_service = SimulationService()
nasa_neo_service = NasaNeoService()
solar_system_service = SolarSystemService()

@app.route('/')
def home():
    """Endpoint de bienvenida"""
    return jsonify({
        "message": "MeteorMadness Backend API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/": "Esta página de bienvenida",
            "/health": "Estado de salud del servidor",
            "/api/orbital/simulate": "POST - Ejecutar simulación orbital",
            "/api/orbital/elements": "POST - Validar elementos orbitales",
            "/api/orbital/presets": "GET - Obtener presets predefinidos",
            "/api/neo/search": "GET - Buscar objetos NEO (proxy SBDB)",
            "/api/neo/object": "GET - Obtener datos de un NEO desde NASA",
            "/api/solar/system": "GET - Estados orbitales aproximados del sistema solar",
            "/api/impactor/2025": "GET - Datos del meteorito IMPACTOR-2025"
        }
    })

@app.route('/health')
def health_check():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy",
        "service": "meteor-madness-backend"
    }), 200

# === RUTAS DE LA API ORBITAL ===

@app.route('/api/orbital/simulate', methods=['POST'])
def simulate_orbit():
    """
    Ejecuta una simulación orbital
    
    Body JSON esperado:
    {
        "elements": {
            "a": 7000,      // Semi-eje mayor (km)
            "e": 0.2,       // Excentricidad (0-1)
            "i": 28.5,      // Inclinación (grados)
            "omega": 0,     // Argumento del periapsis (grados)
            "Omega": 0,     // Longitud del nodo ascendente (grados)
            "M0": 0         // Anomalía media inicial (grados)
        },
        "duration": 7200,   // Duración en segundos (opcional, default: 2 horas)
        "timestep": 60      // Paso de tiempo en segundos (opcional, default: 60s)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'elements' not in data:
            return jsonify({
                "error": "Missing required field 'elements'"
            }), 400
        
        # Extraer parámetros
        elements = data['elements']
        duration = data.get('duration', 7200)  # 2 horas por defecto
        timestep = data.get('timestep', 60)    # 60 segundos por defecto
        
        # Validar elementos orbitales
        validation_result = orbital_service.validate_orbital_elements(elements)
        if not validation_result['valid']:
            return jsonify({
                "error": "Invalid orbital elements",
                "details": validation_result['errors']
            }), 400
        
        # Ejecutar simulación
        simulation_result = simulation_service.run_simulation(
            elements, duration, timestep
        )
        
        if not simulation_result['success']:
            return jsonify({
                "error": "Simulation failed",
                "details": simulation_result['error']
            }), 500
        
        return jsonify({
            "success": True,
            "data": simulation_result['data'],
            "metadata": {
                "elements": elements,
                "duration": duration,
                "timestep": timestep,
                "total_points": simulation_result['total_points'],
                "orbital_period": simulation_result['orbital_period']
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/api/orbital/elements', methods=['POST'])
def validate_elements():
    """
    Valida elementos orbitales sin ejecutar simulación
    
    Body JSON esperado:
    {
        "elements": {
            "a": 7000,
            "e": 0.2,
            "i": 28.5,
            "omega": 0,
            "Omega": 0,
            "M0": 0
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'elements' not in data:
            return jsonify({
                "error": "Missing required field 'elements'"
            }), 400
        
        elements = data['elements']
        validation_result = orbital_service.validate_orbital_elements(elements)
        
        if validation_result['valid']:
            # Calcular información adicional de la órbita
            orbital_info = orbital_service.calculate_orbital_info(elements)
            
            return jsonify({
                "valid": True,
                "orbital_info": orbital_info
            })
        else:
            return jsonify({
                "valid": False,
                "errors": validation_result['errors']
            }), 400
            
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/api/orbital/presets', methods=['GET'])
def get_presets():
    """Obtiene presets predefinidos de órbitas"""
    try:
        presets = orbital_service.get_orbital_presets()
        return jsonify({
            "success": True,
            "presets": presets
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route('/api/neo/object', methods=['GET'])
def get_neo_object():
    """Proxy hacia la API de la NASA para obtener datos de un NEO."""

    identifier = (
        request.args.get('sstr')
        or request.args.get('designation')
        or request.args.get('neo_id')
    )

    if not identifier:
        return jsonify({
            "success": False,
            "error": "Query parameter 'designation' (o 'neo_id'/'sstr') es requerido",
        }), 400

    result = nasa_neo_service.fetch_object(identifier)

    if not result.success:
        return jsonify({
            "success": False,
            "error": result.error,
        }), result.status_code

    return jsonify({
        "success": True,
        "data": result.data,
    })


@app.route('/api/neo/search', methods=['GET'])
def search_neo_objects():
    """Busca objetos NEO usando el proxy de la SBDB (sbdb.api)."""

    query = request.args.get('q') or request.args.get('query') or request.args.get('sstr')
    limit_param = request.args.get('limit', 10)

    try:
        limit = int(limit_param)
    except (TypeError, ValueError):
        limit = 10

    result = nasa_neo_service.search_objects(query, limit)

    if not result.success:
        return jsonify({
            "success": False,
            "error": result.error,
        }), result.status_code

    return jsonify({
        "success": True,
        "data": result.data,
    })


@app.route('/api/solar/system', methods=['GET'])
def get_solar_system_state():
    """Devuelve estados orbitales aproximados para los planetas del sistema solar."""

    data = solar_system_service.get_planet_states()
    return jsonify({
        "success": True,
        "data": data,
    })


@app.route('/api/impactor/2025', methods=['GET'])
def get_impactor_2025():
    """Obtiene los datos del meteorito IMPACTOR-2025."""
    
    try:
        # Datos del meteorito IMPACTOR-2025
        impactor_data = {
            "name": "IMPACTOR-2025",
            "designation": "IMPACTOR-2025",
            "full_name": "IMPACTOR-2025",
            "description": "Meteorito hipotético con trayectoria de impacto potencial",
            "color": "#ff4444",
            "orbitColor": "#ff6666",
            "radiusKm": 0.5,  # Pequeño para visualización
            "semiMajorAxisKm": 373922988.41,  # a ≈ 373,922,988.41 km
            "eccentricity": 0.6,  # e = 0.6
            "inclinationDeg": 3.0,  # i = 3.0°
            "longitudeOfAscendingNodeDeg": 12.64,  # Ω = 12.64°
            "argumentOfPeriapsisDeg": 0.0,  # ω = 0.0°
            "meanAnomalyDeg": -1.0,  # M₀ = -1.0°
            "orbitalPeriodDays": 1443.36,  # P ≈ 1443.36 días
            "isNeo": True,
            "pha": True,  # Potencialmente peligroso
            "moid_au": 0.02,  # Distancia mínima de intersección orbital muy pequeña
            "absolute_magnitude_h": 18.5,  # Magnitud estimada
            "orbit_class": "Apollo",
            "warning": "⚠️ Objeto con trayectoria de impacto potencial - ÓRBITA MUY PELIGROSA",
            "simulation_elements": {
                "a": 373922988.41,
                "e": 0.6,
                "i": 3.0,
                "omega": 0.0,
                "Omega": 12.64,
                "M0": -1.0,
                "mu": 1.32712440018e11  # Constante gravitacional solar
            }
        }
        
        return jsonify({
            "success": True,
            "data": impactor_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Error al obtener datos de IMPACTOR-2025",
            "details": str(e)
        }), 500

# === MANEJO DE ERRORES ===

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/health",
            "/api/orbital/simulate",
            "/api/orbital/elements", 
            "/api/orbital/presets",
            "/api/neo/search",
            "/api/neo/object",
            "/api/solar/system",
            "/api/impactor/2025"
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "message": "Check the HTTP method for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on our end"
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando MeteorMadness Backend...")
    print(f"🌍 Servidor disponible en: http://{app.config['HOST']}:{app.config['PORT']}")
    print("📡 Endpoints disponibles:")
    print("   GET  / - Página de bienvenida")
    print("   GET  /health - Health check")
    print("   POST /api/orbital/simulate - Ejecutar simulación")
    print("   POST /api/orbital/elements - Validar elementos orbitales")
    print("   GET  /api/orbital/presets - Obtener presets")
    print("   GET  /api/neo/search - Buscar objetos NEO (SBDB Query)")
    print("   GET  /api/neo/object - Obtener datos de NEO desde NASA")
    print("   GET  /api/solar/system - Estados orbitales del sistema solar")
    print("   GET  /api/impactor/2025 - Datos del meteorito IMPACTOR-2025")
    print()
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
