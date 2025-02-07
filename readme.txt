_____________________________________________________________
Bank system
_____________________________________________________________

Autor: Matouš Podaný
Třída: C4b

_____________________________________________________________
Konfigurace v config.json:
_____________________________________________________________
__________________
CONNECTION STRING:

Connection string vaší MSSQL (Microsoft SQL) databáze

příklad:
--conn-string "DRIVER={ODBC Driver 17 for SQL Server};SERVER=jmeno\serveru;DATABASE=jmenoDatabaze;Trusted_Connection=yes;"
_________
BANKCODE:

Musí být ipv4 v rámci lokální sítě! Jinak se banky nedokáží spojit.

Správný příklad: 
10.0.0.x
PC1: 10.0.0.99
PC2: 10.0.0.98
PC3: 10.0.0.97

Špatný příklad:
PC1: 10.0.0.99
PC2: 192.168.50.1
PC3: 192.168.49.1

_________
Port:

V rozmezí 65525 až 65535
_____________________________________________________________
Spuštění:
_____________________________________________________________

Vytvořte v MSSQL management studio novou databázi s názvem Banka
Stáhněte si Banka.zip nebo projekt naclonujte z GitHub (doporučené):
https://github.com/ToshiroCZ/Banka.git

Při práci v terminálu/příkazovém řádku (CMD) musíte být v directory projektu
cd ...\Banka

Vytvořte virtuální prostředí:
python -m venv venv

Poté aktivujte virtuální prostředí:
venv\Scripts\activate

Nainstalujte závislosti:
pip install -r requirements.txt

(Při vyskytnutí problému, jako nefunkčnost balíčků, dvě složky venv => smažte složku/y venv a zkuste postup znovu)


py -m src.bank_node --config config.json


Vlastnosti programu:

Akceptuje příkazy ve správném formátu i s malými písmeny
Komunikuje s jinými bankami


Název 			Kód 	Volání				Odpověď při úspěchu	Odpověď při chybě
_________________________________________________________________________________________________________
Bank code		BC	BC				BC <ip>			ER <message>
Account create		AC	AC				AC <account>/<ip> 	ER <message>
Account deposit		AD	AD <account>/<ip> <number>	AD			ER <message>
Account withdrawal	AW	AW <account>/<ip> <number>	AW			ER <message>
Account balance		AB	AB <account>/<ip>		AB <number>		ER <message>
Account remove		AR	AR <account>/<ip>		AR			ER <message>
Bank (total) amount	BA	BA				BA <number>		ER <message>
Bank number of clients	BN	BN				BN <number>		ER <message>
_________________________________________________________________________________________________________

Vysvětlení k <ip>, <account> a <number>

<ip> IP adresa, používá jako kód banky, tj. unikátní indentifikátor každé banky v naší síti
<account> Kladné celé číslo v rozsahu 10000 až 99999 (deset tisíc až devadesát devět tisíc devět set devadesát devět)
<number> Nezáporné celé číslo v rozsahu 0 až  9223372036854775807 (nula až dvě na šedesátou třetí, mínus jedna, tedy velikost 64bitového datového typu, zpravidla označovaného jako long)

_____________________________________________________________
Testy:
_____________________________________________________________

Spustíte pomocí: py -m unittest discover -s tests

_____________________________________________________________
Znovu-použití kódu:
_____________________________________________________________

S menšími/většími úpravami:
Kód pro práci s konfiguračním souborem (config.json)
Kód pro práci s databází

_____________________________________________________________
Zdroje:
_____________________________________________________________

https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
https://docs.python.org/3.9/library/logging.html
https://www.python.org/doc/
https://www.geeksforgeeks.org/logging-in-python/
https://www.geeksforgeeks.org/socket-programming-python/