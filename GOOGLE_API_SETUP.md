# Google Fact Check API - Setup Instructions

## ⚠️ You have OAuth2 credentials, but we need an API Key

The JSON file you downloaded is for OAuth2 authentication (used for user login flows).
For TrustNet, we need a simpler **API Key** for server-to-server calls.

---

## 🔧 Get the Correct API Key

### Step 1: Go to Google Cloud Console
https://console.cloud.google.com/

### Step 2: Select your project
- Project: `meta-domain-475310-p3` (from your JSON file)

### Step 3: Enable Fact Check Tools API
1. Click "APIs & Services" → "Library"
2. Search for "Fact Check Tools API"
3. Click "ENABLE" (if not already enabled)

### Step 4: Create API Key
1. Click "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "API Key"
3. A new API key will be created
4. Copy the API key (looks like: AIzaSyDxxxxxxxxxxxxxxxxxxxxxx)
5. (Optional) Click "RESTRICT KEY" to secure it:
   - API restrictions → Select "Fact Check Tools API"
   - Save

### Step 5: Add to .env file
```bash
GOOGLE_FACTCHECK_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔍 Alternative: Use Custom Search API

If you also want to use Google Custom Search (for reverse image search):

### Enable Custom Search API
1. In Google Cloud Console → APIs & Services → Library
2. Search for "Custom Search API"
3. Click "ENABLE"

### Create Custom Search Engine
1. Go to: https://programmablesearchengine.google.com/
2. Click "Add" to create new search engine
3. Sites to search: "Search the entire web"
4. Name it: "TrustNet Fact Checker"
5. Copy the "Search engine ID" (CX parameter)

### Add to .env file
```bash
GOOGLE_CSE_ID=your-search-engine-id-here
GOOGLE_CSE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxx  # Same or different API key
```

---

## ✅ What to do with your OAuth2 JSON file

You can:
1. **Keep it** - Might be useful if you want to add user authentication later
2. **Delete it** - Not needed for current TrustNet setup
3. **Move it** - Create a `credentials/` folder and store it there

For now, we don't need it for the fact-checking functionality.

---

## 🧪 Test Your API Key

Once you have the API key, test it:

```bash
# Test Fact Check API
curl "https://factchecktools.googleapis.com/v1alpha1/claims:search?query=vaccines&key=YOUR_API_KEY"
```

You should get JSON results with fact-check information.

---

## 📝 Quick Summary

**What you need to do:**
1. ✅ Go to Google Cloud Console
2. ✅ Enable "Fact Check Tools API" 
3. ✅ Create an API Key (NOT OAuth2)
4. ✅ Add key to `.env` file as `GOOGLE_FACTCHECK_API_KEY`
5. ✅ Test the API key with curl command above

**Current status:**
- ❌ OAuth2 credentials (not what we need)
- ⏳ Waiting for API Key

Let me know when you get the API key and I'll help you configure it! 🚀
