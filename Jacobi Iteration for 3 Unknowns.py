import math
import numpy as np
from numpy.linalg import *
import os

def jacobi(A, b, x_init, epsilon, max_iterations):
    D = np.diag(np.diag(A)) #Get The Diagonal Values
    print("This Shows The Matrix With Diagonal Values\n", D)
    
    LU = A - D #Get The Matrix Where Diagonal Values = 0
    print("\nThis Shows The Matrix Where Diagonal Values = 0\n", LU)
    print("\n")

    #Forming the inverse matrix of the Diagonal matrix which soon will be multiplied into the numerator
    D_inv = np.diag(1 / np.diag(D))
    
    print("n".center(10), "Old x1".center(15), "Old x2".center(15), "Old x3".center(15), "New x1".center(20), "New x2".center(20), "New x3".center(20), "Norm Of Matrix xNew-xOld".center(25))
    print("="*155)
    x = x_init #Initial values
 
    for i in range(max_iterations):
        ###https://stackoverflow.com/questions/43074634/checking-if-a-matrix-is-diagonally-dominant-in-python
        x_new = np.dot(D_inv, b - np.dot(LU, x))
        print(str(i+1).center(10),
              str(format(x[0], '.'+ str(dp) + 'f').center(15)), str(format(x[1], '.'+ str(dp) + 'f')).center(15), str(format(x[2], '.'+ str(dp) + 'f')).center(15),
               str(format(x_new[0], '.'+ str(dp) + 'f')).center(20),str(format(x_new[1], '.'+ str(dp) + 'f')).center(20),str(format(x_new[2], '.'+ str(dp) + 'f')).center(20),
               str(format(np.linalg.norm(x_new - x)).center(25)))

        ##Stop if reached TOL
        ##Norm is Frobenius norm of matrix which contains new value of x1, x2, x3,.... xn compared to the previous value of x1, x2, x3, .....xn, (xNew - xOld)^2 for each value
        if np.linalg.norm(x_new - x) < epsilon:
            print("\nThe Jacobi Method Succeeded After " + str(i+1) + " Iterations")
            return x_new
        #else continue to iteration
        x = x_new
    if (i+1 == max_iterations)and np.linalg.norm(x_new - x) > epsilon:
        print("\nThe Jacobi Method Has Failed After " + str(max_iterations) + " Iterations")
    return x

#problem data and validation
converge = False
cont = 'N'
diagonal_zero = False

while converge == False:
    A = eval(input("Enter your square matrix (n x n) in 2D array form, eg [[1,2,3],[2,3,1],[1,2,3]]: "))
    A = np.array(A)

    num_rows, num_cols = A.shape #Dimension

    #first column
    k = 0

    ##Check diagonals for 0
    for i in range (num_rows):
        if (A[i][k] == 0):
            print("\nWARNING! 0 Is Detected In Diagonal Of The Position Of Row Number", i+1, "and Column Number", k+1, "Please Enter A New Matrix\n")
            diagonal_zero = True
            break
        else:
            k = k + 1
            diagonal_zero = False
            
    if diagonal_zero == False:
        D = np.diag(np.abs(A)) # Find diagonal coefficients
        S = np.sum(np.abs(A), axis=1) - D # Find row sum without diagonal
        if np.all(D > S):
            print ('Matrix is diagonally dominant')
        else:
            print ('Matrix is NOT diagonally dominant')
        
        D = np.diag(np.diag(A))
        D_inv = np.diag(1 / np.diag(D))
        LU = A - D
        norm = np.linalg.norm(np.dot(D_inv,LU))
        if norm >= 1:
            print("WARNING! This Iteration MAY NOT Converge, The Frobenius Norm of ||D^-1 times M|| Is " + str(norm) + " " + u"\u2265 1\n")
            cont = input("Do you want to proceed with the iteration? Y for Yes, N for No and Enter New 2D Array: " )
            print("")
            cont = cont.upper()
            if cont == 'Y':
                converge = True
        
        else:
            print("This Iteration Will Converge, The Frobenius Norm of ||D^-1 times M|| Is ", norm,  " < 1\n")
            converge = True
    
b = eval(input("Enter your value of b in 1D array form, eg [1,2,3]: "))
b = np.array(b)

# you can choose any starting vector
# array of 0 for initial guess
x_init = eval(input("Enter your initial guess in 1D array form, eg [2,4,6]: "))
x_init = np.array(x_init)

# get TOL
epsilon = eval(input("Enter TOL: "))
dp = str(epsilon)[::-1].find('.')

##fomat how many deimal places
dp = dp + 1
np.set_printoptions(precision=dp)

# get maximum iteration
max_iterations = eval(input("Enter Number Of Maximum Iterations: "))


#call jacobi method
x = jacobi(A, b, x_init, epsilon, max_iterations)

print('\nx:', x)
print('Computed b by substituting the computed x value:', np.dot(A, x))
print('Real b values:', b)
print('Actual Solution from built-in functions = %s' % solve(A, b))
os.system("pause")

#example problem data 1 (The one in Presentation Slide)

##A = np.array([
##    [10, 2, -1],
##    [1, 8, 3],
##    [-2, -1, 10],
##])
##[[10,2,-1],[1,8,3],[-2,-1,10]]

##b = np.array([7,-4,9])

# you can choose any starting vector
#array of 0 for initial guess
##x_init = np.zeros(len(b))
##x = jacobi(A, b, x_init)




#example problem data 2
##A = [[4,2,1],[1,5,-1],[1,1,8]]
##b = [14,10,20]
##x_init = [0,0,0]

#Example Of Issue Of Matrix
#Diagonal Issues
#[[4,2,1],[1,5,-1],[1,1,0]]

##Converging But Not Stricly Diagonally Dominant
#A = [[9,2,1],[1,8,2],[1,3,2]], b = [30,20,10]

##Explaination Of Formula

#Assuming Row 1 Is As Below, Where x1 Is To Be Made subject
##5x1 - 1x2 + 2x3 = 12
##5x1 = 12 - (0x1 - 1x2 + 2x3) where 0 is the digonal coefficient of matrix of Row 1
        
##np.dot(LU,x) is forming the numerator (eg: ax2 - bx3 where a and b is a constant,
##which will be multiplied by the initial value and the new x value) hence multiplication of 2 matrix
##In this case, a = -1 and b = 2 and x2 and x3 are initial value guessed
        
##b - np.dot(LU,x) is taking the answer (which is in matrix b) to minus off
##In this case the answer in matrix B is 12, 12 - (- x2 + 2x3) = 12 + x2 + 2x3
#Numerator Formation Completed

#This Line Below Is To Bring The Constant of x1 to the other side, 1/a, in this case: 1/5 and then multiply with the numerator
#This computes the new values of x1
#x_new = np.dot(D_inv, b - np.dot(LU, x))

#numpy.dot(vector_a, vector_b, out = None) returns the dot product of vectors a and b.
#It can handle 2D arrays but considering them as matrix and will perform matrix multiplication. 

    

