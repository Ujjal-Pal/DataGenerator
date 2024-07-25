import os
import random
import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from faker import Faker

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

# Function to generate a unique .eml file with investment information
def generate_investment_eml(company, details_text):
    # Create an EmailMessage object for the investment information
    investment_message = EmailMessage()
    investment_message['From'] = fake.email()
    investment_message['Subject'] = f"Investment Information: {company}"
    investment_message.set_content(details_text)

    # Add date header
    investment_message['Date'] = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    return investment_message

# Function to generate a wrapper email with attached investment .eml file
def generate_wrapper_email(investment_message):
    # Create a new EmailMessage object for the wrapper email
    wrapper_message = MIMEMultipart()
    wrapper_message['From'] = investment_message['From']
    wrapper_message['To'] = fake.email()
    wrapper_message['Subject'] = f"Wrapper Email: {investment_message['Subject']}"

    # Attach the investment .eml file
    investment_attachment = MIMEApplication(investment_message.as_bytes(), _subtype='rfc822')
    investment_attachment.add_header('Content-Disposition', 'attachment', filename=f"{investment_message['Subject']}.eml")
    wrapper_message.attach(investment_attachment)

    return wrapper_message

# Function to save EmailMessage as .eml file
def save_eml_file(message, output_dir, filename):
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(message.as_bytes())
    print(f"Saved .eml file: {file_path}")

# Create 1000 wrapper .eml files
if __name__ == "__main__":
    output_dir = 'wrapper_eml_files'
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(1, 1001):
        # Generate fake investment information longer than 1000 characters
        company, details_text = generate_investment_info_long()

        # Generate investment .eml file
        investment_message = generate_investment_eml(company, details_text)

        # Generate wrapper email with attached investment .eml file
        wrapper_message = generate_wrapper_email(investment_message)

        # Save wrapper email as .eml file
        file_name = f'wrapper_email_{i}.eml'
        save_eml_file(wrapper_message, output_dir, file_name)

