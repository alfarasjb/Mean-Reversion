import numpy as np

class Metrics: 

    def __init__(self, data, cash):
        self.data = data 
        self.cash = cash 

        self.returns = self.data['strategy_returns'].cumsum() 
        self.net_returns_percent = self.data['strategy_returns'].sum() * 100 
        self.equity = (self.returns * self.cash) + self.cash
        self.final_equity = (self.data['strategy_returns'].sum() * self.cash) + self.cash
        self.peak = self.equity.cummax()
        self.drawdown = (self.equity-self.peak) / self.peak * 100 

        traded =self.data.query('strategy_returns != 0')
        strategy_mean = traded['strategy_returns'].mean()
        strategy_std = traded['strategy_returns'].std()

        risk_free_rate = 0.05 
        self.sharpe_daily = (strategy_mean - (risk_free_rate/252)) / strategy_std 
        self.sharpe_annual = self.sharpe_daily * np.sqrt(252)

        target_data = self.data['strategy_returns']
        grouped = target_data.groupby(target_data.index.year).sum() * 100 

        self.annual_mean = grouped.mean()

        
    def show_data(self):
        print()
        print("===== SIMULATION RESULTS =====")
        print(f"Returns: {self.net_returns_percent:.2f}%")
        print(f"Deposit: ${self.cash}")
        print(f"Final Equity: ${self.final_equity:.2f}")
        print(f"Peak: ${self.equity.max():.2f}")
        print(f"Max Drawdown: {abs(self.drawdown.min()):.2f}%")
        print(f"Average Annual Returns: {self.annual_mean:.2f}%")
        print(f"Daily Sharpe: {self.sharpe_daily:.2f}")
        print(f"Annualized Sharpe: {self.sharpe_annual:.2f}")
        print("==========")
        print()

