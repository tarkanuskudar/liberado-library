import pandas as pd
import random

# data_xls = pd.read_excel(r'/Users/mac/Desktop/python_project/Project_Database.csv.xlsx')
#
# data_xls.to_csv('csvfile.csv', encoding='utf-8')

stars = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

library = pd.read_csv('csvfile')

library['Stars'] = [random.choice(stars) for _ in range(0, 500)]

library['Copies'] = [random.randint(1, 10) for _ in range(0, 500)]

library.to_csv('csvfile', index = False)