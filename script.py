#imports
import cv2 as cv
from time import sleep
import numpy as NP

#video-settings
Fps = 60 #Fps 
offset = 5 #Margem de erro
#video-contagem
linha_p = 550 #Posicao
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

#video input
cap = cv.VideoCapture("video.mp4")
sub = cv.bgsegm.createBackgroundSubtractorMOG()

#tirar imperfeições
while True:
    ret , frame1 =cap.read()
    #capturar frames
    ajuste= float(1/Fps)
    sleep(ajuste)
    #ajustar processamento
    cinza = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(cinza,(3,3),5)
    subVideo = sub.apply(blur)
    dilatar = cv.dilate(subVideo, NP.ones((5,5)))
    #tirando imperfeições
    matriz = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    #criando matriz
    imgfinal = cv.morphologyEx (dilatar, cv.MORPH_CLOSE, matriz)
    imgfinal = cv.morphologyEx (imgfinal, cv.MORPH_CLOSE, matriz)
    #ajuste final

    contorno,a = cv.findContours(imgfinal, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #achar contornos
    cv.line(frame1, (25, linha_p), (1200, linha_p), (255,255,255), 3)
    #criar linha
    for(i, Autoc) in enumerate(contorno):
        (x,y,l,a) = cv.boundingRect(Autoc)
        contornoVerificado = ( l >= largura) and ( a >= altura)
        if not contornoVerificado:
            continue

        cv.rectangle(frame1, (x,y), (x+l, y+a),(255,203,219), 2)
        Fcentro = centro(x,y,l,a)
        Detectar.append(Fcentro)
        cv.circle(frame1, Fcentro, 4, (153, 51, 153), -1)
    #detectar os carros e colocar boxes e meio(com circulo)

        for (x,y) in Detectar:
            if y <(offset+linha_p) and y>(offset-linha_p):
                Carros+=1
                print("Carros: "+ str(Carros))
                cv.line(frame1, (25, linha_p), (1200, linha_p), (0,128,0), 3)
                Detectar.remove((x,y))
    #Passou da linha (verificação)
    
    cv.imshow("Video",frame1)
    cv.imshow("Algoritimo",imgfinal)
    #mostrar os videos

    if cv.waitKey(1) == 27:
        break
    #sair (Esc)

cv.destroyAllWindows()
cap.release()
#Final
