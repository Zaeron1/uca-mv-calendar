import requests
import os
from git import Repo
from datetime import datetime

# === PARAMÈTRES ===
uca_url = "https://edt.uca.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=17227,17226,15732,15724,10397,10385,10384,7652&projectId=3&calType=ical&nbWeeks=8&displayConfigId=128"
repo_path = "uca-mv-calendar"  # chemin local vers ton dépôt cloné
output_filename = "index.ics"
github_username = "Zaeron1"
github_token = "ghp_xxxxxxxxxxxxxxxxxxxxxx"  # Ton token GitHub

# === TÉLÉCHARGER ICS ===
response = requests.get(uca_url)
lines = response.text.splitlines()

# === FILTRER EVENEMENTS MV ===
filtered_events = []
event = []
in_event = False

for line in lines:
    if line.startswith("BEGIN:VEVENT"):
        in_event = True
        event = [line]
    elif line.startswith("END:VEVENT"):
        event.append(line)
        in_event = False
        block = "\n".join(event)
        if "MV" in block:
            filtered_events.extend(event)
    elif in_event:
        event.append(line)

# === HEADER / FOOTER ===
header = []
footer = []
in_header = True
for line in lines:
    if line.startswith("BEGIN:VEVENT"):
        in_header = False
    if in_header:
        header.append(line)
    if line.startswith("END:VCALENDAR"):
        footer.append(line)
        break

# === ÉCRITURE ===
final_content = "\n".join(header + filtered_events + footer)
output_path = os.path.join(repo_path, output_filename)
os.makedirs(repo_path, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("✅ Calendrier filtré écrit :", output_path)

# === PUSH AUTOMATIQUE ===
repo = Repo(repo_path)
repo.git.add(output_filename)
repo.index.commit(f"Update MV calendar - {datetime.now().isoformat()}")
repo.remote().set_url(f"https://{github_username}:{github_token}@github.com/{github_username}/uca-mv-calendar.git")
repo.git.push("origin", "gh-pages")

print("🌍 Calendrier en ligne :")
print(f"https://{github_username}.github.io/uca-mv-calendar/{output_filename}")