def transfer(in_path, out_path):
    in_file = open(in_path, "r")
    file_content = in_file.read()
    in_file.close()

    out_file = open(out_path, "w")
    out_file.write(file_content)
    out_file.close()
