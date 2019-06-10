import mailparser
import math
import csv
import random
import numpy as np
import pandas as pd
from featureExtractor import featExt
from dsWriter import dsWriter
from nltk.corpus import words
from pathlib import Path

def createRandom10PercentSample():
   path_to_formatted = (Path(__file__).parent / "../dataSets/formated/ds_full.csv").resolve()
   path_to_ten_percent = (Path(__file__).parent / "../dataSets/formated/ds_10.csv").resolve()

   df = pd.read_csv(path_to_formatted, header=0,dtype=object,na_filter=False)
   df_shuffled = df.reindex(np.random.permutation(df.index))
   ten_percent_ind = math.floor(df_shuffled.shape[0]*0.1)
   df_shuffled.loc[[i for i in range(ten_percent_ind)], :].to_csv(path_to_ten_percent, index=False)
