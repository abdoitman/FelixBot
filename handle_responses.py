import handle_expr
from imagine import imagine
import optimize
import check
import re

def __show_latex(message, is_equation_only= False):
    try:
        filename = handle_expr.generate_latex_png(message, is_equation_only)
        response = "This is your equation bellow:"
        return response , filename
    except Exception as e:
        raise(e)
    
def __show_guide():
    guide1 = """Hey everyone! I'm here to assist you with understanding optimization problems.
Here are the available commands right now
[Remember: all my commands start with `f::`]:
```f::show var x y # equation```This is used to display **written equation in a better way**.
    - `f::show` to specify the command.
    - State the variables in the equations using `var:`.
    - Separate with `#`, then write your equation.
    `ex` f::show var x z # sin(x)+cos(z)
    `ex` f::show var x_1 x_2 f # log(x_1) / sqrt(x_2 \* sin(2 \* pi * f))
```f::imagine```This is used to display **vector**, **a set of vectors**, or **an equation with/without constraints**.
    You have **multiple options** to draw as follows:

    - `f::imagine vector` displays a **single vector**.
    `ex` f::imagine vector [5, 9, 7]

    - `f::imagine vectors` displays **a set of vectors** with `#` to separate vectors apart.
    `ex` f::imagine vectors [1, -4, 3] # [2, 6, 9] # [1, 7, -6]

    - Use `f::imagine equation ... var ... with constraints ... , ...` to display **an equation with (or without) some constraints**.
    `ex` f::imagine equation 3 \* x \* sin(z) var x z with constraints x >= 0, x + z < 1

    **IMPORTANT NOTES**:
        - Currently this command takes a minute to send the results.
        - Use `var` keyword to specify the variables in the equation.
        - If you want to draw an equation with no constraints, use the keyword `none`.
            `ex` f::imagine equation 3 \* x_1\*\*2 var x_1 with constraints none."""

    guide2= """```f::optimize```This is used to **solve some optimization problems.**
    To specify the type of equation you want to solve, use one of the following commands:

    - `f::optimize func ... var ... with constraints ...` solves **general optimization problems**
    `ex` f::optimize func 3 \* x_1 - 5 \* x_2 var x_1 x_2 with constraints x_1 >= 0, x_2 <= 5
    **For better understanding**: This function also graphs the equation *automatically*, to disable this feature type `!func` instead of `func`.

    - `f::optimize linear A = [...] # b= [...] # c= [...]` solves **LP optimization problems**
    `ex` f::optimize linear A = [[1, 2], [2, 0]] # b= [1, 1] # c= [3, -2]
    **For better understanding**: This function also graphs the equation *automatically*, to disable this feature type `!linear` instead of `linear`.
    **REMINDER**: LP problems take the following form:  `minimize c.T*X subject to A*X <= b`
        
    - `f::optimize ls A = [...] # b = [...]` solves **least squares problems**
    `ex` f::optimize ls A = [3, -4] # b = [0]
    **REMINDER**: Least squares problems is where you have measurement matrix `A` and a seek vector `x` and `Ax` is close to `b`.
                This closeness is defined as the sum of the squared differences, or the **second norm** of `Ax - b`.
                The objective in this problem is to minimize the seek vector `x` to get the smallest squared difference.
```f::check```This is used to **check on some properties.** The available tests right now are:

    - `f::check dt [ [...] , [...] ]` which checks the **definite type** of a matrix and returns its **eigenvalues**.
    **NOTE**: The matrix has to be **square** and **symmetric**.
    `ex` f::check dt [ [2, 1] , [1, 2] ]

Type `f::help` anytime to show this message again."""
    return guide1, guide2

async def process(message, client):
    contains_media = False
    command = message.split()[0]
    message = message.replace(command, "").strip()

    if command == 'show':
        response, filename = __show_latex(message, is_equation_only=True)
        contains_media = True
        return response , contains_media , filename
    
    if command == 'imagine':
        response, filename = await imagine.see_through(message, client)
        contains_media = True
        return response, contains_media, filename
    
    if command == 'optimize':
        response, drawing_command = optimize.solve(message)
        if drawing_command != "":
            _ , filename = imagine.see_through(drawing_command)
            contains_media = True
        else:
            filename = ""
            contains_media = False
        return response, contains_media, filename
    
    if command == 'check':
        response = check.inspect(message)
        return response, contains_media, ""

    if command == 'help':
        response1, response2 = __show_guide()
        return response1 , contains_media , response2
    
    if message != "" and command + " " + message.split()[0] == "solve sheet":
        response = "https://tenor.com/bhDEJ.gif"
        return response, contains_media, ""

    raise TypeError(f"`{command}` is not yet supported! - Check your command again, maybe it's a Typo.")