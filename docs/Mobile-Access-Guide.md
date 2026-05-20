# Seiritsu Mobile Access Guide

**Quick Reference for iOS & Android Users**

---

## 📱 Three Ways to Access Seiritsu on Mobile

### Option 1: Power Apps Mobile (Recommended) ⭐

**Best for:** Daily users, field workers, managers on the go

**Installation:**
1. Download **"Power Apps"** from App Store (iOS) or Google Play (Android)
2. Open app and sign in with your Adidas credentials
3. Find **"Seiritsu"** in the app list
4. Tap star icon to add to favorites
5. Done! 🎉

**Features:**
- ✅ Works offline
- ✅ Push notifications for SLA alerts
- ✅ Camera integration for attachments
- ✅ Biometric login (Face ID / Fingerprint)
- ✅ Native performance

---

### Option 2: Microsoft Teams Mobile

**Best for:** Quick lookups, users already in Teams

**Setup:**
1. Open Teams mobile app
2. Go to "Apps" tab
3. Search for "Seiritsu"
4. Add as a tab
5. Pin for quick access

**Features:**
- ✅ No separate install needed
- ✅ Integrated with Teams notifications
- ✅ Quick access from Teams

---

### Option 3: Mobile Web Browser

**Best for:** Occasional users, external contractors

**Access:**
1. Open Safari (iOS) or Chrome (Android)
2. Go to: `https://apps.powerapps.com/seiritsu`
3. Sign in with Adidas credentials
4. (Optional) Add to home screen for app-like experience

**To add to home screen:**
- **iOS:** Tap Share → "Add to Home Screen"
- **Android:** Tap Menu (⋮) → "Add to Home screen"

---

## 🚀 Mobile Features

### Quick Actions from Home Screen

**Power Apps Mobile widgets:**
- "My Assignments" - See your tasks
- "SLA Alerts" - View overdue items
- "Quick Submit" - Fast request submission

### Offline Mode

**How it works:**
1. App downloads your data when online
2. You can view/edit while offline
3. Changes sync automatically when reconnected

**Available offline:**
- ✅ View assigned requests
- ✅ Read request details
- ✅ Add comments (saves as draft)
- ✅ Submit new requests (saves to queue)
- ❌ Power BI reports (require connection)

### Push Notifications

**You'll receive alerts for:**
- 🚨 SLA breaches on your requests
- ⚠️ Requests approaching SLA deadline
- 📬 New assignments
- 💬 Comments on watched requests
- ✅ Approvals/stage changes

**Managing notifications:**
- Tap notification → opens directly to request
- Swipe to dismiss or mark as read
- Configure in Settings → Notifications

---

## 📋 Mobile Use Cases

### Use Case 1: Submit Request from Field
**Scenario:** You're at a store and spot an issue needing a new feature

**Steps:**
1. Open Seiritsu on mobile
2. Tap **"+ New Request"** button
3. Fill title and description (use voice-to-text)
4. Take photo with camera (attach directly)
5. Select priority and market
6. Submit!

**Time:** ~2 minutes

---

### Use Case 2: Quick Status Check
**Scenario:** In a meeting, stakeholder asks about REQ-0245

**Steps:**
1. Open Seiritsu on mobile
2. Use search (🔍) at top
3. Type "REQ-0245" or keyword
4. Tap request to view details
5. Share status verbally

**Time:** ~15 seconds

---

### Use Case 3: Approve on the Go
**Scenario:** You're traveling, urgent funding approval needed

**Steps:**
1. Receive push notification
2. Tap notification (opens request)
3. Review business case
4. Tap **"Approve"** button
5. Add comment (optional)
6. Done!

**Time:** ~1 minute

---

### Use Case 4: Daily Standup Prep
**Scenario:** Morning commute, prep for team standup

**Steps:**
1. Open Seiritsu mobile
2. View "My Work" dashboard
3. Check "At Risk" items (amber/red SLA)
4. Add quick notes to requests
5. Ready for standup!

**Time:** ~5 minutes

---

## 🎨 Mobile UI Overview

### Bottom Navigation Bar

```
┌─────────────────────────────┐
│                             │
│    [Content Area]           │
│                             │
│                             │
└─────────────────────────────┘
  🏠   📋   ➕   📊   👤
 Home  Work  New  Stats Profile
```

**Tabs:**
- **🏠 Home** - Dashboard with alerts and stats
- **📋 My Work** - Your assignments and watched items
- **➕ New** - Submit new request (quick access)
- **📊 Stats** - Analytics (requires connection)
- **👤 Profile** - Settings and notifications

### Home Screen Layout

```
┌─────────────────────────────┐
│  🚨 3 SLA Breaches         │ ← Alert banner
├─────────────────────────────┤
│  My Assignments (5)        │ ← Tap to expand
│  REQ-0245  [Green dot]     │
│  REQ-0221  [Green dot]     │
├─────────────────────────────┤
│  At Risk (2)               │ ← SLA approaching
│  REQ-0234  [Red dot]       │
│  REQ-0189  [Amber dot]     │
├─────────────────────────────┤
│  Recent Activity           │
│  Updated 2 min ago         │
└─────────────────────────────┘
```

### Request Detail Screen

**Swipe gestures:**
- Swipe left: Next request
- Swipe right: Previous request
- Pull down: Refresh

**Quick actions (bottom sheet):**
- Comment
- Watch/Unwatch
- Share (via Teams/Email)
- Reassign
- Change stage

---

## ⚙️ Mobile Settings

### Recommended Settings

**Notifications:**
- ✅ SLA Breaches (High priority)
- ✅ Assignments (High priority)
- ✅ Comments on watched items (Normal)
- ❌ Stage changes (optional - can be noisy)

**Offline Mode:**
- ✅ Auto-sync when connected
- ✅ Download data for: "My assignments only" (saves storage)
- Data retention: 30 days

**Security:**
- ✅ Require biometric (Face ID / Fingerprint)
- ✅ Auto-lock after 5 minutes
- ✅ Clear cache on sign out

**Data Usage:**
- ✅ Download over Wi-Fi only (saves mobile data)
- ✅ Compress images before upload
- Sync frequency: Every 15 minutes

---

## 🔒 Security & Privacy

**Enterprise Security Features:**
- Azure AD authentication (same as desktop)
- App-level encryption
- Remote wipe (if device lost)
- Session timeout (configurable)
- No data stored in device backups

**IT can enforce:**
- PIN or biometric required
- Screenshot prevention (sensitive data)
- Copy/paste restrictions
- Jailbreak/root detection

---

## 🆘 Troubleshooting

### App won't sync
**Fix:**
1. Check internet connection
2. Force quit and reopen app
3. Pull down to refresh manually
4. Sign out and sign back in

### Push notifications not working
**Fix:**
1. Check phone notification settings
2. Allow notifications for Power Apps
3. In Seiritsu: Profile → Notifications → Enable all
4. Test: Submit a request and assign to yourself

### "Unable to connect" error
**Fix:**
1. Check if on corporate VPN (if required)
2. Check Wi-Fi/cellular connection
3. Try switching between Wi-Fi and cellular
4. Contact IT if persists

### App is slow
**Fix:**
1. Clear app cache: Profile → Settings → Clear cache
2. Reduce offline data retention (Settings → Offline)
3. Close other apps (free up memory)
4. Update to latest app version

### Can't find Seiritsu in Power Apps
**Fix:**
1. Sign in with correct Adidas account
2. Check with IT that you're authorized
3. Pull down to refresh app list
4. Contact Seiritsu support

---

## 📞 Support

**Need help?**
- Teams channel: **#seiritsu-support**
- Email: **seiritsu-help@adidas.com**
- In-app: Profile → Help & Feedback

**Quick tips:**
- 🎥 Watch mobile tutorial: "Using Seiritsu on Your Phone" (2 min)
- 📄 Full documentation: SharePoint → Seiritsu Docs
- 💬 Ask in Teams: #seiritsu-users community

---

## 📊 Performance Tips

**For best mobile experience:**

1. **Keep app updated** - Install updates from app store
2. **Use Wi-Fi when possible** - Faster sync, saves data
3. **Enable offline mode** - Access data without connection
4. **Pin favorites** - Quick access to frequent requests
5. **Use search** - Faster than scrolling (🔍 icon)
6. **Compress photos** - App does this automatically
7. **Clear old cache** - Monthly cleanup keeps app fast

**Expected performance:**
- App launch: 1-2 seconds
- Request list load: <1 second
- Request detail: <500ms
- Search: <500ms
- Photo upload: ~2-3 seconds (compressed)

---

## 🎯 Mobile-First Workflows

### Workflow 1: Morning Routine (5 min)
1. ☕ Coffee + open Seiritsu mobile
2. Check "SLA Alerts" - any red flags?
3. Review "My Assignments" - priorities for today
4. Check "Watching" - updates from others
5. Add notes to items you'll work on
6. Close app, start your day!

### Workflow 2: Weekly Review (10 min)
1. Open "Stats" tab
2. Check your SLA compliance rate
3. Review completed requests (this week)
4. Identify bottlenecks (requests stuck >5 days)
5. Plan actions for next week

### Workflow 3: Executive Glance (30 sec)
1. Open dashboard
2. See total active requests
3. See SLA breach count
4. Check roadmap progress
5. Done - high-level view acquired!

---

## 🌟 Pro Tips

**Power User Shortcuts:**

1. **Voice input** - Use microphone icon for descriptions
2. **Shake to refresh** - Shake phone to force sync
3. **3D Touch / Long press** - Preview request without opening
4. **Widgets** - Add Seiritsu widget to phone home screen
5. **Siri Shortcuts** (iOS) - "Hey Siri, show my Seiritsu tasks"
6. **Quick share** - Share request via Teams/Email (Share button)
7. **Copy link** - Long press request → Copy link → Share anywhere

**Gestures:**
- Swipe left on request: Quick actions menu
- Swipe right on request: Mark as read
- Pinch to zoom: Charts and images
- Pull down: Refresh data

---

## 📱 Device Requirements

**Minimum:**
- **iOS:** iPhone 6s or newer, iOS 14+
- **Android:** Android 8.0 (Oreo) or newer
- **Storage:** 100 MB free space
- **Network:** Wi-Fi or cellular data

**Recommended:**
- **iOS:** iPhone XR or newer, iOS 16+
- **Android:** Android 11+, 3GB+ RAM
- **Storage:** 500 MB free (for offline data)
- **Network:** 4G/LTE or 5G for best performance

**Tested devices:**
- ✅ iPhone 13/14/15 (iOS 16+)
- ✅ Samsung Galaxy S21/S22/S23
- ✅ Google Pixel 6/7/8
- ✅ iPad (any model with iOS 14+)
- ✅ Samsung tablets (Android 10+)

---

## 🚀 Coming Soon (Future Enhancements)

**Planned mobile features:**
- 📷 QR code scanning (link to requests)
- 🎤 Voice notes (attach audio comments)
- 📍 Location tagging (for field submissions)
- 🌍 Multi-language support
- 🌙 Dark mode
- ⌚ Apple Watch / Wear OS app
- 🚗 CarPlay integration (view-only)

---

**Version:** 1.0  
**Last Updated:** May 19, 2026  
**Feedback:** seiritsu-help@adidas.com

*Seiritsu - Portfolio management in your pocket* 📱