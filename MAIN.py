import TopicParser
import UserInterface

def main():
    TopicParser.extract_topics()
    ui = UserInterface.UI()

    ui.display_info()
    print()
    ui.add_topic_filter("Functions")
    ui.display_info()
    print()
    ui.remove_topic_filter("Functions")
    ui.add_lecturer_filter("Steven Bradley")
    ui.display_info()
    print()
    print("Running")

if __name__ == "__main__":
    main()