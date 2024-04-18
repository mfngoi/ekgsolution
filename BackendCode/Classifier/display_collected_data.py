import pandas as pd
import matplotlib.pyplot as plt

csv = pd.read_csv(f"collected_dataset.csv")

RACE = 'WHITE' # WHITE, ASIAN, AFRICAN AMERICAN
SEX = 'M' # M, F
CONDITION = 'PLACEBO' # RANOLAZINE, VERAPAMIL, QUINIDINE, DOFETILIDE, PLACEBO


# Placebo White PR
race_csv = csv.loc[csv['RACE'] == RACE]
race_sex_csv = race_csv.loc[race_csv['SEX'] == SEX]

plt.title(f"{RACE} {CONDITION} (AVG_P_WAVE vs AGE)")
plt.xlabel('AGE')
plt.ylabel('AVG_P_WAVE')
plt.scatter(race_sex_csv['AGE'],race_sex_csv[f"{CONDITION}_P_WAVE"])
plt.show()

plt.title(f"{RACE} {CONDITION} (AVG_QTC vs AGE)")
plt.xlabel('AGE')
plt.ylabel('AVG_QTC')
plt.scatter(race_sex_csv['AGE'],race_sex_csv[f"{CONDITION}_QTC_INTERVAL"])
plt.show()
