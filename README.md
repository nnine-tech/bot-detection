# 🤖 Bot Detection System

A simple system that analyzes website traffic and detects bots vs real users.

## 🎯 What does it do?

- **Reads log files** - Your server access logs
- **Detects bots** - Using machine learning
- **Creates reports** - CSV files with results
- **Provides API** - For real-time checking

## 📋 Requirements

```
pip install -r requirements.txt
Python 3.8+
MongoDB

```

## ⚡ Quick Setup

### 1. Download & Install

```bash
git clone <your-repo>
cd bot-detection-system

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Database Setup

**Local MongoDB:**
- Install MongoDB
- Start the service

**Or use MongoDB Atlas (free cloud)**

### 3. Configuration

Create `.env` file:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=bot_detection
```

### 4. Add Log Files

Put your log files in `data/` folder:
```
data/
  - access.log
  - access.log.1
```

### 5. Run It

```bash
# Run everything
python src/main.py

# Start API server
uvicorn src.api:app --reload
```

## 📁 File Structure

```
bot-detection-system/
├── data/           ← Put log files here
├── output/         ← Results go here
├── src/            ← Code files
├── .env            ← Settings
└── requirements.txt
```

## 🚀 Usage

### Command Line
```bash
python src/main.py           # Full process
python src/train_model.py    # Train model only
python src/predict.py        # Predict only
```

### API
After starting API server, go to: `http://localhost:8000/docs`

## 📊 Output

Results saved as CSV in `output/` folder:
- Bot IPs list
- Detection confidence
- Traffic patterns

## 🔧 Log Format Expected

```
192.168.1.1 - - [01/Jan/2024:12:00:00 +0000] "GET /page HTTP/1.1" 200 1234 "referer" "user-agent"
```

## 🛠️ Common Issues

**MongoDB Error:**
- Check if MongoDB is running
- Verify connection string

**No Log Files:**
- Put files in `data/` folder
- Check file permissions

**Import Errors:**
- Run: `pip install -r requirements.txt`
- Check virtual environment
- 
## 🎯 Detection Features
The bot detection model uses the following features:

- **Status codes (`status`)** → High error responses (4xx/5xx).
- **User agent patterns (`ua_has_bot_like_keyword`)** → Detect bot-like UA strings.
- **Referrer check (`referrer_is_missing`)** → Missing referrer indicates non-human traffic.
- **HTTP method (`method`)** → Identifies abnormal request types.
- **Endpoint accessed (`endpoint`)** → Bots often target repetitive/suspicious URLs.
- **Request timing & frequency (`timestamp`)** → Detects unnatural request intervals.
- **Aggregated behavior metrics** → e.g., request volume per IP, error ratios.



---

**Note:** Test with sample data first before running on large log files!
