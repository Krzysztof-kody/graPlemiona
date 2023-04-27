import pygame
import random

pygame.init()
window = pygame.display.set_mode((400, 400))
world = [[None] * 300 for i in range(300)]
animals = set()
died = set()
born = set()


class Animal:
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

    def __init__(self, posx=0, posy=0, zapladniacz=True, rodzacy=True):
        self.color = (255, 255, 255)
        self.life = 10
        self.age = 0
        self.zapladniacz = zapladniacz
        self.rodzacy = rodzacy
        self.alive = True
        self.posX = posx
        self.posY = posy
        self.ciaza = 0
        self.lenCiaza = 50
        self.lifeLong = 1000
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
            a = Animal(self.posX + 1, self.posY, zapladniacz=zapladniacz, rodzacy=rodzacy)
            born.add(a)
            # a = Animal(self.posX - 1, self.posY, zapladniacz=zapladniacz, rodzacy=rodzacy)
            # born.add(a)
            # a = Animal(self.posX , self.posY+1, zapladniacz=zapladniacz, rodzacy=rodzacy)
            # born.add(a)
            # a = Animal(self.posX, self.posY-1, zapladniacz=zapladniacz, rodzacy=rodzacy)
            # born.add(a)

            world[a.posY][a.posX] = a
            # if not isinstance(world[self.posY][self.posX + 1], Animal):
            #     rodzacy  = False
            #     zapladniacz = False
            #     if random.randint(1,100) > 50:
            #         rodzacy = True
            #     else:
            #         zapladniacz = False
            #     a = Animal(self.posX+1, self.posY, zapladniacz=zapladniacz, rodzacy= rodzacy)
            #     born.add(a)
            #     world[a.posY][a.posX] = a
            # elif not isinstance(world[self.posY+1][self.posX], Animal):
            #     rodzacy  = False
            #     zapladniacz = False
            #     if random.randint(1,100) > 50:
            #         rodzacy = True
            #     else:
            #         zapladniacz = False
            #     a = Animal(self.posX, self.posY+1, zapladniacz=zapladniacz, rodzacy= rodzacy)
            #     born.add(a)
            #     world[a.posY][a.posX] = a
            # elif not isinstance(world[self.posY - 1][self.posX], Animal):
            #     rodzacy = False
            #     zapladniacz = False
            #     if random.randint(1, 100) > 50:
            #         rodzacy = True
            #     else:
            #         zapladniacz = False
            #     a = Animal(self.posX, self.posY - 1, zapladniacz=zapladniacz, rodzacy=rodzacy)
            #     born.add(a)
            #     world[a.posY-1][a.posX] = a
            # elif not isinstance(world[self.posY][self.posX-1], Animal):
            #     rodzacy = False
            #     zapladniacz = False
            #     if random.randint(1, 100) > 50:
            #         rodzacy = True
            #     else:
            #         zapladniacz = False
            #     a = Animal(self.posX-1, self.posY, zapladniacz=zapladniacz, rodzacy=rodzacy)
            #     born.add(a)
            #     world[a.posY][a.posX-1] = a
            self.ciaza = 0
            # print("---------------------- narodziny")

    def insemination(self):
        global world

        if self.rodzacy is True and self.ciaza == 0 and self.age <= self.lifeLong * 0.8:
            if random.randint(0, 100) > 0:
                if isinstance(world[self.posY - 1][self.posX], Animal) and world[self.posY - 1][self.posX].zapladniacz:
                    self.ciaza = 1
                    return
                if isinstance(world[self.posY + 1][self.posX], Animal) and world[self.posY + 1][self.posX].zapladniacz:
                    self.ciaza = 1
                    return
                if isinstance(world[self.posY][self.posX - 1], Animal) and world[self.posY][self.posX - 1].zapladniacz:
                    self.ciaza = 1
                    return
                if isinstance(world[self.posY][self.posX + 1], Animal) and world[self.posY][self.posX + 1].zapladniacz:
                    self.ciaza = 1
                    return

    def goLeft(self):
        global world
        if self.posX - 1 > 0 and world[self.posY][self.posX - 1] is None:
            world[self.posY][self.posX - 1] = self
            world[self.posY][self.posX] = None
            self.posX -= 1
            return True
        return False

    def goRight(self):
        global world
        if self.posX + 1 < 100 and world[self.posY][self.posX + 1] is None:
            world[self.posY][self.posX + 1] = self
            world[self.posY][self.posX] = None
            self.posX += 1
            return True
        return False

    def goUp(self):
        global world
        if self.posY - 1 > 0 and world[self.posY - 1][self.posX] is None:
            world[self.posY - 1][self.posX] = self
            world[self.posY][self.posX] = None
            self.posY = self.posY - 1
            return True
        return False

    def goDown(self):
        global world
        if self.posY + 1 < 100 and world[self.posY + 1][self.posX] is None:
            world[self.posY + 1][self.posX] = self
            world[self.posY][self.posX] = None
            self.posY = self.posY + 1
            return True
        return False


for i in range(15):
    a = Animal(random.randint(1, 15), random.randint(1, 15), zapladniacz=False)
    animals.add(a)
    world[a.posY][a.posX] = a
for i in range(15):
    a = Animal(random.randint(1, 15), random.randint(1, 15), rodzacy=False)
    animals.add(a)
    world[a.posY][a.posX] = a
wait = 50
run = True
color = (255, 255, 255)
window.fill(color)
clock = pygame.time.Clock()

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for a in animals:
        if not a.go():
            a.die()
    animals.difference_update(died)
    died.clear()
    animals.update(born)
    born.clear()

    window.fill(color)
    print(len(animals))
    for pix in animals:
        # window.set_at((50 + pix.posX, 50 + pix.posY), (255-(pix.age/pix.lifeLong)*255, 255-(pix.age/pix.lifeLong)*255, 255-(pix.age/pix.lifeLong)*255))
        pygame.draw.rect(window, (
            255 - int((pix.age / pix.lifeLong) * 255),
            255 - int((pix.age / pix.lifeLong) * 255),
            255 - int((pix.age / pix.lifeLong) * 255)),
            (50 + pix.posX * 3, 50 + pix.posY * 3, 3, 3))
    pygame.display.update()

    clock.tick(10)

pygame.quit()
exit()
