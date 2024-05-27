import pygame

class luchador():
  def __init__(self, jugador, x, y, vuelta, data, lista_mov, animacion_mov, sound):
    self.Jugador = jugador
    self.altura = data[0]
    self.escala = data[1]
    self.variable = data[2]
    self.vuelta = vuelta
    self.lista_animacion = self.load_images(lista_mov, animacion_mov)
    self.play = 0
    self.cuadro = 0
    self.image = self.lista_animacion[self.play][self.cuadro]
    self.tiempo = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True


  def load_images(self, sprite_sheet, animation_steps):
    #extraer la lista de mov
    animation_list = []
    for y, animation in enumerate(animation_steps):
      lista_de_las_imagnes = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.altura, y * self.altura, self.altura, self.altura)
        lista_de_las_imagnes.append(pygame.transform.scale(temp_img, (self.altura * self.escala, self.altura * self.escala)))
      animation_list.append(lista_de_las_imagnes)
    return animation_list


  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    variable1 = 0
    variable2 = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    golpe = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking == False and self.alive == True and round_over == False:
      #controles del elfo
      if self.Jugador == 1:
        #movimiento
        if golpe[pygame.K_a]:
          variable1 = -SPEED
          self.running = True
        if golpe[pygame.K_d]:
          variable1 = SPEED
          self.running = True
        #saltar
        if golpe[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #botones para atacar
        if golpe[pygame.K_s] or golpe[pygame.K_z]:
          self.attack(target)
          #ponemos que ataque utilizara
          if golpe[pygame.K_s]:
            self.attack_type = 1
          if golpe[pygame.K_z]:
            self.attack_type = 2


      #controles del Mago
      if self.Jugador == 2:
        #determinamos sus movimientos
        if golpe[pygame.K_LEFT]:
          variable1 = -SPEED
          self.running = True
        if golpe[pygame.K_RIGHT]:
          variable1 = SPEED
          self.running = True
        #jump
        if golpe[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #ataques
        if golpe[pygame.K_KP1] or golpe[pygame.K_KP2]:
          self.attack(target)
          #determinar que ataque utilizara
          if golpe[pygame.K_KP1]:
            self.attack_type = 1
          if golpe[pygame.K_KP2]:
            self.attack_type = 2


    #gravedad
    self.vel_y += GRAVITY
    variable2 += self.vel_y

    #detrminar que el jugador este en la pantalla, tanto del elfo que estara
    # en la izquierda y el mago que estara en la desrecha
    if self.rect.left + variable1 < 0:
      variable1 = -self.rect.left
    if self.rect.right + variable1 > screen_width:
      variable1 = screen_width - self.rect.right
    if self.rect.bottom + variable2 > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      variable2 = screen_height - 110 - self.rect.bottom

    #enfrentamiento
    if target.rect.centerx > self.rect.centerx:
      self.vuelta = False
    else:
      self.vuelta = True

    #detenimiento de ataques
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #actualizar posiciones del jugador
    self.rect.x += variable1
    self.rect.y += variable2


  #actualizaciones
  def update(self):
    #vemos que las accciones o movimientos sean devidamente realizados
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.movimientos_act(6)#6:death
    elif self.hit == True:
      self.movimientos_act(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 1:
        self.movimientos_act(3)#3:attack1
      elif self.attack_type == 2:
        self.movimientos_act(4)#4:attack2
    elif self.jump == True:
      self.movimientos_act(2)#2:jump
    elif self.running == True:
      self.movimientos_act(1)#1:run
    else:
      self.movimientos_act(0)#0:idle

    animation_cooldown = 50
    #cargar imagenes
    self.image = self.lista_animacion[self.play][self.cuadro]
    #tiempo de la actualizacion, comprobamos
    if pygame.time.get_ticks() - self.tiempo > animation_cooldown:
      self.cuadro += 1
      self.tiempo = pygame.time.get_ticks()
    #comprobar si la animación ha terminado
    if self.cuadro >= len(self.lista_animacion[self.play]):
      #determinamos que si el jugador está muerto, finaliza la animación.
      if self.alive == False:
        self.cuadro = len(self.lista_animacion[self.play]) - 1
      else:
        self.cuadro = 0
        #vemos si ya se realizo el ataque
        if self.play == 3 or self.play == 4:
          self.attacking = False
          self.attack_cooldown = 20
        #comprobar si se sufrió daño
        if self.play == 5:
          self.hit = False
          #Si el jugador estaba en medio de un ataque, entonces el ataque se detiene.
          self.attacking = False
          self.attack_cooldown = 20


  def attack(self, target):
    if self.attack_cooldown == 0:
      #ejecutar ataque
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.vuelta), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True


  def movimientos_act(self, new_action):
    #comprobar si la nueva acción es diferente a la anterior
    if new_action != self.play:
      self.play = new_action
      #actualizar la configuración de animación
      self.cuadro = 0
      self.tiempo = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.vuelta, False)
    surface.blit(img, (self.rect.x - (self.variable[0] * self.escala), self.rect.y - (self.variable[1] * self.escala)))
