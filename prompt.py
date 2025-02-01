def get_prompt() -> str:
    fields_to_extract = ["candidate_name", "professional_experience_start_date", "year_of_graduation",
                         "candidate_skills"]

    response_format = {
        "candidate_name": "John Doe",
        "professional_experience_start_date": "2024-01-01",
        "year_of_graduation": "2021",
        "candidate_skills": ["skill1", "skill2", "skill3"]
    }

    prompt_message = f"""
    You are an expert resume screening agent whose role is to extract important fields from any given user resume.
    The fields that you need to extract should be properly formatted in a json format.
    The fields that you need to extract are: {fields_to_extract}.
    The response format should look like:
    {response_format}
    ---
    Resume below:
    """

    return prompt_message