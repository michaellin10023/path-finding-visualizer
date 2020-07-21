import os
import pygame
import pygame_menu
import pathfinding

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH = 600
surface = pygame.display.set_mode((WIDTH, WIDTH))
algo = 1 # A star: 1, BFS: 2, DFS: 3


def set_algo(selected, value):
    """
    Set the difficulty of the game.
    """
    print('Set difficulty to {} ({})'.format(selected[0], value))
    global algo
    algo = value


def start_the_game():
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.
    """
    print(algo)
    pathfinding.main(surface,WIDTH,algo)



menu = pygame_menu.Menu(height=WIDTH,
                        width=WIDTH,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome Pathfinding Visualizer')

menu.add_selector('Algorithm: ', [('A star', 1), ('BFS', 2)], onchange=set_algo)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()