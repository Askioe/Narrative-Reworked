# Narrative

I'll come up with a better description some other time, but the general gist is this is a raid tool thats quite outdated for Discord.
It's quite outdated and needs to introduce new features to make it functional again. Overall needs an entire rework.
If I were to rewrite this I would do it in Go or possibly NodeJs just for efficiency sakes.
Main application would be centered around NT.py.


# How-to-run
In all honesty I don't suggest you run it hence why I am neglecting to include the compiled version of it, the requirements file, and 
optimization to prevent crashes.

# How-it-works
* Creates threading for each individual task
* Sends mass amounts of api requests to discord's url's as everything is electron based
* Can create subprocesses of discord.py applications to do tasks that are inaccessible with requests
* Uses PyQt5 to develop the UI that took me 30 minutes to make
