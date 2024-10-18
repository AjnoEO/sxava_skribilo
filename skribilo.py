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
	KOLOROJ: dict[str, str] = json.load(dosiero)

TEKSTOALTO = 360
SPACETLARĜO = 70
FORIGENDA_INTERSPACO = 0
LETERA_INTERPSPACO = 25
LINIA_INTERSPACO = 200
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

def unikodigi(teksto: str):
	teksto = teksto.lower()
	rezulto = ''
	for simb in teksto:
		rezulto += UNIKODO[simb] if simb in UNIKODO else simb
	return rezulto

def koloro(nomo: str | None = None):
	if not nomo:
		return KOLOROJ['nigra']
	nomo = nomo.lower()
	if nomo[-1] in {'o', 'a'} and (nomo[:-1] + 'a') in KOLOROJ:
		return KOLOROJ[nomo[:-1] + 'a']
	raise Warning(f'Nekonata koloro: {nomo}')

def bildigi(teksto: str, koloro: str, ĝisrandigo: int = 1, larĝolimo: int | None = None):
	"""
	ĝisrandigo: maldekstrigi = 0, centrigi = 1, dekstrigi = 2
	"""
	teksto = teksto.lower()
	tekstobildo = Image.new("RGBA", (FORIGENDA_INTERSPACO, TEKSTOALTO))
	lasta_tekstobildo = None
	bildaro: list[Image.Image] = []
	baroj = PLENBARO
	simboloj = list(teksto)
	i = len(simboloj)
	while i > 0:
		for kombinaĵlongo in range(PLEJ_LONGA_KOMBINAĴO, -1, -1):
			if i - kombinaĵlongo < 0: continue
			if kombinaĵlongo == 0:
				raise ValueError(f"Nekonvertebla simbolo: «{teksto[i - 1]}»")
			if "".join(simboloj[i - kombinaĵlongo : i]) in LITERARO:
				simboloj = simboloj[:i - kombinaĵlongo] + ["".join(simboloj[i - kombinaĵlongo : i])] + simboloj[i:]
				i = i - kombinaĵlongo
				break
	i = 0
	lasta_i = 0
	while True:
		if i == len(simboloj):
			if larĝolimo and tekstobildo.width > larĝolimo and not lasta_tekstobildo:
				longa_vorto = "".join(simboloj[lasta_i:i])
				raise OverflowError(f"La larĝo ne estis sufiĉa por la vorto «{longa_vorto}»")
			bildaro.append(tekstobildo)
			break
		simb = simboloj[i]
		i += 1
		if i < len(simboloj) and simb != ' ':
			tekstobildo, baroj = aldoni(tekstobildo, baroj, simb)
			continue
		if larĝolimo and tekstobildo.width > larĝolimo:
			if not lasta_tekstobildo:
				longa_vorto = "".join(simboloj[lasta_i:i])
				raise OverflowError(f"La larĝo ne estis sufiĉa por la vorto «{longa_vorto}»")
			bildaro.append(lasta_tekstobildo)
			tekstobildo = Image.new("RGBA", (FORIGENDA_INTERSPACO, TEKSTOALTO))
			baroj = PLENBARO
			i = lasta_i
			lasta_tekstobildo = None
		else:
			lasta_tekstobildo = tekstobildo
			tekstobildo, baroj = aldoni(tekstobildo, baroj, simb)
			lasta_i = i
	larĝo = max(map(lambda b: b.width, bildaro))
	alto = TEKSTOALTO * len(bildaro) - LINIA_INTERSPACO * (len(bildaro) - 1)
	tekstobildo = Image.new("RGBA", (larĝo, alto))
	for i, bildo in enumerate(bildaro):
		x = 0 + round((larĝo - bildo.width) * (ĝisrandigo / 2))
		tekstobildo.alpha_composite(bildo, (x, i*(TEKSTOALTO-LINIA_INTERSPACO)))
	kolorbildo = Image.new("RGB", tekstobildo.size, koloro)
	tekstobildo = Image.merge(
		"RGBA",
		(kolorbildo.getchannel("R"), kolorbildo.getchannel("G"), kolorbildo.getchannel("B"), tekstobildo.getchannel("A"))
	)
	return tekstobildo

print("Entajpu la konvertendan tekston")
konvertota = input()
print(unikodigi(konvertota))

print("Agordoj: [koloro=(nigro)] [maldekstrigi|centrigi|dekstrigi] [larĝolimo=(0)]")

kolornomo = koloro()
ĝisrandigo = 1
larĝolimo = None
for agordo in input().split():
	nomo_valoro = agordo.split('=')
	nomo, valoro = nomo_valoro[0], nomo_valoro[-1]
	try:
		match nomo:
			case 'koloro': kolornomo = koloro(valoro)
			case 'maldekstrigi': ĝisrandigo = 0
			case 'centrigi':     ĝisrandigo = 1
			case 'dekstrigi':    ĝisrandigo = 2
			case 'larĝolimo': larĝolimo = int(valoro)
			case _: raise Warning(f"Nekonata argumento: {nomo}")
	except Warning as w:
		print("!!!", w)

tekstobildo = bildigi(konvertota, kolornomo, ĝisrandigo, larĝolimo)

dosierujo = "rezultoj"
Path(dosierujo).mkdir(parents=True, exist_ok=True)
tekstobildo.save(dosierujo + "/" + konvertota.replace(" ", "_") + ".png")
