# Import standard libraries
import sys

# Import project modules
from queries import(
    store_platform_password, retrieve_plaform_password,
    retrieve_all_platform_password, update_platform_password,
    delete_platform_password
)
from utils import(
    generate_encryption_key, encrypt_data,
    decrypt_data,check_platform_password,
    check_platform, generate_password,
    check_username, check_password
)
from models import User, Login, session

# Import third party libraries
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


# Project main function extension
def main_extention(choice, username):
        exit_program = False
        if choice == "1":
            # Get user metadata
            while not exit_program:
                platform = input(Fore.GREEN + "Enter service: ").lower().strip()
                unique_platform = check_platform(username, platform) # Ensure platform is unique
                if unique_platform  == True:
                    while True:
                        password = input(Fore.GREEN + "Enter password: ").strip()
                        unique_password = check_platform_password(username, password) # Ensure password is unique for all user password
                        if unique_password == True:
                            email = input(Fore.GREEN + "Enter email: ").lower().strip()
                            key = generate_encryption_key() # Generate encryption key
                            encrypt_password = encrypt_data(key, password) # Encrypt user password
                            store = store_platform_password(platform, email, encrypt_password, key, username)
                            if store == True:
                                print(Fore.WHITE + Back.GREEN + f"Success {username} your password for {platform} is safe")
                                exit_program = True
                                print("\n")
                                break
                            else:
                                print(Fore.RED + f"{store}")
                                sys.exit()
                        elif unique_password == False:
                            print(Fore.YELLOW + f"{username} this password is alredy in use by you. enter another password")
                        else:
                            print(Fore.RED + f"{unique_password}")
                            sys.exit()
                elif unique_platform == False:
                    print(Fore.YELLOW + f"{username} a password for {platform} already exists.")
                    sys.exit()
                else:
                    print(Fore.RED + f"{unique_platform}")
                    sys.exit()
        # Retrieve platform password
        elif choice == "2":
            while not exit_program:
                # Get user input
                platform = input(Fore.GREEN + "Enter service: ").lower().strip()
                verify_platform = check_platform(username, platform) # Very platform exists for user
                if verify_platform == False:
                    while True:
                        master_password = input(Fore.GREEN + "Enter master password: ").strip()
                        retrieve  = retrieve_plaform_password(username, platform, master_password)
                        if type(retrieve) != str and type(retrieve) != bool:
                            print(retrieve)
                            exit_program = True
                            print("\n")
                            break
                        elif retrieve == False:
                            print(Fore.YELLOW + f"Invalid master password for {username}. enter a valid master password")
                        else:
                            print(Fore.RED + f"{retrieve}")
                elif verify_platform == True:
                    print(Fore.YELLOW + f"{username} no password for {platform}. enter correct platform name as stored")
                else:
                    print(Fore.RED + f"{verify_platform}")
                    sys.exit()
        # Retrieve all passwword
        elif choice == "3":
            while not exit_program:
                # Get user master password
                master_password = input(Fore.GREEN + "Enter master password: ").strip()
                retrieve_all = retrieve_all_platform_password(username, master_password)
                if type(retrieve_all) != int and type(retrieve_all) != bool:
                    print(retrieve_all)
                    exit_program = True
                    print("\n")
                    break
                elif retrieve_all == False:
                    print(Fore.YELLOW + f"Invalid master password for {username}. enter a valid master password")
                elif retrieve_all == 0:
                    print(Fore.RED + f"{username} your 909ine vault is empty")
                    sys.exit()
                else:
                    print(Fore.RED +  f"{retrieve_all}")
                    sys.exit()
        # Generate password
        elif choice == "4":
            print(Fore.YELLOW + f"{username} you can customize the length of your password with a minimum of 14 and maximum of 64 characters")
            while not exit_program:
                # Get user customize password length
                length = input(Fore.GREEN + "Enter your desired password length: ").strip()
                if length.isdigit(): # user input must be a valid number
                    x = int(length)
                    if x >= 14 and x <= 64: # length must greater or equal to 14 or less than or equal to 64
                        generated_password = generate_password(x) # Generate password
                        print(Fore.GREEN + f"password: {generated_password}")
                        exit_program = True
                        print("\n")
                        break
                    else:
                        print(Fore.RED + "please enter a number from 14 - 64")
                else:
                    print(Fore.RED + "please enter a valid number")
        # Update Platform password
        elif choice == "5":
            while not exit_program:
                # Get user input for update
                platform_name = input(Fore.GREEN + "Enter service to update: ").lower().strip()
                is_valid_platform = check_platform(username, platform_name) #  Verify platform exists for user
                if is_valid_platform == False:
                    new_password = input(Fore.GREEN + "Enter new password: ").strip()
                    while True:
                        master_password = input(Fore.GREEN + "Enter master password: ").strip()
                        update_password = update_platform_password(username, platform_name, new_password, master_password)
                        if update_password == True:
                            print(Fore.WHITE + Back.GREEN + f"{username} your password for {platform_name} has been updated")
                            exit_program = True
                            print("\n")
                            break
                        elif update_password == False:
                            print(Fore.YELLOW + f"Invalid master password for {username}. enter a valid master password")
                        else:
                            print(Fore.RED + f"{update_password}")
                            syys.exit()
                elif is_valid_platform == True:
                    print(Fore.YELLOW + f"{username} no data found for {platform_name} ensure the platform you entered is correct")
                else:
                    print(Fore.RED + f"{is_valid_platform}")
                    sys.exit()
        # Dlete platform password
        elif choice == "6":
            while not exit_program:
                # Get user data to be deleted
                platform_to_delete = input(Fore.GREEN + "Enter service: ").lower().strip()
                is_valid_platform = check_platform(username, platform_to_delete) # Verify platform exists for user
                if is_valid_platform == False:
                    while True:
                        master_password = input(Fore.GREEN + "Enter master password: ").strip()
                        deleted = delete_platform_password(username, platform_to_delete, master_password) # Delete data
                        if deleted == True:
                            print(Fore.WHITE + Back.GREEN + f"{username} your password for {platform_to_delete} has been deleted")
                            exit_program = True
                            print("\n")
                            break
                        elif deleted == False:
                            print(Fore.YELLOW + f"Invalid master password for {username}. enter a valid master password")
                        else:
                            print(Fore.RED + f"{deleted}")
                elif is_valid_platform == True:
                    print(Fore.YELLOW + f"{username} no data found for {platform_to_delete} ensure the platform you entered is correct")
                else:
                    print(Fore.RED + f"{is_valid_platform}")
                    sys.exit()
        # Exit programme if choice eequals 7
        else:
            while True:
                confirm = input(Fore.YELLOW + "Enter yes to exit 909ine: ").lower().strip()
                if confirm == "yes":
                    sys.exit()
                else:
                    print(Fore.RED + "please enter yes to exit")



