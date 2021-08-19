import pandas as pd
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('ML_data.csv')

# Label Encoder
le = LabelEncoder()
df['Classification'] = le.fit_transform(df['Classification'].astype('str'))

# drop label
Y = df['Classification'].values
X = df.drop('Classification', axis=1).values

# Training : Test = 8:2
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size =0.3, random_state =1)

# Build model
svc = svm.SVC()
dtc = DecisionTreeClassifier()
rfc = RandomForestClassifier(max_depth=2, random_state=0)

# Train model
svc.fit(X_train, Y_train)
dtc.fit(X_train, Y_train)
rfc.fit(X_train, Y_train)

#Test model
Y_pred_svm = svc.predict(X_test)
Y_pred_tree = dtc.predict(X_test)
Y_pred_rf = rfc.predict(X_test)

print ("Decision Tree: ")
# Measuring performance using Accuracy
print ("Accuracy: ", accuracy_score (Y_pred_tree, Y_test))

#Measuring the performance using Confusion Matrix
print ("Confusion Matrix: \n", confusion_matrix (Y_pred_tree, Y_test))

print ("SVM: ")
# Measuring performance using Accuracy
print ("Accuracy: ", accuracy_score (Y_pred_svm, Y_test))

#Measuring the performance using Confusion Matrix
print ("Confusion Matrix: \n", confusion_matrix (Y_pred_svm, Y_test))

print ("Random Forest: ")
# Measuring performance using Accuracy
print ("Accuracy: ", accuracy_score (Y_pred_rf, Y_test))

#Measuring the performance using Confusion Matrix
print ("Confusion Matrix: \n", confusion_matrix (Y_pred_rf, Y_test))