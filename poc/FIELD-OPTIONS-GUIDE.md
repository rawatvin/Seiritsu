# Seiritsu POC - Field Options Management Guide

**Edit Allowed Values for List Fields**

---

## 🎯 Overview

You can now **edit the allowed values** (options) for protected list-type fields like Market, Status, and Funding Source. This allows you to customize dropdown values without compromising the core field structure required by the system.

**Key Principle:**
- ✅ **CAN** edit list of allowed values (options)
- ❌ **CANNOT** delete the field itself
- ❌ **CANNOT** change field name, type, or section

---

## 📋 Which Fields Have Editable Options?

### Protected Fields with Editable Options

| Field Name | Display Label | Current Options | Usage |
|------------|---------------|-----------------|-------|
| **market** | Market(s) in Scope | Global, EMEA, North America, APAC, Latin America, Greater China | Filters in Kanban, Dashboard, All Requests |
| **status** | Status | Submitted, Under Review, Approved, Committed, In Progress, Completed, On Hold, Rejected | Kanban columns, Timeline filter, Dashboard stats |
| **fundingSource** | Funding Source | Global, Market, Mixed, TBD | Timeline filter, Budget tracking |
| **requestCategory** | Request Category | New Feature, Enhancement, Bug Fix, Technical Debt, Research, Other | Classification, Reporting |

### Other Protected Fields (No Options to Edit)

These fields don't have options because they're not list-type:
- `request` (Text)
- `requestId` (Auto-generated)
- `submissionDate` (Date - auto)
- `requesterName` (Contact)
- `globalTechLead` (Contact)
- `globalBusinessLead` (Contact)
- `marketSuccessOwner` (Contact)
- `watchers` (Text)
- `ballparkValue` (Money)
- `expectedStartDate`, `expectedEndDate`, `actualStartDate`, `actualEndDate` (Dates)

---

## ✏️ How to Edit Options

### Step-by-Step: Edit Market Values

**Scenario:** You want to add "Middle East" as a new market option.

1. **Open Settings**
   - Click the **"Settings"** tab in navigation

2. **Find the Field**
   - Scroll through the Field Configuration table
   - Find row with:
     - Field Name: **Market(s) in Scope**
     - Technical name: `market`
     - Type: Single Select
     - Status: Protected

3. **Click Edit Options**
   - In the Actions column, click **"Edit Options"** button
   - Modal opens

4. **Edit Options List**
   - Modal shows field properties (all disabled except Options)
   - Notice at top: *"Protected Field: You can only edit the list of allowed values..."*
   - Options field shows current values (one per line):
     ```
     Global
     EMEA
     North America
     APAC
     Latin America
     Greater China
     ```
   - Add new line:
     ```
     Global
     EMEA
     North America
     APAC
     Latin America
     Greater China
     Middle East
     ```

5. **Save Changes**
   - Click **"Save Field"** button
   - Confirmation: "Options updated successfully!"

6. **Verify Changes**
   - Go to All Requests → + New Request
   - Check Market dropdown
   - ✅ "Middle East" now appears!

---

## 🎨 Use Cases

### Use Case 1: Add New Market Region

**Situation:** Company expands to new region  
**Action:** Add "Southeast Asia" to market options  
**Steps:**
1. Settings → Find `market` field → Edit Options
2. Add line: `Southeast Asia`
3. Save
4. Now available in all dropdowns

---

### Use Case 2: Rename Status Value

**Situation:** Change "Under Review" to "Feasibility Assessment"  
**Action:** Edit status options

**⚠️ IMPORTANT:** If you change status names, you MUST update:
- **Kanban View:** Column headers (manual code update required)
- **Timeline View:** Filter logic checks for "Committed", "In Progress", "Completed"
- **Dashboard:** "In Progress" stat calculation

**Recommended Approach:**
1. **DON'T** rename existing status values if they're used in logic
2. **Instead:** Add new values, migrate data, then remove old values
3. **Or:** Keep technical names stable, use display labels

**How to Safely Add Status:**
1. Settings → Find `status` field → Edit Options
2. Add new status at end (e.g., `Backlog`)
3. Save
4. New status appears in dropdowns
5. Update Kanban view columns if needed

---

### Use Case 3: Add Funding Type

**Situation:** New funding model "Partner Co-Funded"  
**Action:** Add to fundingSource options

**Steps:**
1. Settings → Find `fundingSource` field → Edit Options
2. Current: Global, Market, Mixed, TBD
3. Add: `Partner Co-Funded`
4. Save
5. Now available when creating/editing requests

---

### Use Case 4: Add Request Category

**Situation:** Track "Strategic Initiative" separately from other categories  
**Action:** Add new request category

**Steps:**
1. Settings → Find `requestCategory` field → Edit Options
2. Current: New Feature, Enhancement, Bug Fix, Technical Debt, Research, Other
3. Add: `Strategic Initiative`
4. Save
5. Users can now select this category

---

## 🔒 What You CANNOT Change

When editing options for protected fields:

❌ **Field Name** - Disabled (technical name `market` cannot change)  
❌ **Display Label** - Disabled (stays "Market(s) in Scope")  
❌ **Description** - Disabled  
❌ **Field Type** - Disabled (stays Single Select)  
❌ **Section** - Disabled (stays Requester Information)  
❌ **Required** - Disabled  

✅ **Options** - ONLY this is editable

**Why?** These properties are hardcoded into the system logic. Changing them would break:
- Dashboard filtering
- Kanban view columns
- Timeline view logic
- Statistics calculations

---

## ⚠️ Important Considerations

### 1. Removing Options with Existing Data

**Question:** What if I remove "APAC" from market options, but 20 requests already use "APAC"?

**Answer:**
- The field will be updated successfully
- Existing requests with "APAC" will **keep** the value
- But "APAC" won't show in dropdowns for new/edited requests
- This creates "orphaned" data

**Best Practice:**
1. Export data (Data Management → Export as Excel)
2. Check if any requests use the value you want to remove
3. If yes, update those requests first or keep the option
4. If no, safe to remove

### 2. Status Values and Timeline

**Critical:** Timeline view filters by these exact status names:
- `Committed`
- `In Progress`
- `Completed`

If you rename or remove these, timeline will break.

**To Fix:**
1. Open HTML file in text editor
2. Find `renderTimeline()` function (around line 1621)
3. Update this line:
   ```javascript
   requests = requests.filter(r =>
       ['Committed', 'In Progress', 'Completed'].includes(r.status) &&
       r.expectedStartDate && r.expectedEndDate
   );
   ```
4. Replace with your new status names

**Example:**
If you changed "Committed" to "In Delivery", "In Progress" to "Building", update to:
```javascript
['In Delivery', 'Building', 'Completed'].includes(r.status)
```

### 3. Kanban View and Status

**Kanban columns are hardcoded** in the HTML. If you add/remove status values, they won't automatically appear as columns.

**Current Columns:**
1. Submitted
2. Under Review
3. Approved
4. Committed
5. In Progress
6. Completed
7. On Hold
8. Rejected

**To add a new status column:** Manual HTML/JavaScript update required (beyond POC scope).

**Workaround:** Use existing status names, just add more granularity in comments or custom fields.

### 4. Dashboard Statistics

Dashboard "In Progress" stat counts items with status = "In Progress" or "Committed".

If you change these status names, update the dashboard rendering logic.

---

## 💡 Best Practices

### DO:
✅ Add new market regions as you expand  
✅ Add new funding sources for new business models  
✅ Add new request categories for better classification  
✅ Export data before making changes  
✅ Test changes with a sample request  
✅ Communicate changes to users  

### DON'T:
❌ Remove status values used in Timeline logic  
❌ Rename status values without updating code  
❌ Remove options that existing data uses  
❌ Add too many options (keep dropdowns manageable)  
❌ Use special characters in option names  
❌ Create duplicate option names  

---

## 🧪 Testing Your Changes

### After Editing Options:

**Test 1: Create New Request**
1. All Requests → + New Request
2. Check dropdown for your field
3. Verify new option appears
4. Select it and save
5. ✅ Should work

**Test 2: Edit Existing Request**
1. All Requests → Click Edit on a request
2. Check dropdown
3. Verify new option appears
4. Change to new option and save
5. ✅ Should update

**Test 3: Filters**
1. Kanban View → Use filter dropdown
2. Verify new option appears
3. Select and apply filter
4. ✅ Should filter correctly

**Test 4: Export/Import**
1. Data Management → Export as Excel
2. Open Excel
3. Check if new option appears in data
4. ✅ Should be there

---

## 🔄 Sample Scenarios

### Scenario 1: Company Expansion

**Before:**
- Markets: Global, EMEA, North America, APAC, Latin America, Greater China

**Change:** Expand to new regions
1. Settings → Edit market options
2. Add: `Africa`, `Middle East`, `India`
3. Save

**After:**
- Markets now include Africa, Middle East, India
- Users can select these when creating requests
- Reports can filter by new markets

---

### Scenario 2: New Funding Model

**Before:**
- Funding Sources: Global, Market, Mixed, TBD

**Change:** Add partner co-funding option
1. Settings → Edit fundingSource options
2. Add: `Partner Co-Funded`, `External Grant`
3. Save

**After:**
- Users can specify partner funding
- Better financial tracking
- More accurate portfolio reporting

---

### Scenario 3: Refine Categories

**Before:**
- Categories: New Feature, Enhancement, Bug Fix, Technical Debt, Research, Other

**Change:** Split "Other" into specific types
1. Settings → Edit requestCategory options
2. Remove: `Other`
3. Add: `Process Improvement`, `Compliance`, `Training`
4. Save

**After:**
- More precise categorization
- Better portfolio mix analysis
- Clearer reporting

---

## 📊 Impact on Different Views

### Dashboard
- Filters use option values
- Stats calculations check specific status values
- No immediate impact from adding options

### Kanban View
- Filters use option values
- Columns hardcoded (adding status won't add column)
- Cards show current option values

### Timeline View
- **Critical:** Uses hardcoded status check for "Committed", "In Progress", "Completed"
- Funding filter uses fundingSource options
- Must update code if renaming these statuses

### All Requests
- Filters use option values
- Table displays option values
- Immediate impact when options change

### Settings
- Shows updated options in field list
- Options column displays new values

---

## 🚨 Troubleshooting

**Problem:** I edited options but dropdown still shows old values

**Solution:**
1. Refresh the browser (Ctrl+R / Cmd+R)
2. Clear browser cache if needed
3. Check if you saved changes (click "Save Field")

---

**Problem:** Timeline is empty after changing status names

**Solution:**
1. You renamed a status used by Timeline logic
2. Open HTML in text editor
3. Update `renderTimeline()` function with new status names
4. Or: Revert status names to original

---

**Problem:** I removed an option but some requests still show it

**Solution:**
- This is expected behavior
- Existing data keeps old values
- New requests won't have that option
- To clean up: Export → Find/Replace → Import

---

**Problem:** I added an option but it doesn't appear in Kanban columns

**Solution:**
- Kanban columns are hardcoded
- Adding status values won't create new columns
- This requires code update (beyond POC scope)
- Consider using existing status names

---

## 📝 Documentation Checklist

When you edit field options, document:

- [ ] What field you changed
- [ ] What options you added/removed
- [ ] Date of change
- [ ] Reason for change
- [ ] Which views are impacted
- [ ] Any code updates needed
- [ ] Communication sent to users

**Example:**
```
Field: market
Change: Added "Middle East" and "Africa"
Date: 2026-05-20
Reason: Business expansion into new regions
Impact: Filters in all views, dropdown in forms
Code Updates: None required
Communication: Emailed portfolio team
```

---

## 🎯 Quick Reference

**Edit Market Options:**
Settings → Find `market` → Edit Options → Add/Remove → Save

**Edit Status Options:**
Settings → Find `status` → Edit Options → Add/Remove → Save  
⚠️ Don't rename: Committed, In Progress, Completed (used by Timeline)

**Edit Funding Options:**
Settings → Find `fundingSource` → Edit Options → Add/Remove → Save

**Edit Category Options:**
Settings → Find `requestCategory` → Edit Options → Add/Remove → Save

**Remove Sample Data:**
Data Management → Remove Sample Data → Confirm

---

**Last Updated:** May 19, 2026  
**File:** Seiritsu-Working-POC.html  
**Feature:** Field Options Management
