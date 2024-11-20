## FLASHCARDS : A game to memorise the main commands needed to be operational in the data professions.

THIS PROJECT IS CONSTANTLY EVOLVING.

### Table of Contents

1. [Project Purpose](#projet)
2. [Installation](#install)
3. [Files Descriptions](#files)
4. [Authors and motivations](#authors)



### What is the project ? <a name="projet"></a>

This python program, designed in the form of a question and answer format, lets you practise memorising the essential commands of certain APIs that you need to know to succeed in the data professions.

For each question, the user validates to make the answer appear on the screen. If the answer is correct, they answer O for ‘yes’, otherwise they simply confirm.

For each wrong answer, a counter is incremented by one for the question asked. Conversely, if the answer is correct, the counter decreases by one point (until it reaches a minimum of zero).

The programme starts by asking the questions with the highest counter, followed by the questions with a counter of zero. Questions with the same counter are arranged by date from oldest to newest.

When the user stops the programme using the ‘STOP’ command, the programme updates on the database the counter and the current date for each question that has been asked.

At the start of the program, the question database (flashcards.csv) is checked. Lines in error are corrected :

- no counter => counter set to zero

- no date => date set to 19/03/1969

- no question or answer => ‘a completer’.

### Installation <a name="install"></a>

To play with the project download the dataset (flashcards.csv) and the python program (flashcard.py). Then run the python file 'python3 flashcard.py'.

To reset the counters and dates to zero, you need to update the 'flashcards.csv' file by deleting the last two columns. When the programme is launched, you will be asked to complete the counters to zero and to set the date to 19/03/1969.

### Files Descriptions <a name="files"></a>

 * flashcard.py : program written with Python 3.12 
    
 * flashcards.csv :  database with questions and answers composed of 5 variables 
 - groupe : each question is attached to a group. The groups are bash / SQL / py for Python / git / spark
 - question : question
 - answer : answer
 - compteur : counteur for each question
 - date_derniere_question : the date the last question was asked

### Authors & Motivations <a name="authors"></a>

This project was carried out by Guillaume NONY as part of the ‘data upskilling’ course prepared and presented by Benjamin DUBREU.

