import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from .animate import animate_vectors
from time import gmtime, strftime
import re

def __get_vectors(str_vectors):
    
    ## Error handling
    #Check for missing '#'
    if "][" in str_vectors.replace(" ",""): raise Exception("Missing `#`")
    #Chck for missing '['
    if error := re.findall(r"\]\d", str_vectors.replace(" ","")): raise Exception(f"Fix `{str(*error)}` !\nPerhaps missing a `[`")

    str_vectors_list = str_vectors.split("#")

    vectors = []
    max_coordinate = min_coordinate = 0
    for vec in str_vectors_list:
        try:
            temp_vec = eval(vec.strip())
        except:
            raise Exception("Something's wrong! Perhaps missing a `comma` or `]`?")
        vectors.append(temp_vec)
        if(max(temp_vec) >= max_coordinate ): max_coordinate = max(temp_vec)
        if(min(temp_vec) <= min_coordinate ): min_coordinate = min(temp_vec)

    if max_coordinate > 60 or min_coordinate < -60:
        raise Exception("Your vector is too epic. Try something smaller!")
    return vectors, max_coordinate, min_coordinate

def __imagine_2d(vectors, max_coordinate, min_coordinate):
    fig, ax = plt.subplots(figsize=(10.24,10.24))

    #set limits for axes
    ax.set_xlim(min_coordinate* 1.1, max_coordinate* 1.1)
    ax.set_ylim(min_coordinate* 1.1, max_coordinate* 1.1)

    #define colors
    colors = ["#DE0004", "#3C00DE", "#E56E17", "#0094E5",
              "#00E509", "#00E509", "#D1BC0E", "#DE00D9"]

    for index, vector in enumerate(vectors):
        x = vector[0]
        y = vector[1]

        color = colors[index % 8]
        ax.quiver(0,0, x,y, color= color, label="vector: "+ str(vector), angles='xy', scale_units='xy', scale=1)

    #set axes ticks
    #ax.set_xticks(range(round(min_coordinate*1.1), round(max_coordinate*1.1), 2))
    #ax.set_yticks(range(round(min_coordinate*1.1), round(max_coordinate*1.1), 2))

    #plot
    ax.title(f"Drawing {len(vectors)} vector(s)", fontdict={'fontsize': 18})
    ax.legend()
    ax.grid(visible=True, alpha= 0.25)
    fig.savefig(filename := "./__output/2Dvec_" + strftime("%d%b%Y%H%M%S", gmtime()) + ".png")
    return filename

def __imagine_3d(vectors, max_coordinate, min_coordinate, angle= 240, is_frame= False):

    fig = plt.figure(figsize=(10.24, 10.24))
    ax = fig.add_subplot(projection="3d")
    plt.rcParams["figure.autolayout"] = True

    #set limits for axes
    ax.set_xlim(min_coordinate* 1.1, max_coordinate* 1.1)
    ax.set_ylim(min_coordinate* 1.1, max_coordinate* 1.1)
    ax.set_zlim(min_coordinate* 1.1, max_coordinate* 1.1)

    #define colors
    colors = ["#DE0004", "#3C00DE", "#E56E17", "#0094E5",
              "#00E509", "#00E509", "#D1BC0E", "#DE00D9"]

    for index, vector in enumerate(vectors):
        x = vector[0]
        y = vector[1]
        z = vector[2]

        color = colors[index % 8]
        ax.quiver(0,0,0, x,y,z, color= color, label="vector: "+ str(vector))

    #set axes ticks
    # ax.set_xticks(range(round(min_coordinate*1.1), round(max_coordinate*1.1), 2))
    # ax.set_yticks(range(round(min_coordinate*1.1), round(max_coordinate*1.1), 2))
    # ax.set_zticks(range(round(min_coordinate*1.1), round(max_coordinate*1.1), 2))

    #draw axes
    ax.plot([0,0], [0,0], [max_coordinate* -1.5, max_coordinate* 1.5], color="black",  alpha= 0.3)
    ax.plot([0,0], [max_coordinate* -1.5, max_coordinate* 1.5], [0,0], color="black",  alpha= 0.3)
    ax.plot([max_coordinate* -1.5, max_coordinate* 1.5], [0,0], [0,0], color="black",  alpha= 0.3)

    ax.view_init(elev=35, azim= angle, roll=0)

    #plot
    plt.title(f"Drawing {len(vectors)} vector(s)", fontdict={'fontsize': 18})
    plt.legend()
    if is_frame:
        fig.savefig(f"./__frames/frame_{angle}.png")
        plt.close()
    else:
        fig.savefig(filename := "./__output/3Dvec_" + strftime("%d%b%Y%H%M%S", gmtime()) + ".png")
        plt.close()
        return filename
    
def draw_vectors(str_vectors):
    vectors, max_coordinate, min_coordinate = __get_vectors(str_vectors)
    length_vectors = [len(vec) for vec in vectors]

    if(len(set(length_vectors)) != 1): raise Exception("Make sure all vectors are of the same dimension!")
    
    if len(vectors[0]) == 1:
        if (length_vectors == [1] * len(length_vectors)):
            vectors = [vec + [0] for vec in vectors]
        filename = __imagine_2d(vectors, max_coordinate, min_coordinate)
        
    elif len(vectors[0]) == 2:
        filename = __imagine_2d(vectors, max_coordinate, min_coordinate)
        
    elif len(vectors[0]) == 3:
        # __imagine_3d(vectors, max_coordinate, min_coordinate)
        filename = animate_vectors(vectors, max_coordinate, min_coordinate, __imagine_3d)
    else:
        raise Exception("Can't render vectors that have a dimension greater than 3!")
    
    return filename
