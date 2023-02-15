# import os
import sys
import random
import pygame

BLACK = (0, 0, 0)
GREY = (169, 169, 169)
WHITE = (255, 255, 255)


class Player(object):
    def __init__(self) -> None:
        self.size = pygame.Rect(50,50,25,25)
        self.status = 0
        player_1 = pygame.image.load(".\\assets\\player_1.png")
        player_1 = pygame.transform.scale(player_1, (30, 25))
        self.all_status = [player_1]
        
        # position
        self.x = 180
        self.y = 550

        # status
        self.left_jump = False
        self.right_jump = False
        self.dead = False

        # movement
        self.jump_speed = 15
        self.x_speed = 5
        self.back_move = 0
        self.gravity = 0.5

    def update(self):
        if self.left_jump:
            self.jump_speed -= 1
            self.x -= self.x_speed
            self.y -= self.jump_speed
        elif self.right_jump:
            self.jump_speed -= 1
            self.x += self.x_speed
            self.y -= self.jump_speed
        else:
            self.gravity += 0.01
            self.y += self.gravity

        # restrict in the screen
        if self.x > 385:
            self.x = 385
        elif self.x < -15:
            self.x = -15

        # restrict in centre
        if self.y < 340:
            self.back_move = 340 - self.y
            self.y = 340
        
        # update position
        self.size[1] = self.y
        self.size[0] = self.x


class Obstacle(object):
    def __init__(self, start_pos: int, x_pos: int) -> None:
        # record if scored
        self.scored = False
        
        # position initials
        self.wall_y = start_pos
        self.wall_x = x_pos
        
        self.squ_y = start_pos - 165 - 630*2
        self.squ_x = x_pos + gen_squ_x() 

        # load assets
        self.left = pygame.image.load(".\\assets\\obstacle.jpg")
        self.left = pygame.transform.scale(self.left, (250, 30))

        self.right = pygame.image.load(".\\assets\\obstacle.jpg")
        self.right = pygame.transform.scale(self.right, (250, 30))

        self.squ = pygame.image.load(".\\assets\\obstacle.jpg")
        self.squ = pygame.transform.scale(self.squ, (30, 30))

    def update(self, player: Player) -> None:
        global score

        # sync obstacles with player
        self.wall_y += player.back_move
        self.squ_y += player.back_move

        if not self.scored and self.wall_y > 370:
            score += 1
            self.scored = True

        if self.wall_y > 630:
            self.wall_y -= 950
            self.wall_x = gen_obstacle_x()
            self.scored = False

        if self.squ_y > 630:
            self.squ_y -= 950
            self.squ_x = self.wall_x + gen_squ_x()


def create_map(screen: pygame.Surface, player: Player, obstacle_0: Obstacle, obstacle_1: Obstacle, obstacle_2: Obstacle) -> None:
    global score
    screen.fill(WHITE)

    # obstacle initialise
    screen.blit(obstacle_0.left, (obstacle_0.wall_x, obstacle_0.wall_y))
    screen.blit(obstacle_0.right, (obstacle_0.wall_x+380, obstacle_0.wall_y))

    screen.blit(obstacle_1.left, (obstacle_1.wall_x, obstacle_1.wall_y))
    screen.blit(obstacle_1.right, (obstacle_1.wall_x+380, obstacle_1.wall_y))

    screen.blit(obstacle_2.left, (obstacle_2.wall_x, obstacle_2.wall_y))
    screen.blit(obstacle_2.right, (obstacle_2.wall_x+380, obstacle_2.wall_y))

    # squares
    screen.blit(obstacle_0.squ, (obstacle_0.squ_x, obstacle_0.squ_y))
    screen.blit(obstacle_1.squ, (obstacle_1.squ_x, obstacle_1.squ_y))
    screen.blit(obstacle_2.squ, (obstacle_2.squ_x, obstacle_2.squ_y))

    obstacle_0.update(player)
    obstacle_1.update(player)
    obstacle_2.update(player)

    # player initialise
    player.player_status = 0
    screen.blit(player.all_status[player.status], (player.x, player.y))
    player.update()

    # score board
    font = pygame.font.SysFont("arial", 50)
    screen.blit(font.render(str(score), -1, BLACK), (190, 60))

    pygame.display.update()


def check_dead(obstacle_0: Obstacle, obstacle_1: Obstacle, obstacle_2: Obstacle, player: Player, height: int) -> bool:
    ob_rect_l_0 = pygame.Rect(obstacle_0.wall_x, obstacle_0.wall_y, obstacle_0.left.get_width(), obstacle_0.left.get_height())
    ob_rect_r_0 = pygame.Rect(obstacle_0.wall_x+380, obstacle_0.wall_y, obstacle_0.left.get_width(), obstacle_0.left.get_height())
    ob_rect_s_0 = pygame.Rect(obstacle_0.squ_x, obstacle_0.squ_y, obstacle_0.squ.get_width(), obstacle_0.squ.get_height())

    ob_rect_l_1 = pygame.Rect(obstacle_1.wall_x, obstacle_1.wall_y, obstacle_1.left.get_width(), obstacle_1.left.get_height())
    ob_rect_r_1 = pygame.Rect(obstacle_1.wall_x+380, obstacle_1.wall_y, obstacle_1.left.get_width(), obstacle_1.left.get_height())
    ob_rect_s_1 = pygame.Rect(obstacle_1.squ_x, obstacle_1.squ_y, obstacle_1.squ.get_width(), obstacle_1.squ.get_height())

    ob_rect_l_2 = pygame.Rect(obstacle_2.wall_x, obstacle_2.wall_y, obstacle_2.left.get_width(), obstacle_2.left.get_height())
    ob_rect_r_2 = pygame.Rect(obstacle_2.wall_x+380, obstacle_2.wall_y, obstacle_2.left.get_width(), obstacle_2.left.get_height())
    ob_rect_s_2 = pygame.Rect(obstacle_2.squ_x, obstacle_2.squ_y, obstacle_2.squ.get_width(), obstacle_2.squ.get_height())

    if ob_rect_l_0.colliderect(player.size) or ob_rect_r_0.colliderect(player.size):
        player.dead = True
        return True

    if ob_rect_l_1.colliderect(player.size) or ob_rect_r_1.colliderect(player.size):
        player.dead = True
        return True

    if ob_rect_l_2.colliderect(player.size) or ob_rect_r_2.colliderect(player.size):
        player.dead = True
        return True

    if ob_rect_s_0.colliderect(player.size) or ob_rect_s_1.colliderect(player.size) or ob_rect_s_2.colliderect(player.size):
        player.dead = True
        return True

    if player.y > height:
        player.dead = True
        return True

    return False


def get_result(screen: pygame.Surface):
    final_text1 = "Game over"
    final_text2 = "score:" + str(score)
    final_text3 = "press 'R' to restart"

    ft1_font = pygame.font.SysFont("arial",60)
    ft1_surf = ft1_font.render(final_text1, 1, GREY)
    ft2_font = pygame.font.SysFont("arial",40)
    ft2_surf = ft2_font.render(final_text2, 1, GREY)
    ft3_font = pygame.font.SysFont("arial",30)
    ft3_surf = ft3_font.render(final_text3, 1, GREY)

    screen.blit(ft1_surf,[screen.get_width()/2-ft1_surf.get_width()/2,100])
    screen.blit(ft2_surf,[screen.get_width()/2-ft2_surf.get_width()/2,160])
    screen.blit(ft3_surf,[screen.get_width()/2-ft3_surf.get_width()/2,200])
    
    pygame.display.flip()


def gen_obstacle_x() -> int:
    return random.randint(-200, -30)


def gen_squ_x() -> int:
    return random.randint(250, 300)


def main():
    global score
    score = 0
    # game window setup
    size = width, height = 400, 630
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    pygame.display.set_caption("jump square")

    obstacle_0 = Obstacle(-360, gen_obstacle_x())
    obstacle_1 = Obstacle(-30, gen_obstacle_x())
    obstacle_2 = Obstacle(300, gen_obstacle_x())

    player = Player()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not player.dead:
                    player.left_jump = True
                    player.right_jump = False
                    player.back_move = 0
                    player.gravity = 0.5
                    player.x_speed = 5
                    player.jump_speed = 15
                elif event.key == pygame.K_RIGHT and not player.dead:
                    player.right_jump = True
                    player.left_jump = False
                    player.back_move = 0
                    player.gravity = 0.5
                    player.x_speed = 5
                    player.jump_speed = 15
                elif event.key == pygame.K_r:
                    score = 0
                    obstacle_0 = Obstacle(-360, gen_obstacle_x())
                    obstacle_1 = Obstacle(-30, gen_obstacle_x())
                    obstacle_2 = Obstacle(300, gen_obstacle_x())
                    player = Player()

        if check_dead(obstacle_0, obstacle_1, obstacle_2, player, height):
            get_result(screen)
        else:
            create_map(screen, player, obstacle_0, obstacle_1, obstacle_2)

if __name__ == "__main__":
    score = 0
    pygame.init()
    main()
