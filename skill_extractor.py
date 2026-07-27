import re

import pandas as pd


def load_skill_dictionary(
    file_path: str = "data/skill_dictionary.csv",
) -> pd.DataFrame:
    """Load the controlled skill dictionary."""
    skills_df = pd.read_csv(file_path)

    skills_df["skill"] = (
        skills_df["skill"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return skills_df


def skill_exists(skill: str, text: str) -> bool:
    """Check for a skill using safe text boundaries."""
    escaped_skill = re.escape(skill)

    pattern = rf"(?<![a-z0-9]){escaped_skill}(?![a-z0-9])"

    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(
    cleaned_text: str,
    file_path: str = "data/skill_dictionary.csv",
) -> list[str]:
    """Return skills found in the cleaned resume text."""
    skills_df = load_skill_dictionary(file_path)

    detected_skills = []

    for skill in skills_df["skill"]:
        if skill_exists(skill, cleaned_text):
            detected_skills.append(skill)

    return sorted(set(detected_skills))


def group_skills(
    detected_skills: list[str],
    file_path: str = "data/skill_dictionary.csv",
) -> dict[str, list[str]]:
    """Group detected skills according to their categories."""
    skills_df = load_skill_dictionary(file_path)

    grouped = {}

    for _, row in skills_df.iterrows():
        skill = row["skill"]
        category = row["category"]

        if skill in detected_skills:
            grouped.setdefault(category, []).append(skill)

    return grouped