import pygame
import random

class Sprite:
    def __init__(self, img: pygame.image, x: int, y: int):
        self.img = img
        self.rect = pygame.Rect(x,y,img.get_width(),img.get_height())

    def move(self, new_x: int, new_y: int):
        size = (self.rect.width, self.rect.height)
        self.rect.update(new_x,new_y,*size)

    def draw(self, surface: pygame.Surface):
        position = (self.rect.left, self.rect.top)
        surface.blit(self.img, position)

class BOX(Sprite):
    def __init__(self, x: int, y: int):
        img = pygame.Surface((100,100))
        self.colour = [85 * random.randint(1,2) for x in range(3)]
        img.fill(self.colour)
        super().__init__(img, x*100, y*100)

class ListBox:
    def __init__(self, boxes: list[BOX]):
        self.boxes = [[box,True] for box in boxes]
        self.width = 7
        self.height = 5
        self.cur_scroll = 0
        self.max_scroll = 0
        self.set_max_scroll()
        self.box_size = (100,100)
        self.update_box_positions()

    def set_max_scroll(self):
        visible = sum([1 for _, valid in self.boxes if valid])
        if(visible <= self.width * self.height):
            self.max_scroll = 0
            return
        rows = (visible - 1)// self.width + 1
        self.max_scroll = rows - self.height

    def draw_contents(self, screen: pygame.Surface):
        for box, validity in self.boxes:
            if(validity): box.draw(screen)

    def toggle_validity(self, code: list[int]):
        for x, box_data in enumerate(self.boxes):
            box, _ = box_data
            if(box.colour == code):
                self.boxes[x][1] = not self.boxes[x][1]
        self.update_box_positions()

    def sort(self, attribute: int, ascending: bool):
        #INSERTION SORT
        num_sorted = 0
        while num_sorted < len(self.boxes):
            current = num_sorted
            my_colour = self.boxes[current][0].colour[attribute]
            for x in range(num_sorted-1,-1,-1):
                old_colour = self.boxes[x][0].colour[attribute]
                if(my_colour < old_colour):
                    self.boxes[current], self.boxes[x] = self.boxes[x], self.boxes[current]
                    current -= 1
                else:
                    break
            num_sorted += 1
        if(not ascending):
            self.boxes = self.boxes[::-1]
        self.update_box_positions()

    def update_box_positions(self):
        self.set_max_scroll()
        self.update_scroll(0) #Will scroll back up as necessary

        x,y = 0,-self.box_size[1] * self.cur_scroll
        width = self.box_size[0] * self.width
        for box, validity in self.boxes:
            if(not validity): continue
            box.move(x,y)
            x += self.box_size[0]
            if(x == width):
                x = 0
                y += self.box_size[1]

    def update_scroll(self, amount: int):
        self.cur_scroll += amount
        self.cur_scroll = min(self.max_scroll, max(0, self.cur_scroll))

pygame.init()
screen = pygame.display.set_mode((768,512))
clock = pygame.time.Clock()

boxes = [BOX(z%3,z//3) for z in range(35*5)]
listbox = ListBox(boxes)
running = True
counter = 0
down_flag = up_flag = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if(keys[pygame.K_DOWN]):
        down_flag = True
    if(keys[pygame.K_UP]):
        up_flag = True
    if(counter % 10 == 0):
        shift = 0
        if(down_flag): shift += 1
        if(up_flag): shift -= 1
        if(shift != 0):
            listbox.update_scroll(shift)
            listbox.update_box_positions()
        down_flag = up_flag = False

    #Testing
    if(counter % 60 == 0):
        listbox.sort(((counter // 60)-1)%3, True)#random.randint(0,1)==1)
    if(counter % 120 == 0):
        listbox.toggle_validity([random.randint(1,2)*85 for x in range(3)])
    if(counter == 360): counter = 0
    counter += 1
    #Testing
    listbox.draw_contents(screen)

    pygame.display.flip()
    screen.fill((0,0,0))
    clock.tick(60)
    