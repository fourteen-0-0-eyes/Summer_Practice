import zlib, os


def compress(output_path: str, level: int, *file_paths: str):
    file_name_lines = []
    num_lines_sum = 0
    if os.path.exists(output_path):
        os.remove(output_path)
    for file_path in file_paths:
        with open(file_path, mode="rb") as fin, open(output_path, mode="ab") as fout:
            data = fin.read()
            fout.write(zlib.compress(data, level))
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
            decompressed_data = zlib.decompress(data_block)
            data = data[data_block_index + 1:]
            with open(os.path.join(output_path, file_name), mode="wb+") as fout:
                fout.write(decompressed_data)


def main():
    curr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decompressed")
    compress("data.pzip", 6, "data1", "data2", "data3")
    decompress("data.pzip", output_path=curr_path)


if __name__ == "__main__":
    main()
