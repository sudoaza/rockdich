# Rockdich

**See huggingface repo for model, dictionary and updates.**
https://huggingface.co/sudoaza/rockdich

Toolkit to translate password dictionaries into German, but possibly to other languages. Includes tools to generate the training dataset by using local ollama or OpenAI API. Fine tune a llama3 model into the translation task using Unsloth. A script to translate a password dictionary using the finetuned model. And finally a translation into German of rockyou.txt as rockdich.txt. Each script has a description comment in the same file.

## Motivation

On the original rockyou.txt dictonary you can find some German passwords but they are a small minority.
We find 50 examples with variations of "passwort" while there are 4685 ocurrances of the English alternative. 
'i.?love.?you' matches 6472 passwords while '(ich)?.?liebe.?dich' matches 117. 
While there are 53k ocurrances of passwords including "girl" variations of "mädchen" are only 30 (usually with "a", sometimes "ae" and rarely the original "ä").

## Results

After translatng the dictionary we get 4593 passwords matching "passwort", 50287 matching 'm.?.?dchen' and 32729 matching '(ich)?.?liebe.?dich'. Notably the model translated the passwords with the correct spelling, so removing umlauts or replacing them with their ae/oe/ue alternatives may be good dictionary mutation strategies.

Access the dictionary here https://huggingface.co/sudoaza/rockdich/resolve/main/rockdich.txt.gz

