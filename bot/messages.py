from .config import load_config

INITIAL_TEMPLATE = (
    "Hey {name}! You were randomly selected from the Community team to share quick feedback this week.\n"
    "It takes less than 30 seconds. Please fill this by Friday 5pm:\n\n"
    "{form_url}\n\n"
    "React with 👍 to this message after you're done so the bot can check you off. If you don't do it, I will track you down! 😤\n\n"
    "You won't be selected again until your whole team has done it. Thanks!"
)

FIRST_REMINDER_TEMPLATE = (
    "Friendly reminder for {team} feedback — could you fill this by Friday 5pm?\n{form_url}"
)

FINAL_REMINDER_TEMPLATE = (
    "Final reminder — today is the deadline for this week’s {team} feedback.\n{form_url}\n"
    "Appreciate your help!"
)

def render_initial(name: str, team: str) -> str:
    cfg = load_config()
    return INITIAL_TEMPLATE.format(name=name, team=team.capitalize(), form_url=cfg.form_url)


def render_first_reminder(team: str) -> str:
    cfg = load_config()
    return FIRST_REMINDER_TEMPLATE.format(team=team.capitalize(), form_url=cfg.form_url)


def render_final_reminder(team: str) -> str:
    cfg = load_config()
    return FINAL_REMINDER_TEMPLATE.format(team=team.capitalize(), form_url=cfg.form_url)
