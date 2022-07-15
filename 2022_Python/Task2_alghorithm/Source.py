import random
import os


def compress(output_path: str, *file_paths: str):
    file_name_lines = []
    num_lines_sum = 0
    if os.path.exists(output_path):
        os.remove(output_path)
    for file_path in file_paths:
        with open(file_path, mode="rb") as fin, open(output_path, mode="ab") as fout:
            data = fin.read()
            fout.write(compress_bytes(data))
            path_line = f"\n{os.path.basename(file_path)}\n"
            fout.write(path_line.encode('utf-8'))
        with open(output_path, mode="rb") as fin:
            num_lines = len(fin.readlines()) - num_lines_sum
            num_lines_sum += num_lines
            file_name_lines.append(num_lines - 1)
    with open(output_path, mode="a+") as fout:
        fout.write(" ".join(map(str, file_name_lines)))
        

def decompress(path: str, output_path: str=os.path.dirname(os.path.abspath(__file__))):
    if not (os.path.exists(output_path)):
        os.makedirs(os.path.dirname(f"{output_path}\\"), exist_ok=True)
    with open(path, mode="rb") as fin:
        data = fin.readlines()
        file_name_lines = [int(x) for x in data[-1].decode('utf-8').split(' ')]
        for data_block_index in file_name_lines:
            file_name = data[data_block_index].decode('utf-8').removesuffix("\n")
            data[data_block_index - 1] = data[data_block_index - 1].removesuffix(b"\n")
            data_block = b''.join(data[:data_block_index])
            decompressed_data = decompress_bytes(data_block)
            data = data[data_block_index + 1:]
            with open(os.path.join(output_path, file_name), mode="wb+") as fout:
                fout.write(decompressed_data)


def compress_bytes(uncompressed: bytes):
    dictionary = {}

    depth = 10
    height = 20
    step = 10

    word_index = 0
    local_shift = height
    
    while local_shift >= depth:
        data = uncompressed
        while word_index + local_shift < len(uncompressed):
            data = uncompressed
            word = uncompressed[word_index:word_index + local_shift]
            index = data.find(word)
            indexes = []
            while index != -1:
                count = len(indexes)
                indexes.append(index)
                data = data.replace(word, b'', 1)
                index = data.find(word)
            count = len(indexes)
            if count > 5:
                uncompressed = data
                dictionary[word] = indexes
            else: word_index += step
        local_shift -= 1

    chars = [chr(x).encode("raw_unicode_escape").decode('unicode_escape') for x in random.sample(range(65, 90), 3)]
    keys_str = b''.join(dictionary)
    while True:
        c1 = keys_str.find((f'~{chars[0]}').encode())
        c2 = keys_str.find((f':{chars[1]}').encode())
        c3 = keys_str.find((f';{chars[2]}').encode())
        if c1 + c2 + c3 == -3:
            break
        chars = [chr(x) for x in random.sample(range(65, 90), 3)]
        
    append_str = f"~{chars[0]}"
    for key, value in dictionary.items():
        append_str += f"{key.decode('unicode_escape')}:{chars[1]}"
        for i in value:
            append_str += f"{i},"
        append_str = append_str[:-1] + f";{chars[2]}"
    append_str += chars[0] + chars[1] + chars[2]
    
    return uncompressed + append_str.encode("raw_unicode_escape")


def decompress_bytes(compressed: bytes):
    chars = [chr(compressed[-3]), chr(compressed[-2]), chr(compressed[-1])]
    compressed = compressed[:-3]
    index = compressed.rfind((f'~{chars[0]}').encode())
    str_dict = compressed[index + 2:].decode('unicode_escape').split(f';{chars[2]}')
    compressed = compressed[:index]
    del(str_dict[-1])
    dictionary = {}
    for value in str_dict:
        data = value.split(f':{chars[1]}')
        indexes = []
        for index in data[1].split(','):
            indexes.append(int(index))
        dictionary[data[0].encode("raw_unicode_escape")] = indexes

    for key, value in reversed(dictionary.items()):
        for i in reversed(value):
            compressed = compressed[0: i] + key + compressed[i:]
            
    return compressed

def main():
    print()


if __name__ == "__main__":
    main()
