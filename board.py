import pygame


pygame.init()

def render(screen, squares, pos):
    # Fill the background with white
    screen.fill((255, 255, 255))
    for square in squares:
        if pos and pos[0] >= square.left and pos[0] < square.right and pos[1] >= square.top and pos[1] < square.bottom:
            pygame.draw.rect(screen, green, square)
        elif square.left % 200 ^ square.top % 200:
            pygame.draw.rect(screen, blue, square)
        else:
            pygame.draw.rect(screen, white, square)

    # Flip the display
    pygame.display.flip()


white = (255,255,255)
blue = (66, 135, 245)
green = (96, 240, 132)


screen = pygame.display.set_mode([800, 800])

squares = []
for r in range (0,900,100):
    for c in range (0,900,100):
        squares.append(pygame.Rect(r,c,100,100))


running = True
render(screen, squares, False)
while running:
    # Did the user click the window close button?
    #pos = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            render(screen, squares, pos)
            # print(pos)
    

# Done! Time to quit.
pygame.quit()