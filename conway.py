import pygame
from pygame.locals import *
from typing import Set, Tuple
from itertools import product
from functools import reduce
from time import sleep


def conway(state: Set[Tuple[int, int]], max_x: int = 10, max_y: int = 10) -> Set[Tuple[int, int]]:
    yield state
    while len(state) != 0:
        #refactor this into array index scheme or nparray
        for x, y in product(range(max_x), range(max_y)):
            alive = False
            if (x, y) in state:
                state.remove((x,y))
                alive = True
            xs, ys = x - 1, y -1
            neighbours = reduce(lambda acc, x: acc + (1 if x in state else 0), [
                (xs, ys),
                (xs, ys + 1),
                (xs, ys + 2),
                (xs + 1, ys),
                (xs + 1, ys + 2),
                (xs + 2, ys),
                (xs + 2, ys + 1),
                (xs + 2, ys + 2)
            ], 0)
            # rules
            if alive and neighbours in [2, 3] or not alive and neighbours == 3:
                state.add((x,y))
        yield state
    return None


def main(initial_state: Set[Tuple[int, int]], width=500, height=500, max_x=100, max_y=100) -> None:
    pygame.init()
    assert width > 0 and height > 0 and max_x > 0 and max_y > 0
    if len(list(filter(lambda s: s[0] < 0 or s[0] >= max_x or s[1] < 0 or s[1] >= max_y, initial_state))) != 0:
        raise ValueError(f"max_x: {max_x-1} max_y: {max_y-1} given: {initial_state}")
    size_x = width // max_x
    size_y = height // max_y

    screen = pygame.display.set_mode((width, height))

    def inp():
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    pygame.quit()

    def game():
        for i, s in enumerate(conway(initial_state, max_x, max_y)):
            screen.fill((255, 255, 255))
            for x, y in s:
                pygame.draw.rect(screen, (0, 0, 0), [x * size_x, y * size_y, size_x, size_y])
            pygame.display.flip()

    t1 = pygame.threads.Thread(target=inp, daemon=True)
    t2 = pygame.threads.Thread(target=game, daemon=True)
    t1.start()
    t2.start()
    t2.join()
    pygame.quit()

from random import randint
if __name__ == "__main__":
    width, height = 1000, 1000
    max_x, max_y = 500, 500
    s = set()
    for x, y in product(range(max_x), range(max_y)):
        if randint(0, 1):
            s.add((x, y))
    main(s, width, height, max_x, max_y)
