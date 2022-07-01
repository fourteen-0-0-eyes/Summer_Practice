import unittest

from Source import compress, decompress


input_data_path = ["data1", "data2", "data3"]
out_path = "data.pzip"
compress_level = 5

class TestMethod(unittest.TestCase):

    def test_compress_size(self):
        import sys, os
        input_size = 0
        output_size = 0
        for data_path in input_data_path:
            with open(data_path, mode="rb") as fdata:
                input_size += sys.getsizeof(fdata.read())

        compress(out_path, compress_level, *input_data_path)

        with open(out_path, mode="rb") as fcdata:
            output_size = sys.getsizeof(fcdata.read())

        if os.path.exists(out_path):
            os.remove(out_path)
        self.assertLess(output_size, input_size)

    def test_decompress_integrity(self):
        import os
        decompress_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decompressed")
        input_hash_sum = 0
        output_hash_sum = 0
        for data_path in input_data_path:
            with open(data_path, mode="rb") as fdata:
                input_hash_sum += hash(fdata.read())

        compress(out_path, compress_level, *input_data_path)
        decompress(out_path, decompress_path)

        for data_path in input_data_path:
            with open(os.path.join(decompress_path, data_path), mode="rb") as fdata:
                output_hash_sum += hash(fdata.read())
        self.assertEqual(input_hash_sum, output_hash_sum)


if __name__ == "__main__":
    unittest.main()
