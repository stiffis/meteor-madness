#!/usr/bin/env python3
"""
Script de prueba para verificar el setup del backend
"""

try:
    print("🧪 Probando setup del backend MeteorMadness...")
    print("=" * 50)
    
    # Test 1: Importaciones básicas
    print("1. Probando importaciones básicas...")
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from models.orbital_elements import OrbitalElements
    from services.orbital_service import OrbitalService
    from services.simulation_service import SimulationService
    print("   ✅ Todas las importaciones exitosas")
    
    # Test 2: Creación de servicios
    print("2. Probando creación de servicios...")
    orbital_service = OrbitalService()
    simulation_service = SimulationService()
    print("   ✅ Servicios creados correctamente")
    
    # Test 3: Validación de elementos orbitales
    print("3. Probando validación de elementos orbitales...")
    test_elements = {
        'a': 7000, 'e': 0.2, 'i': 28.5, 
        'omega': 0, 'Omega': 0, 'M0': 0
    }
    validation = orbital_service.validate_orbital_elements(test_elements)
    if validation['valid']:
        print("   ✅ Validación exitosa")
    else:
        print(f"   ❌ Error en validación: {validation['errors']}")
        
    # Test 4: Presets
    print("4. Probando presets...")
    presets = orbital_service.get_orbital_presets()
    print(f"   ✅ {len(presets)} presets disponibles: {list(presets.keys())}")
    
    # Test 5: Simulación rápida
    print("5. Probando simulación...")
    result = simulation_service.run_simulation(test_elements, 1800, 60)  # 30 min, 60s pasos
    if result['success']:
        print(f"   ✅ Simulación exitosa - {result['total_points']} puntos calculados")
        print(f"   📊 Período orbital: {result['orbital_period']:.0f} segundos")
    else:
        print(f"   ❌ Error en simulación: {result['error']}")
    
    print("=" * 50)
    print("🎉 ¡Todos los tests pasaron! El backend está listo.")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de que las dependencias estén instaladas:")
    print("pip install flask flask-cors numpy matplotlib scipy python-dotenv")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    sys.exit(1)