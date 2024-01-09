import pygame


def scale_image(image, x, y):
    image_scale = 45 / image.get_rect().width
    new_width = image.get_rect().width * image_scale
    new_height = image.get_rect().height * image_scale
    image = pygame.transform.scale(image, (new_width, new_height))
    rect = image.get_rect()
    rect.center = [x, y]
    return image, rect


def car_rotate_center(image, screen, position, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=position).center)
    screen.blit(rotated_image, new_rect)
