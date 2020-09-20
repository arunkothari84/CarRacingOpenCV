import pygame  # install pygame library
import time
import random
import cv2
import numpy as np

pygame.init()  # initialize the pygame library
vid = cv2.VideoCapture(0)

# SCREEN ELEMENTS
width = 800
height = 600
screen = pygame.display.set_mode((width, height))  # height is 600 and 800 is width


# TO MANAGE TIME AND FPS
clock = pygame.time.Clock()

# IMAGE ELEMENTS
carImg = pygame.image.load("car1.jpg")
car_width = 56


def background():
    grass = pygame.image.load("grass.jpg")
    yellow_strip = pygame.image.load("yellow_strip.jpg")
    strip = pygame.image.load("strip.jpg")
    screen.blit(grass, (0, 0))
    screen.blit(grass, (700, 0))
    screen.blit(strip, (120, 0))
    screen.blit(strip, (680, 0))
    for x in [0, 100, 200, 300, 400, 500]:
        screen.blit(yellow_strip, (400, x))


# FOR CAPTION AND FONTS
pygame.display.set_caption("RACING")
myFont = pygame.font.SysFont("None", 100)
render_text = myFont.render("CAR CRASHED", 0, (0, 0, 0))


# APPEARING OF CAR
def car(x, y):
    screen.blit(carImg, (x, y))


def obstacle(obs_x, obs_y, obs):
    obs_pic = 0
    if obs == 0:
        obs_pic = pygame.image.load("car2.jpg")
    elif obs == 1:
        obs_pic = pygame.image.load("car4.jpg")
    elif obs == 2:
        obs_pic = pygame.image.load("car5.jpg")
    elif obs == 3:
        obs_pic = pygame.image.load("car6.jpg")
    elif obs == 4:
        obs_pic = pygame.image.load("car7.jpg")
    screen.blit(obs_pic, (obs_x, obs_y))


def car_crash():
    screen.blit(render_text, (80, 200))
    pygame.display.update()
    time.sleep(2)
    game_loop()


def game_loop():
    bumped = False
    x = 400
    y = 470
    obstacle_speed = 10
    obs = random.randrange(0, 4)
    obs_x = random.randrange(200, 650)
    obs_y = -750
    obs_width = 56
    obs_height = 125
    # define a video capture object

    a = 0

    # To quit the game when close button is pressed
    while not bumped:
        ret, frame = vid.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        blurred = cv2.medianBlur(gray, 5)

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(blurred,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                            param2=30, minRadius=20, maxRadius=40)

        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

            print(a)
            if 0 < a < 250:
                x += 5
            if 400 < a < 600:
                x -= 5
            else:
                pass

        # To change the background color
        screen.fill((119, 119, 119))
        background()
        obs_y -= (obstacle_speed / 4)
        obstacle(obs_x, obs_y, obs)
        obs_y += obstacle_speed

        # Calling the car function
        car(x, y)
        if x >= 680 - car_width or x < 120:
            car_crash()

        # For returning the car back from top
        if obs_y > height:
            obs_y = 0 - obs_width
            obs_x = random.randrange(170, width - 170)
            obs = random.randrange(0, 4)

        # For crash the car when the obs car is in the range of the main car
        if y < obs_y + obs_height:
            if obs_x < x < obs_x + obs_width or x + obs_width < obs_width and x + obs_width < obs_x + obs_width:
                car_crash()

        # Updating the game
        pygame.display.update()
        clock.tick(100)


game_loop()

pygame.quit()
quit()
