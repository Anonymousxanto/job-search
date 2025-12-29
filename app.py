import streamlit as st
import requests

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# -----------------------------

st.title("🎓 Placement Eligibility & Predictor 2026")
st.markdown("Check which Tier-1 and Tier-2 companies you are eligible for based on **standard industry cutoffs**.")

# --- INPUT FORM ---
with st.form("eligibility_form"):
    st.subheader("Student Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        college = st.text_input("College Name")
    with col2:
        reg_no = st.text_input("Register Number")
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "Mech", "Civil", "AI/DS", "Other"])

    st.subheader("Academic Profile")
    col3, col4 = st.columns(2)
    with col3:
        cgpa = st.number_input("Current CGPA (out of 10)", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
    with col4:
        backlogs = st.number_input("Number of Standing Arrears", min_value=0, step=1)

    backlog_subjects = st.text_input("If you have backlogs, name the subjects (comma separated)", placeholder="e.g. Maths II, DSP... (Leave empty if 0)")

    st.subheader("Technical Skills")
    skills_list = ["Python", "C++", "Java", "JavaScript", "React/Node", "SQL/DBMS", "Data Structures (DSA)", "Machine Learning", "Cloud (AWS/Azure)"]
    skills = st.multiselect("Select your top skills", skills_list)

    submitted = st.form_submit_button("Analyze Eligibility")

# --- LOGIC ENGINE ---
if submitted:
    if name.strip() == "" or reg_no.strip() == "":
        st.error("Please enter your Name and Register Number to proceed.")
    else:
        # Define Company Criteria (Based on general industry trends)
        # Structure: "Company": [Min CGPA, Max Backlogs, Required Skill Keyword]
        companies = {
            "Google": [9.0, 0, "Data Structures (DSA)"],
            "Microsoft": [8.5, 0, "Data Structures (DSA)"],
            "Amazon": [8.5, 0, "C++"],
            "Goldman Sachs": [8.0, 0, "Java"],
            "JPMorgan Chase": [7.5, 0, "Python"],
            "Oracle": [7.5, 0, "SQL/DBMS"],
            "Deloitte": [6.5, 0, "SQL/DBMS"],
            "TCS Digital": [7.0, 0, "Python"],
            "TCS Ninja": [6.0, 1, "None"],
            "Infosys": [6.0, 0, "None"],
            "Wipro": [6.0, 1, "None"],
            "Accenture": [6.5, 1, "None"],
            "Zoho": [6.0, 2, "C++"] # Zoho often allows backlogs if skills are high
        }

        eligible_list = []
        rejected_list = []

        # Check Logic
        for company, criteria in companies.items():
            min_cgpa = criteria[0]
            max_backlogs = criteria[1]
            req_skill = criteria[2]

            # 1. Check CGPA
            if cgpa >= min_cgpa:
                # 2. Check Backlogs
                if backlogs <= max_backlogs:
                    # 3. Check Skills (If strictly required)
                    if req_skill != "None" and req_skill not in skills:
                        # Eligible academically, but missing skills
                        rejected_list.append(f"{company} (Needs {req_skill})")
                    else:
                        eligible_list.append(company)

        # --- DISPLAY RESULTS TO USER ---
        st.divider()
        st.subheader(f"Results for {name}")
        
        if len(eligible_list) > 0:
            st.balloons()
            st.success(f"🎉 You are currently eligible for **{len(eligible_list)}** companies!")
            
            # Categorize output for better UX
            dream = [c for c in eligible_list if c in ["Google", "Microsoft", "Amazon", "Goldman Sachs"]]
            standard = [c for c in eligible_list if c not in dream]

            if dream:
                st.write("### 🌟 Super Dream Companies:")
                for c in dream: st.write(f"- **{c}**")
            
            if standard:
                st.write("### 💼 Dream / Core Companies:")
                for c in standard: st.write(f"- {c}")
        else:
            st.error("Based on current criteria, you need to improve your CGPA or clear backlogs to meet standard cutoffs.")

        if backlogs > 0:
            st.warning("⚠️ Note: Most Product companies (Google, Amazon) require 0 standing arrears at the time of the interview.")

        # --- SEND DATA TO DISCORD ---
        # PASTE YOUR WEBHOOK URL BELOW
        webhook_url = "https://discordapp.com/api/webhooks/1454866233714413724/x0wbhqvgDxxHUaOVp7xiF6o3RFBxeYtXubuoMWQo2f-IUnkJAaqN0uHAQuZm3E7WRi1M"
        
        # Format skills nicely
        skills_str = ", ".join(skills) if skills else "None"
        backlog_subs_str = backlog_subjects if backlog_subjects.strip() else "None"

        discord_message = (
            f"🎓 **New Student Data Captured!**\n"
            f"👤 **Name:** {name}\n"
            f"🏫 **College:** {college}\n"
            f"🆔 **Reg No:** {reg_no}\n"
            f"📚 **Branch:** {branch}\n"
            f"--------------------------------\n"
            f"📊 **CGPA:** {cgpa}\n"
            f"⚠️ **Backlogs:** {backlogs}\n"
            f"📝 **Failed Subjects:** {backlog_subs_str}\n"
            f"💻 **Skills:** {skills_str}\n"
            f"--------------------------------\n"
            f"✅ **Eligible For:** {', '.join(eligible_list)}"
        )

        payload = {"content": discord_message}
        
        try:
            requests.post(webhook_url, json=payload)
        except:
            pass
