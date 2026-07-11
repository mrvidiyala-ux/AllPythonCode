Name = input("Enter your Name: ")
Grade = int(input("Enter your Class: "))
Sec = input("Enter your Section: ")
Age = int(input("Enter your Age: "))

English = int(input("Enter your English Marks (out of 80): "))
Second_Language = int(input("Enter your 2nd Language Marks (out of 80): "))
Maths = int(input("Enter your Maths Marks (out of 80): "))
Science = int(input("Enter your Science Marks (out of 80): "))
Social_Studies = int(input("Enter your Social Studies Marks (out of 80): "))
Computer = int(input("Enter your Computer Marks (out of 80): "))
Third_Language = int(input("Enter your 3rd Language Marks (out of 80): "))

# Input validation
subjects = [English, Second_Language, Maths, Science, Social_Studies, Computer, Third_Language]
for mark in subjects:
    if mark < 0 or mark > 80:
        print("Error: Marks should be between 0 and 80")
        exit()

Total_Marks = English + Second_Language + Maths + Science + Social_Studies + Computer + Third_Language
Percentage = (Total_Marks / 560) * 100

print("\n----- Student Report Card -----")
print("Name: ", Name)
print("Class: ", Grade)
print("Section: ", Sec)
print("Age: ", Age)
print("\n----- Subject Wise Marks (Out of 80) -----")
print("English:", English)
print("Second Language:", Second_Language)
print("Mathematics:", Maths)
print("Science:", Science)
print("Social Studies:", Social_Studies)
print("Computer:", Computer)
print("Third Language:", Third_Language)
print("\nTotal Marks: ", Total_Marks, "/ 560")
print("Percentage:", round(Percentage, 2), "%")

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

print("Grade:", Grade)
