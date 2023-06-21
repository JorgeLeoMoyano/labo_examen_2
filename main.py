import pygame
import random
import sys
import pygame.mixer
import json
from colores import *
from constantes import *
from player import *
from enemigos import *
from button import *




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

















class Juego:
    def __init__(self):

    #!===========Propiedades=================================
    
        pygame.init()
        pygame.mixer.init()
        # *Tamaño  de pantalla
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        # *==Nombre del juego ==
        pygame.display.set_caption("The game")
        # *==Relog==
        self.clock = pygame.time.Clock()
        # *==Cargamos imagen de fondo
        self.imagen_fondo = pygame.image.load("img/fondo_space.jpg")
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # *==Cargamos la musica de fondo ==
        pygame.mixer.music.load("sonidos/terraria-moon-lord.mp3")
        # *==Creo los grupos de sprites
            #?==Proyectiles
        self.balas = pygame.sprite.Group()
        self.proyectiles_enemigos=pygame.sprite.Group()
            #?==Enemigos
        self.enemigos = pygame.sprite.Group()
        self.enemigos_tiradores=pygame.sprite.Group()
            #?==Jugador
        self.player1 = Player(VELOCIDAD, TIEMPO_ENTRE_DISPAROS)
        self.players = pygame.sprite.Group()
        self.players.add(self.player1)
        
        self.spawn_timer = 0
        self.collision_detected = False

      
    #!==============Metodos===================================

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_backgroud(self):
        self.screen.blit(self.imagen_fondo, (0, 0))

    def draw_score(self):
        font = pygame.font.Font("freesansbold.ttf", 20)
        score_text = font.render("SCORE: {0}".format(
            self.player1.score), True, blanco)
        self.screen.blit(score_text, (10, 10))

    def play_music(self):
        pygame.mixer.music.play(loops=-1)   
        pygame.time.delay(100)

    def update_player(self, keys):
        self.players.update(keys)

    def draw_player(self):
        self.players.draw(self.screen)

    def shoot(self):
        self.player1.shoot(self.balas)

    def spawn_Enemies(self):
        if self.spawn_timer >= SPAWN_DELAY:
            enemigo = Enemigo()
            enemigo2= Enemigo2(500)
            self.enemigos.add(enemigo)
            self.enemigos_tiradores.add(enemigo2)
            self.spawn_timer = 0
        else:
            self.spawn_timer += self.clock.get_time()
    
    def update_enemies(self):
        self.enemigos.update()
        self.enemigos_tiradores.update(self.proyectiles_enemigos)
        
    def draw_enemies(self):
        self.enemigos.draw(self.screen)
        self.enemigos_tiradores.draw(self.screen)
    

                
    def colisiones_enemigo_jugador(self):
        if not self.collision_detected:  
            if pygame.sprite.spritecollide(self.player1, self.enemigos, False):
                self.player1.vida_actual -= 10
                self.collision_detected = True  

            if pygame.sprite.spritecollide(self.player1, self.proyectiles_enemigos, False):
                self.player1.vida_actual -= 10
                self.collision_detected = True 
        else:
            self.collision_detected = False  

    def colisiones_player(self):
        colisiones = pygame.sprite.groupcollide(self.balas, self.enemigos, True, True)
        for bala, enemigos in colisiones.items():
            self.player1.score += 10

    def colisiones_enemigos(self):
        colisiones = pygame.sprite.groupcollide(self.balas, self.enemigos_tiradores, True, True)
        for bala, enemigos in colisiones.items():
            self.player1.score += 15
            
    def colisiones_jugador_x_enemigos(self):
        self.player1.colisiones_enemigo_jugador(self.enemigos, self.player1.vida_actual)


    def dibujar_barra_vida(self,posicion, ancho, alto, vida_actual, vida_maxima):
        #*=Calcula el ancho de la barra de vida proporcional al valor actual y máximo
        ancho_vida = int(ancho * (vida_actual / vida_maxima))

        #*=Dibuja el fondo de la barra de vida (rectángulo gris)
        pygame.draw.rect(self.screen, (150, 150, 150), (posicion[0], posicion[1], ancho, alto))

        #*=Dibuja la barra de vida actual (rectángulo verde)
        pygame.draw.rect(self.screen, (0, 255, 0), (posicion[0], posicion[1], ancho_vida, alto))

    def game_over(self):
        if self.player1.vida_actual <= 0:
            return True
        else:
            return False
    

    def run(self):
        running = True
        while running:
            self.events()
            keys = pygame.key.get_pressed()
            self.update_player(keys)
            self.draw_backgroud()
            self.draw_player()
            #=====
            self.spawn_Enemies()
            self.draw_enemies()
            self.update_enemies()
            #=====  
            
            self.proyectiles_enemigos.update()  
            self.proyectiles_enemigos.draw(self.screen)  

            self.proyectiles_enemigos.draw(self.screen)
            self.enemigos.update()
            
            
            self.player1.shoot(keys,self.balas)
            self.balas.draw(self.screen)
            self.balas.update()
            #=====
            # self.colisiones_enemigo_jugador()
            self.colisiones_player()
            self.colisiones_enemigos()
            self.colisiones_enemigo_jugador()
            self.dibujar_barra_vida((10, 30), 200, 20, self.player1.vida_actual, self.player1.vida)         
            self.draw_score()

            self.clock.tick(60)
            
            if self.game_over():
                guardar_puntaje(self.player1.nombre_jugador, self.player1.score)
                mostrar_score()
                pygame.quit()
                sys.exit()
            pygame.display.flip()
        pygame.quit()


