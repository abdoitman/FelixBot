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

    match opt_type:
        case "ls":
            m_A, n_A = matricies['A'].shape
            if matricies['b'].size != m_A: raise Exception("""Check the dimensions of `A` and `b`!
**REMINDER**: If `A` is of size `m.n`, then `b` should be of size `m`""")

        case "linear":
            if "c" not in matricies.keys():
               raise Exception("""Missing attributes for the `linear` program
**Reminder**: Necessary matrix or vector is: `c`.""")
            
            #checks if c is a matrix
            try:
                m , n = matricies['c'].shape
                raise Exception("`c` must be a vector!")
            except:
                pass

            if "b" in matricies.keys() and "A" not in matricies.keys():
                raise Exception("Missing the matrix `A` to form: `Ax <= b`.\nMake sure Matricies are capitalized (like `A`) and vectors are small (like `b`)")
                
            if "A" in matricies.keys():
                if "b" not in matricies.keys():
                    raise Exception("Missing the vector `b` to form: `Ax <= b`.\nMake sure Matricies are capitalized (like `A`) and vectors are small (like `b`)")
                m_A, n_A = matricies['A'].shape
                if matricies['b'].size != m_A: raise Exception("""Check the dimensions of `A` and `b`!
**REMINDER**: If `A` is of size `m.n`, then `b` should be of size `m`""")

                if matricies['c'].size != n_A:
                    raise Exception("""Check the dimensions of `A`, `b` and `c` again!
**REMINDER**: If `A` is of size `m.n`, then `b` should be of size `m` & c should be of size `n`""")
            
            
        case "quadratic":
            #check if any matrix is missing
            if "P" not in matricies.keys() or "q" not in matricies.keys():
                raise Exception("""Missing attributes for the `quadratic` program
**Reminder**: Necessary matricies and vectors are: `P`, `q`.
If you want to add an **equality** constraint, add the matrix `A` and vector `b` to complete the form: `Ax = b`.
To add an **inequality** constriant, add the matrix `G` and the vector `h` to form: `Gx <= h`""")
            
            m_P, n_P = matricies["P"].shape

            #check if P is symmetric or not
            if not np.array_equiv(matricies['P'], matricies["P"].T) or m_P != n_P:
                raise Exception("Matrix `P` must be **symmetric** and at least **positive semi definite**.")

            #check if P is positive semi definite
            if np.any(np.linalg.eigvals(matricies['P']) < 0):
                raise Exception("Matrix `P` must be at least **positive semi-definite**!")
            
            if matricies['q'].size != m_P:
                raise Exception("""Check the dimensions of `P` and `q`!
**REMINDER**: If `P` is of size `m.m`, then `q` should also be of size `m`""")


            #check if b is specified and not A
            if "b" in matricies.keys() and "A" not in matricies.keys():
                raise Exception("Missing the matrix `A` to form: `Ax = b`.\nMake sure Matricies are capitalized (like `A`, `P` and, `G`) and vectors are small (like `b`, `q` and, `h`)")


            #If A is specified, b must also be given
            if "A" in matricies.keys():
                if "b" not in matricies.keys(): raise Exception("Missing the vector `b` to form: `Ax = b`.\nMake sure Matricies are capitalized (like `A`, `P` and, `G`) and vectors are small (like `b`, `q` and, `h`)")
                m_A, n_A = matricies['A'].shape
                if matricies['b'].size != m_A: raise Exception("""Check the dimensions of `A` and `b`!
**REMINDER**: If `A` is of size `m.n`, then `b` should be of size `m`""")
                
            
            #check if h is specified and not G
            if "h" in matricies.keys() and "G" not in matricies.keys():
                raise Exception("Missing the matrix `G` to form: `Ax = b`.\nMake sure Matricies are capitalized (like `A`, `P` and, `G`) and vectors are small (like `b`, `q` and, `h`)")


            #If G is specified, h must also be given
            if "G" in matricies.keys():
                if "h" not in matricies.keys(): raise Exception("Missing the vector `h` to form: `Gx <= h`.\nMake sure Matricies are capitalized (like `A`, `P` and, `G`) and vectors are small (like `b`, `q` and, `h`)")
                m_G, n_G = matricies['G'].shape
                if matricies['h'].size != m_G:
                    raise Exception("""Check the dimensions of `G` and `h`!
**REMINDER**: If `G` is of size `m.n`, then `h` should be of size `m`""")
                
                if n_G != n_A:
                    raise Exception("Size of `G` does not match the size of `A`!\n**REMINDER**: They should have the same number of columns.")
                
        case unkown_case:
            raise Exception(f"Type `{unkown_case}` is not recognized.")
        