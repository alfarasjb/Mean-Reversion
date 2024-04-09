import numpy as np 
from .metrics import Metrics
from statsmodels.tsa.stattools import adfuller

class MeanReversion:
    
    def __init__ (self, data, cash=1000000):
        self.cash = cash 

        data.columns = [c.lower() for c in data.columns]
        self.data = data 
        self.built_model = self.build_model(self.data.copy())
        self.metrics = Metrics(self.built_model, self.cash)

    def build_model(self, data): 
        data['log_returns'] = np.log(data['close']/data['close'].shift(1))
        data['mean'] = data['close'].ewm(span=20).mean()
        data['spread'] = data['close'] - data['mean']
        
        spread_mu = data['spread'].ewm(span=10).mean()
        spread_sigma = data['spread'].ewm(span=10).std()

        # z-score = (x - mu) / sigma 
        data['z_score'] = (data['spread'] - spread_mu) / spread_sigma
        
        lower_threshold = -1 
        upper_threshold = 1
        long_entry = (data['z_score'] < lower_threshold)
        long_exit = data['z_score'] >= 0

        short_entry = (data['z_score'] > upper_threshold)
        short_exit = data['z_score'] <= 0 

        def attach_signal(d, side, entry, exit, signal):
            d[side] = np.nan 
            
            d.loc[entry, side] = signal 
            
            d.loc[exit, side] = 0 
            return d[side].ffill().fillna(0)
        
        data['long_pos'] = attach_signal(data, 'long_pos', long_entry, long_exit, 1) 
        data['short_pos'] = attach_signal(data, 'short_pos', short_entry, short_exit, -1)
        data['signal'] = data['long_pos'] + data['short_pos']
        data['signal'] = data['signal'].shift(1) # shift to mitigate look ahead bias 

        data['strategy_returns'] = data['signal'] * data['log_returns']

        data.loc[data['signal'] == -1, 'strategy_returns'] = 0 
        
        return data

    def stationarity_test(self, data, target):
        
        adf = adfuller(data[target], maxlag=1)
        test_statistic, p_value, _, _, critical_value, _ = adf 
        print(f"ADF Result Parameters: \n{adf}\n")
        print(f"Test Statistic: {test_statistic:.4f}")
        print(f"Critical Value: {critical_value['5%']:.4f}")
        print(f"P-Value: {p_value:.4e}")

        stationary = p_value < 0.05 

        if stationary:
            print(f"Series is stationary. (p-value {p_value*100:.4f}%)")
        else:
            print(f"Series is NOT stationary. (p-value {p_value*100:.4f}%)")


    
   

    @staticmethod
    def columns_valid(data):
        
        target_cols = ['open','high','low','close']
        for t in target_cols:
            if t not in data.columns:
                return False 
            
        return True
    
