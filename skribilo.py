from PIL import Image
import os
from pathlib import Path
import json
#from functools import lru_cache

TEKSTOALTO = 80
SPACETLARĜO = 20
FORIGENDA_INTERSPACO = 5
LETERA_INTERPSPACO = 10
PLENBARO = [1, 2, 3, 4]
PLEJ_LONGA_KOMBINAĴO = 3

def leterbildo(letero: str):
	return Image.open("literoj/" + letero + ".svg")

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

with open("datumoj.json", mode="r", encoding="utf-8") as dosiero:
	datumoj = json.load(dosiero)
	UNIKODO = datumoj['Unikodo']
	BARARO = datumoj['Baroj']
	LITERARO = list(BARARO) + [" "]

print("Entajpu la konvertendan tekston")
konvertota = input()
konvertota = konvertota.lower()
rezulto = ''
for simb in konvertota:
	rezulto += UNIKODO[simb] if simb in UNIKODO else simb
print(rezulto)

tekstobildo = Image.new("RGBA", (FORIGENDA_INTERSPACO, TEKSTOALTO))
baroj = PLENBARO
i = 0
while i < len(konvertota):
	for kombinaĵlongo in range(PLEJ_LONGA_KOMBINAĴO, -1, -1):
		if i + kombinaĵlongo > len(konvertota): continue
		if kombinaĵlongo == 0:
			raise ValueError("Nekonvertebla simbolo: «" + konvertota[i] + "»")
		if konvertota[i : i + kombinaĵlongo] in LITERARO:
			tekstobildo, baroj = aldoni(tekstobildo, baroj, konvertota[i : i + kombinaĵlongo])
			i += kombinaĵlongo
			break
print("Koloro")
koloro = input()
kolorbildo = Image.new("RGB", tekstobildo.size, koloro)
tekstobildo = Image.merge("RGBA", (kolorbildo.getchannel("R"), kolorbildo.getchannel("G"), kolorbildo.getchannel("B"), tekstobildo.getchannel("A")))
#dosierujo = os.getcwd() + "/rezultoj"
dosierujo = "rezultoj"
Path(dosierujo).mkdir(parents=True, exist_ok=True)
tekstobildo.save(dosierujo + "/" + konvertota.replace(" ", "_") + ".png")