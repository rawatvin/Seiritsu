# Excel Import Template - Seiritsu POC

## How to Create Your Excel File

### Step 1: Create a New Excel File

Open Excel and create a new workbook with the following columns in **Row 1** (header row):

### Column Names (Must Match Exactly)

Copy these column names into your Excel Row 1:

```
requestId | request | description | ballparkValue | requesterName | requestCategory | market | countries | submissionDate | globalBusinessLead | globalTechLead | status | globalComments | marketSuccessOwner | productArea | capabilityId | fundingSource | linkedMustLand | estimatedCapitalCost | estimatedOperatingCost | costEstimationDetails | expectedStartDate | expectedEndDate | actualStartDate | actualEndDate
```

**Note:** Column names are **case-insensitive**. You can use `request`, `Request`, or `REQUEST` - all work!

---

### Step 2: Fill in Your Data

**Required Columns (must have data):**
- `request` - Request title
- `requesterName` - Name of requester

**Optional but Recommended:**
- `description` - Problem/business case
- `market` - Market (Global, EMEA, APAC, North America, Latin America)
- `status` - Status (Submitted, Under Review, Approved, Committed, In Progress, Completed, On Hold, Rejected)
- `ballparkValue` - Annual value in € (number only, no symbols)
- `fundingSource` - Global, Market, or Mixed

**All Other Columns:** Optional

---

### Step 3: Data Format Rules

| Column | Format | Example |
|--------|--------|---------|
| `requestId` | Leave blank (auto-generated) | REQ-0001 |
| `request` | Text | "AR Virtual Try-On Feature" |
| `description` | Text | "Implement AR to reduce returns" |
| `ballparkValue` | Number | 2500000 |
| `requesterName` | Text | "Sarah Chen" |
| `requestCategory` | Text | "New Feature" |
| `market` | Text | "APAC" |
| `countries` | Text | "China, Japan, South Korea" |
| `submissionDate` | Leave blank (auto-generated) | 2026-05-19 |
| `globalBusinessLead` | Text | "Michael Scott" |
| `globalTechLead` | Text | "Jane Smith" |
| `status` | Text | "In Progress" |
| `globalComments` | Text | "Prototype approved" |
| `marketSuccessOwner` | Text | "Wei Zhang" |
| `productArea` | Text | "Mobile App" |
| `capabilityId` | Text | "CAP-001" |
| `fundingSource` | Text | "Global" |
| `linkedMustLand` | Text | "Digital Innovation 2026" |
| `estimatedCapitalCost` | Number | 500000 |
| `estimatedOperatingCost` | Number | 100000 |
| `costEstimationDetails` | Text | "ML models, AR SDK, cloud" |
| `expectedStartDate` | Date (YYYY-MM-DD) | 2026-06-01 |
| `expectedEndDate` | Date (YYYY-MM-DD) | 2026-12-31 |
| `actualStartDate` | Date (YYYY-MM-DD) | 2026-06-15 |
| `actualEndDate` | Date (YYYY-MM-DD) | 2026-12-30 |

**Date Format:** Use `YYYY-MM-DD` (e.g., 2026-06-01) or Excel will recognize most date formats

**Numbers:** Enter as plain numbers (no € symbol, no commas). Excel will format them.

---

### Step 4: Example Data

Here's one complete example row:

| requestId | request | description | ballparkValue | requesterName | requestCategory | market | countries | submissionDate | globalBusinessLead | globalTechLead | status | globalComments | marketSuccessOwner | productArea | capabilityId | fundingSource | linkedMustLand | estimatedCapitalCost | estimatedOperatingCost | costEstimationDetails | expectedStartDate | expectedEndDate | actualStartDate | actualEndDate |
|-----------|---------|-------------|---------------|---------------|-----------------|--------|-----------|----------------|-------------------|----------------|--------|----------------|-------------------|-------------|-------------|---------------|---------------|---------------------|----------------------|---------------------|------------------|----------------|----------------|--------------|
| | AR Virtual Try-On | Implement AR feature for footwear | 2500000 | Sarah Chen | New Feature | APAC | China, Japan, South Korea | | Michael Scott | Jane Smith | In Progress | Prototype approved | Wei Zhang | Mobile App | CAP-001 | Global | Digital Innovation 2026 | 500000 | 100000 | ML models, AR SDK, cloud infrastructure | 2026-06-01 | 2026-12-31 | 2026-06-15 | |

---

### Step 5: Save and Import

1. **Save your Excel file** as `.xlsx` or `.xls`
2. **Open Seiritsu POC** in browser
3. Go to **"Data Management"** tab
4. Click **"Import Excel"** button
5. Select your Excel file
6. Confirm import
7. ✅ Done!

---

## Quick Start: Use Export as Template

**Easiest way to create a template:**

1. Open Seiritsu POC
2. Load sample data
3. Click **"Export as Excel"**
4. Open the exported file
5. Delete sample rows (keep header row!)
6. Add your data
7. Save and re-import

---

## Troubleshooting

### "Excel file is empty or has no data"
- Make sure Row 1 has column headers
- Make sure Row 2+ has data
- Check you're saving as `.xlsx` or `.xls`

### "Error importing Excel file"
- Check column names match (case doesn't matter, but spelling does)
- Make sure at least `request` and `requesterName` columns have data
- Check date formats are valid (YYYY-MM-DD works best)
- Check numbers are plain numbers (no text, no symbols)

### Some rows imported, some didn't
- Check the alert message for error count
- Missing required fields (`request` or `requesterName`) will skip that row
- Invalid data types (text in number fields) will skip that row

### Column order doesn't matter
- Columns can be in any order
- You can include extra columns (they'll be ignored)
- You can omit optional columns

---

## Advanced: Bulk Data Preparation

### If you have existing data in another system:

1. **Export from your system** (usually CSV or Excel)
2. **Open in Excel**
3. **Add/rename columns** to match Seiritsu format
4. **Map your fields:**
   - Your "Title" → `request`
   - Your "Owner" → `globalTechLead`
   - Your "Cost" → `estimatedCapitalCost`
   - etc.
5. **Save as .xlsx**
6. **Import into Seiritsu**

---

## Field Mapping Guide

**If your existing system has different field names:**

| Your System | Seiritsu Column |
|-------------|-----------------|
| Title / Name / Project | `request` |
| Details / Summary / Problem | `description` |
| Value / Benefit / Revenue | `ballparkValue` |
| Submitter / Creator / Author | `requesterName` |
| Type / Kind / Category | `requestCategory` |
| Region / Territory / Area | `market` |
| Location / Geography / Countries | `countries` |
| Business Owner / PM | `globalBusinessLead` |
| Tech Owner / Dev Lead / Architect | `globalTechLead` |
| State / Phase / Stage | `status` |
| Notes / Remarks / Comments | `globalComments` |
| Success Owner / Delivery Owner | `marketSuccessOwner` |
| Domain / Portfolio / Product | `productArea` |
| Capability / Feature ID | `capabilityId` |
| Budget Source / Funding | `fundingSource` |
| Initiative / Program / Theme | `linkedMustLand` |
| CAPEX / Capital | `estimatedCapitalCost` |
| OPEX / Operating / Running Cost | `estimatedOperatingCost` |
| Cost Breakdown / Details | `costEstimationDetails` |
| Planned Start / Start Date | `expectedStartDate` |
| Planned End / Target Date | `expectedEndDate` |
| Started / Commenced | `actualStartDate` |
| Finished / Delivered / Completed | `actualEndDate` |

---

## Status Values

Use one of these exact values for the `status` column:

- **Submitted** (default for new requests)
- **Under Review**
- **Approved**
- **Committed**
- **In Progress**
- **Completed**
- **On Hold**
- **Rejected**

If you use different status values, they'll still import but won't appear correctly in Kanban view.

---

## Market Values

Recommended values for `market` column:

- **Global**
- **EMEA**
- **APAC**
- **North America**
- **Latin America**

You can use custom market names, but these are pre-configured in the tool.

---

## Request Category Values

Recommended values for `requestCategory` column:

- **New Feature**
- **Enhancement**
- **Bug Fix**
- **Technical Debt**
- **Integration**

You can use custom categories as well.

---

## Funding Source Values

Use one of these for `fundingSource` column:

- **Global**
- **Market**
- **Mixed**
- Leave blank for "TBD"

---

## Tips for Large Imports

**Importing 100+ rows?**

1. **Test with 5 rows first** - Make sure format works
2. **Check required fields** - Ensure all rows have `request` and `requesterName`
3. **Use consistent formats** - Especially for dates and numbers
4. **Remove empty rows** - Excel sometimes has hidden blank rows
5. **One sheet only** - POC reads first sheet only

**Performance:**
- 100 rows: ~5 seconds
- 500 rows: ~20 seconds
- 1000 rows: ~40 seconds

---

## Example Excel Structure

```
Row 1 (Headers):
request | description | ballparkValue | requesterName | market | status

Row 2 (Data):
AR Try-On | Implement AR feature | 2500000 | Sarah Chen | APAC | In Progress

Row 3 (Data):
Sustainability Dashboard | Consumer dashboard | 1800000 | Lars Schmidt | EMEA | Approved

Row 4 (Data):
AI Size Recommendation | ML size model | 3200000 | Maria Garcia | Global | Committed

etc.
```

---

## Need Help?

**Common Issues:**

1. **Import button doesn't work** - Make sure file is .xlsx or .xls (not .csv)
2. **All rows skipped** - Check column names match exactly
3. **Numbers importing as text** - Remove any currency symbols or text
4. **Dates not recognized** - Use YYYY-MM-DD format

**Pro Tip:** Export sample data first, use it as your template!

---

**Ready to import? Open Seiritsu-Working-POC.html → Data Management → Import Excel!**