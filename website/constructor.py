import re


def classify_number_pattern (str):
    number_pattern = r'(\d+)\s*\.\s*(.*)'
    data = re.findall (number_pattern, str)
    return data

def classify_letter_pattern (str):
    letter_pattern = r'([A-Za-z]+)\s*\)\s*(.*)'

    data = re.findall (letter_pattern, str)
    return data

def classify_number_letter_pattern (str):
    number_letter_pattern = r'(\d+)\s*\.\s*([A-Za-z]+)\s*\)\s*(.*)'
    data = re.findall (number_letter_pattern, str)
    return data


def t1_classify_line (str): #t1 - stands for type one constructor
    data = classify_number_letter_pattern (str)
    if (data):
        data.append (3)
        return data
    
    data = classify_number_pattern (str)
    if (data):
        data.append (1)
        return data

    data = classify_letter_pattern (str)
    if (data):
        data.append (2)
        return data
    
    
    
    return False


# data = {}
# data["1"] = ["Is earth flat?",{"A" : ["Yes", True], "B" : ["No", False] }] #[1][0] is the title
# data ["1"] [1] ["C"] = ["Maybe", False]
# # print (data ["1"][1]["C"] [0])


def t1_data_constructor (str):
    data = {}
    question_id = ""
    lines = str.splitlines() #each line is in array
    for line in lines:
        classified_line = t1_classify_line (line)
        if (classified_line):

            if (classified_line [1] == 1):
                
                question_id = classified_line [0][0]
                question_content = classified_line [0][1]
                data [question_id] = [question_content, {}]

            elif(classified_line [1] == 2 and question_id in data):
                answer_id = classified_line [0][0]
                answer_content = classified_line [0][1]
                data [question_id][1][answer_id] = [answer_content, False]

            elif (classified_line [1] == 3):
                local_question_id = classified_line [0][0]
                local_answer_id = classified_line [0][1]
            
                if local_question_id in data and local_answer_id in data [local_question_id][1]:
                    data [local_question_id][1][local_answer_id][1] = True

    return data


# tests = """
# Sure, here's a quiz about Object-Oriented Programming (OOP):

# **1. What is the primary goal of Object-Oriented Programming (OOP)?**
#    a) Faster execution of programs
#    b) Better organization and structure of code
#    c) Smaller executable file sizes
#    d) Easier debugging process

# **2. Which concept in OOP refers to bundling data and methods that operate on the data into a single unit?**
#    a) Inheritance
#    b) Encapsulation
#    c) Polymorphism
#    d) Abstraction

# **3. Which principle of OOP states that a subclass can override methods of its superclass?**
#    a) Encapsulation
#    b) Polymorphism
#    c) Inheritance
#    d) Abstraction

# **4. In OOP, what does the acronym 'DRY' stand for?**
#    a) Don't Repeat Yourself
#    b) Duplicate Resolution Yield
#    c) Do Remember Yourself
#    d) Define Reuse Yearly

# **5. Which OOP principle allows a class to inherit attributes and methods from another class?**
#    a) Encapsulation
#    b) Polymorphism
#    c) Abstraction
#    d) Inheritance

# **6. In Python, what keyword is used to define a new class?**
#    a) def
#    b) class
#    c) new
#    d) type

# **7. What is the term used to describe the process of creating a new instance of a class?**
#    a) Casting
#    b) Instantiating
#    c) Initializing
#    d) Constructing

# **8. Which OOP concept allows a class to have multiple methods with the same name but different parameters?**
#    a) Encapsulation
#    b) Polymorphism
#    c) Inheritance
#    d) Abstraction

# **9. Which OOP feature allows restricting access to certain components within a class?**
#    a) Inheritance
#    b) Encapsulation
#    c) Polymorphism
#    d) Abstraction

# **10. What is the term for defining a new class using an existing class as a template, allowing the new class to inherit properties and behaviors of the existing class?**
#     a) Encapsulation
#     b) Polymorphism
#     c) Inheritance
#     d) Abstraction

# **Answers:**
# 1. b) Better organization and structure of code
# 2. b) Encapsulation
# 3. c) Inheritance
# 4. a) Don't Repeat Yourself
# 5. d) Inheritance
# 6. b) class
# 7. b) Instantiating
# 8. b) Polymorphism
# 9. b) Encapsulation
# 10. c) Inheritance

# Feel free to use this quiz for testing your knowledge or for educational purposes!
# """




# dd = t1_data_constructor(tests)
# print (dd)
# dd = t1_classify_line ("**a) What is the primary goal of Object-Oriented Programming 2. dsads ?**")
# print (dd)


       




