# Habit Tracker (Python Backend)

## 📌 Project Overview

This project is a **Python-based habit tracking application backend**, developed as part of an academic assignment (IU – Development Phase / Phase 2).  
The goal is to help users **define, track, and analyse habits** using **Object-Oriented Programming (OOP)** for core domain logic and **Functional Programming (FP)** for analytics.

The application is **CLI-based (Command Line Interface)** and focuses on clean architecture, testability, and clear documentation.  
No graphical user interface (GUI) is required.

---

## 🎯 Key Features (Mapped to Acceptance Criteria)

### ✅ Habit Management (OOP)
- Habits are represented as a **Habit class**
- Each habit has:
  - Name
  - Periodicity (**daily** or **weekly**)
  - Creation timestamp
  - Completion (check-off) timestamps
- Users can:
  - Create habits
  - Delete habits
  - Check off habits within a period

### ✅ Periodicity Support
- **Daily habits** (e.g., “Drink water every day”)
- **Weekly habits** (e.g., “Go to the gym once a week”)

### ✅ Check-offs & Streaks
- A habit is considered completed for a period if it is checked off **at least once**
- Missing a period **breaks the streak**
- Supports:
  - Longest streak for a given habit
  - Longest streak across all habits

### ✅ Analytics Module (Functional Programming)
Implemented using **pure, stateless functions**:
- List all tracked habits
- Filter habits by periodicity
- Find the **longest streak across all habits**
- Find the **longest streak for a specific habit**

> No file I/O, printing, or mutation inside analytics functions.

### ✅ Data Persistence
- Habit data is stored between sessions using **JSON**
- Implemented with Python’s built-in `json` module
- File location: `data/habits.json`

### ✅ Predefined Habits & Test Fixtures
- **5 predefined habits**
  - At least **1 daily**
  - At least **1 weekly**
- Each predefined habit includes **4 weeks of example completion data**
- Used for:
  - Demonstration
  - Testing (fixtures)
  - Validation of streak logic

### ✅ Command Line Interface (CLI)
- Clean and easy-to-use interactive menu
- Allows users to:
  - Create habits
  - Delete habits
  - Check off habits
  - View analytics results
  - Load predefined fixture data

### ✅ Testing
- Comprehensive **unit tests** using `pytest`
- Tests cover:
  - Habit model validity
  - JSON persistence
  - Analytics correctness (FP module)
  - Basic CLI smoke test

---

## 🛠️ Tech Stack & Tools

- **Python**: 3.7 or later
- **Testing**: pytest
- **Persistence**: JSON (built-in `json`)
- **CLI**: built-in `input()` loop (no external CLI frameworks)

---


## 📁 Project Structure
```
habit_tracker/
│
├── README.md
├── requirements.txt
├── main.py
│
├── habit_tracker_app/
│   ├── models/          # OOP domain models (Habit, Completion)
│   ├── storage/         # JSON persistence layer
│   ├── analytics/       # Functional programming analytics
│   ├── cli/             # Command Line Interface
│   ├── seed/            # Predefined habits & fixtures
│   └── utils/           # Date & validation helpers
│
├── data/
│   └── habits.json      # Stored habit data
│
└── tests/               # Pytest unit tests
```

---

## 🚀 Installation & Setup

### 1️⃣ Prerequisites

- Python **3.7 or later**
- `pip` installed

Check Python version:
```bash
python --version
```

### 2️⃣ Clone / Download Project
```bash
git clone <repository-url>
cd habit_tracker
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application (CLI)

Start the habit tracker:
```bash
python main.py
```

On startup, you will see a menu allowing you to:

- Load predefined habits (recommended for first run)
- Start with an empty dataset

---

## 📦 Loading Predefined Habits (Fixtures)

From the CLI menu:

1. Choose **"Load predefined habits"**
2. This loads:
   - 5 predefined habits
   - 4 weeks of example completion data
3. Data is persisted to `data/habits.json`

This fixture data is also used for testing and validation.

---

## 📊 Running Analytics from CLI

From the main menu, select **Analytics**:

- View all tracked habits
- Filter habits by periodicity (daily / weekly)
- View:
  - Longest streak across all habits
  - Longest streak for a selected habit

Analytics results are computed using functional programming logic.

---

## 🧪 Running Tests

Run the full unit test suite with:
```bash
pytest
```

Tests include:

- Habit model validation
- JSON storage correctness
- Analytics streak calculations
- CLI import/smoke tests

All tests are isolated and do not modify real application data.

---

## 📄 Documentation & Code Quality

- All modules include Python docstrings
- Clear separation of concerns:
  - **OOP** → domain logic
  - **FP** → analytics
  - **CLI** → user interaction
- Clean, readable, and maintainable code
- Fully self-contained and suitable for IU submission

---

## ✅ Notes

This project satisfies all required acceptance criteria:

- ✅ Python 3.7+
- ✅ OOP-based habit model
- ✅ Daily & weekly habits
- ✅ Check-offs & streak logic
- ✅ FP-based analytics module
- ✅ JSON persistence
- ✅ Predefined habits with 4-week fixtures
- ✅ CLI-based clean API
- ✅ Unit testing with pytest
- ✅ Clear installation & usage documentation

---

## 👨‍💻 Author

**Harsh**  
Bachelor of Computer Science  
IU International University of Applied Sciences

---

## 📝 License

This project is created for educational purposes as part of IU coursework.