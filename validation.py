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
   
    return True

def validate_vector(vectors: str):
    
    #1 - check for missing '#'
    if "][" in vectors.replace(" ",""):
        raise Exception("Missing `#`")

    #2 check for missing '['
    if error := re.findall(r"\]\d", vectors.replace(" ","")):
        raise Exception(f"Fix `{str(*error)}` !\nPerhaps missing a `[`")
