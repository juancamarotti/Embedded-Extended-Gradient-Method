import numpy as np 

N = [0.3016, 0.59677, 0.1016]

B_gp1 = [-1.2619, 1.2619, 0.1690]
B_gp2 = [-0.3381, 0.3381, 0.6310]

LHS_1 = np.outer(N, N)

LHS_2 = np.outer(B_gp1, B_gp1)*1.25*0.5 + np.outer(B_gp2, B_gp2)*1.25*0.5

RHS_1 = np.outer(N, 0.5)

RHS_2 = np.outer(B_gp1, 1.0)*1.25*0.5 + np.outer(B_gp2, 1.0)*1.25*0.5

print('here', np.linalg.cond(LHS_1+LHS_2))

solution = np.linalg.solve(LHS_1+LHS_2, RHS_1+RHS_2)

print(LHS_1)
print(np.linalg.cond(LHS_1))

print(LHS_2)
print(np.linalg.cond(LHS_2))

print(LHS_1+LHS_2)
print(np.linalg.cond(LHS_1+LHS_2))

print("sol", solution)