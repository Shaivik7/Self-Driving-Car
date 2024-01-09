import pygame
import numpy as np
from pygame.locals import *
from Self_driving_car import Tesla
from Cars import Vehicle
import random
from Sensor import SensorCreate
from Utilities import scale_image
from gloval_variables import (
    CAR_X,
    CAR_Y,
    width,
    height,
    screen_size,
    marker_width,
    marker_height,
    road,
    left_edge_marker,
    right_edge_marker,
    left_lane,
    center_lane,
    right_lane,
    lanes,
    x_axis,
)


pygame.init()

# Creating window
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Self Driving Car!")

# Colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)


fps = 120
clock = pygame.time.Clock()


lane_marker_move_y = 0

other_cars_group = pygame.sprite.Group()


def draw(self_driving_car):
    self_driving_car.draw(screen)


# creating the car and sensors
self_driving_car = Tesla(CAR_X, CAR_Y, 4, 6)
car_sensor = SensorCreate(CAR_X, CAR_Y)

main_car_speed = self_driving_car.max_vel / 1.5
other_car_speed = self_driving_car.max_vel / 3.9

# Game Loop
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    # Draw Grass
    screen.fill(green)

    # Draw Road
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    draw(self_driving_car)

    # Draw Lane markers
    lane_marker_move_y += main_car_speed * 4
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(
            screen,
            white,
            (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
        )
        pygame.draw.rect(
            screen,
            white,
            (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
        )

    # Draw other cars
    if len(other_cars_group) < 2:
        add_cars = True
        for other_car in other_cars_group:
            if other_car.rect.top < other_car.rect.height * 1.5:
                add_cars = False
        if add_cars:
            lane = random.choice(x_axis)
            other_car = pygame.image.load("Images/Other_cars.png")
            vehicle = Vehicle(other_car, lane, height / -4)
            other_cars_group.add(vehicle)
    for car in other_cars_group:
        car.rect.y += other_car_speed * clock.tick(120)
        if car.rect.top >= height:
            car.kill()
    other_cars_group.draw(screen)

    sprite_cars = other_cars_group.sprites()
    for car in sprite_cars:
        car_sensor.sensor_draw(screen, self_driving_car, car, other_cars_group)

    # keys = pygame.key.get_pressed()
    # moved = False
    # if keys[pygame.K_a]:
    #     self_driving_car.rotate(left=True)
    # if keys[pygame.K_d]:
    #     self_driving_car.rotate(right=True)
    # if keys[pygame.K_w]:
    #     self_driving_car.move_forward()

    # if not moved:
    #     self_driving_car.reduce_speed()
    forward_threshold = 0.5
    backward_threshold = -0.5
    neural_network_outputs = car_sensor.neural_network_feedforward()

    # Extract control signals from the neural network outputs
    forward_signal = any(
        output > forward_threshold for output in neural_network_outputs
    )
    backward_signal = any(
        output < backward_threshold for output in neural_network_outputs
    )

    # Apply control signals to the car
    if forward_signal:
        self_driving_car.move_forward()
    elif backward_signal:
        self_driving_car.reduce_speed()

    # Adjust sensitivity for steering based on the neural network outputs
    steering_sensitivity = 0.2
    steering_value = np.mean(neural_network_outputs) * steering_sensitivity
    self_driving_car.rotate(left=steering_value < 0, right=steering_value > 0)

    pygame.display.update()

pygame.quit()
