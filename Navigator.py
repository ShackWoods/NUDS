import time

class File:
    def __init__(self, foldername: str, filename: str, date: str, lecturers: list[str], topics: list[str]):
        self.foldername = foldername
        self.filename = filename
        self.date = date
        self.comp_date = time.strptime(date, "%d/%m/%Y")
        self.lecturers = set(lecturers)
        self.topics = set(topics)

    #DEBUG/CLI Method
    def __str__(self) -> str:
        return f"{self.foldername}/{self.filename}: {str(self.date)} - {self.lecturers}, {self.topics}"
    
    #Just for interfacing sake#
    def get_lecturers(self) -> set:
        return self.lecturers
    
    def get_topics(self) -> set:
        return self.topics
    #Just for interfacing sake#
    
    def validate_file(self, topic_filters: set, lecturer_filters: set) -> bool:
        topic_valid = True
        if(topic_filters): #If there are filters [abusing truthy values]
            topic_intesection = self.topics.intersection(topic_filters)
            topic_valid = bool(topic_intesection)
        lecturer_valid = True
        if(lecturer_filters):
            lecturer_intersection = self.lecturers.intersection(lecturer_filters)
            lecturer_valid = bool(lecturer_intersection)
        return topic_valid and lecturer_valid

class Folder:
    def __init__(self, foldername: str):
        self.foldername = foldername
        self.hidden = False
        self.files = []

    #DEBUG/CLI Method
    def __str__(self) -> str:
        return self.foldername + ":\n" + "\n".join([str(file) for file in self.files])

    def add_file(self, file:File):
        self.files.append(file)

    def search(self, topic_filters: set, lecturer_filters: set) -> list[File]:
        if(self.hidden): return
        results = []
        for file in self.files:
            if(not file.validate_file(topic_filters, lecturer_filters)): continue
            results.append(file)
        return results

def initialise_objects():
    folders = {}
    cur_folder = None
    state = "new_folder"
    with open("AllTopics.txt", 'r') as f:
        for line in f:
            line = line.strip()
            match state:
                case "new_folder":
                    cur_folder = Folder(line[:-1])
                    folders[cur_folder.foldername] = cur_folder
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
                    new_file = File(cur_folder.foldername, filename, date, lecturers, topics)
                    cur_folder.add_file(new_file)
                case "end_of_folder":
                    state = "new_folder"
    return folders

def sort_wrapper(sort_function):
    def wrap(files: list[File], ascending = True) -> list[File]:
        sorted_list = sort_function(files)
        if(ascending): return sorted_list
        return sorted_list[::-1]
    return wrap

@sort_wrapper
def sort_by_date(files: list[File]) -> list[File]:
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

@sort_wrapper
def sort_by_folder(files: list[File]) -> list[File]:
    length = len(files)
    if(length == 1):
        return files
    elif(length == 2):
        if(files[0].foldername < files[1].foldername): return files
        return files[::-1]
    mid = length // 2
    left, right = sort_by_date(files[:mid]), sort_by_date(files[mid:])
    l = r = 0
    final = []
    while l < len(left) and r < len(right):
        if(left[l].foldername <= right[r].foldername):
            final.append(left[l])
            l += 1
        else:
            final.append(right[r])
            r += 1
    if(l < len(left)): final += left[l:]
    elif(r < len(right)): final += right[r:]
    return final
