#imports
import cv2 as cv
from time import sleep
import numpy as NP

#video-settings
Fps = 60 #Fps (60fps)
offset = 6 #Margem de erro OK
#video-contagem
linha_p = 525 #Posicao OK
largura = 45 #Valor minimo (testar) (resultadoBom = 45)
altura = 45 #Valor minimo (testar) (resultadoBom = 45)
Detectar = [] #Array OK 
Carros = 0 #Contagem OK

def centro(x,y,l,a):
    xC = int(l / 2)
    yC = int(a / 2)
    totalxC = x + xC
    totalyC = y + yC
    return totalxC, totalyC
#função centro

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
    blur = cv.GaussianBlur(cinza,(3,3),2) #5
    subVideo = sub.apply(blur)
    dilatar = cv.dilate(subVideo, NP.ones((5,5)))
    #tirando imperfeições
    matriz = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    #criando matriz
    imgfinal = cv.morphologyEx (dilatar, cv.MORPH_CLOSE, matriz)
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
            if (linha_p + offset) > y > (linha_p - offset):
                Carros += 1
                cv.line(frame1, (25, linha_p), (1200, linha_p), (0, 127, 255), 3)
                Detectar.remove((x, y))
                print("Carros detectados: " + str(Carros))
    #Passou da linha (verificação)
    
    cv.imshow("Video",frame1)
    cv.imshow("Algoritimo",imgfinal)
    #mostrar os videos

    if cv.waitKey(1) == 27:
        break
    #sair (Esc)

cv.destroyAllWindows()
cap.release()
print("Total de carros em media: " +str(Carros)+ " pode haver pequenos erros na contagem")
print("Importante: se voce nao deixar ele finalizar a contagem, a contagem total vai ser o numero total ate o pause")
#Final
