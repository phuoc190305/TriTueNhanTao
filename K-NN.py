import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # datavisualization
from sklearn.datasets import make_blobs # synthetic dataset
from sklearn.neighbors import KNeighborsClassifier # kNN classifier
from sklearn.model_selection import train_test_split # train and test sets

X,y = make_blobs(n_samples = 100, n_features = 2, centers = 4,
cluster_std = 1, random_state = 4)

plt.figure(figsize=(9, 6))
plt.scatter(X[:, 0], X[:, 1], c=y, marker='o', s=50)
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=0)
plt.figure(figsize = (9,6))
plt.scatter(X_test[:,0], X_test[:,1], c=y_test, marker= 'o', s=40)
plt.show()

knn5 = KNeighborsClassifier(5) # k=5
knn5.fit(X_train, y_train)
y_pred_5 = knn5.predict(X_test)
plt.figure(figsize = (9,6))
plt.scatter(X_test[:,0], X_test[:,1], c=y_pred_5, marker= 'o', s=40)
plt.show()

knn1 = KNeighborsClassifier(1) # k=1
knn1.fit(X_train, y_train)
y_pred_1 = knn1.predict(X_test)
plt.figure(figsize = (9,6))
plt.scatter(X_test[:,0], X_test[:,1], c=y_pred_1, marker= 'o', s=40)
plt.show()

from sklearn.model_selection import GridSearchCV
knn_grid = GridSearchCV(estimator = KNeighborsClassifier(),
param_grid={'n_neighbors': np.arange(1,10)}, cv=5)
knn_grid.fit(X,y)
print (knn_grid.best_params_)

def KNN(X_train,X_test,y_train,k):
    num_test = X_test.shape[0] # số lượng dữ liệu test
    num_train = X_train.shape[0] # số lượng dữ liệu train
# y_pred là một ma trận, mỗi hàng tương ứng là khoảng cách của một điểm dữ liệu trong tập test đối với tất cả các điểm dữ liệu trong tập train
    y_pred = np.zeros((num_test,num_train))
    # duyệt qua mỗi điểm trong tập test
    for i in range(num_test):
        # tương ứng một điểm trong tập test sẽ duyêt qua hết bộ train
        for j in range(num_train):
            # tính khoảng cách tới tập train
            y_pred[i,j] = np.sqrt(np.sum(np.power(X_test[i,:]-
X_train[j,:],2)))
    results = []
# sắp xếp theo chiều tăng dần khoảng cách
    for i in range(len(y_pred)):
        zipped = zip(y_pred[i,:],y_train)
        res = sorted(zipped,key = lambda x:x[0])
        results_topk = res[:k]
        # Đếm số lượng của mỗi class
        classes = {}
        for _,j in results_topk:
            j = int(j)
            if j not in classes:
                classes[j] = 1
            else:
                classes[j] = classes[j] + 1
# trả về class có số lượng nhiều nhất
        results.append(max(classes,key = classes.get))
    return np.array(results)

(X,y) = make_blobs(n_samples = 500, n_features = 2, centers = 4,
cluster_std = 1, random_state = 4)
X_test=np.array([(1,3)])
results = KNN(X,X_test,y,3)
print (results)