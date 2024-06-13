import pygame
import random
import sys
from queue import PriorityQueue
from utils import update_time, check_breeze, check_glitter, check_stench, shoot_arrow, check_scream, update_wumpus_location

pygame.init()

# 색깔, 위치, 화면설정
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wumpus Game")

character = pygame.image.load("./images/character.jpg")
wumpus = pygame.image.load("./images/wumpus.jpg")
gold = pygame.image.load("./images/gold.jpg")
pitch = pygame.image.load("./images/pitch.jpg")
arrow = pygame.image.load("./images/new_arrow.jpg")

# 게임판 위 좌표
startBoxPointX = 340
startBoxPointY = 60

interval = 75
point = {
    '12': (1, 7),
    '13': (3, 7),
    '14': (5, 7),
    '15': (7, 7),
    '8': (1, 5),
    '9': (3, 5),
    '10': (5, 5),
    '11': (7, 5),
    '4': (1, 3),
    '5': (3, 3),
    '6': (5, 3),
    '7': (7, 3),
    '0': (1, 1),
    '1': (3, 1),
    '2': (5, 1),
    '3': (7, 1)
}

# wumpus, pitch, gold 발생할 격자 random 고르기
realGold = random.randint(1, 15)
goldLocation = [False] * 16
wumpusLocation = [False] * 16
pitchLocation = [False] * 16

goldLocation[realGold] = True

# 하나의 Wumpus만 생성
realWumpus = random.randint(1, 15)
while realWumpus == realGold:
    realWumpus = random.randint(1, 15)
wumpusLocation[realWumpus] = True

for i in range(1, 16):
    if i == realGold or i == realWumpus:
        continue
    pitchLocation[i] = random.choices([True, False], weights=[0.1, 0.9])[0]

for i in range(16):
    if wumpusLocation[i] and pitchLocation[i]:
        pitchLocation[i] = False

wumpusTrue = [i for i in range(16) if wumpusLocation[i]]
pitchTrue = [i for i in range(16) if pitchLocation[i]]

# 캐릭터들 사이즈 변경
character = pygame.transform.scale(character, (120, 120))
wumpus = pygame.transform.scale(wumpus, (120, 120))
gold = pygame.transform.scale(gold, (120, 120))
pitch = pygame.transform.scale(pitch, (120, 120))
arrow = pygame.transform.scale(arrow, (120, 120))

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
title = pygame.font.SysFont(None, 50, True)
boardText = pygame.font.SysFont(None, 30)
winText = pygame.font.SysFont(None, 70, True)


# 경로 찾기 함수 (A* 알고리즘)
def find_path(grid, start, goal, avoid=None):
    if avoid is None:
        avoid = []
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        _, current = frontier.get()

        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (current[0] + dx, current[1] + dy)
            if 0 <= next_pos[0] < 4 and 0 <= next_pos[1] < 4:
                if any(grid[next_pos[0]][next_pos[1]].get(avoid_item)
                       for avoid_item in avoid):
                    continue

                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[
                        next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + abs(next_pos[0] -
                                              goal[0]) + abs(next_pos[1] -
                                                             goal[1])
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current
    path = []
    if current == goal:
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
    return path


# 에이전트를 이동시키는 함수
def move_agent(agent_pos, current_path):
    if current_path:
        return list(current_path.pop(0))
    else:
        return agent_pos


# 에이전트가 stench를 감지한 위치에서 Wumpus 위치를 추정하는 함수
def find_wumpus_position(stench_positions):
    possible_positions = {}
    for (x, y) in stench_positions:
        adjacent_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for pos in adjacent_positions:
            if 0 <= pos[0] < 4 and 0 <= pos[1] < 4:
                if pos in possible_positions:
                    possible_positions[pos] += 1
                else:
                    possible_positions[pos] = 1

    max_prob_position = max(possible_positions, key=possible_positions.get)
    return max_prob_position


# 그리드 초기화 및 에이전트 위치 설정
grid = [[{'wumpus': False, 'pit': False} for _ in range(4)] for _ in range(4)]
for i in range(16):
    x, y = divmod(i, 4)
    if goldLocation[i]:
        grid[x][y]['gold'] = True
    if wumpusLocation[i]:
        grid[x][y]['wumpus'] = True
    if pitchLocation[i]:
        grid[x][y]['pit'] = True
agent_pos = [0, 0]

# 안전한 경로를 찾음
gold_pos = (realGold // 4, realGold % 4)
safe_path_to_gold = find_path(grid,
                              tuple(agent_pos),
                              gold_pos,
                              avoid=['pit', 'wumpus'])
safe_path_back = find_path(grid, gold_pos, (0, 0), avoid=['pit', 'wumpus'])

current_path = safe_path_to_gold + safe_path_back[1:]

running = True
clock = pygame.time.Clock()  # 시간을 조정하기 위한 clock 객체 생성

playing = True
time = 0  # 시간 초기화
arrows = 3  # 에이전트의 화살 수 초기화
scream = False  # scream 초기화
wumpus_death_pos = None  # Wumpus가 죽은 위치 초기화
stench_positions = []  # 에이전트가 stench를 감지한 위치들
has_gold = False  # 골드 획득 상태 초기화
win = False  # 승리 상태 초기화

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    screen.fill(WHITE)
    old_agent_pos = agent_pos[:]
    agent_pos = move_agent(agent_pos, current_path)

    # 에이전트가 이동했을 때 시간 증가
    time = update_time(agent_pos, old_agent_pos, time)

    # breeze 상태 확인
    breeze = check_breeze(agent_pos, pitchLocation)

    # glitter 상태 확인
    glitter = check_glitter(agent_pos, goldLocation)
    if glitter:
        has_gold = True

    # stench 상태 확인
    stench = check_stench(agent_pos, wumpusLocation)
    if stench:
        stench_positions.append(tuple(agent_pos))

    # stench 위치 기반으로 Wumpus 위치 추정 및 화살 발사
    if len(stench_positions) >= 2 and arrows > 0:
        wumpus_pos = find_wumpus_position(stench_positions)
        wx, wy = wumpus_pos
        if wx < agent_pos[0]:
            arrow_direction = 'UP'
        elif wx > agent_pos[0]:
            arrow_direction = 'DOWN'
        elif wy < agent_pos[1]:
            arrow_direction = 'LEFT'
        else:
            arrow_direction = 'RIGHT'

        scream, wumpusLocation, wumpus_death_pos, arrows = shoot_arrow(
            agent_pos, wumpusLocation, arrow_direction, arrows)
        wumpusLocation = update_wumpus_location(wumpusLocation,
                                                wumpus_death_pos)

    # scream 상태 확인 및 일시적 scream 설정
    if wumpus_death_pos and check_scream(agent_pos, wumpus_death_pos):
        scream = True
    else:
        scream = False

    # 격자 그리기 및 상태 표시
    pygame.draw.rect(screen, BLACK, [340, 60, 600, 600])
    lineStart = [340, 60]  # 가로시작, 세로시작
    for i in range(3):
        lineStart[0] += 150
        pygame.draw.line(screen, GREEN, [lineStart[0], 60],
                         [lineStart[0], 660], 1)
    for i in range(3):
        lineStart[1] += 150
        pygame.draw.line(screen, GREEN, [340, lineStart[1]],
                         [940, lineStart[1]], 1)

    # gold 위치설정
    goldRect = gold.get_rect()
    goldRect.centerx = startBoxPointX + interval * point[f"{realGold}"][0]
    goldRect.centery = startBoxPointY + interval * point[f"{realGold}"][1]
    screen.blit(gold, goldRect)

    # pitch 위치설정 및 출력
    for i in pitchTrue:
        pitchRect = pitch.get_rect()
        pitchRect.centerx = startBoxPointX + interval * point[f"{i}"][0]
        pitchRect.centery = startBoxPointY + interval * point[f"{i}"][1]
        screen.blit(pitch, pitchRect)

    # wumpus 위치설정 및 출력
    for i in wumpusTrue:
        if wumpus_death_pos and i == wumpus_death_pos[
                0] * 4 + wumpus_death_pos[1]:
            continue  # 죽은 Wumpus는 출력하지 않음
        wumpusRect = wumpus.get_rect()
        wumpusRect.centerx = startBoxPointX + interval * point[f"{i}"][0]
        wumpusRect.centery = startBoxPointY + interval * point[f"{i}"][1]
        screen.blit(wumpus, wumpusRect)

    # 에이전트 이동 및 출력
    characterRect = character.get_rect()
    characterRect.centerx = startBoxPointX + interval * point[
        f"{agent_pos[0] * 4 + agent_pos[1]}"][0]
    characterRect.centery = startBoxPointY + interval * point[
        f"{agent_pos[0] * 4 + agent_pos[1]}"][1]
    screen.blit(character, characterRect)

    # 승리 조건 체크 및 화면 중앙에 승리 메시지 표시
    if has_gold and agent_pos == [0, 0]:
        win = True
        win_message = winText.render("AGENT WIN", True, BLUE)
        win_rect = win_message.get_rect(center=(SCREEN_WIDTH // 2,
                                                SCREEN_HEIGHT // 2))
        screen.blit(win_message, win_rect)

    # 추가 텍스트 및 레이아웃 설정
    wumpusTitle = title.render("WUMPUS GAME", True, BLACK)
    screen.blit(wumpusTitle, [10, 10])
    pygame.draw.rect(screen, BLACK, [10, 50, 200, 300], 1)
    Stench = boardText.render(f"Stench : {stench}", True, BLACK)
    screen.blit(Stench, [15, 60])
    Breeze = boardText.render(f"Breeze : {breeze}", True, BLACK)
    screen.blit(Breeze, [15, 90])
    Glitter = boardText.render(f"Glitter : {glitter}", True, BLACK)
    screen.blit(Glitter, [15, 120])
    Scream = boardText.render(f"Scream : {scream}", True, BLACK)  # 비명 상태 추가
    screen.blit(Scream, [15, 150])
    ArrowCount = boardText.render(f"Arrows : {arrows}", True, BLACK)  # 화살 개수 추가
    screen.blit(ArrowCount, [15, 180])
    TimeText = boardText.render(f"Time : {time}", True, BLACK)
    screen.blit(TimeText, [600, 10])

    pygame.display.flip()

    clock.tick(1)#0.6

pygame.quit()
sys.exit()
