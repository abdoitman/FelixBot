![banner 1](https://user-images.githubusercontent.com/77892920/228115884-0316d0ac-5988-4a4f-80e6-7a758c2fa3d1.png)

# **Welcome to FelixBot**
FelixBot is a discord bot designed to help students visualize **spaces and vectors** in **2D and 3D** using matplotlib. Also, **solve optimization problems** using **CVXPY**.

**Table of Contents** :
  * [__Demonstration__](#demonstration)
    * [__Key Features__](#key-features)
    * [__Quick Examples__](#quick-examples)
  * [__How To Use__](#how-to-use)
  * [__How It Works__](#how-it-works)

<hr>

## **Demonstration**
### **Key Features**
* __Easy to set up and use.__
* __Plot spaces and vectors.__
* __Can solve linear program, quadratic program and general functions optimization problems.__

### **Quick Examples**
* Showing an equation in a **mathematical** form: ```f::show sin(2*x_1*pi) / sqrt(x_2) var x_1 x_2```<br>
*Response*:<br>
<p align="center"> <img src="https://user-images.githubusercontent.com/77892920/231904497-f6e047e3-214d-4754-96bf-950bbba85dd4.png"> </p>

* Plotting a **set of vectors**: ```f::imagine vectors [2, 3] # [1, 0] # [6,4]```<br>
*Response*:<br>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231904770-7a7821ab-2f27-4863-8e9c-c7331646aff2.png" width = "512" height = "512"> </p>

* Plotting **equation**: ```f::imagine equation x**2 + y**2 var x y with constraints x > 0```<br>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231906540-0aa46ae4-2d99-4446-b347-8a44c4d7ea65.gif"> </p>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231906547-a0137c07-5730-4395-9b44-5b4e3cad3722.gif" width = "512" height = "512"> </p>

* **Solving an optimization problem**: ```f::optimize linear c=[5, 1, 2, 0, -5, 6 ,0.5] # constraints= [x >= 0, sum(x) == 3]```<br>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231906011-d98e68e7-2f61-4a95-855a-92abcec40841.png"> </p>

<hr>

## **How To Use**
You can use [this link](https://discord.com/api/oauth2/authorize?client_id=1080176668297142403&permissions=8&scope=bot) to make the bot join your server. Also, note that the bot needs a `#bot-help` channel to be in the server before it arrives. <br>

The link above will take you to *this screen*, where you get to choose which of the servers you mange you want to add the bot to. <br>

<p align="center"><img src= "https://github.com/abdoitman/FelixBot/assets/77892920/5f973fc0-d7f4-4e63-b3f2-87ee1684e1b6"></p>

**NOTE**: currently the bot is **not** hosted on any online server, therefore, sadly it's down <br>

<hr>

## **How It Works**
The project has an architecture of multiple modules that can be classified as follows: <br>
  * **Bot entry point** <br>
    * [main](#main)
    * [bot module](#bot-module)
  * **Taking the input** <br>
    * [handle_responses module](#handle_responses-module)
    * [input_commands module](#input_commands-module)
    * [validation module](#validation-module)
  * **Executing the input** <br>
    * [help module](#help-module)
    * [write_latex module](#write_latex-module)
    * [imagine package](#imagine-package)
    * [optimize module](#optimize-module)
    * [check module](#check-module)

<hr>

### **Bot entry point**
#### `main`
[main.py](https://github.com/abdoitman/FelixBot/blob/main/main.py) is the main entry point of running the bot. It only calls `run_discord_bot()` from [bot module](#bot).
#### `bot` module
[bot.py](https://github.com/abdoitman/FelixBot/blob/main/bot.py) contains 3 functions:
  1. `run_discord_bot()` which is responsible for running the bot. It also defines the behavior of the bot. Among receiving a message that starts with `f::` it calls `process_message` to process the input message.
  2. `process_message(user, channel, user_message, client)` which calls the `process` function from the `handle_responses` module to understand and analyze the input message.
  3. `send_message_to_channel(user_id, channel, response)` which **mentions the user** that messaged the bot and **sends the response** of the bot to the channel.

<hr>

### **Taking the input**
#### `handle_responses` module
[handle_responses.py](https://github.com/abdoitman/FelixBot/blob/main/handle_responses.py) has one main function `process` which **extracts what command the user entered** and calls the corresponding response function.
#### `input_commands` module
[input_commands.py](https://github.com/abdoitman/FelixBot/blob/main/input_commands.py) introduces 3 main classes that will be used to define and change the string input message into numeric values and equations. The classes are:
  1. `InputParser` : parses the input messages into **an equation**, **variables**, and **constraints.**
  2. `VectorsParser` : parses the input into a **vector or multiple vectors**.
  3. `OptimizationMatriciesParser` : this is used to parse the matricies and vectors used as **optimization parameters**.
#### `validation` module
[validation.py](https://github.com/abdoitman/FelixBot/blob/main/validation.py) works hand in hand with [input_commands module](#input-commands-module). It makes sure that the input being fed into the input_command classes is valid.

<hr>

### **Executing the input**
#### `help` module
[help.py](https://github.com/abdoitman/FelixBot/blob/main/help.py) has one main function; `show_general_guide()` which returns a general guide about the about and the functionality of it. Also, there are other functions that returns specific, more detailed message about each functionality of the bot.
#### `write_latex` module
[write_latex.py](https://github.com/abdoitman/FelixBot/blob/main/write_latex.py) has a main function which is `show_latex`. Internal function `__save_latex_png` uses [latex.codecogs](http://latex.codecogs.com) to convert the latex into PNG transparent images. After the image is saved, `show_latex` returns the path to the PNG file.
#### `imagine` package
See the documentation of the package [here](#https://github.com/abdoitman/FelixBot/blob/main/imagine/readme.md).
#### `optimize` module
[optimize.py](https://github.com/abdoitman/FelixBot/blob/main/optimize.py) has a main function which is `solve` which analyzes the input command and calls the corresponding the solver functions; which are:
  1. `__optimize_general_functions` which solves a general function optimization problem.
  2. `__optimize_linear_program` which solves LP optimization problem.
  3. `__optimize_least_squares` which solves a least squares optimization problem.
  4. `__optimize_quadratic` which solves a quadratic optimization problem.
#### `check` module
[check.py](https://github.com/abdoitman/FelixBot/blob/main/check.py) contains the main function; `inspect` which chooses the function being executed depending on the user input. <br>
Currently, the only check function is `__check_definite_type` which checks the definite type of a matrix whether it's positive-definite, positive-semi-definite, negative-definite, ... etc.
