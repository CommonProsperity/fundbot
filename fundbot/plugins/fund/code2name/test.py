import code2name

if __name__ == "__main__":
    while True:
        inp = input("Input the name ")
        print(code2name.getCodeByName(inp, relative_path='.'))


