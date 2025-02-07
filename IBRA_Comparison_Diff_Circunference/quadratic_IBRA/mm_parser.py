import scipy
import numpy as np

csr_matrix = scipy.io.mmread("A.mm")

cond_number = np.linalg.cond(csr_matrix.todense())

print("Condition number:", cond_number)
