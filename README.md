# Alpha-4.0 (Peer-to-peer chat)
## Autor: Tomáš Novotný, kontakt: novotny10@spsejecna.cz
## Datum vypracování: 09.02.2024 - 25.02.2024
## Název a adresa školy: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30

# *Popis programu*
Tento program je navržen pro komunikaci mezi peer-to-peer sítěmi pomocí UDP a TCP protokolů. 

Program využívá třídu `Communication`, která obsahuje metody pro komunikaci pomocí UDP a TCP. Třída `Communication` obsahuje metody pro naslouchání příchozím paketům UDP, odesílání zpráv o objevení UDP, odesílání a přijímání zpráv a práci s TCP serverem a klientem.

Program pravidelně odesílá zprávy o objevení UDP na broadcastovou adresu, aby objevil vrstevníky v síti. Když program objeví vrstevníka, vytvoří TCP klienta pro komunikaci s tímto vrstevníkem.

Program také obsahuje metody pro odesílání a přijímání zpráv. Uživatel může zadat zprávu, která se odesílá všem připojeným klientům TCP. Přijaté zprávy se vypisují do konzole.

Pokud je program přerušen, funkce `cleanup_and_exit` uzavře všechny otevřené sokety a ukončí program.
</br></br>

# *Instalace potřebných knihoven*
- Pro správné fungování programu je zapotřebí doinstalovat určité knihovny.
- Nejjednoušší způsob, jak všechny knihovny nainstalovat, je spustit příkaz po příkazu tak, jak jsou zde napsány:
## *Instalace pythonu*
- Pro instalaci pythonu použijte následující příkaz:
``` python
sudo apt-get install python3
```
- Pro kontrolu verze pythonu použíjte následující příkaz:
```
python3 --version
```
## *Instalace knihovny .NET*
- Pro instalaci .NET použijte následující příkazy tak, jak jsou zde napsány za sebou:
1. ```
   wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
   ```
2. ```
   chmod +x ./dotnet-install.sh
   ```
3. ```
   ./dotnet-install.sh --channel 6.0
   ```
4. ```
   export DOTNET_ROOT=$(pwd)/.dotnet
   ```
5. ```
   export PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools
   ```

## *Instalace knihovny git*
- Pro instalaci gitu použijte následující příkaz:
```
sudo apt-get install git
```
- Pro kontrolu verze gitu použijte následující příkaz:
```
git -v
```
</br></br>

# *Spuštění programu*
Pro správné spuštění aplikace je třeba mít nainstalovaný Python, .NET a git.</br>
## *Spuštění skriptu*
1. Stáhněte si .zip soubor programu do svého PC.
2. Soubor extrahujte. Extrahovaný soubor bude obsahovat 2 následující soubory:
   - Složka Alpha4.0, kde je uložený celý projekt.
   - Textový soubor s odkazem na tuto GitHub stránku.
4. V textovém souboru se pomocí odkazu přesměrujte na tuto GitHub stránku.
5. Otevřete si svůj VM a nainstalujte všechny potřebné knihovny. Pro instalaci je dobré se seznámit s částí [Instalace potřebných knihoven](https://github.com/tomasnovotnyy/Alpha-4.0?tab=readme-ov-file#instalace-pot%C5%99ebn%C3%BDch-knihoven)
6. Nyní si ve svém VM zvolte místo, kde chcete mít uložený tento projekt.
7. Naklonujte si projekt pomocí tohoto příkazu:
```
git clone https://github.com/tomasnovotnyy/Alpha-4.0.git
```
8. Pro spuštění programu se přesměrujte do nově vytvořené složky s názvem `Alpha-4.0` a napište následující:
```
python3 Main.py
```
</br></br>

# Communication.py

Třída `Communication` je statická třída, která zvládá komunikaci pomocí socketů jak pro UDP, tak pro TCP. Je navržena tak, aby objevovala vrstevníky, odesílala a přijímala zprávy pomocí protokolů UDP a TCP.

## Atributy

- `udp_socket`: Objekt socketu UDP používaný pro odesílání a přijímání paketů UDP.
- `my_peer_id`: Řetězec představující jedinečný identifikátor aktuálního vrstevníka.
- `tcp_server_socket`: Objekt socketu TCP používaný pro přijímání příchozích TCP spojení.
- `tcp_client_sockets`: Seznam objektů socketů TCP představujících aktivní klientská spojení.
- `messages`: Slovník ukládající přijaté zprávy, klíčovaný podle ID zprávy.
- `discovered_peers`: Sada ukládající IP adresy objevených vrstevníků.

## Metody

- `udp_listener()`: Naslouchá příchozím paketům UDP a přidává IP adresu odesílatele do sady `discovered_peers`.
- `start_udp_listener()`: Inicializuje socket UDP a spustí naslouchání UDP v novém vlákně.
- `periodic_udp_discovery()`: Pravidelně odesílá zprávy o objevení UDP na broadcastovou adresu.
- `send_udp_discovery()`: Odesílá zprávu o objevení UDP na broadcastovou adresu.
- `send_messages()`: Neustále vyzývá uživatele k zadání zprávy a odesílá ji všem připojeným klientům TCP.
- `receive_messages()`: Neustále tiskne přijaté zprávy na konzoli.
- `start_tcp_server()`: Inicializuje serverový socket TCP a naslouchá příchozím spojením v novém vlákně.
- `handle_client(client_socket)`: Zvládá komunikaci s připojeným klientem TCP.
- `start_tcp_client(peer_ip)`: Připojuje se k serveru TCP na dané IP adrese a začíná vyměňovat zprávy.
- `send_tcp_message(message)`: Odesílá zprávu všem připojeným klientům TCP.
- `merge_messages(new_messages)`: Sloučí nově přijaté zprávy do slovníku `messages`.

# Main.py

Funkce `main()` v `Main.py` je vstupním bodem aplikace. Nastavuje zacházení se signály, spouští naslouchání a objevování UDP, spouští server TCP, připojuje se k objeveným vrstevníkům a začíná odesílat a přijímat zprávy.

## Funkce

- `cleanup_and_exit()`: Uzavře všechny otevřené sockety a ukončí aplikaci.
- `main()`: Hlavní funkce aplikace. Nastavuje aplikaci a spouští všechna potřebná vlákna.

## Zacházení se signály

Funkce `main()` nastavuje obsluhu signálů pro signál `SIGINT` (obvykle odeslaný stiskem Ctrl+C). Když je tento signál přijat, volá se funkce `cleanup_and_exit()` pro uzavření všech otevřených socketů a ukončení aplikace.
