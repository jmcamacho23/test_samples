import random
import string, os
from random import randrange, choice


def random_phone_num_generator():
    area_code = randrange(101, 999)
    phone_prefix = randrange(201, 999)
    last_four = randrange(1000, 9999)
    phone_number = str(area_code) + '-' + str(phone_prefix) + '-' + str(last_four)
    return str(phone_number)

def random_phone_num_generator_custom(area_code_start=100, area_code_end=999, prefix_start=125, prefix_end=888, last_four_start=1234, last_four_end=9999):
    area_code = randrange(int(area_code_start), int(area_code_end))
    area_code_three_digits = f"{area_code:03d}"
    if (len(str(area_code_start)) < 3) or (len(str(area_code_end)) < 3):
        print(f'Area code start and end must be 3 digits, you entered {area_code_start} and {area_code_end}')

    phone_prefix = randrange(int(prefix_start), int(prefix_end))
    phone_prefix_three_digits = f"{phone_prefix:03d}"
    if (len(str(prefix_start)) < 3) or (len(str(prefix_end)) < 3):
        print(f'Phone prefix start and end must be 3 digits, you entered {prefix_start} and {prefix_end}')

    last_four = randrange(int(last_four_start), int(last_four_end))
    last_four_four_digits = f"{last_four:04d}"
    if (len(str(last_four_end)) < 4) or (len(str(last_four_end)) < 4):
        print(f'Last four start and end must be 4 digits, you entered {last_four_start} and {last_four_end}')

    phone_number = str(area_code_three_digits) + '-' + str(phone_prefix_three_digits) + '-' + str(last_four_four_digits)
    return str(phone_number)


def random_id_num_generator(start_num: int, stop_num: int):
    id_num = randrange(int(start_num), int(stop_num))
    return str(id_num)


def random_password_generator(character_count: int):
    pw = ''.join(random.choices(string.ascii_letters + string.digits, k=int(character_count)))
    return pw


def random_string_generator(iteration_count: int):
    str = ''.join(random.choices(string.ascii_letters + string.digits, k=int(iteration_count)))
    return str


def random_coordinates_generator():
    coordx = randrange(70, 1300)
    coordy = randrange(10, 500)
    coords = (coordx, coordy)
    return coords


def create_random_long_input(length_of_input):
    output = ""
    char_choices = string.ascii_letters + string.digits
    num_of_possible_chars = len(char_choices)
    print(num_of_possible_chars)
    print(random.randrange(num_of_possible_chars))
    for x in range(length_of_input):
        char_choice = char_choices[random.randrange(num_of_possible_chars)]
        output = output+char_choice
    return output

def create_random_browser_version():
    browser_version  = randrange(120, 146)
    minor_release = randrange(5111, 5699)
    patch_version = randrange(1,99)
    browser_version_with_patch = str(browser_version) + '.0.' + str(minor_release) + '.' + str(patch_version)
    return browser_version_with_patch
