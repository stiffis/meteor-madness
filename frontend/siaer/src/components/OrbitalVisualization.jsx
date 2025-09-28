/**
 * Componente de visualización 3D de órbitas usando Three.js
 */

import React, { Suspense, useRef, useEffect, useState } from "react";
import { Canvas, useFrame, useThree, useLoader } from "@react-three/fiber";
import { OrbitControls, Line, Sphere, Text } from "@react-three/drei";
import * as THREE from "three";

const EARTH_TEXTURE_URL =
  import.meta.env.VITE_EARTH_TEXTURE_URL ||
  "/textures/earth-daymap.jpg";

const EARTH_CLOUDS_TEXTURE_URL =
  import.meta.env.VITE_EARTH_CLOUDS_URL ||
  "/textures/earth-clouds.png";

// Componente para la Tierra
function Earth() {
  const earthRef = useRef();
  const cloudRef = useRef();

  const earthTexture = useLoader(THREE.TextureLoader, EARTH_TEXTURE_URL, (loader) => {
    loader.setCrossOrigin("anonymous");
  });

  const cloudsTexture = useLoader(THREE.TextureLoader, EARTH_CLOUDS_TEXTURE_URL, (loader) => {
    loader.setCrossOrigin("anonymous");
  });

  useEffect(() => {
    if (earthTexture) {
      earthTexture.colorSpace = THREE.SRGBColorSpace;
    }

    if (cloudsTexture) {
      cloudsTexture.colorSpace = THREE.SRGBColorSpace;
    }
  }, [earthTexture, cloudsTexture]);

  useFrame((_, delta) => {
    if (earthRef.current) {
      earthRef.current.rotation.y += delta * 0.05; // Rotación lenta de la Tierra
    }

    if (cloudRef.current) {
      cloudRef.current.rotation.y += delta * 0.08; // Nubes ligeramente más rápidas
    }
  });

  return (
    <group>
      <Sphere ref={earthRef} args={[6371, 64, 64]} position={[0, 0, 0]}>
        <meshPhongMaterial
          map={earthTexture}
          shininess={12}
          specular={new THREE.Color("#111822")}
        />
      </Sphere>

      {cloudsTexture && (
        <Sphere ref={cloudRef} args={[6430, 64, 64]} position={[0, 0, 0]}>
          <meshPhongMaterial
            map={cloudsTexture}
            transparent
            opacity={0.35}
            depthWrite={false}
          />
        </Sphere>
      )}
    </group>
  );
}

// Componente para la trayectoria orbital
function OrbitalTrajectory({ positions, currentIndex, showComplete = true, trailLength = 100 }) {
  if (!positions || positions.length === 0) return null;

  const points = positions.map(
    (pos) => new THREE.Vector3(pos[0], pos[1], pos[2]),
  );

  const trailPoints = points.slice(Math.max(0, currentIndex - trailLength), currentIndex + 1);

  const geometry = new THREE.BufferGeometry().setFromPoints(trailPoints);

  const colors = new Float32Array(trailPoints.length * 3);
  const startColor = new THREE.Color(0x00ff88);
  const endColor = new THREE.Color(0x004422);

  for (let i = 0; i < trailPoints.length; i++) {
    const t = i / (trailPoints.length - 1);
    const color = startColor.clone().lerp(endColor, 1 - t);
    color.toArray(colors, i * 3);
  }

  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  return (
    <group>
      {showComplete && (
        <Line
          points={points}
          color="#888888"
          lineWidth={2}
          transparent
          opacity={0.3}
        />
      )}

      {trailPoints.length > 1 && (
        <line geometry={geometry}>
          <lineBasicMaterial vertexColors={true} lineWidth={24} transparent opacity={0.9} />
        </line>
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

function Skybox() {
  const { scene } = useThree();
  const texture = useLoader(THREE.TextureLoader, "/textures/space-skybox.jpg");

  useEffect(() => {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = texture;
  }, [scene, texture]);

  return null;
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
        <Suspense fallback={null}>
          <Earth />
        </Suspense>
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
      <Suspense fallback={null}>
        <Earth />
      </Suspense>

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
    <div className={`w-full h-full ${className}`}>
      <Canvas
        camera={{
          fov: 50,
          near: 1,
          far: 100000,
          position: [15000, 15000, 15000],
        }}
      >
        <Skybox />
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
