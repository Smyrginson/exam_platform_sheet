with open('source.txt') as file:
    password_list = file.readlines()


def password_validation(password):
    if len(password.split()) == len(set(password.split())):
        return True
    return False


pass_valid_nr = 0
for password in password_list:
    if password_validation(password):
        pass_valid_nr += 1

print(f'Ther is {pass_valid_nr} valid paswords')
