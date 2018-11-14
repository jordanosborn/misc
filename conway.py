import pygame, functools, itertools
from typing import Set, Tuple
from random import randint
from time import sleep


def main(state: Set[Tuple[int, int]], width: int = 500, height: int = 500, max_x: int = 100, max_y: int = 100):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    size_x, size_y = width // max_x, height // max_y
    is_paused = True

    def conway() -> Set[Tuple[int, int]]:
        positions = list(itertools.product(range(max_x), range(max_y)))
        nonlocal state
        yield state
        while len(state) != 0:
            states_to_add, states_to_remove = set(), set()
            for x, y in positions:
                alive = (x, y) in state
                neighbours = functools.reduce(lambda acc, v: acc + (1 if v in state else 0), [
                    (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                    (x - 1, y), (x + 1, y),
                    (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)], 0)
                if alive and neighbours in [2, 3] or not alive and neighbours == 3:
                    states_to_add.add((x, y))
                elif alive and neighbours < 2 or neighbours > 3:
                    states_to_remove.add((x, y))
            state = state.difference(states_to_remove).union(states_to_add)
            yield state

    def input_loop():
        nonlocal is_paused, state
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: is_paused = not is_paused
            elif event.type == pygame.MOUSEBUTTONUP and is_paused:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    state.add((mouse_x // size_x, mouse_y // size_y))
                else:
                    try: state.remove((mouse_x // size_x, mouse_y // size_y))
                    except ValueError: pass

    def game_loop():
        nonlocal state
        for s in conway():
            while is_paused:
                screen.fill((255, 255, 255))
                for x, y in state: pygame.draw.rect(screen, (0, 0, 0), [x * size_x, y * size_y, size_x, size_y])
                pygame.display.flip()
                sleep(0.5)
            screen.fill((255, 255, 255))
            for x, y in s: pygame.draw.rect(screen, (0, 0, 0), [x * size_x, y * size_y, size_x, size_y])
            pygame.display.flip()
            sleep(0.1)

    t1 = pygame.threads.Thread(target=input_loop, daemon=True)
    t2 = pygame.threads.Thread(target=game_loop, daemon=True)
    t1.start(); t2.start()
    t2.join(); t1.join()

# Do something with walls / add more rules
if __name__ == "__main__":
    width, height, max_x, max_y = 1000, 1000, 100, 100
    random_state = {(x, y) for x, y in itertools.product(range(max_x), range(max_y)) if randint(0, 1)}
    main(random_state, width, height, max_x, max_y)
