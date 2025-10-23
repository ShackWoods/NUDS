import os
import Navigator

class UI:
    def __init__(self):
        self.folders = Navigator.initialise_objects()
        self.all_topics = set()
        self.all_lecturers = set()
        self.topic_filters = set() #Inclusive filter
        self.lecturer_filters = set() #Inclusive filter

        for foldername in self.folders:
            for file in self.folders[foldername].files:
                self.all_topics = self.all_topics.union(file.get_topics())
                self.all_lecturers = self.all_lecturers.union(file.get_lecturers())

    def load_file(self, filename: str):
        try:
            folder, file = filename.split("/")
        except:
            print(f"{filename} is not a file - did you include a /?")
            return

        known_folders = self.folders.keys()
        if(folder not in known_folders):
            print(f"'{folder}' is not a folder")
            return

        for real_file in self.folders[folder].files:
            real_filename = real_file.filename
            if(file.upper() != real_filename.upper()):
                continue
            source_path = os.getcwd() ###[1]
            file_path = source_path + "/" + folder + "/" + real_filename + ".docx"
            os.startfile(file_path) ###[2]
            return
        print(f"'{file}' is not a file in '{folder}'")
        return

    def list_lecturers(self):
        for lecturer in self.all_lecturers:
            print(lecturer)

    def list_topics(self):
        for topic in self.all_topics:
            print(topic)
                
    #Can these filters be merged ***
    def add_topic_filter(self, filter: str):
        self.topic_filters.add(filter)

    def remove_topic_filter(self, filter: str):
        self.topic_filters.remove(filter)

    def add_lecturer_filter(self, filter: str):
        self.lecturer_filters.add(filter)

    def remove_lecturer_filter(self, filter: str):
        self.lecturer_filters.remove(filter)
    #End of mergeable filters

    def toggle_folder_filter(self, filter: str):
        self.folders[filter].hidden = not self.folders[filter].hidden #Exclusive filter

    def display_info(self, sort_mode: str):
        valid_files = []
        for foldername in self.folders:
            folder = self.folders[foldername]
            valid_files += folder.search(self.topic_filters, self.lecturer_filters)

        match sort_mode:
            case "DA": #by date, ascending
                sorted_files = Navigator.sort_by_date(valid_files)
            case "DD": #by date, descending
                sorted_files = Navigator.sort_by_date(valid_files, ascending=False)
            case "FA": #by fodler, ascending
                sorted_files = Navigator.sort_by_folder(valid_files)
            case "FD": #by folder, descending
                sorted_files = Navigator.sort_by_folder(valid_files, ascending=False)
            case _:
                sorted_files = valid_files
        for file in sorted_files:
            print(file)

'''
[1] - geeksforgeeks <https://www.geeksforgeeks.org/python/get-current-directory-python/> Accessed on 10/10/2025
[2] - Nick on stackoverflow <https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os> Accessed on 15/10/2025
'''

'''
***NO
The goals of modularisations:
- Make it easy to read
- Separate and solve subproblems
- Make it easy to debug

The last goal is actually two goals in one:
- Make it easy to find and fix a problem
- Make it easy to determine sufficient test cases for all that can go wrong*
*For example, take the fun that is covering all reasonable states for a .docx file to be in when topic parsing
*In that case we build the system to reduce how the user can interact

This is also why switch-case statements are valid, as we can inherently design test cases according to the cases we match.

Yes merging them makes the code smaller, but if I change the structure of the topic filter (for example)
then the one function is no longer sufficient
'''