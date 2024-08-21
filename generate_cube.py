import argparse
import sys
import csv
from PIL import Image

factions = ["axiom", "bravos", "lyra", "muna", "ordis", "yzmir"]

def fill_car_list_from_faction(faction):
    card_list = []
    with open(faction + '/list.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=':')
        line_count = 0
        for row in csv_reader:
            card_name = f'{row[0]}_{row[1]}'
            card_name = card_name.lower()
            card_name = card_name.replace(" ", "_")
            card_name = card_name.replace(",", "")
            card_name = card_name.replace(".", "")
            for i in range(int(row[2])):
                card_list.append("images/" + faction + "/" + card_name + ".jpg")
            line_count += 1
    return card_list

def generate_from_card_list(faction, cards):
    images = [Image.open(x) for x in cards]
    width = images[0].size[0] * 6
    height = images[0].size[1] * ((0 if len(cards) % 6 == 0 else 1) + len(cards) // 6)
    new_im = Image.new('RGB', (width, height))
    x_offset = 0
    y_offset = 0

    for i in range(len(cards)):
        if i % 6 == 0 and i != 0:
            x_offset = 0
            y_offset += images[i].size[1]
        new_im.paste(images[i], (x_offset, y_offset))
        x_offset += images[i].size[0]

    new_im.save("images/cube_" + faction + ".jpg")


def generate_pdf_from_faction_jpg():
    image_list = []
    for faction in factions:
        image = Image.open(f'images/cube_{faction}.jpg')
        image_list.append(image)

    image_list[0].save('cube.pdf', 'PDF', resolution=100.0, save_all=True, append_images=image_list[1:])

def main():
    parser = argparse.ArgumentParser(description='jpg and pdf cube generator')
    parser.add_argument('--pdf', action='store_true', help='generate pdf from\
                        existing jpg')
    parser.add_argument('--jpg', action='store_true', help='generate all\
    faction jpg')
    args = parser.parse_args()

    if args.jpg:
        for faction in factions:
            card_list = fill_car_list_from_faction(faction)
            generate_from_card_list(faction, card_list)

    if args.pdf:
        generate_pdf_from_faction_jpg()
    return 0

if __name__ == "__main__":
    main()
