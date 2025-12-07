# Segmentation Framework for Low-Risk Customer Identification

## Executive Summary

This framework defines a systematic approach to segment AlphaCare Insurance Solutions (ACIS) customers into risk categories, with a primary focus on identifying **low-risk customer groups** for targeted marketing and optimized pricing strategies.

The segmentation uses a **multi-dimensional approach** combining demographic, geographic, vehicle, behavioral, and insurance plan attributes to create actionable customer segments.

---

## Segmentation Dimensions

### 1. Demographic Attributes

#### Gender
- **Low-Risk Indicator**: Female drivers (historically lower claim rates)
- **High-Risk Indicator**: Male drivers in younger age brackets
- **Rationale**: Industry data shows gender-based risk differences

#### Marital Status
- **Low-Risk Indicator**: Married customers
- **High-Risk Indicator**: Single customers
- **Rationale**: Married individuals tend to exhibit more cautious driving behavior

#### Legal Type
- **Low-Risk Indicator**: Individual policyholders
- **Medium-Risk**: Close Corporations (business use)
- **High-Risk Indicator**: Complex legal entities with fleet operations
- **Rationale**: Individual ownership correlates with personal care and maintenance

#### Title
- **Low-Risk Indicator**: Professional titles (Dr, Prof)
- **Medium-Risk**: Standard titles (Mr, Mrs, Ms)
- **Rationale**: Professional status may correlate with risk awareness

---

### 2. Geographic Attributes

#### Province
- **Low-Risk Provinces**: Western Cape, Gauteng (urban, well-developed infrastructure)
- **Medium-Risk Provinces**: KwaZulu-Natal, Eastern Cape
- **High-Risk Provinces**: Provinces with higher crime rates or poor road infrastructure
- **Rationale**: Geographic risk varies by infrastructure quality, crime rates, and traffic density

#### Cresta Zones
- **Low-Risk Zones**: Suburban residential areas (MainCrestaZone analysis required)
- **High-Risk Zones**: High-crime areas, industrial zones
- **Rationale**: Cresta zones are insurance industry standard for geographic risk assessment

#### Postal Code
- **Usage**: Fine-grained risk differentiation within provinces
- **Validation**: Cross-reference with claims data to identify low-risk postal codes

---

### 3. Vehicle Attributes

#### Vehicle Type
- **Low-Risk Types**: 
  - Sedan (family vehicles)
  - Light Commercial Vehicles (business use, well-maintained)
- **Medium-Risk Types**: SUVs, Hatchbacks
- **High-Risk Types**: 
  - Motorcycles
  - High-performance sports cars
  - Taxis (commercial high-mileage use)
- **Rationale**: Vehicle type correlates with usage patterns and accident risk

#### Vehicle Age
- **Low-Risk Age**: 2-5 years old (modern safety features, still reliable)
- **Medium-Risk Age**: 6-10 years old
- **High-Risk Age**: 
  - 0-1 years (inexperienced with new vehicle)
  - 10+ years (maintenance issues, outdated safety)
- **Calculation**: Current Year - RegistrationYear

#### Vehicle Value (SumInsured)
- **Low-Risk Range**: R150,000 - R400,000 (mid-range vehicles)
- **Medium-Risk Range**: R400,000 - R800,000
- **High-Risk Range**: 
  - < R150,000 (older, less safe vehicles)
  - > R800,000 (luxury vehicles, theft targets)
- **Rationale**: Mid-range vehicles balance safety and theft risk

#### Security Features
- **Low-Risk Indicators**:
  - AlarmImmobiliser = Yes
  - TrackingDevice = Yes
  - Both security features present
- **High-Risk Indicators**: No security features
- **Rationale**: Security features reduce theft and aid recovery

#### Vehicle Condition
- **Low-Risk Indicators**:
  - NewVehicle = No (experienced ownership)
  - WrittenOff = No
  - Rebuilt = No
  - Converted = No
- **High-Risk Indicators**: Any history of write-off, rebuild, or conversion
- **Rationale**: Vehicle history affects reliability and safety

---

### 4. Behavioral Attributes

#### Claims History
- **Low-Risk Indicator**: 
  - TotalClaims = 0 (no claims in period)
  - ClaimFrequency = 0
- **Medium-Risk**: 1 small claim
- **High-Risk Indicator**: Multiple claims or high-value claims
- **Rationale**: Past claims predict future claims

#### Payment Frequency (TermFrequency)
- **Low-Risk Indicator**: Annual payment (financial stability)
- **Medium-Risk**: Monthly payment
- **Rationale**: Annual payment suggests financial discipline and commitment

#### Capital Outstanding
- **Low-Risk Indicator**: No outstanding finance (CapitalOutstanding = No)
- **Medium-Risk**: Financed vehicle
- **Rationale**: Owned vehicles may receive better maintenance

---

### 5. Insurance Plan Attributes

#### Cover Type
- **Low-Risk Indicator**: 
  - Comprehensive coverage (suggests vehicle value and care)
  - Windscreen coverage (preventive maintenance)
- **Medium-Risk**: Third Party Fire & Theft
- **High-Risk Indicator**: Third Party Only (minimum coverage)
- **Rationale**: Comprehensive coverage correlates with vehicle care

#### Excess Selected
- **Low-Risk Indicator**: Moderate to high excess (R2,500 - R7,500)
- **Medium-Risk**: Standard excess (R1,000 - R2,500)
- **High-Risk Indicator**: No excess or very low excess
- **Rationale**: Higher excess suggests confidence in risk management

#### Cover Category
- **Low-Risk Categories**: Own Damage, Windscreen
- **Medium-Risk Categories**: Third Party
- **High-Risk Categories**: Passenger Liability (commercial use)

---

## Low-Risk Segment Definition

A customer is classified as **LOW-RISK** if they meet **at least 5 of the following 8 criteria**:

1. ✅ **Demographic**: Married OR Female OR Professional Title
2. ✅ **Geographic**: Province in [Western Cape, Gauteng] AND Low-risk Cresta Zone
3. ✅ **Vehicle Type**: Sedan OR Light Commercial Vehicle
4. ✅ **Vehicle Age**: 2-5 years old
5. ✅ **Security**: Has both AlarmImmobiliser AND TrackingDevice
6. ✅ **Claims**: TotalClaims = 0 in the analysis period
7. ✅ **Coverage**: Comprehensive cover with moderate excess (≥ R2,500)
8. ✅ **Vehicle Condition**: No write-off, rebuild, or conversion history

### Scoring System
- **Low-Risk Segment**: Score ≥ 5 (meets 5+ criteria)
- **Medium-Risk Segment**: Score 3-4
- **High-Risk Segment**: Score ≤ 2

---

## High-Risk Exclusion Rules

Customers are **automatically excluded from low-risk segments** if they meet **any** of the following:

1. ❌ **Multiple Claims**: TotalClaims > 0 AND ClaimFrequency > 1
2. ❌ **High Loss Ratio**: LossRatio > 0.8 (claims exceed 80% of premiums)
3. ❌ **Vehicle History**: WrittenOff = Yes OR Rebuilt = Yes
4. ❌ **High-Risk Vehicle**: VehicleType in [Motorcycle, Sports Car, Taxi]
5. ❌ **No Security**: AlarmImmobiliser = No AND TrackingDevice = No
6. ❌ **Very Old Vehicle**: Vehicle Age > 15 years
7. ❌ **High-Risk Province**: Province in high-crime areas (data-driven identification)
8. ❌ **Minimum Coverage**: CoverType = Third Party Only

---

## Segment Validation Methodology

### 1. Loss Ratio Validation
- **Expected Low-Risk Loss Ratio**: < 0.40 (claims < 40% of premiums)
- **Expected Medium-Risk Loss Ratio**: 0.40 - 0.70
- **Expected High-Risk Loss Ratio**: > 0.70

**Validation Process**:
```python
segment_loss_ratios = df.groupby('RiskSegment').agg({
    'TotalClaims': 'sum',
    'TotalPremium': 'sum'
})
segment_loss_ratios['LossRatio'] = (
    segment_loss_ratios['TotalClaims'] / segment_loss_ratios['TotalPremium']
)
```

### 2. Statistical Significance Testing
- **Test**: ANOVA to compare loss ratios across segments
- **Null Hypothesis**: No significant difference in loss ratios between segments
- **Alternative Hypothesis**: Low-risk segment has significantly lower loss ratio
- **Significance Level**: α = 0.05

### 3. Segment Size Validation
- **Minimum Segment Size**: Each segment should contain ≥ 5% of total customers
- **Maximum Segment Size**: No segment should exceed 60% (ensures differentiation)
- **Rationale**: Segments must be large enough for statistical power but distinct enough for targeting

### 4. Business Metric Validation

#### Profitability Check
```python
segment_metrics = df.groupby('RiskSegment').agg({
    'TotalPremium': ['sum', 'mean'],
    'TotalClaims': ['sum', 'mean'],
    'PolicyID': 'nunique'
})
segment_metrics['Profit'] = (
    segment_metrics['TotalPremium']['sum'] - segment_metrics['TotalClaims']['sum']
)
```

#### Retention Potential
- Low-risk segments should show:
  - Higher average premium (willing to pay for quality)
  - Lower claim frequency (less friction)
  - Longer policy duration (loyalty indicator)

### 5. Temporal Stability
- **Test**: Validate segment performance across different time periods
- **Method**: Split data by TransactionMonth and compare loss ratios
- **Requirement**: Low-risk segment should maintain LossRatio < 0.40 across all quarters

---

## Implementation Guidelines

### Data Requirements
1. **Completeness**: Segments require non-missing values in key fields:
   - Province, VehicleType, RegistrationYear
   - TotalPremium, TotalClaims
   - AlarmImmobiliser, TrackingDevice
   - CoverType, ExcessSelected

2. **Data Quality**: 
   - Remove records with TotalPremium = 0
   - Handle missing Gender/MaritalStatus with separate "Unknown" category
   - Validate date fields for temporal features

### Segmentation Algorithm
```python
def assign_risk_segment(row):
    score = 0
    
    # Demographic (1 point)
    if row['MaritalStatus'] == 'Married' or row['Gender'] == 'Female':
        score += 1
    
    # Geographic (1 point)
    if row['Province'] in ['Western Cape', 'Gauteng']:
        score += 1
    
    # Vehicle Type (1 point)
    if row['VehicleType'] in ['Sedan', 'Light Commercial Vehicle']:
        score += 1
    
    # Vehicle Age (1 point)
    if 2 <= row['VehicleAge'] <= 5:
        score += 1
    
    # Security (1 point)
    if row['AlarmImmobiliser'] == 'Yes' and row['TrackingDevice'] == 'Yes':
        score += 1
    
    # Claims (1 point)
    if row['TotalClaims'] == 0:
        score += 1
    
    # Coverage (1 point)
    if row['CoverType'] == 'Comprehensive' and row['ExcessAmount'] >= 2500:
        score += 1
    
    # Vehicle Condition (1 point)
    if row['WrittenOff'] == 'No' and row['Rebuilt'] == 'No':
        score += 1
    
    # Apply exclusion rules
    if (row['TotalClaims'] > 0 and row['ClaimFrequency'] > 1) or \
       (row['LossRatio'] > 0.8) or \
       (row['WrittenOff'] == 'Yes') or \
       (row['VehicleType'] in ['Motorcycle', 'Taxi']) or \
       (row['VehicleAge'] > 15):
        return 'High-Risk'
    
    # Assign segment based on score
    if score >= 5:
        return 'Low-Risk'
    elif score >= 3:
        return 'Medium-Risk'
    else:
        return 'High-Risk'
```

---

## Expected Outcomes

### Segment Distribution (Estimated)
- **Low-Risk**: 25-35% of customers
- **Medium-Risk**: 40-50% of customers
- **High-Risk**: 20-30% of customers

### Performance Metrics
| Segment | Expected Loss Ratio | Expected Avg Premium | Expected Claim Frequency |
|---------|-------------------|---------------------|------------------------|
| Low-Risk | < 0.40 | R 3,500 - R 5,000 | < 15% |
| Medium-Risk | 0.40 - 0.70 | R 2,500 - R 4,000 | 15% - 30% |
| High-Risk | > 0.70 | R 1,500 - R 3,000 | > 30% |

---

## Next Steps

1. **Implementation**: Apply segmentation logic in `preprocess.py`
2. **Validation**: Run validation tests on segment performance
3. **Refinement**: Adjust criteria based on actual loss ratio results
4. **Business Review**: Present segments to stakeholders for approval
5. **Deployment**: Integrate segments into pricing and marketing systems

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Owner**: Data Science Team - ACIS Risk Analytics Project
