# Seiritsu - Settings & Field Configuration Guide

**Configurable Fields System**

---

## 🎯 Overview

The Settings section allows you to customize the fields in your Seiritsu tool. You can:

- ✅ Create custom fields specific to your needs
- ✅ Edit existing custom fields
- ✅ Delete fields you no longer need
- ✅ Configure field types, options, and behavior
- 🔒 Protected fields (required by system) cannot be deleted

**Important:** Some fields are "protected" because they're essential for the tool's core functionality (Dashboard, Kanban, Timeline views). These fields are marked with 🔒 and cannot be deleted.

---

## 📋 Accessing Settings

1. Open Seiritsu POC (`Seiritsu-Working-POC.html`)
2. Click **"⚙️ Settings"** tab in the navigation
3. You'll see the **Field Configuration** table

---

## 🔒 Protected vs Custom Fields

### Protected Fields (Cannot Delete)

These fields are **required by system logic** and marked as Protected:

**Note:** Protected list fields (market, status, fundingSource, requestCategory) allow editing their options/values. See FIELD-OPTIONS-GUIDE.md for details.

**Critical for Dashboard:**
- `requesterName` - Required to filter "My Submissions"
- `globalTechLead` - Required to filter "My Assignments"
- `globalBusinessLead` - Required to filter "My Assignments"
- `marketSuccessOwner` - Required to filter "My Assignments"
- `watchers` - Required to filter "Watching" section

**Critical for Kanban:**
- `status` - Required for columns (Submitted, Under Review, etc.)
- `market` - Required for filtering

**Critical for Timeline:**
- `fundingSource` - Required for filtering (Market/Global)
- `expectedStartDate` - Required for timeline display
- `expectedEndDate` - Required for timeline display
- `actualStartDate` - Required for delay calculation
- `actualEndDate` - Required for delay calculation

**Core Fields:**
- `request` - Request title (required for all views)
- `requestId` - Auto-generated ID
- `submissionDate` - Auto-generated date
- `ballparkValue` - Used in stats and calculations

### Custom Fields (Can Edit/Delete)

All other fields are **custom** and marked with ✏️:
- `description`
- `requestCategory`
- `countries`
- `globalComments`
- `productArea`
- `capabilityId`
- `linkedMustLand`
- `estimatedCapitalCost`
- `estimatedOperatingCost`
- `costEstimationDetails`
- Plus any fields you create!

---

## ➕ Adding a Custom Field

### Step 1: Open Add Field Modal

1. Go to **Settings** tab
2. Click **"+ Add Custom Field"** button
3. Modal opens

### Step 2: Fill Out Field Information

**Required Fields:**

1. **Field Name** (required)
   - Technical name used in database
   - Must be **camelCase** (e.g., `customPriority`, `marketNotes`)
   - No spaces or special characters
   - Start with lowercase letter
   - Example: `regionalApprovalNeeded`

2. **Display Label** (required)
   - What users see in the form
   - Can have spaces and capitals
   - Example: "Regional Approval Needed?"

3. **Field Type** (required) - Choose from:
   - **Text** - Single line text input
   - **Text Area** - Multi-line text (for long descriptions)
   - **Number** - Numeric values
   - **Money (€)** - Currency with € symbol
   - **Date** - Date picker
   - **Checkbox** - Yes/No toggle
   - **Single Select** - Dropdown (choose one option)
   - **Multi-Select** - Multiple checkboxes (choose many)
   - **Contact** - Person name field
   - **Calculation** - Auto-calculated from formula

4. **Section** (required) - Where field appears:
   - Requester Information
   - Portfolio Team
   - Tech Lead - Cost & Timeline
   - Custom Section (you provide name)

**Optional Fields:**

5. **Description** - Help text explaining the field
6. **Options** - For Single/Multi-Select (one per line)
7. **Calculation Formula** - For Calculation type (e.g., `field1 + field2`)
8. **Required Field** - Check to make field mandatory

### Step 3: Save Field

1. Click **"Save Field"**
2. Field is added to configuration
3. Field will now appear in the Add/Edit Request form

---

## ✏️ Editing a Custom Field

1. Go to **Settings** tab
2. Find your field in the table
3. Click **"Edit"** button (only available for custom fields)
4. Modify field properties
5. Click **"Save Field"**

**Note:** You cannot change the **Field Name** when editing (technical name is permanent). If you need a different field name, delete and recreate.

---

## 🗑️ Deleting a Custom Field

### Before Deleting

**Warning checks:**
- ✅ Cannot delete protected fields (🔒)
- ✅ Cannot delete if data exists in that field
- ✅ System checks all existing requests

### Delete Steps

1. Go to **Settings** tab
2. Find your custom field (marked ✏️)
3. Click **"Delete"** button
4. Confirm deletion in popup
5. Field is removed

### If Delete Fails

**Error: "Cannot delete protected field"**
→ This field is required by system logic. It cannot be deleted.

**Error: "It contains data in X existing request(s)"**
→ Some requests have values in this field. Options:
- Keep the field
- Clear data from all requests first
- Archive requests that use it

---

## 📝 Field Types Explained

### 1. Text
- Single line input
- Use for: names, IDs, short descriptions
- Example: Product code, initiative name

### 2. Text Area
- Multi-line input
- Use for: long descriptions, comments
- Example: Problem statement, detailed notes

### 3. Number
- Numeric input only
- Use for: quantities, counts, ratings
- Example: Number of markets, priority score

### 4. Money (€)
- Currency format with €
- Use for: costs, values, budgets
- Example: Estimated cost, revenue impact
- Displays with € symbol

### 5. Date
- Date picker
- Use for: deadlines, milestones
- Format: YYYY-MM-DD
- Example: Review date, launch date

### 6. Checkbox
- Yes/No toggle
- Use for: flags, confirmations
- Example: "Legal approval received?", "Executive sponsor assigned?"

### 7. Single Select (Dropdown)
- Choose ONE option from list
- Use for: categories, status, priorities
- **Example configuration:**
  ```
  Options (one per line):
  High
  Medium
  Low
  ```
- User sees dropdown with 3 choices

### 8. Multi-Select
- Choose MANY options from list
- Use for: tags, features, markets
- **Example configuration:**
  ```
  Options (one per line):
  Mobile App
  Web Portal
  API Integration
  Analytics Dashboard
  ```
- User can select multiple checkboxes

### 9. Contact
- Person name field
- Use for: owners, approvers, stakeholders
- Example: Regional lead, product owner

### 10. Calculation
- Auto-calculated from formula
- Use for: totals, percentages, computed values
- **Formula syntax:** Use field names and operators (+, -, *, /)
- **Example:**
  ```
  Formula: estimatedCapitalCost + estimatedOperatingCost
  ```
- **Example 2:**
  ```
  Formula: ballparkValue * 0.1
  ```
- Field is read-only (user cannot edit)

---

## 🎨 Custom Sections

If default sections don't fit, create your own!

**Default sections:**
- Requester Information
- Portfolio Team
- Tech Lead - Cost & Timeline

**Create custom section:**
1. In Field Type, select **"Custom Section"**
2. New field appears: "Custom Section Name"
3. Enter your section name (e.g., "Regional Details")
4. All fields with this section name are grouped together

**Use cases:**
- "Market-Specific Requirements"
- "Finance Team Review"
- "Legal & Compliance"
- "Executive Approval"

---

## 💡 Example Custom Fields

### Example 1: Priority Field

**Scenario:** You want to track priority (High/Medium/Low)

**Configuration:**
- Field Name: `priority`
- Display Label: Priority
- Description: Business priority level
- Type: Single Select
- Options:
  ```
  High
  Medium
  Low
  ```
- Section: Portfolio Team
- Required: No

**Result:** Dropdown with 3 options appears in form

---

### Example 2: Total Estimated Cost

**Scenario:** Auto-calculate total of capital + operating costs

**Configuration:**
- Field Name: `totalEstimatedCost`
- Display Label: Total Estimated Cost (€)
- Description: Sum of capital and operating costs
- Type: Calculation
- Formula: `estimatedCapitalCost + estimatedOperatingCost`
- Section: Tech Lead - Cost & Timeline
- Required: No

**Result:** Field shows calculated sum automatically

---

### Example 3: Regional Approval Status

**Scenario:** Track which regions approved the request

**Configuration:**
- Field Name: `regionalApprovals`
- Display Label: Regional Approvals
- Description: Which regions have approved this request
- Type: Multi-Select
- Options:
  ```
  EMEA
  North America
  APAC
  Latin America
  Greater China
  ```
- Section: Custom Section → "Regional Review"
- Required: No

**Result:** Users can check multiple regions

---

### Example 4: Legal Review Required

**Scenario:** Flag if legal review is needed

**Configuration:**
- Field Name: `legalReviewRequired`
- Display Label: Legal Review Required?
- Description: Does this request require legal team review?
- Type: Checkbox
- Section: Portfolio Team
- Required: No

**Result:** Simple yes/no checkbox

---

### Example 5: Expected ROI Percentage

**Scenario:** Calculate ROI as percentage of value vs cost

**Configuration:**
- Field Name: `expectedROI`
- Display Label: Expected ROI (%)
- Description: Return on investment percentage
- Type: Calculation
- Formula: `(ballparkValue / estimatedCapitalCost) * 100`
- Section: Portfolio Team
- Required: No

**Result:** Shows calculated ROI automatically

---

## 🔧 Advanced Tips

### Tip 1: Organize by Workflow Stage

Create custom sections matching your workflow:
- "Intake Stage Fields"
- "Feasibility Review Fields"
- "Funding Approval Fields"
- "Execution Tracking Fields"

### Tip 2: Use Calculations for KPIs

Common formulas:
- Total cost: `estimatedCapitalCost + estimatedOperatingCost`
- ROI: `(ballparkValue / estimatedCapitalCost) * 100`
- Cost per market: `estimatedCapitalCost / numberOfMarkets`

### Tip 3: Required vs Optional Strategy

**Make required:**
- Critical business info
- Fields used in reports
- Fields used for approvals

**Keep optional:**
- Nice-to-have details
- Fields used only sometimes
- Exploratory/experimental fields

### Tip 4: Field Naming Convention

**Good field names:**
- `executiveSponsor` ✅
- `targetLaunchDate` ✅
- `riskLevel` ✅

**Bad field names:**
- `Executive Sponsor` ❌ (has spaces)
- `target-launch-date` ❌ (has hyphens)
- `Risk` ❌ (should be descriptive)

### Tip 5: Test Before Rolling Out

1. Add new field in Settings
2. Create a test request to see how it looks
3. Edit the field if needed
4. Once satisfied, announce to team

---

## ⚠️ Important Warnings

### Warning 1: Don't Delete Fields with Data

If you delete a field that has data:
- Data is NOT deleted from database
- But users can no longer see or edit it
- Field becomes "orphaned"

**Best practice:** Export data first, clear field values, then delete.

### Warning 2: Can't Rename Field Name

Once a field is created, its technical **Field Name** is permanent.

**If you need to rename:**
1. Export all data (Excel/JSON)
2. Delete old field
3. Create new field with new name
4. Manually update data

**Better:** Just edit the **Display Label** (what users see)

### Warning 3: Calculation Fields Can Break

If your calculation references a field that gets deleted:
- Calculation will fail
- Shows error or 0

**Solution:** Update calculation formula to remove deleted field

### Warning 4: Protected Fields Exist for a Reason

Don't try to work around protected fields:
- They're used in Dashboard, Kanban, Timeline
- Deleting them would break core features
- System prevents deletion for safety

---

## 🚀 Power User Workflow

### Morning: Review Field Usage

1. Open Settings
2. Scan custom fields
3. Check if any are unused
4. Consider consolidating similar fields

### Quarterly: Field Audit

1. Export all data
2. Analyze which fields are populated
3. Delete unused custom fields
4. Add new fields based on team feedback

### When Onboarding New User

1. Show them Settings tab
2. Explain protected vs custom
3. Show examples of custom fields
4. Encourage them to suggest new fields

---

## ❓ FAQ

**Q: Can I change a field type after creating it?**  
A: Yes, if it's a custom field (not protected). However, data might not display correctly. Example: Changing "Text" to "Number" - existing text data won't convert.

**Q: How many custom fields can I create?**  
A: No hard limit, but keep it practical. Too many fields make the form overwhelming. Aim for <50 total fields.

**Q: Can I reorder fields in the form?**  
A: Not in the POC. In production (Power Platform), field order is configurable.

**Q: What happens if two fields have same Display Label?**  
A: Allowed, but confusing for users. Field Name must be unique (system enforces this).

**Q: Can I hide a field without deleting it?**  
A: Not in the POC. In production, you can set visibility rules.

**Q: Can I make a field conditional (show only if another field = X)?**  
A: Not in the POC. In production (Power Platform), you can use conditional logic.

**Q: How do I backup my field configuration?**  
A: Field config is stored in IndexedDB (browser database). Export data regularly as backup. In production, field config is in SharePoint/Dataverse.

**Q: Can I import field configuration from Excel?**  
A: Not in the POC. Manual configuration only.

**Q: If I delete a custom field, can I restore it?**  
A: No. Once deleted, it's gone. Recreate manually if needed.

---

## 📊 Field Configuration Table Explained

**Columns:**

1. **Status**
   - 🔒 Protected - Cannot delete (required by system)
   - ✏️ Custom - Can edit/delete

2. **Field Name**
   - Bold text = Display label (what users see)
   - `Code text` = Technical field name (database key)

3. **Description**
   - Help text explaining the field

4. **Type**
   - Field type (Text, Date, etc.)
   - Red * = Required field

5. **Options**
   - For Select fields: List of options
   - For Calculation: Formula
   - Otherwise: -

6. **Section**
   - Where field appears in form

7. **Actions**
   - Edit button (custom fields only)
   - Delete button (custom fields only)
   - "Cannot Edit" (protected fields)

---

## 🎯 Best Practices Summary

✅ **DO:**
- Use descriptive field names (camelCase)
- Add helpful descriptions
- Test new fields before announcing
- Group related fields in custom sections
- Review and clean up unused fields quarterly
- Use calculations for auto-computed values
- Make critical fields required

❌ **DON'T:**
- Delete fields that have data
- Create duplicate fields
- Use spaces in field names
- Delete protected fields (system prevents it anyway)
- Create too many fields (keep it manageable)
- Forget to document custom fields for team

---

**Updated:** May 19, 2026  
**File:** Seiritsu-Working-POC.html  
**Feature:** Configurable field system
