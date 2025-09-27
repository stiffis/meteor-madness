/**
 * Panel de controles para elementos orbitales y simulación
 */

import React, { useState, useEffect } from 'react';

// Componente para sliders de parámetros orbitales
function OrbitalSlider({ 
  label, 
  value, 
  min, 
  max, 
  step = 1, 
  unit = "", 
  onChange, 
  disabled = false 
}) {
  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <label className="text-sm font-medium text-gray-200">
          {label}
        </label>
        <span className="text-xs text-gray-400">
          {value.toFixed(step < 1 ? 3 : 1)} {unit}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        disabled={disabled}
        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer 
                   slider-thumb:appearance-none slider-thumb:w-4 slider-thumb:h-4 
                   slider-thumb:rounded-full slider-thumb:bg-blue-500 
                   slider-thumb:cursor-pointer disabled:opacity-50"
      />
    </div>
  );
}

// Componente para botones de preset
function PresetButton({ name, description, onClick, disabled = false }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="w-full p-2 mb-2 text-left bg-gray-800 hover:bg-gray-700 
                 disabled:bg-gray-900 disabled:opacity-50 
                 border border-gray-600 rounded-lg transition-colors
                 text-sm"
    >
      <div className="font-semibold text-gray-200">{name}</div>
      <div className="text-xs text-gray-400">{description}</div>
    </button>
  );
}

// Componente principal del panel de control
export default function ControlPanel({
  elements,
  onElementsChange,
  presets = {},
  onPresetSelect,
  simulationData,
  isLoading = false,
  className = ""
}) {
  const [localElements, setLocalElements] = useState({
    a: 7000,      // Semi-eje mayor (km)
    e: 0.2,       // Excentricidad
    i: 28.5,      // Inclinación (grados)
    omega: 0,     // Argumento del periapsis (grados)
    Omega: 0,     // Longitud del nodo ascendente (grados)
    M0: 0         // Anomalía media inicial (grados)
  });

  // Sincronizar con elementos externos
  useEffect(() => {
    if (elements) {
      setLocalElements(elements);
    }
  }, [elements]);

  // Manejar cambios en los elementos
  const handleElementChange = (key, value) => {
    const newElements = { ...localElements, [key]: value };
    setLocalElements(newElements);
    onElementsChange(newElements);
  };

  // Manejar selección de preset
  const handlePresetClick = (presetKey) => {
    const preset = presets[presetKey];
    if (preset && preset.elements) {
      setLocalElements(preset.elements);
      onPresetSelect(presetKey, preset.elements);
    }
  };

  // Resetear a valores por defecto
  const handleReset = () => {
    const defaultElements = {
      a: 7000,
      e: 0.2,
      i: 28.5,
      omega: 0,
      Omega: 0,
      M0: 0
    };
    setLocalElements(defaultElements);
    onElementsChange(defaultElements);
  };

  return (
    <div className={`bg-space-900 border-r border-space-700 overflow-y-auto ${className}`}>
      <div className="p-4">
        {/* Título */}
        <h2 className="text-xl font-bold text-space-50 mb-6 text-center">
          🚀 Control Orbital
        </h2>

        {/* Información orbital */}
        {simulationData?.orbital_info && (
          <div className="mb-6 p-3 bg-gray-800 rounded-lg border border-gray-600">
            <h3 className="text-sm font-semibold text-gray-200 mb-2">
              📊 Información Orbital
            </h3>
            <div className="text-xs text-gray-400 space-y-1">
              <div>
                Período: {simulationData.orbital_info.orbital_period_hours.toFixed(2)} h
              </div>
              <div>
                Perigeo: {simulationData.orbital_info.perigee_altitude.toFixed(0)} km
              </div>
              <div>
                Apogeo: {simulationData.orbital_info.apogee_altitude.toFixed(0)} km
              </div>
              {simulationData.orbital_info.will_impact_earth && (
                <div className="text-red-400 font-semibold">
                  ⚠️ IMPACTO: {simulationData.orbital_info.impact_depth.toFixed(0)} km bajo superficie
                </div>
              )}
            </div>
          </div>
        )}

        {/* Controles de elementos orbitales */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-200 mb-4">
            Elementos Orbitales
          </h3>
          
          <OrbitalSlider
            label="Semi-eje mayor (a)"
            value={localElements.a}
            min={6000}
            max={50000}
            step={100}
            unit="km"
            onChange={(value) => handleElementChange('a', value)}
            disabled={isLoading}
          />
          
          <OrbitalSlider
            label="Excentricidad (e)"
            value={localElements.e}
            min={0}
            max={0.99}
            step={0.01}
            onChange={(value) => handleElementChange('e', value)}
            disabled={isLoading}
          />
          
          <OrbitalSlider
            label="Inclinación (i)"
            value={localElements.i}
            min={0}
            max={180}
            step={1}
            unit="°"
            onChange={(value) => handleElementChange('i', value)}
            disabled={isLoading}
          />
          
          <OrbitalSlider
            label="Arg. Periapsis (ω)"
            value={localElements.omega}
            min={0}
            max={360}
            step={1}
            unit="°"
            onChange={(value) => handleElementChange('omega', value)}
            disabled={isLoading}
          />
          
          <OrbitalSlider
            label="Long. Nodo Asc. (Ω)"
            value={localElements.Omega}
            min={0}
            max={360}
            step={1}
            unit="°"
            onChange={(value) => handleElementChange('Omega', value)}
            disabled={isLoading}
          />
          
          <OrbitalSlider
            label="Anomalía Media (M₀)"
            value={localElements.M0}
            min={0}
            max={360}
            step={1}
            unit="°"
            onChange={(value) => handleElementChange('M0', value)}
            disabled={isLoading}
          />
        </div>

        {/* Botón de reset */}
        <div className="mb-6">
          <button
            onClick={handleReset}
            disabled={isLoading}
            className="w-full p-3 bg-gray-700 hover:bg-gray-600 
                       disabled:bg-gray-800 disabled:opacity-50 
                       border border-gray-600 rounded-lg transition-colors
                       text-white font-medium"
          >
            🔄 Reset a Defecto
          </button>
        </div>

        {/* Presets */}
        {Object.keys(presets).length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-200 mb-4">
              Presets de Órbitas
            </h3>
            
            {Object.entries(presets).map(([key, preset]) => (
              <PresetButton
                key={key}
                name={preset.name}
                description={preset.description}
                onClick={() => handlePresetClick(key)}
                disabled={isLoading}
              />
            ))}
          </div>
        )}

        {/* Estado de carga */}
        {isLoading && (
          <div className="mt-6 p-3 bg-blue-900 bg-opacity-50 border border-blue-600 rounded-lg">
            <div className="flex items-center justify-center text-blue-200">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-200 mr-2"></div>
              Calculando órbita...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}