import re
import numpy as np

## Validating Equations ##
def validate_equation(equation: str, variables: list):
    
    #1 - check if 2 variables follow eachother without an opertation
    error = " ".join(variables)
    if len(variables) > 1 and error.replace(" ", "") in equation.replace(" ", ""):
        raise Exception(
            f"Fix `{error}` !\n**NOTE**: To multiply 2 variables use * in between.")
    
    #2 - check if any digit have a letter afterwards
    if error := re.findall(r"(\d[A-Za-z])", equation.replace(" ", "")):
        raise Exception(
            f"Something's wrong. Fix `{str(*error)}`!\n**NOTE**: To multiply 2 expression use \* in between.")


## Validating Vectors ##
def validate_str_vectors(vectors: str):
    
    #1 - check for missing '#'
    if "][" in vectors.replace(" ",""):
        raise Exception("Missing `#`")

    #2 check for missing '['
    if error := re.findall(r"\]\d", vectors.replace(" ","")):
        raise Exception(f"Fix `{str(*error)}` !\nPerhaps missing a `[`")


def validate_evaluated_vectors(vectors: list, max_coordinate: int, min_coordinate: int):

    #1 check for the length of all vectors
    length_vectors = [len(vec) for vec in vectors]
    if(len(set(length_vectors)) != 1):
        raise Exception("Make sure all vectors are of the same dimension!")

    #2 check for the max & min coordinates in the vectors
    if max_coordinate > 60 or min_coordinate < -60:
        raise Exception("Your vector is too epic.\nTry a vector with coordinates **less than 60**!")


## Validating matricies ##
def validate_str_matricies(str_matricies: str):

    #1 check if a # is missing
    if error := re.findall(r"\][A-Za-z]", str_matricies.replace(" ","")):
        raise Exception(f"Fix `{str(*error)}` !\nPerhaps missing a `#`")
    

def validate_evaluated_matricies_dimensions(matricies: dict, opt_type):

    m_A, n_A = matricies['A'].shape
    if matricies['b'].size != m_A: raise Exception("Size of `b` does not match the size of `A`!")

    match opt_type:
        case "linear":
            try:
                if matricies['c'].size != n_A:
                    raise Exception("Size of `c` does not match the size of `A`!")
            except:
                raise Exception("Missing attribute: `c`")
            
        case "quadratic":
            #check if any matrix is missing
            if not all(var in ['P', 'q', 'G', 'h'] for var in matricies.keys()):
                raise Exception("Missing attributes for the quadratic program\n**Reminder**: Expected matricies and vectors are: `P`, `q`, `G`, `h`, `A` and, `b`")
            
            m_P, n_P = matricies["P"].shape
            m_G, n_G = matricies['G'].shape

            #check if P is symmetric or not
            if not np.array_equiv(matricies['P'], matricies["P"].T) or m_P != n_P:
                raise Exception("Matrix P must be **symmetric** and at least **positive semi definite**.")

            #check if P is positive semi definite
            if np.any(np.linalg.eigvals(matricies['P']) < 0):
                raise Exception("Matrix `P` must be at least **positive semi-definite**!")
            
            if matricies['q'].size != m_P:
                raise Exception("Size of `q` does not match the size of `P`!")
            
            if m_G != matricies['h'].size:
                raise Exception("Size of `h` does not match the size of `G`!")
            
            if n_G != n_A:
                raise Exception("Size of `G` does not match the size of `A`!\nThe should have the same number of columns.")
            
        case unkown_case:
            raise Exception(f"Type `{unkown_case}` is not recognized.")
        
    def get_matrix(self, symbol):
        return self.__matricies[symbol]