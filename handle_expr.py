import os, requests, re
import sympy
from sympy.parsing.sympy_parser import parse_expr
from time import gmtime, strftime

def get_exprs(message, is_equation_only= False):

    if is_equation_only:
        try:
            var = re.findall(r"(?<=var).+(?=#)", message)[0].strip()
        except Exception as e:
            print(e)
            print("couldn't find variables")
            raise Exception(":question: Missing `var`.")
        
        try:
            eq = re.findall(r"(?<=#).*", message)[0]
            eq = eq.replace("^", "**").strip()
        except Exception as e:
            print(e)
            print("Couldn't find equation")
            raise Exception(":question: Missing equation.")
        
        return var, eq

    try:
        obj = re.findall(r"(?<=#).+?(?=[\s\d\(\)])", message)[0].strip()
    except Exception as e:
        print(e)
        print("couldn't find objective")
        raise Exception(":question: Missing `objective`.")

    message = message.replace(" ", "")
    try:
        var = re.findall(r"(?<=var).+(?=#)", message)[0].replace("", " ").strip()
    except Exception as e:
        print(e)
        print("couldn't find variables")
        raise Exception(":question: Missing variables. Use `var:` to state the variables.")

    try:
        eq = re.findall(r"(?<=e).+(?=w)", message)[0]
        eq = eq.replace("^", "**")
    except Exception as e:
        print(e)
        print("couldn't find equation")
        raise Exception(":question: Missing equation.")

    try:
        constraints = re.findall(r"(?<=constraints).+", message)[0].split(",")
    except Exception as e:
        print(e)
        print("couldn't find constraints")
        raise Exception(":question: Missing constraints.")

    return obj, var, eq, constraints

def __remove_escape_characters(s: str) -> str:
    escape_char_dict = {'\f':'\\f',
                        '\t':'\\t',
                        '\n':'\\n',
                        '\b':'\\r',
                        '\r':'\\r',
                        '\a':'\\a',
                        '\b':'\\b',
                        '\v':'\\v',}
    
    for (key, value) in escape_char_dict.items():
        s = s.replace(key,value)
    
    return s

def __save_latex_png(latex_exp, file = 'output.png', to_white=True):
    tfile = file
    latex_exp = __remove_escape_characters(latex_exp)
    if to_white:
        tfile = './__output/tmp.png'
    r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{300} \huge %s' % latex_exp )
    f = open( tfile, 'wb' )
    f.write( r.content )
    f.close()
    if to_white:
        os.system( 'magick convert ./__output/tmp.png -channel RGB -negate -colorspace rgb %s' %file )

def generate_latex_png(message, is_equation_only= False):

    try:
        if is_equation_only:
            vars, eq = get_exprs(message, is_equation_only)
        else:
            _, vars, eq, _ = get_exprs(message)
    except Exception as e:
        raise(e)
        
    for var in vars.split():
        globals()[f"{var}"] = sympy.symbols(var)
    
    # eq = __change_operations(eq)
    latex_expr =  sympy.latex(parse_expr(eq))
    
    final_latex_expr = "f({}): ".format(", ".join(vars.split())) + latex_expr
    filename = "./__output/latex_" + strftime("%d%b%Y%H%M%S", gmtime()) + ".png"
    __save_latex_png(final_latex_expr, filename)

    return filename