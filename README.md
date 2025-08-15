Once upon a time, in a land full of keyboards and carpal tunnel syndrome,
someone said: "Why type when I can talk to my browser?"  
And thus, this project was born.  

This is a Flask-powered, browser-based web app that:
- Lives in a `web/` folder (HTML, CSS, JS live here like roommates in a sitcom).
- Gets served to you by `app.py` (a friendly Python concierge).
- Optionally listens to your voice (if you wire up the backend later).
- Comes with a favicon, because every website needs a hat 🎩.

📂 FOLDER TOUR
---------------
Here's what you'll find inside:

1. web/ 🎨  
   - `index.html` → The big stage where your app lives.  
   - `style.css` → The fashion designer for your HTML.  
   - `script.js` → The brains (or chaos gremlin) behind interactions.  
   - `favicon.ico` → The tiny icon next to your tab title (the "website hat").

2. app.py 🐍  
   - Your personal Python butler.
   - Uses Flask to serve everything from `web/`.
   - Knows where the favicon lives (because you always lose it otherwise).

3. README.txt 📜 (this file)  
   - You’re reading it. Congrats. You’re ahead of 90% of users already.

🛠 HOW TO RUN IT
-----------------
Step 1: Install Flask (if not already):
pip install flask

Step 2: Stand in the project folder and run:
python app.py

Step 3: Open your browser and visit:
http://127.0.0.1:5000

Step 4: Enjoy. Or panic if something breaks. Your choice.

💡 TIPS FOR DIFFERENT FOLDERS:
-------------------------------
- If you edit HTML/CSS/JS → Just refresh the browser. No Python restart needed.
- If you edit app.py → Restart the Flask server (CTRL+C, then run `python app.py` again).
- If you add more static files → Put them in `web/` and they’ll magically appear.
- If favicon disappears → Don’t cry. Check `web/favicon.ico` is still there.

🎉 FINISHING WORDS
-------------------
If this works — great, you’re a genius.
If it doesn’t — it’s clearly the computer’s fault. Blame it. Loudly.
