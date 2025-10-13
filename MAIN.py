import TopicParser
import UserInterface

def main():
    TopicParser.extract_topics()
    ui = UserInterface.UI()
    print("Running")

if __name__ == "__main__":
    main()