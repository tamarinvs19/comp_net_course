## RIP
Реализация RIP протокола маршрутизации. Основан на алгоритме Форда-Беллмана, позволяет маршрутизаторам небольших сетей динамически обновлять маршрутную информацию.

Запуск

```bash
$ pipenv run simulate
```

Схема сети задается в файле `network_schema.json`:
```json
{
        "simulation_cycles": 4,
        "networks": {
                "192.168.0.2": ["192.168.0.3", "192.168.0.4", "123.45.5.6"],
                "192.168.0.3": ["192.168.0.2", "88.88.88.88", "123.45.5.6"],
                "192.168.0.4": ["192.168.0.2"],
                "123.45.5.6": ["192.168.0.2", "192.168.0.3"],
                "88.88.88.88": ["192.168.0.3"]
        }
}
```

Пример вывода (также в файле `output.txt`):
```
Simulation step 1 of router 192.168.0.4
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.4	192.168.0.2		192.168.0.2	1

Simulation step 1 of router 192.168.0.3
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.3	192.168.0.2		192.168.0.2	1
192.168.0.3	123.45.5.6		123.45.5.6	1
192.168.0.3	88.88.88.88		88.88.88.88	1

Simulation step 1 of router 123.45.5.6
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
123.45.5.6	192.168.0.2		192.168.0.2	1
123.45.5.6	192.168.0.3		192.168.0.3	1
123.45.5.6	88.88.88.88		192.168.0.3	2

Simulation step 1 of router 192.168.0.2
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.2	192.168.0.4		192.168.0.4	1
192.168.0.2	192.168.0.3		192.168.0.3	1
192.168.0.2	123.45.5.6		123.45.5.6	1

Simulation step 1 of router 88.88.88.88
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
88.88.88.88	192.168.0.2		192.168.0.3	2
88.88.88.88	192.168.0.3		192.168.0.3	1
88.88.88.88	123.45.5.6		192.168.0.3	2

Simulation step 2 of router 192.168.0.3
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.3	192.168.0.4		192.168.0.2	2
192.168.0.3	192.168.0.2		192.168.0.2	1
192.168.0.3	123.45.5.6		123.45.5.6	1
192.168.0.3	88.88.88.88		88.88.88.88	1

Simulation step 2 of router 192.168.0.4
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.4	192.168.0.2		192.168.0.2	1
192.168.0.4	192.168.0.3		192.168.0.2	2
192.168.0.4	123.45.5.6		192.168.0.2	2
192.168.0.4	88.88.88.88		192.168.0.2	3

Simulation step 2 of router 123.45.5.6
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
123.45.5.6	192.168.0.4		192.168.0.2	2
123.45.5.6	192.168.0.2		192.168.0.2	1
123.45.5.6	192.168.0.3		192.168.0.3	1
123.45.5.6	88.88.88.88		192.168.0.3	2

Simulation step 2 of router 192.168.0.2
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.2	192.168.0.4		192.168.0.4	1
192.168.0.2	192.168.0.3		192.168.0.3	1
192.168.0.2	123.45.5.6		123.45.5.6	1
192.168.0.2	88.88.88.88		192.168.0.3	2

Simulation step 2 of router 88.88.88.88
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
88.88.88.88	192.168.0.4		192.168.0.3	3
88.88.88.88	192.168.0.2		192.168.0.3	2
88.88.88.88	192.168.0.3		192.168.0.3	1
88.88.88.88	123.45.5.6		192.168.0.3	2

Simulation step 3 of router 192.168.0.4
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.4	192.168.0.2		192.168.0.2	1
192.168.0.4	192.168.0.3		192.168.0.2	2
192.168.0.4	123.45.5.6		192.168.0.2	2
192.168.0.4	88.88.88.88		192.168.0.2	3

Simulation step 3 of router 192.168.0.3
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.3	192.168.0.4		192.168.0.2	2
192.168.0.3	192.168.0.2		192.168.0.2	1
192.168.0.3	123.45.5.6		123.45.5.6	1
192.168.0.3	88.88.88.88		88.88.88.88	1

Simulation step 3 of router 88.88.88.88
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
88.88.88.88	192.168.0.4		192.168.0.3	3
88.88.88.88	192.168.0.2		192.168.0.3	2
88.88.88.88	192.168.0.3		192.168.0.3	1
88.88.88.88	123.45.5.6		192.168.0.3	2

Simulation step 3 of router 123.45.5.6
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
123.45.5.6	192.168.0.4		192.168.0.2	2
123.45.5.6	192.168.0.2		192.168.0.2	1
123.45.5.6	192.168.0.3		192.168.0.3	1
123.45.5.6	88.88.88.88		192.168.0.3	2

Simulation step 3 of router 192.168.0.2
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.2	192.168.0.4		192.168.0.4	1
192.168.0.2	192.168.0.3		192.168.0.3	1
192.168.0.2	123.45.5.6		123.45.5.6	1
192.168.0.2	88.88.88.88		192.168.0.3	2

Simulation step 4 of router 123.45.5.6
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
123.45.5.6	192.168.0.4		192.168.0.2	2
123.45.5.6	192.168.0.2		192.168.0.2	1
123.45.5.6	192.168.0.3		192.168.0.3	1
123.45.5.6	88.88.88.88		192.168.0.3	2

Simulation step 4 of router 192.168.0.3
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.3	192.168.0.4		192.168.0.2	2
192.168.0.3	192.168.0.2		192.168.0.2	1
192.168.0.3	123.45.5.6		123.45.5.6	1
192.168.0.3	88.88.88.88		88.88.88.88	1

Simulation step 4 of router 192.168.0.2
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.2	192.168.0.4		192.168.0.4	1
192.168.0.2	192.168.0.3		192.168.0.3	1
192.168.0.2	123.45.5.6		123.45.5.6	1
192.168.0.2	88.88.88.88		192.168.0.3	2

Simulation step 4 of router 88.88.88.88
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
88.88.88.88	192.168.0.4		192.168.0.3	3
88.88.88.88	192.168.0.2		192.168.0.3	2
88.88.88.88	192.168.0.3		192.168.0.3	1
88.88.88.88	123.45.5.6		192.168.0.3	2

Simulation step 4 of router 192.168.0.4
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.4	192.168.0.2		192.168.0.2	1
192.168.0.4	192.168.0.3		192.168.0.2	2
192.168.0.4	123.45.5.6		192.168.0.2	2
192.168.0.4	88.88.88.88		192.168.0.2	3

Final state of router 192.168.0.4 table:
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.4	192.168.0.2		192.168.0.2	1
192.168.0.4	192.168.0.3		192.168.0.2	2
192.168.0.4	123.45.5.6		192.168.0.2	2
192.168.0.4	88.88.88.88		192.168.0.2	3

Final state of router 192.168.0.2 table:
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.2	192.168.0.4		192.168.0.4	1
192.168.0.2	192.168.0.3		192.168.0.3	1
192.168.0.2	123.45.5.6		123.45.5.6	1
192.168.0.2	88.88.88.88		192.168.0.3	2

Final state of router 192.168.0.3 table:
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
192.168.0.3	192.168.0.4		192.168.0.2	2
192.168.0.3	192.168.0.2		192.168.0.2	1
192.168.0.3	123.45.5.6		123.45.5.6	1
192.168.0.3	88.88.88.88		88.88.88.88	1

Final state of router 123.45.5.6 table:
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
123.45.5.6	192.168.0.4		192.168.0.2	2
123.45.5.6	192.168.0.2		192.168.0.2	1
123.45.5.6	192.168.0.3		192.168.0.3	1
123.45.5.6	88.88.88.88		192.168.0.3	2

Final state of router 88.88.88.88 table:
[Sourse IP]	[Destination IP]	[Next Hop]	[Metric]
88.88.88.88	192.168.0.4		192.168.0.3	3
88.88.88.88	192.168.0.2		192.168.0.3	2
88.88.88.88	192.168.0.3		192.168.0.3	1
88.88.88.88	123.45.5.6		192.168.0.3	2
```
