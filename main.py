import argparse
from textwrap import wrap
from encrypt import encrypt
from decrypt import decrypt

path_image_with_message = "new_image.bmp"
path_image_without_message = "test.jpg"

BLACK = [0, 0, 0]
CONTROL_COLOR = BLACK
ENCODE_COLOR = [0,0,1]
message = "HOLA MUNDOoo jeje"

def init_parser():
    parser = argparse.ArgumentParser(
            usage="%(prog)s [KEY] [FILE]",
            description="Encode a message in an image using steganography "
        )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )

    # TODO Add lenght validation, it must be a 9 number strings
    parser.add_argument('key', type=str, nargs=1, help="Color key used to encode and decode the message")

    parser.add_argument('file', type=str, nargs=1, help="File used to be encoded or decoded")
    

    action_group = parser.add_mutually_exclusive_group(required=True)

    action_group.add_argument("--decode", action="store_true")
    action_group.add_argument('--encode', action="store", dest="message", help="Message to encrypt")

    return parser


def main():
    parser = init_parser()
    arguments = parser.parse_args()
    file = arguments.file[0]
    key = arguments.key[0]
    
    key = [int(element) for element in wrap(key, 3)]


    if arguments.decode:
        decrypt(file, key)
    else:
        encrypt(file, arguments.message, key)



if __name__ == "__main__":
    main()