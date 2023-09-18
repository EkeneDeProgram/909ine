# 909ine Command-line Password Manager

#### Video Demo: https://youtu.be/401ROSPhJfg

#### Description:
909ine is a user friendly  command-line password manager that allows users solve poor passwords
habits easily and quickly. It generate and securely store complex passwords for services
such as SSH (Secure Shell), SFTP (SSH File Transfer Protocol), MySQL Command-line client,
Network Configuration etc.

#### Tech Stack:
    - Python
    - SQLite
    - SQLAlchemy
    - pwnedpasswords API

#### Project Structure:
    - main_extension.py
    - models.py
    - project.py
    - queries.py
    - requirements.txt
    - test_project.py
    - utils.py

#### Features:
    - Register user
    - Unique username
    - Unique master password
    - Unique service
    - Unique password for each service
    - hash and salt master password
    - encrypt service passwords
    - Login user
    - Genearte strong and unique password
    - Retrieve password for a service
    - Retrieve passwwords for services
    - Update password
    - Delete password

#### Instalation:
To install and run 909ine command-line password manager, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using the pip command below.
```
pip install -r requirements.txt
```
4. Run the application with the command below.
```
python main.py
```

#### Usage:
To use 909ine command-line password mananger, follow these steps:
1. Creat account:
To start using 909ine command-line password manager, you need to create an acount.
with your username and master password Use the following command below:
```
 Enter your choice (1 - 2): 1
 ```
 2. Loging:
 Login with your username and master password
 ```
Enter your choice (1 - 2): 2
```
3. Store password:
Once You're login you can store passwords for any service using the following command
```
Enter your choice (1 - 7): 1
```
4. Retrieve password:
To retrieve a stored password, use the following command:
```
Enter your choice (1 - 7): 2
```
5. Retrieve all password:
To retrieve all stored passwords, use the following command:
```
Enter your choice (1 - 7): 3
```
6. Generate password:
To generate a strong and unique password, use the following command:
```
Enter your choice (1 - 7): 4
```
7. Update password:
You can update stored passwords, using the following commands:
```
Enter your choice (1 - 7): 5
```
8. Delete password:
You can delete stored passwords, using the following commands:
```
Enter your choice (1 - 7): 6
```
9. Exit:
You can exit the application, using the following
```
Enter your choice (1 - 7): 6
```

#### Files:
1. models.py:
This file defines the data models of the application, each model as a Python class with methods, where
each attribute of the class corresponds to a field in the database table

2. main.py:
This is the main project file it is the entry point of the application
the file contain 3 functions and the main function.

3. queries.py:
This file contains functions and code for interacting
with the database.

4. utils.py:
This file contains utility functions and helper code that can be used
across various parts of the project.

5. test_project.py:
This is a test file it contains test cases that verify the
correctness of the functions in the project.py file except
the main function code.

6. main_extension.py:
The main_extension file extends or complements the functionality of the project.py file.

#### Design Choices:

###### Data Storage:
For data storage, i debated between using a traditional relational database and CSV file. I ultimately chose a relational database because of its flexibility and scalability. This choice allows me to organize data into structured tables with defined relationships between them.
###### User Interface:
My goal was to create a user-friendly, intuitive and responsive interface. To achieve this, i followed some principles for designing a command-line application user interface.
- Consistency
- Interactive Mode
- Clear Feedback
- Color Coding
- Security
###### Color Palette:
One of the design choices i had to make was selecting the color palette for the project. I opted for a combination of Greens, Cyan, Yellow, Red . These colors were chosen to create a visually pleasing and calming user experience.

#### Security Tips and Best Practices
Here are some security tips to help you keep your passwords secured while using 909ine:
- Use a Strong Master Password
- Regularly Update Your Passwords
- Secure Your Device
- Use Secure Networks
- Stay Informed

Security is a top priority. 909ine follows industry best practices to keep your data safe. For any security concerns or vulnerability reports, please contact our security team at 9009ine@gmail.com.

