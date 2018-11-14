import pygame, functools, itertools
from typing import Set, Tuple
from random import randint


def conway(state: Set[Tuple[int, int]], max_x: int = 100, max_y: int = 100) -> Set[Tuple[int, int]]:
    positions = list(itertools.product(range(max_x), range(max_y)))
    yield state
    while len(state) != 0:
        for x, y in positions:
            alive = False
            if (x, y) in state:
                state.remove((x,y))
                alive = True
            neighbours = functools.reduce(lambda acc, v: acc + (1 if v in state else 0), [
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y),                 (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)], 0)
            if alive and neighbours in [2, 3] or not alive and neighbours == 3: state.add((x, y))
        yield state


def main(initial_state: Set[Tuple[int, int]], width=500, height=500, max_x=100, max_y=100) -> None:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    size_x, size_y = width // max_x, height // max_y

    def input_loop():
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.quit()

    def game_loop():
        for s in conway(initial_state, max_x, max_y):
            screen.fill((255, 255, 255))
            for x, y in s: pygame.draw.rect(screen, (0, 0, 0), [x * size_x, y * size_y, size_x, size_y])
            pygame.display.flip()

    t1 = pygame.threads.Thread(target=input_loop, daemon=True)
    t2 = pygame.threads.Thread(target=game_loop, daemon=True)
    t1.start(); t2.start()
    t2.join()
    pygame.quit()


if __name__ == "__main__":
    width, height, max_x, max_y = 1000, 1000, 500, 500
    s = {(x, y) for x, y in itertools.product(range(max_x), range(max_y)) if randint(0, 1)}
    main(s, width, height, max_x, max_y)
