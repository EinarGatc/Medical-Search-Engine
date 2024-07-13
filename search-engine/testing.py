def write_to_txt(file, tokens):
    last_token = None
    file.seek(0)
    file.truncate()
    for token in tokens:
        current_pointer = file.tell()
        if last_token and token == last_token:
            file.seek(current_pointer-1)
        file.write(token+"\n")
        last_token = token
    
if __name__ == "__main__":
    with open("test.txt", "r+") as f:
        write_to_txt(f,["allow", "crash", "crash", "create", "determine"])