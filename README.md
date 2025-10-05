# Why?
To help me study norwegian using my paper textbook with minimal work outside of said textbook.  

# What is a premise?
1. Take a photo of a book.   
2. Scrap text from photo using OCR.   
3. Translate norwegian words to english.   
4. Use LLM to translate it into polish.   
5. Hear pronunciation.   

# What does it do now?  
Not sure for now. It's implemented as PoC even for the scope of this project.  
Even main.py will be updated to reflect more standard FastAPI ways (it likely won’t work in its current form, as it only served its initial purpose).  
  
# Use    
Run on local host -> address -> 0.0.0.0:8000 (or 127.0.0.1:8000)  
If you want to use phone check your ipv4 then add port (:8000) -> somthing like 192.168.X.X:8000  
  
address/send  
Send photo (can be done with phone conncected to the same network)
  
address/transcribe  
Choose photo -> it will redirect somewhere (now to the page with json on the screen)

# Instalation
Section in progress, like others :)

# What is the plan for it?
Create somewhat of database for words  
Listen to pronunciation for words and sentences  
Check knowledge with flashcards or something else (?)  
Dictionary (NOR -> ENG -> PL As english wikitionary (API) gives more information than polish one.)  

# Known issues   
There are some, but main one:  
- Algorithm used to straighten images only works with white pages (no black backround).  
And time of course, i wanted to use local OpenAI model, and I can't make it not to think.  
