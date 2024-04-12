## A Backtesting environment for Mean Reversion Strategies

Mean Reversion is a theory that implies that asset prices and historical returns gradually move towards their long-term mean. In this model, mean-reverting tendency is measure by standardizing the spread of asset prices to its mean. A mean reverting price series is therefore, stationary. 

In general, a time series is said to be stationary if their statistical properties do not change over time. To determine stationarity, we can use an Augmented Dickey-Fuller Test, which is also included in this script. 

The demonstration below tests the Mean Reversion strategy on `BDO`, configured to trade `Long Only`. 

## Usage
```
I. Select File. 

File requires the ff. columns: Open, High, Low, Close

Store CSV files in the data folder. 
```

![console_1](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/e58a4b0b-5c77-45b2-a06f-feb0f0e16037)


```
II. Configure Simulation Parameters

Mean Period: Rolling window of closing mean
Spread Mean Period: Rolling window of spread mean 
Spread Sdev Period: Rolling window of spread standard deviation 
Threshold: Z-Score threshold 
Side: Filters signals by side. Long only, short only, neutral 
Calculation: Exponential or Simple
```

![console_2](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/e2347515-3ea1-417e-9c1e-1792a404f3ac)



```
III. Augmented Dickey-Fuller Test (Stationarity)
```

![console_3](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/c3bbdeb2-2ab8-4f35-b7ce-4748b52ba28b)



```
IV. Backtest Results 
```

![console_4](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/02a9c459-8f48-4568-aad4-b98ecdef8aba)



```
V. Plots 

Spread vs Z-Score
Equity Curve
Heatmap
Annual Returns
```

![signal](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/0adb6538-a893-47f4-b39b-f8bff193b533)

*Plot of the close-mean spread vs Z-Score*

---

![equity_curve](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/69d6c318-ad2b-48b2-8d86-720f30b55831)

*BDO Equity Curve* 

---
![heatmap](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/d3d605a5-6243-4ee0-84c8-ba1b0c2fe1c9)

*Heatmap of returns for BDO* 

---
![annual_returns](https://github.com/alfarasjb/Mean-Reversion/assets/72119101/9d587657-1d60-4181-a6dc-416b0fb96ba8)

*Annual Returns*

---

### DISCLAIMER: The contents of this repository does not, and is not inteded to, constitute financial advice. 
