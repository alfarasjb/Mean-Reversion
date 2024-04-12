import warnings
warnings.filterwarnings('ignore')
import mean_reversion 
import os 



class MeanReversionBacktest: 
    def __init__(self):
        self.file = None 
        self.cash_amount = None 
        self.sim = None 

        self.defaults = mean_reversion.Defaults()

    # ----------------------------- generic ----------------------------- #

    @staticmethod 
    def use_defaults(value:str):
        if len(value.strip()) == 0:
            return True 
        if value.isspace():
            return True 
        return False 

    @staticmethod
    def validate_integer_input(value:str, min_value:int=None):   
        
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
    def prompt(source:str, default:int, min_value:int= None):
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
                if self.use_defaults(inp_val):
                    print(f"Using default for {source}: {default}")
                    return default 
                return int(inp_val)
            except AssertionError as e:
                print(f"Error. {e}")
    
    

    # ----------------------------- main methods ----------------------------- #

    def select_dataset(self):
        dl = mean_reversion.DataLoader()
        print("Select File..")
        ## generates options
        files = dl.files()
        if len(files) == 0:
            print(f"No files detected in data folder. Add files before testing.")
            print("Columns required: open, high, low, close")
            return None
        self.generate_options(files)
        
        file = input("File: ")
        try:
            file = int(file)
        except ValueError:
            # only accept index as input 
            print(f"Invalid input. Use index to select file.")
            return self.select_dataset()

        if file == 0:
            return None 
        
        try: 
            self.file = files[file-1]
            print(f"Selected File: {self.file}")
            return dl.load_data(self.file)
        except IndexError:
            print("Invalid selected value. Try Again.")
            return self.select_dataset()
      
    
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
        calc = mean_reversion.RollingCalculationType()
        self.generate_options(calc.valid_values, show_exit = False) 
        calc_type = input(f"Calculation Type [{self.defaults.calc_type}]: ")

        # Validate String/Integer Input 
        try:
            # Raises value error if input cannot be casted to integer
            calc_type = int(calc_type)
        except ValueError:
            # If input is string, either empty input, or calc type string
            if self.use_defaults(calc_type):
                return self.defaults.calc_type
            calc_type_str = calc_type.strip().lower()
            if calc_type_str in calc.valid_values:
                # Test case: exponential/simple 
                # If input is found in valid values, return that value. 
                return calc_type_str 
            print(f"Invalid String input for Calculation Type. Value: {calc_type_str}.")
            return self.get_calculation_type()
        
        if calc_type == 0: 
            
            print(f"Invalid selected value. Try Again.")
            return self.get_calculation_type() 
        
        try: 
            return calc.valid_values[calc_type - 1]
        except IndexError: 
            # If selected index does not exist, try again 
            print("Invalid selected value. Try Again.")
            return self.get_calculation_type()

    def get_side(self) -> str:
        s = mean_reversion.Side()
        self.generate_options(s.valid_values, show_exit = False)
        side = input(f"Side [{self.defaults.side}]: ")

        try:
            side = int(side)
        except ValueError:  
            if self.use_defaults(side):
                return self.defaults.side        
            side_str = side.strip().lower()
            if side_str in s.valid_values:
                return side_str
            print(f"Invalid string input for Side. Value: {side_str}.")
            return self.get_side()
        
        if side == 0: 
            print(f"Invalid selected value. Try Again.")
            return self.get_side()
        
        try:
            return s.valid_values[side-1]
        except IndexError:
            print(f"Invalid selected value. Try Again.")
            return self.get_side()

    # ----------------------------- backtesting params ----------------------------- #

    def hyperparameters(self):
        
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
    
    def accounts(self):
        cash = self.get_cash()

        accts = mean_reversion.Accounts(
            cash=cash 
        )
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