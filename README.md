# Alpha-4.0

# UDP.py

Třída `UDP` je statická třída, která zvládá komunikaci pomocí socketů jak pro UDP, tak pro TCP. Je navržena tak, aby objevovala vrstevníky, odesílala a přijímala zprávy pomocí protokolů UDP a TCP.

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
