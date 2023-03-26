import imageio
from time import gmtime, strftime
# import asyncio

__step = 2
__start = __step
__stop = 360
__fps = 20

def __create_frames(drawing_func, *args):

    global __start, __stop, __step

    for angle in range(__start,__stop,__step):
        drawing_func(*args, angle, is_frame= True)

def animate_vectors(vectors, max_coordinate, min_coordinate, drawing_func):
    __create_frames(drawing_func, vectors, max_coordinate, min_coordinate)

    global __start, __stop, __step, __fps
    frames = []
    try:
        for t in range(__start,__stop,__step):
            image = imageio.v2.imread(f'./__frames/frame_{t}.png')
            frames.append(image)

        filename = "./__output/animated_3Dvec_" + strftime("%d%b%Y%H%M%S", gmtime()) + ".mp4"
        imageio.mimsave(filename, frames, fps= __fps)
        return filename
    except Exception as r:
        print(r)
        raise Exception(r)

def animate_surface(variables, eq, constraints, drawing_func):
    __create_frames(drawing_func, variables, eq, constraints)

    global __start, __stop, __step, __fps
    frames = []
    try:
        for t in range(__start,__stop,__step):
            image = imageio.v2.imread(f'./__frames/frame_{t}.png')
            frames.append(image)
        filename = "./__output/animated_3Deq_" + strftime("%d%b%Y%H%M%S", gmtime()) + ".mp4"
        imageio.mimsave(filename, frames, fps= __fps)
        return filename
    except Exception as r:
        print(r)
        raise Exception(r)