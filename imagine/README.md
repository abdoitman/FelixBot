# Imagine Package
This package consists of 4 main files:
  1. [**imagine.py**](#imagine)
  2. [**imagine_vectors.py**](#imagine_vectors)
  3. [**imagine_space.py**](#imagine_space)
  4. [**animate.py**](#animate)

<hr>

## imagine
This ([imagine.py](https://github.com/abdoitman/FelixBot/blob/main/imagine/imagine.py)) is considered as the entry point of the package. The function `see_through` gets called by `handle_responses.process` when invoced with the keyword *imagine*. This will process the input message and call the appropiate function whether it's `draw_space` or `draw_vectors` from the appropiate module.

<hr>

## imagine_vectors
This ([imagine_vectors.py](https://github.com/abdoitman/FelixBot/blob/main/imagine/imagine_vectors.py)) is responsible for drawing the vector(s) whether in 2D or 3D. The main function that gets called is `draw_vectors`.

<hr>

## imagine_space
This ([imagine_space.py](https://github.com/abdoitman/FelixBot/blob/main/imagine/imagine_space.py)) is responsible for drawing an equation in a 2D plane or a surface in a 3D space. The main function that gets called is `draw_space`.

<hr>

## animate
This ([animate.py](https://github.com/abdoitman/FelixBot/blob/main/imagine/animate.py)) is responsible for animating every plot. The result is a .mp4 file of the rotating surface/vectors in space with an elevation and roll angles of (35°, 0°).
