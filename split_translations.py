"""Split passwords into translated and untranslated"""

def read_passwords(file_path):
    """Read passwords from a file and return a list of those passwords."""
    with open(file_path, 'r', encoding='latin1') as file:
        return file.read().splitlines()

def compare_passwords(file_path1, file_path2):
    """Compare passwords from two files and categorize them, preserving order."""
    passwords1 = read_passwords(file_path1)
    passwords2 = read_passwords(file_path2)
    unique_passwords_1 = []
    unique_passwords_2 = []
    common_passwords = []
    for i in range(len(passwords1)):
        if passwords1[i] == passwords2[i]:
            common_passwords.append(passwords1[i])
        else:
            unique_passwords_1.append(passwords1[i])
            unique_passwords_2.append(passwords2[i])

    return common_passwords, unique_passwords_1, unique_passwords_2

def save_passwords(file_path, password_list):
    """Save the list of passwords to a file."""
    with open(file_path, 'w', encoding='latin1') as file:
        for password in password_list:
            file.write(password + '\n')

def main():
    # Define the paths to the input files and output files
    # 1st Run
    file_path1 = 'orig_4k.txt'
    file_path2 = 'de_4k.txt'
    untranslated_file = 'untranslated.txt'
    orig_translated_file = 'orig_translated.txt'
    trans_translated_file = 'trans_translated.txt'

    # 2nd Run
    # file_path1 = 'untranslated.txt'
    # file_path2 = 're_translated.txt'
    # untranslated_file = 'untranslated2.txt'
    # orig_translated_file = 'orig_translated2.txt'
    # trans_translated_file = 'trans_translated2.txt'

    # 3rd Run
    # file_path1 = 'untranslated2.txt'
    # file_path2 = 're_translated2.txt'
    # untranslated_file = 'untranslated3.txt'
    # orig_translated_file = 'orig_translated3.txt'
    # trans_translated_file = 'trans_translated3.txt'

    # Compare passwords and get the lists
    common_passwords, unique_passwords_1, unique_passwords_2 = compare_passwords(file_path1, file_path2)

    # Save the resulting lists to files
    save_passwords(untranslated_file, common_passwords)
    save_passwords(orig_translated_file, unique_passwords_1)
    save_passwords(trans_translated_file, unique_passwords_2)

if __name__ == "__main__":
    main()
