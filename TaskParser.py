import docx2txt
import re

#Using the navigator folder
def parse_tasklist(filename) -> list:
    results = []
    content = docx2txt.process(filename)
    sections = content.split("<TO DO>")
    if(len(sections) < 2): return []
    tasks = sections[1].split("Post-Reading")[0].strip().split("\n")
    for task in tasks:
        if(re.search("^#\\[.*\\]", task)):
            trimmed_task = task[2:-1]
            results.append(trimmed_task)
    return results

def extract_tasklists(folders):
    compilation = []
    for folder in folders:
        folder_compilation = [f"{folder}:\n"]
        for file in folders[folder].files:
            nickname = folder + "/" + file.filename
            path = nickname + ".docx"
            newTasks = parse_tasklist(path)
            if(len(newTasks) == 0): continue
            folder_compilation.append(f"{file.filename}; {newTasks}\n")
        folder_compilation.append("---<END OF FOLDER>---\n")
        compilation.append("".join(folder_compilation))
    
    with open("tasks.txt","w") as f:
        f.write("\n".join(compilation))

def remove_tasks(tasklist: str) -> list:
    tasklist = tasklist[1:-1]
    tasks = tasklist.split(", ")
    return [task[1:-1] for task in tasks]


def announce_tasks():
    with open("tasks.txt","r") as f:
        content = f.readlines()

    current_state = "new_folder"
    folder_name = ""
    for line in content:
        line = line.strip()
        match current_state:
            case "new_folder":
                folder_name = line[:-1]
                current_state = "new_file"
            case "new_file":
                if(line == "---<END OF FOLDER>---"):
                    current_state = "end_of_folder"
                    continue
                parts = line.split("; ")
                print(folder_name + "/" + parts[0])
                this_tasks = remove_tasks(parts[1])
                for x, task in enumerate(this_tasks):
                    print(f"---Task {x+1}: {task}")
            case "end_of_folder":
                current_state = "new_folder"