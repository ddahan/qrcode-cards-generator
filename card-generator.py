#!/usr/local/bin/python3

import os, qrcode
from uuid import uuid4
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from copy import copy

# Card generator v0.0.1
# DESCRIPTION : This program allows to generate single qr-code cards using
# pillow and qrcode Python libraries.
# AUTHOR: David Dahan (david-dahan.com)
# LICENCE: MIT

# -----------------------------------------------------------------------------
# ---------------------------------- CONFIG -----------------------------------
# -----------------------------------------------------------------------------

NB_CARDS = 10 # Amount of cards to generate per script execution
OUTPUT_FORMAT = "TIFF"
BACKGROUND_IMG = "input/bg/recto.tif"
FONT = "input/fonts/Open_Sans/OpenSans-Semibold.ttf"
FONT_SIZE = 24

# -----------------------------------------------------------------------------
# --------------------------------- FUNCTIONS ---------------------------------
# -----------------------------------------------------------------------------

def create_UUIDs(qty):
    ''' Return a list of `qty` UUIDs transformed in Stirng '''

    return [str(uuid4()) for _ in range(qty)]

def data_to_qrcode(data):
    ''' Return a qrcode image from data '''

    qrc = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,
                        box_size=8,
                        border=0)

    qrc.add_data(data)
    qrc.make(fit=True)
    img = qrc.make_image()

    return img

# -----------------------------------------------------------------------------
# ----------------------------------- SCRIPT ----------------------------------
# -----------------------------------------------------------------------------

def main():

    # UUIDs generation and cast to string to be written with Pillow
    input_ids = create_UUIDs(NB_CARDS)

    # Directory creation to put cards on
    output_path = 'output/cards_' + datetime.now().strftime('%s')
    os.makedirs(output_path)

    # Background image opening + get size
    bg_image = Image.open(BACKGROUND_IMG)
    bg_x, bg_y = bg_image.size

    # Create a non-default font object to write text on images
    fnt = ImageFont.truetype(FONT, FONT_SIZE)

    # Main loop (1 round par card to be created)
    for cpt, elt_id in enumerate(input_ids):

        # Copy the background to the new image, then draw it
        new_bg = copy(bg_image)
        draw = ImageDraw.Draw(new_bg)

        # Generate a QR code as image
        qr_image = data_to_qrcode(elt_id)
        qr_x, qr_y = qr_image.size # Get width/height of QR code image

        # Paste the QR code image to the background
        # DELTA are used to change image placement (default is centered)
        DELTA_X = 0 # Keep the QR code horizontally centered
        DELTA_Y = 107 # Place the QR code according to the background
        new_bg.paste(qr_image,
                     (bg_x//2 - qr_x//2 + DELTA_X, bg_y//2 - qr_y//2 + DELTA_Y))

        # (Optinnal) Draw the ID on the card, just above the QR code
        draw.text((bg_x/2 - 240, 810), # No rule here, just try and adapt
                  text=elt_id,
                  font=fnt,
                  fill=0)

        # Save the picture
        full_path = os.path.join(output_path, elt_id + '.' + OUTPUT_FORMAT)
        new_bg.save(full_path, OUTPUT_FORMAT)

        # Delete in-memory objects (they're not necessary anymore)
        del new_bg
        del qr_image

        # Confirmation message
        print("{0} - The card {1} has been created".format(cpt, full_path))

    del bg_image

# Main
if __name__ == '__main__':
    main()
