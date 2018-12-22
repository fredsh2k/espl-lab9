from plumbum import local


def print_all_students():
    print("Student names: ")
    awk = local["awk"]
    students = awk["{print $1}", "lab10_grades.txt"]
    print(students())


def print_number_of_students():
    print("Number of students: ", end="")
    awk = local["awk"]
    wc = local["wc"]
    number_of_students = awk["{print $1}", "lab10_grades.txt"] | 
                         wc["-l"]
    print(number_of_students())


def print_errors_and_counts():
    print("Count Error-name:", end="")
    awk = local["awk"]
    sed = local["sed"]
    sort = local["sort"]
    uniq = local["uniq"]
    errors_and_counts = awk["{print $2}", "lab10_grades.txt"] | 
                        awk["NF"] | 
                        sed["s/[|]/\\n/g"] | 
                        sed["s/[0-9:.]//g"] | 
                        sort | uniq["-c"]
    print(errors_and_counts())


def print_number_of_unique_errors():
    print("Number of unique errors: ", end="")
    awk = local["awk"]
    sed = local["sed"]
    sort = local["sort"]
    uniq = local["uniq"]
    wc = local["wc"]
    number_of_unique_errors = awk["{print $2}", "lab10_grades.txt"] | 
                              awk["NF"] | 
                              sed["s/[|]/\\n/g"] | 
                              sed["s/[0-9:.]//g"] | 
                              sort | 
                              uniq["-c"] | 
                              wc["-l"]
    print(number_of_unique_errors())


if __name__ == "__main__":
    print_all_students()
    print_number_of_students()
    print_errors_and_counts()
    print_number_of_unique_errors()
