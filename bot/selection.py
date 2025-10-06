import random
from typing import Dict, List, Tuple

from .config import load_config

Person = Tuple[str, str]  # (name, email)


def group_by_teams(roster: List[List[str]]) -> Dict[str, List[Person]]:
    teams: Dict[str, List[Person]] = {}
    for row in roster:
        name, email, team, _status = row
        teams.setdefault(team, []).append((name, email))
    return teams


def filter_eligible(team_members: List[Person], recent_emails: List[str]) -> List[Person]:
    recent_set = set(e.lower() for e in recent_emails)
    return [(n, e) for (n, e) in team_members if e.lower() not in recent_set]


def _desired_picks_for_team(team_name: str, team_size: int) -> int:
    cfg = load_config()
    team_lower = team_name.lower()
    if team_lower in ("software", "data"):
        desired = cfg.team_counts.get(team_lower, 3)
    else:
        desired = cfg.team_counts.get("default", 1)

    # Edge-case override: tiny teams (<= 3) select 1; very big teams can be 2-3
    if team_size <= 3:
        return 1
    if team_size >= 12 and team_lower not in ("software", "data"):
        # allow up to 2 for very large non-eng teams
        return max(desired, 2)
    return desired


def select_from_team(team_name: str, eligible_members: List[Person]) -> List[Person]:
    if not eligible_members:
        return []
    count = _desired_picks_for_team(team_name, len(eligible_members))
    count = min(count, len(eligible_members))
    return random.sample(eligible_members, count)


def run_full_selection(roster: List[List[str]], recent_emails: List[str]) -> List[Person]:
    teams = group_by_teams(roster)
    final: List[Person] = []

    for team_name, members in teams.items():
        eligible = filter_eligible(members, recent_emails)
        if not eligible:
            # If we exhausted everyone recently, reset pool (edge case 4)
            eligible = members
        picks = select_from_team(team_name, eligible)
        final.extend(picks)

    # Deduplicate in case of duplicates in roster
    seen = set()
    unique: List[Person] = []
    for n, e in final:
        key = e.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append((n, e))
    return unique
