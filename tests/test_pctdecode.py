import unittest

from pctdecode import Decoder
from urlapi import Url


class TestDecoder(unittest.TestCase):
    def test_plain_text(self):
        self.assertEqual(Decoder().decode("abc"), "abc")

    def test_plus_becomes_space(self):
        self.assertEqual(Decoder().decode("a+b"), "a b")

    def test_space_percent(self):
        self.assertEqual(Decoder().decode("a%20b"), "a b")

    def test_stats_shape(self):
        self.assertIn("errors", Decoder().stats())

    def test_url_wraps_decoder(self):
        url = Url()
        self.assertEqual(url.decoder.decode("a+b"), "a b")


if __name__ == "__main__":
    unittest.main()
