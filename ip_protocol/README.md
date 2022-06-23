# IP протокол

#### Запуск

Получение ip-адреса и маски подсети
```bash
pipenv run src/ip_address.py [interface]
```

Получение свободных портов
```bash
pipenv run src/available_port.py <ip-addr> <from-port> <to-port>
```
Перебираются порты с `from-port` включительно до `to-port` не включительно.
