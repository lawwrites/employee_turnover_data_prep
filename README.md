# Employee Turnover Data Preparation & Quality Assessment

---

# Executive Summary

This whitepaper documents the structured data profiling, cleaning, and preparation of Technology A’s Employee Turnover Dataset (ETD). The objective of this analysis was to improve dataset integrity prior to predictive modeling and to support the organization’s strategic goal of reducing employee churn.

A comprehensive quality assessment identified 99 duplicate records, significant formatting inconsistencies, categorical standardization issues, measurable outliers in compensation and commuting variables, and missing values across three fields. In particular, 22% of the TextMessageOptIn column contained null values, representing a material data risk for engagement analysis.

Using a reproducible Python-based cleaning pipeline, duplicate rows were removed, numeric fields were standardized, categorical inconsistencies were consolidated, outliers were treated using the Interquartile Range (IQR) method, and appropriate imputation strategies were applied to continuous variables. As a result, the dataset is now structurally consistent, analytically reliable, and suitable for downstream turnover modeling.

The primary finding of this assessment is that data quality—not modeling complexity—is the critical prerequisite for reliable churn analysis. Strengthening upstream HR data validation processes will further enhance analytical accuracy and reduce strategic risk.

---

# 1. Organizational Context

Technology A seeks to understand the drivers of employee turnover in order to reduce attrition-related financial strain.

The Employee Turnover Dataset (ETD) contains 10,199 rows and 16 columns representing demographic, compensation, employment, and behavioral attributes.

Before modeling turnover drivers, it was necessary to validate data quality and ensure consistency across all variables.

---

# 2. Data Profiling

## 2.1 Variable Classification

Variables were categorized as numeric or categorical to guide cleaning strategy.

### Numeric Variables

**Discrete:**

* EmployeeNumber
* NumCompaniesPreviouslyWorked

**Continuous:**

* HourlyRate
* HoursWeekly
* AnnualSalary
* DrivingCommuterDistance
* AnnualProfessionalDevHrs
* Age
* Tenure

### Categorical Variables

**Nominal:**

* Turnover
* CompensationType

**Ordinal or Structured Categorical:**

* JobRoleArea
* Gender
* MaritalStatus
* PaycheckMethod
* TextMessageOptIn

Initial inspection using `.info()`, `.describe()`, `.value_counts()`, and `.nunique()` revealed structural inconsistencies and quality issues.

---

# 3. Identified Data Quality Issues

The following issues were detected:

## 3.1 Duplicate Records

* 99 duplicate rows identified using `.duplicated()`

## 3.2 Formatting Errors

* HourlyRate stored as string with "$" symbol
* HoursWeekly stored as object instead of integer
* Trailing whitespace in column names and object fields

## 3.3 Inconsistent Categorical Values

* PaycheckMethod contained 7 unique variants instead of expected standardized categories
* JobRoleArea included homonyms and synonyms for similar departments

## 3.4 Missing Values

* NumCompaniesPreviouslyWorked
* AnnualProfessionalDevHrs
* TextMessageOptIn (22% null)

## 3.5 Outliers

* AnnualSalary
* DrivingCommuterDistance

Outliers were identified using summary statistics and interquartile range (IQR) analysis.

---

# 4. Data Cleaning Methodology

## 4.1 Duplicate Removal

Duplicate records were removed using:

`drop_duplicates()`

Verification confirmed zero remaining duplicate entries.

---

## 4.2 Data Type Standardization

* Removed "$" from HourlyRate
* Converted HourlyRate to float
* Converted HoursWeekly to integer
* Standardized object columns using `.str.strip()`

Automated loops ensured consistent transformation across applicable columns.

---

## 4.3 Handling Inconsistencies

A reusable function was developed to standardize homonyms and synonyms across categorical fields.

Examples:

* Consolidation of IT-related job roles
* Consolidation of paycheck delivery labels

This ensured uniform grouping for future modeling.

---

## 4.4 Outlier Treatment

Outliers were defined using the Interquartile Range (IQR):

Lower Bound = Q1 − 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR

Values outside these bounds were replaced with `np.nan` using conditional logic.

IQR was selected over Z-score methods due to its robustness against skewed distributions.

---

## 4.5 Missing Value Treatment

* NumCompaniesPreviouslyWorked → Mean imputation
* AnnualProfessionalDevHrs → Mean imputation
* TextMessageOptIn → Left as null due to categorical nature and potential compliance requirements

Mean imputation was used only after outliers were removed to avoid distortion.

---

# 5. Advantages of the Approach

* Fully reproducible cleaning pipeline
* Automated transformations via loops and functions
* Robust outlier detection method
* Transparent documentation of assumptions
* Scalable for future dataset updates

Python and Pandas enabled structured data validation and repeatable transformations suitable for collaborative environments.

---

# 6. Limitations and Data Risks

* Outlier removal may eliminate potentially valid extreme cases
* Mean imputation does not restore true values
* 22% null rate in TextMessageOptIn reduces reliability of engagement analysis
* Some inconsistencies may reflect underlying HR system input issues

It is recommended that Technology A conduct upstream database validation to reduce future inconsistencies.

---

# 7. Strategic Recommendations

1. Implement standardized HR data entry validation rules.
2. Audit compensation and commuter distance records for extreme values.
3. Reduce missing data in TextMessageOptIn to improve engagement analytics.
4. Establish quarterly data quality monitoring.
5. Use this cleaned dataset as the foundation for predictive turnover modeling.

---

# 8. Conclusion

This project established a structured and repeatable data preparation framework for Technology A’s turnover reduction initiative.

Key findings include:

* Removal of 99 duplicate records
* Correction of formatting and datatype inconsistencies
* Standardization of categorical variables to eliminate homonyms and synonyms
* Robust IQR-based outlier treatment for compensation and commuting fields
* Identification of a material 22% null rate in TextMessageOptIn

Following remediation, the dataset is now standardized and analytically dependable. However, persistent upstream data-entry inconsistencies and missing-value patterns indicate the need for improved HR data governance.

High-quality predictive modeling depends on high-quality input data. This preparation phase reduces analytical distortion, strengthens the reliability of future churn modeling, and supports evidence-based workforce strategy decisions.
