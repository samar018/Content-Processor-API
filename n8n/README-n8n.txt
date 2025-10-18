Perfect ✅ — so now we can create a **README section for your n8n workflow** and also explain the `Article-processor-Agent-workflow.json` file. This will guide anyone to import and run your workflow.

Here’s how you can add it to your project documentation:

---

# 📂 n8n Workflow – Article Processor Agent

### 🧩 Workflow File

* **File Name:** `Article-processor-Agent-workflow.json`
* **Purpose:** Automates the entire AI article processing pipeline:

  1. Receives article URL + email via webhook
  2. Scrapes article content using Firecrawl
  3. Summarizes article with OpenAI
  4. Extracts 3–5 key insights with OpenAI
  5. Appends results to Google Sheets
  6. Sends an email with summary + insights

---

## ⚙️ How to Import Workflow in n8n

1. Open your n8n instance ([https://app.n8n.cloud](https://app.n8n.cloud) or local)
2. Go to **Workflows → Import from File**
3. Select the file: `Article-processor-Agent-workflow.json`
4. Click **Import**

---

## 🔧 Configure Nodes

### 1️⃣ Webhook Node

* Ensure the **Webhook URL** matches what your backend sends to:

  ```
  POST http://127.0.0.1:8000/process-article
  ```
* Copy the webhook path into your FastAPI backend.

### 2️⃣ Firecrawl Node

* Method: `POST`
* URL: `https://api.firecrawl.dev/v1/scrape`
* Headers:

  ```
  Authorization: Bearer <YOUR_FIRECRAWL_API_KEY>
  Content-Type: application/json
  ```
* Body JSON:

  ```json
  {
    "url": "{{ $json.body.article_url }}"
  }
  ```
* Output: `data.content` (article text)

### 3️⃣ OpenAI Node 1 – Summarization

* Prompt:

  ```
  Summarize the following article in 3–5 sentences:
  {{ $json.data.content }}
  ```
* Model: `gpt-4o-mini` (or your preferred model)

### 4️⃣ OpenAI Node 2 – Insights

* Prompt:

  ```
  Extract 3–5 key insights from the following summary:
  {{ $json.output }}
  ```

### 5️⃣ Google Sheets Node

* Action: *Append Row*
* Columns:

  * `session_id`
  * `article_url`
  * `summary`
  * `insights`
  * `email`
  * `timestamp`

### 6️⃣ Email Node

* To: `{{ $json.body.email }}`
* Subject: `Your Article Summary & Insights`
* Body:

  ```
  📰 Summary:
  {{ $json.summary }}

  💡 Insights:
  {{ $json.insights.join("\n- ")}}

  Best regards,
  Your AI Agent 🤖
  ```

---

## ⚡ Test the Workflow

1. Start your n8n workflow
2. Submit test data from backend or frontend:

```json
{
  "email": "test@example.com",
  "article_url": "https://www.bbc.com/news/articles/cgqlyw9g7weo",
  "session_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

3. Check:

* Google Sheet row appended
* Email received
* Workflow execution log shows success

---

## 🏷 Notes

* Make sure your **Firecrawl API key** is set in environment variables or node credentials.
* Make sure **Google Sheets credentials** are connected to your n8n account.
* Ensure **email node** is configured correctly (SMTP/Gmail/Outlook).


