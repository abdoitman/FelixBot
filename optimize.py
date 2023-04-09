import numpy as np
import cvxpy as cp
import InputCommands

__operations = {"log":"cp.log",
                "abs":"cp.abs",
                "exp":"cp.exp"}

def __change_operation_to_cp(eq):
    global __operations
    equation = eq
    for operator, np_operator in __operations.items():
        equation = equation.replace(operator, np_operator)

    return equation

def __optimize_general_functions(message:str):
    opt_problem = InputCommands.InputParser(message)
    equation, variables, constraints = opt_problem.get_equation(), opt_problem.get_variables(), opt_problem.get_constraints()

    drawing_command = "equation " + message

    for var in variables:
        globals()[f"{var}"] = cp.Variable()

    try:
        constraints = [eval(__change_operation_to_cp(cons)) for cons in constraints]
    except Exception as e:
        print(e)
        raise Exception("Please use `<=` and `>=` instead of `<` and `>`.")
    
    try:
        equation = __change_operation_to_cp(equation)
        obj = cp.Minimize(eval(equation))
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
    opt_problem = InputCommands.OptimizationMatriciesParser(message, "linear")
    A = opt_problem.get_matrix("A")
    b = opt_problem.get_matrix("b")
    c = opt_problem.get_matrix("c")

    m , n = A.shape

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
    opt_problem = InputCommands.OptimizationMatriciesParser(message, "ls")
    A = opt_problem.get_matrix("A")
    b = opt_problem.get_matrix("b")

    m , n = A.shape

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
    opt_problem = InputCommands.OptimizationMatriciesParser(message, "quadratic")
    A = opt_problem.get_matrix("A")
    b = opt_problem.get_matrix("b")
    G = opt_problem.get_matrix("G")
    h = opt_problem.get_matrix("h")
    P = opt_problem.get_matrix("P")
    q = opt_problem.get_matrix("q")

    m_A , n_A = A.shape

    x = cp.Variable(n_A)
    prob = cp.Problem(cp.Minimize((1/2)*cp.quad_form(x, P) + q.T @ x),
                 [G @ x <= h,
                  A @ x == b])
    prob.solve()

    response = f"""The optimal value is {prob.value}
A solution x is {x.value}
A dual solution corresponding to the inequality constraints is {prob.constraints[0].dual_value}"""
    
    return response

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
        
        case "quadratic":
            response = __optimize_quadratic(message[9:])
            return response, ""
        
        case opt_type:
            raise Exception(f"Can't recognize `{opt_type}`. Check again for typos!")