/**
 * MeteorMadness - Simulador Orbital 3D
 * Frontend React con Three.js para visualización de órbitas
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import OrbitalVisualization from './components/OrbitalVisualization';
import ControlPanel from './components/ControlPanel';
import AnimationControls from './components/AnimationControls';
import MeteorMadnessAPI from './services/api';

function App() {
  // Estados principales
  const [elements, setElements] = useState({
    a: 7000,      // Semi-eje mayor (km)
    e: 0.2,       // Excentricidad
    i: 28.5,      // Inclinación (grados)
    omega: 0,     // Argumento del periapsis (grados)
    Omega: 0,     // Longitud del nodo ascendente (grados)
    M0: 0         // Anomalía media inicial (grados)
  });
  
  const [simParams, setSimParams] = useState({
    duration: 7200, // 2 horas
    timestep: 60,   // 1 minuto
  });

  const [simulationData, setSimulationData] = useState(null);
  const [presets, setPresets] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const [isPanelOpen, setIsPanelOpen] = useState(true);

  // Estados de animación
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [animationSpeed, setAnimationSpeed] = useState(1.0);

  // Referencias
  const animationRef = useRef(null);
  const lastFrameTimeRef = useRef(0);

  // Verificar conexión con backend al inicio
  useEffect(() => {
    checkBackendConnection();
    loadPresets();
  }, []);

  // Simular automáticamente cuando cambian los elementos
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (connectionStatus === 'connected') {
        runSimulation();
      }
    }, 500); // Debounce de 500ms

    return () => clearTimeout(timeoutId);
  }, [elements, simParams, connectionStatus]);

  // Manejo de la animación
  useEffect(() => {
    if (isPlaying && simulationData?.trajectory?.positions) {
      const animate = (currentTime) => {
        if (currentTime - lastFrameTimeRef.current >= (100 / animationSpeed)) {
          setCurrentFrame(prev => {
            const maxFrames = simulationData.trajectory.positions.length - 1;
            const next = prev + 1;
            
            if (next > maxFrames) {
              setIsPlaying(false);
              return maxFrames;
            }
            
            return next;
          });
          
          lastFrameTimeRef.current = currentTime;
        }
        
        if (isPlaying) {
          animationRef.current = requestAnimationFrame(animate);
        }
      };
      
      animationRef.current = requestAnimationFrame(animate);
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying, animationSpeed, simulationData]);

  // Funciones de API
  const checkBackendConnection = async () => {
    try {
      const result = await MeteorMadnessAPI.healthCheck();
      if (result.success) {
        setConnectionStatus('connected');
        setError(null);
      } else {
        setConnectionStatus('error');
        setError('No se puede conectar con el backend');
      }
    } catch (err) {
      console.error('Error al verificar el backend:', err);
      setConnectionStatus('error');
      setError('Backend no disponible en http://localhost:5000');
    }
  };

  const loadPresets = async () => {
    try {
      const result = await MeteorMadnessAPI.getPresets();
      if (result.success) {
        setPresets(result.data.presets || {});
      }
    } catch (err) {
      console.warn('No se pudieron cargar los presets:', err);
    }
  };

  const runSimulation = async () => {
    if (connectionStatus !== 'connected') return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await MeteorMadnessAPI.simulate({
        elements,
        duration: simParams.duration,
        timestep: simParams.timestep
      });

      if (result.success) {
        setSimulationData(result.data.data);
        setCurrentFrame(0);
        setIsPlaying(false);
      } else {
        setError(result.error?.error || 'Error en la simulación');
        setSimulationData(null);
      }
    } catch (err) {
      console.error('Error al ejecutar la simulación:', err);
      setError('Error de comunicación con el backend');
      setSimulationData(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Manejadores de eventos
  const handleElementsChange = useCallback((newElements) => {
    setElements(newElements);
  }, []);
  
  const handleSimParamsChange = useCallback((newParams) => {
    setSimParams(newParams);
  }, []);

  const handlePresetSelect = useCallback((presetKey, presetElements) => {
    setElements(presetElements);
  }, []);

  const handlePlay = useCallback(() => {
    if (simulationData?.trajectory?.positions) {
      setIsPlaying(true);
    }
  }, [simulationData]);

  const handlePause = useCallback(() => {
    setIsPlaying(false);
  }, []);

  const handleReset = useCallback(() => {
    setIsPlaying(false);
    setCurrentFrame(0);
  }, []);

  const handleFrameSeek = useCallback((frame) => {
    setCurrentFrame(frame);
    setIsPlaying(false);
  }, []);

  const handleSpeedChange = useCallback((speed) => {
    setAnimationSpeed(speed);
  }, []);

  const togglePanel = useCallback(() => {
    setIsPanelOpen(prev => !prev);
  }, []);

  // Retry connection
  const retryConnection = () => {
    setConnectionStatus('connecting');
    checkBackendConnection();
  };

  // Render de estado de error
  if (connectionStatus === 'error') {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center p-8 bg-gray-800 rounded-lg border border-gray-600 max-w-md">
          <div className="text-red-400 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-white mb-4">
            Backend No Disponible
          </h1>
          <p className="text-gray-400 mb-6">
            No se puede conectar con el backend de MeteorMadness en http://localhost:5000
          </p>
          <div className="space-y-3">
            <button
              onClick={retryConnection}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 
                         text-white rounded-lg transition-colors"
            >
              🔄 Reintentar Conexión
            </button>
            <div className="text-sm text-gray-500">
              Asegúrate de que el backend esté ejecutándose:<br/>
              <code className="text-gray-300">cd backend && python app.py</code>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Render de estado de carga inicial
  if (connectionStatus === 'connecting') {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-400">Conectando con el backend...</p>
        </div>
      </div>
    );
  }

  const totalFrames = simulationData?.trajectory?.positions?.length || 0;

  const bottomPanelStyle = {
    left: isPanelOpen
      ? 'max(1rem, min(calc(20rem + 1.5rem), calc(100% - 10rem)))'
      : '1rem',
    right: '1rem',
    transition: 'left 0.3s ease-in-out, right 0.3s ease-in-out'
  };

  // Render principal
  return (
    <div className="h-screen bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-30 p-4 bg-transparent">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <img
              src="/logo.svg"
              alt="SIAER logo"
              className="h-10 w-10 mr-3"
            />
            <div>
              <h1 className="text-2xl font-bold text-white">SIAER</h1>
              <p className="text-sm text-gray-200 font-normal">
                Simulador Orbital 3D
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <button
              type="button"
              onClick={togglePanel}
              aria-pressed={isPanelOpen}
              className="px-3 py-2 bg-gray-700/70 hover:bg-gray-600/80 border border-gray-500/60 rounded-lg text-sm text-white transition-colors"
            >
              {isPanelOpen ? 'Ocultar panel' : 'Mostrar panel'}
            </button>
            <div className="flex items-center text-sm text-green-300">
              <div className="w-2 h-2 bg-green-300 rounded-full mr-2"></div>
              Backend conectado
            </div>
            {error && (
              <div className="text-sm text-red-300 max-w-md truncate">
                ⚠️ {error}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Layout principal */}
      <main className="flex-1 flex flex-col">
        <div className="flex-1 relative">
          <OrbitalVisualization
            simulationData={simulationData}
            currentFrame={currentFrame}
            isPlaying={isPlaying}
            showTrajectory={true}
            showInfo={true}
            className="h-full w-full"
          />

          <div className="pointer-events-none absolute inset-0 z-20 flex">
            <div
              className={`mt-24 mb-6 ml-4 w-80 max-h-[calc(100%-7rem)] overflow-y-auto rounded-2xl border border-gray-700/60 bg-gray-900/60 backdrop-blur-md shadow-lg transition-all duration-300 ease-in-out transform ${
                isPanelOpen
                  ? 'pointer-events-auto translate-x-0 opacity-100'
                  : 'pointer-events-none -translate-x-[calc(100%+1.5rem)] opacity-0'
              }`}
            >
              <ControlPanel
                elements={elements}
                onElementsChange={handleElementsChange}
                presets={presets}
                onPresetSelect={handlePresetSelect}
                simulationData={simulationData}
                isLoading={isLoading}
                simParams={simParams}
                onSimParamsChange={handleSimParamsChange}
                className="w-full h-full bg-transparent border-none"
              />
            </div>
          </div>
        </div>

        <div
          className="pointer-events-none fixed bottom-6 z-20 flex justify-center"
          style={bottomPanelStyle}
        >
          <div className="pointer-events-auto mx-4 w-full max-w-5xl rounded-2xl border border-gray-700/60 bg-gray-900/60 backdrop-blur-md shadow-lg">
            <AnimationControls
              isPlaying={isPlaying}
              onPlay={handlePlay}
              onPause={handlePause}
              onReset={handleReset}
              currentFrame={currentFrame}
              totalFrames={totalFrames}
              onFrameSeek={handleFrameSeek}
              speed={animationSpeed}
              onSpeedChange={handleSpeedChange}
              simulationData={simulationData}
              disabled={isLoading || !simulationData}
              className="bg-transparent border-none"
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
