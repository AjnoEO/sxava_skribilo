from PIL import Image
from pathlib import Path
import json
#from functools import lru_cache

with open("datumoj.json", mode="r", encoding="utf-8") as dosiero:
	datumoj = json.load(dosiero)
	UNIKODO = datumoj['Unikodo']
	BARARO = datumoj['Baroj']
	LITERARO = list(BARARO) + [" "]

with open("koloroj.json", mode="r", encoding="utf-8") as dosiero:
	KOLOROJ = json.load(dosiero)

TEKSTOALTO = 360
SPACETLARĜO = 70
FORIGENDA_INTERSPACO = 0
LETERA_INTERPSPACO = 25
PLENBARO = [1, 2, 3, 4]
PLEJ_LONGA_KOMBINAĴO = max(map(len, LITERARO))

def leterbildo(letero: str):
	return Image.open("literoj/" + letero + ".png")

def komunaj_elementoj(listo1, listo2):
	for el in listo1:
		if el in listo2:
			return True
	return False

def aldoni(tekstobildo, baroj, nova_litero: str):
	if nova_litero == " ":
		nova_bildo = Image.new("RGBA", (tekstobildo.size[0] + SPACETLARĜO, TEKSTOALTO))
		nova_bildo.paste(tekstobildo)
		return (nova_bildo, PLENBARO)
	novliteraj_baroj = BARARO[nova_litero]
	novlitera_bildo = leterbildo(nova_litero)
	nova_larĝo = tekstobildo.size[0] + novlitera_bildo.size[0] - FORIGENDA_INTERSPACO
	if not komunaj_elementoj(baroj, novliteraj_baroj["Maldekstre"]):
		nova_larĝo -= LETERA_INTERPSPACO
	nova_bildo = Image.new("RGBA", (nova_larĝo, TEKSTOALTO))
	nova_bildo.paste(tekstobildo)	
	nova_bildo.alpha_composite(novlitera_bildo, dest=(nova_larĝo - novlitera_bildo.size[0], 0))
	return (nova_bildo, novliteraj_baroj["Dekstre"])

print("Entajpu la konvertendan tekston")
konvertota = input().lower()
rezulto = ''
for simb in konvertota:
	rezulto += UNIKODO[simb] if simb in UNIKODO else simb
print(rezulto)

tekstobildo = Image.new("RGBA", (FORIGENDA_INTERSPACO, TEKSTOALTO))
baroj = PLENBARO
simboloj = list(konvertota)
i = len(simboloj)
while i > 0:
	for kombinaĵlongo in range(PLEJ_LONGA_KOMBINAĴO, -1, -1):
		if i - kombinaĵlongo < 0: continue
		if kombinaĵlongo == 0:
			raise ValueError("Nekonvertebla simbolo: «" + konvertota[i - 1] + "»")
		if "".join(simboloj[i - kombinaĵlongo : i]) in LITERARO:
			simboloj = simboloj[:i - kombinaĵlongo] + ["".join(simboloj[i - kombinaĵlongo : i])] + simboloj[i:]
			i = i - kombinaĵlongo
			break
for simb in simboloj:
	tekstobildo, baroj = aldoni(tekstobildo, baroj, simb)
print("Koloro")
koloro = input().lower()
if koloro in KOLOROJ or (koloro[-1] == 'o' and koloro[:-1] + 'a' in KOLOROJ): koloro = KOLOROJ[koloro[:-1] + 'a']
kolorbildo = Image.new("RGB", tekstobildo.size, koloro)
tekstobildo = Image.merge("RGBA", (kolorbildo.getchannel("R"), kolorbildo.getchannel("G"), kolorbildo.getchannel("B"), tekstobildo.getchannel("A")))
dosierujo = "rezultoj"
Path(dosierujo).mkdir(parents=True, exist_ok=True)
tekstobildo.save(dosierujo + "/" + konvertota.replace(" ", "_") + ".png")