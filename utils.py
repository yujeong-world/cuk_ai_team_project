def update_time(agent_pos, old_agent_pos, time):
    if agent_pos != old_agent_pos:
        time += 1
    return time

def check_breeze(agent_pos, pitchLocation):
    x, y = agent_pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for pos in adjacent_positions:
        if 0 <= pos[0] < 4 and 0 <= pos[1] < 4:
            if pitchLocation[pos[0] * 4 + pos[1]]:
                return True
    return False

def check_glitter(agent_pos, goldLocation):
    x, y = agent_pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for pos in adjacent_positions:
        if 0 <= pos[0] < 4 and 0 <= pos[1] < 4:
            if goldLocation[pos[0] * 4 + pos[1]]:
                return True
    return False

def check_stench(agent_pos, wumpusLocation):
    x, y = agent_pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for pos in adjacent_positions:
        if 0 <= pos[0] < 4 and 0 <= pos[1] < 4:
            if wumpusLocation[pos[0] * 4 + pos[1]]:
                return True
    return False


def check_scream(agent_pos, wumpus_death_pos):
    if not wumpus_death_pos:
        return False
    x, y = agent_pos
    wx, wy = wumpus_death_pos
    adjacent_positions = [(wx-1, wy), (wx+1, wy), (wx, wy-1), (wx, wy+1)]
    return (x, y) in adjacent_positions

def shoot_arrow(agent_pos, wumpusLocation, direction, arrows):
    scream = False
    wumpus_death_pos = None
    x, y = agent_pos

    if direction == 'UP':
        for i in range(x-1, -1, -1):
            if wumpusLocation[i * 4 + y]:
                wumpusLocation[i * 4 + y] = False
                scream = True
                wumpus_death_pos = (i, y)
                arrows -=1
                break
    elif direction == 'DOWN':
        for i in range(x+1, 4):
            if wumpusLocation[i * 4 + y]:
                wumpusLocation[i * 4 + y] = False
                scream = True
                wumpus_death_pos = (i, y)
                arrows -= 1
                break
    elif direction == 'LEFT':
        for i in range(y-1, -1, -1):
            if wumpusLocation[x * 4 + i]:
                wumpusLocation[x * 4 + i] = False
                scream = True
                wumpus_death_pos = (x, i)
                arrows -= 1
                break
    elif direction == 'RIGHT':
        for i in range(y+1, 4):
            if wumpusLocation[x * 4 + i]:
                wumpusLocation[x * 4 + i] = False
                scream = True
                wumpus_death_pos = (x, i)
                arrows -= 1
                break

    if not scream:
        for i in range(x-1, -1, -1):
            if wumpusLocation[i * 4 + y]:
                wumpusLocation[i * 4 + y] = False
                scream = True
                wumpus_death_pos = (i, y)
                arrows -= 1
                break
        for i in range(x+1, 4):
            if wumpusLocation[i * 4 + y]:
                wumpusLocation[i * 4 + y] = False
                scream = True
                wumpus_death_pos = (i, y)
                arrows -= 1
                break
        for i in range(y-1, -1, -1):
            if wumpusLocation[x * 4 + i]:
                wumpusLocation[x * 4 + i] = False
                scream = True
                wumpus_death_pos = (x, i)
                arrows -= 1
                break
        for i in range(y+1, 4):
            if wumpusLocation[x * 4 + i]:
                wumpusLocation[x * 4 + i] = False
                scream = True
                wumpus_death_pos = (x, i)
                arrows -= 1
                break

    return scream, wumpusLocation, wumpus_death_pos, arrows



def update_wumpus_location(wumpusLocation, wumpus_death_pos):
    if wumpus_death_pos:
        x, y = wumpus_death_pos
        wumpusLocation[x * 4 + y] = False
    return wumpusLocation

