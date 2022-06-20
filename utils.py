import matplotlib.pyplot as plt
import numpy as np

from bitarray import bitarray


def display_image(image: np.ndarray) -> None:
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.show()


def display_histogram(histogram: np.ndarray, num_values: int, title: str) -> None:
    values = [i for i in range(0, num_values)]
    plt.bar(values, histogram)
    plt.xlabel("Wartość")
    plt.ylabel("Liczba wystąpień")
    plt.title(title)
    plt.show()


def calculate_entropy(image: np.ndarray, num_values: int = 256) -> float:
    histogram = calculate_histogram(image, num_values)
    entropy = 0

    for value in histogram:
        if value != 0:
            p = value / image.size
            entropy += -p * np.log2(p)

    return entropy


def calculate_histogram(image: np.ndarray, num_values: int) -> np.ndarray:
    histogram = np.zeros(num_values)
    for row in image:
        for value in row:
            histogram[value] += 1
    return histogram


def calculate_compression_rate(
    input_image: np.ndarray, encoded_image: list[list[bitarray]], bits=8
) -> float:
    input_size = input_image.size * bits
    encoded_size = sum_bit_length(encoded_image)
    return input_size / encoded_size


def sum_bit_length(coded_image: list[list[bitarray]]) -> int:
    return sum([sum([len(code) for code in row]) for row in coded_image])


def average_code_bit_length(coded_image: list[list[bitarray]]) -> float:
    total_bit_length = sum_bit_length(coded_image)
    num_code_words = len(coded_image) * len(coded_image[0])
    return total_bit_length / num_code_words


def differencial_encode(image: np.ndarray, offset) -> np.ndarray:
    new_image = np.copy(image)
    predictions = np.ones(new_image.shape) * offset

    return (new_image - predictions).astype(np.int16)


def differencial_decode(image: np.ndarray, offset) -> np.ndarray:
    new_image = np.copy(image)
    predictions = np.ones(new_image.shape) * offset

    return (new_image + predictions).astype(np.uint8)


def map_to_positive_integers(image: np.ndarray) -> np.ndarray:
    new_image = np.zeros(image.shape, dtype=np.uint8)
    for i, row in enumerate(image):
        for j, pixel in enumerate(row):
            if pixel >= 0:
                new_image[i][j] = 2 * pixel
            else:
                new_image[i][j] = 2 * (-pixel) - 1
    return new_image


def reverse_map_to_positive_integers(image: np.ndarray) -> np.ndarray:
    new_image = np.zeros(image.shape, dtype=np.int16)
    for i, row in enumerate(image):
        for j, pixel in enumerate(row):
            if pixel % 2 != 0:
                new_image[i][j] = -(pixel + 1) / 2
            else:
                new_image[i][j] = pixel / 2

    return new_image


def load_pgm_file(file_path: str) -> np.ndarray:
    with open(file_path, "rb") as pgmf:
        file = plt.imread(pgmf)

    return file


def differential_code_left(image: np.ndarray, offset: int) -> np.ndarray:
    """
        Formula for differential coding using left neighbour
        output[i][j] = image[i][j] - offset,            for j=0, offset=128
        output[i][j] = image[i][j] - image[i][j-1],     for j>0
    """
    image = np.copy(image)
    column = np.repeat(offset, image.shape[0])
    prediction = np.column_stack((column, image[:, :-1]))
    return (image - prediction).astype(np.int16)
