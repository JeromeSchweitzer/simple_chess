import pygame
import chess


pygame.init()

def render(screen, squares, newsquare, oldsquare, board):
    # Fill the background with white
    screen.fill((255, 255, 255))
    for square in squares:
        if square.left % 200 ^ square.top % 200:
            pygame.draw.rect(screen, blue, square)
        else:
            pygame.draw.rect(screen, white, square)
    if newsquare:
        pygame.draw.rect(screen, green, newsquare)
    if oldsquare:
        pygame.draw.rect(screen, darkgreen, oldsquare)
    
    ranks = ['1','2','3','4','5','6','7','8']
    files = ['A','B','C','D','E','F','G','H']
    
    for r in range(8):
        for f in range(8):
            coord = files[f] + ranks[r]
    # Flip the display
    im = pygame.image.load('./pieces/bbishop.png').convert_alpha()
    screen.blit(im, squares[20])
    pygame.display.flip()


white = (255,255,255)
blue = (66, 135, 245)
green = (96, 240, 132)
darkgreen = (54, 186, 58)


screen = pygame.display.set_mode([800, 800])

squares = []
for r in range (0,900,100):
    for c in range (0,900,100):
        squares.append(pygame.Rect(r,c,100,100))


running = True
board = chess.Board()
render(screen, squares, False, False, board)
oldsquare = False
newsquare = False
while running:
    # Did the user click the window close button?
    #pos = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            #oldpos = pos
            pos = pygame.mouse.get_pos()
            oldsquare = newsquare
            for square in squares:
                if pos and pos[0] >= square.left and pos[0] < square.right and pos[1] >= square.top and pos[1] < square.bottom:
                    newsquare = square
                    # print(square.left)
                    # print(square.right)
            if newsquare == oldsquare:
                newsquare = False
                oldsquare = False
            render(screen, squares, newsquare, oldsquare, board)
            # print(pos)

    

# Done! Time to quit.
pygame.quit()