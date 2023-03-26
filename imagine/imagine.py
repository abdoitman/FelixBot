from imagine import imagine_vectors, imagine_space
import functools
import json

def __check_if_sent_before(message: str):
    with open("past_commands.json", "r") as past_commands_json:
        try:
            past_commands = json.load(past_commands_json)
            filename = past_commands[message]
            return filename
        except:
            return False

def __save_to_past_commands(message: str, filename: str):
    with open("past_commands.json", "r") as past_commands:
        try:
            json_data = json.load(past_commands)
        except: #json file is empty.
            json_data = {}

    with open("past_commands.json", "w") as past_commands:
        try:
            json_data[message] = filename
            json.dump(json_data, past_commands)
        except Exception as e:
            print(e)

async def run_async_drawing_function(client, drawing_func, *args, **kwargs):
    func = functools.partial(drawing_func, *args, **kwargs)
    return await client.loop.run_in_executor(None, func)

async def see_through(original_message, client):

    response = "This might take a couple of seconds..."
    if (filename := __check_if_sent_before(original_message.replace(" ", ""))):
        return response, filename

    imagine_what = original_message.split()[0]
    message = original_message.replace(imagine_what, "")
    if imagine_what.lower() in ["vectors", "vector"]:
        try:
            filename = await run_async_drawing_function(client, imagine_vectors.draw_vectors, message)
            # filename = imagine_vectors.draw_vectors(message)
            __save_to_past_commands(original_message.replace(" ", ""), filename)
        except Exception as e:
            raise Exception(e)
        return response , filename
    
    if imagine_what.lower() == "equation":
        try:
            filename = await run_async_drawing_function(client, imagine_space.draw_space, message)
            # filename = imagine_space.draw_space(message)
            __save_to_past_commands(original_message.replace(" ", ""), filename)
        except Exception as e:
            raise Exception(e)
        return response , filename
    
    raise Exception(f"`{imagine_what.title()}` is not a valid keyword for `imagine` command")
