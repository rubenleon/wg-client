#!/usr/bin/python3

import subprocess
import time

from colorama import init, Fore, Back, Style

# [Peer]
# #Client=Mi6
# PublicKey = 9olTvgc5AU/LkEwinsdCvM74cVHZY1JKEuKYWztIoXI=
# AllowedIPs = 192.168.99.1/32

# Instalación
# https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html
# pip3 install colorama
 
#Archivo /etc/wireguard/wg0.conf
f = open("/etc/wireguard/wg0.conf")
f_wireguard = f.readlines()
f.close()

#print("f_wireguard: ",f_wireguard)

#print()
#Archivo /etc/wireguard/wg0.conf
lista = []
for i in range(0,len(f_wireguard)-1):
    w = f_wireguard[i]
    w = w.replace("\n","").strip()

    
    if w.find("Client")>=0:
        raw = w.split("=")
        #print("raw",raw)
        client = raw[1].replace("\n","").strip()
        #print("client:",client)

        peer = f_wireguard[i+1]
        peer = peer.split("=",1)[1].strip()
        
        lista.append({"peer":peer,"client":client})
        
        #print(lista) # Dicccionario generado.


wg=subprocess.Popen('wg',shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
salida=wg.stdout.readlines()

sw=False #Interruptor para imprimir linea normal y RESET de estilos
for r in salida:
    linea=str(r.decode("utf-8")) #Línea de la salida del comando 'wg'

    if linea.find("interface")>=0:
        print(Fore.GREEN+linea,end="")
        sw = True

    
    if linea.find("peer")>=0:
        raw = linea.split(":")
        #print("raw",raw)
        peer = raw[1].replace("\n","").strip()
        #print("p33r:",peer)

        for l in lista:
            #print(l["peer"])
            #print(peer)
            if(peer == l["peer"]):
                sw=True
                print(Fore.YELLOW+"("+l["client"]+") "+linea,end="")
                break
            
    if not sw:    
        print(Style.RESET_ALL+linea,end="")
    else:
        sw = False
            
        
        
