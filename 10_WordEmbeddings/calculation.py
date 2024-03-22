import numpy as np

eingabevektor = np.array([[0],[0],[0],[1],[0],[0],[0]])
gewichtsmatrix = np.array([[0.5,1.6,-1.75,5,0.1,0,1.5], [1.75,2.5,-6,1.6,-2.3,2,0.85], [-2,4,1.25,4.85,1.2,3.8,-0.5]])

projektion = np.dot(gewichtsmatrix, eingabevektor)



print(projektion)