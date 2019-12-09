import os
import unittest
from CryptoFactory.CFFile import *


class TestFile(unittest.TestCase):
    def test_file_split_merge(self):
        md5_value = get_file_md5('./testdata/test.mp4')
        file_split('./testdata/test.mp4', './testdata/test_split.mp4', 100 * 1024 * 1024)

        sub_files_count = 0
        for file_path in os.listdir('./testdata/'):
            if 'test_split.mp4' in file_path:
                sub_files_count += 1

        file_merge('./testdata/test_split.mp4', './testdata/test_merge.mp4', sub_files_count)
        merge_md5_value = get_file_md5('./testdata/test_merge.mp4')
        self.assertEqual(md5_value, merge_md5_value)
        for num in range(1, sub_files_count + 1):
            os.remove('./testdata/test_split.mp4.' + str(num))

        os.remove('./testdata/test_merge.mp4')


if __name__ == '__main__':
    unittest.main()
