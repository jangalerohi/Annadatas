# 🌾 ANNADATA – Pure Village Pulses (Django Project)

Annadata is a complete Django-based web platform for selling 100% organic pulses sourced directly from trusted village farmers.  
The project includes a fully functional frontend (HTML/CSS/JS) and backend (Django), with features like product listings, order tracking, authentication, and Razorpay payment integration.

---

## 🌐 Live Backend URL  
https://annadatas-2.onrender.com/

---

# ⚙️ Features  
- 🌿 100% Organic Village Pulses  
- 🛒 Product Catalog & Details  
- 💳 Razorpay Payment Integration  
- 👤 User Login / Signup  
- 🛍 Cart Functionality  
- 📦 Order Tracking  
- 📱 Fully Responsive Frontend  
- 📊 Admin Panel  
- 🎨 Static Files (CSS / JS / Images)

---

# 📁 Project Structure
Annadatas/
│── Annadata/ # Django project (settings.py, wsgi.py)
│── websites/ # Django application
│── template/ # HTML pages (Frontend UI)
│── static/ # CSS, JavaScript, Images
│── env/ # Virtual environment (not uploaded)
│── manage.py
│── db.sqlite3
│── requirements.txt


### 1️⃣ Clone the repository
```bash
git clone https://github.com/jangalerohi/Annadatas.git
cd Annadatas


How Run Project
2️⃣ Create virtual environment
python -m venv env
3️⃣ Activate environment
Windows:
env\Scripts\activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Run the server
python manage.py runserver

🔐 Environment Variables (Optional for local)

Create a .env file:

SECRET_KEY=your_secret_key
DEBUG=True
RAZORPAY_KEY_ID=your_id
RAZORPAY_KEY_SECRET=your_secret

🚀 Deployment (Render)
✔ Build Command
pip install -r requirements.txt && python manage.py collectstatic --noinput

✔ Start Command
gunicorn Annadata.wsgi
