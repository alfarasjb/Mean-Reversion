import mean_reversion 
import os 
import warnings
warnings.filterwarnings('ignore')


class MeanReversionBacktest: 
    def __init__(self):
        self.file = None 
        self.cash_amount = None 
        self.sim = None 

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


        try:
            selected_file = int(input("Selection (index): "))
            if selected_file == 0:
                return None 
        
            self.file = files[selected_file-1]
            print(f"Selected File: {self.file}")

            return dl.load_data(self.file)
            
        except ValueError:
            print(f"Invalid input. Use index to select file.")

            self.select_dataset()



    @staticmethod 
    def generate_options(options, show_exit:bool=True):
        if show_exit:
            print(f"0. Exit")

        for index, option in enumerate(options):
            print(f"{index+1}. {option}")
    
    def cash(self):
        cash_amount = input("Cash: ")
        if not cash_amount.strip():
            return 1000000
        
        if not cash_amount.isnumeric():
            print(f"Invalid input for cash amount. Value is not numeric. Value: {cash_amount}")
            self.cash()
        
        self.cash_amount = int(cash_amount)
        return self.cash_amount

    def hyperparameters(self):

        mean_period = input("Mean Period [>0]: ")
        if not self.validate_integer_input(mean_period):
            print(f"Invalid Input: Mean Period. Value: {mean_period}")
            self.hyperparameters()
        
        spread_mean_period = input("Spread Mean Period [>0]: ")
        if not self.validate_integer_input(spread_mean_period):
            print(f"Invalid Input: Spread Mean Period. Value: {spread_mean_period}")
            self.hyperparameters()
        
        spread_sdev_period = input("Spread Sdev Period [>0]: ")
        if not self.validate_integer_input(spread_sdev_period):
            print(f"Invalid Input: Spread Sdev Period. Value: {spread_sdev_period}")
            self.hyperparameters()

        threshold = input("Threshold: ")
        if not self.validate_integer_input(threshold):
            print(f"Invalid Input: Threshold. Value: {threshold}" )
            self.hyperparameters()

        calc_type = self.get_calculation_type()
        side = self.get_side()
               

        hparam = mean_reversion.Hyperparameters(
            mean_period=None if not mean_period.strip() else int(mean_period),
            spread_mean_period=None if not spread_mean_period.strip() else int(spread_mean_period),
            spread_sdev_period=None if not spread_sdev_period.strip() else int(spread_sdev_period),
            threshold=None if not threshold.strip() else int(threshold),
            calc_type=None if not calc_type.strip() else calc_type,
            side=None if not side.strip() else side
        )
        
        return hparam

    @staticmethod
    def validate_integer_input(value:str):
        if not value.strip():
            return True
        return value.isnumeric()

    def get_calculation_type(self):
        calc = mean_reversion.RollingCalculationType()
        self.generate_options(calc.valid_values, show_exit = False) 

        try:
            calc_type = int(input("Calculation Type: "))
            if calc_type == 0:
                print(f"Invalid selected value. Value: {calc_type}. Try Again.")
                return self.get_calculation_type()

            return calc.valid_values[calc_type-1] 
        except ValueError:
            print(f"Invalid input. Use index to select option.")      
            return self.get_calculation_type()       

    def get_side(self):
        s = mean_reversion.Side()
        self.generate_options(s.valid_values, show_exit = False)

        try:
            side = int(input("Side: "))
            if side == 0:
                print(f"Invalid selected value. Value: {side}. Try Again.")
                return self.get_side()
            return s.valid_values[side-1]
        except ValueError:
            print(f"Invalid input. Use index to select option.")
            return self.get_side()
        
    def adf(self, sim:mean_reversion.MeanReversion):
        sim.stationarity_test(data=sim.built_model, target='spread')
        
    def print_results(self, sim:mean_reversion.MeanReversion):
        sim.metrics.show_data()

    def plot(self, sim:mean_reversion.MeanReversion):
        pass 

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
        cash = backtest.cash()
        hparam = backtest.hyperparameters()

        print()
        print("===== GENERATING SIMULATION =====")
        simulation = mean_reversion.MeanReversion(
            data = df, 
            hyperparemeters=hparam,
            cash=cash
        )
        print("==========")
        print()

        backtest.evaluate(simulation)