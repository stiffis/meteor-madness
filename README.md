# 🚀 Meteor Impact Simulator and Risk Assessment Tool

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=threedotjs&logoColor=white)
![React Three Fiber](https://img.shields.io/badge/React%20Three%20Fiber-000000?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

**IN DEVELOPMENT**. Interactive web tool that simulates asteroid impacts on Earth and evaluates environmental consequences, integrating real data from NASA and USGS.

## 📁 Project Structure

```
MeteorMadness/
├── README.md                    # This file
├── backend/                     # Flask REST API
│   ├── app.py                   # Main application
│   ├── requirements.txt         # Python dependencies
│   ├── start_dev.sh            # Development script
│   ├── test_setup.py           # Setup test
│   ├── test_api.py             # Endpoints test
│   ├── models/                 # Data models
│   │   └── orbital_elements.py # Keplerian orbital elements
│   └── services/               # Business logic
│       ├── orbital_service.py  # Validation and presets
│       └── simulation_service.py # Orbital simulation
├── frontend/                   # React + Three.js frontend
│   ├── src/                   # React source code
│   │   ├── components/        # React components
│   │   └── services/          # API services
│   ├── README.md              # Frontend documentation
│   └── start_dev.sh          # Development script
└── simultion_trajectory/      # Original orbital simulation
    ├── orbital_simulation.py  # Base simulation
    ├── interactive_orbital_sim.py # Interactive interface
    └── README.md              # Detailed documentation
```

## 🎯 Current Development Status

### ✅ **Completed (Phase 1 - Orbital Simulation)**

1. **Orbital Trajectory Simulation**
   - ✅ Complete implementation of Kepler's equations
   - ✅ Orbital propagation with Keplerian elements
   - ✅ Interactive 3D visualization with Three.js
   - ✅ 6 educational presets (ISS, Geostationary, Molniya, etc.)
   - ✅ Earth impact detection

2. **Functional Flask Backend**
   - ✅ REST API for orbital simulation
   - ✅ Orbital elements validation
   - ✅ Integration with existing Python simulation
   - ✅ Orbital analysis (periapsis, apoapsis, periods)

3. **React + Three.js Frontend**
   - ✅ Modern and responsive web interface
   - ✅ Control panel for orbital elements
   - ✅ Real-time satellite animation
   - ✅ Speed and temporal navigation controls

### 🔄 **In Development (Phase 2 - Impact Effects)**

1. **Impact Effects Simulation** ⚠️ **PENDING**
   - ❌ Crater formation calculation
   - ❌ Blast wave simulation
   - ❌ Tsunami modeling (ocean impacts)
   - ❌ Seismic and geological effects
   - ❌ Damage assessment by zones

2. **External APIs Integration** ⚠️ **PENDING**
   - ❌ NASA Near-Earth Object (NEO) API
   - ❌ USGS Earthquake Catalog API
   - ❌ Real near-Earth asteroid data
   - ❌ Historical seismic information

3. **Advanced Features** ⚠️ **PENDING**
   - ❌ 2D maps of affected zones
   - ❌ Kinetic energy and TNT equivalent calculation
   - ❌ Mitigation strategies simulation
   - ❌ Educational section on asteroid impacts

### 📋 **Next Priorities (Based on Project Proposal)**

#### **Objective 1: Environmental Impact Effects**

- [ ] Implement crater formation models (Collins et al., 2005)
- [ ] Calculate blast waves using Kingery-Bulmash scaling
- [ ] Simulate tsunamis with Ward and Asphaug models (2000)
- [ ] Evaluate thermal and seismic effects

#### **Objective 2: Real Data Integration**

- [ ] Connect with NASA NEO API for near-Earth asteroids
- [ ] Integrate USGS Earthquake Catalog for seismic effects
- [ ] Implement validation with historical cases (Tunguska, Chelyabinsk)

#### **Objective 3: Advanced Interactive Interface**

- [ ] 2D maps with D3.js to visualize affected zones
- [ ] Sliders for asteroid parameters (size, velocity, angle)
- [ ] Mitigation strategies visualization
- [ ] Data export (GeoJSON, CSV)

#### **Objective 4: Educational Component**

- [ ] Explanatory section on scientific fundamentals
- [ ] Interactive historical case studies
- [ ] Glossary and scientific references
- [ ] Planetary protection measures

### 🔧 Technologies

- **Backend**: Flask, NumPy, SciPy, Matplotlib
- **Frontend**: React 18, Vite, Three.js, Tailwind CSS
- **3D Graphics**: React Three Fiber, Three.js
- **Simulation**: Kepler's equations, Newton-Raphson
- **API**: REST with validation and presets
- **Testing**: Automated test scripts

## 🚀 Installation and Usage

### 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Git** to clone the repository

### 🔧 Complete Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd MeteorMadness
```

#### 2. Setup Backend (Python/Flask)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_setup.py
```

#### 3. Setup Frontend (React/Three.js)

```bash
# Navigate to frontend directory
cd frontend/siaer

# Install dependencies
npm install

# Verify installation
npm run build
```

### 🎮 Application Usage

#### **Option 1: Complete Web Application (Recommended)**

1. **Start Backend**:

```bash
cd backend
source venv/bin/activate  # Linux/Mac
python app.py
```

Backend will be available at: `http://localhost:5000`

2. **Start Frontend** (in another terminal):

```bash
cd frontend/siaer
npm run dev
```

Frontend will be available at: `http://localhost:5173`

3. **Use the Application**:
   - Open your browser at `http://localhost:5173`
   - Modify orbital elements with sliders
   - Try presets (ISS, Molniya, CRASH)
   - Control animation with Play/Pause/Reset

#### **Option 2: Original Python Simulation**

```bash
# Navigate to simulation
cd simultion_trajectory

# Activate virtual environment
source orbital_env/bin/activate  # Linux/Mac

# Interactive simulation with controls
python interactive_orbital_sim.py

# Basic simulation with graphics
python orbital_simulation.py
```

### 🛠️ Development Scripts

#### Backend

```bash
cd backend
./start_dev.sh    # Start server with automatic configuration
python test_api.py # Test all endpoints
```

#### Frontend

```bash
cd frontend/siaer
./start_dev.sh    # Start server with backend verification
npm run build     # Build production version
npm run preview   # Preview the build
```

### 🔍 Installation Verification

#### Backend

```bash
cd backend
python test_setup.py
# Should show: "🎉 All tests passed! Backend is ready."
```

#### Frontend

```bash
cd frontend/siaer
npm run dev
# Should automatically open http://localhost:5173
```

### 🐛 Troubleshooting

#### Backend won't start

```bash
# Verify Python and dependencies
python --version
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Frontend won't load

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Verify Node.js
node --version  # Must be 18+
```

#### Frontend-Backend connection error

- Verify backend is running at `http://localhost:5000`
- Check that no firewall is blocking the port
- Review browser console for CORS errors

### 📱 Basic Usage

1. **Modify Orbits**: Use sliders in the left panel to change orbital elements
2. **Presets**: Click ISS, Molniya, etc. to load famous orbits
3. **Animation**: Use Play/Pause to see the satellite orbiting
4. **Camera**: Drag to rotate, scroll to zoom, right-click to pan
5. **Information**: Observe real-time orbital data in the control panel

## 📡 API Endpoints

- `GET /` - Welcome page
- `GET /health` - Health check
- `GET /api/orbital/presets` - Get presets
- `POST /api/orbital/elements` - Validate orbital elements
- `POST /api/orbital/simulate` - Run simulation

### Usage Example

```bash
# Simulate ISS orbit
curl -X POST http://localhost:5000/api/orbital/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "elements": {
      "a": 6778, "e": 0.0003, "i": 51.6,
      "omega": 0, "Omega": 0, "M0": 0
    },
    "duration": 3600,
    "timestep": 60
  }'
```

## 🎮 Features

### Web Frontend (React + Three.js)

- **3D Visualization**: Earth, orbital trajectories, animated satellites
- **Control Panel**: Real-time modification of orbital elements
- **Integrated Presets**: ISS, Geostationary, Molniya, Crash
- **Smooth Animation**: Play/Pause/Reset of simulations
- **Modern Interface**: Tailwind CSS with space theme
- **Responsive**: Adaptable to different screen sizes

### Orbital Simulation

- **Kepler's Equations**: Precise implementation
- **6 Orbital Elements**: a, e, i, ω, Ω, M₀
- **Complete Analysis**: Periapsis, apoapsis, period
- **Impact Detection**: Automatic alerts
- **Educational Presets**: ISS, Geostationary, Molniya, etc.

### Backend API

- **Complete REST**: Validation and simulation
- **CORS Enabled**: Ready for frontend
- **Error Handling**: Consistent responses
- **Documentation**: Self-documented endpoints

## 📊 Available Presets

1. **default**: LEO orbit with eccentricity (7,000 km)
2. **iss**: International Space Station (6,778 km)
3. **geostationary**: Geostationary satellite (42,164 km)
4. **molniya**: Russian elliptical orbit (26,600 km, e=0.74)
5. **polar**: Polar observation orbit (8,000 km)
6. **crash**: ⚠️ Educational impact orbit

## 🌐 Complete Web Application

### How to Use the Web Interface

1. **Start Backend**: `cd backend && python app.py`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Open**: http://localhost:5173

### Web Features

- **Side Panel**: Controls for orbital elements
- **3D Viewer**: Earth, orbits and satellites in Three.js
- **Camera Controls**: Zoom, rotation, pan
- **Real-time Information**: Period, altitudes, elapsed time
- **Quick Presets**: Instant loading of famous orbits

## 🏗️ Architecture and Methodology (According to Project Proposal)

### **Scientific Approach**

The project implements validated scientific methodologies for asteroid impact simulation:

1. **Validated Physical Models**
   - Kepler's equations for orbital propagation
   - Earth Impact Effects Program (Collins et al., 2005)
   - Kingery-Bulmash scaling for blast waves
   - Ward-Asphaug models for tsunamis

2. **Real Data Integration**
   - NASA Near-Earth Object (NEO) API
   - USGS Earthquake Catalog
   - Validation with historical cases

3. **Client-Server Architecture**
   - **Frontend**: React + Vite + Three.js + D3.js
   - **Backend**: Flask + Python (NumPy, SciPy, AstroPy)
   - **APIs**: RESTful with real-time data

### **Current Development Phase vs Final Objective**

| Component               | Current Status     | Final Objective             |
| ----------------------- | ------------------ | --------------------------- |
| **Orbital Trajectory**  | ✅ Complete        | ✅ Kepler's equations       |
| **Impact Effects**      | ❌ Not started     | 🎯 Craters, waves, tsunamis |
| **External APIs**       | ❌ Not integrated  | 🎯 NASA NEO + USGS          |
| **2D Maps**             | ❌ Not implemented | 🎯 D3.js + GeoJSON          |
| **Educational Section** | ❌ Not started     | 🎯 Scientific fundamentals  |

## 🤝 Contributing

The project is fully structured for contributions:

- **Backend**: Extensible REST API in Flask
- **Frontend**: Modular React components
- **Simulation**: Modular algorithms
- **Documentation**: Complete and updated

## 📚 Scientific References

### **Validation with Historical Cases**

- **Tunguska (1908)**: Atmospheric explosion event in Siberia
- **Chelyabinsk (2013)**: Documented meteorite and blast wave
- **Chicxulub**: Impact associated with K-Pg mass extinction

### **APIs and Real Data**

- **NASA NEO API**: Near-Earth Object database for close asteroids
- **USGS Earthquake Catalog**: Global seismic data for modeling
- **NASA Mission Visualization**: Orbital design methodology

### **Frameworks and Technologies**

- [NASA Mission Visualization - Elliptical Orbit Design](https://nasa.github.io/mission-viz/RMarkdown/Elliptical_Orbit_Design.html)
- [Three.js Documentation](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [D3.js](https://d3js.org/) - Data visualization and 2D maps

## 📄 License

Open source project under MIT license.

---

## ⚡ Project Status

### 🏆 **Phase 1 Completed: Orbital Simulation**

✅ **Asteroid Trajectories** - Kepler's equations implemented  
✅ **3D Visualization** - Three.js with real-time animation  
✅ **Flask Backend** - Functional REST API  
✅ **React Frontend** - Modern and interactive interface

### 🚧 **Phase 2 In Development: Impact Effects**

⚠️ **Impact Models** - Craters, blast waves, tsunamis  
⚠️ **NASA/USGS APIs** - Real asteroid data and seismic effects  
⚠️ **Damage Maps** - 2D visualization of affected zones  
⚠️ **Educational Component** - Scientific fundamentals

**MeteorMadness** is in active development. Orbital simulation is complete and functional, while impact effects and real data integration are in implementation phase.

### 📈 **Current Progress: ~40% Completed**

- ✅ Orbital simulation and 3D visualization
- 🔄 Impact effects (next priority)
- 📋 External APIs and real data
- 📋 Educational section and scientific documentation
