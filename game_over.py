import pygame
import colores
from button import *
from constantes import *
import sys
import main
import player
import json


#!=============================================================


def guardar_puntaje(nombre_jugador, score):
    puntaje = {"nombre": nombre_jugador, "score": score}
    with open("puntajes.json", "a") as file:
        json.dump(puntaje, file)
        file.write("\n")

def mostrar_score():
    puntajes = []
    with open("puntajes.json", "r") as file:
        for line in file:
            puntaje = json.loads(line)
            puntajes.append(puntaje)

    puntajes.sort(key=lambda x: x["score"], reverse=True)

    print("=== Puntajes ===")
    for i, puntaje in enumerate(puntajes, start=1):
        print(f"{i}. {puntaje['nombre']}: {puntaje['score']}")


#!=============================================================    
    
    
screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.init()
clock = pygame.time.Clock()

fondo = pygame.image.load("img/terraria.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))



 
def salir_juego():
    pygame.quit()
    sys.exit()
    
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir_juego()


 
    screen.blit(fondo,(0,0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
