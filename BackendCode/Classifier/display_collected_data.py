import pandas as pd
import matplotlib.pyplot as plt

csv = pd.read_csv(f"subjects/collected_dataset.csv")

RACE = 'WHITE' # WHITE, ASIAN, AFRICAN AMERICAN
SEX = 'M' # M, F
CONDITION = 'PLACEBO' # RANOLAZINE, VERAPAMIL, QUINIDINE, DOFETILIDE, PLACEBO


# Placebo White PR
race_csv = csv.loc[csv['RACE'] == RACE]
race_sex_csv = race_csv.loc[race_csv['SEX'] == SEX]

plt.title(f"{RACE} {CONDITION} (AVG_PR vs AGE)")
plt.xlabel('AGE')
plt.ylabel('AVG_PR')
plt.scatter(race_sex_csv['AGE'],race_sex_csv[f"{CONDITION}_PR"])
plt.show()

plt.title(f"{RACE} {CONDITION} (AVG_QT vs AGE)")
plt.xlabel('AGE')
plt.ylabel('AVG_QT')
plt.scatter(race_sex_csv['AGE'],race_sex_csv[f"{CONDITION}_QT"])
plt.show()


asian_csv = csv.loc[csv['RACE'] == 'ASIAN']

african_csv = csv.loc[csv['RACE'] == 'AFRICAN AMERICAN']

# Placebo
    # WHITE
        # PR vs AGE
        # QT vs AGE

    # ASIAN
        # PR vs AGE
        # QT vs AGE

    # AFRICAN AMERICAN
        # PR vs AGE
        # QT vs AGE


