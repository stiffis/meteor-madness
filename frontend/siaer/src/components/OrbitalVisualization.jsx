/**
 * Componente de visualización 3D de órbitas usando Three.js
 */

import React, { useRef, useEffect, useState } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Line, Sphere, Text } from "@react-three/drei";
import * as THREE from "three";

// Componente para la Tierra
function Earth() {
  const earthRef = useRef();

  useFrame(() => {
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.002; // Rotación lenta de la Tierra
    }
  });

  return (
    <Sphere ref={earthRef} args={[6371, 32, 32]} position={[0, 0, 0]}>
      <meshPhongMaterial
        color="#4A90E2"
        transparent
        opacity={0.8}
        shininess={100}
      />
    </Sphere>
  );
}

// Componente para la trayectoria orbital
function OrbitalTrajectory({ positions, currentIndex, showComplete = true }) {
  const lineRef = useRef();

  if (!positions || positions.length === 0) return null;

  // Convertir posiciones a Vector3 de Three.js
  const points = positions.map(
    (pos) => new THREE.Vector3(pos[0], pos[1], pos[2]),
  );

  // Puntos hasta la posición actual para el trail
  const currentPoints =
    currentIndex !== null && currentIndex >= 0
      ? points.slice(0, currentIndex + 1)
      : points;

  return (
    <group>
      {/* Trayectoria completa (sutil) */}
      {showComplete && (
        <Line
          points={points}
          color="#888888"
          lineWidth={2}
          transparent
          opacity={0.3}
        />
      )}

      {/* Trayectoria recorrida (resaltada) */}
      {currentPoints.length > 1 && (
        <Line
          points={currentPoints}
          color="#00FF88"
          lineWidth={6}
          transparent
          opacity={0.9}
        />
      )}
    </group>
  );
}

// Componente para el satélite animado
function Satellite({ position, isImpacting = false }) {
  const satelliteRef = useRef();
  const [scale, setScale] = useState(1);

  useFrame((state) => {
    if (satelliteRef.current) {
      if (isImpacting) {
        // Efecto de "explosión" en impacto
        const pulse = Math.sin(state.clock.elapsedTime * 10) * 0.5 + 1;
        setScale(pulse * 2);
        satelliteRef.current.material.color.setHex(0xff4444);
      } else {
        // Satélite normal
        setScale(1);
        satelliteRef.current.material.color.setHex(0x44ff44);
      }
    }
  });

  if (!position) return null;

  return (
    <Sphere
      ref={satelliteRef}
      args={[200, 8, 8]}
      position={position}
      scale={scale}
    >
      <meshPhongMaterial
        color={isImpacting ? "#FF4444" : "#44FF44"}
        emissive={isImpacting ? "#440000" : "#004400"}
        transparent
        opacity={0.9}
      />
    </Sphere>
  );
}

// Componente para información de texto en 3D
function InfoText({ text, position, color = "white" }) {
  if (!text || !position) return null;

  return (
    <Text
      position={position}
      fontSize={400}
      color={color}
      anchorX="center"
      anchorY="middle"
    >
      {text}
    </Text>
  );
}

// Componente principal de escena 3D
function OrbitalScene({
  simulationData,
  currentFrame,
  isPlaying,
  showTrajectory = true,
  showInfo = true,
}) {
  const { camera } = useThree();

  useEffect(() => {
    // Configurar cámara inicial
    camera.position.set(15000, 15000, 15000);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  if (!simulationData?.trajectory?.positions) {
    return (
      <group>
        <Earth />
        <InfoText
          text="Cargando simulación..."
          position={[0, 10000, 0]}
          color="yellow"
        />
      </group>
    );
  }

  const { positions, times } = simulationData.trajectory;
  const currentPosition = positions[currentFrame] || positions[0];

  // Verificar si está impactando
  const isImpacting =
    simulationData.analysis?.impact?.will_impact &&
    currentFrame >= simulationData.analysis.impact.impact_index;

  return (
    <group>
      {/* Tierra */}
      <Earth />

      {/* Trayectoria orbital */}
      {showTrajectory && (
        <OrbitalTrajectory
          positions={positions}
          currentIndex={currentFrame}
          showComplete={!isPlaying}
        />
      )}

      {/* Satélite */}
      <Satellite position={currentPosition} isImpacting={isImpacting} />

      {/* Información de impacto */}
      {isImpacting && showInfo && (
        <InfoText
          text="¡IMPACTO!"
          position={[
            currentPosition[0],
            currentPosition[1] + 2000,
            currentPosition[2],
          ]}
          color="red"
        />
      )}

      {/* Información de tiempo actual */}
      {showInfo && times && (
        <InfoText
          text={`T: ${(times[currentFrame] / 3600).toFixed(2)}h`}
          position={[0, -10000, 0]}
          color="cyan"
        />
      )}
    </group>
  );
}

// Componente principal de visualización
export default function OrbitalVisualization({
  simulationData,
  currentFrame = 0,
  isPlaying = false,
  className = "",
  showTrajectory = true,
  showInfo = true,
}) {
  return (
    <div className={`w-full h-full bg-black ${className}`}>
      <Canvas
        camera={{
          fov: 50,
          near: 1,
          far: 100000,
          position: [15000, 15000, 15000],
        }}
      >
        {/* Iluminación */}
        <ambientLight intensity={0.3} />
        <directionalLight
          position={[10000, 10000, 5000]}
          intensity={1}
          castShadow
        />
        <pointLight position={[0, 0, 0]} intensity={0.5} color="orange" />

        {/* Controles de cámara */}
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          zoomSpeed={0.5}
          panSpeed={0.5}
          rotateSpeed={0.3}
        />

        {/* Escena orbital */}
        <OrbitalScene
          simulationData={simulationData}
          currentFrame={currentFrame}
          isPlaying={isPlaying}
          showTrajectory={showTrajectory}
          showInfo={showInfo}
        />
      </Canvas>
    </div>
  );
}
