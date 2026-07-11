print("Welcome to Library!")
name = input("Enter your name: ")

print("\nBooks:")
print("1. Python Guide")
print("2. Math Fun")
print("3. Science Book")

choice = input("Pick 1, 2, or 3: ")

if choice == "1":
    print(name + " got Python Guide")
elif choice == "2":
    print(name + " got Math Fun")
elif choice == "3":
    print(name + " got Science Book")
else:
    print("Wrong!")