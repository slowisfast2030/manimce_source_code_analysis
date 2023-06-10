from calculator import add

def main():
    x = 3.0
    y = 4.0
    result = add(x, y)
    print(f"The result of adding {x} and {y} is {result}")

if __name__ == "__main__":
    main()

'''
这里给出了calculator包的两种用法:
python -m calculator 3 4 add
python add.py
'''
