import Navigator

class UI:
    def __init__(self):
        self.folders = Navigator.initialise_objects()
        self.topic_filters = set() #Inclusive filter
        self.lecturer_filters = set() #Inclusive filter

    #Can these filters be merged
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

    def display_info(self):
        valid_files = []
        for foldername in self.folders:
            folder = self.folders[foldername]
            valid_files += folder.search(self.topic_filters, self.lecturer_filters)

        #Just temporarily doing stuff
        for file in valid_files:
            print(file)