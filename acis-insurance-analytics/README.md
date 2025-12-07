# ACIS Insurance Analytics

## 📊 Project Overview

This project analyzes insurance data to derive actionable insights for **AlphaCare Insurance Solutions (ACIS)**. The goal is to optimize marketing strategies and identify low-risk targets for premium reduction by analyzing historical insurance claim data.

## 🎯 Business Problem

AlphaCare Insurance Solutions (ACIS) faces challenges in:
- **Risk Assessment**: Identifying low-risk client segments for targeted premium optimization
- **Marketing Optimization**: Understanding which features correlate with lower claims
- **Profitability**: Balancing competitive pricing with risk management
- **Customer Retention**: Offering attractive rates to low-risk customers while maintaining profitability

This project aims to analyze historical insurance data to discover "low-risk" targets for potential premium reductions and improved marketing strategies.

## 📁 Data Description

The dataset contains historical insurance claim data with the following key features:

### Policy Information
- **UnderwrittenCoverID**: Unique identifier for insurance cover
- **PolicyID**: Unique policy identifier
- **TransactionMonth**: Month of transaction

### Client Demographics
- **IsVATRegistered**: VAT registration status
- **Citizenship**: Client citizenship
- **LegalType**: Legal entity type
- **Title**, **Language**, **Bank**, **AccountType**: Client attributes
- **MaritalStatus**, **Gender**: Personal demographics
- **Country**, **Province**, **PostalCode**: Geographic information

### Vehicle Information
- **MainCrestaZone**, **SubCrestaZone**: Geographic risk zones
- **ItemType**: Type of insured item
- **make**, **Model**, **VehicleType**: Vehicle specifications
- **RegistrationYear**: Year of vehicle registration
- **Cylinders**, **cubiccapacity**: Engine specifications
- **kilowatts**, **NumberOfDoors**: Vehicle attributes
- **VehicleIntroDate**: Vehicle introduction date
- **CustomValueEstimate**: Estimated vehicle value
- **AlarmImmobiliser**, **TrackingDevice**: Security features

### Coverage & Claims
- **CapitalOutstanding**: Outstanding capital amount
- **NewVehicle**, **WrittenOff**, **Rebuilt**: Vehicle status flags
- **Converted**, **CrossBorder**: Policy attributes
- **NumberOfVehiclesInFleet**: Fleet size
- **SumInsured**: Total insured amount
- **TermFrequency**: Payment frequency
- **CalculatedPremiumPerTerm**: Premium amount
- **ExcessSelected**: Excess/deductible amount
- **CoverCategory**, **CoverType**, **CoverGroup**: Coverage classification
- **Section**: Insurance section
- **Product**: Insurance product type
- **StatutoryClass**, **StatutoryRiskType**: Regulatory classification
- **TotalPremium**, **TotalClaims**: Financial metrics

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.9+**: Primary programming language
- **Jupyter Notebook**: Interactive data analysis and visualization
- **Git & GitHub**: Version control and collaboration

### Data Analysis & ML
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms
- **scipy**: Statistical analysis

### Visualization
- **matplotlib**: Static visualizations
- **seaborn**: Statistical data visualization
- **plotly**: Interactive visualizations

### Data Versioning
- **DVC (Data Version Control)**: Dataset versioning and pipeline management

### CI/CD
- **GitHub Actions**: Automated testing and linting
- **pytest**: Unit testing framework
- **flake8**: Code linting
- **black**: Code formatting

## 🚀 Getting Started

### Prerequisites
```bash
python --version  # Python 3.9 or higher
git --version
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/acis-insurance-analytics.git
cd acis-insurance-analytics
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Set up DVC** (if using data versioning)
```bash
dvc init
dvc remote add -d storage path/to/remote/storage
```

## 📊 Running Exploratory Data Analysis (EDA)

### Option 1: Jupyter Notebooks (Recommended)
```bash
# Start Jupyter Lab
jupyter lab

# Navigate to notebooks/eda/ and open:
# - 01_data_overview.ipynb
# - 02_univariate_analysis.ipynb
# - 03_bivariate_analysis.ipynb
# - 04_missing_data_analysis.ipynb
```

### Option 2: Python Scripts
```bash
# Run complete EDA pipeline
python scripts/run_eda.py

# Run specific analysis modules
python scripts/eda/data_summary.py
python scripts/eda/visualizations.py
```

### Option 3: Automated Report Generation
```bash
# Generate HTML EDA report
python scripts/generate_eda_report.py --output reports/eda_report.html
```

## 🌿 Branching Strategy

We follow **Git Flow** branching strategy for organized development:

### Main Branches
- **`main`**: Production-ready code, always stable
- **`develop`**: Integration branch for features

### Supporting Branches

#### Feature Branches
- **Naming**: `task-{number}` or `feature/{feature-name}`
- **Purpose**: Develop new features or tasks
- **Branch from**: `develop`
- **Merge into**: `develop`

```bash
# Create feature branch
git checkout develop
git checkout -b task-1

# Work on feature, then merge back
git checkout develop
git merge task-1 --no-ff
```

#### Hotfix Branches
- **Naming**: `hotfix/{issue-name}`
- **Purpose**: Quick fixes for production issues
- **Branch from**: `main`
- **Merge into**: `main` and `develop`

### Workflow Example
```bash
# Start new task
git checkout develop
git pull origin develop
git checkout -b task-1

# Make changes and commit
git add .
git commit -m "feat: implement data loading module"

# Push to remote
git push -u origin task-1

# Create Pull Request on GitHub
# After review and approval, merge to develop
```

### Commit Message Convention
We use **Conventional Commits**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

## 📂 Project Structure

```
acis-insurance-analytics/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── data/
│   ├── raw/                       # Original, immutable data
│   ├── processed/                 # Cleaned, transformed data
│   └── external/                  # External reference data
├── notebooks/
│   ├── eda/                       # Exploratory data analysis
│   ├── modeling/                  # Model development
│   └── experiments/               # Ad-hoc experiments
├── scripts/
│   ├── eda/                       # EDA automation scripts
│   ├── preprocessing/             # Data preprocessing
│   ├── modeling/                  # Model training scripts
│   └── utils/                     # Utility functions
├── tests/
│   ├── test_preprocessing.py
│   ├── test_models.py
│   └── test_utils.py
├── reports/
│   ├── figures/                   # Generated visualizations
│   └── eda_report.html           # EDA reports
├── models/
│   └── saved_models/             # Trained model artifacts
├── .gitignore
├── .dvcignore
├── requirements.txt
├── setup.py
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_preprocessing.py
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Your Name - [GitHub Profile](https://github.com/YOUR_USERNAME)

## 📧 Contact

For questions or feedback, please open an issue on GitHub or contact [your.email@example.com]

---

**Last Updated**: December 2025
