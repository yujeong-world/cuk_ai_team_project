class KnowledgeBase:
  def __init__(self, size):
      self.size = size
      self.percepts = [[None for _ in range(size)] for _ in range(size)]
      self.safe = [[False for _ in range(size)] for _ in range(size)]
      self.visited = [[False for _ in range(size)] for _ in range(size)]
      self.breeze = [[False for _ in range(size)] for _ in range(size)]
      self.stench = [[False for _ in range(size)] for _ in range(size)]
      self.pit_possible = [[False for _ in range(size)] for _ in range(size)]
      self.wumpus_possible = [[False for _ in range(size)] for _ in range(size)]
      self.scream = False

  def update(self, position, percept):
      x, y = position
      self.percepts[x][y] = percept
      self.visited[x][y] = True
      if percept == "SAFE":
          self.safe[x][y] = True
      if "BREEZE" in percept:
          self.breeze[x][y] = True
          self.update_possible_pit(x, y)
      if "STENCH" in percept:
          self.stench[x][y] = True
          self.update_possible_wumpus(x, y)
      if "SCREAM" in percept:
          self.scream = True

  def update_possible_pit(self, x, y):
      directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
      for dx, dy in directions:
          nx, ny = x + dx, y + dy
          if 0 <= nx < self.size and 0 <= ny < self.size and not self.visited[nx][ny]:
              self.pit_possible[nx][ny] = True

  def update_possible_wumpus(self, x, y):
      directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
      for dx, dy in directions:
          nx, ny = x + dx, y + dy
          if 0 <= nx < self.size and 0 <= ny < self.size and not self.visited[nx][ny]:
              self.wumpus_possible[nx][ny] = True

  def is_safe(self, position):
      x, y = position
      return self.safe[x][y] and not self.pit_possible[x][y] and not self.wumpus_possible[x][y]

  def is_visited(self, position):
      x, y = position
      return self.visited[x][y]

  def get_percept(self, position):
      x, y = position
      return self.percepts[x][y]

  def should_shoot_arrow(self, position):
      x, y = position
      return self.stench[x][y] and not self.scream
