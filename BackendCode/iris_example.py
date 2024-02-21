from sklearn import svm

training_data = [
[5.1,3.5,1.4,0.2], # 10 sec ekg reading from one file
[7.0,3.2,4.7,1.4],
]

training_label = ["l. setosa", "l. versicolor"]

model = svm.SVC()
model.fit(training_data, training_label) # Training

answer = model.predict([[5.5,3.5,1.3,0.2]])

print(answer)