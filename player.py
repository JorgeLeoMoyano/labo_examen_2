import pygame
import time
from constantes import *
from proyectiles import *
import sys


def get_surface(path,columnas,filas):
    lista = []
    surface_image = pygame.image.load(path)
    fotograma_ancho = int(surface_image.get_width()/columnas)
    fotograma_alto = int(surface_image.get_height()/filas)
    x = 0
    for columna in range(columnas):
        for fila in range(filas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            surface_fotograma = surface_image.subsurface((x, y, fotograma_ancho, fotograma_alto))
            lista.append(surface_fotograma)
    
    return lista

        
class Player(pygame.sprite.Sprite):
    def __init__(self, speed, fire_rate):
        super().__init__()
        #*==SPRITE==
        self.image = pygame.image.load("img/nave.png")
        self.image = pygame.transform.scale(self.image, (nuevo_ancho, nuevo_alto))
        self.rect = self.image.get_rect()
        #*==Sonido de disparo==
        self.sonido_corchazo = pygame.mixer.Sound("sonidos/laser.mp3")
        #*==POSICIÓN==
        self.rect.x = ANCHO_PANTALLA //2
        self.rect.y = ALTO_PANTALLA -80
        #*==CARACTERISTICAS==
        self.speed = speed
        self.vida = 100
        self.vida_actual = 100
        self.shield = 1000
        self.score = 0
        self.nombre_jugador = ""
        #*==limite de tiempo entre disparos
        self.fire_rate = fire_rate
        #*==Tiempo del ultimo disparo
        self.last_shot_time = 0
        self.img_proyectil = pygame.image.load("img/proyectil_player.png")

    def update(self, keys):
        #*==Movimiento del player==
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO_PANTALLA:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTO_PANTALLA:
            self.rect.y += self.speed

    def draw(self, screen):
        #*==Dibuja al player==
        screen.blit(self.image, self.rect)


    def shoot(self, keys, grupo_proyectiles):
        #*==Disparos del player==
        current_time = pygame.time.get_ticks()  #*==Tiempo actual del juego
        #*==verificar si la tecla de espacio está presionada y si ha pasado suficiente tiempo desde el último disparo
        if keys[pygame.K_SPACE] and current_time - self.last_shot_time > self.fire_rate:
            #*== Crear una nueva instancia de la clase Bullet en la posición del jugador
            bullet = Bullet(self.rect.centerx -5, self.rect.top -30,-10,self.img_proyectil)
            #*==Agrega la bala a la lista
            grupo_proyectiles.add(bullet)
            #*==Actualizar el tiempo del último disparo al tiempo actual
            self.last_shot_time = current_time
            self.sonido_corchazo.play()
            
