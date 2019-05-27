##A quantum encryption project by OrigamiDrag0n (Henry Jaspars) 22-26/05/19
##The quantum encryptor system - completely and utterly insecure as of yet, but a nice thought experiment to play around with.
##The idea is: you send a polarised photon from a grating (which is referred to as the basis which is in red), and another recieves it (reciever, which is in blue).
##The bit is considered a 0 if it is parallel to the grate, and 1 if it is perpendicular (in practice, you would use a beam splitter and two perpendicular polarising gratings.
##The probability of bit corruption is sin(angle_difference)**2, which is the crux of the code. ALL ANGLES ARE RADIANS (We'll have none of this degree crap).
##To work, open in terminal; the code for removing a line works a lot better there, looking really impressive (hacker-y) - although beware of annoying noises, and click the panel to initialise.
##Currently working on a version with images and/or sound (just to see if that works)

##The Modules

from random import gauss, random, uniform
from math import sin, cos, pi, atan2
from tkinter import *
import turtle
import os

##The basis code (encryption/decryption)

def prob(probability):                                     #Returns 1 with probability probability; otherwise, 0
    if random() < probability: return 1
    else: return 0
    
def completebinary(character):
    binary = [int(k) for k in str(bin(ord(character)))[2:]]
    return (7 - len(binary))*[0] + binary

def encode(string):                                        #Encodes string into binary
    return [k for c in string for k in completebinary(c)]
    
def decode(binary):
    return "".join([chr(int("0b" + "".join([str(binary[7*i + k]) for k in range(7)]),2)) for i in range(int(len(binary)/7))])
                   
#print(decode(encode("H3LL0 testing this 3NCRYPT10N")))    #This shows how bit errors can accumulate dramatically, and the importance of error correcting codes
#text = decode([0]+encode("H3LL0 testing this 3NCRYPT10N"))
#print(text)
#print(decode(encode(text)[1:]))

def quantum_angles(binary, basis, error_deviation = 0):    #Converts the series of binary into angles, 0 going to basis, 1 going to basis + pi/2 (like a polarising grating)
    return [basis + bit*pi/2 + gauss(0, error_deviation) for bit in binary]

def quantum_binary(angles, basis):                         #Converts the angles back into binary, with 1 appearing with probability sin(angle - basis)**2 (which is to do with quantum encryption)
    return [prob(sin(angle - basis)**2) for angle in angles]

def quantum_encode(string, basis, error_deviation = 0):    #String to angles
    return quantum_angles(encode(string), basis, error_deviation)

def quantum_decode(angles, basis):                         #Angles to string
    return decode(quantum_binary(angles, basis))

def rotate(point, angle):                                  #Rotates a point through angle radians clockwise
    return (point[0]*cos(angle) - point[1]*sin(angle), point[1]*cos(angle) + point[0]*sin(angle))

##Now for the main section of the code: a moveable dial and keystroke interface to change the angle of grating which in turn shows up as text on the screen.

string = "Does God play dice?"                              #The disturbed text
basis = uniform(0, 2*pi)
grating = uniform(0, 2*pi)
perturbation = 0.2                                         #Error angle
h = 200                                                    #Half height of the box
n = 50                                                     #Number of slots
margin = 20                                                #Margin on outside

##Main routine

def main():

    delta = 0.08                                           #Angle of change from keystrokes
    basis_show = False                                     #Whether the basis grating will show (in red - fix colours)
    word = string                                          #Perturbed string

    root = Tk()
    root.title("Use the dial to adjust")
    c = Canvas(root, width = 2*h, height = 2*h, bg = "#000000")
    c.pack()
    text_frame = Canvas(root, width = 2*h, height = h/2, bg = "#000000")
    text_frame.pack()
    
    def dial(c):                                           #The dial (just a circle, of radius h - margin)
        c.create_oval(margin, margin, 2*h-margin, 2*h-margin, outline = "#111", fill = "#fff", width = 3)      

    def lines(c, angle, colour):                           #The grating
        for i in range(n):
            across = (h - margin)*(2*i/(n-1) - 1)
            up = ((h - margin)**2 - across**2)**0.5
            point1 = rotate((up, across), angle)
            point2 = rotate((-up, across), angle)
            c.create_line(point1[0] +h, point1[1]+h, point2[0]+h, point2[1]+h, fill = colour)        

    def draw(c, frame, word):                               #Draws the gratings and text widget (with the basis in red only showing if basis_show is set to true)
        c.delete("all")
        frame.delete("all")
        dial(c)
        lines(c, grating, "#11f")
        if basis_show:
            lines(c, basis, "#f11")
        frame.create_text(h,h/4,fill="white",font="Courier 20", text=word)
        
        
    def left(event):                                       #Anticlockwise (I think... do correct if I'm wrong)
        global grating
        nonlocal c
        global word
        grating -= delta
        word = quantum_decode(quantum_encode(string, basis, perturbation), grating)
        draw(c, text_frame, word)

    def right(event):                                      #Clockwise
        global grating
        nonlocal c
        global word
        grating += delta
        word = quantum_decode(quantum_encode(string, basis, perturbation), grating)
        draw(c, text_frame, word)

    def click(event):                                       #Moveable dial - click, and the grating moves to point to your mouse
        global grating
        nonlocal c
        global word
        c.focus_set()                                       #To record keystrokes
        grating = atan2(event.y - h, event.x - h)           #The angle to the horizontal - add graphics to this
        word = quantum_decode(quantum_encode(string, basis, perturbation), grating)
        draw(c, text_frame, word)
        
    def nothing(event):   #Doesn't affect grating angle: just iterates again
        global word
        word = quantum_decode(quantum_encode(string, basis, perturbation), grating) #This has problems with some characters, so \r does not work. Looks pretty cool in terminal, though.        
        draw(c, text_frame, word)

    def toggle(event):                                       #Flips the basis_show (called by 'b')
        nonlocal basis_show
        nonlocal c
        global word
        basis_show = not basis_show
        draw(c, text_frame, word)

##Now the keystroke binding, and the initialisation.

    c.bind("<Left>", left)
    c.bind("<Right>", right)
    c.bind("<Return>", nothing)
    c.bind("<Button-1>", click)
    c.bind("b", toggle)
    c.pack()
    draw(c, text_frame, word)

    root.mainloop()

if __name__ == "__main__":
    main()
