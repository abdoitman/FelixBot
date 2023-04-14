import os, requests, re
import sympy
from sympy.parsing.sympy_parser import parse_expr
from time import gmtime, strftime
import InputCommands

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

def __generate_latex_png(message):

    latex_command = InputCommands.InputParser(message)

    for var in latex_command.get_variables():
        globals()[f"{var}"] = sympy.symbols(var)
    
    latex_expr =  sympy.latex(parse_expr(latex_command.get_equation()))
    
    final_latex_expr = "f({}): ".format(", ".join(latex_command.get_variables())) + latex_expr
    filename = "./__output/latex_" + strftime("%d%b%Y%H%M%S", gmtime()) + ".png"
    __save_latex_png(final_latex_expr, filename)

    return filename

def show_latex(message):
    try:
        filename = __generate_latex_png(message)
        response = "This is your equation bellow:"
        return response , filename
    except Exception as e:
        raise(e)