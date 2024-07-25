import os
import random
import datetime
import sys
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from faker import Faker

# Receive arguments from command line
arg1 = sys.argv[1]

# Initialize Faker to generate fake data
fake = Faker()

# Function to generate fake investment information longer than 1000 characters
def generate_investment_info_long():
    company = fake.company()
    amount = fake.random_int(min=100000, max=1000000)
    date = fake.date_this_year()
    details = fake.paragraphs(nb=random.randint(5, 10))  # Generate multiple paragraphs
    details_text = f"Company: {company}\nAmount: ${amount:,}\nDate: {date}\n\n" + "\n\n".join(details)
    return company, details_text

# Function to generate a unique .eml file with investment information including TO and CC
def generate_investment_eml(company, details_text):
    # Create an EmailMessage object for the investment information
    investment_message = EmailMessage()
    investment_message['From'] = f"investor@{fake.domain_name()}"
    investment_message['To'] = f"recipient@{fake.domain_name()}"
    investment_message['CC'] = f"cc_recipient@{fake.domain_name()}"
    investment_message['Subject'] = f"Investment Information: {company}"
    investment_message.set_content(details_text)

    # Add date header
    investment_message['Date'] = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    return investment_message

# Function to save EmailMessage as .eml file
def save_eml_file(message, output_dir, filename):
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(message.as_bytes())
    #print(f"Saved .eml file: {file_path}")

# Create 1000 wrapper .eml files
if __name__ == "__main__":
    output_dir = 'C:/CS/TODODelete/Sparkethon/DataSets/wrapper_eml_files'
    main_dir = output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    num_iterations = int(arg1)

    for i in range(1, num_iterations):
        # Generate fake investment information longer than 1000 characters
        company, details_text = generate_investment_info_long()

        # Generate investment .eml file
        investment_message = generate_investment_eml(company, details_text)

        # Save investment .eml file
        file_name = f'investment_email_{i}.eml'
        save_eml_file(investment_message, output_dir, file_name)
    print(main_dir)
