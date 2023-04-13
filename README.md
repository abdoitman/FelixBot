![banner 1](https://user-images.githubusercontent.com/77892920/228115884-0316d0ac-5988-4a4f-80e6-7a758c2fa3d1.png)

# **Welcome to FelixBot**
FelixBot is a discord bot designed to help students visualize **spaces and vectors** in **2D and 3D** using matplotlib. Also, **solve optimization problems** using **CVXPY**.

## **Key Features**
* __An easy way to plot spaces and vectors.__
* __Can solve linear program, quadratic program and general functions optimization problems.__

## **Quick Examples**
* Showing an equation in a **mathematical** form: ```f::show sin(2*x_1*pi) / sqrt(x_2) var x_1 x_2```<br>
*Response*:<br>
<p align="center"> <img src="https://user-images.githubusercontent.com/77892920/231904497-f6e047e3-214d-4754-96bf-950bbba85dd4.png"> </p>

* Plotting a **set of vectors**: ```f::imagine vectors [2, 3] # [1, 0] # [6,4]```<br>
*Response*:<br>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231904770-7a7821ab-2f27-4863-8e9c-c7331646aff2.png" width = "512" height = "512"> </p>

* Plotting **equation**: ```f::imagine equation x**2 + y**2 var x y with constraints x > 0```<br>
*Response*:<br>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231906540-0aa46ae4-2d99-4446-b347-8a44c4d7ea65.gif"> </p>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231906547-a0137c07-5730-4395-9b44-5b4e3cad3722.gif" width = "512" height = "512"> </p>

* **Solving an optimization problem**: ```f::optimize linear c=[5, 1, 2, 0, -5, 6 ,0.5] # constraints= [x >= 0, sum(x) == 3]```
*Response*:<br>
<p align="center"><img src="https://user-images.githubusercontent.com/77892920/231906011-d98e68e7-2f61-4a95-855a-92abcec40841.png"> </p>
