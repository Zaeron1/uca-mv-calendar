import requests

UCA_URL = "https://edt.uca.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=17227,17226,15732,15724,10397,10385,10384,7652&projectId=3&calType=ical&nbWeeks=8&displayConfigId=128"
OUTPUT_FILE = "ADE_UCA_MV_filtré.ics"

response = requests.get(UCA_URL)
lines = response.text.splitlines()

filtered_events = []
current_event = []
in_event = False

for line in lines:
    if line.startswith("BEGIN:VEVENT"):
        in_event = True
        current_event = [line]
    elif line.startswith("END:VEVENT"):
        current_event.append(line)
        in_event = False
        event_text = '\n'.join(current_event)
        if "MV" in event_text:
            filtered_events.extend(current_event)
    elif in_event:
        current_event.append(line)

# En-tête et pied
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

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write('\n'.join(header + filtered_events + footer))
