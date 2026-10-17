# Chat TCP

Aplicație de chat în linie de comandă, cu un server TCP care servește mai mulți clienți simultan.

## Funcționalități

- fiecare client se conectează cu un nume
- mesajele unui client sunt trimise tuturor celorlalți
- intrarea și ieșirea din chat sunt anunțate
- serverul tratează fiecare client pe un fir de execuție separat (`ThreadingTCPServer`); lista clienților este protejată cu un `Lock`
- clientul citește mesajele pe un fir separat, ca să poată primi și trimite în același timp

## Protocol

Text, câte un mesaj pe linie. Prima linie trimisă de client este numele.

## Rulare

Necesită Python 3.8 sau mai nou, fără alte dependențe.

Server (portul implicit 5000):

```
python server.py
python server.py 6000
```

Client, în alte terminale:

```
python client.py
python client.py 192.168.1.10 6000
```

Teste:

```
python -m unittest
```
