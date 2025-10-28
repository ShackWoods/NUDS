# Note Utility Database Software (NUDS)

NUDS is a program to navigate .docx files that are being used as university notes.

## How to use

>Do not use this as I don't know how to properly package and release python projects

### Prerequisites

Notes must have the following formats:
[Header](#Header:)
[Body](#Body:)
>When i learn how to package, template files will be included

Lecture files must be in folders one level below the python scripts

#### Header:

DATE | TOPIC - LECTURERS

DATE in the form (DD/MM/YYYY)

TOPIC is just the topic of the lecture

LECTURERS - The relevant lecturers separated by a comma

#### Body:

So long as the top most section has the title <COVERED TOPICS> everything will work.

### Using the CLI

>This will become a GUI, but I need to learn TkInter

The CLI accepts the following commands:

"SHOW" - Print all valid files;

- "SHOW DD" - Sort by date, descending

- "SHOW DA" - Sort by date, ascending

- "SHOW FD" - Sort by folder, descending

- "SHOW FA" - Sort by folder, ascending

"TODO" - Print all tasks listed under TODO tags

"EXIT" - End the program

"LOAD *" - Load the file *

"LL" - List all the lecturers

"LT" - List all the topics

FILTERS - use the below commands, appending the name of the topic/lecturer/folder

- "A*" - Add filter

- "R*" - Remove filter

- "*L" - Lecturer filter

- "*T" - Topic filter

- "TF" - Toggle a folder filter

## Why am I making this?

1) I didn't want to spend £50 to share Obsidian files across my devices
2) To provide some more practice with coding in python
3) To practice using git for version control
4) To learn good programming practices
