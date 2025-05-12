
# 🔍 Opportunity Tracker

Automatically track scholarships, internships, awards, and other programs — get predicted deadlines and receive email notifications so you never miss out again!

## ✨ Features

- 🔎 **Google Search + AI Deadline Prediction**  
  Parses program-related webpages to extract past dates and predicts upcoming deadlines.

- 📧 **Email Alerts**  
  Users receive a summary and top links in their inbox instantly.

- 🧠 **Auto Categorization**  
  Classifies each opportunity as Scholarship, Internship, Hackathon, Award, or Other.

- 📊 **Google Sheets Integration**  
  Stores all analyzed data for record-keeping and further analysis.

---

## 🛠️ Tech Stack

- **Frontend:** React + Bootstrap  
- **Backend:** FastAPI (Python)  
- **Data Storage:** Google Sheets (via `gspread`)  
- **Email:** Gmail SMTP  
- **Search:** Google Custom Search API

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/swastim01/opportunity-tracker.git
cd opportunity-tracker
````

### 2. Set up environment variables

Create a `.env` file in the root and add:

```env
GOOGLE_API_KEY=your_google_api_key
CSE_ID=your_custom_search_engine_id
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

### 3. Add Google Sheets credentials

Place your `creds.json` (Google service account credentials) in the root folder.

### 4. Run the backend (FastAPI)

```bash
uvicorn main:app --reload
```

### 5. Start the frontend (React)

```bash
cd frontend
npm install
npm start
```

---

## 📝 Example Use Case

1. Enter a program name like *"Adobe Women in Tech Scholarship"*
2. Add your email.
3. Get back:

   * Predicted deadline
   * Top 3 links
   * Auto-labeled type
   * All stored to Google Sheets
   * A summary email in your inbox 🎯

---

## 📸 Preview

Coming soon! (or you can add a screenshot here)

---

## 📄 License

MIT License

---

## 💡 Future Ideas

* 🔔 Reminders before actual deadlines
* 🗓️ Calendar integration
* 📱 Mobile-friendly UI
* 🧠 Smarter ML-based deadline prediction

---

Made with ❤️ by [@swastim01](https://github.com/swastim01)

