import json, ziafont

with open("datumoj.json", mode="r", encoding="utf-8") as f:
	data = json.load(f)
	UNICODE = data['Unikodo']

font = ziafont.Font('seguihis.ttf')

for letter in UNICODE:
	print('>', letter)
	with open(f"literoj/{letter}.svg", mode="w", encoding="utf-8") as f:
		f.write(font.text(UNICODE[letter]).svg())
	print(f'  La litero «{letter}» aldoniĝis')
