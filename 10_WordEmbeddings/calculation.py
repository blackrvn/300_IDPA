import numpy as np
from icecream import ic
from scipy.special import softmax

eingabevektor = np.array([[0], [0], [0], [1], [0], [0], [0]])
ic(eingabevektor.shape)
gewichtsmatrix = np.array([
    [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2],
    [0.4, 0.6, 0.8, 1, 0.2, 0.4, 0.6],
    [0.8, 1, -0.2, -0.4, -0.6, -0.8, -1]
])
ic(gewichtsmatrix.shape)
projektion = np.dot(gewichtsmatrix, eingabevektor)
ic(projektion.shape)
ic(projektion)
gewichtsmatrix_ausgabe = np.array([
    [0.54, -0.88, -0.10, -0.01, -0.96, 0.50, 0.11],
    [-0.72, -0.78, 0.69, -0.75, 0.29, -0.59, 0.52],
    [0.98, -0.21, -0.61, -0.41, 0.56, 0.06, -0.97]
]).transpose()

ausgabevektor = np.dot(gewichtsmatrix_ausgabe, projektion)

normalisiert = softmax(ausgabevektor)

ic(ausgabevektor)
ic(ausgabevektor.shape)
ic(normalisiert)
