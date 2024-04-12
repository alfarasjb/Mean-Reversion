import warnings
warnings.filterwarnings('ignore')
import mean_reversion 
import os 
import pandas as pd 



class MeanReversionBacktest: 

    def __init__(self):
        self.file = None 
        self.cash_amount = None 
        self.sim = None 

        self.defaults = mean_reversion.Defaults()

    # ----------------------------- generic ----------------------------- #
    
    @staticmethod
    def is_blank(value:str) -> bool: 
        if len(value.strip()) == 0: 
            return True 
        if value.isspace():
            return True 
        return False 

    @staticmethod
    def validate_integer_input(value:str, min_value:int=None) -> bool:   
        
        # Returns true if input string is empty 
        if len(value) == 0:
            return True 

        # Checks empty inputs and whitespaces. 
        # Use defaults if whitespace
        if value.isspace():
            return True
        
        # Checks if value is integer. Throws error if cannot be casted to integer
        try:
            int(value)
        except ValueError as e:
            print(e)
            return False
            
        # Checks for negative values
        assert int(value) >= 0, "Value must be positive."        

        # Returns true if no mininum value is specified
        if min_value is None:
            return True

        # Checks if value is greater than minimum only if minimimum value is specified
        assert int(value) > min_value, f"Value must be greater than {min_value}"

        # Returns True if no errors are raised
        return True
    

    @staticmethod
    def error_msg(source:str, value:any):
        print(f"Invalid {source}. Value: {value}") 


    @staticmethod 
    def generate_options(options, show_exit:bool=True):
        if show_exit:
            print(f"0. Exit")

        for index, option in enumerate(options):
            print(f"{index+1}. {option}")
            

    @staticmethod 
    def prompt(source:str, default:int, min_value:int= None) -> str:
        if min_value is None:
            return f"\n{source} [{default}]: "
     
        return f"\n{source} [>{min_value}, {default}]: "
    

    def get_integer_value(self, source:str, default:int, min_value:int=None) -> int:
        while True:
            inp_val = input(self.prompt(source, default))
            try:
                valid = self.validate_integer_input(inp_val, min_value)
                if not valid:
                    self.error_msg(source, inp_val)
                    continue 
                if self.is_blank(inp_val):
                    print(f"Using default for {source}: {default}")
                    return default 
                return int(inp_val)
            except AssertionError as e:
                print(f"Error. {e}")
         
    
    def get_string_value(self, source:str, default: int, valid_values:list=None, show_exit:bool=False, use_str_input:bool=False) -> str:
        print()
        self.generate_options(valid_values, show_exit=show_exit)
                
        while True: 
            inp_val = input(self.prompt(source, default))
            try: 
                inp_val = int(inp_val)

            except ValueError: 
                # For string inputs 
                if self.is_blank(inp_val):
                    print(f"Using default for {source}: {default}")
                    return default 
                if not use_str_input:
                    # For selecting files (string inputs not allowed)
                    print(f"Invalid input. Use index to select file.")
                    continue 
                # if use str input 
                inp_val_str = inp_val.strip().lower()
                if inp_val_str not in valid_values:
                    print(f"Invalid string input for {source}. Value: {inp_val_str}.")
                    continue 
                return inp_val_str     

                
            if inp_val == 0:
                print(f"Invalid selected value. Try Again.")
                return None 
            
            try:
                return valid_values[inp_val-1]
            except IndexError:
                print(f"Invalid selected value. True Again.")
                continue 


    # ----------------------------- main methods ----------------------------- #

    
    def select_dataset(self) -> pd.DataFrame: 

        dl = mean_reversion.DataLoader()
        print("Select File...")
        files=dl.files()
        if len(files) == 0:
            print(f"No files detected in data folder. Add files before testing.")
            print("Colmuns required: open, high, low, close")
            return None 
        
        dataset_value = self.get_string_value(
                source = "Files",
                default = None, 
                valid_values=files,
                show_exit=True,
                use_str_input=False
            )

        if dataset_value is None: 
            return dataset_value 
        
        self.file = dataset_value 
        print(f"Selected File: {self.file}")
        return dl.load_data(self.file)

    
    def get_cash(self) -> int:
        return self.get_integer_value("Cash", self.defaults.cash)

    def get_mean_period(self) -> int: 
        return self.get_integer_value("Mean Period", self.defaults.mean_period, 0)

    def get_spread_mean_period(self) -> int: 
        return self.get_integer_value("Spread Mean Period", self.defaults.spread_mean_period, 0)

    def get_spread_sdev_period(self) -> int: 
        return self.get_integer_value("Spread Sdev Period", self.defaults.spread_sdev_period, 0)

    def get_threshold(self) -> int: 
        return self.get_integer_value("Threshold", self.defaults.threshold)     


    def get_calculation_type(self) -> str: 

        return self.get_string_value(
            source="Calculation Type",
            default = self.defaults.calc_type,
            valid_values = mean_reversion.RollingCalculationType().valid_values,
            use_str_input = True 
        )
    

    def get_side(self) -> str: 

        return self.get_string_value( 
            source="Side",
            default=self.defaults.side, 
            valid_values=mean_reversion.Side().valid_values,
            use_str_input=True 
        )
    
    
    # ----------------------------- backtesting params ----------------------------- #

    def hyperparameters(self) -> mean_reversion.Hyperparameters:
        
        mean_period = self.get_mean_period()
        spread_mean_period = self.get_spread_mean_period()
        spread_sdev_period = self.get_spread_sdev_period()
        threshold = self.get_threshold()
        calc_type = self.get_calculation_type()
        side = self.get_side()
               
        hparam = mean_reversion.Hyperparameters(
            mean_period=mean_period,
            spread_mean_period=spread_mean_period,
            spread_sdev_period=spread_sdev_period,
            threshold=threshold,
            calc_type=calc_type,
            side=side
        )
        
        return hparam
    
    def accounts(self) -> mean_reversion.Accounts:

        cash = self.get_cash()
        accts = mean_reversion.Accounts(cash=cash)
        return accts
    

    # ----------------------------- evaluation ----------------------------- #

    def adf(self, sim:mean_reversion.MeanReversion):
        sim.stationarity_test(data=sim.built_model, target='spread')
        

    def print_results(self, sim:mean_reversion.MeanReversion):
        sim.metrics.show_data()


    def plot(self, sim:mean_reversion.MeanReversion):

        print()
        print("===== PLOT FIGURES =====")
        plots = mean_reversion.Plots(sim.built_model)
        plot_options = {
            'Spread' : plots.plot_spread_signal,
            'Equity Curve' : plots.plot_equity_curve,
            'Heatmap' : plots.plot_heatmap, 
            'Annual Returns' : plots.plot_annual_returns 
        }

        self.sim = sim 
        self.generate_options(plot_options.keys())

        try:
            plot = int(input("Select Option: "))

            if plot == 0:
                return None 
            
            keys = list(plot_options.keys())
            plot_options[keys[plot-1]]()
            self.plot(sim=sim)
            
        except ValueError:
            print(f"Invalid input. Use index to select option.")
            self.plot(sim=sim)

        print()


    def evaluate(self, sim):

        print()
        print("===== EVALUATE =====")
        sim_options = {
            "ADF Test" : backtest.adf, 
            "Results" : backtest.print_results, 
            "View Plots" : backtest.plot, 
        }

        self.sim = sim 
        self.generate_options(sim_options.keys())

        try:
            evaluation = int(input("Select Option: "))

            if evaluation == 0:
                return None 
            
            keys = list(sim_options.keys())
            sim_options[keys[evaluation-1]](sim)
            self.evaluate(sim=sim)

        except ValueError:
            print(f"Invalid input. Use index to select option.")      
            self.evaluate(sim=sim)

        print()
            

if __name__ == "__main__":

    backtest = MeanReversionBacktest()

    while True: 

        print("==========================")
        print("===== MEAN REVERSION =====")
        print("==========================")
        
        inp = input("Press any key to continue..")

        df = backtest.select_dataset()
        if df is None:
            continue 

        accounts = backtest.accounts() 
        hparam = backtest.hyperparameters()

        print()
        print("===== GENERATING SIMULATION =====")
        simulation = mean_reversion.MeanReversion(
            data = df, 
            hyperparemeters=hparam,
            accounts=accounts
        )
        print("==========")
        print()

        backtest.evaluate(simulation)