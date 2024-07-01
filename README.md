<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="https://github.com/hieulhaiwork/Meal-Management-Chatbot/blob/main/images/chatbot-for-resturant.jpg" alt="Logo" width="693" height="449">
  </a>

<h3 align="center">Meal Management Chatbot</h3>

  <p align="center">
    This is my personal project to create a chatbot that provides nutritional support for people with health problems. 
    <br />
    <br />
    <a href="https://drive.google.com/file/d/1_7ovjM1mcIwo-BQ1TiK9G0t7g9HdaZXx/view?usp=drive_link">View Demo</a>
  </p>
</div>


  <!-- ABOUT THE PROJECT -->
## About The Project

The chatbot has the ability to:
- Process the user's medical records to provide accurate responses without requiring the user to enter information manually.
- Answer questions about nutrition based on the user's medical conditions, such as 'Is coffee good for me?' or 'Should I eat a lot of sweets?'
- Suggest meals for the user for specific times such as breakfast, lunch, dinner, or snacks.
- Create daily and weekly meal plans for the user.

## Built with

<a href="https://ai.google.dev/gemini-api/docs?hl=vi">Gemini</a>
<br />
<a href="https://www.crewai.com/">CrewAI</a>

## Run

The `requirements.txt` file should list all Python libraries that your notebooks
depend on, and they will be installed using:

```
pip install -r requirements.txt
```

Then create a new file named .env includes:

- <a href="https://aistudio.google.com/app/apikey?hl=vi">GOOGLE_API_KEY</a>
- <a href="https://serper.dev/">SERPER_API_KEY</a>
- MAX_OUTPUT = 100

Finally, run main.py and enjoy!

## Futher Improvement

- Apply user data storage on Google Cloud
- Implement reinforcement learning from human feedback to optimize the chatbot's responses instead of storing them in a file
