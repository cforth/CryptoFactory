import os
import unittest
from CryptoFactory.File import *


class TestFile(unittest.TestCase):
    def test_file_split_merge(self):
        md5_value = get_file_md5('./testdata/test.mp4')
        file_split('./testdata/test.mp4', './testdata/test_split.mp4', 100*1024*1024)
        file_merge('./testdata/test_split.mp4', './testdata/test_merge.mp4', 5)
        merge_md5_value = get_file_md5('./testdata/test_merge.mp4')
        self.assertEqual(md5_value, merge_md5_value)
        os.remove('./testdata/test_split.mp4.1')
        os.remove('./testdata/test_split.mp4.2')
        os.remove('./testdata/test_split.mp4.3')
        os.remove('./testdata/test_split.mp4.4')
        os.remove('./testdata/test_split.mp4.5')
        os.remove('./testdata/test_merge.mp4')


if __name__ == '__main__':
    unittest.main()
