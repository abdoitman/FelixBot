import numpy as np

def __check_definite_type(message):
    '''
    This function simply checks for the definite type of a matrix\n
    positive definite/semi-definite - negative definite/semi-definite - indefinite\n
    
    :param message: the string matrix which we want to check its type
    '''
    try:
        input_matrix = np.array(eval(message))
    except:
        raise Exception("Can't resolve matrix from the input. Make sure the input is in the form `[ [...] , [...] , ... ]`")
    
    m, n = input_matrix.shape
    if m != n : raise Exception("To check the definite type, matrix has to be square!")
    if not np.array_equiv(input_matrix, input_matrix.T): raise Exception("Input matrix is not symmetric.")

    eigenvalues = list(np.linalg.eigvals(input_matrix))
    eigenvalues = [round(eigenvalue, 3) for eigenvalue in eigenvalues]

    if np.all(np.linalg.eigvals(input_matrix == 0)):
        return f"Matrix has all zeros eiganvalues. Nilponent Martix."
    
    elif np.all(np.linalg.eigvals(input_matrix) > 0):
        return f"Matrix is Positive definite.\nEigenvalues are {eigenvalues}"
    
    elif np.all(np.linalg.eigvals(input_matrix) >= 0): # the 2nd condition to avoid the case of all-zero-eigenvalues matrix
        return f"Matrix is Positive semi-definite.\nEigenvalues are {eigenvalues}"
    
    elif np.all(np.linalg.eigvals(input_matrix) < 0):
        return f"Matrix is Negative definite.\nEigenvalues are {eigenvalues}"
    
    elif np.all(np.linalg.eigvals(input_matrix) <= 0): # the 2nd condition to avoid the case of all-zero-eigenvalues matrix
        return f"Matrix is Negative semi-definite.\nEigenvalues are {eigenvalues}" 
    
    else:
        return f"Matrix is Indefinite.\nEigenvalues are {eigenvalues}"

def inspect(message):
    inspect_what = message.split()[0]
    message = message.replace(inspect_what, "").strip()
    match inspect_what.upper():
        case "DT":
            response = __check_definite_type(message)
            return response
        
        case unkown_type:
            return f"`{unkown_type}` is not yet supported."
