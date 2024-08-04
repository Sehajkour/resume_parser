import json
import pdfplumber
import os
import logging
from argparse import ArgumentParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_pdf_resume(file_path):
    """
    Parses a PDF resume and extracts information into a structured format.
    
    Args:
        file_path (str): Path to the PDF resume file.

    Returns:
        dict: Extracted resume data structured in a dictionary.
    """
    resume_data = {
        "personal_info": {},
        "education": [],
        "work_experience": [],
        "skills": [],
    }

    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as e:
        logging.error(f"Failed to read PDF file: {e}")
        raise

    if not text:
        logging.warning("No text extracted from the resume.")
        return resume_data

    lines = text.split("\n")
    section = None

    for line in lines:
        line = line.strip()
        if "Name:" in line:
            resume_data["personal_info"]["name"] = line.replace("Name:", "").strip()
        elif "Email:" in line:
            resume_data["personal_info"]["email"] = line.replace("Email:", "").strip()
        elif "Education" in line:
            section = "education"
        elif "Experience" in line:
            section = "work_experience"
        elif "Skills" in line:
            section = "skills"
        else:
            if section == "education":
                resume_data["education"].append(line)
            elif section == "work_experience":
                resume_data["work_experience"].append(line)
            elif section == "skills":
                resume_data["skills"].append(line)

    return resume_data

def save_to_json(data, output_file):
    """
    Saves extracted data to a JSON file.
    
    Args:
        data (dict): Data to be saved.
        output_file (str): Path to save the JSON output.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to write JSON file: {e}")
        raise

def print_resume(data):
    """
    Prints the resume data to the terminal in a readable format.
    
    Args:
        data (dict): Data to be printed.
    """
    print("\nPersonal Information:")
    if "name" in data["personal_info"]:
        print(f"Name: {data['personal_info']['name']}")
    if "email" in data["personal_info"]:
        print(f"Email: {data['personal_info']['email']}")
    
    print("\nEducation:")
    for entry in data["education"]:
        print(f"- {entry}")
    
    print("\nWork Experience:")
    for entry in data["work_experience"]:
        print(f"- {entry}")
    
    print("\nSkills:")
    for entry in data["skills"]:
        print(f"- {entry}")

def main():
    parser = ArgumentParser(description="Parse a resume from a PDF file and save the data in JSON format.")
    parser.add_argument("file_path", help="Path to the resume PDF file.")
    parser.add_argument("output_file", help="Path to save the JSON output.")
    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        logging.error("The provided file path does not exist.")
        return

    resume_data = parse_pdf_resume(args.file_path)
    
    # Print the resume data to the terminal
    print_resume(resume_data)
    
    # Save the resume data to a JSON file
    save_to_json(resume_data, args.output_file)
    logging.info(f"Resume data saved to {args.output_file}")

if __name__ == "__main__":
    main()
