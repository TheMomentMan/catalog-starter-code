import re

def extract_course_titles(text):
    """
    Extracts course titles from academic course listings.
    
    Args:
        text (str): The input text containing course listings
    
    Returns:
        list: A list of tuples containing (course_number, course_title)
    """
    # Pattern to match course numbers and titles
    pattern = r'(1\.\d+[A-Za-z]*J?)\s+([^\n]+)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Process matches to clean up titles
    courses = []
    for course_num, title in matches:
        # Clean up the title:
        # Remove any trailing 'Prereq.:' and everything after
        title = re.split(r'(?:Prereq\.:|Same subject as)', title)[0].strip()
        courses.append((course_num, title))
    
    return courses

def format_results(courses):
    """
    Formats the extracted courses for display
    """
    output = "Extracted Courses:\n"
    output += "-" * 50 + "\n"
    for number, title in courses:
        output += f"Course {number}: {title}\n"
    return output