import numpy as np 
from .metrics import Metrics
from statsmodels.tsa.stattools import adfuller
import pandas as pd 
"""
Calculation type for mean and std (simple or exponential)

Mean period 
spread mean period 
spread std dev period 
threshold (symmetrical)
long/short bias
""" 

class RollingCalculationType:
    def __init__(self):
        self.calculation_simple='simple'
        self.calculation_exponential='exponential'

        self.valid_values = [self.calculation_simple, self.calculation_exponential]


class Side:
    def __init__(self):
        self.side_long='long'
        self.side_short='short'
        self.side_neutral='neutral'

        self.valid_values = [self.side_long, self.side_short, self.side_neutral]


class Defaults:
    def __init__(self):
        self.mean_period = 20 
        self.spread_mean_period = 10 
        self.spread_sdev_period = 10 
        self.threshold = 1 
        self.side = Side().side_long 
        self.calc_type = RollingCalculationType().calculation_exponential 
        self.cash = 1000000

class Hyperparameters:
    def __init__(self, 
                 mean_period:int, 
                 spread_mean_period:int,
                 spread_sdev_period:int, 
                 threshold:int,
                 side:str,
                 calc_type:str):
        
        defaults = Defaults()

        self.mean_period = mean_period if mean_period is not None else defaults.mean_period
        self.spread_mean_period = spread_mean_period if spread_mean_period is not None else defaults.spread_mean_period
        self.spread_sdev_period = spread_sdev_period if spread_sdev_period is not None else defaults.spread_sdev_period
        self.threshold = abs(threshold) if threshold is not None else defaults.threshold
        self.side = side if side is not None else defaults.side
        self.calc_type = calc_type if calc_type is not None else defaults.calc_type

    def validate(self, mean_period, spread_mean_period, spread_sdev_period, side, calc_type): 
        if not self.valid_period(mean_period):
            self.period_error('Mean Period', mean_period)
            return None 
        
        if not self.valid_period(spread_mean_period):
            self.period_error('Spread Mean Period', spread_mean_period)
            return None 
            
        if not self.valid_period(spread_sdev_period):
            self.period_error('Spread Sdev Period', spread_sdev_period)
            return None

        s = Side()
        if side not in s.valid_values:
            print(f"Invalid Side. Value not found in valid values. Value: {side}, Valid: {s.valid_values}")
            return None 

        c = RollingCalculationType()
        if calc_type not in c.valid_values:
            print(f"Invalid Calculation Type. Value not found in valid values. Value: {calc_type}, Valid: {c.valid_values}")
            return None 


    def valid_period(self, prd):
        return prd > 0
    
    def period_error(self, prd_name, value):
        print(f"Invalid {prd_name}. Value must be greater than 0. Value: {value}")

    def print_values(self):
        print(f"Mean Period: {self.mean_period}")
        print(f"Spread Mean Period: {self.spread_mean_period}")
        print(f"Spread Sdev Period: {self.spread_sdev_period}")
        print(f"Threshold: {self.threshold}")
        print(f"Side: {self.side}")
        print(f"Calculation Type: {self.calc_type}")
        
class Accounts:
    def __init__(self, cash):
        self.cash = cash if cash is not None else Defaults().cash

class MeanReversion:
    
    def __init__ (self, data, hyperparemeters:Hyperparameters, accounts:Accounts):
        self.hyperparameters = hyperparemeters
        self.cash = accounts.cash


        print(f"Simulation Created. Columns: {len(data.columns)}, Rows: {len(data)}, Cash: ${self.cash}")
        self.hyperparameters.print_values()

        self.tpl_side = Side()
        self.tpl_calc = RollingCalculationType()

        data.columns = [c.lower() for c in data.columns]
        self.data = data 
        self.built_model = self.build_model(self.data.copy())
        self.metrics = Metrics(self.built_model, self.cash)

    def build_model(self, data): 
        
        data['log_returns'] = np.log(data['close']/data['close'].shift(1))
        if self.hyperparameters.calc_type == self.tpl_calc.calculation_exponential:
            data['mean'] = data['close'].ewm(span=self.hyperparameters.mean_period).mean()
            data['spread'] = data['close'] - data['mean']

            
            spread_mu = data['spread'].ewm(span=self.hyperparameters.spread_mean_period).mean()
            spread_sigma = data['spread'].ewm(span=self.hyperparameters.spread_sdev_period).std()
        
        else: 
            data['mean'] = data['close'].rolling(self.hyperparameters.mean_period).mean()
            data['spread'] = data['close'] - data['mean']


            spread_mu = data['spread'].rolling(self.hyperparameters.spread_mean_period).mean()
            spread_sigma = data['spread'].rolling(self.hyperparameters.spread_sdev_period).std()


        
        lower_threshold = -self.hyperparameters.threshold 
        upper_threshold = self.hyperparameters.threshold
        # z-score = (x - mu) / sigma 
        data['z_score'] = (data['spread'] - spread_mu) / spread_sigma
        data['z_upper'] = upper_threshold 
        data['z_lower'] = lower_threshold
        
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

        if self.hyperparameters.side == self.tpl_side.side_long:
            data.loc[data['signal'] == -1, 'strategy_returns'] = 0 
        elif self.hyperparameters.side == self.tpl_side.side_short: 
            data.loc[data['signal'] == 1, 'strategy_returns'] = 0 
        else:
            pass 

        data['returns'] = data['strategy_returns'].cumsum()
        data['equity'] = (data['returns'] * self.cash) + self.cash 
        data['peak'] = data['equity'].cummax()
        data['drawdown'] = (data['equity'] - data['peak']) / data['peak'] * 100 
        
        return data

    def stationarity_test(self, data=None, target=None):
        data = self.built_model if data is None else data 
        target = 'spread' if target is None else target
        if data is None: 
            data = self.built_model 

        adf = adfuller(data[target], maxlag=1)
        test_statistic, p_value, _, _, critical_value, _ = adf 
        print()
        print("===== AUGMENTED DICKEY-FULLER TEST (STATIONARITY) =====")
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
    
