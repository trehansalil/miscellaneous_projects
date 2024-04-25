# Assistant

from typing import List
import numpy as np
import pandas as pd
import yfinance as yf

class PortfolioAssesmentApp:
    
    def __init__(self, stock_symbols: List[str]):
        self.stock_symbols = stock_symbols
    
    def retreive_data(self):
        
        data = pd.DataFrame()
        
        try:
            # Download daily stock price data from Yahoo Finance from 1-year ago
            data = yf.download(tickers=", ".join(self.stock_symbols), period='1y', interval='1d')

        except Exception as e:
            print(f"\nError: {e} raised, probably because there is either an incorrect Stock Name Input or there is some problem with yfinance API\n")
               
        if data.shape[0] == 0:
            # Can not download data or there is no data, return empty data frame table
            print('\nThere is no asset data or it failed to retreive.\n')
        else:
            if len(self.stock_symbols) == 1:
                # There is only one asset
                data = pd.DataFrame(data={self.stock_symbols[0]: data['Close']}) if data['Close'].isnull().sum() == 0 else data
            else:
                data = pd.DataFrame(data={stock_symbol: data['Close', stock_symbol] for stock_symbol in self.stock_symbols if data['Close', stock_symbol].isnull().sum() == 0})     
                
                if data.shape[1] != len(self.stock_symbols):
                    data = pd.DataFrame()   
                
                else:
                    print("\nData retrieval Successful!!!\n")    
            
        return data
    
    def _is_valid_weight(self, input_list: List[float]):
        
        a = list(filter(lambda x: (1>= x >=0 ), input_list))
        a = a if sum(a) == 1 else []

        return len(a) == len(input_list)
    
    def calculate_portfolio_risk(self, asset_weights: List[float]):
        
        portfolio_risk = False
        
        assets_data = self.retreive_data()
        
        if (assets_data.shape[0] != 0) & (self._is_valid_weight(input_list=asset_weights)):
            
            # Converting list to array for matrix calculations
            asset_weights = np.array(asset_weights)
        
            # Calculate individual asset return
            assets_return = assets_data.pct_change()

            # Calculate covariance matrix
            covariance_matrix = assets_return.cov()

            # Calculate portfolio variance by matrix multiplication
            portfolio_variance = np.dot(asset_weights.T, np.dot(covariance_matrix, asset_weights))

            # The portfolio risk is the square root of portfolio variance
            portfolio_risk = np.sqrt(portfolio_variance)
            
        return portfolio_risk  

# Example Usage

if __name__ == '__main__':
    
    stock_symbols = ['AMZN', 'COIN', 'META']
    asset_weights = [0.1, 0.7, 0.2]
    
    app = PortfolioAssesmentApp(stock_symbols=stock_symbols)
    portfolio_risk = app.calculate_portfolio_risk(asset_weights=asset_weights)
  
    if portfolio_risk:
        print(f'portfolio risk = {portfolio_risk}\n')    
    else:
        print("Check your inputs\n")
