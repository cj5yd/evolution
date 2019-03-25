import pygame

food_health = 30
wound_health = 20
cell_size = 10
length = 30
height = 20
win_length = length * cell_size + 200
win_height = height * cell_size + 200


class Bot:
    """creating of bot for simulation"""
    def __init__(self, npos):
        """initiating of bot"""
        self.number = len(bots)+1
        self.health = 100
        self.dna = 'abcbcba'
        self.pos = npos
        self.counter = 0
        fieldmap[self.pos[1]][self.pos[0]] = self.number

    def eat(self):
        self.health += food_health

    def move(self):
        new_pos = [self.pos[0]+1, self.pos[1]+1]
        fieldmap[self.pos[1]][self.pos[0]] = 0
        self.pos = new_pos
        fieldmap[self.pos[1]][self.pos[0]] = self.number

    def info(self):
        print('Bot №' + str(self.number) + ', health = ' + str(self.health) + '\n' + 'DNA: ' + self.dna + '\n'
              + 'Counter = ' + str(self.counter) + '\n' + 'Position = ' + str(self.pos) + '\n')

    def wound(self):
        self.health -= wound_health

    def act(self):
        print('---------------------------------------------------------------')
        self.info()
        if self.dna[self.counter] == 'a':
            self.eat()
        if self.dna[self.counter] == 'b':
            self.move()
        if self.dna[self.counter] == 'c':
            self.wound()

        self.info()
        print('---------------------------------------------------------------')
        self.counter += 1


class Field:
    def __init__(self, field_length, field_height):
        self.length = field_length
        self.height = field_height
        self.screen = pygame.display.set_mode((win_length, win_height))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('Evolution')

    def draw_field(self):
        for i in range(self.length + 1):
            x = (i + 1) * cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (x, cell_size), (x, (self.height+1) * cell_size))
        for j in range(self.height + 1):
            y = (j + 1) * cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (cell_size, y), ((self.length+1) * cell_size, y))
        pygame.draw.rect(self.screen, (192, 192, 192), (0, 0, (self.length + 2) * cell_size+1, cell_size))
        pygame.draw.rect(self.screen, (192, 192, 192),
                         (0, (self.height+1)*cell_size+1, (self.length + 2) * cell_size+1, cell_size))
        pygame.draw.rect(self.screen, (192, 192, 192), (0, cell_size, cell_size, self.height * cell_size+1))
        pygame.draw.rect(self.screen, (192, 192, 192),
                         ((self.length+1)*cell_size+1, cell_size, cell_size, self.height * cell_size+1))

    def show_field(self):
        self.screen.fill((255, 255, 255))
        self.draw_field()
        for j in range(len(fieldmap)):
            for i in range(len(fieldmap[j])):
                if fieldmap[j][i] >= 1:
                    x = (i+1)*10+1
                    y = (j+1)*10+1
                    pygame.draw.rect(self.screen, (0, 0, 255), (x, y, 9, 9))
        pygame.display.update()


# --------------------------------MAIN----------------------------
'''
clock = pygame.time.Clock()
clock.tick(60)
Добавить возможность создания нескольких полей и связать каждого бота со своим полем
Сделать чтобы изображение ботов накладывалось 



'''

pygame.init()

# на карте цифры 1 и больше - порядковые номера ботов.
# 0 - пустота, номера других объектов отрицательные: -1 - еда
fieldmap = [[0 for i in range(length)] for j in range(height)]
field = Field(length, height)
field.draw_field()
pos = [0, 0]

bots = []

bots.append(Bot(pos))
bots.append(Bot([1, 3]))


def field_click(pos):
    fieldpos = [int(pos[0] / cell_size)-1, int(pos[1] / cell_size)-1]
    if fieldmap[fieldpos[1]][fieldpos[0]] >= 1:
        numb_of_bot = fieldmap[fieldpos[1]][fieldpos[0]]-1
        bots[numb_of_bot].info()


while True:
    field.show_field()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                bots[0].move()
            elif i.key == pygame.K_RETURN:
                bots[1].move()
            field.show_field()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            field_click(pygame.mouse.get_pos())
