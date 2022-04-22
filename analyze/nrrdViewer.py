import pygame, numpy as np
import tkinter, tkinter.filedialog
import argparse, pickle

patients_dir="/nv/vol141/phys_nrf/Emery/dataset/"
parser = argparse.ArgumentParser()
parser.add_argument('patient', type=str, help="Patient's Initials")
args=parser.parse_args()

with open(patients_dir+args.patient+"/Pre/Raw_CT.pickle",'rb') as file:
    data=pickle.load(file)
img=data['ct_img']


class Slider():
    def __init__(self, name, val, maxi, mini, xpos, ypos, screen):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = xpos  # x-location on screen
        self.ypos = ypos
        self.surf = pygame.surface.Surface((1000, 50))  #Background surface
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.screen = screen

        self.maxLen=250

        self.txt_surf = pygame.font.SysFont("Verdana", 12).render(name, 1, (0, 0, 0))
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        self.surf.fill((100, 100, 115))
        pygame.draw.rect(self.surf, (255, 255, 255), [10, 30, self.maxLen, 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill((1, 1, 1))
        self.button_surf.set_colorkey((1, 1, 1))
        pygame.draw.circle(self.button_surf, (0, 0, 0), (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, (200, 100, 250), (10, 10), 4, 0)

    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*self.maxLen), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        self.screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / self.maxLen * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi






sliders = []







class Viewer:
    def __init__(self, update_func1, update_func2, update_func3):
        self.display_size = (1000,700)
        self.update_func1 = update_func1
        self.update_func2 = update_func2
        self.update_func3 = update_func3
        pygame.init()
        self.display = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption("Scan Viewer")

        global sliders
        self.sliders = sliders
        for I in [Slider("View 1", 10, 15, 1, 40, 300, self.display),
                        Slider("View 3", 10, 15, 1, 310, 300, self.display),
                        Slider("View 2", 10, 15, 1, 310, 150, self.display)]:
            sliders.append(I)
    

    
    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                #Move sliders
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for s in self.sliders:
                        if s.button_rect.collidepoint(pos):
                            s.hit = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    for s in self.sliders:
                        s.hit = False

            self.display.fill([100,100,115])

            Z = self.update_func1()
            anterior = pygame.surfarray.make_surface(Z)
            anterior = pygame.transform.scale(anterior, (250,250))
            self.display.blit(anterior, (50, 50))

            Z2 = self.update_func2()
            surf2 = pygame.surfarray.make_surface(Z2)
            surf2 = pygame.transform.scale(surf2, (250,100))
            self.display.blit(surf2, (320, 50))

            Z3 = self.update_func3()
            surf3 = pygame.surfarray.make_surface(Z3)
            surf3 = pygame.transform.scale(surf3, (250,100))
            self.display.blit(surf3, (320, 200))


            #Update sliders
            for s in self.sliders:
                if s.hit:
                    s.move()
            for s in self.sliders:   
                s.draw()
            
            

            pygame.display.update()

        pygame.quit()


def update1():
    global img
    global sliders
    m=img.shape[2]-1
    print(sliders[0].val/15*512)
    return img[:,:,min(m, int(sliders[0].val/15*512))]

def update2():
    global img
    global sliders
    m=img.shape[1]-1
    print(sliders[1].val/15*512)
    return img[:,min(m, int(sliders[1].val/15*512)),:]

def update3():
    global img
    global sliders
    m=img.shape[0]-1
    print(sliders[2].val/15*512)
    return img[min(m, int(sliders[2].val/15*512)),:,:]

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name



v=Viewer(update1,update2,update3)
v.start()
