from typing import List

from typing_extensions import override

from skill_interface import SkillInterface


class DirectSkillMatch(SkillInterface):
    @override
    def skill_match(self, user_skills: List[str], skills_to_match: List[str]) -> float:
        matched_skills = 0
        for skill in user_skills:
            if skill.lower() in map(lambda x: x.lower(), skills_to_match):
                matched_skills += 1

        return round((matched_skills / len(skills_to_match)) * 100, 2)