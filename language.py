make str1 = "this programming lang is just for fun"

print({str1})

make str2 = "its capabilities are cool tho"

print({str2})



make num1 = 5.5

make num2 = 20

make num3 = 5

make num4 = 10

make num5 = 12

make num6 = 6

make result = 0

set result = calc num1 + num2 * num3 / num4 - num5 + num6
// 5 + 20 * 5 / 10 - 12 + 6
// expected result is 9


print("Lets do test out the langauge by doing some math: " + {num1} + "+" + {num2} + "x" + {num3} + "/" + {num4} + "-" + {num5} + "+" + {num6})
print("the expected result is 9.5")
print("the calculated result is " + {result})
print("hopefully the two results match up")

print("next operation ")

blank()

set num1 = 10

set result = calc num1 + num2 * num3 / num4 - num5 + num6
// 5 + 20 * 5 / 10 - 12 + 6
// expected result is -1


print("Lets do some more math!" + {num1} + "+" + {num2} + "x" + {num3} + "/" + {num4} + "-" + {num5} + "+" + {num6})
print("the expected result is -6")
print("the calculated result is " + {result})
print("hopefully the two results match up")

nl()

loop i, 5
print("We can loop too")
print({result})
end

el();

print("LOOK! We can even take input")

input(userInput, "Say something, I'll say it back!")

print("'", {userInput}, "'" )
end

el()

print("We can delete variables too")
print("Here is a list of all the variables in our project:")
rh.variables.list()
print("And now we delete the result variable:")
del result
rh.variables.list()
