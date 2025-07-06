# AI-Powered Test Case Prioritization

This project demonstrates how to use machine learning (Random Forest) to prioritize software test cases based on historical and feature data, enabling smarter and more efficient test execution. It is designed for easy integration with CI/CD pipelines (e.g., Jenkins) and provides colored output for clear status reporting.

---

## Project Structure

```text
📁 ai-test-prioritization/
├── 📄 requirements.txt                 # Python dependencies
├── 📄 run_ai_test_prioritization.bat   # Batch file for running the pipeline (Jenkins-ready)
├── 📄 PROJECT_OVERVIEW.md              # Project overview and documentation
├── 📄 README.md                        # Project readme
├── 📁 src/                             # Source code root
│   ├── 📄 __init__.py                  # Marks src as a package
│   ├── 📄 main.py                      # Main entry point for the pipeline
│   ├── 📄 test_data.csv                # (Optional) Sample test data
│   ├── 📁 ai/                          # AI/ML logic
│   │   └── 📄 prioritizer.py           # ML model for prioritization
│   ├── 📁 data/                        # Data loading and preparation
│   │   └── 📄 dataset_loader.py        # Loads and prepares data
│   ├── 📁 utils/                       # Utility functions
│   │   └── 📄 helpers.py               # Helper functions (e.g., data generation)
│   └── 📁 tests/                       # Unit tests
│       └── 📄 test_prioritizer.py      # Unit tests for prioritizer
```

---

## Workflow & Components

### 1. Data Preparation
- **[helpers.py](src/utils/helpers.py)**: Contains [`generate_sample_test_data()`](src/utils/helpers.py#L22) to create a synthetic CSV dataset of test cases with features (e.g., execution time, last run status, etc.).
- **[dataset_loader.py](src/data/dataset_loader.py)**: Loads the CSV data, extracts features and labels, and prepares it for the ML model.

### 2. Model & Prioritization
- **[prioritizer.py](src/ai/prioritizer.py)**: Implements [`TestCasePrioritizer`](src/ai/prioritizer.py#L27) using `RandomForestClassifier` from scikit-learn.
    - [`train()`](src/ai/prioritizer.py#L36): Trains the model on the dataset.
    - [`prioritize()`](src/ai/prioritizer.py#L40): Predicts and sorts test cases by their likelihood of failure or importance, so high-priority tests run first.

### 3. Main Pipeline
- **[main.py](src/main.py)**: Orchestrates the workflow:
    1. Loads/generates the dataset.
    2. Trains the prioritization model.
    3. Outputs the prioritized list of test cases (with color-coded status for clarity).

### 4. Testing
- **[test_prioritizer.py](src/tests/test_prioritizer.py)**: Unit tests to verify the prioritization logic and model correctness.

### 5. CI/CD Integration
- **[run_ai_test_prioritization.bat](run_ai_test_prioritization.bat)**: Batch file to run the pipeline in Windows (Jenkins-friendly):
    - Sets up ANSI color codes for output (requires Jenkins ANSI Color plugin).
    - Runs the main script and prints colored success/failure messages based on the result.

---

## How It Works

1. **Data Generation/Loading**: If no real data is present, helpers generate a sample dataset. Otherwise, the loader reads from [`test_data.csv`](.\src\test_data.csv).
2. **Feature Extraction**: Features (e.g., test duration, last status, etc.) are extracted for ML input.
3. **Model Training**: The Random Forest model is trained to predict test case priority (e.g., likelihood of failure or business impact).
4. **Prioritization**: The model predicts and sorts test cases so the most important ones are run first.
5. **Output**: Results are printed to the console with color codes for easy reading in Jenkins or local terminals.
6. **Testing**: Unit tests ensure the prioritization logic is correct and robust.

---

## Running the Project

1. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the pipeline (locally or in Jenkins)**:
   ```sh
   run_ai_test_prioritization.bat
   ```
   - Output will be color-coded for easy status checking.

---

## Extending the Project
- Replace the sample data with real test case history for production use.
- Tune the Random Forest model or swap for another ML algorithm as needed.
- Integrate with your test runner to automatically execute prioritized tests.
- Expand features (e.g., code coverage, risk, business criticality) for smarter prioritization.

---

## Summary
This project provides a practical, extensible template for AI-driven test case prioritization, ready for CI/CD integration and further experimentation.
