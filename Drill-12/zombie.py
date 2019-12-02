import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import main_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


animation_names = ['Attack', 'Dead', 'Idle', 'Walk']




class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        positions = [(43, 750), (1118, 750), (1050, 530), (575, 220), (235, 33), (575, 220), (1050, 530)]
        self.patrol_positions = []
        for p in positions:
            self.patrol_positions.append((p[0], 1024 - p[1]))
        self.patrol_order = 1
        self.target_x, self.target_y = None, None
        self.x, self.y = 400,400
        #self.x, self.y = 1280 / 4 * 3, 1024 / 4 * 3
        self.load_images()
        self.dir = random.random()*2*math.pi # random moving direction
        self.speed = 0
        self.timer = 1.0 # change direction every 1 sec when wandering
        self.frame = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.build_behavior_tree()
        self.zombie_hp=0

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def wander(self):
        self.speed =RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer <0:
            self.timer +=1.0
            self.dir = random.random()*2*math.pi

        return BehaviorTree.SUCCESS

    def ballcount(self):
        if main_state.ball_count==5:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def bigballcount(self):
        if main_state.ball_count==5:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL



    def find_player(self):
        # fill here
        boy=main_state.get_boy()
        distance=(boy.x-self.x)**2+(boy.y-self.y)**2
        if distance < (PIXEL_PER_METER*10)**2:
            self.dir =math.atan2(boy.y-self.y,boy.x-self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed=0
            return BehaviorTree.FAIL


    def find_bigball(self):
        bigballs = main_state.get_bigball()
        temp_distance = (bigballs[0].x - self.x) ** 2 + (bigballs[0].y - self.y) ** 2
        pos_ball_x = 0
        pos_ball_y = 0
        for bigball in bigballs:
            distance = (bigball.x - self.x) ** 2 + (bigball.y - self.y) ** 2
            if distance < temp_distance:
                temp_distance = distance
                pos_ball_x = bigball.x
                pos_ball_y = bigball.y

        if temp_distance < (PIXEL_PER_METER*100)**2:
            self.dir = math.atan2(pos_ball_y - self.y, pos_ball_x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def find_ball(self):
        balls = main_state.get_ball()
        temp_distance = (balls[0].x - self.x)**2 + (balls[0].y - self.y)**2
        pos_ball_x = 0
        pos_ball_y = 0
        for ball in balls:
            distance = (ball.x - self.x)**2 + (ball.y - self.y)**2
            if distance < temp_distance:
                temp_distance = distance
                pos_ball_x = ball.x
                pos_ball_y = ball.y
        if temp_distance < (PIXEL_PER_METER*10)**2 and main_state.bigball_count==5:
            self.dir = math.atan2(pos_ball_y - self.y, pos_ball_x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass



    def move_to_player(self):
        # fill here
        self.speed=RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS

    def move_to_ball(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS

    def get_next_position(self):
        # fill here
        self.target_x,self.target_y = self.patrol_positions[self.patrol_order%len(self.patrol_positions)]
        self.patrol_order +=1
        self.dir = math.atan2(self.target_y-self.y,self.target_x-self.x)
        return BehaviorTree.SUCCESS
    def move_to_target(self):
        # fill here
        self.speed=RUN_SPEED_PPS
        self.calculate_current_position()
        distance = (self.target_x - self.x)**2 + (self.target_y - self.y)**2

        if distance <PIXEL_PER_METER**2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):


        find_player_node = LeafNode("Find Player", self.find_player) # left node -> left node
        move_to_player_node = LeafNode("Move to Player", self.move_to_player) #left node -> right node
        chase_node = SequenceNode("Chase") #letf node
        chase_node.add_children(find_player_node, move_to_player_node) #left node 정리

        bigballcount_node=LeafNode("Big Ball Count", self.bigballcount)
        ballcount_node = LeafNode("Ball Count", self.ballcount)
        kill_node = SequenceNode("kill")
        kill_node.add_children(ballcount_node,chase_node)
        move_to_ball_node = LeafNode("Move to ball", self.move_to_ball)

        ball_eat = LeafNode('bigball_eat', self.find_ball)
        balls_eat = SequenceNode("balls eat")  # right node
        balls_eat.add_children(ball_eat, move_to_ball_node)  # right node 정리

        bigball_eat = LeafNode('bigball_eat', self.find_bigball)
        bigballs_eat = SequenceNode("balls eat")  # right node
        bigballs_eat.add_children(bigball_eat,move_to_ball_node)  # right node 정리

        count = SequenceNode("count")  # right node
        count.add_children(ball_eat,bigballcount_node)  # right node 정리

        eat = SelectorNode("eat")  # right node
        eat.add_children(bigballs_eat, balls_eat)  # right node 정리

        wander_node=LeafNode('Wander',self.wander)
        wander_or_eat_node = SelectorNode("Wander or eat")#right node
        wander_or_eat_node.add_children(eat)  # right node 정리
        wander_chase_node = SelectorNode("WanderChase")  # root node
        wander_chase_node.add_children(kill_node, wander_or_eat_node)  #root node 정리
        self.bt = BehaviorTree(wander_chase_node)


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
       self.bt.run()

    def draw(self):
        self.font.draw(self.x - 60, self.y + 50, '(ZOMBIE_HP: %3.0f)' % self.zombie_hp, (255, 0, 255))
        draw_rectangle(*self.get_bb())
        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)

    def handle_event(self, event):
        pass

