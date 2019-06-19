import nltk
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path


# FIXME Check the integrity of the pickles before trying to construct the pickles
def _checkIntegrityPickle():
    return False


if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('words')

    # FIXME give the option to use the full dataset or a 10 percent
    path_to_formatted = (Path(__file__).parent /
                         "../dataSets/formated/ds.csv").resolve()
    path_to_ten_percent = (Path(__file__).parent /
                           "../dataSets/formated/ds_10.csv").resolve()

    df = pd.read_csv(path_to_formatted, header=0, dtype=object,
                     na_filter=False)

    # FIXME The number of features will depend on the classifier used, for NaiveBayes
    # using all seems to give the best accuracy, investigate random forest and logistic regression.
    tf = TfidfVectorizer(stop_words="english", analyzer="word") # , max_features=2)

    trained = tf.fit(df.words)

    x = trained.fit_transform(df.words)
    # FIXME Use the label encoder to transform the other features
    # FIXME np.concatenate axis 0, to use the rest of the features once transformed
    # IE:
    # y = LabelEncoder().fit(['spam', 'ham']).transform(df['classification'])
    y = df['classification']

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
                                                        random_state=40)

    print("X_train shape: ", X_train.shape)
    print("y_train shape: :", y_train.shape)
    print("X_test shape: ", X_test.shape)
    print("Y_test shape: ", y_test.shape)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    print("Finished training")
    print("Targets: ", clf.classes_)

    print("Test set accuracy: {}".format(clf.score(X_test, y_test)))
    print("Confusion matrix test: \n{}\n".format(confusion_matrix(y_test, clf.predict(X_test))))
    print(classification_report(y_test, clf.predict(X_test)))

    print("Train set accuracy: {}".format(clf.score(X_train, y_train)))
    print("Confusion matrix train: \n{}\n".format(confusion_matrix(y_train, clf.predict(X_train))))
    print(classification_report(y_train, clf.predict(X_train)))

    with open('NBfullcsv_trained.pickle', 'wb') as handle:
        pickle.dump(clf.fit(x, y), handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('TfidfVectorizer_fitted.pickle', 'wb') as handle:
        pickle.dump(trained, handle, protocol=pickle.HIGHEST_PROTOCOL)
