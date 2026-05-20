# Seiritsu POC - Quick Start Guide

**5-Minute Setup**

---

## 🚀 Step 1: Open the POC (30 seconds)

1. Navigate to: `C:\Users\rawatvin\Seiritsu-Project\poc\`
2. Double-click: **`Seiritsu-Working-POC.html`**
3. Opens in your browser ✅

**No installation needed!**

---

## 📊 Step 2: Load Sample Data (30 seconds)

1. Click **"Data Management"** tab
2. Click **"Load Sample Data"** button
3. Click **"OK"** to confirm
4. ✅ 100 sample requests loaded!

---

## 🎨 Step 3: Explore Features (3 minutes)

### Dashboard Tab
- See stats: Total requests, your assignments, value
- View "My Assignments" table
- See chart

### Kanban View Tab
- **Try this:** Drag a card from one column to another
- Status updates automatically! 🎯
- Use filters at top (Market, Country, Funding)

### Timeline Tab
- Shows committed items
- Filter by Market/Global funded
- Color-coded (green=Market, yellow=Global)

### All Requests Tab
- Full table of all requests
- Click **"Edit"** on any request to see form
- Click **"+ New Request"** to add one

---

## 📥 Step 4A: Import Your Excel Data (1 minute)

**If you have data in Excel:**

1. Go to **"Data Management"** tab
2. Click **"Export as Excel"** (to get template)
3. Open the exported Excel file
4. Replace sample data with YOUR data
5. Save the Excel file
6. Click **"Import Excel"** in POC
7. Select your file
8. ✅ Your data imported!

**Excel Column Names (copy/paste into Row 1):**
```
request | description | ballparkValue | requesterName | requestCategory | market | countries | globalBusinessLead | globalTechLead | status | globalComments | marketSuccessOwner | productArea | capabilityId | fundingSource | linkedMustLand | estimatedCapitalCost | estimatedOperatingCost | costEstimationDetails | expectedStartDate | expectedEndDate | actualStartDate | actualEndDate
```

**Required:** `request` and `requesterName` (all others optional)

---

## 📥 Step 4B: Import Your JSON Data (1 minute)

**If you have data in JSON format:**

1. Create a JSON file (see format below)
2. Go to **"Data Management"** tab
3. Click **"Import JSON"**
4. Select your JSON file
5. ✅ Data imported!

**JSON Format:**
```json
[
  {
    "request": "Your Request Title",
    "description": "Problem statement",
    "ballparkValue": 1000000,
    "requesterName": "Your Name",
    "market": "EMEA",
    "status": "Submitted"
  }
]
```

---

## 💾 Step 5: Export Your Data (30 seconds)

**Export as Excel (Recommended):**
1. Go to **"Data Management"** tab
2. Click **"Export as Excel"**
3. Downloads: `seiritsu-export-YYYY-MM-DD.xlsx`
4. Open in Excel, edit, re-import!

**Export as JSON (Backup):**
1. Click **"Export as JSON"**
2. Downloads: `seiritsu-export-YYYY-MM-DD.json`
3. Technical backup format

---

## 🎯 Key Features At a Glance

| Feature | What It Does |
|---------|-------------|
| **Dashboard** | Personalized view of YOUR assignments |
| **Kanban** | Drag-drop cards to change status |
| **Timeline** | See committed items by funding source |
| **All Requests** | Full table with edit/delete |
| **Import Excel** | Bulk upload from Excel file |
| **Export Excel** | Download as Excel for editing |
| **Filters** | Filter by market, country, status, funding |
| **Real Database** | Data persists between sessions (IndexedDB) |

---

## 📋 All 26 Fields Captured

**Requester (9 fields):**
1. Request (title)
2. Description
3. Ballpark Value (€)
4. Request ID (auto)
5. Requester Name
6. Request Category
7. Market
8. Countries
9. Submission Date (auto)

**Portfolio Team (9 fields):**
10. Global Business Lead
11. Global Tech Lead
12. Status
13. Global Comments
14. Market Success Owner
15. Product Area
16. Capability ID
17. Funding Source
18. Linked Must Land

**Tech Lead - Cost & Timeline (8 fields):**
19. Estimated Capital Cost (€)
20. Estimated Operating Cost (€)
21. Cost Estimation Details
22. Expected Start Date
23. Expected End Date
24. Actual Start Date
25. Actual End Date
26. Delay Status (auto-calculated)

---

## 🎨 Demo Tips (10-Minute Presentation)

**Opening (2 min):**
- "This is a working POC with real database"
- Load sample data
- Show Dashboard

**Kanban Demo (3 min):**
- Click "Kanban View"
- **DRAG a card** between columns
- "Status updates in real-time!"
- Show filters

**Timeline Demo (2 min):**
- Click "Timeline"
- Filter by "Market Funded"
- Point out color coding

**Form Demo (2 min):**
- Click "All Requests" → "+ New Request"
- Scroll through 26 fields
- "All organized by owner team"

**Data Import Demo (1 min):**
- Click "Data Management"
- Show "Export as Excel"
- "Can bulk import from Excel!"

---

## 📱 Bonus: Mobile Access

**The POC works on mobile too!**

1. Email yourself the HTML file
2. Open on phone
3. Add to home screen (iOS: Share → Add to Home Screen)
4. ✅ App-like experience on mobile!

**Or:** Host it on any web server and access via URL

---

## 🔧 Troubleshooting

**Data not saving?**
- Check browser supports IndexedDB (Chrome, Edge, Firefox, Safari do)
- Check not in Incognito/Private mode

**Import not working?**
- Excel: Make sure column names match (case-insensitive)
- Excel: Check at least `request` and `requesterName` have data
- JSON: Validate JSON format at jsonlint.com

**Charts not showing?**
- Check internet connection (Chart.js loads from CDN)
- Refresh page

**Drag-drop not working?**
- Check internet connection (SortableJS loads from CDN)
- Refresh page

---

## 📚 Full Documentation

**Need more details?**

- **POC User Guide:** `POC-USER-GUIDE.md` (complete instructions)
- **Excel Import Guide:** `Excel-Import-Template-Instructions.md` (Excel templates)
- **Implementation Plans:** `../docs/` folder (cost, timeline, features)

---

## ✅ Ready Checklist

Before presenting to management:

- [ ] POC opens in browser
- [ ] Sample data loaded
- [ ] Tested drag-drop in Kanban
- [ ] Exported data as Excel
- [ ] Imported data back from Excel
- [ ] Checked all 4 main views work
- [ ] Prepared your own data (optional)

---

## 🎯 What's Next?

**After management approves:**

1. Use this POC as specification
2. Start Power Platform implementation
3. 12-week timeline to production
4. Budget: $25k-50k (Lean) or $84k-134k (Standard)

**This POC proves the concept works! 🚀**

---

**Total Time: 5 minutes to fully functional demo!**

Open `Seiritsu-Working-POC.html` now! →