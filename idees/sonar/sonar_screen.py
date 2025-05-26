#! /bin/python3.11

import sys


# ========================================== #
#                   Imports                  #
# ========================================== #

try:
    ## External modules
    import random
    from math import cos, sin, radians
    import matplotlib.pyplot as plt
    import serial

    ## Data
    from data.sonar import Sonar
    from data.wave import Wave

    print("> Successful imports")

except Exception as importError:
    print(f"Error :\n> {importError}\n")
    sys.exit(0)


# ========================================== #
#                 Connection                 #
# ========================================== #

try:
    port = "COM3"
    print(f"> Successful connection to {port} port")
    
except Exception as portConnectionError:
    print(f"Connection Error :\n> {portConnectionError}\n")


# ========================================== #
#                    Grid                    #
# ========================================== #

class Grid:
    def __init__(self, length, height, rayon):
        self.length = length
        self.height = height
        self.rayon = rayon

    def setup(self):
        # cm to inches
        l_inches, h_inches = (self.length/2.54), (self.height/2.54)

        #Window
        plt.figure(figsize=(l_inches, h_inches))
        plt.axis("equal")
        plt.xlim(-self.rayon, self.rayon)
        plt.ylim(-self.rayon, self.rayon)

        #Grid background
        plt.grid(linestyle='--')
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        
        #Description
        plt.title("Sonar")
        plt.ylabel("axe Y")
        plt.xlabel("Axe x")

    def printOrigin(self, origine):
        Xi, Yi = origine
        plt.plot(Xi, Yi, 'X', color="red", label="Origine")

    def printPoint(self, origin, distance, angleDeg):
        angleRad = radians(angleDeg)
        Xi, Yi = origin
        x = Xi + distance * cos(angleRad)
        y = Yi + distance * sin(angleRad)
        plt.plot(x, y, 'o', color="blue")
        plt.text(x, y, f"{angleDeg}°", fontsize=8, ha='right', va='bottom')


# ========================================== #
#                   Update                   #
# ========================================== #

def generate(n):
    waveList = []
    for i in range(n):
        distance = random.randint(50, 200)
        angle = random.randint(0, 360)
        waveList.append(Wave(i, distance, angle))
        #print(f"Wave n°{i} ---> distance = {distance} & angle = {angle}")
    return waveList

def update():
    try:
        #Grid
        grid = Grid(length=20, height=20, rayon=200)
        grid.setup()

        # Sonar
        sonar = Sonar(position=(0,0), waveList=(generate(10)))
        origin1 = sonar.postion

        #Wave
        #w1 = Wave(0, 100, 15)

        # Obstacle display
        grid.printOrigin(origin1)
        for wave_i in sonar.waveList:
            grid.printPoint(origin1, wave_i.distance, wave_i.angle)
        #grid.printPoint(origin1, w1.distance, w1.angle)

        # Window Open/close
        plt.show()
        plt.close()

    except Exception as execError:
        print(f"\nExecution error :\n> {execError}")

update()