from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent
JOB_ROLES_FILE = BASE_DIR / "data" / "job_roles.csv"


def load_job_roles(file_path=None):
    if file_path is None:
        file_path = JOB_ROLES_FILE

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"job_roles.csv was not found at: {file_path}"
        )

    jobs_df = pd.read_csv(file_path)

    required_columns = {"job_role", "required_skills"}

    if not required_columns.issubset(jobs_df.columns):
        raise ValueError(
            "job_roles.csv must contain the columns "
            "'job_role' and 'required_skills'."
        )

    jobs_df["job_role"] = (
        jobs_df["job_role"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    jobs_df["required_skills"] = (
        jobs_df["required_skills"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return jobs_df


def calculate_role_matches(resume_text, file_path=None):
    jobs_df = load_job_roles(file_path)

    if not resume_text or not resume_text.strip():
        results = jobs_df.copy()
        results["match_score"] = 0.0
        return results

    documents = [
        resume_text
    ] + jobs_df["required_skills"].tolist()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    vectors = vectorizer.fit_transform(documents)

    resume_vector = vectors[0:1]
    role_vectors = vectors[1:]

    similarity_scores = cosine_similarity(
        resume_vector,
        role_vectors,
    ).flatten()

    results = jobs_df.copy()

    results["match_score"] = (
        similarity_scores * 100
    ).round(2)

    return results.sort_values(
        by="match_score",
        ascending=False,
    ).reset_index(drop=True)


def get_role_requirements(role_name, file_path=None):
    jobs_df = load_job_roles(file_path)

    selected_role = jobs_df[
        jobs_df["job_role"].str.lower()
        == role_name.lower().strip()
    ]

    if selected_role.empty:
        return []

    skills_text = selected_role.iloc[0]["required_skills"]

    return [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]


def calculate_skill_coverage(
    detected_skills,
    required_skills,
):
    detected_set = {
        skill.lower().strip()
        for skill in detected_skills
    }

    required_set = {
        skill.lower().strip()
        for skill in required_skills
    }

    found_skills = sorted(
        required_set.intersection(detected_set)
    )

    missing_skills = sorted(
        required_set.difference(detected_set)
    )

    if not required_set:
        coverage_score = 0.0
    else:
        coverage_score = round(
            len(found_skills)
            / len(required_set)
            * 100,
            2,
        )

    return (
        found_skills,
        missing_skills,
        coverage_score,
    )