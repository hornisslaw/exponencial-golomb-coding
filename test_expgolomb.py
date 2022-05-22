import pytest
import numpy as np

from expgolomb import ExpGolombCoder


@pytest.mark.parametrize(
    ('input_image'),
    (
        pytest.param(np.array([]), id='empty'),
        pytest.param(np.ones((2, 2), dtype=np.int32), id='ones'),
        pytest.param(np.array([[1, 2], [3, 4]], dtype=np.int32), id='array'),
    ),
)
def test_codec_flow(input_image):
    exp_golomb = ExpGolombCoder(k=2)
    enc = exp_golomb.encode_image(input_image)
    dcd = exp_golomb.decode_encoded_image(enc)
    assert np.array_equal(input_image, dcd)


@pytest.mark.parametrize(
    ('k', 'value', 'expected'),
    (
        pytest.param(0, 6, '001|11'),
        pytest.param(2, 2, '1|10'),
        pytest.param(0, 0, '1|'),
        pytest.param(1, 0, '1|0'),
        pytest.param(2, 0, '1|00'),
        pytest.param(3, 0, '1|000'),
    ),
)
def test_encode_value(k, value, expected):
    exp_golomb = ExpGolombCoder(k=k)
    assert exp_golomb.encode_str(value) == expected


@pytest.mark.parametrize(
    ('k', 'code', 'expected'),
    (
        pytest.param(1, '001|001', 7),
        pytest.param(2, '1|10', 2),
        pytest.param(0, '1|', 0),
        pytest.param(0, '01|0', 1),
    ),
)
def test_decode_value(k, code, expected):
    exp_golomb = ExpGolombCoder(k=k)
    assert exp_golomb.decode_str(code) == expected
