import pygame
import math
from gloval_variables import road_border_list
from neural_network import NeuralNetwork
import numpy as np
from pygame.math import Vector2
from math import inf


class SensorCreate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sensor_color = [(0, 0, 0), (200, 0, 0)]
        self.intersected_color = (200, 0, 0)
        self.sensor_count = 7
        sensor_spacing = 55  # Adjust this value based on your requirements
        sensor_length = 220

        # Initialize sensor positions based on initial car position
        self.sensor_offsets = [
            ((i - (self.sensor_count - 1) / 2) * sensor_spacing, -sensor_length)
            for i in range(self.sensor_count)
        ]

        self.sensor_positions = [
            (x + offset[0], y + offset[1]) for offset in self.sensor_offsets
        ]
        self.sensor_readings = []
        self.valid_readings = []

    def line_rect_collision(self, line_start, line_end, rect):
        adjusted_line_start = self.sensor_positions[0]
        line_rect = pygame.Rect(
            line_start[0],
            line_start[1],
            line_end[0] - line_start[0],
            line_end[1] - line_start[1],
        )

        # Check if the line segment collides with the rectangle
        if line_rect.colliderect(rect.rect):
            return True

        return False

    def sensor_draw(self, screen, tesla, rect, rect_group):
        self.update_sensor_positions(tesla)
        # Update sensor line coordinates based on car's position
        for i in range(len(self.sensor_positions) - 1):
            sensor_start = self.sensor_positions[i]
            sensor_end = self.sensor_positions[i + 1]

            # Check for collision between the sensor line segment and the vehicle rectangle
            collision_rect = self.line_rect_collision(
                (tesla.x, tesla.y), sensor_end, rect
            )

            # Draw the sensor line and rectangle based on collision status
            rays = self.ray_cast(
                origin=Vector2(tesla.x, tesla.y),
                target=sensor_end,
                obstacles=rect_group,
            )

            self.sensor_readings.append(rays)
            valid_readings = [
                [reading.x, reading.y]
                for reading in self.sensor_readings
                if reading is not None
            ]
            self.valid_readings.append(valid_readings)

            if collision_rect is True:
                pygame.draw.line(
                    screen, self.sensor_color[1], (tesla.x, tesla.y), sensor_end, 2
                )
            else:
                pygame.draw.line(
                    screen, self.sensor_color[0], (tesla.x, tesla.y), sensor_end, 2
                )
        self.neural_network_feedforward()

    # def ray_cast(self, origin, target, obstacles):
    #     current_pos = Vector2(origin)
    #     heading = target - origin
    #     # A normalized vector that points to the target.
    #     direction = heading.normalize()
    #     for _ in range(int(heading.length())):
    #         current_pos += direction
    #         for sprite in obstacles:
    #             # If the current_pos collides with an
    #             # obstacle, return it.
    #             if sprite.rect.collidepoint(current_pos):
    #                 return current_pos
    #     # Otherwise return the target.
    #     return None
    def ray_cast(self, origin, target, obstacles):
        current_pos = Vector2(origin)
        heading = target - origin
        direction = heading.normalize()

        closest_reading = None
        closest_distance = inf

        for _ in range(int(heading.length())):
            current_pos += direction
            for sprite in obstacles:
                if sprite.rect.collidepoint(current_pos):
                    distance = current_pos.distance_to(origin)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_reading = current_pos

        return closest_reading

    def sensor_position_update(self, screen, tesla, rect):
        self.update_sensor_positions(tesla)
        self.sensor_draw(screen, tesla, rect)

    def update_sensor_positions(self, tesla):
        # Update sensor positions based on car's position
        angle_rad = math.radians(tesla.angle)
        for i, offset in enumerate(self.sensor_offsets):
            sensor_x = (
                tesla.x
                - offset[0] * math.cos(angle_rad)
                + offset[1] * math.sin(angle_rad)
            )
            sensor_y = (
                tesla.y
                + offset[0] * math.sin(angle_rad)
                + offset[1] * math.cos(angle_rad)
            )
            self.sensor_positions[i] = (sensor_x, sensor_y)

    def neural_network_feedforward(self):
        if not self.valid_readings:
            return None  # No valid readings available

        # Flatten the list of readings
        flat_readings = [item for sublist in self.valid_readings for item in sublist]

        # Convert to a numpy array
        input_vector = np.array(flat_readings).flatten().reshape((-1, 1))

        # Assuming you have a NeuralNetwork class defined
        neural_network = NeuralNetwork(
            input_size=input_vector.shape[1], hidden_sizes=[1], output_size=1
        )

        # Perform feedforward

        output = neural_network.feedforward(input_vector)
        neural_network_output = output.flatten()

        return neural_network_output
