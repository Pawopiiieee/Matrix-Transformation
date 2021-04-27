import tkinter as tk
from tkinter import Button,GROOVE
import math

window_width = 750
window_height = 600
master = tk.Tk()
master.title("Matrix Transformation")
master.geometry("750x600")
master.resizable(0, 0)
canvas = tk.Canvas(master,height = window_height,width = window_width, bg = "#85a3e0" ) 
canvas.pack()#put drawing in the canvas
"""make x,y coorinate lines"""
canvas.create_line(window_width/2 , 0, window_width/2, window_height, fill = "#fff", width = 1 ) #y axis
canvas.create_line(0,window_height/2,window_width,window_height/2, fill = "#fff" , width = 1) #x axis

#Making a fox by creating half a shape at the Tk coordinate point (0,0), then transfrom it to an offset. 
# Later it can be mirrorred to the coordinated areas. There might be an easier  and simplier way to make a fox on Tk, but I have no clue. 
def composite_matx(matrix_a,matrix_b): #mirroring process/translate point/rescaling
	"""
	This function follows the matrix composite transformation method (Mathematics for Engineering p.589) 
	by using homogeneous matrix and extended matrix
	in this function, there's also a calculation for matrices multiplication. 
	Instead of raising an exception if the column of the first matrix != the number of row in the second matrix, 
	homogeneous coordinate will be appended to the smaller matrix so that it can be used for matrices multiplication.
	"""
	smaller_m = matrix_a
	bigger_m = matrix_b
	if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]): # first check the size of two matrices and check if they are of different size, 
		if len(matrix_a) > len(matrix_b) or len(matrix_a[0]) > len(matrix_b[0]): # if so then decide which one is 2x2(smaller) or 3x3(bigger)	
			bigger_m = matrix_a
			smaller_m = matrix_b
		
		for k in range(len(smaller_m)):
			if len(bigger_m[k]) > len(smaller_m[k]):
				smaller_m[k].append(0) # if multiplying 2x2 by 3x3 matrix, add homogenous coordinates to the 2x2
		smaller_m.append([0,0,1])
	result = [] 
	for i in range(len(matrix_a)): 
		row = []
		for j in range(len(matrix_b[0])):
			value = 0
			for k in range( len(matrix_b)):
				value += matrix_a[i][k] * matrix_b[k][j] # multiplication of 2 matrices which results in the composite matrix of the 2 seperate matrices
			row.append(value)
		result.append(row)
	#print("composition: ", result)
	return result

def vector_x_matrix(matx,vectorxy): #this function is for vector(x,y points) and matrix(the result from composit matx function) multiplication
	vector = [] #result of matrices multiplication
	if len(vectorxy) < len(matx):
		vectorxy.append(1)	#if the size of vectorxy < the size of matx, add "1" to the last index. (this makes the homogenius vector)
	for k in range(len(vectorxy)):
		vector.append(0) #add "0" as much as the same amount of the input vector, to make sure that the initial vector in the list is 0	
	for i in range(len(matx)):
		for j in range (len(matx[i])):
			vector[i] += vectorxy[j] * matx[i][j] # vector x matrix multiplication
	#print ("vector: ", vector) #to check the points if it's correct 
	return vector	#return the real points on Tk	

def create_polygon(xy_points,matrix, canvas,color = ""): #to draw multiple triangels to make half a fox
	result = []
	for point in xy_points:
		point = vector_x_matrix(matrix,point)
		#print("point: ", point) #result in 3x3 Matrix: x,y,z 
		result.append([point[0], point[1]]) #use only the first 2 indexes: x,y so we can work on 2D
	canvas.create_polygon(*result, outline = "#331a00", fill = color, width = 2 )

def draw_heart(matrix): #to draw a simple geometric heart
	#the coordinate points for drawing geometric full heart shape, cannot use reflecting matrix because it's not symmetrical
	create_polygon([[0,-0.25],[1,-1.25],[2,-0.7],[3,-1.25],[4,-0.25],[2,2],[0,-0.25]],matrix,canvas,color="pink") #a set of vector x,y
	create_polygon([[0,-0.25],[0.9,-0.2],[1,-1.25],[0,-0.25]],matrix,canvas,color="#dc7474")
	create_polygon([[0.9,-0.2],[1,-1.25],[2,-0.7],[0.9,-0.2]],matrix,canvas,color="#ff5050")
	create_polygon([[4,-0.25],[3,-1.25],[2.9,-0.2],[4,-0.25]],matrix,canvas,color="#dc7474")
	create_polygon([[2,-0.7],[2.9,-0.2],[3,-1.25],[2,-0.7]],matrix,canvas,color="#ff5050")
	create_polygon([[2,-0.7],[0.9,-0.2],[2.9,-0.2],[2,-0.7]],matrix,canvas,color="#dc7474")
	create_polygon([[0,-0.25],[2,2],[0.9,-0.2],[0,-0.25]],matrix,canvas,color="#ff5050")
	create_polygon([[2,2],[4,-0.25],[2.9,-0.2],[2,2]],matrix,canvas,color="#ff5050")

#to draw a full fox on the 1st quarter (counter clockwise) by using the composit matrix method
def draw_half_fox_shape(matrix): #the coordinate points for making half of a fox face(half left side). To make a full shape, I exploit the mirror matrix approach
	create_polygon([[-2.7,0], [-2.3,-4], [0,3], [-2.7,0]],matrix, canvas ,color = "#fff2e6") #a set of vectorx,y #light area
	create_polygon([[0,3], [-2.3,-4], [0,-2],[0,3]],matrix,canvas,color = "#b35900")
	create_polygon([[-2.7,0], [0,0], [0,-2], [-2.7,0]],matrix, canvas)
	create_polygon([[-1.4,0], [-1,0], [-0.9,0.5],[-1.4,0]],matrix, canvas, color = "#00264d") #eye
	create_polygon([[0,3], [-0.2,2.2], [0,2.2],[0,3]],matrix, canvas, color = "black") #nose
	create_polygon([[-1.8,1], [0,3], [0,5.7], [-1.8,1]],matrix, canvas,color = "#ffcc99") #chest

def draw_fox_body(matrix): #a set of vector x,y for the fox  body on Tk
	create_polygon([[-1.8,1], [-4.1,2.7], [0,5.7], [-1.8,1]],matrix, canvas,color = "#993d00") #body
	create_polygon([[-4.1,2.7], [0,5.7], [0,7],[-4.1,2.7]],matrix, canvas,color = "#ffbf80") #body
	create_polygon([[-4.1,2.7], [-5.5,5], [-3.8,6.5],[0,7],[-4.1,2.7]],matrix, canvas,color = "#cc5200") #body
	create_polygon([[-5.5,5],[-3.8,6.5],[-2.8,4],[-5.5,5]],matrix, canvas,color = "#e3ccb5") #tail
	create_polygon([[0,5.7], [0,7], [1,6.35], [0,5.7]],matrix, canvas,color = "#331a00") #tail

def draw_fox(matrix): #this function will draw the fox on Tk canvas by using composite transformation
	fox_left_side = composite_matx(matrix, draw_left_side) 
	fox_right_side = composite_matx(matrix, draw_right_side)
	draw_half_fox_shape(composite_matx(translate_to_tkinter, fox_left_side)) #draw half a fox on Tk canvas, 2 times composite transformation
	draw_half_fox_shape(composite_matx(translate_to_tkinter, fox_right_side)) #draw another half of a fox, the completed shape on Tk canvas
	draw_fox_body(composite_matx(translate_to_tkinter, fox_left_side)) #draw a fox body on Tk canvas

scale_points = [[10,0],[0,10]] #scale matrix for composit method
mirror_scale = [[-1,0],[0,1]] #mirroring scale matrix for composit method, it's for reflecting another half of a fox
translate_to_offset = [[1,0,100],[0,1,-150],[0,0,1]] #translate the points in a shape to the offset[100,-150]
translate_to_tkinter = [[1,0,375],[0,1,300],[0,0,1]] #translate points in a shape to Tk canvas [375,300]
draw_left_side = composite_matx(translate_to_offset, scale_points) #calculate all the points to the offset
draw_right_side = composite_matx(translate_to_offset, composite_matx(scale_points, mirror_scale))  #calculate all the mirroring points to the offset
identity = [[1,0],[0,1]] #identity matrix for drawing a fox on the 1st quarter
mirror_xscale = [[1,0],[0,-1]] #mirror scale matix for reflecting a fox over the x axis 
mirror_yscale = [[-1,0],[0,1]] #mirror scale matix for reflecting a fox over the y axis
move_fox = [[1,0,200],[0,1,300],[0,0,1]] #to move a fox to the bottom of a canvas by adding x=200, y=300 to the original one
rescale_matrix_smaller = [[0.5,0],[0,0.5]] #a matrix for rescalling a fox, to draw a smaller one
rescale_heart_smaller = [[0.8,0],[0,0.8]] #a matrix for resizing a heart
rescale_matrix_bigger = [[1.3,0,-350],[0,1.3,0],[0,0,1]] #a matric for rescalling a fox, to draw a bigger one and move away x = -350
move_point = [[1,0,-200],[0,1,150],[0,0,1]] #for moving points, in Tk space ,away from the original fox
move_point_heart = [[1,0,230],[0,1,415],[0,0,1]] #same idea as moving point, but this is for drawing a heart at the bottom of a screen
draw_heart(composite_matx(translate_to_tkinter, composite_matx(move_point_heart,(composite_matx(draw_left_side,rescale_heart_smaller))))) #draw geometric heart on the bottom of a screen, right corner
"""
To be able to make each button works, all commands are put in a different function. The function will be call when the button is pressed
the reason why the functions are seperated because I cannot put a parameter in a cammand. Otherwise, Idk how to get it work.
"""
def fox_button(): #To draw full shape of a fox on right side of the canvas
	draw_fox(identity) #make use of identity matrix for drawing an original fox
def reflectX_button(): #To project a reflected a fox according to the x axis
	draw_fox(mirror_xscale)
def reflectY_button(): #To project a reflected a fox according to the y axis
	draw_fox(mirror_yscale)
degree = 0 # initial angle for rotation
def rotate_button(): #To rotate a fox on its central point(0,0) and move away from the full shaped fox head to the 3rd quarter
	global degree 
	#also in this function, if you press the rotation button as many time as you want, you will see that it will rotate until it reach 360 degree radians
	if degree < 360:
		degree += 30 #increment by 30 degrees
		angle = math.radians(degree) #to calculate the radians rotation
		rotate_angle= [[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]] #a matrix for rotation
		draw_fox(composite_matx(move_point, rotate_angle)) #rotate a fox, move away from the original space
		#draw_fox(rotate_angle) #alternative way for rotating a fox but not doing any points translation
	else:
		print("A Full Cycle is reached")
def smaller_fox_button(): #To rescale a fox to a smaller version
	draw_fox(rescale_matrix_smaller)
def bigger_fox_button(): #To rescale a fox to a bigger version
	draw_fox(rescale_matrix_bigger)
def move_fox_button():
	draw_fox(move_fox)

#place buttons on canvas so it's more convenient to user.
drawfox_button=Button(master,bg='#969696',width=16,fg='#3058d1',text='Draw a Fox',font = "Courier",command = fox_button, activebackground='#323232', relief = GROOVE,height=1)	
drawfox_button.place(x = 600,y = 15)
reflecty_button=Button(master, bg='#A50062',width=16,fg='#3058d1',text='Move a Fox',font = "Courier",command = move_fox_button, activebackground='#323232', relief = GROOVE,height=1)
reflecty_button.place(x = 600,y = 40)
reflectx_button=Button(master, bg='#990099',width=16,fg='#3058d1',text='a Fox on X-axis',font = "Courier",command = reflectX_button, activebackground='#323232', relief = GROOVE,height=1)
reflectx_button.place(x = 600,y = 65)
reflecty_button=Button(master, bg='#A50062',width=16,fg='#3058d1',text='a Fox on Y-axis',font = "Courier",command = reflectY_button, activebackground='#323232', relief = GROOVE,height=1)
reflecty_button.place(x = 600,y = 90)
smaller_button=Button(master, bg='#A50062',width=16,fg='#3058d1',text='a Smaller Fox ',font = "Courier",command = smaller_fox_button,activebackground='#323232', relief = GROOVE,height=1)
smaller_button.place(x = 600,y = 115)
bigger_button=Button(master, bg='#A50062',width=16,fg='#3058d1',text='a Bigger Fox ',font = "Courier",command = bigger_fox_button,activebackground='#323232', relief = GROOVE,height=1) 
bigger_button.place(x = 600,y = 140)
rotate_button=Button(master,bg='#969696',width=16,fg='#3058d1',text='Rotate a Fox',font = "Courier",command = rotate_button, activebackground='#323232', relief = GROOVE,height=1)
rotate_button.place(x = 600,y = 165)

master.mainloop()
