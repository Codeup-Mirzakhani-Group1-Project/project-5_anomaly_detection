import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def get_anonymized_curriculum_access_data():
    # Import .txt file and convert it to a DataFrame object
    df = pd.read_table("anonymized-curriculum-access.txt", sep = '\s', header = None, 
                    names = ['date', 'time', 'page', 'id', 'cohort', 'ip'])
    
    return df