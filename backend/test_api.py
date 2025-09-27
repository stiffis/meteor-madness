#!/usr/bin/env python3
"""
Script para probar los endpoints del backend
"""

import requests
import json
import time

def test_endpoint(method, url, data=None, description=""):
    """Prueba un endpoint y muestra el resultado"""
    print(f"🧪 {description}")
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and 'message' in result:
                print(f"   ✅ {result['message']}")
            else:
                print(f"   ✅ Respuesta exitosa")
        else:
            print(f"   ❌ Error: {response.text}")
        print()
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Error: No se pudo conectar al servidor")
        print("   💡 Asegúrate de que el servidor esté corriendo en http://localhost:5000")
        print()
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        print()
        return False
    
    return True

def main():
    base_url = "http://localhost:5000"
    
    print("🚀 Probando API del backend MeteorMadness")
    print("=" * 50)
    
    # Test 1: Página de bienvenida
    if not test_endpoint("GET", f"{base_url}/", description="Probando página de bienvenida"):
        return
    
    # Test 2: Health check
    test_endpoint("GET", f"{base_url}/health", description="Probando health check")
    
    # Test 3: Obtener presets
    test_endpoint("GET", f"{base_url}/api/orbital/presets", description="Probando obtener presets")
    
    # Test 4: Validar elementos orbitales
    test_elements = {
        "elements": {
            "a": 7000,
            "e": 0.2,
            "i": 28.5,
            "omega": 0,
            "Omega": 0,
            "M0": 0
        }
    }
    test_endpoint("POST", f"{base_url}/api/orbital/elements", test_elements, 
                 description="Probando validación de elementos orbitales")
    
    # Test 5: Simulación completa (rápida)
    simulation_data = {
        "elements": {
            "a": 6778,  # ISS
            "e": 0.0003,
            "i": 51.6,
            "omega": 0,
            "Omega": 0,
            "M0": 0
        },
        "duration": 1800,  # 30 minutos
        "timestep": 60     # 1 minuto
    }
    test_endpoint("POST", f"{base_url}/api/orbital/simulate", simulation_data,
                 description="Probando simulación orbital (ISS - 30 min)")
    
    print("=" * 50)
    print("🎉 ¡Pruebas de API completadas!")
    print()
    print("💡 Para iniciar el servidor:")
    print("   python app.py")
    print()
    print("🌍 Servidor disponible en: http://localhost:5000")

if __name__ == "__main__":
    main()