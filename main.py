import pygame
import random
import cProfile

pygame.init()
window = pygame.display.set_mode((300, 300))
world = [[None] * 300 for i in range(300)]
animals = set()
died = set()
born = set()


class animal:
  color = None
  life = 0
  age = 0
  zapladniacz = False
  rodzacy = False
  lifeLong = 100
  alive = True
  posX = 0
  posY = 0
  ciaza = 0
  lenCiaza = 0

  def __init__(self, posX=0, posY=0, zapladniacz=True, rodzacy=True):
    self.color = (255, 255, 255)
    self.life = 10
    self.age = 0
    self.zapladniacz = zapladniacz
    self.rodzacy = rodzacy
    self.alive = True
    self.posX = posX
    self.posY = posY
    self.ciaza = -10
    self.lenCiaza = 50
    self.lifeLong = 255
    self.trup = False

  def die(self):
    global died
    self.trup = True
    world[self.posY][self.posX] = None
    died.add(self)

  def go(self):
    global died
    self.age += 1
    self.death()
    if self.trup:
      return False
    if self.ciaza != 0:
      self.ciaza += 1
    self.insemination()
    self.narodziny()

    sides = [1, 3, 2, 4]
    for n in range(10):
      i = int(random.random() * 4)
      j = int(random.random() * 4)
      sides[i], sides[j] = sides[j], sides[i]
    moved = False

    for side in sides:
      match side:
        case 1:
          moved = self.goRight()
        case 2:
          moved = self.goLeft()
        case 3:
          moved = self.goUp()
        case 4:
          moved = self.goDown()
      if moved:
        break
    # for side in sides:
    #     if side == 1 and moved is False:
    #         moved = self.goRight()
    #     if side == 2 and moved is False:
    #         moved = self.goLeft()
    #     if side == 3 and moved is False:
    #         moved = self.goUp()
    #     if side == 4 and moved is False:
    #         moved = self.goDown()
    #     if moved:
    #         break
    return moved

  def death(self):
    if self.age >= self.lifeLong:
      self.die()

  def narodziny(self):
    global animals
    global world
    global born
    rodzacy = True
    zapladniacz = True
    if self.ciaza == self.lenCiaza:
      # if random.randint(1, 100) > 50:
      #    rodzacy = True
      # else:
      #    zapladniacz = False
      a = animal(self.posX + 1, self.posY, zapladniacz=zapladniacz, rodzacy=rodzacy)
      born.add(a)
      # a = animal(self.posX - 1, self.posY, zapladniacz=zapladniacz, rodzacy=rodzacy)
      # born.add(a)
      # a = animal(self.posX , self.posY+1, zapladniacz=zapladniacz, rodzacy=rodzacy)
      # born.add(a)
      # a = animal(self.posX, self.posY-1, zapladniacz=zapladniacz, rodzacy=rodzacy)
      # born.add(a)

      world[a.posY][a.posX] = a
      # if not isinstance(world[self.posY][self.posX + 1], animal):
      #     rodzacy  = False
      #     zapladniacz = False
      #     if random.randint(1,100) > 50:
      #         rodzacy = True
      #     else:
      #         zapladniacz = False
      #     a = animal(self.posX+1, self.posY, zapladniacz=zapladniacz, rodzacy= rodzacy)
      #     born.add(a)
      #     world[a.posY][a.posX] = a
      # elif not isinstance(world[self.posY+1][self.posX], animal):
      #     rodzacy  = False
      #     zapladniacz = False
      #     if random.randint(1,100) > 50:
      #         rodzacy = True
      #     else:
      #         zapladniacz = False
      #     a = animal(self.posX, self.posY+1, zapladniacz=zapladniacz, rodzacy= rodzacy)
      #     born.add(a)
      #     world[a.posY][a.posX] = a
      # elif not isinstance(world[self.posY - 1][self.posX], animal):
      #     rodzacy = False
      #     zapladniacz = False
      #     if random.randint(1, 100) > 50:
      #         rodzacy = True
      #     else:
      #         zapladniacz = False
      #     a = animal(self.posX, self.posY - 1, zapladniacz=zapladniacz, rodzacy=rodzacy)
      #     born.add(a)
      #     world[a.posY-1][a.posX] = a
      # elif not isinstance(world[self.posY][self.posX-1], animal):
      #     rodzacy = False
      #     zapladniacz = False
      #     if random.randint(1, 100) > 50:
      #         rodzacy = True
      #     else:
      #         zapladniacz = False
      #     a = animal(self.posX-1, self.posY, zapladniacz=zapladniacz, rodzacy=rodzacy)
      #     born.add(a)
      #     world[a.posY][a.posX-1] = a
      self.ciaza = 0
      # print("---------------------- narodziny")

  def insemination(self):
    global world

    if self.rodzacy is True and self.ciaza == 0 and self.age <= self.lifeLong * 0.8:
      if random.randint(0, 100) > 0:
        if isinstance(world[self.posY - 1][self.posX], animal) and world[self.posY - 1][self.posX].zapladniacz:
          self.ciaza = 1
          return
        if isinstance(world[self.posY + 1][self.posX], animal) and world[self.posY + 1][self.posX].zapladniacz:
          self.ciaza = 1
          return
        if isinstance(world[self.posY][self.posX - 1], animal) and world[self.posY][self.posX - 1].zapladniacz:
          self.ciaza = 1
          return
        if isinstance(world[self.posY][self.posX + 1], animal) and world[self.posY][self.posX + 1].zapladniacz:
          self.ciaza = 1
          return

  def goLeft(self):
    global world
    if self.posX - 1 > 0 and world[self.posY][self.posX - 1] == None:
      world[self.posY][self.posX - 1] = self
      world[self.posY][self.posX] = None
      self.posX = self.posX - 1
      return True
    return False

  def goRight(self):
    global world
    if self.posX + 1 < 100 and world[self.posY][self.posX + 1] == None:
      world[self.posY][self.posX + 1] = self
      world[self.posY][self.posX] = None
      self.posX = self.posX + 1
      return True
    return False

  def goUp(self):
    global world
    if self.posY - 1 > 0 and world[self.posY - 1][self.posX] == None:
      world[self.posY - 1][self.posX] = self
      world[self.posY][self.posX] = None
      self.posY = self.posY - 1
      return True
    return False

  def goDown(self):
    global world
    if self.posY + 1 < 100 and world[self.posY + 1][self.posX] == None:
      world[self.posY + 1][self.posX] = self
      world[self.posY][self.posX] = None
      self.posY = self.posY + 1
      return True
    return False


for i in range(15):
  a = animal(random.randint(1, 15), random.randint(1, 15), zapladniacz=False)
  animals.add(a)
  world[a.posY][a.posX] = a
for i in range(15):
  a = animal(random.randint(1, 15), random.randint(1, 15), rodzacy=False)
  animals.add(a)
  world[a.posY][a.posX] = a
wait = 50
run = True
color = (255, 255, 255)
window.fill(color)
clock = pygame.time.Clock()
cProfile.run("""
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #window.fill(0)

    for a in animals:
        x = a.posX
        y = a.posY
        if a.go() == False:
            a.die()
    animals.difference_update(died)
    died.clear()
    animals.update(born)
    born.clear()

    window.fill(color)
    print(len(animals))
    wait -=1
    if wait <= 0:
        wait = 0
        for pix in animals:
            if pix.trup:
                print("trup")
                window.set_at((50 + j, 50 + i), color)
            window.set_at((50 + pix.posX, 50 + pix.posY), (255-(pix.age/pix.lifeLong)*255, 255-(pix.age/pix.lifeLong)*255, 255-(pix.age/pix.lifeLong)*255))

        pygame.display.update()

clock.tick(10)
""")
pygame.quit()
exit()
