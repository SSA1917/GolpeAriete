import numpy as np
import pandas as pd

TablaGeneral = pd.read_csv('./TablaVersion1.csv')


QCaudalSection0 = TablaGeneral['Q0']
QSectionArray = QCaudalSection0.to_numpy() 
print(QSectionArray.std())
