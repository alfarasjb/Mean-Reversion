import matplotlib.pyplot as plt 
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')
bg_color_light = '#3A3B3C'
bg_color = '#242526'
fg_color = '#B0B3B8'

plt.rcParams['font.size'] = 11 
plt.rcParams['font.family'] = 'Calibri'
plt.rcParams['axes.labelcolor'] = fg_color
plt.rcParams['axes.titlecolor'] = fg_color
plt.rcParams['axes.facecolor'] = bg_color
plt.rcParams['xtick.color'] = fg_color
plt.rcParams['xtick.labelcolor'] = fg_color
plt.rcParams['ytick.color'] = fg_color
plt.rcParams['ytick.labelcolor'] = fg_color
plt.rcParams['grid.color'] = bg_color_light
plt.rcParams['figure.facecolor'] = bg_color
plt.rcParams['legend.labelcolor'] = fg_color

class Plots:

    def __init__(self, data):
        self.data = data 
        

    def plot_spread_signal(self):
        fig, ax = plt.subplots(figsize=(12, 4))
        self.data['z_score'].plot(ax=ax, color='dodgerblue',alpha=0.8)
        self.data['z_upper'].plot(ax=ax, color ='red', alpha=0.8, ls='--')
        self.data['z_lower'].plot(ax=ax, color='red',alpha=0.8, ls='--')
        plt.ylabel('Z-Score')

        ax1=ax.twinx()
        self.data['spread'].plot(ax=ax1, color='darkgrey',alpha=0.8)
        plt.ylabel('Spread')

        plt.grid()
        plt.title('Spread vs Z-Score')
        plt.show()
        
    def plot_equity_curve(self):
        fig, (ax, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,gridspec_kw={'height_ratios':[3, 1]})
        self.data['equity'].plot(color='dodgerblue', ax = ax)
        ax.set_ylabel('Equity (PHP)')
        ax.legend(labels=['Equity'])

        #plt.title(f'{ticker} Equity Curve - Mean Reversion')

        self.data['drawdown'].plot(ax=ax2, kind='area', color = 'red', alpha = 0.3)
        ax2.set_ylabel('Drawdown (%)')
        plt.show()

    def plot_heatmap(self):
        returns = self.data[['strategy_returns']]
        grouped = returns.groupby([returns.index.year, returns.index.month])[['strategy_returns']].sum()
        grouped.index = grouped.index.rename(names=['year','month'])
        grouped = grouped.reset_index()

        matrix = grouped.pivot_table(values='strategy_returns', index=grouped['year'], columns=grouped['month'])
        matrix.columns=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        
        plt.figure(figsize=(10,7))

        sns.heatmap(matrix, annot=True, fmt='.2%', cbar=False)

        plt.xlabel('Month')
        plt.ylabel('Year')
        plt.show()

    def plot_annual_returns(self): 

        target_data = self.data['strategy_returns']
        grouped = target_data.groupby(target_data.index.year).sum() * 100 
        grouped.plot(kind='bar', figsize=(10, 6), color ='dodgerblue')
        plt.xlabel('Year')
        plt.ylabel('Returns (%)')
        plt.title('Annual Returns - Mean Reversion')
        plt.grid()
        plt.show()
        