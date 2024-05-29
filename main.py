import pygame
import sys
from game import Game
import time

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wumpus Game")

character = pygame.image.load("./images/character.jpg")
wumpus = pygame.image.load("./images/wumpus.jpg")
gold = pygame.image.load("./images/gold.jpg")
pitch = pygame.image.load("./images/pitch.jpg")
arrow = pygame.image.load("./images/arrow.jpg")

character = pygame.transform.scale(character, (50, 50))
wumpus = pygame.transform.scale(wumpus, (50, 50))
gold = pygame.transform.scale(gold, (50, 50))
pitch = pygame.transform.scale(pitch, (50, 50))
arrow = pygame.transform.scale(arrow, (50, 50))

def main():
    game = Game(4, screen, character, wumpus, gold, pitch, arrow)
    clock = pygame.time.Clock()

    start_time = time.time()
    while time.time() - start_time < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        game.play_step()
        game.draw()
        pygame.display.flip()
        clock.tick(1)

    if game.agent.has_found_gold():
        print("Congratulations! The agent has found the gold and won the game!")
    else:
        print("The agent has lost the game.")
    print(f"Total cost: {game.agent.cost}")

if __name__ == "__main__":
    main()
