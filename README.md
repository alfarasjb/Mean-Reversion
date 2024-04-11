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


![image](assets\console_1.png)

```
II. Configure Simulation Parameters

Mean Period: Rolling window of closing mean
Spread Mean Period: Rolling window of spread mean 
Spread Sdev Period: Rolling window of spread standard deviation 
Threshold: Z-Score threshold 
Side: Filters signals by side. Long only, short only, neutral 
Calculation: Exponential or Simple
```

![image](assets\console_2.png)


```
III. Augmented Dickey-Fuller Test (Stationarity)
```

![image](assets\console_3.png)


```
IV. Backtest Results 
```

![image](assets\console_4.png)


```
V. Plots 

Spread vs Z-Score
Equity Curve
Heatmap
Annual Returns
```

![image](assets\signal.png)
*Plot of the close-mean spread vs Z-Score*

---

![image](assets\equity_curve.png)
*BDO Equity Curve* 

---
![image](assets\heatmap.png)
*Heatmap of returns for BDO* 

---
![image](assets\annual_returns.png)
*Annual Returns*

---

### DISCLAIMER: The contents of this repository does not, and is not inteded to, constitute financial advice. 