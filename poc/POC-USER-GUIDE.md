# Seiritsu Working POC - User Guide

**File:** `Seiritsu-Working-POC.html`

---

## 🎯 What This Is

A **fully functional** proof-of-concept with:
- ✅ Real local database (IndexedDB - stores data in browser)
- ✅ All fields you requested (25+ fields per request)
- ✅ Personalized dashboard
- ✅ Kanban view with drag-drop
- ✅ Timeline view (committed items)
- ✅ Data import/export (JSON)
- ✅ Sample data included
- ✅ Responsive design (works on mobile)

**Cost:** $0 (runs entirely in browser)

---

## 🚀 How to Use

### Step 1: Open the POC

1. Navigate to: `C:\Users\rawatvin\Seiritsu-Project\poc\`
2. Double-click `Seiritsu-Working-POC.html`
3. Opens in your default browser

**No installation, no server, no setup needed!**

---

### Step 2: Load Sample Data

1. Click **"Data Management"** tab
2. Click **"Load Sample Data"** button
3. Confirms: "This will add sample data..."
4. Click **OK**
5. ✅ 6 sample requests loaded!

Now you have data to explore.

---

### Step 3: Explore Features

#### **Dashboard Tab**
- **Stats cards:** Total requests, your assignments, in progress, total value
- **My Assignments table:** Requests assigned to you
- **Chart:** Requests by status (doughnut chart)

**Personalization:** Dashboard shows only YOUR assignments (simulated as "John Doe")

---

#### **Kanban View Tab**
- **5-stage pipeline:** Submitted → Under Review → Approved → Committed → In Progress → Completed
- **Drag & Drop:** Drag cards between columns to change status
- **Filters:**
  - Market (All/EMEA/APAC/etc.)
  - Country (extracted from requests)
  - Funding Source (All/Market/Global)
- **Cards show:** Request ID, title, market, requester, value

**Try it:**
1. Click "Kanban View"
2. Drag a card from "Submitted" to "Under Review"
3. Status updates automatically!

---

#### **Timeline Tab**
- **Shows committed items** (status = Committed/In Progress/Completed)
- **Filter by:**
  - Funding Source (Market/Global)
  - Status
- **Timeline items show:**
  - Request ID & title
  - Funding type (color-coded: green=Market, yellow=Global)
  - Expected dates
  - Actual dates (if started)
  - Delay status (on track / delayed X days)
  - Owner, market, value

**Color coding:**
- Green border-left: Market funded
- Yellow border-left: Global funded

---

#### **All Requests Tab**
- **Full table view** of all requests
- **Filters:** Status, Market
- **Actions:** Edit, Delete buttons
- **+ New Request button:** Add new request

**Try it:**
1. Click "All Requests"
2. Click "Edit" on any request
3. Modal opens with full form
4. Modify fields
5. Click "Save Request"
6. ✅ Updated!

---

### Step 4: Add Your Own Data

#### Option A: Manual Entry

1. Go to "All Requests" tab
2. Click **"+ New Request"**
3. Fill out the form (25+ fields organized by owner team)
4. Click **"Save Request"**

#### Option B: Import Excel ⭐ EASIEST!

1. Create an Excel file (.xlsx or .xls) with your data
2. Go to "Data Management" tab
3. Click **"Import Excel"**
4. Select your Excel file
5. Confirms import
6. ✅ Data loaded!

**Excel Template:**
- See `Excel-Import-Template-Instructions.md` for full guide
- **Quick tip:** Export data first to get a template!

**Excel Column Names:**
```
request, description, ballparkValue, requesterName, requestCategory, 
market, countries, globalBusinessLead, globalTechLead, status, 
globalComments, marketSuccessOwner, productArea, capabilityId, 
fundingSource, linkedMustLand, estimatedCapitalCost, 
estimatedOperatingCost, costEstimationDetails, expectedStartDate, 
expectedEndDate, actualStartDate, actualEndDate
```

**Required columns:** `request` and `requesterName` (all others optional)

#### Option C: Import JSON

1. Create a JSON file with your data (see format below)
2. Go to "Data Management" tab
3. Click **"Import JSON"**
4. Select your JSON file
5. Confirms import
6. ✅ Data loaded!

**JSON Format:**
```json
[
  {
    "request": "Your Request Title",
    "description": "Problem statement",
    "ballparkValue": 1000000,
    "requesterName": "Your Name",
    "requestCategory": "New Feature",
    "market": "EMEA",
    "countries": "Germany, France",
    "globalBusinessLead": "Business Lead Name",
    "globalTechLead": "Tech Lead Name",
    "status": "Submitted",
    "globalComments": "",
    "marketSuccessOwner": "",
    "productArea": "E-Commerce",
    "capabilityId": "CAP-001",
    "fundingSource": "Global",
    "linkedMustLand": "",
    "estimatedCapitalCost": 500000,
    "estimatedOperatingCost": 100000,
    "costEstimationDetails": "Details here",
    "expectedStartDate": "2026-06-01",
    "expectedEndDate": "2026-12-31"
  }
]
```

---

### Step 5: Export Your Data

#### Export as Excel (Recommended)

1. Go to "Data Management" tab
2. Click **"Export as Excel"**
3. Downloads: `seiritsu-export-YYYY-MM-DD.xlsx`
4. ✅ Excel file ready!

**Benefits:**
- Open in Excel, edit, re-import
- Share with colleagues (they can view in Excel)
- Use as template for bulk data entry

#### Export as JSON

1. Go to "Data Management" tab
2. Click **"Export as JSON"**
3. Downloads: `seiritsu-export-YYYY-MM-DD.json`
4. ✅ Backup created!

**Use cases:**
- Technical backup format
- Share with developers
- Move data between browsers
- Smaller file size

---

## 📋 All Fields Included

### Requester Information
1. ✅ Request (title)
2. ✅ Description: Problem / Business Case
3. ✅ Ballpark Incremental Annual NS (€)
4. ✅ Request ID (auto-generated: REQ-0001, REQ-0002, etc.)
5. ✅ Requester Name
6. ✅ Request Category (dropdown)
7. ✅ Market(s) in Scope (dropdown)
8. ✅ Countries in Scope (text)
9. ✅ Submission Date (auto-generated)

### Portfolio Team
10. ✅ Global Business Lead
11. ✅ Global Tech Lead
12. ✅ Status (dropdown: Submitted, Under Review, Approved, Committed, In Progress, Completed, On Hold, Rejected)
13. ✅ Global Comments (textarea)
14. ✅ Market Success Owner
15. ✅ Product Area / Home
16. ✅ Capability ID from Capability Map
17. ✅ Funding Source (dropdown: Global, Market, Mixed, TBD)
18. ✅ Linked Global Must Land

### Cost & Timeline (Global Tech Lead)
19. ✅ Estimated Capital Cost (€)
20. ✅ Estimated Operating Cost (€)
21. ✅ Cost Estimation Details (textarea)
22. ✅ Expected Start Date
23. ✅ Expected End Date
24. ✅ Actual Start Date
25. ✅ Actual End Date
26. ✅ Arriving Early / Delayed (auto-calculated based on dates)

**Total:** 26 fields, organized by owner team in the form!

---

## 🎨 Features Demonstrated

### ✅ Core Functionality
- CRUD operations (Create, Read, Update, Delete)
- Persistent local storage (IndexedDB)
- Data import/export
- Real-time updates (drag-drop updates status)
- Filtering & searching

### ✅ Views
- **Dashboard:** Personalized stats & "My Assignments"
- **Kanban:** Drag-drop pipeline with filters
- **Timeline:** Committed items with funding filter
- **All Requests:** Full table with edit/delete
- **Data Management:** Import/export/sample data

### ✅ UX Features
- Responsive design (mobile-friendly)
- Modal forms (overlay dialogs)
- Color-coded badges (status, funding)
- Interactive charts (Chart.js)
- Drag & drop (SortableJS)
- Auto-calculations (delay status, request ID)

### ✅ Data Features
- Auto-generated Request ID (REQ-0001, REQ-0002...)
- Auto-generated Submission Date
- Auto-calculated delay status (Arriving Early / Delayed)
- Persistent storage (survives page refresh)
- Export/import (JSON format)

---

## 💡 Demo Tips

### For Management Presentation:

**Opening (2 min):**
1. Open POC: "This is a working prototype, not just mockup"
2. Click "Load Sample Data"
3. Show Dashboard: "Personalized for each user"

**Kanban (3 min):**
1. Click "Kanban View"
2. Show filters: "Filter by market, country, funding"
3. **Drag a card:** "Watch status update in real-time"
4. Show different statuses: "5-stage pipeline"

**Timeline (2 min):**
1. Click "Timeline"
2. Show funding filter: "See market vs global funded"
3. Point out color coding: "Green = market, Yellow = global"
4. Show delay status: "Auto-calculated from dates"

**Form (2 min):**
1. Click "All Requests" → "+ New Request"
2. Scroll through form: "25+ fields, organized by owner team"
3. Point out dropdowns, auto-fields
4. "This shows what users would fill out"

**Data Management (1 min):**
1. Click "Data Management"
2. Show export: "Data can be backed up as JSON"
3. Show import: "Can load initial data from CSV → JSON"
4. "Database is local, no server needed for POC"

**Total:** 10-minute demo

---

## 🔧 Technical Details

### How It Works:

**Frontend:**
- Pure HTML + CSS + JavaScript
- No frameworks (lightweight, fast)
- Chart.js for charts
- SortableJS for drag-drop

**Database:**
- IndexedDB (built into browser)
- Stores data locally
- Survives page refresh
- ~5 MB storage limit (enough for 1000s of requests)

**Data Flow:**
```
User Action → JavaScript → IndexedDB → Re-render View
```

**File Structure:**
- Single HTML file (137 KB)
- All CSS inline (easy to customize)
- All JavaScript inline (no dependencies)
- Works offline (no internet needed)

### Limitations (POC-specific):

❌ **Multi-user:** Simulated (everyone is "John Doe")
❌ **Real authentication:** No login (would need backend)
❌ **Server sync:** Each browser has own database
❌ **Real-time collaboration:** Not multi-user (IndexedDB is local)
❌ **File attachments:** Not implemented (would need file storage)
❌ **Email notifications:** Not implemented (would need backend)

**These would be solved in real implementation (Power Platform)!**

---

## 🚀 Customization

### Change User Name:

Line 825 in HTML:
```javascript
const currentUser = {
    name: 'John Doe',  // ← Change this
    initials: 'JD',    // ← Change this
    email: 'john.doe@adidas.com',
    role: 'Portfolio Manager'
};
```

### Change Statuses:

Line 1227:
```javascript
const statuses = ['Submitted', 'Under Review', 'Approved', 'Committed', 'In Progress', 'Completed'];
// Add/remove statuses
```

### Change Markets:

In the form (line 539):
```html
<option>Global</option>
<option>EMEA</option>
<!-- Add more markets -->
```

### Change Colors:

Top of CSS (line 15):
```css
:root {
    --primary: #0078d4;  /* Change to Adidas colors */
    --success: #107c10;
    /* etc. */
}
```

---

## 📊 Sample Data Included

**6 sample requests covering:**
- Different markets (EMEA, APAC, North America, Global)
- Different statuses (Submitted, Under Review, Approved, Committed, In Progress)
- Different funding sources (Market, Global)
- Different values (€1.5M - €4.5M)
- Different categories (New Feature, Enhancement, Technical Debt)

**Requests:**
1. AR Virtual Try-On (APAC, Global funded, In Progress)
2. Sustainability Dashboard (EMEA, Market funded, Approved)
3. AI Size Recommendation (Global, Global funded, Committed)
4. Supply Chain Platform (North America, Global funded, Under Review)
5. Loyalty Program V2 (Global, Global funded, In Progress)
6. Store Inventory Sync (EMEA, Market funded, Submitted)

---

## ✅ What Management Sees

**This POC proves:**
1. ✅ All required fields can be captured
2. ✅ Personalized dashboards are feasible
3. ✅ Kanban view with filters works well
4. ✅ Timeline view shows funding clearly
5. ✅ Data import/export is possible
6. ✅ UI can be professional and usable
7. ✅ Zero infrastructure needed for demo

**What it doesn't prove (needs real implementation):**
- Multi-user collaboration (would use SharePoint/Dataverse)
- Real-time sync across users (Power Platform handles this)
- Authentication/permissions (Azure AD)
- Email notifications (Power Automate)
- JIRA integration (Power Automate connectors)

**But it shows the concept works!**

---

## 🎯 Next Steps After POC

**If approved:**
1. Use this as specification for Power Platform build
2. Field list → SharePoint columns
3. Views → Power Apps screens
4. Filters → Power Apps delegation
5. Data import → SharePoint migration
6. 12-week timeline to production!

---

## 📞 Support

**POC Issues:**
- Clear browser cache if data acts weird
- Try different browser if IndexedDB doesn't work
- Export data before clearing to backup

**POC Files:**
- Working POC: `Seiritsu-Working-POC.html`
- User Guide: `POC-USER-GUIDE.md` (this file)
- Original demo: `Seiritsu-POC-Demo.html`

---

**Ready to present? Open `Seiritsu-Working-POC.html` and show management the working solution!** 🚀