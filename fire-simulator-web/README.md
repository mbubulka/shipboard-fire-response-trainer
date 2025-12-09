# Web Directory Structure

This directory contains the organized components of the Shipboard Fire Response Training System.

## Directory Organization

### Frontend/UI Components
- **`bubulkaanalytics-site/`** - Main website and user interface
  - `index.html` - Portfolio landing page
  - `firetrainer/` - Fire response training interface
  - `dca-training/` - DCA training modules
  - `enhanced-dca-knowledge-base.js` - Knowledge base integration

- **`firetrainer/`** - Legacy firetrainer components

### Backend/API Components  
- **`backend/`** - Server-side components and APIs
  - API servers (`app.py`, `server.py`, `production_server.py`)
  - DCA assessment and feedback systems
  - Database files and response evaluators

### Machine Learning/AI
- **`models/`** - AI/ML models and training scripts
  - DQN model files (`.pth` format)
  - Training and evaluation scripts
  - Model performance results

### Documentation & Reference
- **`docs/`** - Documentation and reference materials
  - NFPA standards (1500, 1521, 1670)
  - USCG firefighting manual
  - System documentation and integration guides

### Training Data
- **`training-data/`** - JSON training data and scenarios
  - AI training prompts
  - Scenario definitions
  - Knowledge base configurations
  - Source document references

### Development & Testing
- **`testing/`** - Test files and development tools
  - Test DQN components
  - Simple test interfaces
  - Development utilities

### Deployment
- **`deployment/`** - Deployment configurations
  - Netlify configuration and simulators
  - Lambda deployment scripts
  - Platform-specific deployment files

### Utilities
- **`utils/`** - Utility scripts and tools
  - Training data processors
  - System status reporters
  - Integration utilities

## Key Files
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This documentation file

## Usage
The main entry point is through `bubulkaanalytics-site/index.html` which provides access to all training components.