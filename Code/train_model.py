
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA


class train():
    def __init__(self, train_inputs, k_value):
        super(train, self).__init__()
       #attributes
        self.accuracy = 0
        self.data = 0
        self.train_inputs = train_inputs
        self.model_algorithm = 0
        self.k_value = int(k_value)

        #functions
        self.data_processing()
        self.create_model()

        print("Training complete")
####==================================   CREATE MODEL FUNCTION ====================================############

    def create_model(self):
        print("Creating model...")
        print("Data in model class is:",self.train_inputs)

        #######  TRAIN AND SPLIT #######
        train_split = int(self.train_inputs[1][0] + self.train_inputs[1][1] ) #only take the first two digits since it has a %
        test_split = (100 - train_split)/100
        model_algorithim = self.train_inputs[2]

        # make table for preprocessing
        column_names = ["Distance(mi)", "Temperature(F)","Wind_Chill(F)", "Humidity(%)", "Pressure(in)",
                        "Visibility(mi)", "Wind_Speed(mph)", "Precipitation(in)",
                        "Severity"]

        X = [list(self.data["Distance(mi)"]), list(self.data["Temperature(F)"]),
             list(self.data["Wind_Chill(F)"]), list(self.data["Humidity(%)"]), list(self.data["Pressure(in)"]),
             list(self.data["Visibility(mi)"]), list(self.data["Wind_Speed(mph)"]), list(self.data["Precipitation(in)"])]
        X = np.transpose(X)
        y = list(self.data["Severity"])


        #if the model is KNN, perform PCA before splitting,
        if self.train_inputs == "KNN":
            X = PCA().fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=0)


        #########   PICKED MODEL GOES HERE   ###
        if self.train_inputs[2] == "Decision Trees":
            self.decision_tree(X_train, X_test, y_train, y_test)
        elif self.train_inputs[2] == "Random Forest":
            self.random_forest(X_train, X_test, y_train, y_test)
        elif self.train_inputs[2] == "Logistic Regression":
            self.logistic_regression(X_train, X_test, y_train, y_test)
        elif self.train_inputs[2] == "KNN":
            self.knn_classifier(X_train, X_test, y_train, y_test)
        elif self.train_inputs[2] == "SVM":
            self.svm_classifier(X_train, X_test, y_train, y_test)
        elif self.train_inputs[2] == "Naive Bayes":
            self.naive_bayes(X_train, X_test, y_train, y_test)


###================================ MACHINE LEARNING FUNCTIONS =====================================###
    def decision_tree(self, X_train, X_test, y_train, y_test):
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        sc.fit(X_train)
        X_train_std = sc.transform(X_train)
        X_test_std = sc.transform(X_test)
        X_combined_std = np.vstack((X_train_std, X_test_std))
        y_combined = np.hstack((y_train, y_test))

        # Build decision tree model
        # visualize tree train
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X_train, y_train)
        print("Model created")

        # Predict test from train
        y_pred = clf.predict(X_test)
        print("shape of y_pred:", X_test.shape)
        print("y_pred:", X_test)
        acc_score = accuracy_score(y_test, y_pred)
        self.accuracy = (acc_score * 100).round(2)
        # Accuracy
        print('DT Accuracy:', acc_score)
        print('DT Accuracy:', self.accuracy)
        self.model_algorithm = clf
        print("train model is:", clf)


    def random_forest(self, X_train, X_test, y_train, y_test):
        rf = RandomForestClassifier(n_estimators=100, random_state=23, verbose=3,
                                    n_jobs=-1)  # https://stackoverflow.com/questions/43640546/how-to-make-randomforestclassifier-faster
        rf.fit(X_train, y_train)  # https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
        predictions = rf.predict(X_test)  # Calculate the absolute errors

        # Accuracy
        accuracy = accuracy_score(y_test, predictions)*100
        print('Random Forest Model Accuracy:', round(accuracy, 2), '%.')


        self.accuracy = round(accuracy, 2)
        self.model_algorithm = rf
        print("train model is:", rf)

    def logistic_regression(self, X_train, X_test, y_train, y_test):
        regressor = LogisticRegression()
        regressor.fit(X_train, y_train)  # training the algorithm
        predictions = regressor.predict(X_test)

        # Accuracy
        accuracy = accuracy_score(y_test, predictions)*100
        reg_score = regressor.score(X_test,y_test)
        print('Logistic Regression Model Accuracy:', round(accuracy, 2), '%.')
        print('Logistic Regression Score:', round(reg_score, 2), '%.')


        self.accuracy = round(accuracy, 2)
        self.model_algorithm = regressor
        print("train model is:", regressor)

    def knn_classifier(self, X_train_PCA, X_test_PCA, y_train_PCA, y_test_PCA):
        import matplotlib.pyplot as plt
        import seaborn as sns
        from sklearn.neighbors import KNeighborsClassifier
        neigh = KNeighborsClassifier(n_neighbors=self.k_value,n_jobs=-1)
        neigh.fit(X_train_PCA, y_train_PCA)
        predictions = neigh.predict(X_test_PCA)

        # Accuracy
        accuracy = accuracy_score(y_test_PCA, predictions)*100
        print('KNN Model Accuracy:', round(accuracy, 2), '%.')

        self.accuracy = round(accuracy, 2)
        self.model_algorithm = neigh
        print("train model is:", neigh)




        from sklearn.neighbors import KNeighborsClassifier
        k_range = range(1, 26, 2)

        # We can create Python dictionary using [] or dict()
        scores = []

        for k in k_range:
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X_train_PCA, y_train_PCA)
            y_pred = knn.predict(X_test_PCA)
            scores.append(accuracy_score(y_test_PCA, y_pred))

        # plot the relationship between K and testing accuracy
        # plt.plot(x_axis, y_axis)
        plt.clf()
        plt.plot(k_range, scores)
        plt.xlabel('Value of K for KNN')
        plt.ylabel('Testing Accuracy')
        plt.savefig('k_accuracy.png')

    def svm_classifier(self, X_train, X_test, y_train, y_test):
        from sklearn.svm import LinearSVC
        clf = LinearSVC(random_state=0, tol=1e-5)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        # Accuracy
        accuracy = accuracy_score(y_test, predictions) * 100
        print('SVM Accuracy:', round(accuracy, 2), '%.')

        self.accuracy = round(accuracy, 2)
        self.model_algorithm = clf
        print("train model is:", clf)

    def naive_bayes(self, X_train, X_test, y_train, y_test):
        from sklearn.naive_bayes import GaussianNB
        clf = GaussianNB()
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)

        # Accuracy
        accuracy = accuracy_score(y_test, predictions) * 100
        print('Naive Bayes Model Accuracy:', round(accuracy, 2), '%.')

        self.accuracy = round(accuracy, 2)
        self.model_algorithm = clf
        print("train model is:", clf)

#########-------------------------------------- DATA PROCESSING AND ANALYSIS -------------------------------------- #########
    def data_processing(self):
        ######### DATA PROCESSING  #########
        print("--------------------------DATA PROCESSING--------------------------")
        print("Processing sample size of:", self.train_inputs[0])

        datafile = "US_Accidents_Dec19.csv"

        try:
            import pre_process
        except:
            print("import exception")

        data_instance = pre_process.data_frame(datafile, self.train_inputs)
        self.data = data_instance.create_dataframe()
        data_instance.cleanup_data()

        ######### DATA ANALYSIS  #########
        print("--------------------------DATA ANALYSIS--------------------------")
        try:
            import eda_stats
        except:
            print("import exception")
        data_analysis = eda_stats.eda(self.data)
        data_analysis.perform_eda()
###============================== GET DATA FUNCTIONS ===============================###########
    def get_map_data_points(self):
        return self.data
    def get_model_accuracy(self):
        return self.accuracy
    def get_model(self):
        return self.model_algorithm
