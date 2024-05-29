import random

class Environment:
    def __init__(self, size, screen, character, wumpus, gold, pitch, arrow):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.screen = screen
        self.character = character
        self.wumpus = wumpus
        self.gold = gold
        self.pitch = pitch
        self.arrow = arrow
        self.agent = None
        self.place_objects()

    def place_objects(self):
        self.place_object('WUMPUS')
        self.place_object('GOLD')
        for _ in range(self.size // 2):
            self.place_object('PIT')
        self.add_breeze_and_stench()

    def place_object(self, obj):
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[x][y] == '' and (x, y) != (0, 0):
                self.grid[x][y] = obj
                break

    def add_breeze_and_stench(self):
        for x in range(self.size):
            for y in range(self.size):
                if 'PIT' in self.grid[x][y]:
                    self.add_effect(x, y, 'BREEZE')
                if 'WUMPUS' in self.grid[x][y]:
                    self.add_effect(x, y, 'STENCH')

    def add_effect(self, x, y, effect):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if effect not in self.grid[nx][ny]:
                    self.grid[nx][ny] += effect

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def get_cell(self, position):
        x, y = position
        return self.grid[x][y]

    def shoot_arrow(self, position, direction):
        x, y = position
        while self.is_valid_position((x, y)):
            if direction == "UP":
                x -= 1
            elif direction == "DOWN":
                x += 1
            elif direction == "LEFT":
                y -= 1
            elif direction == "RIGHT":
                y += 1
            cell = self.get_cell((x, y))
            if 'WUMPUS' in cell:
                self.grid[x][y] = 'DEAD WUMPUS'
                return True
        return False

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                cell = self.grid[i][j]
                x, y = j * 50, i * 50
                if 'WUMPUS' in cell:
                    self.screen.blit(self.wumpus, (x, y))
                elif 'DEAD WUMPUS' in cell:
                    self.screen.blit(self.arrow, (x, y))
                elif 'GOLD' in cell:
                    self.screen.blit(self.gold, (x, y))
                elif 'PIT' in cell:
                    self.screen.blit(self.pitch, (x, y))
        if self.agent:
            agent_x, agent_y = self.agent[1] * 50, self.agent[0] * 50
            self.screen.blit(self.character, (agent_x, agent_y))

    def update_agent_position(self, position):
        self.agent = position
