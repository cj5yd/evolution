import pygame
import random

food_health = 30
wound_health = 20
cell_size = 10
length = 40
height = 30
win_length = length * cell_size + 200
win_height = height * cell_size + 200
food_quantity = 40
poison_quantity = 20
bots_quantity = 20
walls_quantity = 20

# значения для конвертации позиции относительно бота в абсолютные и обратно
# Для бота, номер строки которого делится на 2 без остатка (нумерация строк начинается с 0)
convert_pos1 = {
    0: [-1, 0],
    1: [-1, 1],
    2: [0, 1],
    3: [1, 1],
    4: [1, 0],
    5: [0, -1],
    6: [-2, -1],
    7: [-2, 0],
    8: [-2, 1],
    9: [-1, 2],
    10: [0, 2],
    11: [1, 2],
    12: [2, 1],
    13: [2, 0],
    14: [2, -1],
    15: [1, -1],
    16: [0, -2],
    17: [-1, -1]}
# Для бота, номер строки которого делится на 2 с остатком (нумерация строк начинается с 0)
convert_pos2 = {
    0: [-1, -1],
    1: [-1, 0],
    2: [0, 1],
    3: [1, 0],
    4: [1, -1],
    5: [0, -1],
    6: [-2, -1],
    7: [-2, 0],
    8: [-2, 1],
    9: [-1, 1],
    10: [0, 2],
    11: [1, 1],
    12: [2, 1],
    13: [2, 0],
    14: [2, -1],
    15: [1, -2],
    16: [0, -2],
    17: [-1, -2]
    }


class Bot:
    """creating of bot for simulation"""
    def __init__(self, npos):
        """initiating of bot"""
        self.number = len(bots)+1
        self.health = 100
        self.pos = npos
        self.view = [0 for i in range(18)]
        fieldmap[self.pos[0]][self.pos[1]] = self.number
        self.dna = {
            # 1 - любой другой бот
            1: [random.random() for i in range(12)],
            0: [random.random() for i in range(12)],
            -1: [random.random() for i in range(12)],
            -2: [random.random() for i in range(12)],
            -3: [random.random() for i in range(12)]}

    def rel_to_abs_pos(self, rel_pos):
        if self.pos[0] % 2 == 0:
            abs_pos = [self.pos[0] + convert_pos1[rel_pos][0], self.pos[1] + convert_pos1[rel_pos][1]]
        else:
            abs_pos = [self.pos[0] + convert_pos2[rel_pos][0], self.pos[1] + convert_pos2[rel_pos][1]]
        return abs_pos

    def abs_to_rel_pos(self, abs_pos):
        if self.pos[0] % 2 == 0:
            for key in convert_pos1:
                if convert_pos1[key] == abs_pos:
                    return key
        else:
            for key in convert_pos2:
                if convert_pos2[key] == abs_pos:
                    return key

    def move(self):
        aim = 4
        new_pos = self.rel_to_abs_pos(aim)
        if fieldmap[new_pos[0]][new_pos[1]] != 0:
            print('The place is not empty')
            return
        fieldmap[self.pos[0]][self.pos[1]] = 0
        self.pos = new_pos
        fieldmap[self.pos[0]][self.pos[1]] = self.number

    def scan(self):
        for i in range(18):
            self.view[i] = fieldmap[self.rel_to_abs_pos(i)[0]][self.rel_to_abs_pos(i)[1]]
        for i in range(len(self.view)):
            if self.view[i] != 0:
                print(str(self.view[i]) + ' ' + str(i))

    def info(self):
        print('Bot №' + str(self.number) + ', health = ' + str(self.health) + '\n'
              + '\n' + 'Position = ' + str(self.pos) + '\n')


class Field:
    def __init__(self):
        self.screen = pygame.display.set_mode((win_length, win_height))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('Evolution')

    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        for j in range(len(fieldmap)):
            for i in range(len(fieldmap[j])):
                y = j * 10
                if j % 2 == 0:
                    x = i * 10 + 5
                else:
                    x = i * 10
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 11, 11), 1)
        pygame.display.update()

    def show_field(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        for j in range(len(fieldmap)):
            for i in range(len(fieldmap[j])):
                y = j * 10 + 1
                if j % 2 == 0:
                    x = i * 10 + 6
                else:
                    x = i * 10 + 1
                if fieldmap[j][i] >= 1:         # bot
                    pygame.draw.rect(self.screen, (0, 0, 255), (x, y, 9, 9))
                elif fieldmap[j][i] == -1:      # wall
                    pygame.draw.rect(self.screen, (192, 192, 192), (x, y, 9, 9))
                elif fieldmap[j][i] == -2:      # food
                    pygame.draw.rect(self.screen, (0, 255, 0), (x, y, 9, 9))
                elif fieldmap[j][i] == -3:      # poison
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 9, 9))
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
# 0 - пустота, номера других объектов отрицательные: -1 - стена, -2 - еда, -3 - яд


def create_fieldmap():
    fieldmap = []
    for j in range(height + 4):
        if j % 2 == 0:
            string = [0 for i in range(length + 3)]
        else:
            string = [0 for i in range(length + 4)]
        fieldmap.append(string)

    for j in range(len(fieldmap)):
        for i in range(len(fieldmap[j])):
            if i == 0:
                fieldmap[j][i] = -1
            if i == 1:
                fieldmap[j][i] = -1
            if i == len(fieldmap[j]) - 1:
                fieldmap[j][i] = -1
            if i == len(fieldmap[j]) - 2:
                fieldmap[j][i] = -1
            if j == 0:
                fieldmap[j][i] = -1
            if j == 1:
                fieldmap[j][i] = -1
            if j == len(fieldmap) - 1:
                fieldmap[j][i] = -1
            if j == len(fieldmap) - 2:
                fieldmap[j][i] = -1
    return fieldmap

fieldmap = create_fieldmap()
field = Field()
bots = []

# Создаем объекты на поле
# Создаем рандомные стены
for i in range(walls_quantity):
    pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    while fieldmap[pos[0]][pos[1]] != 0:
        pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    fieldmap[pos[0]][pos[1]] = -1

# Создаем еду
for i in range(food_quantity):
    pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    while fieldmap[pos[0]][pos[1]] != 0:
        pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    fieldmap[pos[0]][pos[1]] = -2

# Создаем яд
for i in range(poison_quantity):
    pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    while fieldmap[pos[0]][pos[1]] != 0:
        pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    fieldmap[pos[0]][pos[1]] = -3

# Создаем ботов
for i in range(bots_quantity):
    pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    while fieldmap[pos[0]][pos[1]] != 0:
        pos = [random.randint(0, height) + 2, random.randint(0, length) + 2]
    bots.append(Bot(pos))


def field_click(click_pos):
    if int(click_pos[1] / cell_size) % 2 == 0:
        fieldpos = [int(click_pos[1] / cell_size), int((click_pos[0] - 5) / cell_size)]
    else:
        fieldpos = [int(click_pos[1] / cell_size), int(click_pos[0] / cell_size)]
    try:
        if fieldmap[fieldpos[0]][fieldpos[1]] >= 1:
            numb_of_bot = fieldmap[fieldpos[0]][fieldpos[1]]-1
            bots[numb_of_bot].info()
        if fieldmap[fieldpos[0]][fieldpos[1]] == 0:
            print("There is empty")
        if fieldmap[fieldpos[0]][fieldpos[1]] == -1:
            print('This is a wall')
        if fieldmap[fieldpos[0]][fieldpos[1]] == -2:
            print('This is a food')
        if fieldmap[fieldpos[0]][fieldpos[1]] == -3:
            print('This is a poison')
    except IndexError:
        print("Out of the field")


while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                bots[0].move()
                bots[0].scan()
            elif i.key == pygame.K_RETURN:
                bots[1].move()
                bots[1].scan()
            field.show_field()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                field_click(pygame.mouse.get_pos())
        field.show_field()

