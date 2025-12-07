# AlphaCare Insurance Solutions (ACIS) - Risk Analytics Project

## 📋 Project Overview

This project analyzes South African car insurance data (February 2014 - August 2015) to identify low-risk customer segments, optimize marketing strategies, and improve premium pricing models for AlphaCare Insurance Solutions.

### Business Objectives
- Identify low-risk customer segments for targeted marketing
- Analyze loss ratio patterns across different dimensions
- Assess data quality and prepare for predictive modeling
- Test hypotheses about risk factors
- Build predictive models for optimal premium pricing

### Key Business Metric
**Loss Ratio** = Total Claims / Total Premium

A lower loss ratio indicates more profitable customer segments.

---

## 📊 Dataset Overview

**Source**: South African car insurance data  
**Period**: February 2014 - August 2015  
**Records**: ~1M policy transactions

### Data Fields

#### Policy Information
- `UnderwrittenCoverID`: Unique policy identifier
- `PolicyID`: Policy number
- `TransactionMonth`: Month of transaction

#### Client Demographics
- `IsVATRegistered`: VAT registration status
- `Citizenship`: Citizenship status
- `LegalType`: Legal entity type
- `Title`: Client title
- `Language`: Preferred language
- `Bank`: Banking institution
- `AccountType`: Type of bank account
- `MaritalStatus`: Marital status
- `Gender`: Gender

#### Location
- `Country`: Country
- `Province`: Province
- `PostalCode`: Postal code
- `MainCrestaZone`, `SubCrestaZone`: Geographic risk zones

#### Vehicle Attributes
- `ItemType`: Type of insured item
- `mmcode`: Make and model code
- `VehicleType`: Vehicle category
- `RegistrationYear`: Year of registration
- `make`: Vehicle manufacturer
- `Model`: Vehicle model
- `Cylinders`: Engine cylinders
- `cubiccapacity`: Engine capacity
- `kilowatts`: Engine power
- `bodytype`: Body type
- `NumberOfDoors`: Number of doors
- `VehicleIntroDate`: Introduction date
- `CustomValueEstimate`: Estimated value
- `AlarmImmobiliser`: Security features
- `TrackingDevice`: GPS tracking
- `CapitalOutstanding`: Outstanding finance
- `NewVehicle`: New/used status
- `WrittenOff`: Write-off status
- `Rebuilt`: Rebuild status
- `Converted`: Conversion status
- `CrossBorder`: Cross-border usage
- `NumberOfVehiclesInFleet`: Fleet size

#### Insurance Plan
- `SumInsured`: Insured amount
- `TermFrequency`: Payment frequency
- `CalculatedPremiumPerTerm`: Premium per term
- `ExcessSelected`: Excess amount
- `CoverCategory`: Coverage category
- `CoverType`: Type of cover
- `CoverGroup`: Cover group
- `Section`: Policy section
- `Product`: Insurance product
- `StatutoryClass`, `StatutoryRiskType`: Statutory classifications

#### Financial Metrics
- `TotalPremium`: Total premium paid
- `TotalClaims`: Total claims amount

---

## 🛠️ Technical Stack

### Core Technologies
- **Python 3.8+**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib & Seaborn**: Data visualization
- **Jupyter Notebook**: Interactive analysis

### Development Tools
- **Git**: Version control
- **GitHub**: Code hosting and collaboration
- **DVC**: Data version control
- **GitHub Actions**: CI/CD pipeline

### Future Stack (Tasks 2-4)
- **Scikit-learn**: Machine learning models
- **Scipy**: Statistical testing
- **Statsmodels**: Statistical analysis

---

## 📁 Project Structure

```
week_3/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── data/
│   └── raw/
│       └── insurance.csv          # Raw data (tracked by DVC)
├── notebooks/
│   └── task1_eda.ipynb           # Exploratory Data Analysis
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Data loading utilities
│   ├── data_cleaning.py          # Data cleaning functions
│   └── visualization.py          # Visualization utilities
├── outputs/
│   └── plots/                    # Generated visualizations
├── docs/
│   ├── eda_plan.md              # EDA methodology
│   ├── insights.md              # Key findings
│   └── interim_report.md        # Task 1 report
├── .gitignore
├── .dvcignore
├── README.md
└── requirements.txt
```

---

## 🔄 Git Workflow & Branching Strategy

### Branch Structure
- `main`: Production-ready code
- `task-1`: EDA and project setup
- `task-2`: Data quality assessment
- `task-3`: A/B hypothesis testing
- `task-4`: Predictive modeling

### Workflow
1. Create feature branch from `main`
2. Implement changes with atomic commits
3. Push to GitHub
4. Create Pull Request
5. Code review and merge to `main`

### Commit Message Convention
```
<type>: <subject>

<body>

Examples:
feat: add loss ratio calculation by province
fix: correct missing value handling in gender field
docs: update EDA insights with outlier analysis
```

---

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Git
git --version
```

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd week_3
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize DVC**
```bash
dvc init
dvc pull  # Pull data from remote storage
```

### Running EDA

1. **Navigate to notebooks directory**
```bash
cd notebooks
```

2. **Launch Jupyter Notebook**
```bash
jupyter notebook task1_eda.ipynb
```

3. **Run all cells** to generate:
   - Summary statistics
   - Loss ratio analysis
   - Visualizations (saved to `outputs/plots/`)
   - Data quality reports

### Running Tests
```bash
# Run linting
flake8 src/

# Run unit tests (when available)
pytest tests/
```

---

## 📈 Key Analyses

### Task 1: Exploratory Data Analysis
- Data structure and quality assessment
- Missing value analysis
- Outlier detection
- Summary statistics
- Loss ratio by Province, VehicleType, Gender
- Claim frequency and severity metrics
- Time series trends
- Correlation analysis

### Task 2: Data Quality Assessment (Upcoming)
- Data versioning with DVC
- Advanced data quality checks
- Data cleaning pipeline

### Task 3: A/B Hypothesis Testing (Upcoming)
- Risk differences across provinces
- Risk differences between zip codes
- Margin differences between zip codes
- Risk differences between genders

### Task 4: Predictive Modeling (Upcoming)
- Feature engineering
- Model building (Linear Regression, Random Forest, XGBoost)
- Model evaluation and interpretation
- SHAP analysis

---

## 📊 Key Findings (Task 1)

> See `docs/insights.md` for detailed findings

**Preliminary Insights:**
- Loss ratios vary significantly across provinces
- Certain vehicle types show higher claim frequencies
- Data quality issues identified in specific fields
- Temporal patterns observed in claims and premiums

---

## 👥 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit a Pull Request

---

## 📝 License

This project is part of the 10 Academy training program.

---

## 📧 Contact

For questions or feedback, please contact the project team.

---

## 🗓️ Project Timeline

- **Week 1**: Task 1 - EDA and Project Setup ✅
- **Week 2**: Task 2 - Data Quality & DVC
- **Week 3**: Task 3 - A/B Hypothesis Testing
- **Week 4**: Task 4 - Predictive Modeling

---

**Last Updated**: December 2025
