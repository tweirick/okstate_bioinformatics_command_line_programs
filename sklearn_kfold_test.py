from sklearn import cross_validation

X = np.array([[1, 2], [3, 4], [1, 2], [3, 4]])
y = np.array([1, 2, 3, 4])
kf = cross_validation.KFold(4, n_folds=2)


