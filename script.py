#imports
import cv2 #OpenCV
from time import sleep
import numpy as NP

#video-settings
delay = 60 #Fps 
offset = 5 #Erro entre px
#video-contagem
linha_p = 500 #Posicao
largura = 80 #Valor minimo
altura = 80 #Valor minimo
Detectar = [] #Array
Carros = 0 #Contagem

def centro(x,y,l,a):
    xC = int(l / 2)
    yC = int(a / 2)
    totalxC = x + xC
    totalyC = y + yC
    return totalxC, totalyC