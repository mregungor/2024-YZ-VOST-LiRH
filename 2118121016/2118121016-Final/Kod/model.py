import pickle
import joblib
import numpy
import pandas
import sklearn.ensemble as ek
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

dataset = pandas.read_csv('C:/Users/Makbaba/Desktop/Virus_Vigilante/datasets/dataset_1.csv', sep=',', low_memory=False)



# Veri ön işleme
X = dataset.drop(['ID', 'md5', 'legitimate'], axis=1).values
y = dataset['legitimate'].values


extratrees = ek.ExtraTreesClassifier().fit(X, y)
model = SelectFromModel(extratrees, prefit=True)
X_new = model.transform(X)
nbfeatures = X_new.shape[1]


X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2)

features = []
index = numpy.argsort(extratrees.feature_importances_)[::-1][:nbfeatures]
for f in range(nbfeatures):
    features.append(dataset.columns[2 + f])



model = ek.RandomForestClassifier(n_estimators=500, max_depth=4, n_jobs=-1)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print("Accuracy:", (score * 100), '%')

joblib.dump(model, "model/model.pkl")
open('model/features.pkl', 'wb').write(pickle.dumps(features))

# Yanlış Pozitifler ve Negatifler
res = model.predict(X_new)
mt = confusion_matrix(y, res)
print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0]))) * 100))
print('False negative rate : %f %%' % (mt[1][0] / float(sum(mt[1])) * 100))
