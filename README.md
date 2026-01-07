# Typing Speed Test (Tkinter)

A desktop typing speed test built with **Python** and **Tkinter**, designed to measure typing performance using **Words Per Minute (WPM)** and **accuracy**.  
The app includes multiple typing paragraphs, each with its **own persistent high score**.

---

## Features

- ⏱️ **5-second countdown** before typing begins
- ⌨️ **30-second typing test**
- 📄 **5 different typing paragraphs**
- 🏆 **Separate high score for each paragraph**
- 📊 **WPM calculation** (standard: 5 characters = 1 word)
- 🎯 **Accuracy tracking** based on correct characters
- 💾 **Persistent high scores** stored locally in JSON
- 🔒 Input locked outside the typing window
- 🖱️ Minimal, draggable, always-on-top window
- ♻️ Reset high score (per paragraph or all)

---

## How Scoring Works

- **Correct characters** are counted by comparing typed text to the target paragraph position-by-position.
- **Accuracy (%)** = `(correct characters ÷ total typed characters) × 100`
- **WPM** = `(correct characters ÷ 5) ÷ minutes`

Only correct characters contribute to the final WPM score.

---

## How to Use

1. Select a paragraph from the dropdown
2. Click **Start**
3. Wait for the 5-second countdown
4. Type the paragraph as accurately and quickly as possible for 30 seconds
5. View your **WPM**, **accuracy**, and **high score**

---

## High Scores

- Each paragraph has its **own high score**
- High scores are saved in `high_scores.json`
- You can:
  - Reset the current paragraph’s high score
  - Reset all paragraph high scores

---

## Technologies Used

- Python 3
- Tkinter (standard Python GUI library)

---

## File Overview

