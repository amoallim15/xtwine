import argparse
import sys
from src.twine import Twine
from src._version import __version__


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt/Decrypt Using TWINE Block Cipher"
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.add_argument(
        "--input-file",
        "-i",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file path to be encryped/decrypted.",
    )
    parser.add_argument(
        "text", nargs="?", type=str, help="Input text to be encryped/decrypted."
    )
    parser.add_argument(
        "--output-file",
        "-o",
        type=argparse.FileType("w"),
        help="Output file name.",
        default=sys.stdout,
    )
    parser.add_argument("-d", "--decrypt", action="store_true", help="decrypt data.")
    parser.add_argument(
        "-z", default=0x50, help="Encryption/Decryption bit size (80 or 128) bits"
    )
    parser.add_argument("-k", help="Encryption/Decryption secret key")

    args = parser.parse_args()
    input = args.text or args.input_file.read()
    output = ""
    twine = Twine(key=args.k, key_size=args.z)

    print(vars(twine))

    if args.decrypt:
        output = twine.decrypt(input)
    else:
        output = twine.encrypt(input)

    args.output_file.write(output)


if __name__ == "__main__":
    main()
