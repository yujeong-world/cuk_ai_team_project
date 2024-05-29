import pygame
import time

class Agent:
    def __init__(self, environment, knowledge_base):
        self.environment = environment
        self.knowledge_base = knowledge_base
        self.position = (0, 0)
        self.environment.update_agent_position(self.position)
        self.has_gold = False
        self.alive = True
        self.path = []
        self.cost = 0
        self.arrows = 1

    def move(self, direction):
        if direction == "UP":
            new_position = (self.position[0] - 1, self.position[1])
        elif direction == "DOWN":
            new_position = (self.position[0] + 1, self.position[1])
        elif direction == "LEFT":
            new_position = (self.position[0], self.position[1] - 1)
        elif direction == "RIGHT":
            new_position = (self.position[0], self.position[1] + 1)
        else:
            return

        if self.environment.is_valid_position(new_position):
            self.position = new_position
            self.environment.update_agent_position(self.position)
            self.check_current_position()
            self.cost += 1

    def shoot_arrow(self, direction):
        if self.arrows > 0:
            self.arrows -= 1
            if self.environment.shoot_arrow(self.position, direction):
                self.cost += 1
                self.environment.draw()
                pygame.display.flip()
                print("wumpus dead")
                time.sleep(1)
                return True
        return False

    def check_current_position(self):
        cell = self.environment.get_cell(self.position)
        if 'WUMPUS' in cell and 'DEAD' not in cell:
            self.alive = False
        elif 'PIT' in cell:
            self.alive = False
        elif 'GOLD' in cell:
            self.has_gold = True

        percept = ""
        if 'BREEZE' in cell:
            percept += "BREEZE"
        if 'STENCH' in cell:
            percept += "STENCH"
        if 'GOLD' in cell:
            percept += "GOLD"
        self.knowledge_base.update(self.position, percept if percept else "SAFE")

    def is_alive(self):
        return self.alive

    def has_found_gold(self):
        return self.has_gold

    def find_gold(self):
        self.check_current_position()
        if self.knowledge_base.should_shoot_arrow(self.position):
            self.shoot_towards_wumpus()
        elif not self.path or not self.path:
            self.path = self.plan_path_to_gold()
        if self.path:
            step = self.path.pop(0)
            self.move(step)
        else:
            self.move_random()

    def shoot_towards_wumpus(self):
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        for direction in directions:
            x, y = self.position
            while self.environment.is_valid_position((x, y)):
                if 'WUMPUS' in self.environment.get_cell((x, y)):
                    if self.shoot_arrow(direction):
                        return
                if direction == "UP":
                    x -= 1
                elif direction == "DOWN":
                    x += 1
                elif direction == "LEFT":
                    y -= 1
                elif direction == "RIGHT":
                    y += 1

    def move_random(self):
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        for direction in directions:
            new_position = self.get_next_position(self.position, direction)
            if self.environment.is_valid_position(new_position) and not self.knowledge_base.is_visited(new_position):
                self.move(direction)
                return

    def plan_path_to_gold(self):
        from queue import PriorityQueue
        frontier = PriorityQueue()
        frontier.put((0, self.position))
        came_from = {}
        cost_so_far = {}
        came_from[self.position] = None
        cost_so_far[self.position] = 0

        while not frontier.empty():
            _, current = frontier.get()

            if self.environment.get_cell(current) == "GOLD":
                break

            for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
                next_pos = self.get_next_position(current, direction)
                if self.environment.is_valid_position(next_pos) and not self.knowledge_base.is_visited(next_pos) and self.knowledge_base.is_safe(next_pos):
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost
                        frontier.put((priority, next_pos))
                        came_from[next_pos] = current

        return self.reconstruct_path(came_from, current)

    def get_next_position(self, position, direction):
        x, y = position
        if direction == "UP":
            return (x - 1, y)
        elif direction == "DOWN":
            return (x + 1, y)
        elif direction == "LEFT":
            return (x, y - 1)
        elif direction == "RIGHT":
            return (x, y + 1)

    def reconstruct_path(self, came_from, current):
        path = []
        while current:
            next_current = came_from[current]
            if next_current:
                path.append(self.get_direction(next_current, current))
            current = next_current
        path.reverse()
        return path

    def get_direction(self, from_pos, to_pos):
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        if from_x > to_x:
            return "UP"
        elif from_x < to_x:
            return "DOWN"
        elif from_y > to_y:
            return "LEFT"
        elif from_y < to_y:
            return "RIGHT"
