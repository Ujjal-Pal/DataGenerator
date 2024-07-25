import os
import random
import datetime
import pyttsx3
import xml.etree.ElementTree as ET
from faker import Faker
import string
from xml.dom import minidom  # For pretty printing

# Initialize Faker to generate fake data
fake = Faker()

# Function to generate fake investment information
def generate_fake_investment():
    company = fake.company()
    amount = fake.random_int(min=100000, max=1000000)
    date = fake.date_this_year()
    return company, amount, date

# Function to generate investment tips
def generate_investment_tips():
    tips = [
        "Invest in quality stocks for long-term growth.",
        "Diversify your portfolio to manage risk.",
        "Stay informed about market trends and news.",
        "Consider investing in emerging markets for higher returns.",
        "Avoid making impulsive investment decisions.",
        "Review your investment strategy regularly.",
        "Understand the company's financial health before investing.",
        "Consult with a financial advisor for personalized advice."
    ]
    return random.sample(tips, 3)  # Select 3 random tips

# Function to create XML metadata with pretty printing
def create_xml_metadata(company, amount, date):
    root = ET.Element("CAudioFile")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    cri = ET.SubElement(root, "CRI")
    start_time = ET.SubElement(cri, "StartTime")
    duration = ET.SubElement(cri, "Duration")
    direction = ET.SubElement(cri, "Direction")
    agent_pbx_id = ET.SubElement(cri, "AgentPBXID")
    agent_id = ET.SubElement(cri, "AgentID")

    # Generate random private data entries
    private_data = ET.SubElement(cri, "PrivateData")
    private_data_inner = ET.SubElement(private_data, "PrivateData")
    for _ in range(8):
        dictionary_entry = ET.SubElement(private_data_inner, "DictionaryEntry")
        key = ET.SubElement(dictionary_entry, "Key")
        value = ET.SubElement(dictionary_entry, "Value")
        key.text = fake.word()
        value.text = fake.word()

    channel = ET.SubElement(cri, "Channel")
    unit = ET.SubElement(cri, "Unit")
    screen_unit = ET.SubElement(cri, "ScreenUnit")
    local_start_time = ET.SubElement(cri, "LocalStartTime")
    local_end_time = ET.SubElement(cri, "LocalEndTime")
    contact_id = ET.SubElement(cri, "ContactID")
    data_source_name = ET.SubElement(cri, "DataSourceName")
    extension = ET.SubElement(cri, "Extension")

    agent = ET.SubElement(root, "Agent")
    groups_list = ET.SubElement(agent, "GroupsList")
    name = ET.SubElement(agent, "Name")

    file_elem = ET.SubElement(root, "File")
    location = ET.SubElement(file_elem, "Location")
    raw_location = ET.SubElement(file_elem, "RawLocation")
    raw_location_type = ET.SubElement(file_elem, "RawLocationType")

    instances = ET.SubElement(root, "Instances")
    cinstance = ET.SubElement(instances, "CInstance")
    id_elem = ET.SubElement(cinstance, "Id")
    name_elem = ET.SubElement(cinstance, "Name")

    xml_version = ET.SubElement(root, "XmlVersion")
    xml_version.text = "1.0"

    # Assign fake data to elements
    start_time.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    duration.text = str(random.randint(60, 600))
    direction.text = random.choice(["Inbound", "Outbound"])
    agent_pbx_id.text = fake.uuid4()
    agent_id.text = str(fake.random_number(digits=5))
    channel.text = str(fake.random_number(digits=2))
    unit.text = str(fake.random_number(digits=2))
    screen_unit.text = str(fake.random_number(digits=2))
    local_start_time.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    local_end_time.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    contact_id.text = fake.uuid4()
    data_source_name.text = fake.word()
    extension.text = fake.word()
    name.text = fake.name()
    location.text = fake.uri()
    raw_location.text = fake.uri()
    raw_location_type.text = fake.word()
    id_elem.text = str(fake.random_number(digits=5))
    name_elem.text = fake.word()

    # Convert ElementTree to a formatted string for pretty printing
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    return xml_str

# Function to generate fake voice file
def generate_fake_voice_file(company, amount, date, output_file):
    engine = pyttsx3.init()
    
    # Generate investment tips
    tips = generate_investment_tips()
    
    # Generate company paragraph
    company_paragraph = f"{company} is a leading company in the investment sector. " \
                        f"We recommend considering this opportunity seriously."

    # Investment information text
    investment_text = f"Investment in {company}. Amount: ${amount:,}. Date: {date}. " \
                      f"Here are some investment tips: {' '.join(tips)}. " \
                      f"{company_paragraph}"

    # Convert text to speech using pyttsx3
    engine.save_to_file(investment_text, output_file)
    engine.runAndWait()

# Function to sanitize company name (remove or replace special characters)
def sanitize_filename(filename):
    valid_chars = f"{string.ascii_letters}{string.digits}_"
    return ''.join(c if c in valid_chars else '_' for c in filename)

# Function to create output directory
def create_output_directory(output_dir):
    os.makedirs(output_dir, exist_ok=True)

# Function to generate and save XML and voice files
def generate_and_save_files(output_dir, i):
    company, amount, date = generate_fake_investment()

    # Generate XML metadata
    xml_content = create_xml_metadata(company, amount, date)
    xml_file = os.path.join(output_dir, f"{i}_{sanitize_filename(company)}_metadata.xml")
    
    # Write the formatted XML content to file
    with open(xml_file, "w", encoding="utf-8") as xml_writer:
        xml_writer.write(xml_content)
    
    # Generate voice file
    voice_file = os.path.join(output_dir, f"{i}_{sanitize_filename(company)}_voice.mp3")
    generate_fake_voice_file(company, amount, date, voice_file)

    print(f"Generated XML metadata file: {xml_file}")
    print(f"Generated voice file: {voice_file}")

# Main execution
if __name__ == "__main__":
    output_dir = 'fake_investment_files'
    create_output_directory(output_dir)
    
    for i in range(1, 3):
        generate_and_save_files(output_dir, i)

