# Import third party libraries
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy import func
import pandas as pd

# Import modules
from utils import generate_hashed_password, generate_encryption_key, encrypt_data, decrypt_data
from models import User, Login, session



# Store user data
def store_platform_password(platform, email, password, key, username):
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            logs = Login(
                platform = platform,
                email = email,
                password = password,
                key = key,
                user = user
            )
            Login.insert(logs) # Add user logins
            return True
        else:
            return False
    except IntegrityError:
        # Handle IntergrityError exceptions
        session.rollback()
        raise ValueError()
    except OperationalError  as e:
        # Handle OperationalError exceptions
        session.rollback()
        print(f"An error occured {e}")
    except SQLAlchemyError as e:
        # Handle database exceptions
        session.rollback()
        print("An error occurred: ", str(e))
    finally:
         session.close()



# Retrieve user data
def retrieve_plaform_password(username, platform, user_inputed_password):
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            # Get user details
            user_id = user.id
            stored_hashed_password = user.password
            stored_salt = user.salt
            # Hash user inputed password with stored salt
            hash_user_input = generate_hashed_password(user_inputed_password, stored_salt)
            if hash_user_input == stored_hashed_password: # Verify user inputed password
                # search user data stored in Login table
                user = session.query(Login).filter_by(user_id=user_id, platform=platform).first()
                if user: # If data exists
                    # Get metadata
                    platform = user.platform
                    email = user.email
                    encrypted_password = user.password
                    key = user.key
                    decrypted_password = decrypt_data(key, encrypted_password)
                    # Create dictionary with metadata
                    data = {
                        "service": platform,
                        "email": email,
                        "password": decrypted_password
                    }
                    # Convert data to pandas dataframe
                    result =  pd.DataFrame(data, index=[0])
                    return(result)
                else:
                    return 0
            else:
                return False
        else:
            return 0
    except SQLAlchemyError as e:
        # Handle database exceptions
        session.rollback()
        print("An error occurred:", str(e))
    finally:
        session.close()



# Retrieve all platforms password
def retrieve_all_platform_password(username, master_password):
    # Initialize variables
    user_platform = []
    user_email = []
    user_password = []
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            user_id = user.id
            stored_hashed_password = user.password
            stored_salt = user.salt
            # Hash user inputed password with stored salt
            hash_user_input = generate_hashed_password(master_password, stored_salt)
            if hash_user_input == stored_hashed_password: # Verify user inputed password
                # Count number of passwords stored by user
                user_data = session.query(Login).filter(Login.user_id==user_id).count()
                if user_data > 0:
                    # Get all user stored data
                    data = session.query(Login).filter_by(user_id=user_id).all()
                    for row in data:
                        platform = row.platform
                        email = row.email
                        password = row.password
                        key = row.key
                        decrypted_data = decrypt_data(key, password)
                        # Add data to list
                        user_platform.append(platform)
                        user_email.append(email)
                        user_password.append(decrypted_data)
                    # Create dictionary with list
                    metadata = {
                         "service": user_platform,
                         "email": user_email,
                         "password": user_password
                    }
                    # Convert data to pandas dataframe
                    result =  pd.DataFrame(metadata)
                    return result
                else:
                    return 0
            else:
                return False
        else:
            return 0
    except SQLAlchemyError as e:
        session.rollback()
        print("An error occurde:", str(e))
    finally:
        session.close()


# Update password
def update_platform_password(username, platform, new_password, master_password):
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            user_id = user.id
            stored_hashed_password = user.password
            stored_salt = user.salt
            # Hash user inputed password with stored salt
            hash_user_input = generate_hashed_password(master_password, stored_salt)
            if hash_user_input == stored_hashed_password: # Verify user inputed password
                user_data = session.query(Login).filter_by(user_id=user_id, platform=platform).first()
                if user_data:
                    new_key = generate_encryption_key()
                    new_password = encrypt_data(new_key, new_password)
                    user_data.key = new_key
                    user_data.password = new_password
                    user_data.update()
                    return True
                else:
                    return 0
            else:
                return False
        else:
            return 0
    except SQLAlchemyError as e:
        session.rollback()
        print("An error occurde:", str(e))
    finally:
        session.close()



# Delete user platform
def delete_platform_password(username,  platform, master_password):
    try:
        # Search for user in the database filter by username
        user = session.query(User).filter_by(username=username).first()
        if user: # If user exists
            user_id = user.id
            stored_hashed_password = user.password
            stored_salt = user.salt
            # Hash user inputed password with stored salt
            hash_user_input = generate_hashed_password(master_password, stored_salt)
            if hash_user_input == stored_hashed_password:
                user_data = session.query(Login).filter_by(user_id=user_id, platform=platform).first()
                if user_data:
                    user_data.delete()
                    return True
                else:
                    return 0
            else:
                return False
        else:
            return 0
    except SQLAlchemyError as e:
        session.rollback()
        print("An error occurde:", str(e))
    finally:
        session.close()



