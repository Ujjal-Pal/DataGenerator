import os
import random
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO

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

# Function to generate PDF file content using reportlab
def generate_pdf_content(details_text):
    try:
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.drawString(100, 750, details_text)  # Example text placement
        c.showPage()
        c.save()
        pdf_content = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_content
    except Exception as e:
        print(f"Error generating PDF content: {e}")
        return None

# Function to generate JPEG image buffer
def generate_jpeg_image():
    image = Image.new('RGB', (300, 200), color='red')
    jpeg_buffer = BytesIO()
    image.save(jpeg_buffer, format='JPEG')
    jpeg_buffer.seek(0)
    return jpeg_buffer

# Function to create the original email with attachments and distinct recipients
def create_original_email(company, details_text, pdf_content, jpeg_buffer):
    # Generate random email addresses for From, To, and CC with testemail.com domain
    from_email = fake.email(domain='testemail.com')
    to_email = fake.email(domain='testemail.com')
    cc_email = fake.email(domain='testemail.com')

    # Create a MIMEMultipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['CC'] = cc_email
    msg['Subject'] = f"Investment Information: {company}"
    msg['Date'] = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    # Add investment details as text/plain
    body_text = MIMEText(details_text, 'plain')
    msg.attach(body_text)

    # Attach PDF file
    pdf_attachment = MIMEApplication(pdf_content, _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename="investment_details.pdf")
    msg.attach(pdf_attachment)

    # Attach JPEG image
    jpeg_attachment = MIMEApplication(jpeg_buffer.getvalue(), _subtype="jpeg")
    jpeg_attachment.add_header('Content-Disposition', 'attachment', filename="investment_image.jpg")
    msg.attach(jpeg_attachment)

    return msg

# Function to save EmailMessage as .eml file
def save_eml_file(message, output_dir, filename):
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(message.as_bytes())
    print(f"Saved .eml file: {file_path}")

# Create 1000 .eml files each with original email containing attachments and distinct recipients with testemail.com domain
if __name__ == "__main__":
    output_dir = 'original_eml_with_attachments_testemail'
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, 1001):
        # Generate fake investment information longer than 1000 characters
        company, details_text = generate_investment_info_long()

        # Generate PDF content
        pdf_content = generate_pdf_content(details_text)

        # Generate JPEG image buffer
        jpeg_buffer = generate_jpeg_image()

        # Create original email with attachments and distinct recipients
        original_email = create_original_email(company, details_text, pdf_content, jpeg_buffer)

        # Save .eml file
        safe_company_name = ''.join(c if c.isalnum() else '_' for c in company)
        file_name = f'{i}_{safe_company_name}.eml'
        save_eml_file(original_email, output_dir, file_name)
