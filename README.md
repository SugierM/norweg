# Why?
To help me study norwegian using my paper textbook with minimal work outside of said textbook.

# What does it do now?
Current implementation only has option to visualize "final" json on the page

Use: 
Run on local host -> address -> 0.0.0.0:8000 (or 127.0.0.1:8000)
If you want to use phone check your ipv4 then add port (:8000) -> somthing like 192.168.X.X:8000

address/send
Send photo (can be done with phone conncected to the same network)

address/transcribe
Choose photo -> it will redirect somewhere (now to the page with json on the screen)


# What is the plan for it?
Create somewhat of database for words
Listen to pronunciation for words and sentences
Check knowledge with flashcards
Dictionary (Will be implemented but I know there is google that is most probably a better solution)

# Known issues
There are some, but main one:
- Algorithm used to straighten images only works with white pages (no black backround).
And time of course, i wanted to use local OpenAI model, and I can't make it not to think.
