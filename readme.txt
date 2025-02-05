Vytvořte virtuální prostředí:
python -m venv venv

Poté aktivujte virtuální prostředí:
venv\Scripts\activate

Nainstalujte závislosti:
pip install -r requirements.txt


py -m src.bank_node --conn-string "DRIVER={ODBC Driver 17 for SQL Server};SERVER=THE-BEAST\SQLEXPRESS;DATABASE=Banka;Trusted_Connection=yes;" --port 65525 --bankcode 10.1.2.3


Vlastnosti:

Akceptuje příkazy ve správném formátu i s malými písmeny
