import re
import numpy as np
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

        validate_str_vectors(input_msg.strip())
        self.__str_vectors_list = input_msg.split("#")

        self.__vectors = []
        self.__max_coordinate = self.__min_coordinate = 0

        for vec in self.__str_vectors_list:

            try:
                temp_vec = eval(vec.strip())
            except:
                raise Exception("Something's wrong! Perhaps missing a `comma` or `]`?")
            
            self.__vectors.append(temp_vec)
            if(max(temp_vec) >= self.__max_coordinate ): self.__max_coordinate = max(temp_vec)
            if(min(temp_vec) <= self.__min_coordinate ): self.__min_coordinate = min(temp_vec)

        validate_evaluated_vectors(self.__vectors, self.__max_coordinate, self.__min_coordinate)
        
    def get_vectors(self):
        return self.__vectors
    
    def get_max_coordinate(self):
        return self.__max_coordinate
    
    def get_min_coordinate(self):
        return self.__min_coordinate
    

class OptimizationMatriciesParser:
    def __init__(self, input_str_matricies: str, opt_type: str) -> None:
        validate_str_matricies(input_str_matricies)

        self.__matricies = {}

        for mat in input_str_matricies.split("#"):
            if mat.split("=")[0].strip() == "constraints":
                mat = mat.replace(" ", "")
                self.__constraints: list = mat[13:-1].split(",")

            else:
                name, value = mat.split("=")
                try:
                    self.__matricies[name.strip()] = np.array(eval(value.strip()))
                except:
                    raise Exception("Something's wrong in one of the matricies!\nPerhaps missing a `comma` or `]`?")
                        

        validate_evaluated_matricies_dimensions(self.__matricies, opt_type)
    
    def get_matricies(self):
        return self.__matricies
    
    def get_constraints(self):
        try:
            return self.__constraints
        except:
            return False

if __name__ == "__main__":
    e1 = OptimizationMatriciesParser("P = [[5, 1], [1,5]] # q = [2, 3] # a= [5, 1] # constraints = [sum(x) >= 1]", "quadratic")
    print(e1.get_matricies(), e1.get_constraints())