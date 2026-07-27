ROADMAP_TOPICS = {
    "python": "Study Python syntax, functions, OOP and error handling.",
    "sql": "Learn SELECT, JOIN, GROUP BY, subqueries and window functions.",
    "excel": "Practise formulas, pivot tables, charts and data cleaning.",
    "pandas": "Learn DataFrames, filtering, grouping, merging and missing values.",
    "power bi": "Build dashboards using Power Query, DAX and visualisations.",
    "statistics": "Study probability, distributions, hypothesis tests and regression.",
    "machine learning": "Learn preprocessing, training, validation and evaluation.",
    "scikit-learn": "Build classification and regression pipelines.",
    "deep learning": "Study neural networks, backpropagation and model training.",
    "tensorflow": "Build and train neural networks using TensorFlow and Keras.",
    "pytorch": "Learn tensors, datasets, training loops and neural networks.",
    "nlp": "Study tokenisation, text classification and language models.",
    "spacy": "Practise tokenisation, entity recognition and phrase matching.",
    "transformers": "Learn pretrained transformer models and fine-tuning.",
    "hugging face": "Use Hugging Face pipelines, tokenizers and models.",
    "fastapi": "Build and test REST APIs for Python applications.",
    "docker": "Learn images, containers, Dockerfiles and deployment.",
    "mlflow": "Track experiments, models and metrics using MLflow.",
    "aws": "Learn cloud storage, computing and basic deployment.",
    "azure": "Learn Azure services and deploy a small application.",
    "opencv": "Practise image loading, transformation and detection.",
    "cnn": "Learn convolution, pooling and image classification.",
    "yolo": "Build a basic object-detection project.",
    "git": "Learn commits, branches, merges and remote repositories.",
    "github": "Upload projects and maintain README documentation.",
}


def generate_roadmap(
    missing_skills: list[str],
    maximum_weeks: int = 4,
) -> list[dict[str, str]]:
    """Generate one learning topic for each of the first missing skills."""
    roadmap = []

    for week, skill in enumerate(
        missing_skills[:maximum_weeks],
        start=1,
    ):
        topic = ROADMAP_TOPICS.get(
            skill.lower(),
            f"Study the fundamentals of {skill} and complete a small project.",
        )

        roadmap.append(
            {
                "week": f"Week {week}",
                "skill": skill.title(),
                "topic": topic,
            }
        )

    return roadmap