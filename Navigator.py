import time

class File:
    def __init__(self, filename: str, date: str, lecturers: list[str], topics: list[str]):
        self.filename = filename
        self.date = date
        self.comp_date = time.strptime(date, "%d/%m/%Y")
        self.lecturers = tuple(lecturers)
        self.topics = tuple(topics)

    def __str__(self) -> str:
        return f"{self.filename}: {str(self.date)} - {self.lecturers}, {self.topics}"

class Folder:
    def __init__(self, foldername: str):
        self.foldername = foldername
        self.files = []

    def __str__(self) -> str:
        return self.foldername + ":\n" + "\n".join([str(file) for file in self.files])

    def add_file(self, file:File):
        self.files.append(file)

def initialise_objects():
    folders = {}
    cur_folder = None
    state = "new_folder"
    with open("AllTopics.txt", 'r') as f: ###[1]
        for line in f:
            line = line.strip()
            match state:
                case "new_folder":
                    cur_folder = Folder(line[:-1])
                    state = "new_file"
                case "new_file":
                    if(line == "---<END OF FOLDER>---"):
                        state = "end_of_folder"
                        continue
                    filename, line = line.split(": ")
                    line = line[7:]
                    date, line = line[:10], line[23:]
                    list_end = line.find("]")
                    raw_lecturers, line = line[:list_end], line[list_end + 12:-1]
                    lecturers = [x[1:-1] for x in raw_lecturers.split(", ")]
                    topics = [x[1:-1] for x in line.split(", ")]
                    new_file = File(filename, date, lecturers, topics)
                    cur_folder.add_file(new_file)
                case "end_of_folder":
                    folders[cur_folder.foldername] = cur_folder
                    state = "new_folder"
    return folders

#Complex searches can be done by ANDing multiple single search results
def search_by_topic(folders: list[Folder], topic: str) -> list[File]:
    results = []
    for folder in folders:
        results += [file for file in folder.files if topic in file.topics]
    return results

#This is just merge sort but on files.comp_date
def sort_by_date(files: list[File]):
    length = len(files)
    if(length == 1):
        return files
    elif(length == 2):
        if(files[0].comp_date < files[1].comp_date): return files
        return files[::-1]
    mid = length // 2
    left, right = sort_by_date(files[:mid]), sort_by_date(files[mid:])
    l = r = 0
    final = []
    while l < len(left) and r < len(right):
        if(left[l].comp_date <= right[r].comp_date):
            final.append(left[l])
            l += 1
        else:
            final.append(right[r])
            r += 1
    if(l < len(left)): final += left[l:]
    elif(r < len(right)): final += right[r:]
    return final

'''
[1] - W3Schools <https://www.geeksforgeeks.org/python/read-a-file-line-by-line-in-python/> Accessed on 09/10/2025
'''