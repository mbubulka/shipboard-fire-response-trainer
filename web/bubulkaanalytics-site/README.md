# 🚢 Shipboard Fire Response Training System

A comprehensive AI-powered training platform for shipboard fire emergency response, featuring realistic fire progression modeling and dynamic question generation.

## 🔥 Features

### **DCA Fire Response Assessment**
- **Dynamic Fire Progression**: 20-30 minute realistic fire development with 2-3 minute intervals
- **Compartment Spread Mechanics**: Fire spreads between galley → berthing → corridors with realistic shipboard layout
- **HVAC Contamination**: Smoke spreads through ventilation systems affecting ship-wide visibility
- **30+ Question Templates**: Eliminates repetition with smart tracking system
- **Four Escalation Phases**:
  - 🚨 Initial Detection (0-5 min): Assessment & initial response
  - 🔥 Active Suppression (5-15 min): Firefighting operations  
  - ⚠️ Emergency Response (15-25 min): Emergency tactics
  - 🆘 Critical Operations (25+ min): Resource management

### **AI-Powered Scenario Generation**
- Real-time fire behavior modeling with temperature, oxygen, and smoke progression
- Adaptive difficulty based on user performance
- Context-aware question generation matching fire conditions
- Immediate feedback with detailed explanations

### **Professional Training Interface**
- Live fire status dashboard with compartment tracking
- Time-based scenario evolution
- Performance analytics and decision scoring
- Mobile-responsive design for shipboard use

## 🚀 Quick Start

1. **Open the training system**: Open `index.html` in a web browser
2. **Navigate to Fire Trainer**: Click "Launch Fire Response Trainer"
3. **Choose training mode**:
   - **DCA Assessment**: 10-question dynamic assessment
   - **Scenario Analysis**: Interactive fire progression
   - **Knowledge Base**: Reference materials

## 📁 Project Structure

```
├── index.html                 # Main portfolio/landing page
├── firetrainer/              
│   └── comprehensive.html    # Complete fire training system
├── dca-training/             # Additional training modules
├── dev-backup/               # Development files (preserved)
└── assets/
    └── Michael_9028-Bkgd-square.jpg
```

## 🔧 Technical Implementation

### **Fire Physics Engine**
- Temperature progression modeling (45°F/min for electrical fires)
- Oxygen depletion calculations (0.3%/min consumption)
- Smoke generation and visibility reduction
- Flashover prediction and critical event detection

### **Compartment Spread Algorithm**
```javascript
// Fire spreads when conditions are met
if (spreadRadius > 15 && temperature > 800) {
    // Calculate spread probability based on:
    // - Fire conditions (temperature, spread radius)
    // - Compartment vulnerability (berthing 1.4x, fuel storage 1.8x)
    // - Fire type (electrical 1.3x, fuel 1.3x)
}
```

### **Question Generation System**
- Template-based dynamic questions with real-time fire data
- Smart repeat prevention (tracks last 5 templates)
- Phase-appropriate question selection
- Performance-based difficulty adjustment

## 🎯 Educational Objectives

### **Assessment Skills**
- Fire classification and identification
- Compartment conditions evaluation
- Crew safety status determination
- Structural integrity assessment

### **Suppression Techniques**
- Agent selection for different fire types
- Tactical decision making under pressure
- Resource allocation in multi-compartment fires
- Emergency evacuation procedures

### **Leadership & Command**
- Multi-phase emergency management
- Crew coordination and communication
- Critical resource decisions
- Risk assessment and mitigation

## 🛡️ Safety & Compliance

- **Educational Focus**: All scenarios based on publicly available maritime safety documentation
- **No Sensitive Data**: Removed claims about classified or restricted information
- **Professional Standards**: Aligned with standard maritime safety procedures
- **Realistic Training**: Maintains educational value without security concerns

## 🔄 Recent Updates

### v2.0 - Major Assessment Improvements
- **Eliminated question repeats** with 30+ template expansion
- **Realistic fire progression** (2-3 minutes per question)
- **Compartment spread mechanics** with shipboard layout
- **Time-based escalation phases** for progressive difficulty
- **Enhanced UI** showing affected compartments and HVAC status

### v1.5 - Security Compliance
- Removed claims about actual ship layouts and classified data
- Updated all references to use publicly available sources
- Added appropriate disclaimers and data source acknowledgments

### v1.0 - Professional Polish
- Added back navigation and DataCamp profile integration
- Cleaned development files to dev-backup folder
- Fixed deployment issues and embedded dependencies

## 🚀 Deployment

The system is **deployment-ready** with:
- ✅ Self-contained HTML/CSS/JavaScript (no external dependencies)
- ✅ Mobile-responsive design
- ✅ Cross-browser compatibility
- ✅ Professional UI/UX
- ✅ Comprehensive error handling
- ✅ Security compliance verified

## 👨‍💻 Developer

**Michael Bubulka**
- 🔗 [GitHub](https://github.com/mikebubulka)
- 💼 [LinkedIn](https://linkedin.com/in/mikebubulka)
- 📊 [DataCamp](https://www.datacamp.com/portfolio/mikebubulka)

## 📄 License

This project is for educational and training purposes. Please ensure compliance with your organization's training and safety protocols.

---

### 🎓 **Train Smart. Fight Safe. Save Ships.**