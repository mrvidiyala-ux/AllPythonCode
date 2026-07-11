Name = input("Enter your Name: ")
Grade = int(input("Enter your Class: "))
Sec = input("Enter your Section: ")
Age = int(input("Enter your Age: "))

English = int(input("Enter your English Marks: "))
Second_Language = int(input("Enter your 2nd Language Marks: "))
Maths = int(input("Enter your Maths Marks: "))
Science = int(input("Enter your Science Marks: "))
Social_Studies = int(input("Enter your Social Studies Marks: "))
Computer = int(input("Enter your Computer Marks: "))
Third_Language = int(input("Enter your 3rd Language Marks: "))

Total_Marks = English + Second_Language + Maths + Science + Social_Studies + Computer + Third_Language
Percentage = (Total_Marks / 700) * 100

print("\n----- Student Report Card -----")
print("Name: ", Name)
print("Class: ", Grade)
print("Section: ", Sec)
print("Age: ", Age)
print("Total Marks: ", Total_Marks, "/ 700")
print("Percentage:", Percentage)
if Percentage >= 70:
    Grade = 'A+'
elif Percentage >= 60:
    Grade = 'A'
elif Percentage >= 50:
    Grade = 'B+'
elif Percentage >= 40:
    Grade = 'B'
elif Percentage >= 30:
    Grade = 'C'
else:
    Grade = 'F'

print("Grade: ", Grade)