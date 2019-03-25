import pygame


food_health = 30
wound_health = 20
cell_size = 10
length = 15
height = 10
win_length = length * cell_size + 200
win_height = height * cell_size + 200


class Bot:
    """creating of bot for simulation"""
    def __init__(self, npos):
        """initiating of bot"""
        self.number = len(bots)+1
        self.health = 100
        self.pos = npos
        self.counter = 0
        fieldmap[self.pos[0]][self.pos[1]] = self.number

    def move(self):
        new_pos = [self.pos[0]+1, self.pos[1]+1]
        if fieldmap[new_pos[0]][new_pos[1]] != 0:
            print('The place is not empty')
            return
        fieldmap[self.pos[0]][self.pos[1]] = 0
        self.pos = new_pos
        fieldmap[self.pos[0]][self.pos[1]] = self.number

    def info(self):
        print('Bot №' + str(self.number) + ', health = ' + str(self.health) + '\n'  + 'Counter = ' + str(self.counter)
              + '\n' + 'Position = ' + str(self.pos) + '\n')


class Field:
    def __init__(self, field_length, field_height):
        self.length = field_length
        self.height = field_height
        self.screen = pygame.display.set_mode((win_length, win_height))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('Evolution')

    def draw_field(self):
        for i in range(self.length + 5):
            x = i * cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, (self.height+4) * cell_size))
        for j in range(self.height + 5):
            y = j * cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), ((self.length+4) * cell_size, y))

    def show_field(self):
        self.screen.fill((255, 255, 255))
        self.draw_field()
        for j in range(len(fieldmap)):
            for i in range(len(fieldmap[j])):
                x = i * 10 + 1
                y = j * 10 + 1
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
    fieldmap = [[0 for i in range(length+4)] for j in range(height+4)]
    # делаем стены по краям поля
    for i in range(length+4):
        fieldmap[0][i] = -1
        fieldmap[1][i] = -1
        fieldmap[height + 2][i] = -1
        fieldmap[height + 3][i] = -1
    for j in range(height+4):
        fieldmap[j][0] = -1
        fieldmap[j][1] = -1
        fieldmap[j][length + 2] = -1
        fieldmap[j][length + 3] = -1
    return fieldmap


fieldmap = create_fieldmap()
field = Field(length, height)
field.draw_field()
pos = [5, 4]

bots = []

bots.append(Bot(pos))
bots.append(Bot([3, 4]))


def field_click(click_pos):
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
