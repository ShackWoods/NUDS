import docx2txt
from glob import glob
from time import strptime

def get_folders() -> list:
    files = glob("*")
    return [x for x in files if '.' not in x]

def get_files(folder: str) -> list:
    files = glob(f"{folder}/*.docx")
    return files

def parse_files(folder: str) -> list:
    files = get_files(folder)
    results = []
    sections = ["Pre-Reading","Notes","Exercises","<TO DO>","Post-Reading","References"]
    for file in files:
        nickname = file[:-5]
        filename = nickname.split("\\")[1]
        content = docx2txt.process(file)
        for section in sections:
            content = content.split(section)[0]
        try:
            header, topic_line = content.split("<Covered Topics>")
        except:
            print(f"'{nickname}' needs the tag '<Covered Topics>'")
        try:
            clean_date_line, lecturer_line = header.split(" | ")
        except:
            print(f"'{nickname}' only has one section")
            continue
        split = max(lecturer_line.find(" - "), lecturer_line.find(" – "))
        if(split < 0):
            print(f"'{nickname}' doesn't have a lecturer/subject")
            continue
        clean_lecture_line = lecturer_line[split+3:]
        lecturers = clean_lecture_line.split(", ")
        lecturers[-1] = lecturers[-1][:-2]

        try:
            date_val = strptime(clean_date_line, "%d/%m/%Y")
        except:
            print(f"'{nickname}' has an invalid date")
            continue
        clean_topic_line = topic_line.replace("\n","")
        topics = clean_topic_line.split(", ")
        results.append((date_val, filename, clean_date_line, lecturers, topics))
    results.sort(key=lambda x: x[0])
    return results

def extract_topics():
    folders = get_folders()
    folders.remove("__pycache__")
    compilation = []
    for folder in folders:
        results = parse_files(folder)
        topic_file = f"{folder}/Topics.txt"
        folder_compilation = [f"{folder}:\n"]
        with open(topic_file, "w") as f:
            f.write(f"{folder}:\n")
            for _, filename, date, lecturers, topics in results:
                line = f"{filename}: Date = {date}, Taught by {lecturers}, Covered {topics}\n"
                f.write(line)
                folder_compilation.append(line)
        folder_compilation.append("---<END OF FOLDER>---\n")
        compilation.append("".join(folder_compilation))

    with open("AllTopics.txt", "w") as f:
        f.write("\n".join(compilation))
