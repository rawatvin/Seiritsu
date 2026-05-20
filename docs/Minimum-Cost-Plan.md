# Seiritsu - Minimum Cost Implementation Plan

**Ultra-Lean Approach for Budget-Conscious Start**

---

## Executive Summary

This plan delivers Seiritsu's core portfolio management capabilities at minimum cost while maintaining quality and scalability.

**Key Numbers:**
- **Build Cost:** $25k-50k (vs $84k-134k full-featured)
- **Run Cost:** $0-200/month (vs $1k-2k full-featured)
- **Timeline:** 12 weeks (same)
- **Mobile Access:** Mobile web browser (responsive, app-like)
- **Users Supported:** 500

**Philosophy:** Start lean, prove value, upgrade selectively based on actual needs.

---

## 💰 Cost Breakdown

### One-Time Build Cost: $25k-50k

| Phase | Activity | Cost | Duration |
|-------|----------|------|----------|
| **Phase 1** | SharePoint Lists + Basic Power App | $15k-30k | 4 weeks |
| **Phase 2** | Automation + Views | $5k-10k | 4 weeks |
| **Phase 3** | Polish + Rollout | $5k-10k | 4 weeks |
| **Total** | **Implementation** | **$25k-50k** | **12 weeks** |

### Monthly Run Cost: $0-200

| Component | Cost | Notes |
|-----------|------|-------|
| SharePoint Lists | $0 | Included in M365 E3/E5 |
| Power Apps | $0 | Included in M365 E3/E5 |
| Power Automate | $0 | Included (2000 runs/month) |
| Power BI | $0-200 | Free tier OR 2-3 Pro licenses ($10/user) |
| Mobile web access | $0 | Responsive design |
| **Total Monthly** | **$0-200** | |

**Annual Run Cost:** $0-2,400

---

## 📱 Mobile Access: Lean Approach

### Strategy: Mobile Web Browser

**What users do:**
1. Open browser on phone (Safari/Chrome)
2. Navigate to Seiritsu (bookmark or company portal)
3. Login with company credentials
4. Use app (fully responsive design)

**Optional: Add to Home Screen**
- Users can add icon to phone home screen
- Opens like native app (full screen)
- Bookmarks URL for quick access
- **Cost: $0**

### Why This Works

✅ **No installation barriers** - works immediately  
✅ **Works on any device** - iOS, Android, tablets, desktop  
✅ **No app store approval** - instant updates  
✅ **Same codebase** - maintain once  
✅ **Responsive design** - optimized for mobile  
✅ **$0 cost** - included in base app  

### What Users DON'T Get (Initially)

❌ Offline mode (need internet connection)  
❌ Push notifications (email only)  
❌ Native app performance (web is still fast)  
❌ Biometric login (password/SSO only)  

**Note:** All these features can be enabled later at $0 cost by switching to Power Apps Mobile.

---

## 🚀 Implementation Phases

### Phase 1: Core Functionality (Weeks 1-4)

**Budget: $15k-30k**

#### Week 1-2: Foundation
- Create SharePoint Lists:
  - Portfolio Requests (main table)
  - Activity Log (comments/history)
  - SLA Configuration (rules)
- Configure columns:
  - SLA Due Date (calculated)
  - SLA Status (Red/Amber/Green - calculated)
  - Days Overdue (calculated)
- Setup security groups (Viewers, Contributors, Admins)

#### Week 3-4: Power App
- Build simple Power App (Canvas app):
  - Home screen (dashboard with counts)
  - List view (all requests, filterable)
  - Detail view (request details)
  - Submit form (new request intake)
  - Edit form (update requests)
- Mobile-responsive layout (automatic)
- Connect to SharePoint Lists
- Basic email notifications (on assignment)

**Deliverable:**
✅ Working app accessible on desktop + mobile web  
✅ 10 pilot users can submit and track requests  
✅ Basic SLA calculation  
✅ Email notifications  

**Cost: $15k-30k** (2-4 weeks @ $7.5k-15k/week)

---

### Phase 2: Automation & Views (Weeks 5-8)

**Budget: $5k-10k**

#### Week 5-6: Workflows
- Build Power Automate flows:
  - SLA Monitor (runs hourly)
    - Check for overdue items
    - Send email alerts to owner
    - Escalate to lead if >24h overdue
  - Stage Change Notifications
    - Notify requestor when stage changes
    - Notify new owner on reassignment
  - Comment Notifications
    - Alert watchers when comment added

#### Week 7-8: Enhanced Views
- Personal dashboards:
  - "My Assignments" (filtered to current user)
  - "Watching" (items user follows)
  - "Team View" (department/market filter)
- Kanban board view (by stage)
- Simple Power BI report (optional):
  - Requests by stage (pie chart)
  - SLA compliance rate (gauge)
  - Lead time trend (line chart)
- Search & filter functionality

**Deliverable:**
✅ SLA monitoring automated  
✅ Escalations happening automatically  
✅ Personalized views working  
✅ 50 users onboarded  

**Cost: $5k-10k** (2-4 weeks @ $2.5k-5k/week)

---

### Phase 3: Polish & Rollout (Weeks 9-12)

**Budget: $5k-10k**

#### Week 9-10: Optimization
- Performance tuning:
  - Optimize queries (delegation)
  - Reduce load times
  - Mobile layout refinements
- User testing with 50 pilot users
- Bug fixes
- Training materials:
  - Quick start guide (PDF)
  - Video tutorial (5 min)
  - Mobile access guide
  - FAQ document

#### Week 11-12: Full Rollout
- 500 user onboarding:
  - Security groups configured
  - Permissions assigned
  - Email announcement
  - Teams channel setup (#seiritsu-support)
- Admin training (3-5 admins)
- User training sessions (optional webinars)
- Documentation finalized
- Handover to support team

**Deliverable:**
✅ 500 users with access  
✅ Desktop + mobile web working  
✅ Support structure in place  
✅ Documentation complete  

**Cost: $5k-10k** (2-4 weeks @ $2.5k-5k/week)

---

## 🎯 What You Get (Minimum Version)

### Core Features Included

**✅ Request Management**
- Submit new requests (form)
- View all requests (list with search/filter)
- Edit assigned requests
- Comment on requests
- Attach files/documents
- Watch requests (follow updates)
- Stage management (move through lifecycle)

**✅ SLA Tracking**
- Automatic SLA calculation (by stage)
- Color-coded status (Green/Amber/Red)
- Overdue highlighting
- Email alerts for breaches
- Escalation to leads (24h after breach)

**✅ Dashboards**
- Personal dashboard ("My Assignments", "Watching")
- Team view (by department/market)
- SLA alert section (overdue items)
- Recent activity feed

**✅ Views**
- List view (table with sorting/filtering)
- Kanban board (by stage)
- Detail view (full request info)
- Search functionality

**✅ Notifications**
- Email alerts for assignments
- Email alerts for SLA breaches
- Email alerts for stage changes
- Email alerts for comments (on watched items)

**✅ Reporting (Basic)**
- Built-in SharePoint views/charts OR
- Simple Power BI report (3-5 charts)
- Export to Excel anytime

**✅ Security**
- Azure AD authentication
- Role-based access (Viewer/Contributor/Admin)
- Row-level security (who can edit what)
- Audit log (activity history)

**✅ Mobile Access**
- Responsive web design
- Works in any mobile browser
- Add to home screen (app-like)
- Touch-friendly interface

---

## ❌ What's NOT Included (Can Add Later)

### Deferred Features (Available at $0-500/month if needed)

**Native Mobile Apps** ($0 to enable)
- Power Apps Mobile (iOS/Android)
- Offline mode
- Push notifications
- Biometric login
- *Add in Phase 4 if users request it*

**JIRA Auto-Sync** ($500/month premium connector)
- Start with manual JIRA linking
- Add automatic sync later if critical
- *Most teams don't need real-time sync*

**Advanced Analytics** ($0-5k/month)
- Start with basic reports
- Upgrade to Power BI Premium later if needed
- *Basic reports sufficient for most*

**Copilot AI Agent** ($30/user/month)
- Not essential for launch
- Add in 6-12 months if desired
- *Nice-to-have, not must-have*

**Dataverse** ($40/user/month)
- Start with SharePoint Lists (<5k items)
- Migrate to Dataverse only if outgrow Lists
- *Unlikely to need for 500 users*

**Roadmap Timeline View** (can add for $2k-5k)
- Start with simple list view of roadmap items
- Add Gantt/timeline if requested
- *Most users fine with list view*

---

## 📊 Comparison: Lean vs Full-Featured

| Feature | Lean ($25k-50k) | Full ($84k-134k) |
|---------|----------------|------------------|
| **Core request management** | ✅ | ✅ |
| **SLA tracking & escalation** | ✅ | ✅ |
| **Dashboards & reports** | ✅ Basic | ✅ Advanced |
| **Mobile web access** | ✅ | ✅ |
| **Native mobile apps** | ⏸️ Later | ✅ |
| **Offline mode** | ⏸️ Later | ✅ |
| **Push notifications** | ❌ Email only | ✅ |
| **JIRA auto-sync** | ⏸️ Manual | ✅ Auto |
| **Power BI advanced** | ⏸️ Basic | ✅ Advanced |
| **Copilot AI** | ⏸️ Later | ✅ |
| **Build cost** | $25k-50k | $84k-134k |
| **Run cost** | $0-200/mo | $1k-2k/mo |
| **Timeline** | 12 weeks | 12 weeks |
| **Users supported** | 500 | 500 |

**Lean approach delivers 80% of value at 40% of cost.**

---

## 🔄 Upgrade Path

### When/How to Add Premium Features

**After 3 Months - Evaluate Usage:**

| User Feedback | Solution | Cost | Timeline |
|--------------|----------|------|----------|
| "We need offline access for flights" | Enable Power Apps Mobile | $0 | 1 week |
| "Email alerts not enough" | Enable push notifications | $0 | 1 week |
| "Manual JIRA linking is tedious" | Add premium connector | $500/mo | 2 weeks |
| "Basic reports insufficient" | Upgrade to Power BI Premium | $5k/mo | 2 weeks |
| "We need AI assistance" | Add Copilot agent | $30/user | 4 weeks |

**Philosophy:** Pay only for what users actually need, proven by usage data.

---

## 💡 Cost Optimization Tips

### How to Keep Costs at Absolute Minimum

**1. Use Included M365 Features**
- SharePoint Lists (not Dataverse) = $0
- Basic Power Apps (not Premium) = $0
- Standard Power Automate (not Premium) = $0
- Power BI free tier (not Pro) = $0

**2. Defer Premium Connectors**
- Manual JIRA linking initially
- Automate only if becomes pain point

**3. Limit Power BI Licenses**
- Only 2-3 report authors need Pro ($10/user)
- Everyone else views embedded reports (free)

**4. Start with Email Notifications**
- Email alerts sufficient for most users
- Add push notifications only if requested

**5. Self-Service Training**
- Video tutorials instead of live sessions
- Written guides instead of consultants
- Peer-to-peer support in Teams

**6. Internal Resources**
- Use internal IT for setup (vs consultant)
- Power users as admins (vs dedicated staff)
- Leverage existing M365 skills

---

## 🎯 ROI: Lean Approach

### Cost-Benefit Analysis

**Investment (Year 1): $25k-50k**

| Item | Cost |
|------|------|
| Build | $25k-50k |
| Run (12 months) | $0-2,400 |
| **Total Year 1** | **$25k-52k** |

**Returns (Year 1):**

| Benefit | Savings/Value |
|---------|--------------|
| Eliminate manual tracking (Excel/email) | ~$50k (500 users × 2 hrs/week × $50/hr) |
| Reduce SLA breaches | ~$20k (fewer escalations, faster decisions) |
| Improve roadmap visibility | ~$15k (better resource allocation) |
| Faster feasibility decisions | ~$10k (reduced cycle time) |
| **Total Annual Value** | **~$95k** |

**ROI: ~90-280%** (depends on build cost)

**Payback Period: 3-6 months**

---

## 🚨 Risks & Mitigations (Lean Approach)

### Potential Issues

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Users want offline mode | Medium | Medium | Can enable Power Apps Mobile at $0, 1 week |
| Email alerts too slow | Low | Low | Enable push notifications at $0 if critical |
| SharePoint hits 5k item limit | Medium | Low | Migrate to Dataverse ($40/user) only if needed |
| Manual JIRA linking tedious | Low | Medium | Add premium connector ($500/mo) if pain point |
| Basic reports insufficient | Low | Low | Upgrade Power BI ($5k/mo) only if demanded |

**Key Mitigation:** All deferred features can be added quickly at low cost.

---

## ✅ Recommendation

### Start Lean, Scale Smart

**Phase 1 (Months 0-3): Minimum Viable**
- Build: $25k-50k
- Run: $0-200/month
- Features: Core only
- Mobile: Web browser

**Phase 2 (Months 3-6): Based on Feedback**
- Add features users actually need
- Enable Power Apps Mobile if requested ($0)
- Add JIRA auto-sync if painful ($500/mo)
- Keep costs under $1k/month

**Phase 3 (Months 6-12): Mature Product**
- Advanced analytics if justified
- Copilot AI for power users
- Full-featured, still <$3k/month

**Total Cost (Year 1): $30k-65k**
- vs $84k-134k full-featured upfront
- **Savings: $20k-70k**

---

## 📋 Next Steps

**Week 0 (Now):**
1. Get budget approval for $25k-50k (vs $84k-134k)
2. Confirm M365 E3/E5 licensing
3. Identify internal IT resource (or hire contractor)
4. Define 10 pilot users

**Week 1:**
1. Kick off Phase 1
2. Create SharePoint Lists
3. Begin Power App development

**Week 4:**
1. Pilot with 10 users (desktop + mobile web)
2. Gather feedback
3. Iterate

**Week 12:**
1. Full rollout to 500 users
2. Monitor usage
3. Plan Phase 2 enhancements (based on data)

---

**Document Version:** 1.0  
**Date:** May 19, 2026  
**Approach:** Lean Start, Proven Value, Smart Scale  
**Target Audience:** Budget-Conscious Stakeholders