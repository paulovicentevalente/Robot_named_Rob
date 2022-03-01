# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 22:40:20 2022

@author: pvval
"""

import serial
import io

print ("Digite f (frente), t (trás), e (esquerda), d (diretia), p (parar) ou qualquer coisa para sair:")
digitado = input()
comando = [b'f', b't', b'e', b'd', b'p']

if digitado == 'f':
    disparo = comando[0]
elif digitado == 't':
    disparo = comando[1]
elif digitado == 'e':
    disparo = comando[2]
elif digitado == 'd':
    disparo = comando[3]
elif digitado == 'p':
    disparo = comando[4]
inicio = True   
while (digitado == 'f' or digitado == 't' or digitado == 'e' or digitado == 'd' or digitado == 'p'):

    
    if inicio == True:
        ser = serial.Serial('COM4')
        print(ser.name)
        inicio = False

    ser.write(disparo)
    line = ser.readline()
    print(line)
    f = open("myfile.txt", "a")
    lineStr = str(line)
    info_fim = lineStr[2:]
    info_fim=info_fim[:-5]
    f.write(info_fim)
        

    
    print ("Digite f (frente), t (trás), e (esquerda), d (diretia), p (parar) ou qualquer coisa para sair:")
    digitado = input()
    
    if digitado == 'f':
        disparo = comando[0]
    elif digitado == 't':
        disparo = comando[1]
    elif digitado == 'e':
        disparo = comando[2]
    elif digitado == 'd':
        disparo = comando[3]
    elif digitado == 'p':
        disparo = comando[4]
    else:
        f.close()
        ser.close()
    
