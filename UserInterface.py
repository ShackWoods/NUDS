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
            source_path = os.getcwd()
            file_path = source_path + "/" + folder + "/" + real_filename + ".docx"
            os.startfile(file_path)
            return
        print(f"'{file}' is not a file in '{folder}'")
        return

    def list_lecturers(self):
        for lecturer in self.all_lecturers:
            print(lecturer)

    def list_topics(self):
        for topic in self.all_topics:
            print(topic)
                
    #Good practice to not merge
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
