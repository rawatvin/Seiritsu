# Seiritsu - A Smart Portfolio & Roadmap Tool

*Portfolio Management Solution for Adidas*

---

## Document Overview

**THIS IS THE STANDARD (FULL-FEATURED) PLAN: $84k-134k Year 1**

For the **minimum-cost option ($25k-50k)**, see: `Minimum-Cost-Plan.md`

---

## Executive Summary

**Seiritsu** is a comprehensive portfolio management tool designed for Adidas to manage requirements from market/global teams through feasibility checks, funding decisions, and roadmap planning. The tool provides personalized dashboards, SLA tracking with automatic escalation, and seamless integration with existing Microsoft 365 and JIRA ecosystems.

**Key Capabilities:**
- Real-time collaborative database
- Flexible personalized dashboards per user
- Automated SLA monitoring and escalation
- Stage-based lifecycle management
- JIRA integration for development tracking
- Power BI advanced analytics
- Microsoft Copilot integration
- **Native mobile apps (iOS & Android) - included at $0!**

**Important Note:** This plan describes the **full-featured "Standard" implementation**. Mobile access (both web browser and native apps) is included in the platform at no additional cost. For a **budget-conscious approach**, see the Lean plan in `Minimum-Cost-Plan.md`.

---

## Implementation Options

### Two Approaches Available:

| | **LEAN** | **STANDARD** (This Doc) |
|---|---|---|
| **Year 1 Cost** | $25k-50k | $84k-134k |
| **Timeline** | 12 weeks | 12 weeks |
| **Mobile Access** | Web browser | Native apps + Web |
| **Best For** | Budget-conscious, prove value | Want all features Day 1 |

**Both options include mobile access at $0 additional cost!**

See `COST-COMPARISON.md` for quick comparison or `Minimum-Cost-Plan.md` for full Lean details.

---

## Technology Stack Recommendation

### ✅ **Microsoft Power Platform** (Recommended Solution)

Given organizational context:
- ✓ Microsoft 365 already licensed
- ✓ 500 user base
- ✓ Advanced reporting requirements (Power BI)
- ✓ JIRA integration needed
- ✓ Copilot agent integration
- ✓ Internal security requirements
- ✓ **Mobile apps (iOS/Android) included at $0**

---

## System Architecture

### Core Components:

**1. SharePoint Lists/Dataverse** (Database layer)
- Real-time updates ✓
- Row-level security (view/edit permissions)
- Already licensed with M365
- **Decision point:** SharePoint Lists (simpler, <5k items) OR Dataverse (enterprise-grade, 500 users)

**2. Power Apps** (Front-end interface)
- Canvas app or Model-driven app
- Personalized dashboards per user
- **Multi-platform access:**
  - Desktop web browser
  - Microsoft Teams (desktop & mobile)
  - **Power Apps Mobile (iOS/Android native apps)**
  - Mobile web browser (responsive)

**3. Power Automate** (Workflow engine)
- SLA monitoring (scheduled checks)
- Escalation workflows (breach → notify lead → reassign)
- JIRA synchronization
- Email/Teams notifications
- Copilot triggers

**4. Power BI** (Reporting & Analytics)
- Embedded in Power App or standalone
- Lead time tracking, SLA compliance reports
- Executive dashboards
- Real-time data refresh

**5. Microsoft Copilot for M365** (AI integration)
- Query portfolio via Teams
- Summarize requirements via Outlook
- Built-in with M365 Copilot licenses

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACES                                 │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ Desktop Web  │ Teams        │ Mobile Apps  │ Outlook      │ Power BI    │
│ (Browser)    │ (Desktop +   │ (iOS/Android)│ (Approvals)  │ (Analytics) │
│              │  Mobile)     │ Power Apps   │              │             │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┴──────┬──────┘
       │              │              │              │              │
       └──────────────┴──────────────┴──────────────┴──────────────┘
                                     │
                       ┌─────────────┴─────────────┐
                       │   DATAVERSE / SHAREPOINT  │ ← Real-time DB
                       │   (with security roles)   │
                       └─────────────┬─────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
       ┌──────▼──────┐      ┌────────▼────────┐     ┌──────▼──────┐
       │ Power       │      │ JIRA Connector  │     │ Copilot     │
       │ Automate    │      │ (via API/Power  │     │ Agent       │
       │ (SLA/Alerts)│      │  Automate)      │     │ (Studio)    │
       └─────────────┘      └─────────────────┘     └─────────────┘
```

---

## Data Model

### Main Tables (SharePoint Lists or Dataverse):

#### **1. Portfolio Requests**
Primary table for managing all incoming requests

| Field Name | Type | Description |
|------------|------|-------------|
| ID | Auto-number | Unique identifier (REQ-0001) |
| Title | Single line text | Request title |
| Description | Rich text | Detailed description |
| Requestor | Person | Links to Azure AD |
| Market/Team | Choice | Global, EMEA, APAC, NA, etc. |
| Stage | Choice | Intake → Feasibility → Funding → Approved → Roadmap → Delivered |
| Priority | Choice | Critical, High, Medium, Low |
| Owner | Person | Current assignee |
| Watchers | Multi-person | Users following this request |
| Created Date | Date/Time | Auto-populated |
| Target Date | Date | Expected completion |
| SLA Due Date | Calculated | Based on stage + creation date |
| SLA Status | Calculated | Green/Amber/Red |
| Days Overdue | Calculated | Negative if overdue |
| Lead | Person | Owner's manager (auto-populated) |
| Feasibility Status | Choice | Pending, In Progress, Complete, Blocked |
| Funding Amount | Currency | Budget requested |
| Funding Approved | Yes/No | Approval status |
| Roadmap Quarter | Choice | Q1-2026, Q2-2026, Q3-2026, Q4-2026... |
| JIRA Key | Text | Linked JIRA issue (e.g., PROJ-1234) |
| Attachments | Attachment | Supporting documents |
| Business Case | Rich text | Justification and expected value |
| Risk Assessment | Choice | Low, Medium, High |
| Dependencies | Lookup | Links to other requests |
| Comments Count | Calculated | Number of activity log entries |

#### **2. Roadmap Items**
Linked to approved requests for roadmap visualization

| Field Name | Type | Description |
|------------|------|-------------|
| ID | Auto-number | Unique identifier |
| Request ID | Lookup | Links to Portfolio Requests |
| Quarter | Choice | Target quarter |
| Status | Choice | Planning, In Progress, Complete, On Hold |
| Start Date | Date | Planned start |
| End Date | Date | Planned completion |
| Milestones | Multi-line text | Key milestones |
| Dependencies | Lookup | Dependent roadmap items |
| Progress % | Number | 0-100 |
| Team Assigned | Choice | Development team |

#### **3. Comments/Activity Log**
Audit trail of all actions

| Field Name | Type | Description |
|------------|------|-------------|
| ID | Auto-number | Unique identifier |
| Request ID | Lookup | Links to Portfolio Requests |
| User | Person | Who made the change |
| Timestamp | Date/Time | When |
| Action Type | Choice | Comment, Status Change, Assignment, etc. |
| Comment | Multi-line text | User comment |
| Old Value | Text | Previous value (for changes) |
| New Value | Text | New value (for changes) |

#### **4. SLA Configuration**
Defines SLA rules per stage

| Field Name | Type | Description |
|------------|------|-------------|
| Stage Name | Text | Intake, Feasibility, etc. |
| SLA Hours | Number | Hours allowed in this stage |
| Warning Threshold % | Number | When to send warning (e.g., 80%) |
| Escalation Rules | Multi-line text | JSON or structured escalation logic |
| Escalate To | Choice | Lead, Manager, Portfolio Manager |

---

## Key Features Implementation

### ✅ **Real-time Updates**
- **SharePoint/Dataverse:** Changes sync instantly across all users
- **Power Apps:** Set `OnVisible` to refresh data or use `Refresh()` function
- **Alternative:** Use Dataverse real-time notifications for instant push updates

### ✅ **Personalized Dashboards**

Each user sees filtered views in Power App:

**Dashboard Sections:**
1. **"My Assignments"** 
   - Filter: `Filter(Requests, Owner.Email = User().Email)`
   - Shows: All items assigned to current user
   
2. **"Watching"**
   - Filter: `Filter(Requests, User().Email in Watchers.Email)`
   - Shows: Items user is watching/interested in
   
3. **"My Team"**
   - Filter: `Filter(Requests, Owner.Department = User().Department)`
   - Shows: All team items
   
4. **"Breached SLAs"**
   - Filter: `Filter(Requests, SLA_Status = "Red" && Owner.Email = User().Email)`
   - Shows: Overdue items requiring immediate attention

5. **"Recent Activity"**
   - Last 7 days of changes to watched/assigned items

**User Preferences Table:**
Store individual user dashboard configurations, favorite views, notification preferences

### ✅ **SLA Tracking & Escalation**

#### **Power Automate Flow: SLA Monitor**

**Trigger:** Recurrence (every 1 hour)

**Steps:**
1. **Get items** where:
   - `SLA Due Date < Now()`
   - `Stage ≠ "Delivered" or "Closed"`
   - `SLA Status ≠ "Breached"`

2. **For each overdue item:**
   - Update `SLA Status` to "Breached"
   - Calculate `Days Overdue`
   - Send Teams adaptive card to Owner with action buttons
   - Send email to Lead (manager) with escalation notice
   - Post to Teams channel: `#sla-escalations`
   - Create activity log entry
   - **Optional:** Auto-reassign to Lead after 24hrs

3. **Warning notifications** (at 80% of SLA):
   - Get items where: `(Now() - Created) / SLA_Hours > 0.8`
   - Send warning notification to Owner
   - Add to "At Risk" dashboard section

#### **SLA Calculation Formulas**

**In SharePoint/Dataverse calculated columns:**

```javascript
// SLA Due Date
= DateAdd(Created, SLA_Hours_Lookup, Hours)

// Days Overdue
= DateDiff(SLA_DueDate, Now(), Days)

// SLA Status
= If(
    DaysOverdue > 1, "Red",
    DaysOverdue > 0, "Amber",
    DaysOverdue > -2, "Yellow",
    "Green"
  )

// SLA Progress %
= (Now() - Created) / (SLA_DueDate - Created) * 100
```

**In Power Apps for dynamic display:**

```javascript
// Color coding
If(ThisItem.SLA_Status = "Red", RGBA(220, 53, 69, 1),
   ThisItem.SLA_Status = "Amber", RGBA(255, 193, 7, 1),
   ThisItem.SLA_Status = "Yellow", RGBA(255, 235, 59, 1),
   RGBA(40, 167, 69, 1))
```

### ✅ **Intake Form**

**Implementation:**
- Power Apps form embedded in Teams tab or SharePoint page
- Publicly accessible form for requestors (minimal permissions)
- Validates required fields before submission
- Auto-assigns to triage queue upon submission

**Form Fields:**
1. Title* (required)
2. Description* (required)
3. Business Case* (required)
4. Expected Value/Benefits*
5. Requestor (auto-populated from User())
6. Market/Team* (dropdown)
7. Priority (dropdown, default: Medium)
8. Target Date (optional)
9. Attachments (optional)
10. Dependencies (optional, lookup to existing requests)

**Submission Flow:**
1. Form submitted → Creates new record in Portfolio Requests
2. Sets Stage = "Intake"
3. Triggers Power Automate flow:
   - Send confirmation email to requestor
   - Notify triage team in Teams channel
   - Assign to default triage owner
   - Calculate initial SLA due date

### ✅ **Stage Management**

**Stages:**
1. **Intake** → New submissions, awaiting triage
2. **Feasibility** → Technical/business feasibility assessment
3. **Funding** → Budget approval process
4. **Approved** → Approved, awaiting roadmap planning
5. **Roadmap** → On roadmap, planning/in development
6. **Delivered** → Completed and closed

**Power App Kanban Board:**
- Gallery grouped by Stage
- Drag-drop cards to change stages
- OnSelect: Update Stage field, trigger workflow

**Stage Transition Workflows:**

| From → To | Trigger Action |
|-----------|----------------|
| Intake → Feasibility | Notify feasibility team, assign feasibility lead |
| Feasibility → Funding | Notify finance team, attach feasibility report |
| Funding → Approved | Notify portfolio manager, calculate ROI |
| Approved → Roadmap | Create roadmap item, assign quarter, create JIRA ticket |
| Roadmap → Delivered | Close JIRA ticket, notify requestor, archive |

**Required Fields per Stage:**
- Feasibility: Feasibility Status, Risk Assessment
- Funding: Funding Amount, Business Case
- Approved: Roadmap Quarter, Target Date
- Roadmap: JIRA Key, Team Assigned

### ✅ **Notifications**

**Power Automate Notification Flows:**

| Trigger Event | Recipients | Channel | Content |
|--------------|-----------|---------|---------|
| Assigned to you | Owner | Teams + Email | "You've been assigned REQ-1234" + action link |
| Comment added | Watchers + Owner | Teams | "@User commented on REQ-1234" |
| Stage changed | Requestor + Owner | Email | "REQ-1234 moved to [Stage]" |
| Approaching SLA (80%) | Owner | Teams | "⚠️ REQ-1234 due in X hours" |
| SLA breached | Owner + Lead | Teams + Email | "🚨 REQ-1234 is overdue by X days" + escalation |
| Funding approved | Requestor + Watchers | Email | "🎉 REQ-1234 approved for roadmap" |
| Added as watcher | Watcher | Teams | "You're now watching REQ-1234" |

**Adaptive Card Example (Teams):**
```json
{
  "type": "AdaptiveCard",
  "body": [
    {
      "type": "TextBlock",
      "text": "SLA Breached: REQ-1234",
      "weight": "Bolder",
      "size": "Large",
      "color": "Attention"
    },
    {
      "type": "TextBlock",
      "text": "Request: New Product Feature X"
    },
    {
      "type": "TextBlock",
      "text": "Overdue: 2 days"
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "View Request",
      "url": "[Deep link to Power App]"
    },
    {
      "type": "Action.Submit",
      "title": "Reassign",
      "data": { "action": "reassign" }
    }
  ]
}
```

### ✅ **JIRA Integration**

**Power Automate Connector:** JIRA Cloud/Server

**Integration Scenarios:**

1. **Create JIRA Issue from Roadmap Item**
   - Trigger: Stage changed to "Roadmap"
   - Action: Create JIRA issue in specified project
   - Map fields:
     - Summary ← Title
     - Description ← Description + Business Case
     - Priority ← Priority
     - Labels ← Market/Team
   - Store JIRA Key back to Seiritsu

2. **Sync JIRA Status to Seiritsu**
   - Trigger: JIRA issue status changed (webhook or scheduled poll)
   - Action: Update Progress % in Roadmap Items
   - Map statuses:
     - To Do → 0%
     - In Progress → 50%
     - Done → 100%

3. **Bi-directional Comment Sync** (optional)
   - JIRA comment → Activity Log in Seiritsu
   - Seiritsu comment → JIRA comment

**Configuration:**
- Store JIRA project mapping in configuration table
- Different JIRA projects per team/market
- Custom field mapping as needed

### ✅ **Power BI Reports**

**Embedded Dashboards:**

#### **1. Executive Overview**
- Total requests by stage (funnel chart)
- SLA compliance rate (gauge: target >95%)
- Average lead time per stage (bar chart)
- Quarterly throughput trend (line chart)
- Top requestors/markets (table)

#### **2. Lead Time Analysis**
- Average time in each stage (waterfall chart)
- Bottleneck identification (stage with longest duration)
- Cycle time distribution (histogram)
- Aging items (requests >30 days in one stage)

#### **3. SLA Performance**
- On-time vs breached (pie chart)
- Breach reasons breakdown
- Team/owner compliance rate (leaderboard)
- Trend over time (line chart with target line)

#### **4. Funding Pipeline**
- Funding requested vs approved (bar chart)
- Approval rate by market (matrix)
- Budget utilization by quarter
- ROI projection

#### **5. Roadmap Timeline**
- Gantt chart of roadmap items
- Capacity planning (items per team per quarter)
- Dependency visualization (network diagram)
- Milestone tracking

#### **6. Personal KPI Dashboard**
- Your assigned items (list)
- Your completion rate (gauge)
- Your average lead time vs team average
- Your SLA compliance rate
- Items needing action (table)

**Data Refresh:**
- Real-time: Direct query to Dataverse/SharePoint
- Or scheduled refresh: Every 15 minutes

**Embedding in Power App:**
```javascript
// Add Power BI component
PowerBITile.Workspace = "YourWorkspaceID"
PowerBITile.Report = "YourReportID"
PowerBITile.Page = "ExecutiveOverview"

// Filter by current user
PowerBITile.Filter = "Owner/Email eq '" & User().Email & "'"
```

### ✅ **Microsoft Copilot Agent** (Phase 4)

**Build in Copilot Studio:**

**Sample Copilot Actions:**

1. **Query Requests**
   - User: "Show my overdue requests"
   - Copilot: Queries Dataverse, returns list with deep links

2. **Status Check**
   - User: "What's the status of REQ-1234?"
   - Copilot: Fetches request details, summarizes current stage, owner, SLA status

3. **Summaries**
   - User: "Summarize this week's escalations"
   - Copilot: Aggregates breached SLAs, provides summary report

4. **Actions**
   - User: "Add a comment to REQ-1234: 'Meeting with stakeholders scheduled'"
   - Copilot: Creates activity log entry, notifies watchers

5. **Analytics**
   - User: "How many requests are in feasibility stage?"
   - Copilot: Count query, provides breakdown by priority

**Integration Points:**
- Teams chat/channels
- Outlook (summarize requests in email)
- Power App (embedded chat widget)

---

## Security Model

### Role-Based Access Control (RBAC)

#### **User Roles:**

| Role | Permissions | Count (est.) |
|------|-------------|--------------|
| **Viewer** | Read all requests | ~450 users |
| **Contributor** | Edit assigned requests, add comments | ~40 users |
| **Owner/Lead** | Edit team requests, reassign, escalate | ~20 users |
| **Portfolio Manager** | Full access, configure SLAs, reports | ~5 users |
| **Admin** | System configuration, user management | ~2 users |

#### **Implementation:**

**SharePoint Lists:**
- Permission groups per role
- Item-level permissions for sensitive requests
- Break inheritance for confidential funding data

**Dataverse:**
- Security roles (Viewer, Contributor, Owner, Admin)
- Business units per market/team
- Field-level security for financial data

**Power App:**
```javascript
// Show edit button only for authorized users
EditButton.Visible = 
    User().Email = ThisItem.Owner.Email || 
    User().Email in AdminsList ||
    ThisItem.Stage = "Intake" && User().Email = ThisItem.Requestor.Email
```

### Row-Level Security (RLS)

**Rules:**
1. **Requestors:** Can edit their own submissions until moved past "Intake"
2. **Owners:** Can edit all assigned items
3. **Leads:** Can view/edit their team's items (based on org hierarchy from Azure AD)
4. **Watchers:** Read-only access + notifications
5. **Admins:** Full access to all records

**Azure AD Integration:**
- Auto-populate user's manager as Lead
- Department/market from user profile
- Security group membership for role assignment

### Data Sensitivity

**Confidential Fields:**
- Funding Amount (visible only to Owner, Lead, Finance team)
- Business Case (visible to all, editable by Requestor/Owner)
- Risk Assessment (visible to Lead, Portfolio Manager)

**Audit Trail:**
- All changes logged in Activity Log
- Who, what, when for compliance
- Retention: 7 years

---

## Cost Analysis (500 Users)

**IMPORTANT:** This section describes the **STANDARD (full-featured) approach**. For a more budget-conscious option, see `Minimum-Cost-Plan.md` ($25k-50k vs $84k-134k).

### Licensing Breakdown

| Component | License Required | Cost per User/Month | Total/Month | Notes |
|-----------|------------------|---------------------|-------------|-------|
| **SharePoint Online** | Microsoft 365 E3/E5 | Included | $0 | Already licensed |
| **Power Apps (basic)** | Microsoft 365 E3/E5 | Included | $0 | Included in M365 |
| **Power Apps Mobile** | Power Apps license | **Included** | **$0** | **iOS/Android apps FREE** |
| **Mobile web access** | Power Apps license | **Included** | **$0** | **Responsive design FREE** |
| **Power Apps Premium** | Per-user or per-app | $10-20 | $0-10,000 | Only if heavy usage or Dataverse |
| **Power Automate** | Microsoft 365 E3/E5 | Included | $0 | 2000 flows included |
| **Premium Connectors** | Power Automate Premium | ~$15 | $0-500 | Only JIRA connector needs Premium |
| **Power BI Pro** | Power BI Pro license | $10 | $200 | For ~20 report authors |
| **Power BI Premium** | Capacity-based | ~$5000 | $0-5000 | Alternative for 500 viewers |
| **Dataverse** | Per-user | $40 | $0-20,000 | Only if SharePoint Lists insufficient |
| **Microsoft Copilot** | M365 Copilot | $30 | $0-15,000 | Optional, Phase 4 |

**Mobile Note:** All mobile access (web browser + native iOS/Android apps) is included at $0 additional cost. The cost differences between Lean ($25k-50k) and Standard ($84k-134k) approaches are due to implementation scope, advanced features, and premium services - NOT mobile access.

### Cost Approach Options

#### **OPTION 1: LEAN (Budget-Conscious) - See Minimum-Cost-Plan.md**

**Monthly cost: $0-200**
- SharePoint Lists (not Dataverse)
- Basic Power Apps (not Premium)
- Standard Power Automate (not Premium connectors)
- Power BI Free or 2-3 Pro licenses
- **Mobile web browser access** (responsive design)
- Native mobile apps optional (enable later if needed, $0)

**Annual Run Cost:** $0-2,400  
**Build Cost:** $25k-50k  
**Year 1 Total:** $25k-52k

---

#### **OPTION 2: STANDARD (Full-Featured) - This Document**

**Phase 1-2: MVP (Months 1-2)**
- Use SharePoint Lists (free)
- Included Power Platform features
- Basic Power BI with Pro licenses for authors
- **Mobile access included** (web + native apps ready)
- **Monthly cost: ~$200-500**

**Phase 3: Scale (Months 3-6)**
- Add JIRA Premium connector if needed
- Power BI embedded for 500 users OR
- Keep Power BI Pro for report authors only
- **Native mobile apps enabled** (if desired, $0)
- **Monthly cost: ~$1,000-2,000**

**Phase 4: Enterprise (Months 6+)**
- Evaluate Dataverse migration if performance issues
- Copilot agent for select power users (50-100 licenses)
- **Monthly cost: ~$3,000-5,000**

**Annual Run Cost:** $12k-48k  
**Build Cost:** $50k-100k + $10k training  
**Year 1 Total:** $84k-134k

### Total Cost of Ownership (TCO) - Year 1

#### STANDARD (Full-Featured) Approach - This Document

| Item | Cost |
|------|------|
| Licensing (average) | $24,000 |
| Implementation (consulting/internal) | $50,000-100,000 |
| Training | $10,000 |
| **Mobile apps (iOS/Android)** | **$0 (included!)** |
| **Mobile web access** | **$0 (included!)** |
| **Offline mode** | **$0 (included!)** |
| **Push notifications** | **$0 (included!)** |
| **Total Year 1 (Standard)** | **$84,000-134,000** |
| **Ongoing (Year 2+)** | **$24,000-60,000/year** |

#### LEAN (Budget-Conscious) Alternative

| Item | Cost |
|------|------|
| Licensing | $0-2,400 |
| Implementation (simplified) | $25,000-50,000 |
| Training (self-service) | Included |
| **Mobile web access** | **$0 (included!)** |
| **Total Year 1 (Lean)** | **$25,000-52,400** |
| **Ongoing (Year 2+)** | **$0-2,400/year** |

**💰 Savings with Lean vs Standard:** $32k-82k (Year 1)

---

**Comparison to Alternatives:**
- **Lean (Power Platform):** $25k-52k Year 1 ⭐ RECOMMENDED for budget
- **Standard (Power Platform):** $84k-134k Year 1 (this document)
- Custom Build (web only): $250k-500k + $100k/year maintenance
- Custom Build + Native Mobile Apps: $450k-800k + $150k/year maintenance
- Airtable: ~$120k/year (500 users @ $20/user, basic mobile)
- Retool/Budibase: ~$60k/year + infrastructure + dev time

**💰 Mobile Savings with Power Platform (vs custom mobile):** ~$250k-350k (Year 1)

---

## Mobile Access Strategy

**🔔 IMPORTANT CLARIFICATION:**

Mobile access does NOT increase cost or timeline! Here's what's available:

| Mobile Option | Cost | Timeline Impact | Available In |
|---------------|------|----------------|--------------|
| **Mobile web browser** | $0 | None | Lean & Standard |
| **Native iOS app** | $0 | None | Lean & Standard |
| **Native Android app** | $0 | None | Lean & Standard |
| **Offline mode** | $0 | None | Lean & Standard |
| **Push notifications** | $0 | None | Lean & Standard |

The difference between **Lean ($25k-50k)** and **Standard ($84k-134k)** is NOT mobile - it's:
- Implementation scope (simplified vs comprehensive)
- JIRA auto-sync (manual vs automatic)
- Advanced analytics (basic vs full Power BI)
- Training (self-service vs full training program)
- Premium features (deferred vs included)

**Both approaches include full mobile access at $0!**

---

### 📱 Native Mobile Apps - Included by Default!

**Power Apps Mobile** provides full native iOS and Android apps with zero additional development. Users get the same Power App on all devices from a single codebase.

**⏱️ Timeline Impact:** None - mobile works from Day 1 (responsive design)  
**💰 Cost Impact:** $0 - fully included in Power Platform licensing  
**🚀 Deployment:** Same 12-week timeline, mobile tested throughout all phases

### Mobile Deployment Options

#### **Option 1: Power Apps Mobile (Recommended)**

**What it is:**
- Free native app from Apple App Store / Google Play Store
- One app for all Power Apps in the organization
- Install once, access all authorized apps

**Features:**
- ✅ **Offline mode** - Work without internet, auto-sync when connected
- ✅ **Push notifications** - SLA alerts, assignment notifications
- ✅ **Device features** - Camera (upload photos), GPS, biometric auth
- ✅ **Native performance** - Smooth, app-like experience
- ✅ **Background sync** - Data updates automatically
- ✅ **Home screen icon** - Looks like a native app

**User Experience:**
1. Download "Power Apps" from app store (one-time)
2. Sign in with Adidas credentials (Azure AD)
3. See Seiritsu in app list
4. Pin to favorites for quick access
5. Receive push notifications for SLA breaches

**Deployment:**
- Distribute via **Microsoft Intune** (MDM)
- Pre-install on company phones
- Auto-configure with company credentials

#### **Option 2: Microsoft Teams Mobile**

**What it is:**
- Embed Seiritsu as a Teams tab
- Access via Teams mobile app (already installed)

**Advantages:**
- No separate app to install
- Integrated with Teams chat/notifications
- Familiar Teams interface

**Best for:**
- Quick lookups
- Notifications via Teams
- Users already living in Teams mobile

#### **Option 3: Mobile Web Browser**

**What it is:**
- Responsive web version
- Works in any mobile browser (Safari, Chrome)
- Add to home screen for app-like experience

**Best for:**
- External contractors (no company phone)
- Quick access without app install
- BYOD scenarios

### Mobile-Specific Features

**Optimized for Mobile Use Cases:**

1. **Quick Request Submission**
   - Simplified mobile form
   - Camera integration for attachments
   - Voice-to-text for descriptions

2. **SLA Alerts on the Go**
   - Push notifications for breaches
   - One-tap to view request
   - Quick action buttons (approve, comment, reassign)

3. **Dashboard Widgets**
   - "My Assignments" (compact view)
   - "Breached SLAs" (priority list)
   - "Recent Activity" (last 5 items)

4. **Offline Capability**
   - View assigned requests offline
   - Draft comments/updates offline
   - Auto-sync when connection restored

5. **Barcode/QR Scanning**
   - Scan QR code on printed request forms
   - Jump directly to request detail
   - Link physical materials to digital requests

### Mobile UI/UX Considerations

**Design Principles:**
- Larger touch targets (min 44x44 px)
- Simplified navigation (bottom tab bar)
- Swipe gestures (swipe to complete, archive)
- Portrait-optimized layouts
- Reduced data load (pagination)

**Screen Optimization:**
```
Mobile Dashboard Layout:
┌─────────────────────────┐
│  📊 Dashboard           │
├─────────────────────────┤
│  🚨 3 SLA Breaches     │  ← Alert banner
├─────────────────────────┤
│  📋 My Work (5)        │  ← Collapsible sections
│  👁️ Watching (8)       │
│  ⚠️ At Risk (2)        │
├─────────────────────────┤
│  [Recent Activity...]  │  ← Scrollable list
│  REQ-0245 - Updated    │
│  REQ-0234 - Breached   │
│  REQ-0221 - Approved   │
└─────────────────────────┘
  🏠  📊  ➕  📈  👤      ← Bottom nav
```

### Mobile Performance

**Optimization Strategies:**
- **Delegation:** Server-side filtering (not client-side)
- **Lazy loading:** Load data as user scrolls
- **Image compression:** Reduce attachment sizes
- **Caching:** Store frequently accessed data locally
- **Progressive enhancement:** Basic features work, enhanced features when online

**Expected Performance:**
- App launch: <2 seconds
- List load: <1 second (first 20 items)
- Request detail: <500ms
- Offline mode: Instant (cached data)

### Mobile Security

**Enterprise Security Features:**
- Azure AD authentication (SSO)
- Conditional access policies (require PIN, biometric)
- App-level encryption
- Remote wipe capability (via Intune)
- Prevent screenshots (sensitive data)
- Session timeout (configurable)

### Mobile Rollout Plan

**Phase 1 (Week 3):**
- Basic mobile layout optimization
- Test on iOS and Android devices
- 10 pilot users test mobile app

**Phase 2 (Week 6):**
- Push notifications configured
- Teams mobile tab enabled
- 50 users test mobile access

**Phase 3 (Week 9):**
- Offline mode enabled
- Mobile-specific shortcuts
- Camera/attachment features

**Phase 4 (Week 12):**
- Full mobile optimization
- Intune deployment package
- 500 users with mobile access

### Mobile Training

**User Training Materials:**
- 2-minute video: "Installing Power Apps Mobile"
- Quick reference card: "Using Seiritsu on Your Phone"
- In-app tour (first launch)
- Tips & tricks: "Work offline while traveling"

### Mobile Cost

**Additional Cost:** **$0**

All mobile capabilities are included in Power Apps licensing:
- Power Apps Mobile app (free from app stores)
- Mobile access included in per-user license
- Push notifications included
- Offline mode included
- Intune deployment (already licensed)

**No separate mobile app development needed!**

---

## Implementation Roadmap

### **Phase 1: MVP (Weeks 1-3)**

**Goal:** Basic functional system for intake and tracking

**Deliverables:**
- ✅ SharePoint Lists created (Portfolio Requests, Activity Log, SLA Config)
- ✅ Basic Power App with list/detail views
- ✅ Intake form (embedded in Teams)
- ✅ Simple SLA calculation (calculated columns)
- ✅ Email notifications for assignments

**Tasks:**
1. Create SharePoint site and lists
2. Configure calculated columns for SLA
3. Build Power App canvas:
   - Home screen with dashboard tiles
   - Request list (gallery)
   - Request detail form
   - Intake form
4. Set up basic email notifications (Power Automate)
5. Configure security groups
6. User acceptance testing with 10 pilot users

**Success Criteria:**
- 10 pilot users can submit and view requests
- SLA status displays correctly
- Email notifications working

---

### **Phase 2: Workflows & Automation (Weeks 4-6)**

**Goal:** Automated SLA monitoring and stage management

**Deliverables:**
- ✅ Power Automate SLA monitoring flow
- ✅ Escalation workflows
- ✅ Stage transition automation
- ✅ Teams integration (notifications, app embed)
- ✅ Activity logging

**Tasks:**
1. Build SLA monitor flow (hourly recurrence)
2. Build escalation flow (breached SLAs)
3. Create stage transition flows (6 workflows)
4. Implement Teams notifications (adaptive cards)
5. Embed Power App as Teams tab
6. Add activity log automation
7. Expand to 50 users

**Success Criteria:**
- SLA breaches trigger automatic escalations
- Stage changes notify correct users
- Teams integration working smoothly

---

### **Phase 3: Advanced Features (Weeks 7-9)**

**Goal:** Personalized dashboards, reporting, JIRA integration

**Deliverables:**
- ✅ Personalized dashboard views per user
- ✅ Kanban board view for stage management
- ✅ Power BI reports (6 core dashboards)
- ✅ JIRA connector and sync flows
- ✅ Roadmap table and views

**Tasks:**
1. Create user preference system
2. Build personalized dashboard screens:
   - My Assignments
   - Watching
   - My Team
   - Breached SLAs
3. Implement Kanban board (drag-drop)
4. Create Roadmap Items table
5. Build Power BI reports:
   - Executive Overview
   - Lead Time Analysis
   - SLA Performance
   - Funding Pipeline
   - Roadmap Timeline
   - Personal KPIs
6. Set up JIRA connector
7. Create JIRA sync flows (create issue, update status)
8. Embed Power BI in Power App
9. Full user rollout (500 users)

**Success Criteria:**
- Each user sees personalized dashboards
- Power BI reports show accurate, real-time data
- JIRA issues created automatically from roadmap items
- 500 users onboarded

---

### **Phase 4: Polish & Enterprise Features (Weeks 10-12)**

**Goal:** Production-ready, optimized, enterprise-grade with full mobile deployment

**Deliverables:**
- ✅ **Mobile-optimized app (iOS/Android)**
- ✅ **Offline mode enabled**
- ✅ **Push notifications configured**
- ✅ **Intune deployment package ready**
- ✅ Microsoft Copilot agent (basic)
- ✅ Performance tuning
- ✅ User training and documentation (desktop + mobile)
- ✅ Admin console

**Tasks:**
1. **Mobile optimization:**
   - Responsive layouts for all screen sizes
   - Touch-friendly controls (44px minimum)
   - Bottom navigation for mobile
   - Offline mode configuration
   - Push notification setup
   - Test on iPhone (iOS 16+) and Android (12+)
   - Camera/barcode integration for attachments
   
2. **Mobile deployment:**
   - Create Intune deployment package
   - Configure app protection policies
   - Setup conditional access (biometric/PIN)
   - Test remote wipe capability
   - Prepare installation guide
   
3. Build Copilot agent in Copilot Studio:
   - Basic queries (my requests, status check)
   - Summary generation
   - Works in Teams mobile
   
4. Performance optimization:
   - Dataverse migration (if needed)
   - Delegation tuning for mobile
   - Caching strategies
   - Image compression for mobile uploads
   
5. Create admin console:
   - User role management
   - SLA configuration UI
   - System health dashboard
   - Mobile usage analytics
   
6. Documentation:
   - User guide (desktop + mobile versions)
   - Mobile quick start guide
   - Admin guide
   - API documentation (for future integrations)
   - Video: "Using Seiritsu on Your Phone" (2 min)
   
7. Training:
   - End-user training (500 users, desktop + mobile)
   - Mobile-specific training session
   - Admin training (5 users)
   - Video tutorials (desktop, mobile, Teams)
   
8. Handover to support team

**Success Criteria:**
- App works seamlessly on iOS and Android devices
- Offline mode tested and functional
- Push notifications deliver within 30 seconds
- 500 users successfully install mobile app
- Copilot agent handles basic queries
- All documentation complete
- Support team trained
- User satisfaction >80% (desktop + mobile)

---

### **Post-Launch: Continuous Improvement**

**Ongoing activities:**
- Monitor usage analytics
- Gather user feedback
- Monthly feature releases
- Performance monitoring
- Security audits
- JIRA integration enhancements
- Additional Copilot capabilities

---

## Advantages Over Alternatives

| Feature | Power Platform | Airtable | Custom Build | Retool |
|---------|----------------|----------|--------------|--------|
| **Real-time collaboration** | ✓ | ✓ | ✓ (custom) | ✓ |
| **M365 integration** | ✓✓✓ Native | ✗ | Manual | Partial |
| **Azure AD authentication** | ✓✓✓ Built-in | ✗ | Manual | ✓ |
| **JIRA connector** | ✓ Built-in | Via Zapier ($) | API coding | ✓ |
| **Power BI integration** | ✓✓✓ Native | ✗ | Manual | Partial |
| **Copilot integration** | ✓✓✓ Native | ✗ | Manual | ✗ |
| **Teams integration** | ✓✓✓ Native | ✗ | Manual | ✗ |
| **Outlook integration** | ✓✓✓ Native | Partial | Manual | ✗ |
| **Security (Row-level)** | ✓✓✓ Built-in | Basic | Custom | ✓ |
| **Cost (500 users)** | Low ($0-5k) | High (~$10k) | Very High | Medium (~$5k) |
| **Maintenance overhead** | Low | Low | High | Medium |
| **Time to production** | 3 months | 1 month | 6-12 months | 2-3 months |
| **Scalability** | Excellent | Good | Excellent | Good |
| **Mobile app (iOS/Android)** | ✓✓✓ Native (included) | ✓ | Custom build | ✓ |
| **Offline mode** | ✓✓✓ Built-in | ✗ | Custom | Partial |
| **Push notifications** | ✓✓✓ Built-in | ✗ | Custom | Partial |
| **No-code/Low-code** | ✓✓✓ | ✓✓✓ | ✗ | ✓✓ |
| **Enterprise support** | ✓✓✓ Microsoft | ✓ | Custom | ✓ |

**Winner: Power Platform** for Adidas use case due to:
1. Already licensed (lowest cost)
2. Native M365 ecosystem integration
3. **Native iOS/Android apps included - no separate mobile development!**
4. Enterprise-grade security and compliance
5. Fastest time to value (3 months)
6. No additional vendor management
7. Future-proof with Copilot AI integration
8. **Offline mode & push notifications built-in**

---

## Risk Assessment & Mitigation

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| SharePoint list limits (5000 items) | High | Medium | Migrate to Dataverse if approaching limit; use indexed columns |
| Performance with 500 users | Medium | Low | Load testing in Phase 2; optimize delegation; consider Premium |
| JIRA connector failures | Medium | Medium | Error handling in flows; retry logic; fallback to manual sync |
| Power App delegation issues | Low | Medium | Use delegable functions; filter server-side; limit data loads |
| Data loss during migration | High | Low | Backup strategy; staged rollout; rollback plan |

### Organizational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| User adoption resistance | High | Medium | Change management; training; pilot with champions; gather feedback |
| Insufficient Power Platform licenses | Medium | Low | Confirm licensing with IT; budget for Premium if needed |
| JIRA integration complexity | Medium | Medium | Start with one-way sync; iterate; dedicated integration dev |
| SLA definitions unclear | High | Medium | Workshop with stakeholders; document in Phase 1; iterate |
| Scope creep | Medium | High | Strict change control; defer non-MVP features to Phase 4+ |

### Mitigation Strategy

1. **Pilot Program:** 10 users in Week 3, 50 users by Week 6
2. **Regular Checkpoints:** Weekly demos, bi-weekly steering committee
3. **Fallback Plan:** Keep existing process parallel for first month
4. **Training:** Multiple sessions, video library, office hours
5. **Support:** Dedicated support channel in Teams, FAQ documentation

---

## Success Metrics (KPIs)

### System Performance
- **Uptime:** >99.5%
- **Page Load Time:** <2 seconds
- **SLA Calculation Accuracy:** 100%

### User Adoption
- **Active Users:** >450/500 (90%) within 3 months
- **Mobile App Adoption:** >70% (350+ users) within 6 months
- **Requests Submitted via Tool:** >95% (vs manual/email)
- **Mobile Submissions:** >30% of total submissions
- **User Satisfaction:** >80% (quarterly survey, desktop + mobile)

### Process Improvement
- **Average Lead Time:** Reduce by 30% (baseline vs 6 months)
- **SLA Compliance:** >90% (target: 95% by month 6)
- **Escalation Resolution Time:** <48 hours
- **Requests Completed:** Track quarterly throughput

### Business Value
- **Roadmap Visibility:** 100% of approved projects on roadmap
- **Funding Approval Rate:** Track trend (baseline)
- **Time Saved:** ~2 hours/week per portfolio manager (survey)
- **Decision Speed:** Faster feasibility-to-funding cycle

---

## Next Steps & Decision Points

### Immediate Actions (Week 0)

1. **Stakeholder Alignment**
   - [ ] Present proposal to leadership
   - [ ] Confirm budget and timeline
   - [ ] Identify executive sponsor

2. **Technical Validation**
   - [ ] Confirm Power Platform licensing (E3/E5)
   - [ ] Verify JIRA API access
   - [ ] Check Power BI Pro licenses available

3. **Team Formation**
   - [ ] Identify project manager
   - [ ] Assign Power Platform developer(s)
   - [ ] Designate business analyst
   - [ ] Select pilot users (10)

4. **Requirements Workshop**
   - [ ] Define SLA rules per stage (hours)
   - [ ] Map organizational hierarchy (for escalations)
   - [ ] Finalize intake form fields
   - [ ] Document stage transition rules
   - [ ] JIRA project mapping

### Key Decision Points

**Decision 1: SharePoint Lists vs Dataverse?**
- **When:** Week 1
- **Criteria:** Expected volume (<5k items → SharePoint, >5k → Dataverse)
- **Recommendation:** Start with SharePoint, migrate if needed

**Decision 2: Power BI Pro vs Premium?**
- **When:** Week 6 (Phase 3 start)
- **Criteria:** <25 report viewers → Pro, >25 → evaluate Premium
- **Recommendation:** Pro for authors (~20), viewers access via embedded

**Decision 3: Copilot Agent Scope?**
- **When:** Week 8
- **Criteria:** User feedback from Phase 2
- **Recommendation:** Start basic (query + status), expand based on usage

**Decision 4: JIRA Integration Depth?**
- **When:** Week 2
- **Criteria:** JIRA team availability, API access
- **Recommendation:** Start one-way (Seiritsu → JIRA), add bi-directional if needed

---

## Appendix

### A. Glossary

- **Seiritsu:** Japanese word meaning "establishment" or "formation" - fitting for portfolio and roadmap creation
- **SLA:** Service Level Agreement - time commitment for each stage
- **Dataverse:** Microsoft's cloud-based database (formerly Common Data Service)
- **Delegation:** Power Apps ability to send queries to server (vs client-side filtering)
- **Adaptive Card:** Rich Teams notification format with interactive buttons

### B. Reference Links

**Microsoft Documentation:**
- Power Apps: https://learn.microsoft.com/en-us/power-apps/
- Power Automate: https://learn.microsoft.com/en-us/power-automate/
- Power BI: https://learn.microsoft.com/en-us/power-bi/
- Dataverse: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/
- Copilot Studio: https://learn.microsoft.com/en-us/microsoft-copilot-studio/

**Community Resources:**
- Power Platform Community: https://powerusers.microsoft.com/
- Power Apps Samples: https://github.com/microsoft/PowerApps-Samples

### C. Contact & Support

**Project Team:**
- Project Sponsor: [TBD]
- Project Manager: [TBD]
- Technical Lead: [TBD]
- Business Analyst: [TBD]

**Support Channels:**
- Teams Channel: #seiritsu-support
- Email: seiritsu-help@adidas.com
- Office Hours: [TBD]

---

## Document Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-19 | Claude (Seiritsu Planning) | Initial comprehensive plan |

---

*End of Document*

**Next Action:** Review with stakeholders and proceed to Phase 1 kickoff.