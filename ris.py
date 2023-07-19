from PIL import Image, ImageDraw 

import keyboard

import mouse
import pyautogui

import time




orig = Image.open('2.jpg') #Открываем оригинальное изображение
size = (420, 420) #Задаем размер который хотим
image = orig.resize(size) #Изменяем ему размер

draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей 

for x in range(width):
	for y in range(height):
		r = pix[x, y][0] #Значение красного 
		g = pix[x, y][1] #Зеленого
		b = pix[x, y][2] #Синего
		#r, g, b = pix[x, y]
		sr = (r + g + b) // 3 #Среднее значение
		if sr <= 140: #Если ср значение <= числу(n), тогда bw = черному
			bw = 0
		else:         #В остальных случаях равно белому
			bw = 255
		draw.point((x, y), (bw, bw, bw)) #Рисуем пиксель

#image.show()
position_x, position_y = mouse.get_position()

for x in range(width):
	num = 0
	if keyboard.is_pressed('ctrl'):
		break
	for y in range(height):
		if keyboard.is_pressed('ctrl'):
			break
		black = pix[x, y]
		if black == (0, 0, 0):
			if num == 0:
				mouse.release(button='left')
				mouse.move(x+position_x, y+position_y)
				mouse.press(button='left')
			num = num + 1
		else:
			if num > 0:
				mouse.move(x+position_x, y+position_y-1, duration = 0.01)
				mouse.release(button='left')
				#time.sleep(0.01)
			num = 0	
mouse.release(button='left')		 

