import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

def import_files(path: str) -> pd.DataFrame:
    columns = ['Season', 'Position', 'Team', 'Played', 'Won', 'Lost', 'Tied', 'No Result', 'Net Run Rate', 'Score For', 'Overs For', 'Score Against', 'Overs Against', 'Points', 'Qualified?', 'Winner?']
    df = pd.DataFrame(columns=columns)
    for file_name in os.listdir(path):
        df_aux = pd.read_csv(f'{path}/{file_name}')
        df = pd.concat([df, df_aux], axis=0)
    X = df.drop(['Team', 'Position', 'Qualified?', 'Winner?'], axis=1)
    X = X.astype(float)
    y = df['Qualified?']
    y = y.astype(float)
    return X, y

X, y = import_files('Datasets')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

CLASSIFIERS = {SVC(): 'Support Vector Machine', 
               KNeighborsClassifier(): 'K-Nearest Neighbors', 
               DecisionTreeClassifier(): 'Decision Tree', 
               RandomForestClassifier(): 'Random Forest', 
               MultinomialNB(): 'Naive Bayes', 
               MLPClassifier(): 'Perceptron'}

def evaluate_classifier(clf, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test) -> float:
    model = clf.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_true=y_test, y_pred=y_pred)
    prec = precision_score(y_true=y_test, y_pred=y_pred, zero_division=0)
    rec = recall_score(y_true=y_test, y_pred=y_pred, zero_division=0)
    return acc, prec, rec

def train() -> list:
    results = pd.DataFrame(columns=['Model', 'Accuracy', 'Precision', 'Recall'])
    for index, clf in enumerate(CLASSIFIERS.keys()):
        if isinstance(clf, MultinomialNB):
            X_train_ = X_train.drop(['Net Run Rate'], axis=1)
            X_test_ = X_test.drop(['Net Run Rate'], axis=1)
            acc, prec, rec = evaluate_classifier(clf, X_train_, X_test_)
        else:
            acc, prec, rec = evaluate_classifier(clf)
        row = [CLASSIFIERS[clf], acc, prec, rec]
        results.loc[index] = row
    return results

def run():
    results = train()
    results = results.set_index('Model')
    ax = results.plot(kind='bar')
    ax.set_xlabel('Models', ha='center', fontsize=10)
    ax.set_ylabel('Values')
    ax.set_title('Performance Metrics')
    plt.legend(loc='upper right', fontsize='small')
    plt.xticks(rotation=0, fontsize=5)
    plt.show()

run()