import pandas as pd
import numpy as np
from pathlib import Path
import os

# Directory setup
data_dir = Path("monthdata")

def read_monthly_data(month):
    """
    Read a specific month's data from Excel file.
    Args:
        month (str): Month name (e.g., 'May', 'June', etc.)
    Returns:
        pd.DataFrame: DataFrame containing the month's data
    """
    try:
        # Map of standardized filenames
        file_mapping = {
            'May': 'May_Data_Matrix (1).xlsx',
            'June': 'June_Data_Matrix.xlsx',
            'July': 'July_Data_Matrix (1).xlsx',
            'August': 'August_Data_Matrix (1).xlsx',
            'September': 'September_Data_Matrix.xlsx',
            'October': 'October_Data_Matrix_20251103_214000.xlsx'
        }
        
        if month not in file_mapping:
            raise ValueError(f"Invalid month. Choose from: {', '.join(file_mapping.keys())}")
        
        file_path = data_dir / file_mapping[month]
        df = pd.read_excel(file_path)
        print(f"Successfully read {month} data with {len(df)} rows")
        return df
    except FileNotFoundError:
        print(f"Error: {month} Excel file not found")
        return None
    except Exception as e:
        print(f"Error reading {month} data: {str(e)}")
        return None

def read_all_monthly_data():
    """
    Read and combine all monthly data files.
    Returns:
        pd.DataFrame: Combined DataFrame containing all months' data
    """
    months = ['May', 'June', 'July', 'August', 'September', 'October']
    dfs = []
    
    for month in months:
        df = read_monthly_data(month)
        if df is not None:
            # Add month column if not already present
            if 'Month' not in df.columns:
                df['Month'] = month
            dfs.append(df)
    
    if not dfs:
        print("No monthly data files were successfully read")
        return None
    
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Successfully combined {len(dfs)} months of data with {len(combined_df)} total rows")
    return combined_df

def read_shipment():
    """
    Read the shipment data CSV file.
    Returns:
        pd.DataFrame: DataFrame containing shipment data
    """
    try:
        file_path = 'MSY Data - Shipment.csv'
        shipment_df = pd.read_csv(file_path)
        print(f"Successfully read shipment data with {len(shipment_df)} rows")
        return shipment_df
    except FileNotFoundError:
        print("Error: Shipment CSV file not found")
        return None
    except Exception as e:
        print(f"Error reading shipment data: {str(e)}")
        return None

def read_ingredients():
    """
    Read the ingredient data CSV file.
    Returns:
        pd.DataFrame: DataFrame containing ingredient data
    """
    try:
        file_path = 'MSY Data - Ingredient.csv'
        ingredient_df = pd.read_csv(file_path)
        print(f"Successfully read ingredient data with {len(ingredient_df)} rows")
        return ingredient_df
    except FileNotFoundError:
        print("Error: Ingredient CSV file not found")
        return None
    except Exception as e:
        print(f"Error reading ingredient data: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    shipment = read_shipment()
    ingredients = read_ingredients()
    
    if shipment is not None:
        print("\nShipment Data Info:")
        print(shipment.info())
        print("\nFirst few rows of shipment data:")
        print(shipment.head())
    
    if ingredients is not None:
        print("\nIngredient Data Info:")
        print(ingredients.info())
        print("\nFirst few rows of ingredient data:")
        print(ingredients.head())

        # Read monthly data
        print("\nReading monthly data...")
        # Example of reading a single month
        may_data = read_monthly_data('May')
        if may_data is not None:
            print("\nMay Data Info:")
            print(may_data.info())
            print("\nFirst few rows of May data:")
            print(may_data.head())
    
        # Example of reading all months combined
        all_monthly_data = read_all_monthly_data()
        if all_monthly_data is not None:
            print("\nAll Monthly Data Info:")
            print(all_monthly_data.info())
            print("\nSample of rows from each month:")
            print(all_monthly_data.groupby('Month').head(2))
        
