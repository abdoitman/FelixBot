import write_latex
from imagine import imagine
import optimize
import check
import help
    
async def process(message, client):
    contains_media = False
    command = message.split()[0]
    message = message.replace(command, "").strip()

    if command == 'show':
        if message.startswith("var"): raise Exception("**NOTE**: This is an old way of typing this command.\nNow it's `f::show [equation] var [variables]`")
        response, filename = write_latex.show_latex(message)
        contains_media = True
        return response , contains_media , filename
    
    if command == 'imagine':
        response, filename = await imagine.see_through(message, client)
        contains_media = True
        return response, contains_media, filename
    
    if command == 'optimize':
        response, drawing_command = optimize.solve(message)
        if drawing_command != "":
            _ , filename = await imagine.see_through(drawing_command, client)
            contains_media = True
        else:
            filename = ""
            contains_media = False
        return response, contains_media, filename
    
    if command == 'check':
        response = check.inspect(message)
        return response, contains_media, ""

    if command == 'help':
        if message != "": response = help.show_specific_guide(message)
        else: response = help.show_general_guide()
        return response , contains_media , ""
    
    if message != "" and command + " " + message.split()[0] == "solve sheet":
        response = "https://tenor.com/bhDEJ.gif"
        return response, contains_media, ""

    raise TypeError(f"`{command}` is not yet supported! - Check your command again, maybe it's a Typo.")