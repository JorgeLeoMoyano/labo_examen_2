import pygame
import colores
from button import *
from constantes import *
import sys
import main
import player

screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.init()
clock = pygame.time.Clock()

fondo = pygame.image.load("img/terraria.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
boton_play = Button(screen,"img/play.png",x=350, y=100,width=300,height=100)
text_box = TextBox(screen, x=350, y=200, width=300, height=100, font_size=50)
juego = main.Juego()


def iniciar_juego():
    juego.play_music()
    juego.run() 
    
    
def salir_juego():
    pygame.quit()
    sys.exit()
    
def pulsar_star(boton_play):
    if boton_play.clicked():
            iniciar_juego()
        
        
def esribir_nombre_jugador(text_box, event):
        if event.key == pygame.K_RETURN:
            juego.player1.nombre_jugador = text_box.text
            print(juego.player1.nombre_jugador)

        elif event.key == pygame.K_BACKSPACE:
            text_box.text = text_box.text[:-1]

        else:
            text_box.text += event.unicode

    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir_juego()
        if event.type == pygame.KEYDOWN:
            esribir_nombre_jugador(text_box,event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_box.text != "":
                pulsar_star(boton_play)

 
    screen.blit(fondo,(0,0))
    boton_play.update()
    boton_play.draw()
    text_box.update()
    text_box.draw()
    pygame.display.update()
    clock.tick(FPS)
    
    

pygame.quit()
