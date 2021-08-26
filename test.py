from data import data

def test_forloop():
    for i in range(10):
        print(i)

def print_titles():
    """
    Method to learn for loops in python
    1 - import data
    2 - for loop for data list
    3 - print the object
    """

  
    for prod in data:
        print(prod["title"])


def run_test(): 
    print("Running tests")

    #test_forloop()
    print_titles()

run_test()
