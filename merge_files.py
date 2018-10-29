import sys
import re

def merge(file1, file2):
    file1_string = file_to_string(file1)
    file2_string = file_to_string(file1)

    # print(file1_string)
    # print(file2_string)

    # for word, pair in zip(file1_string.split(" "), get_two_words(file2_string)):
    for word, pair in zip(file1_string.split(" "), file2_string.split(" ")):
        print(word, pair)

def file_to_string(file1):
    string = ''
    with open(file1, "r") as f:
        string = f.read()
    return string

def get_two_words(some_string):
    split_pairs = re.split("(\w[\w'])+(\w[\w'])* ", some_string )
    for word in split_pairs:
        # print(word)
        yield word
    # counter = 0
    # string = ""
    # for word in some_string.split(" "):
    #     string = string + " " + word
    #     if counter == 0:
    #         counter = counter + 1
    #     if counter == 1:
    #         counter = 0
    #         yield string



if __name__ == '__main__':
    file1_name = sys.argv[1]
    file2_name = sys.argv[2]
    merge(file1_name, file2_name)