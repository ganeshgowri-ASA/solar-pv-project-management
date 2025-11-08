# 🚀 Solar PV SOP Generator - Quick Start Guide

## ⚡ 5-Minute Quick Start

### Step 1: Launch Application (30 seconds)

```bash
cd /home/user/solar-pv-project-management
streamlit run sop_generator_complete.py
```

The application will open automatically in your browser at `http://localhost:8501`

### Step 2: Navigate to SOP Generator (10 seconds)

1. In the sidebar, click **"📝 SOP Generator"**
2. Click on the **"📝 Create SOP"** tab

### Step 3: Fill Minimum Required Fields (3 minutes)

#### Document Header (Required fields marked with *)
```
Document Title*: Thermal Cycling Test SOP
Document Number*: SOP-TC-001
Document Owner*: Dr. Rajesh Kumar
```

#### Approval Chain (Minimum 1 approver)
```
Role 1: Doer
Name 1: Arun Patel
Signature 1: [Signature]
```

#### Document Sections

**Purpose*** (Copy-paste example):
```
This SOP defines the procedure for conducting thermal cycling tests
on photovoltaic modules as per IEC 61215-2:2016 MQT 12. The test
evaluates the ability of the module to withstand thermal mismatch,
fatigue, and other stresses caused by repeated temperature changes.
```

**Scope*** (Copy-paste example):
```
This procedure applies to all crystalline silicon and thin-film
photovoltaic modules tested for design qualification. The test
consists of 200 thermal cycles between -40°C and +85°C.
```

### Step 4: Generate Document (1 minute)

1. Scroll to bottom of form
2. Ensure **"Export as Word (.docx)"** is checked
3. Click **"🚀 Generate SOP Document"**
4. Wait for processing (5-10 seconds)
5. Click **"📄 Download Word Document"**

**Congratulations! You've created your first SOP!** 🎉

---

## 📋 Complete SOP Creation (15 minutes)

### Enhanced Creation with All Sections

#### 1. Company Branding
- **Upload Company Logo**: Click "Browse files" → Select PNG/JPG logo
- **Company Name**: "Solar Test Lab Pvt Ltd"
- **Division**: "Testing & Certification"

#### 2. Comprehensive Approval Chain (3 approvers)

| Role | Name | Example |
|------|------|---------|
| Doer | Arun Patel | Test Engineer who created SOP |
| Reviewer | Sneha Reddy | Senior Engineer for technical review |
| Approver | Dr. Rajesh Kumar | Lab Manager for final approval |

#### 3. Revision History

| Revision | Date | Description | Author |
|----------|------|-------------|--------|
| 00 | 2024-01-15 | Initial Release | Arun Patel |

#### 4. Definitions (Add 3-5 key terms)

Examples:
- **DUT**: Device Under Test - The PV module being tested
- **STC**: Standard Test Conditions - 1000 W/m², 25°C, AM 1.5
- **Pmax**: Maximum Power - Peak power output under STC
- **TC**: Thermal Cycling - Repeated temperature exposure test

#### 5. Responsibilities (Add 3-4 roles)

Examples:
- **Test Engineer**: Conduct test, record data, prepare draft report
- **Lab Technician**: Sample preparation, equipment setup
- **Quality Manager**: Review test reports, approve SOPs
- **Lab Director**: Final approval and sign-off

#### 6. Normative References

**Select from library**:
- ✅ IEC 61215-2:2016, Terrestrial photovoltaic (PV) modules - Design qualification and type approval - Part 2: Test procedures
- ✅ ISO/IEC 17025:2017, General requirements for the competence of testing and calibration laboratories

**Or add custom**:
```
Laboratory Quality Manual, Document No. LQM-001-R05
Laboratory Safety Handbook, Document No. LSH-001-R03
```

#### 7. HSE Risk Assessment (Add 3-5 risks)

| Hazard | Risk Level | Control Measures | PPE Required |
|--------|-----------|------------------|--------------|
| High/Low Temperature Surfaces | Medium | Warning labels, insulated handles | Heat-resistant gloves |
| Electrical Shock | High | Lockout/tagout, grounding | Insulated gloves, safety shoes |
| Heavy Equipment | Medium | Two-person lift, mechanical aids | Safety shoes, back support |
| Chemical Exposure (cleaning) | Low | Proper ventilation, MSDS review | Nitrile gloves, safety glasses |

#### 8. Equipment and Materials (Add 5-8 items)

| Equipment/Material | Standard Specification | Actual Details |
|-------------------|----------------------|----------------|
| Thermal Cycling Chamber | -40°C to +85°C, ±2°C accuracy | EnviroTest TC-2000, ID: EQP-002 |
| IV Curve Tracer | 0-50V, 0-15A | Keysight B2901A, ID: EQP-015 |
| Data Logger | 8+ channels, 1-minute logging | Agilent 34970A, ID: EQP-023 |
| Temperature Sensors | Type K thermocouple, ±0.5°C | Omega KMQSS-125, Cal: 2024-11-01 |
| Sample Modules | Per IEC 61215 requirements | Customer samples, Batch: 2024-001 |

**Upload**: Equipment photos (optional)

#### 9. Test Procedure Steps (Add 10-15 steps)

Example steps:
```
1. Verify thermal cycling chamber calibration is current (within 6 months)
2. Inspect test samples for pre-existing damage or defects
3. Perform initial electrical characterization at STC (25°C, 1000 W/m²)
4. Record initial Pmax, Voc, Isc values
5. Install module in thermal cycling chamber with thermocouples attached
6. Program chamber for 200 cycles: -40°C (30 min) ↔ +85°C (30 min)
7. Monitor and log chamber temperature every 5 minutes
8. Monitor and log module temperature every 5 minutes
9. Visual inspection every 50 cycles for defects
10. After cycle 200, remove modules and allow stabilization (4 hours at 25°C)
11. Perform final electrical characterization at STC
12. Compare initial vs final electrical parameters
13. Perform detailed visual inspection per IEC 61215-1 Section 7.1
14. Document all observations and measurements
15. Calculate power degradation: Δ = ((Pmax,initial - Pmax,final) / Pmax,initial) × 100%
```

**Upload**: Process flowchart (optional)

#### 10. Analysis Methodology

```
The test results shall be analyzed using the following methodology:

1. Power Degradation Calculation:
   Δ = ((Pmax,initial - Pmax,final) / Pmax,initial) × 100%

2. Visual Inspection Criteria:
   - No evidence of IEC 61215-1 visual defects
   - No broken cells, bubbles, delamination
   - No broken interconnects or solder bonds

3. Electrical Parameters:
   - All parameters within specification
   - Insulation resistance > 40 MΩ

4. Statistical Analysis:
   - Calculate mean and standard deviation for sample set
   - Identify outliers using 2-sigma criteria
```

#### 11. Final Requirements

```
- Completion of all 200 thermal cycles without interruption
- All temperature set points achieved within ±2°C tolerance
- Complete data logging with no gaps
- Visual inspection documented with photographs
- Final electrical characterization within 24 hours of test completion
- Test report prepared within 5 working days
```

#### 12. Pass/Fail Criteria

| Parameter | Pass Criteria | Fail Criteria |
|-----------|--------------|---------------|
| Visual Inspection | No major defects per IEC 61215-1 | Any major defect present |
| Power Degradation (Pmax) | Δ < 5% | Δ ≥ 5% |
| Open Circuit Voltage (Voc) | Degradation < 5% | Degradation ≥ 5% |
| Short Circuit Current (Isc) | Degradation < 5% | Degradation ≥ 5% |
| Insulation Resistance | > 40 MΩ | ≤ 40 MΩ |
| Wet Leakage Current | < 1 mA | ≥ 1 mA |

**Upload**: Test schematic diagram (optional)

#### 13. Appendix

```
Additional Information:
- Thermal cycling chamber qualification records
- Temperature sensor calibration certificates
- IV curve tracer calibration certificate
- Sample photographs (before and after testing)
- Raw data files location: \\server\lab-data\thermal-cycling\
- Reference to laboratory quality manual

Related Documents:
- SOP-EC-001: Electrical Characterization at STC
- SOP-VI-001: Visual Inspection Procedure
- SOP-CAL-001: Equipment Calibration Procedure
```

### Step 5: Configure Export Options

**Translation** (Optional):
- Select language: Hindi / Tamil / Spanish / etc.
- Document will be auto-translated

**Export Formats**:
- ✅ Export as Word (.docx) ← **Recommended**
- ☐ Export as PDF ← For read-only distribution
- ☐ Export as Excel ← For data analysis

### Step 6: Generate and Download

1. Click **"🚀 Generate SOP Document"**
2. Wait for progress bar to complete
3. Download buttons will appear
4. Click **"📄 Download Word Document"**
5. Open in Microsoft Word or LibreOffice
6. Review and customize as needed

---

## 🌐 Translation Feature

### Translate New Document (During Creation)

1. Fill out SOP form as normal
2. Scroll to **"Translation Options"**
3. Select language: **"Hindi"** (हिन्दी)
4. Generate document
5. Document will be automatically translated

### Translate Existing Document

1. Navigate to **"🌐 Translation"** tab
2. Select document from dropdown
3. Choose target language
4. Click **"🌐 Translate Document"**
5. Download translated version

**Supported Languages**:
- 🇮🇳 Hindi, Tamil, Telugu, Gujarati, Marathi, Kannada
- 🌍 Spanish, French, German, Chinese, Japanese

---

## 📚 Using Standards Library

### Browse Standards

1. Click **"📚 Standards Library"** tab
2. Filter by category (optional)
3. Expand any standard to view details
4. Click **"📋 Copy Citation"** to copy

### Add Your Own Standard

1. Click **"➕ Add New Standard"**
2. Fill in form:
   ```
   Standard Code: IEC 62804-1:2015
   Authority: IEC
   Category: PV Module Testing
   Year: 2015
   Title: Photovoltaic (PV) modules - Test methods for the
          detection of potential-induced degradation - Part 1:
          Crystalline silicon
   ```
3. Click **"Add Standard"**
4. Now available in your library

### Use Standards in SOP

When creating SOP:
1. In **"Normative References"** section
2. Use **"Select Standards from Library"** dropdown
3. Select all applicable standards
4. Citations will be auto-inserted

---

## 📄 Document Management

### View All SOPs

1. Click **"📄 My Documents"** tab
2. Browse all created SOPs
3. Expand any document to see details

### Export Existing SOP

1. In "My Documents" tab
2. Expand document
3. Choose export format:
   - **📄 Export Word** - Editable .docx
   - **📕 Export PDF** - Read-only .pdf
   - **📊 Export Excel** - Data tables .xlsx
4. Click download button

### Delete SOP

1. In "My Documents" tab
2. Expand document
3. Click **"🗑️ Delete"**
4. Confirm deletion

---

## 🔧 Advanced Features

### Custom Branding

**Upload Company Logo**:
- Appears on first page of SOP
- Supports PNG, JPG, JPEG
- Recommended size: 200x100 pixels
- Max file size: 5 MB

### Multiple File Uploads

**Equipment Photos**:
- Upload multiple images
- Shows your actual lab equipment
- Embedded in document

**Process Flowcharts**:
- Upload process flow diagrams
- Supports PNG, JPG, PDF
- Helps visualize workflow

**Test Schematics**:
- Upload wiring/connection diagrams
- Critical for electrical tests
- Ensures proper setup

**Data Tables**:
- Upload CSV or Excel files
- Import acceptance criteria tables
- Import equipment lists

### Approval Workflow Integration

The SOP Generator integrates with the existing **Approval Workflow** module:

1. Create SOP document
2. Navigate to **"📝 Workflows"** in sidebar
3. Create new approval request
4. Attach SOP document
5. Define approvers
6. Track approval status

---

## 💡 Tips & Best Practices

### Writing Tips

✅ **DO**:
- Use clear, simple language
- Write in imperative mood ("Measure", "Record", not "The engineer measures")
- Include specific numbers (temperature, time, etc.)
- Reference standards explicitly
- Use consistent terminology
- Include safety warnings

❌ **DON'T**:
- Use ambiguous terms ("about", "approximately")
- Leave steps to interpretation
- Omit safety considerations
- Forget to reference standards
- Use jargon without definitions

### Document Naming Convention

```
SOP-[Category]-[Number]-[Revision]

Examples:
SOP-TC-001-R00  (Thermal Cycling, SOP #1, Revision 00)
SOP-HF-002-R01  (Humidity Freeze, SOP #2, Revision 01)
SOP-UV-003-R00  (UV Test, SOP #3, Revision 00)

Categories:
TC  - Thermal Cycling
HF  - Humidity Freeze
UV  - UV Preconditioning
ML  - Mechanical Load
HL  - Hail Impact
WT  - Wet Leakage
IR  - Insulation Resistance
EC  - Electrical Characterization
```

### Revision Management

**When to create new revision**:
- Procedure changed
- Equipment updated
- Standard revised
- Safety improvement
- Error correction

**Revision numbering**:
```
00 - Initial release
01 - First revision
02 - Second revision
...
10 - Tenth revision
```

**Revision description examples**:
```
"Initial Release"
"Updated temperature tolerance to ±2°C per IEC 61215-2:2021"
"Added safety requirement for lockout/tagout"
"Corrected calculation formula for power degradation"
"Equipment upgraded from Model A to Model B"
```

### Section-Specific Tips

**Purpose**:
- Keep it concise (2-3 sentences)
- State what the test measures
- Reference the standard

**Scope**:
- Define what IS included
- Define what IS NOT included
- Specify module types

**Procedure**:
- Number all steps
- One action per step
- Include decision points
- Specify tolerances

**Criteria**:
- Use measurable values
- Reference standard limits
- Include units
- Be specific

---

## 🆘 Troubleshooting

### Issue: Can't Generate Document

**Check**:
- [ ] All required fields filled (*marked)
- [ ] Purpose section not empty
- [ ] Scope section not empty
- [ ] At least 1 approver defined

### Issue: Translation Not Working

**Check**:
- [ ] Internet connection active
- [ ] deep-translator installed: `pip list | grep deep-translator`
- [ ] Try simpler text first to test

### Issue: Logo Not Showing

**Check**:
- [ ] File format is PNG or JPG
- [ ] File size < 5 MB
- [ ] Image not corrupted (open in image viewer)

### Issue: Download Button Not Working

**Try**:
- [ ] Refresh page (F5)
- [ ] Clear browser cache
- [ ] Try different browser (Chrome recommended)
- [ ] Check popup blocker settings

---

## 📊 Keyboard Shortcuts

```
Ctrl + F5        - Hard refresh page
Tab              - Move to next field
Shift + Tab      - Move to previous field
Ctrl + A         - Select all text in field
Ctrl + C         - Copy
Ctrl + V         - Paste
```

---

## 🎯 Example Use Cases

### Use Case 1: IEC 61215 Full Qualification

**Scenario**: Lab needs SOPs for complete IEC 61215 testing

**SOPs to Create**:
1. SOP-TC-001: Thermal Cycling (MQT 12)
2. SOP-HF-002: Humidity Freeze (MQT 13)
3. SOP-UV-003: UV Preconditioning (MQT 09)
4. SOP-ML-004: Mechanical Load (MQT 16)
5. SOP-HL-005: Hail Impact (MQT 17)

**Time**: ~2 hours for all 5 SOPs using templates

### Use Case 2: NABL Accreditation Preparation

**Scenario**: Lab preparing for ISO/IEC 17025 accreditation

**Requirements**:
- ✅ Documented procedures (SOPs)
- ✅ Review and approval workflow
- ✅ Revision control
- ✅ Document numbering system
- ✅ Normative references
- ✅ Traceability (audit trail)

**Solution**: Use SOP Generator to create all test procedures with proper approval workflow

### Use Case 3: Multi-Language Documentation

**Scenario**: International lab with local language requirements

**Approach**:
1. Create master SOP in English
2. Translate to local language (Hindi, Chinese, etc.)
3. Maintain both versions
4. Update both when revisions occur

---

## ✅ Quality Checklist

Before finalizing your SOP, check:

- [ ] **Header Complete**: Title, doc number, owner filled
- [ ] **Logo Uploaded**: Company branding included
- [ ] **Approval Chain**: All roles and names defined
- [ ] **Revision History**: Initial revision documented
- [ ] **Purpose Clear**: Objective stated clearly
- [ ] **Scope Defined**: Applicability specified
- [ ] **Definitions Added**: Technical terms explained
- [ ] **Responsibilities Assigned**: Who does what
- [ ] **Standards Referenced**: All applicable standards cited
- [ ] **HSE Assessed**: All hazards identified
- [ ] **Equipment Listed**: All equipment specified
- [ ] **Procedure Complete**: All steps numbered and clear
- [ ] **Analysis Described**: How to analyze results
- [ ] **Criteria Defined**: Clear pass/fail criteria
- [ ] **Diagrams Included**: Schematics and flowcharts
- [ ] **Appendix Complete**: Supporting info added
- [ ] **Spell Check**: No typos or errors
- [ ] **Technical Review**: Reviewed by senior engineer
- [ ] **Format Check**: Word document opens correctly

---

## 📞 Need Help?

### Quick Reference

- **Full Documentation**: See `SOP_GENERATOR_README.md`
- **Code Issues**: Check `sop_generator_complete.py` comments
- **Dependencies**: See `requirements.txt`

### Common Questions

**Q: How many SOPs can I create?**
A: Unlimited! Limited only by browser memory.

**Q: Can I edit an existing SOP?**
A: Currently, download the Word document, edit, and create new revision.

**Q: Can I use my own logo?**
A: Yes! Upload any PNG/JPG company logo.

**Q: Is my data saved?**
A: Data is saved in browser session. Export to JSON to save permanently.

**Q: Can I share SOPs with colleagues?**
A: Yes! Download Word/PDF and share via email or network drive.

**Q: Which export format is best?**
A: **Word (.docx)** for editing, **PDF** for final distribution.

---

## 🎓 Learn More

### Recommended Reading

**IEC Standards**:
- IEC 61215 series - PV Module Qualification
- IEC 61730 series - PV Module Safety
- IEC 60904 series - PV Device Measurements

**ISO/IEC 17025**:
- Understanding accreditation requirements
- Document control procedures
- Quality management systems

**Solar PV Testing**:
- NREL PV Performance Modeling Collaborative
- Sandia PV Reliability Database
- PVEL PV Module Reliability Scorecard

---

## 🚀 Next Steps

After creating your first SOP:

1. **Create More SOPs**: Build complete procedure library
2. **Set Up Workflow**: Configure approval workflow
3. **Train Team**: Share SOPs with lab staff
4. **Quality Review**: Have senior engineer review
5. **Implement**: Use SOPs in daily testing
6. **Improve**: Gather feedback and create revisions
7. **Accreditation**: Submit for ISO/IEC 17025 if applicable

---

**Ready to create professional SOPs? Let's get started!** 🚀☀️

---

*Last Updated: 2024 | For Support: Contact Lab IT Administrator*
