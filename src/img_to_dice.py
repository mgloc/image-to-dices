from PIL import Image


class Dices:
    DICE_IMG_PIXEL_SIZE: int = 54
    dices_images: list[Image.Image]
    level_of_white_values: list[int]

    def __init__(self):
        self.dices_images = self.load_dices_images()
        self.level_of_white_values = self.calculate_white_levels()

    def load_dices_images(self):
        dices_images = [None] * 12
        for i in range(6):
            dices_images[i] = Image.open(f"src/dices/white/{i + 1}.png").convert("L")
        for i in range(6):
            dices_images[i + 6] = Image.open(f"src/dices/black/{6 - i}.png").convert("L")
        return dices_images

    def calculate_white_levels(self) -> list[int]:
        level_of_white_values = [None] * 12
        for i in range(12):
            level_of_white_values[i] = self.calculate_white_level(self.dices_images[i])
        return level_of_white_values

    def calculate_white_level(self, image: Image.Image) -> int:
        # Return the medium level of white for the image
        pixels = image.load()
        width, height = image.size
        total = 0
        for x in range(width):
            for y in range(height):
                total += pixels[x, y]
        return round(total / (width * height))

    def get_image_by_white_level(self, level_of_white: float):
        # Return the dice image corresponding to the level of white using self.level_of_white_values
        if level_of_white < 0 or level_of_white > 255:
            raise ValueError("Level of white must be between 0 and 255")
        for i in range(12):
            if level_of_white >= self.level_of_white_values[i]:
                if i != 0:
                    return self.calculate_nearest_white_level(level_of_white, i - 1, i)
                return self.dices_images[i]
        return self.dices_images[11]

    def calculate_nearest_white_level(self, level_of_white, i1, i2):
        # Assuming that i1 == i2 - 1 and self.level_of_white_values[i1] <= level_of_white <= self.level_of_white_values[i2]
        # Return the nearest dice image to the level of white
        if level_of_white - self.level_of_white_values[i1] < self.level_of_white_values[i2] - level_of_white:
            return self.dices_images[i1]
        return self.dices_images[i2]

    def get_img_size(self):
        return self.DICE_IMG_PIXEL_SIZE


def main(image_path: str = "img/sample-image.jpg", output_file: str = "img/output.jpg"):
    # Prerequisites
    dices = Dices()

    # Load image
    image = Image.open(image_path).convert("L")

    # Resize image to represent it as 10k dices
    width, height = image.size
    image_ratio = width / height

    dices_width = round(100 * image_ratio)
    dices_height = round(100 / image_ratio)

    image = image.resize((dices_width, dices_height))

    # Create new image
    new_image = Image.new("L", (dices_width * dices.get_img_size(), dices_height * dices.get_img_size()), color=255)

    pixels = image.load()

    for x in range(dices_width):
        for y in range(dices_height):
            level_of_white = pixels[x, y]
            dice_image = dices.get_image_by_white_level(level_of_white)
            new_image.paste(dice_image, (x * dices.get_img_size(), y * dices.get_img_size()))

    new_image.resize((width, height)).save(output_file)


if __name__ == "__main__":
    main()
