# # calculator/__main__.py

# import argparse
# from calculator import add, subtract, multiply, divide

# def main():
#     # Create an argument parser
#     parser = argparse.ArgumentParser(description="A simple calculator")

#     # Add arguments for two numbers
#     parser.add_argument("x", type=float, help="The first number")
#     parser.add_argument("y", type=float, help="The second number")

#     # Add an argument for the operation
#     parser.add_argument("operation", choices=["add", "subtract", "multiply", "divide"], help="The operation to perform")

#     # Parse the arguments
#     args = parser.parse_args()

#     # Perform the operation
#     if args.operation == "add":
#         result = add(args.x, args.y)
#     elif args.operation == "subtract":
#         result = subtract(args.x, args.y)
#     elif args.operation == "multiply":
#         result = multiply(args.x, args.y)
#     elif args.operation == "divide":
#         result = divide(args.x, args.y)

#     # Print the result
#     print(f"The result of {args.operation}ing {args.x} and {args.y} is {result}")

# if __name__ == "__main__":
#     main()

####################################################################################################
# calculator/__main__.py
# python -m calculator 3 4 add
import click
from calculator import add, subtract, multiply, divide

@click.command()
@click.argument("x", type=float)
@click.argument("y", type=float)
@click.argument("operation", type=click.Choice(["add", "subtract", "multiply", "divide"]))
def main(x, y, operation):
    # Perform the operation
    if operation == "add":
        result = add(x, y)
    elif operation == "subtract":
        result = subtract(x, y)
    elif operation == "multiply":
        result = multiply(x, y)
    elif operation == "divide":
        result = divide(x, y)

    # Print the result
    click.echo(f"The result of {operation}ing {x} and {y} is {result}")

if __name__ == "__main__":
    main()
