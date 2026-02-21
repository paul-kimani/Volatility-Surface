
# Construction and Visualization of an Implied Volatility Surface

## Abstract

This project implements the construction of an implied volatility surface from observed option market data. Using real option chains retrieved via Yahoo Finance, we compute implied volatilities under the Black–Scholes framework and visualize the resulting surface across strike and maturity dimensions. The implementation is fully contained within a single Python script and serves as a compact research pipeline for volatility surface analysis.

---

## 1. Introduction

The implied volatility surface is a central object in derivatives pricing and quantitative finance. While the Black–Scholes model assumes constant volatility, market-observed option prices imply a volatility that varies across strike and time to maturity. This variation manifests as:

- Volatility smiles and skews (strike dimension)
- Term structure effects (maturity dimension)

The objective of this project is to:

1. Retrieve option market data.
2. Compute implied volatility via numerical inversion of Black–Scholes prices.
3. Construct a discretized volatility surface.
4. Visualize the surface in both two-dimensional and three-dimensional form.

---

## 2. Methodology

### 2.1 Market Data Acquisition

Option chain data is retrieved using the `yfinance` interface to Yahoo Finance. For each expiration:

- Calls and puts are collected.
- Observations with non-positive bid or ask are filtered.
- Mid prices are computed as:

\[
\text{mid} = \frac{\text{bid} + \text{ask}}{2}
\]

Spot price is extracted from the latest close.

---

### 2.2 Pricing Model

Option prices are modeled using the Black–Scholes framework:

\[
d_1 = \frac{\ln(S/K) + (r - q + \tfrac{1}{2}\sigma^2)T}{\sigma \sqrt{T}}, \quad
d_2 = d_1 - \sigma \sqrt{T}
\]

Call price:

\[
C = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)
\]

Put price:

\[
P = K e^{-rT} N(-d_2) - S e^{-qT} N(-d_1)
\]

where:

- \( S \) = spot price  
- \( K \) = strike  
- \( T \) = time to maturity (years)  
- \( r \) = risk-free rate  
- \( q \) = dividend yield  
- \( \sigma \) = volatility  

---

### 2.3 Implied Volatility Estimation

Implied volatility is obtained by solving:

\[
\text{BS}(\sigma) = \text{Observed Market Price}
\]

This is performed using a bisection root-finding algorithm, chosen for its numerical robustness and guaranteed convergence under standard monotonicity conditions.

---

### 2.4 Surface Construction

For each option contract:

- Time to maturity is computed as calendar days divided by 365.
- Implied volatility is stored alongside strike and maturity.
- Data is grouped into a strike–maturity grid.
- Mean implied volatility is computed for each grid node.

No interpolation or smoothing is applied in the baseline implementation.

---

## 3. Visualization

Two visualizations are produced:

1. **Smile slices**: Implied volatility as a function of strike for selected maturities.
2. **3D surface**: A discretized surface over:

   - X-axis: Strike \( K \)  
   - Y-axis: Time to maturity \( T \)  
   - Z-axis: Implied volatility \( \sigma \)

These plots reveal skewness and term structure characteristics typical of equity options.

---

## 4. Installation

Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
````

Install required packages:

```bash
pip install numpy pandas matplotlib yfinance
```

---

## 5. Execution

Run the single-file script:

```bash
python vol_surface_onefile.py --ticker AAPL --expiries 6
```

Arguments:

* `--ticker`: Equity or ETF symbol.
* `--expiries`: Number of expiration dates to process.

---

## 6. Data Structure

The internal dataset contains:

| Variable | Description                          |
| -------- | ------------------------------------ |
| S        | Spot price                           |
| r        | Risk-free rate (constant assumption) |
| q        | Dividend yield (assumed zero)        |
| T        | Time to maturity (years)             |
| K        | Strike                               |
| type     | Option type (C or P)                 |
| mid      | Mid market price                     |
| iv       | Implied volatility                   |

---

## 7. Assumptions and Limitations

* Constant risk-free rate.
* Dividend yield set to zero.
* No no-arbitrage enforcement.
* No smoothing or parametric surface fitting.
* Relies on Yahoo Finance data (unofficial source).
* Deep OTM or illiquid options may produce unstable implied volatilities.

---

## 8. Possible Extensions

* Bootstrap risk-free curve from Treasury yields.
* Infer forward price using put–call parity.
* Enforce static arbitrage constraints.
* Fit SVI parameterization per maturity.
* Implement interpolation for smooth surface construction.
* Export surface for further quantitative analysis.

---

## 9. Conclusion

This project demonstrates the full pipeline of volatility surface construction:

* Market data ingestion
* Numerical inversion of option prices
* Surface aggregation
* Multi-dimensional visualization

It serves as a compact yet rigorous implementation suitable for research exploration in quantitative derivatives modeling.

Author : ** Paul Mwaniki Kimani **

```

---


