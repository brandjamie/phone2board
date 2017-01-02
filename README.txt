phone2board gameserver is a pyhon application for mobile phone use in classrooms.

The program allows the teacher to show a 'global web page' on a project showing students progress, a 'control page' on a laptop (or phone) for the teacher to control the procedings and 'client pages' on each connected phone/tablet/laptop for students to answer questions. There are currently six different types of quiz.

Usage:
python phone2board.py quiz.json

Where 'quiz.json' is a file containing the 'quiztype' as well as relevent paramaters, questions and answers (if applicable). 
If no json file is provided a default quiz is started.


Quiz Types and parameters:

'default':

This allows the entering of question prompts on the control page to appear on the global page. Answers sent from the client pages appear on the global page. The teacher can mark answers correct or incorrect individually or enter a correct answer and have all the client pages marked simultaniously. This gametype does not need any config file and is run when the program is started with no config file.

'fixed_answers':

The config file contains the questions and answers. The teacher sends each question to the global page and students can answer using their devices. All questions are marked simultaniously (although the teacher can mark each answer independently or change marks if neccesary). Answers are case sensitive but multiple answers are possible. 

The config json must include the gametype, a description of the quiz ('notes'), an array of questions ('questionarray') and a matching array of answers ('answerarray'). Multiple answers can be seperated by a forwardslash ('/'). 

An example json can be found in 'quizzes/present_simple_fixed_answers.json'

'open_answers':

The config file contains only the questions. The teacher should mark each answer seperately (though they have the option to enter an answer and mark simultaniously if applicable).

The config json must include the gametype, a description of the quiz ('notes') and an array of questions ('questionarray'). 

An example json can be found in 'quizzes/present_simple_open_answers.json'

'fixed_timed':
The config file contains the questions and answers. The teacher sends each question to the global page and a timer starts. Students answer using their devices at the end of the time the students answer is shown on the board. The time for each question is 60 seconds by default but can be changed from the control page.

All questions are marked simultaniously (although the teacher can mark each answer independently or change marks if neccesary). Answers are case sensitive but multiple answers are possible. 

The config json must include the gametype, a description of the quiz ('notes'), an array of questions ('questionarray') and a matching array of answers ('answerarray'). Multiple answers can be seperated by a forwardslash ('/'). 

An example json can be found in 'quizzes/present_simple_fixed_timed.json'

'open_timed':

The config file contains only the questions.The teacher sends each question to the global page and a timer starts. Students answer using their devices at the end of the time the students answer is shown on the board. The time for each question is 60 seconds by default but can be changed from the control page.

The teacher should mark each answer seperately (though they have the option to enter an answer and mark simultaniously if applicable).

The config json must include the gametype, a description of the quiz ('notes') and an array of questions ('questionarray'). 

An example json can be found in 'quizzes/present_simple_open_timed.json'



'multiq':

The config file contains questions and answers for multiple 'levels'. The questions are shown on the client page in a randomized order where students answer them and progress through the levels. The global page shows a leaderboard of how students(clients) are progressing through the levels.

The config json includes the gametype, a description of the quiz, and an array of dictionaries for each level.
Each level is described by a dictionary containing:
'instructions' - (string) instructions for that level,
'numNeeded' - (int) the number needed to get correct to move to the next level 
'resetOnMistake' - (bool) If true the number needed resets after each mistake.
'clearAnswer' - (bool) If true any incorrect answers are cleard from the input box after marking.
'qarray' - (array of strings) The question array.
'aarray' - (array of strings) The answer array.


An example json can be found in 'quizzes/multiq_mixedtense.json'



Dependencies:

This project includes the jquery and howler.js libraries both of which are released under the MIT licence.

The project requires python 3 and tornado web server installed.

All audio files are public domain from kennysassets or are believed to be otherwise public domain. 
