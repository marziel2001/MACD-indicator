# MACD Indicator

A Python tool that computes the **MACD (Moving Average Convergence/Divergence)** technical indicator for stock and currency price data, visualises the results, and simulates a simple buy/sell investment strategy.

---

## What it does

1. **Loads** historical price data from a CSV file.
2. **Calculates** EMA-12, EMA-26, the MACD line, and the Signal line (EMA-9 of MACD).
3. **Simulates** a trading strategy – buys when MACD crosses above Signal, sells when it crosses below – and prints the hypothetical profit/loss.
4. **Plots** two charts (MACD + Signal overlay, and the raw price series) using Matplotlib.

---

## Tech stack

| Layer | Library / Tool |
|---|---|
| Language | Python 3 |
| Numerical computation | NumPy |
| Charting | Matplotlib |
| Date handling | `datetime` (stdlib) |
| Data format | CSV (semicolon-delimited) |

No external framework or database is required – the project runs as a single script.

---

## Architecture

```
main.py
├── wczytaj(filename)        – reads CSV → (dates[], prices[])
├── ema(n, values)           – computes Exponential Moving Average for window n
├── licz_zarobek(...)        – simulates buy/sell trades, returns final portfolio value
├── Gielda (class)           – lightweight portfolio state (shares held, signal position)
└── plotting block           – draws MACD/Signal and price subplots with Matplotlib
```

All logic lives in **`main.py`**. The active dataset is selected by commenting/uncommenting the `filename` variable near the top of the file.

### Data files

| File | Asset |
|---|---|
| `apple.csv` / `apple200.csv` | Apple (AAPL) |
| `microsoft.csv` / `microsoft200.csv` | Microsoft (MSFT) |
| `cdr200.csv` | CD Projekt (CDR) |
| `tesla.csv` | Tesla (TSLA) |
| `usdpln.csv` | USD/PLN exchange rate |

CSV format: `DD.MM.YYYY;price` (semicolon separator, no header).

---

## How to use

### Prerequisites

```bash
pip install numpy matplotlib
```

### Run

```bash
python main.py
```

By default the script analyses **`cdr200.csv`**. To switch dataset, edit the `filename` variable at the top of `main.py`:

```python
# filename = "tesla.csv"
# filename = "usdpln.csv"
filename = "cdr200.csv"        # <-- change this line
# filename = "apple.csv"
# filename = "apple200.csv"
# filename = "microsoft.csv"
# filename = "microsoft200.csv"
```

### Output

- **Console** – prints each trading day with current price, cash balance and shares held, followed by the total hypothetical profit/loss for a starting investment of **1 000 PLN**.
- **Chart window** – two subplots: MACD & Signal lines (top), raw price (bottom).

### Changing the investment amount

Edit the `INWESTYCJA` constant near the top of `main.py`:

```python
INWESTYCJA = 1_000   # starting capital in PLN
```

---

## MACD formula

```
EMA_12   = EMA(price, 12)
EMA_26   = EMA(price, 26)
MACD     = EMA_12 - EMA_26
Signal   = EMA(MACD, 9)
```

The EMA is computed using the standard smoothing factor **α = 2 / (n + 1)**.

---

## Project report

A detailed write-up (in Polish) is available in [`projekt_MACD.pdf`](projekt_MACD.pdf).
