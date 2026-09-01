# Retail Sales Forecasting

A time-series forecasting project developed as the final Data Science project at Digital House.

The project explores monthly retail sales forecasting at the store level using statistical time-series methods. It combines data preprocessing, stationarity analysis, SARIMAX modeling, forecast validation, store performance classification, and a prototype Flask interface for presenting results.

## Project Overview

Retail stores may have different amounts of historical data available, making it difficult to apply the same forecasting workflow uniformly across the entire network.

This project implements a forecasting pipeline that:

* preprocesses historical store sales;
* groups stores according to the amount of available history;
* evaluates time-series stationarity;
* applies differencing when necessary;
* separates observations into training and testing periods;
* fits seasonal SARIMAX models;
* selects model parameters using AIC;
* generates monthly sales forecasts;
* evaluates forecast errors;
* compares predicted, budgeted, and actual performance;
* exposes part of the analysis through a prototype Flask dashboard.

## Forecasting Pipeline

```text
Historical retail sales
        |
        v
Data preprocessing
        |
        v
Store segmentation by history length
        |
        v
ADF stationarity test
        |
        v
Differencing when required
        |
        v
Train / test split
        |
        v
SARIMAX model
        |
        v
AIC-based parameter selection
        |
        v
12-month forecast
        |
        v
Forecast evaluation
        |
        v
Store performance classification
        |
        v
Prototype Flask dashboard
```

## Methodology

### 1. Data Preprocessing

Historical sales data is cleaned and standardized before modeling.

Stores are grouped according to the amount of historical information available:

* approximately 60 months;
* 48–59 months;
* 36–47 months;
* 24–35 months.

This allows the forecasting workflow to handle stores with different historical coverage.

### 2. Stationarity Analysis

The Augmented Dickey-Fuller (ADF) test is used to evaluate whether each store sales series is stationary.

Non-stationary series are transformed using differencing and tested again before modeling.

### 3. Train/Test Split

Each time series is separated chronologically into training and testing samples using an approximately 80/20 split.

### 4. SARIMAX Forecasting

Forecasts are generated using seasonal ARIMA models implemented through `statsmodels` SARIMAX.

The modeling procedure evaluates combinations of:

* autoregressive order `p`;
* moving-average order `q`;
* seasonal autoregressive order `P`;
* seasonal moving-average order `Q`.

The implementation uses:

```text
d = 1
D = 1
seasonal period = 12
```

Candidate models are compared using the Akaike Information Criterion (AIC), with the lowest-AIC specification selected for forecasting.

The pipeline produces forecasts up to 12 months ahead.

### 5. Forecast Validation

Forecast performance is evaluated using multiple error metrics:

* MAE — Mean Absolute Error;
* MFE — Mean Forecast Error;
* MSE — Mean Squared Error;
* RMSE — Root Mean Squared Error;
* MAPE — Mean Absolute Percentage Error.

Using several metrics provides different perspectives on model error and forecast bias.

### 6. Store Performance Analysis

Predicted sales can also be compared with budgeted and actual sales.

Stores are classified into performance ranges according to the relationship between sales and budget:

```text
High    >= 100%
Medium   85% – 100%
Low      < 85%
```

The project also contains functions for generating confusion matrices and comparing predicted performance categories with observed categories.

## Prototype Web Application

A Flask-based prototype was developed to expose forecasting results through a simple web interface.

The application contains functionality for:

* uploading files;
* displaying tabular data;
* running the forecasting pipeline;
* presenting store-level results;
* aggregating performance by management hierarchy;
* displaying forecast classification accuracy;
* generating confusion matrices and charts.

The web application should be considered a historical prototype rather than a production deployment.

## Repository Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── home.py
│   └── uploader.py
│
├── notebooks/
│   ├── forecast-postprocessing-and-evaluation.ipynb
│   └── sales-forecasting-workflow.ipynb
│
├── src/
│   ├── __init__.py
│   ├── differencing.py
│   ├── forecasting.py
│   ├── pipeline.py
│   ├── preprocessing.py
│   ├── stationarity.py
│   ├── train_test_split.py
│   ├── validation.py
│   └── visualization.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

### Core Modules

| Module                | Responsibility                                       |
| --------------------- | ---------------------------------------------------- |
| `preprocessing.py`    | Data cleaning and store segmentation                 |
| `stationarity.py`     | Augmented Dickey-Fuller stationarity testing         |
| `differencing.py`     | Time-series differencing and transformation          |
| `train_test_split.py` | Chronological train/test separation                  |
| `forecasting.py`      | SARIMAX parameter search and forecasting             |
| `validation.py`       | Forecast error metrics                               |
| `pipeline.py`         | End-to-end forecasting workflow                      |
| `visualization.py`    | Performance summaries, charts and confusion matrices |

## Technologies

The project was primarily developed with:

* Python
* Pandas
* NumPy
* Statsmodels
* Scikit-learn
* Matplotlib
* Seaborn
* Flask
* Flask-WTF
* Jupyter Notebook

## Installation

Clone the repository:

```bash
git clone https://github.com/mori-mkm/Digital-House-project.git
cd Digital-House-project
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Reproducibility Note

This repository preserves the source code and notebooks from the original academic project, but some artifacts used during development are not included.

The missing artifacts include parts of the original:

* retail sales datasets;
* Flask templates;
* static assets;
* generated intermediate forecasting files.

Because of this, the original application cannot currently be reproduced end-to-end directly from the repository.

The code is preserved primarily to document the forecasting methodology, analytical workflow, and application prototype developed during the project.

## Project Context

This project was developed as a final project for the **Digital House Data Science program**.

Its main purpose was to combine time-series analysis and predictive modeling with a practical business use case: forecasting sales across a network of retail stores and presenting the resulting information through an analytical interface.

## Disclaimer

This is an academic project and reflects the tools, implementation choices, and software versions used during its original development. It should not be interpreted as a production-ready forecasting system.
