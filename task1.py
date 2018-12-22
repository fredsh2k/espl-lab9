import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# return dictionary of errors {error_name1 : code1, ...}
def parse_error_codes_file():
    error_codes = {}
    with open("error-codes.txt", "r") as input:
        for line in input:
            data = line.replace("\n", "").split("\t")
            if len(data) > 1:  # Ignore empty line
                error_name = data[0]
                error_grade = data[1]
                error_codes[error_name] = int(error_grade)
    return error_codes

# return list of students [{student_name1 : {error_name1 : error_value1}, ...}]
def parse_students_errors_file(error_codes):
    students_errors = []
    with open("lab10_grades.txt", "r") as input:
        for line in input:
            data = line.replace("\n", "").split("\t")
            # print(data)
            student_name = data[0]
            errors = data[1].split("|")
            student_errors = {}

            for error in errors:
                data = error.split(":")
                if len(data) > 1:
                    error_name = data[0]
                    error_value = float(data[1])
                    student_errors[error_name] = error_value
                    print(student_errors)

            student_data = {student_name: student_errors}
            students_errors.append(student_data)

    print(students_errors)
    return students_errors

# return dictionary of errors {error_name1 : frequency1, ...}
def calculate_error_frequency(students_errors):
    error_frequency = {}
    for student in students_errors:
        student_errors = list(student.values())[0]
        for error_name in student_errors.keys():
            if error_name not in error_frequency.keys():
                error_frequency[error_name] = 1
            else:
                error_frequency[error_name] += 1

    return error_frequency

# write error_name|frequency to "errorcodes.stats"
# write student_name|grade to "final_grades"
def write_dict_to_file(dictionary, file_name):
    with open(file_name, "w") as output:
        for key, value in dictionary.items():
            output.write(str(key) + "|" + str(value)+"\n")

# return dictionary of students {student_name1 : final_grade1, ...}
def calculate_student_grade(error_codes, students_errors):
    student_grades = {}
    for student in students_errors:
        student_name = list(student.keys())[0]
        student_grade = 100
        student_errors = list(student.values())[0]
        for error_name, error_value in student_errors.items():
            student_grade -= error_value * error_codes[error_name]
        student_grades[student_name] = student_grade
    return student_grades

# write error_name|frequency to "errorcodes.stats"
def write_error_statistics(error_frequency, file_name):
    write_dict_to_file(error_frequency, file_name)

# write student_name|grade to "final_grades"
def write_student_grade(error_frequency, file_name):
    write_dict_to_file(error_frequency, file_name)

def draw_histogram(student_grades):
    x = list(student_grades.values())
    num_bins = 5
    n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
    plt.show()


def get_most_frequent_error(errors_frequency):
    max_error_name = ""
    max_error_frequency = 0

    for error_name, error_frequency in errors_frequency.items():
        if error_frequency > max_error_frequency:
            max_error_name = error_name
            max_error_frequency = error_frequency

    most_frequent_error = {max_error_name: max_error_frequency}
    return most_frequent_error


def print_most_frequent_error(max_error, error_codes):
    error_name = list(max_error.keys())[0]
    error_frequency = list(max_error.values())[0]
    error_value = error_codes[error_name]
    print("Most frequent error:\n\tName: {}, Frequency: {}, Value: {}".format(
        error_name, error_frequency, error_value))


if __name__ == "__main__":
    error_codes = parse_error_codes_file()
    students_errors = parse_students_errors_file(error_codes)
    errors_frequency = calculate_error_frequency(students_errors)
    student_grades = calculate_student_grade(error_codes, students_errors)

    write_error_statistics(errors_frequency, "errorcodes.stats")
    write_student_grade(student_grades, "final_grades")

    draw_histogram(student_grades)

    max_error = get_most_frequent_error(errors_frequency)
    print_most_frequent_error(max_error, error_codes)
