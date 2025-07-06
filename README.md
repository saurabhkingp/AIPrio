# AI-Powered Test Case Prioritization

This project implements an AI-powered test case prioritization system designed to enhance the efficiency of automation testing. By leveraging machine learning techniques, the system prioritizes test cases based on their likelihood of detecting defects, thereby optimizing the testing process.

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

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ai-test-prioritization
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Overview of AI-Powered Test Case Prioritization

Test case prioritization is a technique used in software testing to arrange test cases in a specific order based on certain criteria. This project utilizes AI to analyze historical test data and predict which test cases are most likely to uncover defects. By prioritizing these test cases, teams can ensure that critical tests are executed first, leading to faster feedback and improved software quality.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
