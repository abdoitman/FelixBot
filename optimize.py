import numpy as np
import cvxpy as cp
import re

__operations = {"log":"cp.log",
                "abs":"cp.abs",
                "exp":"cp.exp"}

def __change_operation_to_cp(eq):
    global __operations
    equation = eq
    for operator, np_operator in __operations.items():
        equation = equation.replace(operator, np_operator)

    return equation

def __get_exprs(message):
    try:
        eq = re.findall(r".+?(?=var)", message)[0].strip()
        variables = re.findall(r"(?<=var).*(?=w)", message)[0].strip().split()
        constraints = re.findall(r"(?<=ts).*", message)[0].strip().split(',')
    except:
        raise Exception("Missing attributes!")

    return variables, eq, constraints

def __get_attributes(message):
    message = message.replace(" ","")
    if "c" in message:
        try:
            A = re.findall(r"(?<=A=).*?(?=#)", message)[0].strip()
            b = re.findall(r"(?<=b=).*(?=#)", message)[0].strip()
            c = re.findall(r"(?<=#c=).*", message)[0].strip()
        except:
            raise Exception("Missing attributes!")
        
    else:
        try:
            A = re.findall(r"(?<=A=).*(?=#)", message)[0].strip()
            b = re.findall(r"(?<=b=).*", message)[0].strip()
        except:
            raise Exception("Missing attributes!")

    return A, b, c

def __optimize_general_functions(message:str):
    variables, eq, constraints = __get_exprs(message)
    fixed_eq, fixed_var, fixed_constraints = eq, " ".join(variables), ",".join(constraints)
    drawing_command = f"equation {fixed_eq} var {fixed_var} with constraints {fixed_constraints}"

    for var in variables:
        globals()[f"{var}"] = cp.Variable()

    try:
        constraints = [eval(__change_operation_to_cp(cons)) for cons in constraints]
    except Exception as e:
        print(e)
        raise Exception("Please use `<=` and `>=` instead of `<` and `>`.")
    
    try:
        eq = __change_operation_to_cp(eq)
        obj = cp.Minimize(eval(eq))
    except Exception as e:
        print(e)
        raise Exception("Review your equation again as some functions are not convex and not supported in CVX such as: `sin`, `cos` and `tan`")
    
    prob = cp.Problem(obj, constraints)
    prob.solve()
    solution = f"""solution status: {prob.status}\noptimal value: {prob.value}"""

    optimal_values_text = ""
    for var in variables:
        cpvar = globals()[f"{var}"]
        optimal_values_text += "\noptimal value for {} is {:.3f}".format(var, cpvar.value)

    response = solution + optimal_values_text
    return response , drawing_command

def __optimize_linear_program(message:str):
    A, b, c = __get_attributes(message)

    try:
        A = np.array(eval(A))
        b = np.array(eval(b))
        c = np.array(eval(c))
    except:
        raise Exception("Error reading A & b")

    try:
        m, n = A.shape
    except:
        m = 1
        n = A.size

    if b.size != m or c.size != n:
        raise Exception("""Check the dimensions of A, b and c again!
**REMINDER**: If A is of size `m.n`, then b should be of size `m` & c should be of size `n`""")

    x = cp.Variable(n)
    prob = cp.Problem(cp.Minimize(c.T@x),
                    [A @ x <= b])
    prob.solve()

    response = f"""Problem solution is {prob.status}
The optimal value is {prob.value}
Optimal value of x is {x.value}"""

    try:
        if m == 1 and n == 1 and c[0] !=0:
            drawing_func = f"equation {c[0]} * x_1 var x_1 with constraints {A[0]} * x_1 <= {b[0]}"
        elif m == 1 and n == 2 and (c[0] != 0 or c[1] != 0):
            drawing_func = f"equation {c[0]} * x_1 + {c[1]} * x_2 var x_1 x_2 with constraints {A[0]} * x_1 + {A[1]} * x_2 <= {b[0]}"
        else:
            drawing_func = ""
    except:
        raise Exception("If A is a vector not a matrix, write it as `[...]` not `[[...]]`")
    
    return response, drawing_func

def __optimize_least_squares(message:str) -> str:
    A, b, _ = __get_attributes(message)

    try:
        A = np.array(eval(A))
        b = np.array(eval(b))
    except:
        raise Exception("Error reading A & b")

    m, n = A.shape

    if b.size != m: raise Exception("Check the dimensions of A and b again!")
    x = cp.Variable(n)
    ls_func = cp.sum_squares(A @ x - b)
    prob = cp.Problem(cp.Minimize(ls_func))
    prob.solve()
    norm_value = cp.norm(A @ x - b, p=2).value
    response = f"""Problem solution is {prob.status}
    The optimal value is {prob.value}
    Optimal value of x is {x.value}
    The norm of the residual is {norm_value}"""
    return response

def __optimize_quadratic(message:str) -> str:
    pass

def solve(message: str):
    plot = True
    if message.strip()[0] == "!":
        plot = False
        message = message[1:]
    optimize_prob = message.strip().split()[0]
    match optimize_prob:
        case "func":
            response , func = __optimize_general_functions(message[4:])
            if plot: return response, func
            else: return response, ""
        
        case "linear":
            response, func = __optimize_linear_program(message[6:])
            if plot: return response, func
            else: return response, ""
        
        case "ls":
            response = __optimize_least_squares(message[2:])
            return response, ""
        
        case "quad":
            response = __optimize_quadratic(message[4:])
            return response, ""
        
        case opt_type:
            raise Exception(f"Can't recognize `{opt_type}`. Check again for typos!")