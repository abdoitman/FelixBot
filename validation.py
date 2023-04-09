import re

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
