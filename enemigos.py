import pygame
import random 
import time
from pygame.sprite import Sprite
from constantes import *
from proyectiles import *
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

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        #*==Imagen
        self.image_list = get_surface("img/NPC_126.png", 1, 6)
        self.image_indice = 0
        self.image = self.image_list[self.image_indice]
        new_width = 30
        new_height = 30
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        #*==Rectangulo
        self.rect = self.image.get_rect()
        #*==Posicion==
        self.timer_descenso = 0
        self.rect.x = random.randrange(ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randrange(-self.rect.height,-20)  

        #*==Movimiento==
        self.velocidad_x = random.randrange(1,5)
        self.velocidad_y = random.randrange(1,5)
        #*==Proyectiles
        self.cooldown = 0
        self.cooldown_duration = 1000 
        
        
    def update(self):
        
        #*==Comprueba si es el momento de descender
        self.timer_descenso += 1
        if self.timer_descenso >= 200:  
            self.rect.y += random.randrange(50,100)  
            self.timer_descenso = 0 

  
        #*==Limita el margen inferior
        if self.rect.bottom > ALTO_PANTALLA:
            self.rect.bottom = ALTO_PANTALLA
        #*=Movimiento del sprite 
        self.update_sprite()



    def update_sprite(self):

        self.image_indice += 1
        if self.image_indice >= len(self.image_list):
            self.image_indice = len(self.image_list) - 3
        self.image = self.image_list[self.image_indice]


class Enemigo2(Enemigo):
    def __init__(self,fire_rate):
        super().__init__()
        #*==Imagen
        self.image_list = get_surface("img/NPC_125.png", 1, 6)
        self.image_indice = 0
        self.image = self.image_list[self.image_indice]
        #*==limite de tiempo entre disparos
        self.fire_rate = fire_rate
        #*==Tiempo del ultimo disparo
        self.last_shot_time = 0
        self.img_proyectil = pygame.image.load("img/proyectil_enemigo.png")
        self.is_stopped = False
        self.stop_duration = 10  
        self.last_stop_time = pygame.time.get_ticks()  
    
    
    def update(self,grupo_proyectiles_enemigos):
        #*==Actualiza el movimiento de los enemigos
        self.rect.x += self.velocidad_x

        #*==Comprueba si es el momento de descender
        self.timer_descenso += 1
        if self.timer_descenso >= 500:  
            self.rect.y += random.randrange(50,100) 
            self.timer_descenso = 0  

        #*==Limita los márgenes derecho e izquierdo
        if self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x *= -1
        elif self.rect.left < 0:
            self.velocidad_x *= -1

        #*==Limita el margen inferior
        if self.rect.bottom > ALTO_PANTALLA:
            self.rect.bottom =SPAWN_ENEMIGO
        #*=Movimiento del sprite 
        self.update_sprite()
        self.shoot(grupo_proyectiles_enemigos)
        
    def shoot(self,grupo_proyectiles_enemigos):
        #*==Disparos del player==
        current_time = pygame.time.get_ticks()  #*==Tiempo actual del juego
        #*==verificar si la tecla de espacio está presionada y si ha pasado suficiente tiempo desde el último disparo
        if current_time - self.last_shot_time > self.fire_rate:
            #*== Crear una nueva instancia de la clase Bullet en la posición del jugador
            bullet = Bullet(self.rect.centerx, self.rect.top-5,10,self.img_proyectil)
            #*==Agrega la bala a la lista
            grupo_proyectiles_enemigos.add(bullet)
            #*==Actualizar el tiempo del último disparo al tiempo actual
            self.last_shot_time = current_time
            
    def update_sprite_2(self):

        self.image_indice += 1
        if self.image_indice >= len(self.image_list):
            self.image_indice = len(self.image_list) - 3
        self.image = self.image_list[self.image_indice]
