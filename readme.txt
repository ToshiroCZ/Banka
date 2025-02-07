_____________________________________________________________
Bank system
_____________________________________________________________

Autor: Matouš Podaný
Třída: C4b

_____________________________________________________________
Konfigurace:
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


py -m src.bank_node --conn-string "DRIVER={ODBC Driver 17 for SQL Server};SERVER=THE-BEAST\SQLEXPRESS;DATABASE=Banka;Trusted_Connection=yes;" --port 65525 --bankcode 10.1.2.3


Vlastnosti programu:

Akceptuje příkazy ve správném formátu i s malými písmeny

_____________________________________________________________
Sources:
_____________________________________________________________

https://www.geeksforgeeks.org/logging-in-python/
https://www.geeksforgeeks.org/socket-programming-python/