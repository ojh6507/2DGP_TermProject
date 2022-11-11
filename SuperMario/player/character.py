from pico2d import *
import math
import game_framework
from fire import Ball
import game_world

RD, LD, RU, LU, SPACE, ATTACK, SHIFTD, SHIFTU, SPACE = range(9)
event_name = ['RD', 'LD', 'RU', 'LU', 'JUMP', 'ATTACK']
key_event_table = {
(SDL_KEYDOWN, SDLK_SPACE): SPACE,
(SDL_KEYDOWN, SDLK_LSHIFT): SHIFTD,
(SDL_KEYDOWN, SDLK_RIGHT): RD,
(SDL_KEYDOWN, SDLK_LEFT): LD,
(SDL_KEYDOWN, SDLK_z): ATTACK,
(SDL_KEYUP, SDLK_RIGHT): RU,
(SDL_KEYUP, SDLK_LEFT): LU,
(SDL_KEYUP, SDLK_LSHIFT): SHIFTU

}

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class IDLE:
    def enter(self, event):
        self.x_dir = 0
        self.frame = 0
        self.Run = False
        self.TIME_PER_ACTION = 1

    def exit(self, event):
        if event == ATTACK:
           self.Fire_Ball()
        pass

    def do(self):
        if not self.jump:

            if self.mario_size == 'Small':
                self.image = load_image('smario_idle.png')
                self.clip = 76

            elif self.mario_size == 'Normal':
                self.clip = 79
                if not self.flower:
                    self.image = load_image('idle_right.png')
                else:
                    self.image = load_image('flower_idle_right.png')

        else:
            self.jump_func()
            if self.face_dir == 1:
                if self.mario_size == 'Small':
                    self.image = load_image('smario_jump.png')
                    self.clip = 30
                elif self.mario_size == 'Normal':
                    if not self.flower:
                        self.image = load_image('jump_right.png')
                    else:
                        self.image = load_image('flower_jump_right.png')

                    self.clip = 18


            if self.Y_velocity < -self.jump_height:
                self.jump = False
                self.possible_jump = True
                self.Y_velocity = self.jump_height
                self.frame = 0

        if self.face_dir == 1:
            self.reflect = ' '
        else:
            self.reflect = 'h'

        self.frame = (self.frame + self.ACTION_PER_TIME * self.clip * game_framework.frame_time) % self.clip


    def draw(self):
        if self.jump:
            if self.mario_size == 'Small':

                self.perframe = 35
                self.action = 0
                self.height = 45


            if self.mario_size == 'Normal':

                self.perframe = 40
                self.action = 0
                self.height = 66

        if not self.jump:
            if self.mario_size == 'Small':

                self.perframe = 30
                self.action = 0
                self.height = 35

            elif self.mario_size == 'Normal':

                self.perframe = 50
                self.action = 0
                self.height = 65

        self.image.clip_composite_draw(int(self.frame) * self.perframe, 0, self.perframe, self.height, 0, self.reflect, self.x, self.y, self.perframe, self.height)


class WALK:
    def enter(self, event):
        self.frame = 0
        if event == RD:
            self.x_dir += 1
            self.face_dir = 1
        elif event == LD:
            self.x_dir -= 1
            self.face_dir = -1
        elif event == RU:
            self.x_dir -= 1
        elif event == LU:
            self.x_dir += 1
        self.TIME_PER_ACTION = 1

    def exit(self,event):
        self.face_dir = self.x_dir

    def do(self):
        if not self.jump:
            if self.Run:
                self.TIME_PER_ACTION = 0.4
                self.velocity = 3
                if self.mario_size == 'Small':
                    self.image = load_image('smario_run.png')
                    self.clip = 13

                if self.mario_size == 'Normal':
                    if not self.flower:
                        self.image = load_image('run_fast.png')
                    else:
                        self.image = load_image('flower_runfast.png')
                    self.clip = 18


            if not self.Run:
                self.TIME_PER_ACTION = 1
                self.velocity = 1
                if self.mario_size == 'Small':
                    self.image = load_image('smario_walk.png')
                    self.clip = 27

                if self.mario_size == 'Normal':
                    if not self.flower:
                        self.image = load_image('mario_walk.png')
                    else:
                        self.image = load_image('flower_mario_walk.png')
                    self.clip = 25
        else:
            if self.mario_size == 'Small':
                self.image = load_image('smario_jump.png')
                self.clip = 30

            elif self.mario_size == 'Normal':
                if not self.flower:
                    self.image = load_image('jump_right.png')
                else:
                    self.image = load_image('flower_jump_right.png')
                self.clip = 18

            self.TIME_PER_ACTION = 1
            self.jump_func()

            if self.Y_velocity < -self.jump_height:
                self.jump = False
                self.possible_jump = True
                self.Y_velocity = self.jump_height

        if self.x_dir == -1:
            self.reflect = 'h'
        else:
            self.reflect = ' '


        self.frame = (self.frame + self.ACTION_PER_TIME * self.clip * game_framework.frame_time) % self.clip
        self.x += self.x_dir * RUN_SPEED_PPS * game_framework.frame_time *self.velocity
        self.x = clamp(25, self.x, 800)

    def draw(self):
        if self.jump:
            if self.mario_size == 'Small':

                self.perframe = 35
                self.action = 0
                self.height = 45

            if self.mario_size == 'Normal':

                self.perframe = 40
                self.action = 0
                self.height = 66

        else:
            if self.Run and self.mario_size == 'Normal':

                self.perframe = 50
                self.action = 0
                self.height = 60

            elif self.Run and self.mario_size == 'Small':

                self.perframe = 45
                self.action = 0
                self.height = 40

            elif not self.Run and self.mario_size == 'Small':

                self.perframe = 30
                self.action = 0
                self.height = 40

            elif not self.Run and self.mario_size == 'Normal':

                self.perframe = 50
                self.action = 70
                self.height = 65


        self.image.clip_composite_draw(int(self.frame) * self.perframe, 0, self.perframe, self.height, 0, self.reflect,self.x, self.y, self.perframe,self.height)


class TRANS_SIZE:
    def enter(self, event):
        print('enter trans size')
        self.TIME_PER_ACTION= 2
        self.frame = 0
        pass
    def exit(self, event):
        pass
    def do(self):
        print('do transsize')
        self.image = load_image('mario_up.png')
        self.clip = 7
        self.perframe = 40
        self.height = 82

        self.frame = (self.frame + self.ACTION_PER_TIME * self.clip * game_framework.frame_time) % self.clip

        if self.face_dir == 1:
            self.reflect = ' '
        else:
            self.reflect = 'h'
        print('reflect',self.reflect)
        print('x_dir', self.x_dir)

        if int(self.frame) == 6:
            self.mario_size = 'Normal'
            self.y += 18
            self.event_que.clear()
            # 이전 상태가 walk면 walk로, idle이면 idle로

            if self.x_dir != 0:
                self.cur_state = WALK
            else:
                self.cur_state = IDLE

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * self.perframe, 0, self.perframe, self.height, 0, self.reflect,
                                       self.x, self.y+20, self.perframe, self.height)
class TRANS_MARIO:
    def enter(self, event):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass
class DIE:
    def enter(self, event):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass

next_state = {
    IDLE: {RU: WALK, LU: WALK, RD: WALK, LD: WALK, ATTACK: IDLE, SHIFTD: IDLE, SHIFTU: IDLE, SPACE: IDLE},
    WALK: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, ATTACK: WALK, SHIFTD: WALK, SHIFTU: WALK, SPACE: WALK},
    TRANS_SIZE: {RU: TRANS_SIZE, LU: TRANS_SIZE, RD: TRANS_SIZE, LD: TRANS_SIZE, ATTACK: TRANS_SIZE, SHIFTD: TRANS_SIZE, SHIFTU: TRANS_SIZE, SPACE: TRANS_SIZE},

}
# class explosion:
#     def __init__(self):
#         self.image = load_image('explosion.png')
#         self.frame = 0
#         self.x = 10
#         self.y = 10
#         self.w = 30
#         self.h = 29
#         self.anim_count = 0
#
#     def update(self):
#         self.anim_count += 1
#         if self.anim_count == 4:
#             self.frame = (self.frame+1)
#             self.anim_count = 0
#         if self.frame >= 5:
#             destroy_exp()
#     def set_pos(self,x,y):
#         self.x = x
#         self.y = y
#     def draw(self):
#         self.image.clip_draw(self.frame * self.w, 0, self.w, self.h, self.x, self.y)

class mario:
    def get_name(self):
        return 'player'
    def __init__(self):

        self.TIME_PER_ACTION = 1
        self.ACTION_PER_TIME = 1
        self.image = load_image('smario_idle.png')
        self.mario_size = 'Small'
        self.frame = 0

        self.height = 0
        self.action = 0
        self.perframe = 0
        self.reflect = ' '

        self.clip = 76
        self.x = 100
        self.y = 100 -10

        self.x_dir = 0
        self.face_dir = 1
        self.y_dir = 0

        self.velocity = 2

        self.flower = False
        self.Run = False
        self.growup = False
        self.jump = False
        self.possible_jump = True

        self.mass = 10
        self.jump_height = 11
        self.Y_gravity = 0.5
        self.Y_velocity = self.jump_height
        self.count_grow = 0
        self.count_jump = 0
        self.fall = False

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def jump_func(self):

        self.y += self.Y_velocity
        self.Y_velocity -= self.Y_gravity
    def fall_func(self):
        if self.Y_velocity < 0:
            self.y += self.Y_velocity
        self.Y_velocity -= self.Y_gravity
        if self.Y_velocity <= -self.jump_height:
            self.fall = False
            self.jump = False
            self.Y_velocity = self.jump_height

    def update(self):
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.cur_state.do(self)
        if self.event_que:
            event = self.event_que.pop()

            if event == SPACE:
                self.frame = 0
                self.jump = True
            elif event == SHIFTD:
                self.frame = 0
                self.Run = True
            if event == SHIFTU:
                self.Run = False

            self.cur_state.exit(self,event)

            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print('Error: ', self.cur_state.__name__,' ', event_name[event])
            self.cur_state.enter(self, event)
        self.x = clamp(0,self.x,800)

        if self.fall:
            self.fall_func()

    def check_gameOver(self):
        if self.die:
            self.image =load_image('gameover_mario.png')
            self.clip = 13
            self.action = 0
            self.height = 60
            self.ch_size = 50

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def add_event(self,event):
        self.event_que.insert(0, event)
    def handle_event(self, event):
       if(event.type, event.key) in key_event_table:
           key_event = key_event_table[(event.type, event.key)]
           self.add_event(key_event)
    def Fire_Ball(self):
        if self.flower:
            ball = Ball(self.x, self.y, self.face_dir * 3)
            game_world.add_object(ball, 1)

    def get_bb(self):
        if self.mario_size == 'Small':
            return self.x - 10, self.y - 14, self.x + 10, self.y + 14
        if self.mario_size == 'Normal':
            return self.x - 10, self.y - 28, self.x + 10, self.y + 28

    def handle_collision(self, other, group):
        if group == 'player:coin':
            print('coin + 1')
        elif group == 'player:item_block':
            self.fall = True
            print('Collision ',group)
        elif group == 'player:bricks':
            self.fall = True
            print('Collision ', group)
        elif group == 'player:mushroom':
            self.cur_state = TRANS_SIZE

