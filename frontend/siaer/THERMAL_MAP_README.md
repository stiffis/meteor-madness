# Mapa de Efectos Térmicos - IMPACTOR-2025

## Descripción

El **Mapa de Efectos Térmicos** es una visualización interactiva que muestra los efectos térmicos de un impacto de asteroide basado en los cálculos científicos de Collins-Melosh-Marcus. Utiliza heatmap.js para crear una representación visual realista de las zonas de temperatura.

## Características

### 🌡️ Visualización Térmica
- **Gradiente de colores**: De azul (frío) a rojo (caliente)
- **Zonas térmicas**: 4 niveles de intensidad basados en temperatura
- **Animación**: Efectos de pulso térmico realistas
- **Interactividad**: Controles de animación y leyenda

### 🔬 Cálculos Científicos
- **Algoritmo Collins-Melosh-Marcus**: Cálculos precisos de efectos de impacto
- **Parámetros realistas**: Basados en IMPACTOR-2025 (1 km de diámetro)
- **Energía del impacto**: 9.85 × 10¹⁹ Joules
- **Escalado automático**: Adaptación a diferentes tamaños de pantalla

### 🎯 Zonas Térmicas

1. **Zona de Incineración** (>1000°C)
   - Radio: ~7.5 km
   - Efectos: Vaporización instantánea
   - Color: Rojo intenso

2. **Zona de Combustión** (300-1000°C)
   - Radio: ~18.75 km
   - Efectos: Incendios masivos, fusión de materiales
   - Color: Naranja

3. **Radiación Térmica** (100-300°C)
   - Radio: ~112.5 km
   - Efectos: Quemaduras graves, incendios
   - Color: Amarillo

4. **Pulso Térmico** (50-100°C)
   - Radio: ~187.5 km
   - Efectos: Quemaduras leves, calor intenso
   - Color: Amarillo claro

## Uso

### Componente ThermalMap

```jsx
import ThermalMap from '../components/ThermalMap';

<ThermalMap 
  impactLat={40.7128}
  impactLng={-74.0060}
  impactEnergy={9.85e19}
  impactorDiameter={1.0}
  showAnimation={true}
/>
```

### Parámetros

- `impactLat`: Latitud del epicentro (default: 40.7128°N)
- `impactLng`: Longitud del epicentro (default: 74.0060°W)
- `impactEnergy`: Energía del impacto en Joules (default: 9.85e19)
- `impactorDiameter`: Diámetro del impactor en km (default: 1.0)
- `showAnimation`: Mostrar animación de pulso térmico (default: true)

## Controles

### 🎮 Interfaz de Usuario
- **▶️ Iniciar/Pausar**: Control de animación
- **🔄 Reset**: Regenerar mapa térmico
- **👁️ Mostrar/Ocultar**: Toggle de leyenda

### 📊 Información Mostrada
- **Escala de temperatura**: Barra de colores con rangos
- **Leyenda detallada**: Descripción de cada zona térmica
- **Estadísticas**: Datos del impacto y efectos
- **Coordenadas**: Ubicación exacta del epicentro

## Implementación Técnica

### Dependencias
- **heatmap.js**: Librería para visualización de mapas de calor
- **React**: Framework de interfaz de usuario
- **Canvas API**: Renderizado de gráficos

### Algoritmo de Generación
1. **Cálculo de radios**: Basado en Collins-Melosh-Marcus
2. **Generación de puntos**: Distribución aleatoria dentro de cada zona
3. **Escalado**: Adaptación al tamaño del canvas
4. **Renderizado**: Aplicación de gradientes y efectos

### Optimizaciones
- **Responsive**: Adaptación automática al tamaño de pantalla
- **Performance**: Animaciones optimizadas con requestAnimationFrame
- **Memory**: Limpieza automática de recursos

## Científica

### Referencias
- Collins, G. S., Melosh, H. J., & Marcus, R. A. (2005). "Earth Impact Effects Program"
- Cálculos basados en parámetros de IMPACTOR-2025
- Modelos de transferencia de calor y radiación térmica

### Precisión
- **Radios calculados**: Basados en ecuaciones empíricas validadas
- **Temperaturas**: Rangos realistas para impactos de asteroides
- **Efectos**: Modelados según literatura científica actual

## Archivos Relacionados

- `src/components/ThermalMap.jsx`: Componente principal
- `src/pages/MapPage.jsx`: Página que integra el mapa térmico
- `src/components/ImpactMap.jsx`: Mapa de impacto general

## Desarrollo Futuro

### Mejoras Planificadas
- [ ] Integración con datos meteorológicos reales
- [ ] Simulación de vientos y dispersión térmica
- [ ] Efectos de topografía en distribución de calor
- [ ] Modo de comparación con otros impactos históricos
- [ ] Exportación de datos térmicos

### Características Avanzadas
- [ ] Simulación temporal (evolución en el tiempo)
- [ ] Efectos de materiales específicos
- [ ] Integración con modelos climáticos
- [ ] Visualización 3D de efectos térmicos

---

**Nota**: Este mapa térmico es una herramienta educativa y de visualización. Los cálculos están basados en modelos científicos establecidos, pero deben considerarse aproximaciones para fines educativos.