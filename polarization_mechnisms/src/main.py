import logging
import os

import pandas as pd

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logging.info('Configured logger')
BASE_DB_PATH = f"{os.getcwd()}/../resources/database/"

# df = pd.read_csv(f"{os.getcwd()}/../resources/database/experiments_configs")


d = {'updated_at': [1, 2], 'id': [3, 3], 'b': [5, 6]}
df = pd.DataFrame(data=d)
print(df['id'].values)
# df.sort_values("updated_at")
# df.drop_duplicates(inplace=True, keep='last', subset=['a'])
# print(df)
