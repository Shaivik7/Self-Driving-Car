from Cars import Vehicle
import pygame
from neural_network import NeuralNetwork
import math
from Utilities import car_rotate_center
from Utilities import scale_image
from gloval_variables import CAR_X, CAR_Y
from Sensor import SensorCreate

MAIN_CAR, rect = scale_image(
    image=pygame.image.load("Images/main_car.png"), x=CAR_X, y=CAR_Y
)


class Tesla:
    car = MAIN_CAR

    def __init__(self, x, y, max_vel, rotation_vel):
        self.image = self.car
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = x, y
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel * 0.7
        elif right:
            self.angle -= self.rotation_vel * 0.7

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        car_rotate_center(self.image, screen, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        horizontal = math.sin(radians * self.vel)
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
