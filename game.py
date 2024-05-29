import pygame
from agent import Agent
from environment import Environment
from knowledge_base import KnowledgeBase

class Game:
    def __init__(self, size, screen, character, wumpus, gold, pitch, arrow):
        self.environment = Environment(size, screen, character, wumpus, gold, pitch, arrow)
        self.knowledge_base = KnowledgeBase(size)
        self.agent = Agent(self.environment, self.knowledge_base)
        self.game_over = False

    def play_step(self):
        self.agent.find_gold()
        if not self.agent.is_alive() or self.agent.has_found_gold():
            self.game_over = True

    def display_environment(self):
        for row in self.environment.grid:
            print(' '.join(row))

    def draw(self):
        self.environment.draw()
        pygame.display.flip()
