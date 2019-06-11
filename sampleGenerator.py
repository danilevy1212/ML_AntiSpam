import math
import numpy as np
import pandas as pd
from pathlib import Path


def createRandom10PercentSample():
    parent_dir = Path(__file__).parent
    path_to_formatted = (parent_dir /
                         "../dataSets/formated/ds_full.csv").resolve()
    path_to_10 = (parent_dir /
                  "../dataSets/formated/ds_10.csv") .resolve()

    df = pd.read_csv(path_to_formatted, header=0, dtype=object,
                     na_filter=False)
    df_shuffled = df.reindex(np.random.permutation(df.index))
    ten_percent_ind = math.floor(df_shuffled.shape[0]*0.1)
    df_shuffled.loc[[i for i in range(ten_percent_ind)], :].to_csv(path_to_10,
                                                                   index=False)
