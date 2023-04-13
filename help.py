def show_general_guide():
    guide = """Hello :wave:!
Here's a general view of the available commands right now:
```f::show ... var ...```This is used to display **written equation in a better way**.
```f::imagine```This is used to display **vector**, **a set of vectors**, or **an equation**.
You have **multiple options** to draw as follows:

(1) `f::imagine vector` : displays a **single vector**.
(2) `f::imagine vectors` : displays **a set of vectors** with `#` to separate vectors apart.
(3) `f::imagine equation ... var ... with constraints ... , ...` : displays **an equation with some constraints**.

- If you want to plot an equation with no constraints, **don't add any**.
    `ex` f::imagine equation 3 \* x_1\*\*2 var x_1
```f::optimize```This is used to **solve some optimization problems**.
Define the problem using the following commands:

(1) `f::optimize func ... var ... with constraints ...` solves **general optimization problems**
(2) `f::optimize linear A = [...] # b = [...] # c = [...]` solves **LP optimization problems**
LP problems take the following form:
    `minimize` c.T * x
    `subject to` A * x <= b
(3) `f::optimize quadratic P = [...] # q = [...] # ...` solves **quadratic optimization problems**
QP problems take the following form:
    `minimize` (1/2) x.T * P * x + q.T x
    `subject to` A * x = b , G * x <= h

**NOTE**: For LP and QP problems, you can enter the parameters specified in the standard form or specify a *custom constraint* using `constraints = [...]`
    `ex` f::optimize linear c= [3, -2] # constraints = [sum(x) == 1, x >= 0]

(4) `f::optimize ls A = [...] # b = [...]` solves **least squares problems**
```f::check```This is used to **check on some properties** The available tests right now are:

(1) `f::check dt [ [...] , [...] ]` which checks the **definite type** of a matrix and returns its **eigenvalues**.

Type `f::help` anytime to show this message again.
For more **detailed** guide about any command: type `f::help command_name`"""
    return guide

def show_specific_guide(command):
    show_guide = """```f::show ... var ...```This is used to display **written equation in a better way**.
    - `f::show` to specify the command.
    - State the variables in the equations using the keyword `var`.
    `ex` f::show sin(x)+cos(z) var x z
    `ex` f::show log(x_1) / sqrt(x_2 \* sin(2 \* pi * f)) var x_1 x_2 f"""

    imagine_guide = """```f::imagine```This is used to display **vector**, **a set of vectors**, or **an equation with/without constraints**.
You have **multiple options** to draw as follows:

**(1)** `f::imagine vector` displays a **single vector**.
    `ex` f::imagine vector [5, 9, 7]

**(2)** `f::imagine vectors` displays **a set of vectors** with `#` to separate vectors apart.
    `ex` f::imagine vectors [1, -4, 3] # [2, 6, 9] # [1, 7, -6]

**(3)** `f::imagine equation ... var ... with constraints ... , ...` displays **an equation with (or without) some constraints**.
    `ex` f::imagine equation 3 \* x \* sin(z) var x z with constraints x >= 0, x + z < 1
    `ex` f::imagine equation x\*\*2 + y\*\*2 var x y

**IMPORTANT NOTES**:
    - Currently this command takes about *50 seconds* to send the results.
    - To get a better view; when drawing anything in 3D, this function returns a **10 seconds video of the surface rotating in space**.
    - Use `var` keyword to specify the variables in the equation.
    - If you want to draw an equation with no constraints, **don't add any**.
        `ex` f::imagine equation 3 \* x_1\*\*2 var x_1"""
    
    optimize_guide = """```f::optimize```This is used to **solve some optimization problems.**
To specify the type of equation you want to solve, use one of the following commands:

**(1)** `f::optimize func ... var ... with constraints ...` solves **general optimization problems**
    `ex` f::optimize func 3 \* x_1 - 5 \* x_2 var x_1 x_2 with constraints x_1 >= 0, x_2 <= 5
    **For better understanding**: If possible, you can plot the objective function using `!func` instead of `func`.

**(2)** `f::optimize linear A = [...] # b = [...] # c = [...]` solves **LP optimization problems**
    **REMINDER**: LP problems take the following form:
        `minimize` c.T * x
        `subject to` A * x <= b
    `ex` f::optimize linear c= [3, -2] # A = [[1, 2], [2, 0]] # b= [1, 1] 
    
**(3)** `f::optimize quadratic P = [...] # q = [...] # ...` solves **quadratic optimization problems**
    **REMINDER**: Standard QP problems take the following form:
        `minimize` (1/2) x.T * P * x + q.T x
        `subject to` A * x = b , G * x <= h
    `ex` f::optimize quadratic P = [[1, 0], [0, 1]] # q = [2, 1] # A= [[1, 3], [0, 6]] # b = [0, 0] # G = [[4, -3] , [3, 0]] # h = [0, 0]
    
**NEW**: For LP and QP problems, you can now add **custom constraints** to your problem not just the standard form!
When specifying the matricies and vectors of the problem, you can define any matrix or vector you need and define the constraints in `constraints = [...]`

**IMPORTANT NOTE** if you want to define custom vectors or matricies: Matricies `A`, `P`, `G` and vectors `b`, `c`, `h`, `q` are *reserved*. So, to aviod any errors, **name your matricies/vectors any thing else**.
    `ex` f::optimize linear c= [3, -2, 5, 0] # constraints = [sum(x) == 3]
    `ex` f::optimize quadratic P = [[1, 2], [2, 1]] # q = [0, 0] # constraints = [sum(x) == 1, x >= 0]

**(4)** `f::optimize ls A = [...] # b = [...]` solves **least squares problems**
    `ex` f::optimize ls A = [3, -4] # b = [0]"""

    check_guide = """```f::check```This is used to **check on some properties** The available tests right now are:

`f::check dt [ [...] , [...] ]` which checks the **definite type** of a matrix and returns its **eigenvalues**.
**NOTE**: The matrix has to be **square** and **symmetric**.
    `ex` f::check dt [ [2, 1] , [1, 2] ]"""

    match command:
        case "show":
            return show_guide
        case "imagine":
            return imagine_guide
        case "optimize":
            return optimize_guide
        case "check":
            return check_guide
        case unrecognized_case:
            return f"Can't recognize `{unrecognized_case}`!"