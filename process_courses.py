import requests
import pandas as pd
import xml.etree.ElementTree as ET
import csv
from time import sleep

df = pd.read_csv('courses.csv', usecols=["Course","Title","CS"])
df[['subjectCode', 'courseNumber']] = df['Course'].str.split(' ', n=1, expand=True)

YEAR = "2023"
SEMESTER = "FALL"
LOGFILE_DIR = "logs.csv"
"""
    CSV Format:
    Course,Error Message,Meeting Days,Start Time,End Time,Meeting Type (Discussion Lecture etc),Section Notes,Section Text,Section Capp Area,XML Link
"""

# iterate through every course and traverse the uiuc api. For every course with multiple sections, go to each section url and append the new course and its meeting times to a csv file

def log(message: list):
    """Log a message to a CSV file"""

    if not LOGFILE_DIR:
        raise Exception("No log file specified")

    with open(LOGFILE_DIR, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write the message as a row
        writer.writerow(message)

def access(url: str, subject_code: str, course_number: str):
    """access the url, its meeting time,"""

    log_message = [""] * 10

    response = requests.get(url)
    log_message[0] = subject_code + " " + course_number
    log_message[9] = url
    
    # Check the response status code
    if response.status_code != 200:
        log_message[1] = f"(access method) Failed to retrieve XML content. Status code: {response.status_code}"
        return
    
    xml_content = response.text
    root = ET.fromstring(xml_content)
    
    days = root.find(".//daysOfTheWeek")
    start_time = root.find('.//start')
    end_time = root.find('.//end')
    type_code = root.find('.//type')
    section_notes = root.find('.//sectionNotes')
    section_text = root.find('.//sectionText')
    section_cap_area = root.find('.//sectionCappArea')

    # Log the extracted information if available
    try:
        if days is not None:
            log_message[2] = days.text.replace(" ", "") # Remove spaces from the string (e.g. "M W F")

        if start_time is not None:
            log_message[3] = start_time.text

        if end_time is not None:
            log_message[4] = end_time.text

        if type_code is not None:
            log_message[5] = type_code.attrib['code']

        if section_notes is not None:
            log_message[6] = section_notes.text

        if section_text is not None:
            log_message[7] = section_text.text

        if section_cap_area is not None:
            log_message[8] = section_cap_area.text
        
    except AttributeError:
        # There's no extra info about the course
        pass

    log(log_message)

if __name__ == "__main__":
    for index, row in df.iterrows():
        print(f"Working on {row['subjectCode']} {row['courseNumber']}")
        sleep(5)
        url = f"https://courses.illinois.edu/cisapp/explorer/schedule/{YEAR}/{SEMESTER}/{row['subjectCode']}/{row['courseNumber']}.xml"

        response = requests.get(url)

        # Check the response status code

        if response.status_code != 200:
            log_message = [""] * 10
            log_message[0] = f"{row['subjectCode']} {row['courseNumber']}"
            log_message[9] = url
            if response.status_code == 404:
                log_message[1] = "Error 404: Course not found"
            else:
                log_message[1] = f"Error {response.status_code}: Failed to retrieve XML content."
            log(log_message)
            continue

        xml_content = response.text
        root = ET.fromstring(xml_content)
        
        for section in root.findall('.//sections/section'):
            section_url = section.get('href')
            
            sleep(5)
            print("Accessing:", section_url)
            access(section_url, row['subjectCode'], row['courseNumber'])
