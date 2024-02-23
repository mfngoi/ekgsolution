import pandas as pd
import numpy as np
import neurokit2 as nk
from sklearn.preprocessing import LabelEncoder

# Load data from compiled csv
file_content = pd.read_csv('target/compiled_dataset.csv')
print(file_content)

# Extract ecg readings as training data
training_data_df = file_content.iloc[:, 32:10033]   # Extract ekg data
print(training_data_df)

# Convert training data to numpy array
training_data_np = training_data_df.to_numpy()
print(training_data_np)

condition_col = file_content['EXTRT']
sex_col = file_content['SEX']
age_col = file_content['AGE']
height_col = file_content['HGHT']
width_col = file_content['WGHT']
ethnicity_col = file_content['RACE']
# r_peak_col = np.random.randn(5232)       # How to retrieve the average rpeak
# pr_int_col = np.random.randn(5232)


# Encode any columns that are not numeric
condition_col = LabelEncoder().fit_transform(condition_col)
sex_col = LabelEncoder().fit_transform(sex_col)

processed_dataset = pd.DataFrame(
    {
        'CONDITION': condition_col,
        'SEX': sex_col,
        'AGE': age_col,
        'HEIGHT': height_col,
        'WIDTH': width_col,
        'ETHNICITY': ethnicity_col,
        'R_PEAK': r_peak_col,         # Should contain the average rpeak of a 10 sec period
        'PR_INT': pr_int_col,
        'PR_SEGMENT': pr_seg_col,
    }
)

print(processed_dataset)