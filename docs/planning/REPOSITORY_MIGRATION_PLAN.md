# Repository Migration Checklist
# From old fire-response-ai to new shipboard-fire-response-ai

## 🗂️ **What to Preserve from Current Repository**

### ✅ **Keep These Assets**
1. **Enhanced DQN System**
   - `enhanced_dqn_system.py` (400+ lines of advanced neural network)
   - Training pipeline architecture
   - Multi-source awareness features

2. **Training Data Integration**
   - NFPA standards processing
   - USCG regulations integration
   - Navy training procedures
   - Comprehensive scenario database

3. **Web Integration Components**
   - API endpoint designs
   - Frontend integration patterns
   - Feedback system architecture

4. **Documentation & Insights**
   - System architecture decisions
   - Training methodology
   - Performance insights

### ❌ **Leave Behind (Clean Start)**
1. **Problematic Files**
   - Broken CI/CD configurations
   - Inconsistent naming conventions
   - Legacy CVN references
   - Accumulated technical debt

2. **Sensitive or Unnecessary**
   - Old model checkpoints
   - Test data with mixed references
   - Temporary files and scripts
   - Development artifacts

## 📋 **Migration Priority Order**

### Phase 1: Foundation (Day 1)
```bash
# 1. Create new repository structure
mkdir shipboard-fire-response-ai
cd shipboard-fire-response-ai

# 2. Initialize with clean files
- README.md (new, clean)
- LICENSE
- .gitignore (comprehensive)
- requirements.txt (minimal, working)
- setup.py
```

### Phase 2: Core System (Day 1-2)
```bash
# 3. Migrate enhanced DQN (cleaned)
src/shipboard_fire_ai/core/
├── dqn_agent.py        # Enhanced DQN system
├── environment.py      # Training environment
└── feedback_system.py  # New feedback system

# 4. Add working tests
tests/
├── test_core.py
├── test_integration.py
└── conftest.py
```

### Phase 3: Training Pipeline (Day 2-3)
```bash
# 5. Migrate training components
src/shipboard_fire_ai/training/
├── scenario_generator.py
├── data_processor.py
└── model_trainer.py

# 6. Add training data structure
data/
├── scenarios/
├── training_sources/
└── README.md
```

### Phase 4: API & Integration (Day 3-4)
```bash
# 7. Create API system
src/shipboard_fire_ai/api/
├── main.py
├── routes/
└── models/

# 8. Add documentation
docs/
├── installation.md
├── usage.md
└── api_reference.md
```

## 🔧 **File Conversion Guide**

### Enhanced DQN System
**From**: `enhanced_dqn_system.py`
**To**: `src/shipboard_fire_ai/core/dqn_agent.py`
**Changes**: 
- Remove CVN references
- Clean imports
- Add proper logging
- Improve documentation

### Training Integration
**From**: `comprehensive_training_integrator.py`
**To**: `src/shipboard_fire_ai/training/data_processor.py`
**Changes**:
- Modularize functions
- Add error handling
- Clean file paths
- Add configuration management

### Web Integration
**From**: `enhanced_web_integration.py`
**To**: `src/shipboard_fire_ai/api/main.py`
**Changes**:
- Convert to FastAPI
- Add proper models
- Improve error handling
- Add authentication (future)

### Feedback System
**From**: Multiple feedback files
**To**: `src/shipboard_fire_ai/core/feedback_system.py`
**Changes**:
- Consolidate functionality
- Add database integration
- Improve data validation
- Add analytics

## 🧪 **Testing Strategy**

### Test Coverage Requirements
1. **Core DQN**: >90% coverage
2. **Training Pipeline**: >85% coverage
3. **API Endpoints**: >95% coverage
4. **Feedback System**: >90% coverage

### Test Types
```bash
tests/
├── unit/           # Individual component tests
├── integration/    # Component interaction tests
├── api/           # API endpoint tests
└── e2e/           # End-to-end scenarios
```

## 🚀 **CI/CD Strategy**

### Simple, Working Pipeline
```yaml
name: Shipboard Fire Response AI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest pytest-cov
    - name: Test
      run: pytest --cov=src
```

## 📊 **Success Metrics**

### Repository Quality
- ✅ All CI/CD passes
- ✅ No sensitive data
- ✅ Clean commit history
- ✅ Comprehensive documentation
- ✅ >85% test coverage

### Functionality
- ✅ Enhanced DQN working
- ✅ Training pipeline operational
- ✅ API endpoints responding
- ✅ Feedback system collecting data
- ✅ Web integration functional

---

**Status**: Ready for clean repository creation
**Timeline**: 3-4 days for complete migration
**Risk Level**: Low (clean start eliminates legacy issues)
