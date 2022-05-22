import numpy as np

from bitarray import bitarray


class ExpGolombCoder:
    """
    The Exponential golomb coder
    """

    def __init__(self, k: int) -> None:
        self.k = k

    def encode_str(self, value: int) -> str:
        q_number = self._calculate_q_number(value)
        r_number = self._calculate_r(value, q_number)
        prefix = "0" * q_number + "1"
        num_significant_bits = self.k + q_number
        format_specification = "0" + str(num_significant_bits) + "b"
        if self.k == 0 and value == 0:
            postfix = ""
        else:
            postfix = format(r_number, format_specification)

        return prefix + "|" + postfix

    def decode_str(self, code: str) -> int:
        separator_index = code.find("|")
        prefix, postfix = code[:separator_index], code[separator_index + 1 :]
        q = prefix.count("0")
        k = len(postfix) - q
        r = int(postfix, 2) if postfix else 0
        value = r - 2**k * (1 - 2**q)
        return value

    def encode(self, value: int) -> bitarray:
        encoded = self.encode_str(value).replace("|", "")
        return bitarray(encoded)

    def decode(self, bitarray_code: bitarray) -> int:
        string_code = bitarray_code.to01()
        first_one_index = string_code.find("1")
        string_code_with_separator = (
            string_code[: first_one_index + 1]
            + "|"
            + string_code[first_one_index + 1 :]
        )

        return self.decode_str(string_code_with_separator)

    def encode_image(self, image: np.ndarray) -> list[list[bitarray]]:
        # encoded = np.zeros(image.size)
        # for i, row in enumerate(image):
        #     for j, value in enumerate(row):
        #         encoded[i][j] = self.encode(value)

        return [[self.encode(value) for value in row] for row in image]

    def decode_encoded_image(self, encoded_image: list[list[bitarray]]) -> np.ndarray:
        return np.array(
            [[self.decode(value) for value in row] for row in encoded_image]
        )

    def _calculate_q_number(self, value: int) -> int:
        return int(np.floor(np.log2(value / 2**self.k + 1)))

    def _calculate_r(self, value: int, q: int) -> int:
        return value + 2**self.k * (1 - 2**q)

    def word_length(self, value: int) -> int:
        q_number = self._calculate_q_number(value)
        return self.k + 2 * q_number + 1
