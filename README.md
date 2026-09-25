# 🏔️ Landslide Risk Map

A machine learning project for mapping, predicting, and evaluating landslide susceptibility and hazard risk in mountainous regions.

---

## 📌 Project Overview
Landslides represent severe geomorphological hazards causing infrastructure destruction and loss of life. This project implements an end-to-end geospatial machine learning workflow to compute the **Landslide Susceptibility Index (LSI)** and categorize regions into actionable risk zones.

## 🧭 Pipeline Architecture ([sample_notebook.ipynb](file:///c:/Users/haris/Desktop/ml%20lab%20record/ml%20project/sample_notebook.ipynb))
1. **Geospatial & Conditioning Factor Synthesis**: Simulates multi-source environmental and topographic data:
   - *Topographic*: Slope Angle, Aspect, Elevation, Plan Curvature
   - *Hydrological & Structural*: Topographic Wetness Index (TWI), Distance to Rivers, Distance to Faults
   - *Anthropogenic & Environmental*: Distance to Roads, Annual Precipitation, NDVI, Bedrock Lithology
2. **Exploratory Data Analysis (EDA) & Geostatistics**:
   - Class distribution and geological unit vulnerability analysis
   - Spearman rank correlation matrix across conditioning factors
   - Spatial clustering projection of historical failure scarps
3. **Preprocessing Pipeline**:
   - `ColumnTransformer` with `StandardScaler` for continuous numerical features and `OneHotEncoder` for lithology
   - Stratified train-test partitioning to prevent data leakage
4. **Multi-Model Benchmarking**:
   - Logistic Regression (Baseline)
   - Support Vector Classifier (RBF Kernel)
   - Random Forest Classifier (Bagging Ensemble)
   - Gradient Boosting Classifier (Sequential Boosting)
5. **Optimization & Diagnostics**:
   - Hyperparameter tuning via Stratified `GridSearchCV`
   - Confusion matrices with normalized error rates (Type I false alarms vs. Type II missed failures)
   - ROC-AUC and Precision-Recall trajectory curves
6. **Geological Factor Importance**:
   - Feature attribution revealing primary trigger factors (Slope, Precipitation, Vegetation density)
7. **5-Tier Landslide Susceptibility Index (LSI) Zoning**:
   - Continuous hazard prediction partitioned into: **Very Low**, **Low**, **Moderate**, **High**, and **Very High**
8. **Interactive Geospatial Visualization**:
   - Matplotlib 2D spatial zoning maps
   - Interactive Leaflet/Folium web map export (`landslide_risk_map.html`)

## 🚀 Getting Started

### Prerequisites
```bash
pip install numpy pandas matplotlib seaborn scikit-learn folium
```

### Running the Notebook
Open [sample_notebook.ipynb](file:///c:/Users/haris/Desktop/ml%20lab%20record/ml%20project/sample_notebook.ipynb) in VS Code, JupyterLab, or Google Colab and run all cells.

