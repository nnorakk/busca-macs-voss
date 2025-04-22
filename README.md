# 🧠 async_lista_macs_extreme

Script Python para listar os endereços MAC de dispositivos Extreme Networks em uma faixa de IPs. Suporta execução local e em containers Docker ou Podman.

---

## ✅ Requisitos

- Python 3.7+
- `asyncio`
- `aiohttp`
- Um arquivo `.env` (opcional) com as variáveis de ambiente `SWITCHUSER` e `PASSWORD`

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/async_lista_macs_extreme.git
cd async_lista_macs_extreme
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Usar

### Execução Local

```bash
python async_lista_macs_extreme.py --ips 10.16.120.{101..115} --switchuser SWITCHUSER --password PASSWORD
```

Ou carregando as variáveis de ambiente de um `.env`:

```bash
source .dockerenv
python async_lista_macs_extreme.py --ips 10.16.120.{101..115}
```

---

## 🐳 Usando com Docker

### Construir a imagem

```bash
docker build -t my-python-app .
```

### Executar com usuário e senha

```bash
docker run --rm my-python-app --ips 10.16.120.{101..102} --switchuser "SWITCHUSER" --password "PASSWORD"
```

### Executar usando arquivo `.env`

```bash
docker run --rm --env-file .env my-python-app --ips 10.16.120.101
```

### Debug com bash

```bash
docker run --rm -it --entrypoint /bin/bash my-python-app
```

---

## 🧪 Usando com Podman

### Construir a imagem

```bash
podman build -t my-python-app .
```

### Executar com usuário e senha

```bash
podman run --rm my-python-app --ips 10.16.120.{101..102} --switchuser "SWITCHUSER" --password "PASSWORD"
```

### Executar usando arquivo `.env`

```bash
podman run --rm --env-file .env my-python-app --ips 10.16.120.101
```

### Debug com bash

```bash
podman run --rm -it --entrypoint /bin/bash my-python-app
```

---

## 🧾 Exemplo de `.env`

```dotenv
SWITCHUSER=admin
PASSWORD=supersecret
```
