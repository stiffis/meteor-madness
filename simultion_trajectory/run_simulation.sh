#!/bin/bash
# Script para ejecutar la simulación orbital básica

echo "🚀 Lanzando Simulación Orbital Básica"
echo "======================================"

# Activar entorno virtual
source orbital_env/bin/activate

# Configurar display para Hyprland
export DISPLAY=:0

# Ejecutar simulación con parámetros por defecto
python3 orbital_simulation.py "$@"

echo "✅ Simulación completada!"