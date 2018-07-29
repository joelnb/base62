import pytest

import base62


bytes_int_pairs = [
    (b'\x00', 0),
    (b'\x01', 1),
    (b'\x01\x01', 0x0101),
    (b'\xff\xff', 0xffff),
    (b'\x01\x01\x01', 0x010101),
    (b'\x01\x02\x03\x04\x05\x06\x07\x08', 0x0102030405060708),
]


def test_basic():
    assert base62.encode(0) == '0'
    assert base62.encode(0, minlen=0) == '0'
    assert base62.encode(0, minlen=1) == '0'
    assert base62.encode(0, minlen=5) == '00000'
    assert base62.decode('0') == 0
    assert base62.decode('0000') == 0
    assert base62.decode('000001') == 1

    assert base62.encode(34441886726) == 'base62'
    assert base62.decode('base62') == 34441886726


def test_basic_inverted():
    kwargs = {'charset': base62.CHARSET_INVERTED}

    assert base62.encode(0, **kwargs) == '0'
    assert base62.encode(0, minlen=0, **kwargs) == '0'
    assert base62.encode(0, minlen=1, **kwargs) == '0'
    assert base62.encode(0, minlen=5, **kwargs) == '00000'
    assert base62.decode('0', **kwargs) == 0
    assert base62.decode('0000', **kwargs) == 0
    assert base62.decode('000001', **kwargs) == 1

    assert base62.encode(10231951886, **kwargs) == 'base62'
    assert base62.decode('base62', **kwargs) == 10231951886

    # NOTE: For backward compatibility. When I first wrote this module in PHP,
    # I used to use the `0z` prefix to denote a base62 encoded string (similar
    # to `0x` for hexadecimal strings).
    assert base62.decode('0zbase62', **kwargs) == 10231951886


@pytest.mark.parametrize('b, i', bytes_int_pairs)
def test_bytes_to_int(b, i):
    assert base62.bytes_to_int(b) == i


@pytest.mark.parametrize('b, i', bytes_int_pairs)
def test_encodebytes(b, i):
    assert base62.encodebytes(b) == base62.encode(i)


@pytest.mark.parametrize('s', ['0', '1', 'a', 'z', 'ykzvd7ga'])
def test_decodebytes(s):
    assert base62.bytes_to_int(base62.decodebytes(s)) == base62.decode(s)


@pytest.mark.parametrize('input_bytes', [
    b'', b'0', b'bytes to encode', b'\x01\x00\x80'])
def test_roundtrip(input_bytes):
    """Ensures type consistency. Suggested by @dhimmel"""
    base62_encoded = base62.encodebytes(input_bytes)
    assert isinstance(base62_encoded, str)
    output_bytes = base62.decodebytes(base62_encoded)
    assert isinstance(output_bytes, bytes)
    assert input_bytes == output_bytes
