# Import standard libraries
import hashlib, string, random, re

# Import third party libraries
import bcrypt, requests
from cryptography.fernet import Fernet
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy import func

# Import modules
from models import User, Login, session


# Generate a random salt
def generate_salt():
    try:
        random_salt = bcrypt.gensalt()
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occured {e}")
    return random_salt


# Generate hash password with salt
def generate_hashed_password(password, random_salt):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), random_salt).upper()
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occured {e}")
    return hashed_password


# Check if a password has been compromised
def check_password_for_compromise(password):
    # Hash user inputed password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest().upper()
    first_five = hashed_password[:5] # Get first 5 characters from hashed password
    last_five = hashed_password[5:]  # Get last 5 characters from hashed password
    try:
        # Connect to the pwnedpasswords API
        response = requests.get(f"https://api.pwnedpasswords.com/range/{first_five}")
        k = response.text.splitlines()
        for i in k:
            x = i.split(":")
            if last_five == x[0]: # Compare last_five against last 5 characters of breached passwords
                return(int(x[1]))
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occurred: {e}")
    return 0


# Generate a key for encryption
def generate_encryption_key():
    try:
        key = Fernet.generate_key()
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occurred: {e}")
    return key


# Encrypt data
def encrypt_data(key, data):
    try:
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occurred: {e}")
    return encrypted_data



# Decrypt data
def decrypt_data(key, encrypted_data):
    try:
        fernet = Fernet(key)
        d_data = fernet.decrypt(encrypted_data).decode()
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occured: {e}")
    return d_data


# Generate strong and unique password
def generate_password(password_length=14):
    letters = string.ascii_letters
    degits = string.digits
    symbols = string.punctuation

    characters = letters + degits + symbols
    pwd = ""
    try:
        """Password must contain at least 14 characters
        Password must contain at least one lowercase letter
        One uppercase letter, one special character (symbol) and one digit"""
        while len(pwd) < password_length or \
        not re.search(r"[a-z]", pwd) or \
        not re.search(r"[A-Z]", pwd) or \
        not re.search(r"\d", pwd) or \
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            generate = random.choice(characters) # Generate random password
            pwd += generate
    except Exception as e:
        # Handling generic exceptions
        print(f"An error occurred: {e}")
    return pwd

# Ensure user name is unique move to main
def check_username(inputed_username):
    my_list = []
    try:
        user_count = session.query(func.count(User.id)).scalar()
        if user_count > 0:
            users = session.query(User).all()
            for row in users:
                username = row.username
                my_list.append(username)
            if inputed_username not in my_list:
                return True
            else:
                return False
        else:
            return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


# Ensure password is unique move to main
def check_password(inputed_password):
    # Initialize variables
    password_list = []
    salt_list = []
    new_password_list = []
    try:
        user_count = session.query(func.count(User.id)).scalar()
        if user_count > 0:
            # Check if password is already use by another user
            users = session.query(User).all()
            for row in users:
                passwords  = row.password
                salts = row.salt
                password_list.append(passwords) # Add password to list
                salt_list.append(salts) # Add salt to list
            for i in salt_list:
                x = generate_hashed_password(inputed_password, i)
                new_password_list.append(x)
            for i in new_password_list:
                if i in password_list:
                    return False
            return True
        else:
            return True
    except SQLAlchemyError as e:
        session.rollback
        print(f"An error occurred: {e}")
    finally:
        session.close()


# Ensure each platform password is unique
def check_platform_password(username, password):
    my_list = []
    password_list = []
    key_list = []
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            user_id = user.id
            # Check if password is use for another platform by same user
            data = session.query(Login).filter_by(user_id=user_id).all()
            if len(data) > 0:
                for row in data:
                     passwords = row.password
                     key = row.key
                     decrypted_data = decrypt_data(key, passwords)
                     my_list.append(decrypted_data)
                if password not in my_list:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback
        print(f"An error occured: {e}")
    finally:
        session.close()


# Ensure platform is unique
def check_platform(username, platform):
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            user_id = user.id
            # Check if similar platform exist for same user
            user_data = session.query(Login).filter_by(user_id=user_id, platform=platform).first()
            if user_data is None:
                return True
            else:
                return False
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback
        print(f"An error occured: {e}")
    finally:
        session.close()

