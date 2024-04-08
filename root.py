import mean_reversion 
import os 

if __name__ == "__main__":
    while True: 
        dl = mean_reversion.DataLoader()
        print(dl.files())
        s = input("test")