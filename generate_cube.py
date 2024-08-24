import argparse
import sys
import csv
from PIL import Image

factions = ["axiom", "bravos", "lyra", "muna", "ordis", "yzmir"]

def get_dimention_from_images(images, col):
    width = images[0].size[0] * col
    overflow = (0 if len(images) % col == 0 else 1)
    height = images[0].size[1] * (overflow + len(images) // col)
    return (width, height)


def card_list_from_file_path(path):
    card_list = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=':')
        for row in csv_reader:
            card_name = f'{row[0]}_{row[1]}'
            card_name = card_name\
                    .lower()\
                    .replace(" ", "_")\
                    .replace(",", "")\
                    .replace(".", "")
            for i in range(int(row[2])):
                card_list.append("images/database/" + card_name + ".jpg")
    return card_list


def jpg_from_card_list(name='custom/export.jpg', card_list=[], col=5):
    images = [Image.open(x) for x in card_list]
    new_im = Image.new('RGB', get_dimention_from_images(images, col))
    x_offset = 0
    y_offset = 0

    for i in range(len(card_list)):
        if (i % col == 0) and (i != 0):
            x_offset = 0
            y_offset += images[i].size[1]
        new_im.paste(images[i], (x_offset, y_offset))
        x_offset += images[i].size[0]

    new_im.save("images/" + name + ".jpg")


def pdf_from_jpg_path_list(path_list):
    for path in path_list:
        image = Image.open(f'{path}')
        image_list.append(image)
    image_list[0].save('Core_Set.pdf', 'PDF', resolution=100.0, save_all=True, append_images=image_list[1:])


def generate_cube():
    for faction in factions:
        card_list = card_list_from_file_path(faction + '/list.txt')
        jpg_from_card_list('cube_display/' + faction, card_list)
        card_list = card_list_from_file_path(faction + '/heros.txt')
        jpg_from_card_list('cube_display/heros_' + faction, card_list)

def main():
    parser = argparse.ArgumentParser(description='jpg and pdf cube generator')
    parser.add_argument('--full', '-f', dest='full', action='store_true',
                    help='generate full cube cube')
    parser.add_argument('--custom', '-c', dest='custom', nargs=3,
                    metavar=('path_list', 'export_name', 'card_per_line'),
                    help='generate from card list')
    args = parser.parse_args()

    if args.custom:
        card_list = card_list_from_file_path(args.custom[0])
        jpg_from_card_list(args.custom[1], card_list, int(args.custom[2]))

    if args.full:
        generate_cube()
    return 0


if __name__ == "__main__":
    main()
