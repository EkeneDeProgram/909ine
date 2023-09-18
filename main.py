# Import standard libraries
import sys, re

# Import modules
from models import User, Login, session
from main_extension import main_extention
from utils import(
    check_password_for_compromise, generate_hashed_password,
    generate_salt, check_username, check_password ,
    generate_password
)
# Import third party libraries
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from validate_email import validate_email
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


# 909ine password policy
password_policy = [
    "At least 14 characters long",
    "At least 1 number",
    "At least 1 lowercase letter",
    "At least 1 uppercase letter",
    "At least 1 special character",
    "Not your email"
]

# 909ine menu
menu = [
    "1. Store password",
    "2. Retrieve password",
    "3. Retrieve all passwword",
    "4. Generate password",
    "5. Update password",
    "6. Delete password",
    "7. Exit"
]

options = [
    "1", "2", "3",
    "4", "5", "6", "7"
]

main_menu = ["1. Sign UP", "2. Sign In"]


# Main password manager function
def main():
    print(Fore.GREEN + "\t\t909ine Password Manager")
    print(Fore.GREEN + "\tSolve all poor password habits easily and quickly")
    exit_program = False
    while not exit_program:
        print(Fore.CYAN + "\n\t Main Menu")
        for i in main_menu:
            print(Fore.WHITE + f"\t {i}")
        choice = input(Fore.CYAN + "Enter your choice (1 - 2): ").strip()

        # Sign Up user to 909ine
        if choice == "1":
            while True:
                exit_inner_loop = False  # Flag variable to control the innermost loop
                # Get username
                username = input(Fore.GREEN + "Enter username: ").lower().strip()
                unique_username = check_username(username)  # Ensure username is unique
                if unique_username == True:
                    while True:
                        # Give the user an option to generate a password
                        generate_pwd = input(Fore.YELLOW + "Generate a strong and unique master password with 909ine (yes/no): ").lower().strip()
                        if generate_pwd == "yes":
                            generated_pwd = generate_password()  # Generate a unique password
                            sign_up = register_user(username, generated_pwd)
                            if sign_up == True:
                                print(Fore.WHITE + Back.GREEN + f"Success {username} account created")
                                print(Fore.GREEN + f"Your password is: {generated_pwd}")
                                #exit_program = True  # Set the flag to exit the outermost loop
                                exit_inner_loop = True  # Set the flag to exit the innermost loop
                                break  # Exit the innermost loop

                            else:
                                print(Fore.RED + f"{sign_up}")
                                sys.exit()
                        elif generate_pwd == "no":
                            # Display 909ine's password policy to guide the user to create a strong and unique password
                            print(Fore.CYAN + "Your password must meet the following requirements:")
                            for required in password_policy:
                                print(Fore.YELLOW + required)
                            while True:
                                # Get user-inputted password
                                user_password = input(Fore.GREEN + "Enter password: ").strip()
                                # Validate user-inputted password meets 909ine's password policy
                                validate_pwd = evaluate_password(user_password)
                                if validate_pwd == True:
                                    unique_password = check_password(user_password)  # Ensure password is unique
                                    if unique_password == True:
                                        sign_up = register_user(username, user_password)  # Register the user
                                        if sign_up == True:
                                            print(Fore.WHITE + Back.GREEN + f"Success {username} account created")
                                            #exit_program = True  # Set the flag to exit the outermost loop
                                            exit_inner_loop = True  # Set the flag to exit the innermost loop
                                            break  # Exit the innermost loop

                                        else:
                                            print(Fore.RED + f"{sign_up}")
                                            sys.exit()
                                    elif unique_password == False:
                                        print(Fore.YELLOW + f"This password {user_password} is already in use by another user. Please try another.")
                                    else:
                                        print(Fore.RED + f"{unique_password}")
                                        sys.exit()
                                elif validate_pwd == False:
                                    print(Fore.YELLOW + "Weak password")
                                else:
                                    print(Fore.RED + f"{validate_pwd}")
                                    sys.exit()
                            break  # Exit the second inner loop

                        else:
                            print(Fore.YELLOW + "Wrong input: enter (yes/no)")
                    if exit_inner_loop:
                        break  # Exit the first inner loop

                elif unique_username == False:
                    print(Fore.YELLOW + f"This username {username} is already in use by another user. Please try another.")
                else:
                    print(Fore.RED + f"{unique_username}")
                    sys.exit()
        elif choice == "2":
            while True:
                # Get username
                username = input(Fore.GREEN + "Enter username: ").lower().strip()
                identify_user = check_username(username) # Ensure user exists
                if identify_user == False:
                    while True:
                        user_password = input(Fore.GREEN + "Enter master password: ").strip()
                        sign_in = user_verification(username, user_password) # Verify user
                        if sign_in == True:
                            while True:
                                # Display 909ine menu
                                print(Fore.CYAN + f"\tWelcome to 909ine {username}")
                                print(Fore.CYAN + "\n\t909ine Menu:")
                                for i in menu:
                                    print(f"\t{i}")
                                choice = input(Fore.CYAN + "Enter your choice (1 - 7): ").strip()
                                if choice in options:
                                    main_extention(choice, username)
                                else:
                                    print(Fore.YELLOW + "Wrong input")
                        elif sign_in == False:
                            print(Fore.YELLOW + f"Invalid password for {username} please enter a valid password")
                        else:
                            print(Fore.RED + f"{sign_in}")
                            sys.exit()
                elif identify_user == True:
                    print(Fore.YELLOW + f"User not found. please enter a valid username")
                else:
                    print(Fore.RED + f"{identify_user}")
                    sys.exit()
        else:
            print(Fore.YELLOW + "Wrong input please choice between 1 - 2")


# Validate user inputed password meets 909ine's password policy
def evaluate_password(password):
    try:
        """Password must contain at least one lowercase letter,
        one uppercase letter, one special character (symbol) and one digit"""
        if not re.search(r"[a-z]", password) or \
        not re.search(r"[A-Z]", password) or \
        not re.search(r"\d", password) or \
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        # password must not be an email.
        if validate_email(password) == True:
            return False
        # At least 14 characters, at most 64 characters
        if len(password) < 14 or len(password) > 64:
            return False
        """Call the check_password_for_compromise functionn  to compare password
        against password breach database"""
        evaluate = check_password_for_compromise(password)
        if evaluate != 0:
             return evaluate
        return True
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occurred: {e}")


# User Registration and Data Storage move to main
def register_user(username, password):
    # Initialize variables
    try:
        user_salt = generate_salt()
        hash_password = generate_hashed_password(password, user_salt)
        user = User(username, hash_password, user_salt)
        User.insert(user)
        return True
    except IntegrityError:
        # Handle IntegrityError here
        session.rollback()
        raise ValueError("An IntegrityError occurred")
    except OperationalError as e:
        # Handle OperationalError exceptions
        session.rollback()
        print(f"OperationalError: {str(e)}")
    finally:
        session.close()


# Login user move to main
def user_verification(username, inputed_password):
    try:
        # Search for user in the database filter by user username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            # Get user data
            stored_hashed_password = user.password
            stored_salt = user.salt
            # Hash and salt user inputed password
            hash_user_input = generate_hashed_password(inputed_password, stored_salt)
            if hash_user_input == stored_hashed_password:
                return True
            else:
                return False
        elif user is None:
            return 0
    except OperationalError as e:
        # Handle OperationalError exceptions
        session.rollback()
        print(f"OperationalError: {str(e)}")
    except SQLAlchemyError as e:
        # Handle database exceptions
        session.rollback()
        return(f"An error occurred: {str(e)}")
    finally:
         session.close()



if __name__ == "__main__":
      main()