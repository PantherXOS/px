from sys import stdout
import px

def main():
    r = px.main()
    stdout.flush()
    if type(r) == str:
        stdout.write(r)
    elif r == None:
        pass
    else:
        stdout.buffer.write(r)
    stdout.flush()

if __name__ == '__main__':
    main()
