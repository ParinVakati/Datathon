import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_monthly_sales(file_paths):
    #loads all monthly sales xlsx files and combines them
    #pile_paths is the dictionaly with month as key and file path as value

    sales_data = {}

    for month, filepath in file_paths.items():
        df = pd.read_excel(filepath)
        df['month'] = month
        sales_data[month] = df

    file = open("Ingredient.csv", "r")
