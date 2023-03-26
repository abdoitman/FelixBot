# message -> f::imagine equation 3*x * sin(z) var x z with constraints x >= 0, x + z < 1
# filtered message -> 3*x * sin(z) var x z with constraints x >= 0, x + z < 1

# message -> f::imagine equation 3*x var x with constraints x >= 0
# filtered message -> 3*x * sin(z) var x z with constraints x >= 0, x + z < 1

import re
from time import gmtime, strftime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D

from .animate import animate_surface

__operations = {"sin": "np.sin",
                "cos": "np.cos",
                "tan": "np.sin",
                "pi": "np.pi",
                "log": "np.log10",
                "ln": "np.log2",
                "abs": "np.abs",
                "exp": "np.exp",
                "sqrt": "np.sqrt"}

__signs = {"<=": ">",
           ">=": "<",
           "<": ">=",
           ">": "<=",
           "==": "!=",
           "!=": "=="}


def __change_operation_to_np(eq):
    global __operations
    equation = eq
    for operator, np_operator in __operations.items():
        equation = equation.replace(operator, np_operator)

    return equation


def __modify_constraints(constraints):
    global __signs
    modified_constraints = []
    for cons in constraints:
        cons = __change_operation_to_np(cons)
        for sign, flipped_sign in __signs.items():
            if sign in cons:
                cons = cons.replace(sign, flipped_sign)
                break

        modified_constraints.append(cons)

    return modified_constraints


def __get_exprs(message):
    try:
        eq = re.findall(r".+?(?=var)", message)[0].strip()
        variables = re.findall(r"(?<=var).*(?=w)", message)[0].strip()
        constraints = re.findall(r"(?<=ts).*", message)[0].strip().split(',')
    except:
        raise Exception("Missing attributes!")

    return variables, eq, constraints


def __imagine_2d(variables, eq, constraints):
    fixed_equation = eq.replace("**", "^")
    fixed_constraints = constraints
    var = variables.split()[0]
    if var != "X":
        eq = eq.replace(var, "X")
        if constraints[0] != 'none':
            constraints = [cons.replace(var, "X") for cons in constraints]

    eq = __change_operation_to_np(eq)
    if constraints[0] != 'none':
        modified_constraints = __modify_constraints(constraints)

    def z_func(eq, a):
        X = a
        result = eval(eq)
        return result

    X = np.arange(-20, 20, 0.05)
    Z = z_func(eq, X)
    if constraints[0] != 'none':
        for cons in modified_constraints:
            Z[eval(cons)] = np.nan

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(X, Z, color="#0E3C45")

    if constraints[0] != 'none':
        str_constraints = ",".join(
            ['$' + cons + '$' for cons in fixed_constraints])
        ax.set_title(f"Drawing $f({var})$ = $ {fixed_equation}$ subject to {str_constraints}",
                  fontdict={'fontsize': 18})
    else:
        ax.set_title(f"Drawing $f({var})$ = $ {fixed_equation}$",
                  fontdict={'fontsize': 18})
        
    ax.set_xlabel(f"${var}$",
                  fontdict={'fontsize': 12})
    ax.set_ylabel(f"$f({var})$",
                  fontdict={'fontsize': 12})
    ax.grid(alpha=0.2)
    fig.savefig(filename := "./__output/2Deq_" +
                strftime("%d%b%Y%H%M%S", gmtime()) + ".png")
    return filename


def __imagine_3d(variables, eq, constraints, angle=240, is_frame=False):
    fixed_equation = eq.replace("**", "^")
    fixed_constraints = [cons.replace("**", "^") for cons in constraints]

    if variables.split() != ["X", "Y"]:
        for var, new_var in zip(variables.split(), ["X", "Y"]):
            eq = eq.replace(var, new_var)
            if constraints[0] != 'none':
                constraints = [cons.replace(var, new_var)
                               for cons in constraints]

    eq = __change_operation_to_np(eq)
    if constraints[0] != 'none':
        modified_constrains = __modify_constraints(constraints)

    def z_func(eq, a, b):
        X, Y = a, b
        result = eval(eq)
        return result

    x = np.arange(-30, 30, 0.05)
    y = np.arange(-30, 30, 0.05)
    X, Y = np.meshgrid(x, y)
    Z = z_func(eq, X, Y)
    if constraints[0] != 'none':
        for cons in modified_constrains:
            Z[eval(cons)] = np.nan

    fig = plt.figure(figsize=(14.4, 14.4))
    ax = fig.add_subplot(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=1,
                           antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.view_init(elev=35, azim=angle, roll=0)

    if constraints[0] != 'none':
        str_constraints = ", ".join(
            ['$' + cons + '$' for cons in fixed_constraints])
        plt.title(f"Drawing $f({variables.split()[0]}, {variables.split()[1]})$ = ${fixed_equation}$ subject to {str_constraints}",
                  fontdict={'fontsize': 18})
    else:
        plt.title(f"Drawing $f({variables.split()[0]}, {variables.split()[1]})$ = ${fixed_equation}$",
                  fontdict={'fontsize': 18})
        
    ax.set_xlabel(f"${variables.split()[0]}$",
                  fontdict={'fontsize': 12})
    ax.set_ylabel(f"${variables.split()[1]}$",
                  fontdict={'fontsize': 12})
    ax.set_zlabel(
        f"$f({variables.split()[0]}, {variables.split()[1]})$", rotation=0)

    if is_frame:
        fig.savefig(f"./__frames/frame_{angle}.png")
        plt.close()
    else:
        fig.savefig(filename := "./__output/3Deq_" +
                    strftime("%d%b%Y%H%M%S", gmtime()) + ".png")
        plt.close()
        return filename


def draw_space(message):
    variables, eq, constraints = __get_exprs(message)

    # Error handling
    # If any digit followed by a string was found
    if error := re.findall(r"(\d[A-Za-z])", eq.replace(" ", "")):
        raise Exception(
            f"Something's wrong. Fix `{str(*error)}`!\n**NOTE**: To multiply 2 expression use \* in between.")

    if len(variables.split()) == 1:
        filename = __imagine_2d(variables, eq, constraints)

    elif len(variables.split()) == 2:
        # Error handling
        # If any 2 variables came after each other
        if variables.replace(" ", "") in eq.replace(" ", ""):
            raise Exception(
                f"Something's worng. Fix `{variables.strip()}`!\n**NOTE**: To multiply 2 expression use \* in between.")

        filename = animate_surface(variables, eq, constraints, __imagine_3d)
    else:
        raise Exception("Can't draw more than 3 dimensions!")

    return filename