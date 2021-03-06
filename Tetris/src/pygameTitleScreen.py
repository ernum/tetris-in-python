import time

import pygame as pg
from random import randint as ri
from .UI import *

fontPath = "../fonts/VCR_OSD_MONO_1.ttf"

INTRO_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "Soundtrack" / "Intro.ogg"
MAIN_SOUND_PATH = pathlib.Path(
    __file__).absolute().parents[1] / "Sound" / "Soundtrack" / "mainloop.ogg"
INTRO_END = pg.USEREVENT+0
pg.mixer.music.set_endevent(INTRO_END)
pg.mixer.music.load(str(INTRO_SOUND_PATH))
pg.mixer.music.play()

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (250, 250, 0)
turq = (20, 250, 250)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 150, 20)
blue = (0, 0, 255)
pink = (200, 20, 250)
colors = [black, yellow, turq, green, red, orange, blue, pink, white]
t = time.time()
FPS = 60
# do stuff
elapsed = time.time() - t

muted = False


def exit():
    raise SystemExit


def start():
    global started
    started = not started


started = False


def sqrDistance(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2


def titlePage(dis):
    pg.display.set_caption("TETRIS")

    # Paths
    ICON_IMG_PATH = pathlib.Path(
        __file__).absolute().parents[1] / "images" / "tetrisIcon2.png"
    KEYS_IMG_PATH = pathlib.Path(
        __file__).absolute().parents[1] / "images" / "keys.png"

    # Icon
    icon = pg.image.load(str(ICON_IMG_PATH))

    # Keys
    keyImage = pg.image.load(str(KEYS_IMG_PATH))
    keyWidth = 300
    keyRect = keyImage.get_rect()
    keyHeight = int(keyWidth * keyRect.height/keyRect.width)
    keyImage = pg.transform.scale(keyImage, (keyWidth, keyHeight))

    pg.display.set_icon(icon)

    w, h = dis.get_rect().size
    titleFontSize = 100
    titleStartY = -titleFontSize
    titleDropSpeed = 1

    buttonWidth = 100
    buttonHeight = 50
    buttonFontSize = 30

    sliderWidth = 20
    sliderHeight = 60
    sliderMargin = 20
    sliderRect = (w-sliderWidth-sliderMargin, h-sliderHeight -
                  sliderMargin, sliderWidth, sliderHeight)

    volumeIconW = 40
    muteClickRadius = 20

    buttonHoverColor = (200, 200, 200)

    titleEndY = (h-buttonHeight)/2 - buttonHeight*1.5 - titleFontSize/2
    title = Text("TETRIS", (255, 255, 255), titleFontSize, (w/2, titleStartY))

    startButton = Button(((w-buttonWidth)/2-buttonWidth*0.6, (h-buttonHeight)/2, buttonWidth, buttonHeight),
                         (255, 255, 255), 0, (100, 100, 100), "START", buttonFontSize, (0, 0, 0), start, buttonHoverColor)
    exitButton = Button(((w-buttonWidth)/2+buttonWidth*0.6, (h-buttonHeight)/2, buttonWidth, buttonHeight),
                        (255, 255, 255), 0, (100, 100, 100), "EXIT", buttonFontSize, (0, 0, 0), exit, buttonHoverColor)

    volume = VolumeController(
        sliderRect, (sliderRect[0]-volumeIconW/2 - 10, sliderRect[1]+sliderRect[3]/2), muteClickRadius)

    clock = pg.time.Clock()
    t = time.time()

    colorIndex = 0

    pauseText = Text("PAUSE", (255, 255, 255), 26,
                     (sliderMargin + 95, h-keyHeight-sliderMargin + 27))
    rotationText = Text("ROTATE", (255, 255, 255), 26,
                        (sliderMargin + 55, h-keyHeight-sliderMargin + 77))
    moveText = Text("MOVE", (255, 255, 255), 26,
                    (sliderMargin + 295, h-keyHeight-sliderMargin + 77))

    while not started:
        dis.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise SystemExit

            if event.type == INTRO_END and event.code == 0:
                MAIN_END = pg.USEREVENT + 1
                pg.mixer.music.set_endevent(MAIN_END)
                pg.mixer.music.load(str(MAIN_SOUND_PATH))
                pg.mixer.music.play(-1)

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                p = pg.mouse.get_pos()
                if startButton.isInside(p):
                    startButton.click()
                    global muted
                    muted = volume.muted
                if exitButton.isInside(p):
                    exitButton.click()

                if volume.buttonInside(p):
                    volume.click()

        if startButton.isInside(pg.mouse.get_pos()):
            startButton.hover()
        else:
            startButton.noHover()

        if exitButton.isInside(pg.mouse.get_pos()):
            exitButton.hover()
        else:
            exitButton.noHover()

        if pg.mouse.get_pressed()[0]:
            if volume.update():
                pg.mixer.music.set_volume(volume.val)

        if time.time() - t > 0.2:
            rand = ri(1, len(colors) - 2)
            while colorIndex == rand:
                rand = ri(1, len(colors) - 2)
            colorIndex = rand
            title.color = colors[colorIndex]
            t = time.time()

        # Title drop animation
        titleY = title.pos[1]
        if titleY < titleEndY:
            titleDropSpeed += 0.5
            title.pos = (title.pos[0], title.pos[1] + titleDropSpeed)
        if titleY > titleEndY and titleDropSpeed != 0:
            if titleDropSpeed > 0:
                titleDropSpeed *= -1
            titleDropSpeed += 3
            title.pos = (title.pos[0], title.pos[1] + titleDropSpeed)
        if titleY > titleEndY + 3:
            titleDropSpeed = 0
            title.pos = (title.pos[0], title.pos[1] + titleDropSpeed)

        startButton.draw(dis)
        exitButton.draw(dis)
        title.draw(dis)
        volume.draw(dis)
        dis.blit(keyImage, (sliderMargin, h-keyHeight-sliderMargin + 7))
        pauseText.draw(dis)
        moveText.draw(dis)
        rotationText.draw(dis)

        pg.display.update()

        clock.tick(FPS)
    start()
