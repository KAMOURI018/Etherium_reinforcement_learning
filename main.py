from crypto_indicators import CryptoTechnicalIndicators
import config
import pandas as pd
from trading_env import TradingEnv
from q_learning_agent import QLearningAgent

if __name__ == "__main__":
    # Instantiate the class with your database and collection names
    indicator_calculator = CryptoTechnicalIndicators(db_name=config.DATABASE_NAME, collection_name=config.COLLECTION_NAME)
    
    # Step 1: Load data from MongoDB
    indicator_calculator.load_data()
    
    # Step 2: Filter for symbol "ETH"
    indicator_calculator.data = indicator_calculator.data[indicator_calculator.data['symbol'] == 'ETH']
    if indicator_calculator.data.empty:
        print("No data found for symbol 'ETH'.")
    else:
        # Step 3: Calculate technical indicators if data is available
        indicator_calculator.calculate_indicators()
        
        # Step 4: Retrieve the DataFrame with indicators
        indicator_df = indicator_calculator.get_indicator_df()
        indicator_df.dropna(inplace=True)
        
        # Combine the close column with indicator_df
        close_column = indicator_calculator.data[['close']]
        combined_df = pd.concat([close_column, indicator_df], axis=1)
        combined_df.dropna(inplace=True)

        # Print combined DataFrame information
        print(combined_df.head())
        combined_df.info()
        
        