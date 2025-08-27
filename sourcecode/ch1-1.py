import pandas as pd
import numpy as np

df = pd.read_csv('./datasets/bike_rentals/bike_rentals.csv')
df.iloc[2, 3] = np.nan
df.head(10)
