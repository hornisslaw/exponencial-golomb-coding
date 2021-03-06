import argparse
import matplotlib.pyplot as plt
import numpy as np

from typing import Optional, Sequence

from expgolomb import ExpGolombCoder
from utils import (
    calculate_compression_rate,
    calculate_entropy,
    calculate_histogram,
    average_code_bit_length,
    display_histogram,
    display_image,
    differencial_encode,
    differencial_decode,
    differential_code_left,
    map_to_positive_integers,
    reverse_map_to_positive_integers,
    load_pgm_file
)

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file_path")
    parser.add_argument("-k", "--k_parameter")
    parser.add_argument("-d", "--diff_encoding_mode")
    args = parser.parse_args(argv)

    pgm_file = load_pgm_file(file_path=args.file_path)
    # display_image(pgm_file)
    diff_mode = args.diff_encoding_mode

    if diff_mode == "mean":
        offset = int(np.average(pgm_file))
        print(f"Offset: {offset}")
        diff = differencial_encode(pgm_file, offset)
        pgm_file = map_to_positive_integers(diff)
    elif diff_mode == "left":
        diff = differential_code_left(pgm_file, offset=128)
        pgm_file = map_to_positive_integers(diff)
    else:
        print("Skipping differential coding")

    k = int(args.k_parameter)
    exp_golomb = ExpGolombCoder(k)
    enc = exp_golomb.encode_image(pgm_file)
    dcd = exp_golomb.decode_encoded_image(enc)

    print(f"{calculate_entropy(pgm_file)=}")
    print(f"{average_code_bit_length(enc)=}")
    print(f"{calculate_compression_rate(pgm_file, enc, bits=8)=}")
    # print(f"input: {pgm_file}")
    # print(f"encoded: {enc}") <- better not to print this :)
    # print(f"decoded: {dcd}")

    histogram = calculate_histogram(pgm_file, num_values=256)
    file_name = args.file_path.split("\\")[-1]
    histogram_title = f"Histogram dla danych z pliku {file_name}"
    # display_histogram(histogram, num_values=256, title=histogram_title)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
