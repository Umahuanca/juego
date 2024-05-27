import pygame
from pygame import mixer
from luchador import luchador

mixer.init()
pygame.init()

#pantalla del juego
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


#Nombre del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("El LEGADO")

#fodo
imagen = pygame.image.load('C:/Users/USUARIO/PycharmProjects/proyecte/images/fondos/castillo.jpg').convert_alpha()

#velocidad
clock = pygame.time.Clock()
FPS = 60


#extras de pantalla
inicio = 3
final_del_inicio = pygame.time.get_ticks()
puntuacion = [0, 0]
primersed = False
final_de_sed = 2000

#sonidos :)
pygame.mixer.music.load("assets/audio/hobbit.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
daga = pygame.mixer.Sound("assets/audio/sword.wav")
daga.set_volume(0.5)
quemar = pygame.mixer.Sound("assets/audio/magic.wav")
quemar.set_volume(0.55)

#definicion de colores
rojo = (255, 0, 0)
Azul = (0, 0, 255)
negro = (0, 0, 0)


#detalles de los personajes
movi = 162
escala = 4
distanca = [80, 52]
datos = [movi, escala, distanca]
movi2 = 250
escala2 = 3
posicion2 = [110, 100]
datos2= [movi2, escala2, posicion2]


#imagenes del elfo
warrior_sheet = pygame.image.load("C:/Users/USUARIO/PycharmProjects/proyecte/images/elfo/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("C:/Users/USUARIO/PycharmProjects/proyecte/images/mago/wizard.png").convert_alpha()

#imagen de victoria
Victoria = pygame.image.load('C:/Users/USUARIO/PycharmProjects/proyecte/images/icons/victory.png').convert_alpha()

#definimos numeros de la animacion
animacion_de_elfo = [10, 8, 1, 7, 7, 3, 7]
animacio_de_mago = [8, 8, 1, 8, 8, 3, 7]

#letras
count_font = pygame.font.Font("C:/Users/USUARIO/PycharmProjects/proyecte/fonts/turok.ttf", 80)
score_font = pygame.font.Font("C:/Users/USUARIO/PycharmProjects/proyecte/fonts/turok.ttf", 30)

#ponemos el texto
def draw_text(texto, font, texto_for, x, y):
  imge = font.render(texto, True, texto_for)
  screen.blit(imge, (x, y))
#poner el texto en la pantalla
def draw_bg():
  scaled_bg = pygame.transform.scale(imagen, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#indicadores de vida
def draw_health_bar(vida, x, y):
  sangre = vida / 100
  pygame.draw.rect(screen, negro, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, rojo, (x, y, 400, 30))
  pygame.draw.rect(screen, Azul, (x, y, 400 * sangre, 30))


#craacion de los 2 personajes en la pantalla
elfo_1 = luchador(1, 200, 310, False, datos, warrior_sheet, animacion_de_elfo, daga)
mago_2 = luchador(2, 700, 310, True, datos2, wizard_sheet, animacio_de_mago, quemar)

#aplicacion de un bucle
correr= True
while correr:

  clock.tick(FPS)

  #final
  draw_bg()

  #show player stats
  draw_health_bar(elfo_1.health, 20, 20)
  draw_health_bar(mago_2.health, 580, 20)
  draw_text("P1: " + str(puntuacion[0]), score_font, rojo, 20, 60)
  draw_text("P2: " + str(puntuacion[1]), score_font, rojo, 580, 60)

  #repetir proceso
  if inicio <= 0:
    #movimiento de personajes
    elfo_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, mago_2, primersed)
    mago_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, elfo_1, primersed)
  else:
    #conteo de pantalla
    draw_text(str(inicio), count_font, rojo, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

    if (pygame.time.get_ticks() - final_del_inicio) >= 1000:
      inicio -= 1
      final_del_inicio = pygame.time.get_ticks()

  #actualizar
  elfo_1.update()
  mago_2.update()

  #descritura de los personajes
  elfo_1.draw(screen)
  mago_2.draw(screen)

  #muerte de alguno de los jugadores
  if primersed == False:
    if elfo_1.alive == False:
      puntuacion[1] += 1
      primersed = True
      round_over_time = pygame.time.get_ticks()
    elif mago_2.alive == False:
      puntuacion[0] += 1
      primersed = True
      round_over_time = pygame.time.get_ticks()
  else:
    #poner la imagen de victoria
    screen.blit(Victoria, (360, 150))
    if pygame.time.get_ticks() - round_over_time > final_de_sed:
      primersed = False
      inicio = 3
      elfo_1 = luchador(1, 200, 310, False, datos, warrior_sheet, animacion_de_elfo, daga)
      mago_2 = luchador(2, 700, 310, True, datos2, wizard_sheet, animacio_de_mago, quemar)

  #condicion
  for ronda in pygame.event.get():
    if ronda.type == pygame.QUIT:
      correr = False


  #para correr o/y actualizar
  pygame.display.update()

#final del juego
pygame.quit()