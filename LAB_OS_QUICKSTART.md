# 🚀 SOLAR PV LAB OS - QUICK START GUIDE

**Module:** CORE_LAB_OS_SESSION1
**Version:** 1.0.0
**Estimated Setup Time:** 5 minutes

---

## ⚡ INSTANT START (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run lab_os_core.py
```

### Step 3: Access the Lab OS
Open your browser to: **http://localhost:8501**

✅ **That's it!** The system will auto-load with complete sample data.

---

## 📱 FIRST LOGIN

**Default User:** Super Admin (Auto-loaded)
- **Name:** First staff member in the system
- **Role:** Super Admin
- **Permissions:** Full access to all features

**No password required** - Session-based authentication (production deployment should add proper auth)

---

## 🎯 WHAT TO EXPLORE FIRST

### 1️⃣ Dashboard (Home Page)
**What you'll see:**
- 5 Real-time KPI metrics
- 4 Interactive charts
- Active alerts panel
- Quick action buttons

**Try this:**
- Hover over charts for details
- Click on different chart tabs
- Check alert notifications

### 2️⃣ Test Management
**Navigate:** Sidebar → 🧪 Test Management

**Features:**
- View 50+ sample test records
- Filter by status, test type, date
- See active tests vs completed
- Export to CSV

**Try this:**
- Switch between tabs
- Apply filters
- Export test data

### 3️⃣ Client Management
**Navigate:** Sidebar → 👥 Client Management

**Features:**
- 20+ client profiles
- Client satisfaction scores
- Outstanding payments
- Test history per client

**Try this:**
- Sort clients by satisfaction
- Check active vs inactive
- Review client details

### 4️⃣ Equipment Management
**Navigate:** Sidebar → 🔧 Equipment

**Features:**
- 10+ equipment entries
- Calibration tracking
- Utilization metrics
- Maintenance alerts

**Try this:**
- Check calibration due dates
- Review equipment status
- Monitor utilization %

### 5️⃣ Staff Management
**Navigate:** Sidebar → 👨‍🔬 Staff Management

**Features:**
- 15+ staff members
- Role hierarchy
- Performance ratings
- Active test assignments

**Try this:**
- Review staff roles
- Check performance ratings
- See workload distribution

---

## 🔍 SEARCH FUNCTIONALITY

**Location:** Dashboard → 🔍 Quick Search (expandable)

**Can search for:**
- Test IDs (e.g., "TST-00001")
- Client names
- Equipment names

**How to use:**
1. Expand "Quick Search"
2. Type search query
3. See instant results

---

## 📊 UNDERSTANDING THE KPIS

### Active Tests
- **What it means:** Tests currently being conducted
- **Good range:** 15-25 (for this lab size)
- **Watch for:** Numbers trending too high (overload)

### Pending Reports
- **What it means:** Reports awaiting completion/approval
- **Good range:** Less than 20
- **Watch for:** Reports stuck in "Draft" status

### Average TAT
- **What it means:** Average turnaround time in days
- **Target:** 30 days
- **Good range:** 25-35 days
- **Watch for:** Increasing trend

### On-Time Percentage
- **What it means:** % of tests completed within target TAT
- **Target:** >80%
- **Good range:** 75-90%
- **Watch for:** Below 75%

### Monthly Revenue
- **What it means:** Revenue for current month
- **Expected:** ₹8-12 lakhs (for this lab)
- **Watch for:** Month-over-month decline

---

## 🔔 ALERT SYSTEM GUIDE

### Alert Types You'll See

1. **🚨 Overdue Tests (High Priority)**
   - Tests past target completion date
   - **Action:** Prioritize completion

2. **⚠️ Calibration Due (Medium/High Priority)**
   - Equipment calibration within 30 days
   - **Action:** Schedule calibration

3. **🔧 Maintenance Required**
   - Scheduled maintenance due
   - **Action:** Plan maintenance window

### Responding to Alerts

**High Priority:**
- Review immediately
- Take corrective action within 24 hours
- Document resolution

**Medium Priority:**
- Plan action within 3-5 days
- Schedule resources
- Monitor until resolved

---

## 📈 CHART INTERPRETATION

### Test Overview Charts

**Status Distribution (Pie Chart):**
- Shows % of tests in each status
- Ideal: 60-70% Completed, 20-30% In Progress

**Top Test Types (Bar Chart):**
- Most requested test types
- Use for resource planning

### Equipment Utilization

**Utilization Bar Chart:**
- Green (70-90%): Optimal
- Yellow (50-70%): Underutilized
- Red (>90%): Overutilized

### Revenue Trends

**Monthly Revenue Line:**
- Upward trend: Growth
- Flat: Stable
- Downward: Investigate

### TAT Analysis

**TAT Performance Pie:**
- Green: On-time
- Red: Delayed
- Target: 80%+ green

**TAT Distribution Histogram:**
- Most tests should cluster around 20-30 days
- Long tail indicates delays

---

## ⚙️ NAVIGATION TIPS

### Sidebar Menu
- **Always visible** on the left
- **Click any menu item** to navigate
- **Current view** highlighted

### Breadcrumb
- Shows **current location**
- Format: 🏠 Home / View Name
- Helps orientation

### Quick Actions
- **Fast access** to common tasks
- Located on Dashboard
- One-click navigation

---

## 💾 DATA MANAGEMENT

### Sample Data Included

**Pre-loaded data represents a 5-10 year old lab:**

| Data Type | Quantity | Period |
|-----------|----------|--------|
| Organization | 1 | Est. 2015 |
| Branches | 2 | 2015-2018 |
| Clients | 20+ | Last 5 years |
| Equipment | 10+ | 1-10 years old |
| Staff | 15+ | 6 mo - 10 yrs |
| Tests | 50+ | Last 3 years |

### Data Characteristics
- **Realistic**: Based on actual lab operations
- **Varied**: Different statuses, types, results
- **Relational**: Clients linked to tests, staff to tests, etc.
- **Time-based**: Historical data with trends

---

## 🎓 LEARNING PATH

### Day 1: Familiarization (30 mins)
1. ✅ Launch application
2. ✅ Explore dashboard
3. ✅ Review KPIs
4. ✅ Check charts

### Day 2: Features (1 hour)
1. ✅ Test Management
2. ✅ Client Management
3. ✅ Equipment tracking
4. ✅ Staff overview

### Day 3: Advanced (1 hour)
1. ✅ Filtering and search
2. ✅ Export data
3. ✅ Alert management
4. ✅ Settings customization

### Week 1: Proficiency
1. ✅ Daily dashboard review
2. ✅ Weekly test monitoring
3. ✅ Monthly reporting
4. ✅ Data-driven decisions

---

## 🔧 CUSTOMIZATION OPTIONS

### Settings View
**Navigate:** Sidebar → ⚙️ Settings

**Tabs:**
1. **Organization** - Lab profile, accreditations
2. **Users** - Role management, permissions
3. **System** - System info, statistics

### What You Can Customize:
- Organization profile (view only in this version)
- User roles review
- System preferences (future)

---

## 📱 BROWSER COMPATIBILITY

### Recommended Browsers:
- ✅ **Chrome** (Best performance)
- ✅ **Firefox**
- ✅ **Edge**
- ⚠️ Safari (Some chart features may vary)
- ❌ IE (Not supported)

### Recommended Screen Resolution:
- **Minimum:** 1280x720
- **Optimal:** 1920x1080 or higher
- **Mobile:** Responsive but best on desktop/tablet

---

## 🐛 TROUBLESHOOTING

### Application Won't Start

**Error:** `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error:** `Address already in use`
```bash
# Solution: Use different port
streamlit run lab_os_core.py --server.port 8502
```

### Charts Not Showing

**Issue:** Blank chart areas

**Solution:**
1. Check browser console (F12)
2. Refresh page (Ctrl+R)
3. Clear browser cache
4. Verify Plotly installed: `pip show plotly`

### Data Not Loading

**Issue:** Empty tables/charts

**Solution:**
1. Check console for errors
2. Verify `st.session_state.lab_os_initialized` is True
3. Restart application
4. Clear Streamlit cache: `streamlit cache clear`

### Performance Issues

**Issue:** Slow loading

**Solution:**
1. Close other browser tabs
2. Reduce date range filters
3. Clear browser cache
4. Check system resources

---

## 📞 SUPPORT RESOURCES

### In-App Help
- **Tooltips:** Hover over metrics/charts
- **Info Boxes:** Blue info messages
- **Alerts:** Red/yellow/orange notifications

### Documentation
1. **LAB_OS_CORE_README.md** - Complete documentation
2. **LAB_OS_QUICKSTART.md** - This guide
3. **requirements.txt** - Dependency list

### Getting Help
1. Check documentation first
2. Review error messages
3. Check browser console
4. Restart application

---

## ✅ VERIFICATION CHECKLIST

After setup, verify all features work:

- [ ] Application launches without errors
- [ ] Dashboard displays with 5 KPI metrics
- [ ] All 4 chart tabs render correctly
- [ ] Sidebar navigation works
- [ ] Test Management shows 50+ records
- [ ] Client Management shows 20+ clients
- [ ] Equipment shows 10+ items
- [ ] Staff shows 15+ members
- [ ] Search functionality works
- [ ] Alerts panel displays
- [ ] All navigation buttons work
- [ ] Settings view accessible

**If all checked:** ✅ You're ready to go!

---

## 🎯 NEXT STEPS

### For Evaluation:
1. ✅ Explore all 8 main views
2. ✅ Test filtering and search
3. ✅ Review sample data quality
4. ✅ Check chart interactivity
5. ✅ Evaluate UI/UX

### For Implementation:
1. **Customize** organization profile
2. **Add** real client data
3. **Configure** equipment list
4. **Import** staff roster
5. **Start** entering real tests

### For Development:
1. **Review** code structure
2. **Extend** functionality
3. **Integrate** with database
4. **Add** authentication
5. **Deploy** to production

---

## 📊 SAMPLE SCENARIOS

### Scenario 1: Daily Operations Check (5 mins)
1. Open Dashboard
2. Review Active Tests count
3. Check TAT metrics
4. Review high-priority alerts
5. Take action on overdue items

### Scenario 2: Client Inquiry (2 mins)
1. Navigate to Client Management
2. Search for client
3. Review test history
4. Check satisfaction score
5. Respond with data

### Scenario 3: Monthly Reporting (15 mins)
1. Navigate to Analytics
2. Review Revenue Trends
3. Check TAT Performance
4. Export test data
5. Generate reports

### Scenario 4: Equipment Planning (10 mins)
1. Navigate to Equipment
2. Check utilization metrics
3. Review calibration schedule
4. Plan maintenance windows
5. Allocate resources

---

## 🌟 POWER USER TIPS

### Tip 1: Use Keyboard Shortcuts
- `Ctrl+R` - Refresh data
- `F11` - Fullscreen mode
- `Ctrl+F` - Browser search in tables

### Tip 2: Bookmark Favorite Views
- Bookmark specific views in browser
- Create shortcuts for frequent tasks

### Tip 3: Export Data Regularly
- CSV exports for Excel analysis
- Backup important data
- Share with stakeholders

### Tip 4: Monitor Trends Weekly
- Review charts weekly
- Identify patterns early
- Proactive problem solving

### Tip 5: Set Up Alerts Review Routine
- Check alerts daily (5 mins)
- Categorize by priority
- Delegate and track

---

## 🏆 SUCCESS METRICS

### Week 1 Goals:
- [ ] Complete system familiarization
- [ ] Navigate all views independently
- [ ] Understand all KPIs
- [ ] Respond to sample alerts

### Month 1 Goals:
- [ ] Daily dashboard review routine
- [ ] Regular data exports
- [ ] Trend analysis capability
- [ ] Data-driven decision making

### Quarter 1 Goals:
- [ ] Full operational use
- [ ] Custom reporting
- [ ] Process optimization
- [ ] Measurable improvements

---

## 📝 FEEDBACK

### We Want to Hear From You!

**What's working well?**
- UI/UX feedback
- Feature usefulness
- Performance observations

**What could be better?**
- Missing features
- Workflow improvements
- Bug reports

**What's next?**
- Feature requests
- Integration needs
- Customization requirements

---

## 🎉 CONCLUSION

Congratulations! You're now ready to use the Solar PV Lab OS.

**Remember:**
- ✅ Start with the Dashboard
- ✅ Explore systematically
- ✅ Use sample data to learn
- ✅ Refer to documentation
- ✅ Practice daily

**The system is designed to:**
- 📊 Provide instant insights
- ⚡ Speed up operations
- ✅ Improve quality
- 💰 Increase profitability
- 😊 Enhance satisfaction

**Happy testing!** 🧪☀️

---

**Quick Reference:**
- 📚 Full Docs: LAB_OS_CORE_README.md
- 🚀 This Guide: LAB_OS_QUICKSTART.md
- 💻 Main File: lab_os_core.py
- 📦 Dependencies: requirements.txt

---

© 2025 Solar PV Lab OS | Quick Start Guide v1.0.0
