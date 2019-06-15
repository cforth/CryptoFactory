import os
import hashlib


# 文件MD5值生成
def get_file_md5(filename):
    if not os.path.isfile(filename):
        raise ValueError('Input file path not exists: %s ', filename)

    my_hash = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            my_hash.update(b)

    return my_hash.hexdigest()


def file_split(file_path, output_file_path, size):
    if not os.path.exists(file_path):
        raise ValueError('Input file path not exists: %s ', file_path)

    all_len = os.path.getsize(file_path)
    num = all_len // size if all_len % size == 0 else (all_len // size) + 1
    index = 0
    with open(file_path, 'rb') as f:
        for i in range(0, num):
            index += 1
            # 每次读取size_block大小的数据，防止内存不够
            size_block = 10 * 1024 * 1024
            size_block_num = size // size_block if size % size_block == 0 else (size // size_block) + 1
            for x in range(0, size_block_num):
                data = f.read(size_block)
                if not data:
                    break
                with open(output_file_path + '.' + str(index), 'ab') as out:
                    out.write(data)


def file_merge(file_path, output_file_path, num):
    if os.path.exists(output_file_path):
        raise ValueError('Output file path exists: %s ', output_file_path)

    with open(output_file_path, 'ab') as out:
        for i in range(1, num + 1):
            with open(file_path + '.' + str(i), 'rb') as f:
                size = os.path.getsize(file_path + '.' + str(i))
                # 每次读取size_block大小的数据，防止内存不够
                size_block = 10 * 1024 * 1024
                size_block_num = size // size_block if size % size_block == 0 else (size // size_block) + 1
                for x in range(0, size_block_num):
                    data = f.read(size_block)
                    if not data:
                        break
                    out.write(data)
