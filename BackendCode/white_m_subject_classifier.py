from sklearn import svm
import pickle

# ,RANDID,RACE,SEX,AGE,HEIGHT,WEIGHT,PLACEBO_PR,PLACEBO_QT,RANOLAZINE_PR,RANOLAZINE_QT,VERAPAMIL_PR,VERAPAMIL_QT,QUINIDINE_PR,QUINIDINE_QT,DOFETILIDE_PR,DOFETILIDE_QT
# 11,1012,WHITE,M,21,180.1,61.8,55.25,417.44,55.01,424.96,53.55,415.51,52.86,421.84,52.21,430.67
# 12,1013,WHITE,M,32,175.5,74.1,103.15,364.21,103.66,369.58,103.07,364.71,107.21,397.08,103.05,384.55
# 13,1014,ASIAN,M,35,168.5,65.5,106.51,413.56,108.36,440.75,104.28,437.11,108.81,471.74,108.36,443.56
# 14,1015,WHITE,M,19,182.5,63.5,120.9,377.47,120.1,393.08,118.74,374.9,120.06,424.01,117.99,404.99
# 15,1016,WHITE,M,25,177.5,78.1,113.59,351.96,112.97,368.73,110.31,370.76,113.06,396.65,115.38,389.67
# 16,1017,WHITE,M,21,170.1,74.6,97.03,375.8,102.23,381.96,97.08,379.62,94.11,428.25,97.61,398.03
# 17,1018,WHITE,M,30,182.0,73.3,102.86,368.32,103.39,372.79,110.29,380.84,100.93,355.38,97.64,376.0
# 19,1020,WHITE,M,20,185.0,61.6,101.6,358.41,91.45,363.05,101.56,349.13,91.21,397.43,91.9,390.7
# 21,1022,WHITE,M,35,174.5,69.5,100.97,385.07,109.59,375.44,107.32,389.48,110.83,412.61,110.64,412.04


training_data = [
    [21.0, float(61.8 / 180.1**2)], # WHITE M  [age, bmi (weight/height^2)]
    [32.0, float(74.1 / 175.5**2)], # WHITE M
    [19.0, float(63.5 / 182.5**2)], # WHITE M
    [25.0, float(78.1 / 177.5**2)], # WHITE M
    [21.0, float(74.6 / 170.1**2)], # WHITE M
    [30.0, float(73.3 / 182.0**2)], # WHITE M
    [20.0, float(61.6 / 185.0**2)], # WHITE M
    [35.0, float(69.5 / 174.5**2)] # WHITE M
]

training_label = range(len(training_data))

# Select an algorithm
model = svm.SVC() # SVC is a ML algorithm

# Train the model
model.fit(training_data, training_label) # Classifer to find the closest white male subject to a white male subject user based off age and bmi

# Save trained model to disk
with open('models/white_male_classifier.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Saved model to disk... ")

# # Use the model
# print(
#     model.predict([
#         [5.1,3.5,1.4,0.2],
#         [6.5,2.8,4.6,1.5],
#         [7.2,3.0,5.8,1.6]
#     ])
# )