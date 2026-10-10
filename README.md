# memory-bound-backend

Aloca um buffer de `mb` megabytes e escreve em cada página dele, forçando o SO a reservar memória física. O custo da requisição é dominado pela alocação de memória.

Só usa a biblioteca padrão do Python 3.

```bash
python3 server.py
curl "http://localhost:8080/?mb=200"
```

A porta pode ser trocada com a variável `PORT`.
