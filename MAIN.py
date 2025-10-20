import TopicParser
import TaskParser
import UserInterface


'''
Command List:
SHOW - Show the current valid files
Sort*
D* - by Date*
F* - by Folder*
*A - Ascending*
*D - Descending*

TODO - Parse for any unattended Post-Reading Tasks

EXIT - End the program
LOAD - Load a file (append exact filename)*

L+ - List*
+L - Lecturers*
+T - Topics*

A@ - Add filter
R@ - Remove filter
@L - Lecturer filter
@T - Topic filter
TF - Toggle folder
'''
def main():
    TopicParser.extract_topics()
    ui = UserInterface.UI()
    TaskParser.extract_tasklists(ui.folders)

    running = True
    while running:
        raw_command = input("What would you like to do ")
        splits = raw_command.split(" ")
        command = splits[0].upper()
        operand = " ".join(splits[1:])
        match command:
            case "SHOW": #Show the current valid files
                ui.display_info(operand)
            case "LOAD": #Load the given file
                ui.load_file(operand)
            case "TODO": #Show all tasks you need to do
                TaskParser.announce_tasks()
            case "EXIT": #Exit the program
                running = False
            case "LL": #List lecturers
                ui.list_lecturers()
            case "LT": #List Topics
                ui.list_topics()
            case "AL": #Add lecturer filter
                ui.add_lecturer_filter(operand)
            case "AT": #Add topic filter
                ui.add_topic_filter(operand)
            case "RL": #Remove lecturer filter
                ui.remove_lecturer_filter(operand)
            case "RT": #Remove topic filter
                ui.remove_topic_filter(operand)
            case "TF": #Toggle folder
                ui.toggle_folder_filter(operand)
            case _:
                print(f"{command} is not a valid command")
        print()

if __name__ == "__main__":
    main()