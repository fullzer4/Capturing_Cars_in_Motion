#imports
import cv2 #OpenCV
from time import sleep
import numpy as NP

#video-settings
Fps = 60 #Fps 
offset = 5 #Margem de erro
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

#video input
cap = cv2.VideoCapture("video.mp4")
sub = cv2.bgsegm.createBackgroundSubtractorMOG()

#tirar imperfeições
while True:
    ret , frame1 =cap.read()
    #capturar frames
    ajuste= float(1/Fps)
    sleep(ajuste)
    #ajustar processamento
    cinza = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(cinza,(3,3),5)
    subVideo = sub.apply(blur)
    dilatar = cv2.dilate(subVideo, NP.ones((5,5)))
    #tirando imperfeições
    matriz = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #criando matriz
    preencher1 = cv2.morphologyEx (dilatar, cv2.Morph_CLOSE, matriz)
    preencher2 = cv2.morphologyEx (preencher1, cv2.Morph_CLOSE, matriz)
    imgfinal = cv2.morphologyEx (preencher2, cv2.Morph_CLOSE, matriz)
    #ajuste final

    img,contorno,a = cv2.findContours(imgfinal,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #achar contornos
    cv2.line(frame1, (25, linha_p), (1200, linha_p), (255,255,255), 3)
    #criar linha
    for(i, Autoc) in enumerate(contorno):
        (x,y,l,a) = cv2.bondingRect(Autoc)
        contornoVerificado = ( l >= largura) and ( a >= altura)
        if not contornoVerificado:
            continue

        cv2.retangle(frame1, (x,y), (x+l, y+a),(255,203,219), 2)
        Fcentro = centro(x,y,l,a)
        Detectar.append(Fcentro)
        cv2.cricle(frame1, centro, 4, (153, 51, 153), -1)
    #detectar os carros e colocar boxes e meio(com circulo)

        for (x,y) in Detectar:
            if y <(offset+linha_p) and y>(offset-linha_p):
                Carros+=1
                print("Carros: "+ Carros)
                cv2.line(frame1, (25, linha_p), (1200, linha_p), (0,128,0), 3)
                Detectar.remove((x,y))
    #Passou da linha (verificação)
    
    cv2.imshow("Video",frame1)
    cv2.imshow("Algoritimo",imgfinal)
    #mostrar os videos

    if cv2.waitKey(1) == 27:
        break
    #sair (Esc)

cv2.destroyAllWindows()
cap.release()
#Final
