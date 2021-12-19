import pygame, sys, random
import time

def draw_floor():
	screen.blit(floor,(floor_x_pos,625))
	screen.blit(floor,(floor_x_pos + 432,625))
def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-650))
	return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes
def draw_pipe(pipes):
	for pipe in pipes:
		if pipe.bottom >= 600:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)
def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			hit.play()
			return False
	if bird_rect.top <= -75 or bird_rect.bottom >= 650:
		die.play()
		return False
	return True
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation():
	new_bird = bird_list[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird, new_bird_rect
def score_display(game_state):
	if game_state == 'main game':
		score_surface = game_font.render(f"Score: {int(score)}",True,(255,255,255))
		score_rect = score_surface.get_rect(center = (216,50))
		screen.blit(score_surface,score_rect)
	if game_state == 'game over':
		score_surface = game_font.render(f"Score: {int(score)}",True,(255,255,255))
		score_rect = score_surface.get_rect(center = (216,200))
		screen.blit(score_surface,score_rect)

		max_surface = game_font.render(f"Max: {int(hight_score)}",True,(255,255,255))
		max_rect = max_surface.get_rect(center = (216,300))
		screen.blit(max_surface,max_rect)
def update_score(score,hight_score):
	if score > hight_score:
		hight_score = score
	return hight_score

pygame.init()

screen = pygame.display.set_mode((432,690))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

gravity = 0.40
bird_movement = 0
game_active = True
game_font = pygame.font.Font('04B_19.ttf',40)
score = 0
hight_score = 0

# bg
bg = pygame.transform.scale2x(pygame.image.load('img/bg.png')).convert()

# floor
floor = pygame.transform.scale2x(pygame.image.load('img/flr.png')).convert()
floor_x_pos = 0

# bird
bird_down = pygame.transform.scale2x(pygame.image.load('img/d.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('img/m.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('img/u.png')).convert_alpha()
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 2
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))

# timer bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)

# pipe
pipe_surface = pygame.transform.scale2x(pygame.image.load('img/pp.png').convert())
pipe_list = []

# timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200,300,400,500,600]

# screen gameover
SG = pygame.transform.scale2x(pygame.image.load('img/go.png'))

# score
ls = pygame.transform.scale2x(pygame.image.load('img/ls.png').convert())

# sound
flap = pygame.mixer.Sound('sound/sfx_wing.wav')
hit = pygame.mixer.Sound('sound/sfx_hit.wav')
point = pygame.mixer.Sound('sound/sfx_point.wav')
die = pygame.mixer.Sound('sound/sfx_die.wav')

# button 181x105
btn = pygame.image.load('img/btn_pa.png').convert()

# while loop
while True:
	mouse_x, mouse_y = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				flap.play()
				bird_movement = 0
				bird_movement =- 11
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,384)
				bird_movement = 0
		if event.type == pygame.MOUSEBUTTONDOWN:
			flap.play()
			bird_movement = 0
			bird_movement =- 11
		if event.type == pygame.MOUSEBUTTONDOWN and game_active == False:
			if event.button == 1:
				if (124 < mouse_x < 306) and (400 < mouse_y < 505):
					game_active = True
					pipe_list.clear()
					bird_rect.center = (100,384)
					bird_movement = 0
		if event.type == spawnpipe:
			pipe_list.extend(create_pipe())
		if event.type == bird_flap:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0
			bird, bird_rect = bird_animation()

	screen.blit(bg,(0,0))
	if game_active:
		bird_movement += gravity
		rotated_bird = rotate_bird(bird)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,(bird_rect))
		game_active=check_collision(pipe_list)
		pipe_list = move_pipe(pipe_list)
		draw_pipe(pipe_list)
		score_display('main game')
	else:
		screen.blit(SG,(25,25))
		screen.blit(ls,(5,150))
		hight_score = update_score(score,hight_score)
		score = score - score
		score_display('game over')
		screen.blit(btn,(125,400))
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= - 432:
		floor_x_pos = 0
	pygame.display.update()
	clock.tick(120)
	score += 1
	time.sleep(0.001)