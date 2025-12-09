# Technical Accuracy Checklist for Portfolio Projects

Use this checklist BEFORE publishing or claiming any technical capability.

## Documentation Phase

- [ ] **Exact Model Name**
  - Specify full name: "ARIMA(1,1,1)" not "ARIMA" not "forecasting"
  - Include library: "statsmodels.tsa.arima.model.ARIMA"
  - Version: "statsmodels==0.14.0"

- [ ] **Implementation Status**
  - [ ] Installed? Check `requirements.txt` or `package.json`
  - [ ] Imported? Check actual import statement in code
  - [ ] Used? Verify function calls
  - [ ] Tested? Run sample data through model

- [ ] **README Accuracy**
  - [ ] Model name matches actual code
  - [ ] No generic terms ("advanced modeling", "ML algorithm")
  - [ ] Accuracy claims are measured/tested
  - [ ] Fallbacks documented if applicable

- [ ] **Code Comments**
  ```python
  # ✅ GOOD:
  # Using ARIMA(1,1,1) from statsmodels (v0.14.0)
  # Implemented: 2025-11-23
  # Accuracy: ±500 CFS on 7-day forecast
  
  # ❌ BAD:
  # Advanced statistical forecasting model
  ```

---

## Before Publishing/Deploying

### Website/HTML
- [ ] Search page HTML for model name
- [ ] Verify it matches actual implementation
- [ ] Test that example data shown is realistic
- [ ] Include methodology section (not just overview)

### GitHub README
- [ ] Model name in first paragraph
- [ ] Link to actual code file
- [ ] Sample API response showing model version
- [ ] Comparison with alternatives (if applicable)

### Documentation Files
- [ ] Create architecture diagram showing data flow
- [ ] Document input/output formats
- [ ] Include performance metrics (not just claims)
- [ ] List any limitations or fallbacks

---

## Database/API Verification

If returning predictions via API:

- [ ] Response includes `model_version` field
  ```json
  {
    "prediction_id": 1,
    "predicted_flow_cfs": 4818.0,
    "model_version": "2.0-arima",
    "confidence_intervals": [4318.0, 5318.0]
  }
  ```

- [ ] Version field updated when model changes
- [ ] Can query predictions by model version
- [ ] Historical data tagged with method used

---

## Testing & Validation

- [ ] Run test data through model
- [ ] Verify output format matches docs
- [ ] Check that fallback mechanisms work
- [ ] Document any edge cases

Example test:
```python
# Should return ARIMA prediction, not mock
response = requests.get("http://localhost:8005/api/predictions/1")
assert response.json()[0]["model_version"] == "2.0-arima"
assert "confidence_lower" in response.json()[0]
```

---

## Red Flags (Don't Publish If True)

🚩 Model name appears nowhere in code  
🚩 Only generic terms used ("forecasting", "prediction", "analysis")  
🚩 No way to verify which model was actually used  
🚩 Claims accuracy but no test data  
🚩 Different models in website vs actual code  
🚩 README says one thing, API returns another  
🚩 Can't point to specific line of code implementing claimed feature  

---

## Commit Message Template

```
feat: implement ARIMA(1,1,1) forecasting

- Replace mock predictions with statsmodels ARIMA
- Model version 2.0-arima
- Accuracy: ±500 CFS confidence intervals
- Fallback to linear trend if <3 data points
- Tested with 30-day historical data

Closes #XX
```

---

## Review Checklist for Code Review

When reviewing someone else's portfolio project:

1. **Claimed vs Actual**
   - [ ] Search code for claimed technology
   - [ ] Verify it's not mocked/stubbed
   - [ ] Check actual implementation

2. **Documentation Check**
   - [ ] README describes actual code
   - [ ] No mismatches between docs and code
   - [ ] Specific model names used

3. **Test the Claims**
   - [ ] Run the application
   - [ ] Trigger the claimed feature
   - [ ] Verify output matches description

---

## Examples

### ✅ GOOD Description
"River Access MVP uses ARIMA(1,1,1) statistical forecasting to predict 7-day river flow with confidence intervals. The model is fitted using 30 days of historical USGS discharge data via the statsmodels library. Falls back to linear trend regression if <3 data points available. Model version identifier stored in database for reproducibility."

### ❌ BAD Description  
"Advanced machine learning predictions for river conditions using sophisticated forecasting algorithms optimized for accuracy."

---

## After This Incident

This checklist prevents repeating: **Original project claimed ARIMA but used linear regression.**

Fix: Updated website documentation + created comparison document + implemented real ARIMA in new Python version.

