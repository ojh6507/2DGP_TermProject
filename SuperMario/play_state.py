import random
import game_framework
import game_world
import round1
from pico2d import *
from player import character
from block import block
from monster import Goomba
from monster import Koopa
from item import MUSHROOM
from item import FLOWER
import server
WIDTH, HEIGHT = 800,600

def setPos():
    for c in server.coin:
        c.set_pos(random.randint(400, 500),random.randint(75, 200))

    for it in server.item:
        it.set_pos(random.randint(400, 5000),random.randint(90, 200))

    for br in brick:
        br.set_pos(random.randint(400, 5000), random.randint(200, 200))


world = None
fire = []
exp = None
brick_block = None
brick = None
green = None
red = None
music = None


def collide(a,b):
    str = ' '
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()
    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False
    # 충돌 없는 것부터 처리


    if ra - lb >= 2 and la < lb:
        str = 'right'

    if rb - la >= 2 and rb < ra:
        str = 'left'

    if ((lb <= ra and la <= lb) or (la <= rb and rb <= ra) or (ra <= rb and lb <= la)) and (tb - ba <= 50 and ta > tb):
        str = 'bottom'

    if ((lb <= ra and la <= lb) or (la <= rb and rb <= ra) or (ra <= rb and lb <= la)) and (ta - bb <= 10 and bb > ba):
        str = 'top'

    return True, str


def set():
    global world

    if world.x < (-2950) and server.player.x - 400 < 0:
        for game_object in game_world.all_objects():
            if game_object.get_name() != 'player':
                game_object.x -= (server.player.x - 400)


    elif server.player.x - 400 > 0:
        for game_object in game_world.all_objects():
            if game_object.get_name() != 'player':
                game_object.x -= (server.player.x - 400)
        server.player.x = 400


    elif server.player.x - 400 < 0 and world.x - (server.player.x - 400) < 3750:
        for game_object in game_world.all_objects():
            if game_object.get_name() != 'player':
                game_object.x -= (server.player.x - 400)
        server.player.x = 400

empty = []
ground = []
underground = []
def set_world():
    global empty,ground,underground
    for col in range(len(round1.INFO)):
        for row in range(len(round1.INFO[col])):

            if round1.INFO[col][row] == 0:
                empty.append( round1.Empty_Tile(col, row))
                # game_world.add_object(empty,2)

            elif round1.INFO[col][row] == 1:
                ground.append(round1.Floor_Tile(col, row))

                # game_world.add_object(ground,3)

            elif round1.INFO[col][row] == 2:
                ground.append(round1.under_Tile(col, row))

                # game_world.add_object(underground,3)

cur_len = None
def enter():
    global world, fire, brick_block,brick ,green,red,exp,music,ground,empty

    world = round1.BACKGROUND()
    set_world()
    server.player = character.mario()

    brick_block = block.Bricks()
    server.coin = [block.COIN() for n in range(0, 20)]
    server.item = [block.item_block() for n in range(0, 5)]
    brick = [block.Bricks() for n in range(0, 4)]
    server.mushroom = MUSHROOM(500,65)

    server.goomba = [Goomba.GOOMBA() for i in range(1)]
    green = [Koopa.GreenKoopa() for i in range(3)]
    red = [Koopa.RedKoopa() for i in range(3)]
    server.flower = FLOWER(1000, 65)
    cur_len = len(character.gen_fire)
    setPos()

    game_world.add_object(world, 0)
    game_world.add_object(server.player, 1)
    game_world.add_object(server.mushroom, 1)
    game_world.add_object(server.flower, 1)
    game_world.add_objects(server.goomba, 1)
    game_world.add_objects(green, 1)

    game_world.add_objects(red, 1)
    game_world.add_objects(server.coin, 1)
    game_world.add_objects(server.item, 1)
    game_world.add_objects(brick, 1)
    game_world.add_objects(ground,3)
    game_world.add_objects(empty,3)

    game_world.add_collision_group(server.player, server.coin, 'player:coin')
    game_world.add_collision_group(server.player, server.item, 'player:item_block')
    game_world.add_collision_group(server.player, brick, 'player:bricks')
    game_world.add_collision_group(server.player, server.mushroom, 'player:mushroom')
    game_world.add_collision_group(server.player, server.flower, 'player:flower')
    game_world.add_collision_group(server.player, ground, 'player:ground')

    #music = load_music('stage1.mp3')
    #music.set_volume(10)
    #music.play()


def exit():
    game_world.clear()
def update():
    set()
    global fire,cur_len
    fire = character.gen_fire
    if cur_len != len(fire) :
        game_world.add_collision_group(fire, ground, 'fire:ground')
        cur_len = len(fire)

    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_paris():
        if collide(a, b):
            v, p = collide(a,b)
            a.handle_collision(b, group, p)
            b.handle_collision(a, group, p)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.player.handle_event(event)

def pause():
    pass
def resume():
    pass

def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas(800,600)
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__': # 단독 실행이면
    test_self()
