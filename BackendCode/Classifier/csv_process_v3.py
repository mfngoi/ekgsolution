import pandas as pd

subject_randid_collection = []
subject_ethnicity_collection = []
subject_sex_collection = []
subject_age_collection = []
subject_height_collection = []
subject_weight_collection = []
avg_placebo_pr_collection = []
avg_placebo_qt_collection = []
avg_ranolazine_pr_collection = []
avg_ranolazine_qt_collection = []
avg_verapamil_pr_collection = []
avg_verapamil_qt_collection = []
avg_quinidine_pr_collection = []
avg_quinidine_qt_collection = []
avg_dofetilide_pr_collection = []
avg_dofetilide_qt_collection = []


for subject in range(1001, 1023):
    print(subject)
    csv = pd.read_csv(f"subjects/processed_dataset_{subject}.csv")

    rows = csv.shape[0]

    placebo_pr = []
    placebo_qt = []
    ranolazine_pr = []
    ranolazine_qt = []
    verapamil_pr = []
    verapamil_qt = []
    quinidine_pr = []
    quinidine_qt = []
    dofetilide_pr = []
    dofetilide_qt = []

    for i in range(rows):

        condition = csv['CONDITION'][i]

        if condition == 'Placebo':
            placebo_pr.append(csv['AVG_PR_INTERVAL'][i])
            placebo_qt.append(csv['AVG_QT_INTERVAL'][i])

        if condition == 'Ranolazine':
            ranolazine_pr.append(csv['AVG_PR_INTERVAL'][i])
            ranolazine_qt.append(csv['AVG_QT_INTERVAL'][i])

        if condition == 'Verapamil HCL':
            verapamil_pr.append(csv['AVG_PR_INTERVAL'][i])
            verapamil_qt.append(csv['AVG_QT_INTERVAL'][i])

        if condition == 'Quinidine Sulph':
            quinidine_pr.append(csv['AVG_PR_INTERVAL'][i])
            quinidine_qt.append(csv['AVG_QT_INTERVAL'][i])

        if condition == 'Dofetilide':
            dofetilide_pr.append(csv['AVG_PR_INTERVAL'][i])
            dofetilide_qt.append(csv['AVG_QT_INTERVAL'][i])

    subject_ethnicity = csv['ETHNICITY'][0]
    subject_sex = csv['SEX'][0]
    subject_age = csv['AGE'][0]
    subject_height = csv['HEIGHT'][0]
    subject_weight = csv['WEIGHT'][0]

    try:
        avg_placebo_pr = round(sum(placebo_pr) / len(placebo_pr),2)
        avg_placebo_pr_collection.append(avg_placebo_pr)
    except:
        avg_placebo_pr_collection.append(-1)

    try:
        avg_placebo_qt = round(sum(placebo_qt) / len(placebo_qt),2)
        avg_placebo_qt_collection.append(avg_placebo_qt)
    except:
        avg_placebo_qt_collection.append(-1)

    try:
        avg_ranolazine_pr = round(sum(ranolazine_pr) / len(ranolazine_pr),2)
        avg_ranolazine_pr_collection.append(avg_ranolazine_pr)
    except:
        avg_ranolazine_pr_collection.append(-1)

    try:
        avg_ranolazine_qt = round(sum(ranolazine_qt) / len(ranolazine_qt), 2)
        avg_ranolazine_qt_collection.append(avg_ranolazine_qt)
    except:
        avg_ranolazine_qt_collection.append(-1)

    try:
        avg_verapamil_pr = round(sum(verapamil_pr) / len(verapamil_pr), 2)
        avg_verapamil_pr_collection.append(avg_verapamil_pr)
    except:
        avg_verapamil_pr_collection.append(-1)

    try:
        avg_verapamil_qt = round(sum(verapamil_qt) / len(verapamil_qt), 2)
        avg_verapamil_qt_collection.append(avg_verapamil_qt)
    except:
        avg_verapamil_qt_collection.append(-1)

    try:
        avg_quinidine_pr = round(sum(quinidine_pr) / len(quinidine_pr), 2)
        avg_quinidine_pr_collection.append(avg_quinidine_pr)
    except:
        avg_quinidine_pr_collection.append(-1)

    try:
        avg_quinidine_qt = round(sum(quinidine_qt) / len(quinidine_qt), 2)
        avg_quinidine_qt_collection.append(avg_quinidine_qt)
    except:
        avg_quinidine_qt_collection.append(-1)

    try:
        avg_dofetilide_pr = round(sum(dofetilide_pr) / len(dofetilide_pr), 2)
        avg_dofetilide_pr_collection.append(avg_dofetilide_pr)
    except:
        avg_dofetilide_pr_collection.append(-1)

    try:
        avg_dofetilide_qt = round(sum(dofetilide_qt) / len(dofetilide_qt), 2)
        avg_dofetilide_qt_collection.append(avg_dofetilide_qt)
    except:
        avg_dofetilide_qt_collection.append(-1)


    # Track each subject's info
    subject_randid_collection.append(subject)
    subject_ethnicity_collection.append(subject_ethnicity)
    subject_sex_collection.append(subject_sex)
    subject_age_collection.append(subject_age)
    subject_height_collection.append(subject_height)
    subject_weight_collection.append(subject_weight)


# Build dataframe out of all the compiled columns
collected_dataframe = pd.DataFrame(
    {
        'RANDID': subject_randid_collection,
        'RACE': subject_ethnicity_collection,
        'SEX': subject_sex_collection,
        'AGE': subject_age_collection,
        'HEIGHT': subject_height_collection,
        'WEIGHT': subject_weight_collection,
        'PLACEBO_PR': avg_placebo_pr_collection,
        'PLACEBO_QT': avg_placebo_qt_collection,
        'RANOLAZINE_PR': avg_ranolazine_pr_collection,
        'RANOLAZINE_QT': avg_ranolazine_qt_collection,
        'VERAPAMIL_PR': avg_verapamil_pr_collection,
        'VERAPAMIL_QT': avg_verapamil_qt_collection,
        'QUINIDINE_PR': avg_quinidine_pr_collection,
        'QUINIDINE_QT': avg_quinidine_qt_collection,
        'DOFETILIDE_PR': avg_dofetilide_pr_collection,
        'DOFETILIDE_QT': avg_dofetilide_qt_collection,
        # ...
    }
)

# print(collected_dataframe)
collected_dataframe.to_csv(f"subjects/collected_dataset.csv")




    
