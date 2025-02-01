from typing import List


class SkillInterface:
    def skill_match(self, user_skills: List[str], skills_to_match: List[str]) -> float:
        raise NotImplementedError