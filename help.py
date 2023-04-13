def show_guide():
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
        - If you want to draw an equation with no constraints, **don't add any**.
            `ex` f::imagine equation 3 \* x_1\*\*2 var x_1"""

    guide2= """```f::optimize```This is used to **solve some optimization problems.**
    To specify the type of equation you want to solve, use one of the following commands:

    - `f::optimize func ... var ... with constraints ...` solves **general optimization problems**
    `ex` f::optimize func 3 \* x_1 - 5 \* x_2 var x_1 x_2 with constraints x_1 >= 0, x_2 <= 5
    **For better understanding**: You can plot the function - if possible -, `!func` instead of `func`.

    - `f::optimize linear A = [...] # b = [...] # c = [...]` solves **LP optimization problems**
    `ex` f::optimize linear A = [[1, 2], [2, 0]] # b= [1, 1] # c= [3, -2]
    **For better understanding**: You can plot the function - if possible -, type `!linear` instead of `linear`.
    **REMINDER**: LP problems take the following form:  `minimize c.T*X subject to A*X <= b`
        
    - `f::optimize quadratic P = [...] # q = [...] # ...` solves **quadratic optimization problems**
    `ex` f::optimize quadratic P = [[1, 2], [2, 1]] # b= [0, 0] # constraints = [sum(x) == 1]
    **For better understanding**: You can plot the function - if possible -, type `!linear` instead of `linear`.
    **REMINDER**: Standard QP problems take the following form:  `minimize (1/2)x.T * P * x + q.T x subject to A*X = b , Gx <= h`

    **NEW**: For LP and QP problems, you can now add **custom constraints** to your problem not just the standard form!
    When specifying the matricies and vectors of the problem, define any matrix or vector you want and define the constraints in `constraints = [...]`
    **IMPORTANT NOTE**: Matricies `A`, `P`, `G` and vectors `b`, `c`, `h`, `q` are *reserved*, so to aviod any errors name your vectors any thing else
    `ex` f::optimize linear c= [3, -2] # constraints = [sum(x) == 1]
    `ex` f::optimize quadratic P = [[1, 2], [2, 1]] # b= [0, 0] # constraints = [sum(x) == 1, x >= 0]

    - `f::optimize ls A = [...] # b = [...]` solves **least squares problems**
    `ex` f::optimize ls A = [3, -4] # b = [0]
```f::check```This is used to **check on some properties.** The available tests right now are:

    - `f::check dt [ [...] , [...] ]` which checks the **definite type** of a matrix and returns its **eigenvalues**.
    **NOTE**: The matrix has to be **square** and **symmetric**.
    `ex` f::check dt [ [2, 1] , [1, 2] ]

Type `f::help` anytime to show this message again."""
    return guide1, guide2