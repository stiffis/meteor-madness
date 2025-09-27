#!/bin/bash
# Script para ejecutar la simulación orbital interactiva

echo "🎮 Lanzando Simulación Orbital Interactiva"
echo "=========================================="

# Activar entorno virtual
source orbital_env/bin/activate

# Configurar display para Hyprland
export DISPLAY=:0

# Configurar backend de matplotlib para mejor compatibilidad con Hyprland
export MPLBACKEND=TkAgg

echo "📋 Instrucciones:"
echo "- Usa los deslizadores para modificar parámetros orbitales"
echo "- 'Reset': Vuelve a valores iniciales"
echo "- 'Preset ISS/Molniya': Carga órbitas reales"
echo "- Los gráficos se actualizan automáticamente"
echo ""

# Ejecutar simulación interactiva
python3 interactive_orbital_sim.py

echo "✅ Simulación interactiva finalizada!"