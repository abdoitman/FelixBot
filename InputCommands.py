import re
from validation import *

class InputParser:

    def __init__(self, input_msg:str):
        self.__message = input_msg

        try:
            self.__equation :str = re.findall(r".+?(?=var)", self.__message)[0].strip()
        except:
            raise Exception("Missing attributes : `Equation`")

        if "with" not in self.__message: #equation has no constraints

            try:
                self.__variables :list = re.findall(r"(?<=var).*", self.__message)[0].strip().split()
            except:
                raise Exception("Missing Attribute: `variables`\n**NOTE**: Specify the variables i nthe equation after entering the equaition using `var` keyword.")
            
            self.__constraints = "none"

        else: #equation does have constraints
            try:
                self.__variables :list = re.findall(r"(?<=var).*(?=with)", self.__message)[0].strip().split()
            except:
                raise Exception("Missing Attribute: `variables`\n**NOTE**: Specify the variables in the equation after entering the equaition using `var` keyword.")
            
            self.__constraints :list = re.findall(r"(?<=ts).*", self.__message)[0].strip().split(',')
            if self.__constraints == ['']: raise Exception("Specify the constraints of the equation.")

        #Validate input
        validate_equation(self.__equation, self.__variables)
        for cons in self.__constraints:
            validate_equation(cons, self.__variables)

    def get_equation(self):
        return self.__equation
    
    def get_variables(self):
        return self.__variables
    
    def get_constraints(self):
        return self.__constraints


class VectorsParser:
    def __init__(self, input_msg) -> None:
        pass


class MatrixParser:
    def __init__(self, input_str_matrix) -> None:
        pass

if __name__ == "__main__":
    e1 = InputParser("sin(x_1 * y_2 ) var x_1 y_2 with consats x>1")
    print(e1.get_equation(), e1.get_variables(), e1.get_constraints())