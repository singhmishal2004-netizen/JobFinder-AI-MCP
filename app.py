import streamlit as st

from src.helper import extract_text_from_pdf, ask_groq
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs


# =========================
# Streamlit Configuration
# =========================

st.set_page_config(
    page_title="Job Recommender",
    layout="wide"
)

st.title("📄 AI Job Recommender")

st.markdown(
    "Upload your resume and get job recommendations based on your "
    "skills and experience from LinkedIn and Naukri."
)


# =========================
# Upload Resume
# =========================

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)


if uploaded_file:

    # =========================
    # Extract Resume Text
    # =========================

    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)


    # =========================
    # Resume Summary
    # =========================

    with st.spinner("Summarizing your resume..."):

        summary = ask_groq(
            f"""
Summarize this resume highlighting the skills, education, and experience.

Resume:
{resume_text}
""",
            max_tokens=500
        )


    # =========================
    # Skill Gap Analysis
    # =========================

    with st.spinner("Finding skill gaps..."):

        gaps = ask_groq(
            f"""
Analyze this resume and highlight missing skills, certifications,
and experiences needed for better job opportunities.

Resume:
{resume_text}
""",
            max_tokens=400
        )


    # =========================
    # Future Roadmap
    # =========================

    with st.spinner("Creating Future Roadmap..."):

        roadmap = ask_groq(
            f"""
Based on this resume, suggest a future roadmap to improve this
person's career prospects.

Include:
- Skills to learn
- Certifications needed
- Industry exposure

Resume:
{resume_text}
""",
            max_tokens=400
        )


    # =========================
    # Display Resume Summary
    # =========================

    st.markdown("---")

    st.header("📑 Resume Summary")

    st.markdown(
        f"""
        <div style="
            background-color: #000000;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            color: white;
        ">
        {summary}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # Display Skill Gaps
    # =========================

    st.markdown("---")

    st.header("🛠️ Skill Gaps & Missing Areas")

    st.markdown(
        f"""
        <div style="
            background-color: #000000;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            color: white;
        ">
        {gaps}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================
    # Display Roadmap
    # =========================

    st.markdown("---")

    st.header("🚀 Future Roadmap & Preparation Strategy")

    st.markdown(
        f"""
        <div style="
            background-color: #000000;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            color: white;
        ">
        {roadmap}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.success("✅ Analysis Completed Successfully!")


    # =========================
    # Job Recommendations
    # =========================

    if st.button("🔎 Get Job Recommendations"):

        with st.spinner("Finding suitable job keywords..."):

            keywords = ask_groq(
                f"""
Extract up to 5 accurate job-search terms from the candidate's
documented experience. Use the resume summary to understand the
candidate and the extracted resume text to verify every term.

Prioritize realistic job titles supported by the candidate's actual
work, then include only important skills explicitly present in the
resume. Do not infer skills, seniority, industries, or certifications
that are not supported by the text. Remove duplicates and generic
terms. Return only a comma-separated list of up to 5 short terms.

Resume summary:
{summary}

Extracted resume text:
{resume_text}
""",
                max_tokens=500,
                reasoning_effort="low"
            )


        search_keywords_clean = (keywords or "").replace("\n", ", ").strip(" ,\t")

        if not search_keywords_clean:
            with st.spinner("Retrying keyword extraction..."):
                keywords = ask_groq(
                    f"""
Extract up to 5 job titles or search keywords from this resume.
Return only a comma-separated list, for example: Data Analyst,
Python Developer, SQL.

Resume:
{resume_text}
""",
max_tokens=500,
reasoning_effort="low"
                )
            search_keywords_clean = (keywords or "").replace(
                "\n", ", "
            ).strip(" ,\t")

        if not search_keywords_clean:
            st.error(
                "Keyword extraction returned no text after a retry. "
                "Please try again; "
                "the job search was not started."
            )
            st.stop()

        st.success(
            f"Extracted Job Keywords: {search_keywords_clean}"
        )


        # =========================
        # Fetch Jobs
        # =========================

        with st.spinner(
            "Fetching jobs from LinkedIn and Naukri..."
        ):

            linkedin_jobs = fetch_linkedin_jobs(
                search_keywords_clean,
                rows=60
            )

            naukri_jobs = fetch_naukri_jobs(
                search_keywords_clean,
                rows=60
            )


        # =========================
        # LinkedIn Jobs
        # =========================

        st.markdown("---")

        st.header("💼 Top LinkedIn Jobs")

        if linkedin_jobs:

            for job in linkedin_jobs:

                st.markdown(
                    f"**{job.get('title')}** "
                    f"at *{job.get('companyName')}*"
                )

                st.markdown(
                    f"- 📍 {job.get('location')}"
                )

                st.markdown(
                    f"- 🔗 [View Job]({job.get('link')})"
                )

                st.markdown("---")

        else:

            st.warning("No LinkedIn jobs found.")


        # =========================
        # Naukri Jobs
        # =========================

        st.markdown("---")

        st.header("💼 Top Naukri Jobs (India)")

        if naukri_jobs:

            for job in naukri_jobs:

                st.markdown(
                    f"**{job.get('title')}** "
                    f"at *{job.get('companyName')}*"
                )

                st.markdown(
                    f"- 📍 {job.get('location')}"
                )

                st.markdown(
                    f"- 🔗 [View Job]({job.get('url')})"
                )

                st.markdown("---")

        else:

            st.warning("No Naukri jobs found.")