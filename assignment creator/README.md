# AI Assignment Creator

A Streamlit web application that uses Claude AI to generate balanced, academically sound assignments. Provide your topics and total marks — the tool allocates marks proportionally, generates varied question types, and produces a ready-to-use Word document.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [API Setup](#api-setup)
- [Running the App](#running-the-app)
- [Using the App](#using-the-app)
  - [Step 1 — Enter Your API Key](#step-1--enter-your-api-key)
  - [Step 2 — Fill in Assignment Details](#step-2--fill-in-assignment-details)
  - [Step 3 — Add Support Documents (Optional)](#step-3--add-support-documents-optional)
  - [Step 4 — Add Topics](#step-4--add-topics)
  - [Step 5 — Generate the Assignment](#step-5--generate-the-assignment)
  - [Step 6 — Review and Edit](#step-6--review-and-edit)
  - [Step 7 — Download](#step-7--download)
- [Support Documents Guide](#support-documents-guide)
- [Mark Allocation Logic](#mark-allocation-logic)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Features

- Automatic mark distribution across topics based on complexity
- Varied question types matched to mark weight (define, explain, discuss, evaluate, etc.)
- Upload PDF reference material to ground questions in your actual course content
- Lock specific topic marks while letting AI distribute the rest
- Editable preview before downloading
- Export as Word document (`.docx`) or JSON
- Word document includes a Teacher Copy with mark allocation rationale

---

## Requirements

- Python 3.8 or higher
- An Anthropic API key ([get one here](https://console.anthropic.com/))
- Windows (batch scripts included), or any OS with Python installed

---

## Installation

**Windows (recommended):**

1. Clone or download this repository.
2. Double-click `setup.bat` to install all dependencies automatically.

**Manual install (any OS):**

```bash
pip install -r requirements.txt
```

Dependencies installed:

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `anthropic` | Claude API client |
| `pdfplumber` | PDF text extraction |
| `python-docx` | Word document generation |
| `python-dotenv` | Load API key from `.env` file |

---

## API Setup

The app uses the **Anthropic Claude API**. You need an API key to use it.

### Getting your API key

1. Go to [console.anthropic.com](https://console.anthropic.com/) and create an account.
2. Navigate to **API Keys** in the left sidebar.
3. Click **Create Key**, give it a name, and copy the key (it starts with `sk-ant-`).

### Setting up the key (choose one method)

**Method 1 — Enter it in the app (easiest):**

Paste your API key into the sidebar field when the app opens. Optionally click **Save** to write it to a `.env` file so you don't have to enter it every session.

**Method 2 — Create a `.env` file manually:**

Create a file named `.env` in the project folder with the following content:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

The app will load this automatically on startup.

**Method 3 — System environment variable:**

```bash
# Windows (Command Prompt)
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# macOS / Linux
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

> **Keep your API key private.** Never commit it to version control or share it publicly. The `.env` file is excluded from git by default.

---

## Running the App

**Windows:**

Double-click `run.bat`.

**Any OS:**

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## Using the App

### Step 1 — Enter Your API Key

Open the **sidebar** (left panel). Paste your Anthropic API key into the **Claude API Key** field.

- Click **Save** to store it in a `.env` file for future sessions.
- If your `.env` file already has the key, the field will be pre-filled.

---

### Step 2 — Fill in Assignment Details

Fill in the fields in the **Assignment Details** section:

| Field | Required | Notes |
|---|---|---|
| Assignment Title | No | Leave blank and AI will suggest one based on your topics |
| Course / Subject | Yes | e.g. "Biology 101" or "Introduction to Economics" |
| Total Marks | Yes | Between 10 and 500 (default: 100) |
| Time Allowed | No | e.g. "2 hours" — shown on the student document |
| Student Instructions | No | Any instructions printed at the top of the assignment |

---

### Step 3 — Add Support Documents (Optional)

Upload one or more **PDF files** in the **Reference Material** section. This is optional but strongly recommended — it makes the questions more relevant to your actual course content.

See the full guide: [Support Documents Guide](#support-documents-guide).

---

### Step 4 — Add Topics

In the **Topics** section, list the topics you want covered in the assignment.

- Click **+ Add Topic** to add more topics.
- Click **Remove** to delete a topic.
- For each topic, enter the topic name.
- Optionally enable **Lock marks** to fix how many marks that topic gets. Leave it off to let the AI decide.

> **Mark locking rule:** The sum of all locked marks cannot exceed your total marks. The app will show a warning if this happens and disable the generate button.

**Example:**

| Topic | Locked Marks |
|---|---|
| Cell Structure | (unlocked — AI decides) |
| Photosynthesis | 30 marks (locked) |
| Respiration | (unlocked — AI decides) |

With 100 total marks and Photosynthesis locked at 30, the AI will distribute the remaining 70 marks between Cell Structure and Respiration based on complexity.

---

### Step 5 — Generate the Assignment

Click the **Generate Assignment** button. Generation takes approximately 30–60 seconds.

The button will be disabled if:
- No API key is entered
- No topics have been filled in
- Locked marks exceed the total

---

### Step 6 — Review and Edit

After generation, a **Preview & Edit** section appears:

- **Summary bar** — shows total questions, total marks, and topics covered.
- **Mark allocation rationale** — expand this to see why the AI distributed marks the way it did.
- **Topic sections** — expand each topic to see its questions. You can edit the mark value for each question directly.
  - A live warning appears if your edited totals no longer match the target.
- Click **Regenerate** to start over with the same settings.

---

### Step 7 — Download

Two download options are available:

| Button | Format | Contents |
|---|---|---|
| Download Word Document | `.docx` | Student-ready assignment + Teacher Copy with rationale |
| Download JSON | `.json` | Raw structured data for further processing |

The Word document includes:
- Assignment title and course
- Marks and time allowed
- Student instructions
- Questions grouped by topic with mark annotations
- A **Teacher Copy** section at the end with the full mark allocation rationale

---

## Support Documents Guide

Support documents let you upload your course material (textbooks, lecture notes, past papers, etc.) so that generated questions are based on what you actually taught — not just what the AI knows generally.

### What formats are supported

Only **PDF files** (`.pdf`) are supported.

### How to prepare your PDFs

- Lecture notes exported as PDF from PowerPoint or Google Slides work well.
- Scanned PDFs may not work if the text is not machine-readable (i.e. it's an image). Use a PDF with selectable text.
- Textbook chapters: you can upload just the relevant chapters rather than the whole book.
- Multiple PDFs can be uploaded at once — all text is combined.

### How to upload

1. Go to the **Reference Material** section.
2. Click **Browse files** or drag and drop your PDFs.
3. You will see a confirmation that the files have been uploaded.
4. Proceed to add topics and generate.

### How the documents are used

- Text is extracted from all pages of each uploaded PDF.
- The combined text (up to 60,000 characters) is sent to Claude alongside your topic list.
- Claude uses this as context when writing questions, preferring terminology, examples, and concepts from your material.
- If the total text exceeds 60,000 characters, it is truncated. Upload only the most relevant sections if you have large documents.

### Tips

- For best results, upload material that specifically covers the topics you listed.
- Uploading unrelated material will not improve results and uses up the character limit.
- If no PDFs are uploaded, Claude generates questions from general academic knowledge of the topic names alone.

---

## Mark Allocation Logic

The AI distributes marks according to these principles:

1. **Locked topics** get exactly the marks you specified.
2. **Unlocked topics** receive marks from the remaining pool, weighted by estimated topic complexity.
3. Within each topic, question types are matched to mark ranges:

| Question Type | Typical Marks |
|---|---|
| Define / State / List | 1–2 marks |
| Explain / Describe / Outline | 3–5 marks |
| Discuss / Analyse / Compare | 6–10 marks |
| Evaluate / Justify / Critique | 8–15 marks |

4. The app auto-corrects any rounding errors by adjusting the final question on the largest topic so the total always matches exactly.

---

## Troubleshooting

**"API key not set" error**

Make sure you have entered your API key in the sidebar. If you saved it to `.env`, check the file exists in the project folder and contains `ANTHROPIC_API_KEY=sk-ant-...`.

**Generation is taking a long time**

Generation typically takes 30–60 seconds. Do not close the browser tab. If it fails after a long wait, it may be a rate limit issue — wait a minute and try again.

**Rate limit errors**

The app retries automatically up to 3 times with exponential backoff. If it still fails, your account may have hit its usage limit. Check your usage at [console.anthropic.com](https://console.anthropic.com/).

**PDF text not being extracted**

Your PDF may be a scanned image rather than text-based. Open the PDF and try to select text with your cursor — if you cannot, the PDF is image-only and cannot be processed. Export or convert it to a text-based PDF first.

**Locked marks validation warning**

The sum of all locked marks must be less than your total marks. Reduce one or more locked values, or increase the total marks.

**Edited totals warning in preview**

If you manually edit question marks in the preview, the total for that topic may no longer match what was generated. This is a warning only — the download will use whatever values you entered.

**App does not open in browser**

Navigate to `http://localhost:8501` manually in your browser.

---

## Project Structure

```
assignment creator/
├── app.py              # Main Streamlit application (UI and export logic)
├── creator.py          # Claude API integration and assignment generation
├── pdf_utils.py        # PDF text extraction utility
├── requirements.txt    # Python dependencies
├── setup.bat           # Windows: install dependencies
├── run.bat             # Windows: launch the app
└── .env                # Your API key (created by app or manually — do not commit)
```
