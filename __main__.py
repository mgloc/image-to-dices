import sys
from src.img_to_dice import main

# Handle all case if the user doesn't give any argument, or the argument is not a jpg or png file
if 2 > len(sys.argv) or len(sys.argv) > 3:
    print("Usage: python3 -m img_to_dice <image> <output_file>")
    exit(1)
if not sys.argv[1].endswith(".jpg") and not sys.argv[1].endswith(".png"):
    print("The image must be a jpg or png file")
    exit(1)

main(sys.argv[1])
