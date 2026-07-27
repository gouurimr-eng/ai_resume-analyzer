import pandas as pd
import plotly.express as px
import streamlit as st

from job_matcher import (
    calculate_role_matches,
    calculate_skill_coverage,
    get_role_requirements,
    load_job_roles,
)
from resume_parser import extract_resume_text
from roadmap_generator import generate_roadmap
from skill_extractor import extract_skills, group_skills
from text_cleaner import clean_text


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("AI Resume Analyzer and Job Recommendation System")

st.info(
    "This application provides educational guidance. "
    "Its scores are estimates and should not be used for automatic hiring decisions."
)

jobs_df = load_job_roles()

selected_role = st.selectbox(
    "Select your target job role",
    jobs_df["job_role"].tolist(),
)

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
)

if uploaded_file is not None:
    try:
        with st.spinner("Analyzing your resume..."):
            raw_text = extract_resume_text(uploaded_file)
            cleaned_text = clean_text(raw_text)

            if not cleaned_text:
                st.error(
                    "No readable text was found. "
                    "The resume may be scanned or image-based."
                )
                st.stop()

            detected_skills = extract_skills(cleaned_text)
            grouped_skills = group_skills(detected_skills)

            role_matches = calculate_role_matches(cleaned_text)

            required_skills = get_role_requirements(selected_role)

            found_skills, missing_skills, skill_coverage = (
                calculate_skill_coverage(
                    detected_skills,
                    required_skills,
                )
            )

            selected_result = role_matches[
                role_matches["job_role"] == selected_role
            ]

            if selected_result.empty:
                selected_match_score = 0.0
            else:
                selected_match_score = float(
                    selected_result.iloc[0]["match_score"]
                )

        st.success(f"Uploaded file: {uploaded_file.name}")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Target-role text match",
            f"{selected_match_score:.2f}%",
        )

        col2.metric(
            "Required-skill coverage",
            f"{skill_coverage:.2f}%",
        )

        col3.metric(
            "Skills detected",
            len(detected_skills),
        )

        st.subheader("Extracted skills")

        if grouped_skills:
            for category, skills in grouped_skills.items():
                st.write(
                    f"**{category}:** "
                    + ", ".join(skill.title() for skill in skills)
                )
        else:
            st.warning(
                "No skills from the current skill dictionary were detected."
            )

        st.subheader("Top recommended roles")

        top_roles = role_matches.head(3).copy()

        st.dataframe(
            top_roles[["job_role", "match_score"]],
            use_container_width=True,
            hide_index=True,
        )

        chart = px.bar(
            top_roles,
            x="job_role",
            y="match_score",
            labels={
                "job_role": "Job role",
                "match_score": "Match score (%)",
            },
            title="Top three role-match scores",
        )

        st.plotly_chart(chart, use_container_width=True)

        left, right = st.columns(2)

        with left:
            st.subheader("Required skills found")

            if found_skills:
                for skill in found_skills:
                    st.write(f"✅ {skill.title()}")
            else:
                st.write("No required skills were directly found.")

        with right:
            st.subheader("Missing skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"❌ {skill.title()}")
            else:
                st.write("No listed skills are missing.")

        st.subheader("Suggested learning roadmap")

        roadmap = generate_roadmap(missing_skills)

        if roadmap:
            roadmap_df = pd.DataFrame(roadmap)
            st.dataframe(
                roadmap_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success(
                "Your resume contains all skills currently listed "
                "for this role."
            )

        with st.expander("View extracted resume text"):
            st.text_area(
                "Resume text",
                raw_text,
                height=300,
            )

    except Exception as error:
        st.error(f"Resume analysis failed: {error}")

else:
    st.write(
        "Upload a PDF or DOCX resume to start the analysis."
    )