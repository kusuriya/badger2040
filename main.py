# Badger badger badger
# This is inspired from the pimoroni badger2040 badge sample, really all I managed to keep is the
# layout
#
# MIT License
# Copyright (c) 2022 Jason Barbier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import badger2040
import time
import qrcode

# persona
NAME = "Jason"
ALIAS = "Kusuriya"
DETAIL1_TITLE = ""
DETAIL1_TEXT = "@kusuriya:corrupted.io"
DETAIL2_TITLE = ""
DETAIL2_TEXT = "kusuriya@hackers.town"
QRCODE_URL = "https://card.corrupted.io"

# Size Options
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
IMAGE_WIDTH = 104
IMAGE_HEIGHT = 128
RNAME_HEIGHT = 20
DETAILS_HEIGHT = 30
NAME_HEIGHT = HEIGHT - RNAME_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

# Text Options
REAL_NAME_TEXT_SIZE = 0.5
DETAILS_TEXT_SIZE = 0.525
LEFT_PADDING = 5
ALIAS_PADDING = 5
DETAIL_SPACING = 5
FONT_FACE = "sans"

STATE = 0

def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text

def get_qr_size(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size

def draw_sql_error():
    display.pen(15)
    display.clear()
    display.pen(0)
    display.text("ERROR: you have an error",20,20,0.6)
    display.text("in your SQL syntax",20,40,0.6)
    display.text("near ; at line 1",20,60,0.6)
    display.update()
    display.update()

def draw_emblem():
    import branch_image
    BRANCH_IMAGE = bytearray(branch_image.data())
    display.image(BRANCH_IMAGE, IMAGE_WIDTH, IMAGE_HEIGHT, WIDTH - 104, 0)

def draw_qr_code(ox, oy, size, code):
    size, module_size = get_qr_size(size, code)
    display.pen(15)
    display.rectangle(ox, oy, size, size)
    display.pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)

def draw_badge():
    display.pen(13)
    display.clear()

    if QRCODE_URL == "":
        draw_emblem()
    elif STATE == 2:
        draw_emblem()
    else:
        code = qrcode.QRCode()
        code.set_text(QRCODE_URL)
        display.pen(15)
        display.rectangle(WIDTH - IMAGE_WIDTH, 0, IMAGE_WIDTH, HEIGHT)
        size, _ = get_qr_size(IMAGE_WIDTH, code)
        offset_x = int(IMAGE_WIDTH / 2 - size / 2)
        offset_y = int(HEIGHT / 2 - size / 2)
        draw_qr_code(WIDTH - IMAGE_WIDTH + offset_x, offset_y, IMAGE_WIDTH, code)

    # Draw a border around the image
    display.pen(13)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    display.pen(0)
    display.rectangle(1, 1, TEXT_WIDTH, RNAME_HEIGHT - 1)

    # Draw the company
    display.pen(15)  # Change this to 0 if a white background is used
    display.font(FONT_FACE)
    display.text(real_name, LEFT_PADDING, (RNAME_HEIGHT // 2) + 1, REAL_NAME_TEXT_SIZE)

    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, RNAME_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font(FONT_FACE)
    display.thickness(4)
    alias_size = 2.0  # A sensible starting scale
    while True:
        alias_length = display.measure_text(ALIAS, alias_size)
        if alias_length >= (TEXT_WIDTH - ALIAS_PADDING) and alias_size >= 0.1:
            alias_size -= 0.01
        else:
            display.text(ALIAS, (TEXT_WIDTH - alias_length) // 2, (NAME_HEIGHT // 2) + RNAME_HEIGHT + 1, alias_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font(FONT_FACE)
    display.thickness(2)
    alias_length = display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail1_text, 5 + alias_length + DETAIL_SPACING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)

    # Draw the second detail's title and text
    display.thickness(2)
    alias_length = display.measure_text(detail2_title, DETAILS_TEXT_SIZE)
    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail2_text, LEFT_PADDING + alias_length + DETAIL_SPACING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)


display = badger2040.Badger2040()
display.led(155)
badger2040.system_speed(badger2040.SYSTEM_VERY_SLOW)

real_name = truncatestring(NAME, REAL_NAME_TEXT_SIZE, TEXT_WIDTH)

detail1_title = truncatestring(DETAIL1_TITLE, DETAILS_TEXT_SIZE, TEXT_WIDTH)
detail1_text = truncatestring(DETAIL1_TEXT, DETAILS_TEXT_SIZE,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE))

detail2_title = truncatestring(DETAIL2_TITLE, DETAILS_TEXT_SIZE, TEXT_WIDTH)
detail2_text = truncatestring(DETAIL2_TEXT, DETAILS_TEXT_SIZE,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE))

display.update_speed(badger2040.UPDATE_NORMAL)
display.clear()
draw_badge()
display.update()
display.update_speed(badger2040.UPDATE_MEDIUM)

changed = not badger2040.woken_by_button()
while True:
    
    if display.pressed(badger2040.BUTTON_UP):
        STATE = 1
        changed = True
        display.led(0)
    if display.pressed(badger2040.BUTTON_DOWN):
        STATE = 2
        changed = True
        display.led(0)
    if display.pressed(badger2040.BUTTON_USER):
        STATE = 3
        changed = True
        display.led(0)
    if changed:
        if STATE == 1:
            draw_badge()
            display.update()
            changed = False
            display.led(255)
        if STATE == 2:
            draw_badge()
            display.update()
            changed = False
            display.led(255)
        if STATE == 3:
            draw_sql_error()
            changed = False
            display.led(255)


