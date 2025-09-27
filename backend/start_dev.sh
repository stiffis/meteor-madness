#!/bin/bash
# Script para iniciar el backend en modo desarrollo

echo "🚀 Iniciando MeteorMadness Backend en modo desarrollo..."
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "⚠️  No se encontró entorno virtual. Creando..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si no están instaladas
echo "🔧 Verificando dependencias..."
pip install -r requirements.txt

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
fi

# Exportar variables de desarrollo
export FLASK_DEBUG=true
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000

echo ""
echo "🌍 Servidor disponible en: http://localhost:5000"
echo "📖 Documentación API: http://localhost:5000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar aplicación
python app.py