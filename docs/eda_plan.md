# Exploratory Data Analysis (EDA) Plan
## AlphaCare Insurance Solutions - Task 1

---

## 🎯 Objectives

1. Understand the structure and quality of the insurance dataset
2. Identify patterns in loss ratios across different dimensions
3. Detect data quality issues and outliers
4. Generate insights for business decision-making
5. Formulate hypotheses for statistical testing in Task 3
6. Prepare data for predictive modeling in Task 4

---

## 📋 EDA Methodology

### Phase 1: Data Structure Review

#### 1.1 Initial Data Loading
- Load the insurance dataset from `data/raw/insurance.csv`
- Display first and last 10 rows
- Check dataset dimensions (rows × columns)
- List all column names and their order

#### 1.2 Data Types Assessment
- Review data types for each column
- Identify columns that need type conversion:
  - Date columns → datetime
  - Categorical columns → category
  - Numeric columns → float/int
- Document memory usage before and after optimization

#### 1.3 Basic Information
- Generate dataset info summary
- Count total records
- Identify unique identifiers (PolicyID, UnderwrittenCoverID)
- Check for duplicate records

---

### Phase 2: Missing Values Analysis

#### 2.1 Missing Value Detection
- Calculate missing value count per column
- Calculate missing value percentage per column
- Visualize missing values with heatmap
- Identify columns with >50% missing data

#### 2.2 Missing Value Patterns
- Analyze if missing values are:
  - Missing Completely at Random (MCAR)
  - Missing at Random (MAR)
  - Missing Not at Random (MNAR)
- Check correlations between missing values across columns
- Document business reasons for missing data

#### 2.3 Missing Value Treatment Strategy
- **Critical fields** (TotalPremium, TotalClaims): Flag for investigation
- **Demographic fields**: Consider mode imputation or "Unknown" category
- **Vehicle attributes**: Investigate if missing indicates specific vehicle types
- **Optional fields**: Document and proceed with analysis

---

### Phase 3: Data Type Corrections

#### 3.1 Date/Time Conversions
- Convert `TransactionMonth` to datetime
- Extract year, month, quarter for temporal analysis
- Validate date ranges (Feb 2014 - Aug 2015)

#### 3.2 Categorical Conversions
- Convert string columns to category dtype:
  - Province, Gender, VehicleType
  - MaritalStatus, Title, Language
  - CoverType, CoverCategory, Product
- Reduce memory footprint

#### 3.3 Numeric Conversions
- Ensure financial columns are float64:
  - TotalPremium, TotalClaims
  - SumInsured, CalculatedPremiumPerTerm
- Ensure count columns are int:
  - NumberOfDoors, Cylinders
  - NumberOfVehiclesInFleet

---

### Phase 4: Summary Statistics

#### 4.1 Descriptive Statistics
- Generate summary statistics for numeric columns:
  - Mean, median, mode
  - Standard deviation, variance
  - Min, max, range
  - 25th, 50th, 75th percentiles

#### 4.2 Categorical Variable Summaries
- Value counts for key categorical variables:
  - Province distribution
  - Gender distribution
  - VehicleType distribution
  - CoverType distribution
- Calculate percentages and cumulative percentages

#### 4.3 Financial Metrics Overview
- **TotalPremium**: Distribution, central tendency, spread
- **TotalClaims**: Distribution, central tendency, spread
- **SumInsured**: Distribution across policies
- Identify zero-claim policies vs. policies with claims

---

### Phase 5: Loss Ratio Computation

#### 5.1 Overall Loss Ratio
```
Loss Ratio = Total Claims / Total Premium
```
- Calculate aggregate loss ratio for entire dataset
- Interpret business meaning (profitability indicator)

#### 5.2 Loss Ratio by Province
- Group by Province
- Calculate sum of TotalClaims and TotalPremium per province
- Compute loss ratio per province
- Rank provinces by loss ratio
- Visualize with horizontal bar chart

#### 5.3 Loss Ratio by VehicleType
- Group by VehicleType
- Calculate loss ratio per vehicle type
- Identify high-risk and low-risk vehicle categories
- Visualize with bar chart

#### 5.4 Loss Ratio by Gender
- Group by Gender
- Calculate loss ratio by gender
- Test for significant differences
- Visualize with bar chart

#### 5.5 Loss Ratio by Other Dimensions
- **MaritalStatus**: Single vs. Married
- **CoverType**: Comprehensive vs. Third Party
- **NewVehicle**: New vs. Used
- **AlarmImmobiliser**: With vs. Without security features

---

### Phase 6: Claim Frequency and Severity

#### 6.1 Claim Frequency
```
Claim Frequency = Number of Claims / Number of Policies
```
- Count policies with claims (TotalClaims > 0)
- Calculate claim frequency overall
- Calculate claim frequency by:
  - Province
  - VehicleType
  - Gender
  - Age of vehicle (current year - RegistrationYear)

#### 6.2 Claim Severity
```
Claim Severity = Average Claim Amount (for policies with claims)
```
- Filter policies with TotalClaims > 0
- Calculate average claim amount
- Calculate claim severity by:
  - Province
  - VehicleType
  - SumInsured brackets

#### 6.3 Combined Frequency-Severity Analysis
- Create 2×2 matrix:
  - High Frequency, High Severity → Highest Risk
  - High Frequency, Low Severity → Moderate Risk
  - Low Frequency, High Severity → Moderate Risk
  - Low Frequency, Low Severity → Lowest Risk
- Map customer segments to risk quadrants

---

### Phase 7: Outlier Detection

#### 7.1 Statistical Outlier Detection
- **IQR Method** for numeric columns:
  - Calculate Q1, Q3, IQR
  - Define outliers as values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR
- Apply to:
  - TotalPremium
  - TotalClaims
  - SumInsured
  - CalculatedPremiumPerTerm

#### 7.2 Visualization-Based Outlier Detection
- **Box plots** for:
  - TotalClaims by VehicleType
  - TotalPremium by Province
  - SumInsured distribution
- **Scatter plots**:
  - TotalPremium vs. TotalClaims
  - SumInsured vs. TotalPremium

#### 7.3 Domain-Based Outlier Detection
- **Business rules**:
  - TotalClaims > SumInsured (investigate)
  - TotalPremium = 0 but TotalClaims > 0 (data error)
  - Negative values in financial columns
  - RegistrationYear > 2015 (future dates)

#### 7.4 Outlier Treatment Strategy
- **Keep**: Legitimate high-value policies
- **Cap**: Extreme values affecting analysis
- **Investigate**: Potential data errors
- **Document**: All outlier decisions

---

### Phase 8: Bivariate Relationships

#### 8.1 Correlation Analysis
- Compute correlation matrix for numeric variables
- Visualize with heatmap
- Identify strong correlations (|r| > 0.7):
  - TotalPremium vs. SumInsured
  - Cylinders vs. cubiccapacity
  - kilowatts vs. cubiccapacity

#### 8.2 Premium vs. Claims Relationship
- Scatter plot: TotalPremium vs. TotalClaims
- Add regression line
- Calculate correlation coefficient
- Identify policies with high claims relative to premiums

#### 8.3 Categorical vs. Numeric Relationships
- **Province vs. TotalPremium**: Box plot
- **Gender vs. TotalClaims**: Box plot
- **VehicleType vs. Loss Ratio**: Bar chart
- **CoverType vs. TotalPremium**: Violin plot

---

### Phase 9: Time Series Trends

#### 9.1 Monthly Aggregation
- Group by TransactionMonth
- Aggregate:
  - Total premiums collected
  - Total claims paid
  - Number of policies
  - Average premium per policy

#### 9.2 Trend Analysis
- **Line plot**: Monthly TotalPremium and TotalClaims
- Identify:
  - Seasonal patterns
  - Growth trends
  - Anomalous months

#### 9.3 Loss Ratio Over Time
- Calculate monthly loss ratio
- Plot time series
- Identify months with highest/lowest loss ratios
- Investigate causes of spikes

---

### Phase 10: Creative Visualizations

#### 10.1 Geographic Heatmap
- **Visualization**: Choropleth map of South Africa
- **Metric**: Loss ratio by province
- **Insight**: Geographic risk distribution
- **Tool**: Plotly or Folium

#### 10.2 Risk Segmentation Matrix
- **Visualization**: 2D scatter plot
- **X-axis**: Claim Frequency
- **Y-axis**: Claim Severity
- **Color**: Province or VehicleType
- **Size**: Total Premium volume
- **Insight**: Identify profitable vs. risky segments

#### 10.3 Premium vs. Claims Bubble Chart
- **Visualization**: Bubble chart
- **X-axis**: Total Premium (by segment)
- **Y-axis**: Total Claims (by segment)
- **Bubble size**: Number of policies
- **Color**: Loss ratio
- **Insight**: Segment profitability and volume

---

## 🔍 Specific Analysis Questions

### Business Questions to Answer

1. **Which provinces have the lowest loss ratios?**
   - Target for marketing expansion

2. **Which vehicle types are most profitable?**
   - Focus underwriting efforts

3. **Do security features (AlarmImmobiliser) reduce claims?**
   - Justify premium discounts

4. **Is there a gender-based risk difference?**
   - Hypothesis for Task 3

5. **Do newer vehicles have lower claim rates?**
   - Inform pricing strategy

6. **What is the optimal coverage type mix?**
   - Product portfolio optimization

7. **Are there seasonal patterns in claims?**
   - Resource planning for claims processing

8. **Which customer segments have high premiums but low claims?**
   - VIP customer identification

---

## 📊 Deliverables

### 1. Jupyter Notebook
- `notebooks/task1_eda.ipynb`
- Well-documented with markdown cells
- Clean, reproducible code
- All outputs visible

### 2. Visualizations
- Saved to `outputs/plots/`
- High-resolution PNG format
- Properly labeled axes and titles
- Color-blind friendly palettes

### 3. Insights Document
- `docs/insights.md`
- Business-friendly language
- Key findings highlighted
- Actionable recommendations

### 4. Data Quality Report
- Missing value summary
- Outlier summary
- Data type issues
- Recommended cleaning steps

---

## 🛠️ Tools and Libraries

### Core Libraries
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
```

### Visualization Settings
```python
# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Color palette
colors = sns.color_palette("husl", 10)
```

---

## ✅ Success Criteria

- [ ] All data quality issues documented
- [ ] Loss ratios calculated for all key dimensions
- [ ] Minimum 10 visualizations created
- [ ] 3 creative visualizations implemented
- [ ] Business insights documented
- [ ] Hypotheses formulated for Task 3
- [ ] Code is clean and well-commented
- [ ] All outputs reproducible

---

## 🚀 Next Steps (Task 2)

1. Implement DVC for data versioning
2. Create automated data quality checks
3. Build data cleaning pipeline
4. Version control cleaned datasets
5. Prepare for A/B hypothesis testing

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Author**: AlphaCare Analytics Team
