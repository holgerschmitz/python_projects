# Numbers are very important in computer programming.
# You will learn later how numbers can be used to represent all sorts of things.

# Just as with strings, you use variables to store numbers

my_number = 17

# And you can use the print function to write them

print(my_number)

# You can do calculations with numbers

result = my_number / 2 + 5
print(result)

# You can see that result has a part behind the decimal point

# 1) Try the same thing, but change my_number to an even number
#    Look closely at the way the two numbers are printed.
#    Do you notice any difference?

# Python has two different types of numbers: integer and floating point
# Integers store whole numbers
# Floating point numbers are used for numbers that can have a fractional part
#
# Integers and floating point numbers are stored in different ways in the computer memory.
# Integers are often simply called "int" or "ints".
# Floating point numbers are often simply called "float" or "floats".
#
# When dividing two numbers ...
#    my_number / 2
# ... the result will always be a float.

# Remember from the last lesson that you can multiply a string with a number
# You can use a variable for this as well

print("." * my_number)

# 2) Now try this with "result"
#    print("." * result)
#    You are getting an error message. What do you think it means?

# You can convert a float to an int using the "int" function

other_number = int(result)
print(other_number)

# Notice how the decimal point is gone.

# 3) Use the "input" function from the last lesson to ask the user for a number.
#    Can you use that number for calculations?
#    Why not?
#
# 4) The "input" function returns a string. 
#    Try using the "int" function to turn it into a number.
#    Now use the result for a calculation.

# In the last lesson you added strings to print out a message.
# 5) Now try this:
#    print("The result is " + result)

# You are getting an error message because you are trying to add a number to a string.
# You need to convert the number to a string first.
# You can use the "str" function to do this.

message = str(result)
print("The result is " + message)

# You can also do this in a single line
print("The result is " + str(result))

# 6) The to convert temperatures from degrees Farenheit to degrees Celsius
#    you first subtract 32 and then multiply by 5/9.
#    Write a program that asks the user for a temperature in Farenheit
#    and calculates the Celsius temperature

# 7) Extend the program from 6) to write out nice message like 
#    "68° Farenheit is 20° Celsius"

# 8) Now extend the program further to display a temperature scale. 
#    For example if the Celcius temperature is 25°, print the following.
#
#    ---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
#    ######################### 25°C
#
#    Use string multiplication to achieve this.
