import re

def check_first_matching_bracket (str):
    for d in str:
        if d == "(":
            return False
        if (d == ")"):
            return True

def classify_number_pattern (str):
    number_pattern = r'(\d+)\s*\.\s*(.*)'
    data = re.findall (number_pattern, str)
    return data

def classify_letter_pattern (str):
    letter_pattern = r'([A-Za-z]+)\s*\)\s*(.*)'
    if (check_first_matching_bracket (str)): #avoid cases like this: (string) that can be classified
        data = re.findall (letter_pattern, str)
        return data
    return False
    
def classify_number_letter_pattern (str):
    number_letter_pattern = r'(\d+)\s*\.\s*([A-Za-z]+)\s*\)\s*(.*)'
    data = re.findall (number_letter_pattern, str)
    return data


def classify_description (str): #we will return string here if its the title, and re will return True if those are closing brackets
    description_pattern = r'```(.*)'
    data = re.findall (description_pattern, str)
    return data

def t1_classify_line (str): #t1 - stands for type one constructor
    data = classify_number_letter_pattern (str)
    if (data):
        data.append (3)
        return data
    
    data = classify_number_pattern (str)
    if (data): #we also check if its accidentaly not the second type

        comparsion_data = classify_letter_pattern (str) #some identifier to avoid misclasifications
        if (comparsion_data and len (comparsion_data[0] [1]) > len (data[0] [1]) ): #we check if the algorithm confused, in cases of a) 235.3 may be classified as number
            data = comparsion_data
            data.append (2)
        
        else: 
            data.append (1)

        return data

    data = classify_letter_pattern (str)
    # if (data and re.match ('^\s*[a-zA-Z]+\)', str)):
    if (data):
        data.append (2)
        return data
    
    data = classify_description (str)
    if (data):
        data.append (4) #id 4 is for the description
        return data
    
    
    
    return False


# data = {}
# data["1"] = ["Is earth flat?",{"A" : ["Yes", True], "B" : ["No", False] }] #[1][0] is the title
# data ["1"] [1] ["C"] = ["Maybe", False]
# # print (data ["1"][1]["C"] [0])


def t1_data_constructor (str):
    data = {}
    question_id = ""
    lines = lines = [line for line in str.splitlines() if line.strip()] #each line as an separate element in array, empty rows removed
   #specifically for description
    current_question_id = False #not directly connected with the description but used inside the description
    description_opened = False
    current_description = ""
    current_description_title =""

    for line in lines:
        
        classified_line = t1_classify_line (line)
        if (classified_line):

            if (classified_line [1] == 1): #case 1
                #in this case we should add option when there are no numbers in the title
                question_id = classified_line [0][0]
                question_content = classified_line [0][1]
                data [question_id] = [question_content, {}]
                current_question_id = question_id

            elif(classified_line [1] == 2 and question_id in data): #case 2
                answer_id = classified_line [0][0]
                answer_content = classified_line [0][1]
                data [question_id][1][answer_id] = [answer_content, False]

            elif (classified_line [1] == 3): #case 3
                local_question_id = classified_line [0][0]
                local_answer_id = classified_line [0][1]
            
                if local_question_id in data and local_answer_id in data [local_question_id][1]:
                    data [local_question_id][1][local_answer_id][1] = True
        
            elif classified_line [1] == 4 and current_question_id: #if we recognize the description

                if (classified_line [1] == 4):
                    
                    if (description_opened):
                        description_opened = False
                        data [current_question_id].append (current_description_title)
                        data [current_question_id].append (current_description)
                        current_description_title = ""
                        current_description = ""
                        
                    else: 
                        description_opened = True
                        current_description_title = classified_line [0]
        
        elif (description_opened): #we add description if its added
            current_description += line+"\n"
    return data




# tests = """
# Sure, here's a Python programming quiz with code snippets:

# ---

# **Question 1:**

# 1.What will be the output of the following code snippet?

# ```python
# x = 10
# y = 3
# result = x / y
# print(result)
# ```

# a) 3.3333333333333335  
# b) 3.33  
# c) 3.0  
# d) 3

# **Question 2:**

# 2.What is the correct way to open a file named "data.txt" in Python for reading?

# a) `file = open("data.txt", "r")`  
# b) `file = open("data.txt", "w")`  
# c) `file = open("data.txt", "rb")`  
# d) `file = open("data.txt", "a")`

# **Question 3:**

# 3.What will be the value of `my_list` after executing the following code?

# ```python
# my_list = [1, 2, 3, 4, 5]
# my_list[1:3] = [7, 8, 9]
# ```

# a) [1, 2, 3, 4, 5]  
# b) [1, 7, 8, 9, 4, 5]  
# c) [1, 7, 8, 9]  
# d) [1, 2, 7, 8, 9, 4, 5]

# **Question 4:**

# 4.Which of the following is a valid way to check if a key exists in a dictionary?

# a) `if key in dict:`  
# b) `if dict.exists(key):`  
# c) `if key.exists(dict):`  
# d) `if key.exists_in(dict):`

# **Question 5:**

# 5.What will be the output of the following code?

# ```python
# def foo(x, lst=[]):
#     lst.append(x)
#     return lst

# print(foo(1))
# print(foo(2))
# ```

# a) [1] [2]  
# b) [1, 2] [2]  
# c) [1] [1, 2]  
# d) [1, 2] [1, 2]

# ---

# **Answers:**

# 1. a) 3.3333333333333335
# 2. a) `file = open("data.txt", "r")`
# 3. d) [1, 2, 7, 8, 9]
# 4. a) `if key in dict:`
# 5. d) [1, 2] [1, 2]

# ---

# Feel free to ask if you have any doubts about the quiz questions or answers!
# """

# tt = [
# "1. What is the primary goal of Object-Oriented Programming (OOP)?",
# "b) 3.0",
# "c) 3",
# "d) Error"
# ]
# dd = t1_classify_line ("printresult)")
# print (dd)

# print (t1_data_constructor (tests))
# print (check_first_matching_bracket ("dsadsa)"))


# print (classify_description (" ``` dsasda"))
       




