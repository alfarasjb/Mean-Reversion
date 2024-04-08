import pandas as pd
import os

class DataLoader:
    
    def __init__(self):
        self.directory = 'data/' if not os.path.isdir('../data/') else '../data/'

    def files(self):
        path = os.path.join(self.directory)
        return os.listdir(path)

    def load_data(self, file:str):
        if file not in os.listdir(self.directory):
            print(f"File: {file} not found in directory.")
            return None 
        
        if not file.endswith('csv'):
            file = f"{file}.csv"
        path = os.path.join(self.directory, file)

        try:
            df = pd.read_csv(path)
        except:
            print("Error reading file. Ensure that correct filename is selected.")
            return None 
        
        df.columns = [c.lower() for c in df.columns]
        if 'date' not in df.columns:
            print("Error. Date column not found.")
            return None 
        
        df = df.set_index('date',drop=True)
        df.index = pd.to_datetime(df.index)
        return df