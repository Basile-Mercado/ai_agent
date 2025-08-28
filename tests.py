from functions.get_files_info import get_files_info, get_files_content


def test():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)
    
    result = get_files_content("calculator", "main.py")
    print("Result for 'main.py' file:")
    print(result)

    result = get_files_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py' file:")
    print(result)
    
    result = get_files_content("calculator", "/bin/cat")
    print("Result for '/bin/cat' file:")
    print(result)
    
    result = get_files_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'pkg/does_not_exist.py' file:")
    print(result)


if __name__ == "__main__":
    test() 