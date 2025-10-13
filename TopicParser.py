import docx2txt ###[1]
from glob import glob
from time import strptime ###[2]

def get_folders() -> list:
    files = glob("*")
    return [x for x in files if '.' not in x]

def get_files(folder: str) -> list:
    files = glob(f"{folder}/*.docx")
    return files

def parse_files(folder: str) -> list:
    files = get_files(folder)
    results = []
    sections = ["Pre-Reading","Notes","Post-Reading","References"]
    for file in files:
        filename = file.split("\\")[1][:-5]
        content = docx2txt.process(file) ###[1]
        for section in sections:
            content = content.split(section)[0]
        header, topic_line = content.split("<Covered Topics>")
        clean_date_line, lecturer_line = header.split(" | ")
        try:
            clean_lecture_line = lecturer_line.split(" - ")[1]
        except:
            clean_lecture_line = lecturer_line.split(" – ")[1]
        lecturers = clean_lecture_line.split(", ")
        lecturers[-1] = lecturers[-1][:-2]
        date_val = strptime(clean_date_line, "%d/%m/%Y") ###[2]
        clean_topic_line = topic_line.replace("\n","")
        topics = clean_topic_line.split(", ")
        results.append((date_val, filename, clean_date_line, lecturers, topics))
    results.sort(key=lambda x: x[0]) ###[3]
    print(f"{folder} has been compiled")
    return results

folders = get_folders()
compilation = []
for folder in folders:
    results = parse_files(folder)
    topic_file = f"{folder}/Topics.txt"
    folder_compilation = [f"{folder}:\n"]
    with open(topic_file, "w") as f: ###[4]
        f.write(f"{folder}:\n")
        for _, filename, date, lecturers, topics in results:
            line = f"{filename}: Date = {date}, Taught by {lecturers}, Covered {topics}\n"
            f.write(line)
            folder_compilation.append(line)
    folder_compilation.append("---<END OF FOLDER>---\n")
    compilation.append("".join(folder_compilation))

with open("AllTopics.txt", "w") as f: ###[4]
    f.write("\n".join(compilation))
    
print("Topics extracted :D")

'''
SOURCES:
[1] - Billal BEGUERADJ on stackoverflow <https://stackoverflow.com/questions/36001482/read-doc-file-with-python>, Accessed on 08/10/2025
[2] - Guillermo Pereira on stackoverflow <https://stackoverflow.com/questions/8142364/how-to-compare-two-dates>, Accessed on 08/10/2025
[3] - mouad on stackoverflow <https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list>, Accessed on 08/10/2025
[4] - W3Schools <https://www.w3schools.com/python/python_file_write.asp>, Accessed on 08/10/2025
'''