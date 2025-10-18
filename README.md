Excellent 🔥 — you’re building a **complete AI Agent system** with:

* 🧠 **n8n Workflow** (handles scraping, summarization, insights, Sheets + email)
* ⚙️ **FastAPI Backend** ([Content-Processor-API](https://github.com/samar018/Content-Processor-API))
* 💻 **Frontend** ([Article-processor-Agent-using-n8n-firecrawl](https://github.com/samar018/Article-processor-Agent-using-n8n-firecrawl))

Here’s a **complete `README.md`** you can put in your main repo (or both repos, with small edits).
It’s written cleanly for **project demo + grading** (as per your Module 16 task).

---

## 🧩 **AI Article Processor Agent – n8n + Firecrawl + FastAPI + Frontend**

### 🚀 Project Overview

This project builds an **AI-driven content processor** that allows users to input an **article URL** and **email**, and then receive:

* A **summary** of the article,
* **3–5 key insights**,
* An **email** with the results,
* And all data logged automatically into **Google Sheets**.

The system integrates:

* **Frontend (Lovable.dev / React)** for user input,
* **FastAPI Backend** to generate session IDs and forward data,
* **n8n Workflow** for web scraping, AI summarization, insight extraction, and emailing results.

---

## ⚙️ Architecture & Data Flow

```
Frontend → FastAPI Backend → n8n Webhook → Firecrawl → OpenAI (Summary + Insights)
     ↓                                            ↓
 Google Sheets (Stores Data) ← Email Tool (Sends Summary + Insights)
```

### 🔄 Step-by-Step Flow

1. **User enters**:

   * Email
   * Article URL

2. **Backend (FastAPI)**:

   * Generates a unique `session_id`
   * Sends `{ email, article_url, session_id }` to the **n8n webhook**

3. **n8n Workflow**:

   * **Webhook** receives data
   * **Firecrawl** scrapes article content
   * **OpenAI Node 1** → Summarizes article
   * **OpenAI Node 2** → Extracts 3–5 insights
   * **Google Sheets Node** → Appends a row with:

     * `Session ID`, `Article URL`, `Summary`, `Insights`, `Email`, `Timestamp`
   * **Email Node** → Sends summary and insights to user

---

## 🧠 n8n Setup Instructions

### 1️⃣ Create n8n Account

* Go to [https://app.n8n.cloud](https://app.n8n.cloud)
* Create a workflow

### 2️⃣ Add Nodes

Your workflow should follow this structure:

```
Webhook → Firecrawl → OpenAI (Summarize) → OpenAI (Insights) → Google Sheets → Email
```

### 3️⃣ Node Configuration

#### 🧩 **Webhook Node**

* Method: `POST`
* Path: `/webhook-test/<your-unique-id>`
* Expected Input:

  ```json
  {
    "email": "user@example.com",
    "article_url": "https://example.com/article",
    "session_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```

#### 🔥 **Firecrawl Node**

* Type: **HTTP Request**
* Method: `POST`
* URL: `https://api.firecrawl.dev/v1/scrape`
* Headers:

  ```
  Authorization: Bearer {{ $env.FIRECRAWL_API_KEY }}
  Content-Type: application/json
  ```
* Body (JSON):

  ```json
  {
    "url": "{{ $json.body.article_url }}"
  }
  ```
* Response field:
  `data.content` → full article text

#### 🧠 **OpenAI Node 1 (Summarization)**

Prompt:

```
Summarize the following article into 3–5 sentences:
{{ $json.data.content }}
```

#### 🧩 **OpenAI Node 2 (Insights Extraction)**

Prompt:

```
Extract 3–5 key insights from the following summary. 
Focus on the most important facts, findings, or takeaways that a reader should remember.

Summary:
{{ $json.output }}
```

#### 📊 **Google Sheets Node**

* Action: *Append Row*
* Columns:

  * Session ID
  * Article URL
  * Summary
  * Insights
  * Email
  * Timestamp

#### ✉️ **Email Node**

* To: `{{ $json.body.email }}`
* Subject: `Your Article Summary & Insights`
* Message:

  ```
  Hi there 👋,

  Here’s your article summary and insights.

  📰 Summary:
  {{ $json.summary }}

  💡 Key Insights:
  {{ $json.insights }}

  Thanks,
  Your AI Agent 🤖
  ```

---

## 🧰 Backend Setup – FastAPI

### 📁 Repo

👉 [Content-Processor-API](https://github.com/samar018/Content-Processor-API)

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/samar018/Content-Processor-API.git
cd Content-Processor-API
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Server

```bash
uvicorn main:app --reload
```

Your API runs at → `http://127.0.0.1:8000`

### 5️⃣ Test Endpoint

```bash
curl -X POST "http://127.0.0.1:8000/process-article" \
     -H "Content-Type: application/json" \
     -d '{
     "email": "samardas.edu@gmail.com",
     "article_url": "https://www.bbc.com/news/articles/cgqlyw9g7weo"
}'
```

Expected Output:

```json
{
  "status": "success",
  "session_id": "e3e01b02-3ca3-4402-8ba5-31c43de98387",
  "message": "Data successfully sent to n8n webhook"
}
```

---

## 💻 Frontend Setup

### 📁 Repo

👉 [Article-processor-Agent-using-n8n-firecrawl](https://github.com/samar018/Article-processor-Agent-using-n8n-firecrawl)

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/samar018/Article-processor-Agent-using-n8n-firecrawl.git
cd Article-processor-Agent-using-n8n-firecrawl
```

### 2️⃣ Start Lovable.dev App

If built using **Lovable.dev**:

* Open in Lovable editor
* Replace backend API URL with your local (or deployed) backend:

  ```javascript
  const API_URL = "http://127.0.0.1:8000/process-article";
  ```
* Or, if deployed using ngrok:

  ```javascript
  const API_URL = "https://yourname.ngrok.io/process-article";
  ```

### 3️⃣ Run and Test

Enter:

* Email
* Article URL

Click **Process Article**
✅ You’ll see:

* Backend response success
* Email sent to your inbox
* New row in Google Sheets

---

## 📊 Deliverables for Submission

✅ Video demo (3–5 min):

* Show user entering input on frontend
* Show backend logs
* Show n8n workflow run
* Show Google Sheet update
* Show email received

✅ Files:

* `n8n_workflow.json` export
* Backend (FastAPI) code
* Frontend (Lovable.dev) code

---

## 🏁 Evaluation Criteria

| Criteria                 | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| 🔗 Integration           | Frontend → Backend → n8n works correctly             |
| 🧠 Workflow Completeness | Scraping → Summarization → Insights → Sheets → Email |
| 🎥 Demo Clarity          | End-to-end shown clearly                             |
| ⚙️ Code Quality          | Clean, modular, and documented                       |

---

## 🧾 Author

👤 **Samar Das**

Built using FastAPI, n8n, Firecrawl, OpenAI, Google Sheets, and Lovable.dev

---

Would you like me to tailor this README for your **frontend repo** separately (so it only explains how to connect to backend + demo usage)?
