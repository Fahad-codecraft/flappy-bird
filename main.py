import pygame
import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird Game v1.0.2")

img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)

clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()


def create_sprites():     
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


bird, game_start_message, score = create_sprites()

game_over_message = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gamestarted:
                    if not gameover:
                        # Start the game if space is pressed and game is not over
                        gamestarted = True
                        game_start_message.kill()
                        pygame.time.set_timer(column_create_event, 1500)
                    else:
                        # Restart the game if space is pressed and game is over
                        gameover = False
                        gamestarted = False
                        sprites.empty()
                        bird, game_start_message, score = create_sprites()
                        if game_over_message:
                            game_over_message.kill()

        if not gameover:
            bird.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and gameover:
            if game_over_message and game_over_message.rect.collidepoint(pygame.mouse.get_pos()):
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_start_message, score = create_sprites()
                if game_over_message:
                    game_over_message.kill()

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        game_over_message = GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
 