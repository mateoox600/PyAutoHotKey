from PyAutoHotKey import PyAutoHotKey

def main():
    instance = PyAutoHotKey()

    instance.execute_file('../test.key')

if __name__ == '__main__':
    main()