# 🧠 Quiz Engine CLI

> **Quiz Engine** is a solo project made only with Python. It is a Command Line Interface (CLI) application. Users can play interactive quizzes, make their own custom tests, and climb the high score list.

This project was built using strict coding rules, without using any external, non-standard libraries (Zero Dependencies). This shows a strong understanding of programming logic and data handling.

### 💡 A Personal Milestone

**Quiz Engine** marks my **first full-cycle application development experience** built entirely from the ground up. The entire journey, from defining the architecture and managing complex data structures, to polishing the final user interface, has been an intensive, hands-on learning process. Every module was written and rigorously tested with the specific goal of demonstrating proficiency in core Python principles within a real-world context.


## ✨ Main Features

*   **🎮 Interactive Game Engine:** Smooth gameplay on the terminal. It manages time, calculates scores with speed bonuses, and handles penalties for wrong answers.
*   **🛠️ Built-in Quiz Creator:** A step-by-step guide that lets users create new quizzes, define questions, options, and difficulty settings, saving everything automatically.
*   **🎨 Colorful Interface:** It uses ANSI escape codes for a nice and readable user experience (without libraries like `colorama`).
*   **💾 Data Saving:** All quizzes and score lists are saved and loaded automatically using JSON files.
*   **🏆 Leaderboard System:** Tracks the best scores for every quiz, saving the username, score, and date.

A new module, **`ai_generator.py`**, has been implemented to handle AI interactions. This feature leverages the power of the **Google Gemini API** to dynamically create quizzes based on user-provided topics.

**Prerequisite:** To use this feature, you **must** provide a Google Gemini API Key. You can obtain one for free at [aistudio.google.com](https://aistudio.google.com/).

## 🚀 Clone & Run (Local Demo)

To get a local copy up and running, follow these simple steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Walliddd/Quiz-Engine
    cd Quiz-Engine
    ```

2.  **Install required dependency for AI functionality:**
    The new AI generation feature requires the `requests` library for network operations.
    ```bash
    pip install requests
    ```

3.  **Run the application:**
    Since the core project strictly avoids external dependencies, only install `requests` if you plan to use the AI feature. The rest of the application runs without it.
    ```bash
    python main.py
    ```

## 📂 Project Structure

The code is split into modules to make it easy to maintain and grow:

```text
quiz-engine/
│
├── data/                 # Holds the quiz .json files and the leaderboard
├── src/                  # Modular source code
│   ├── ui_terminal.py    # Handles input/output and the User Interface (UI)
│   ├── engine.py         # Game logic (scores, timers)
│   ├── data_manager.py   # JSON parsing and file handling
│   ├── colors.py         # Utility for ANSI colors
│   └── ai_generator.py   # Handles connection and validation for AI Quiz Generation (Requires 'requests')
│   └── storage.py        # Handles leaderboard saving
│
├── main.py               # The starting point of the application
└── README.md             # Project documentation
```

## 📅 Progress Status

The core of the project works now, and the main features are done.

- [x] **Initial Project Structure**: Set up the folder structure and modules.
- [x] **JSON Schema Definition**: Standard data structure for quizzes and questions.
- [x] **Dynamic Data Loading**: Strong checking when reading JSON files from the `data/` folder.
- [x] **Game Engine**: Logic for answering, timing, and score calculation.
- [x] **User Interface (UI)**: Navigation menus and visual feedback using colors.
- [x] **Quiz Creator**: Feature to add new quizzes from the CLI.
- [x] **Leaderboard**: System to save and show the best scores.
- [x] **Docstrings** Clean up the code to make it easier to read.
- [x] Add more checks for broken JSON files.
- [x] **AI Quiz Generation Implementation** (New: `ai_generator.py`, requires Google Gemini API Key and `requests`).

### 🔜 Next Steps (To-Do)
- [ ] Implement a "Sudden Death" mode (Hardcore mode).

## 👨‍💻 Author

Project developed by **Wallid** for Midnight.

*Development time tracked on WakaTime: ~50 hours.*

<br>
<div align="center">
<a target="_blank" href="https://hackatime-badge.hackclub.com/U092CKVRNBS/Quiz%20Engine">
<img src="https://hackatime-badge.hackclub.com/U092CKVRNBS/Quiz%20Engine" alt="Quiz Engine Wakatime Badge" />
</a>
</div>
<br>
