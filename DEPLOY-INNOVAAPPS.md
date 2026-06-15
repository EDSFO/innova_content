# Implantação na máquina Innovaapps

Destino:

- Host Tailscale: `innovaapps`
- IP Tailscale: `100.108.2.19`
- Frontend: `http://100.108.2.19:3002`
- API: `http://100.108.2.19:8000`
- Swagger: `http://100.108.2.19:8000/docs`

As portas são vinculadas somente ao IP Tailscale. O PostgreSQL não é publicado
na máquina host.

## Pré-requisitos no destino

- Tailscale conectado com o IP `100.108.2.19`
- Docker Desktop em execução
- Docker Compose v2
- OpenSSH Server, caso o deploy seja transferido por SSH

## Autorizar a máquina Erick no SSH

O host responde na porta `22`, mas ainda não autoriza a chave da máquina Erick.
No PowerShell da máquina Innovaapps, execute como o usuário que fará o deploy:

```powershell
New-Item -ItemType Directory -Path $HOME\.ssh -Force
Add-Content -Path $HOME\.ssh\authorized_keys -Value "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFVKh7uHwmYwJaB3gZg/Ptx6VPbPaux70MfM2PZWdnKV erick@Erick"
```

Depois, informe o nome exato desse usuário para usar no `scp`. Se a conta fizer
parte do grupo local Administrators e o OpenSSH estiver configurado para usar
`C:\ProgramData\ssh\administrators_authorized_keys`, a chave deverá ser
adicionada nesse arquivo com as permissões exigidas pelo OpenSSH para Windows.

## Criar o pacote na máquina Erick

```powershell
.\scripts\package-deployment.ps1
```

O arquivo será criado em:

```text
dist\innova-content-agent-deploy.zip
```

O pacote contém `.env` e a chave da OpenAI. Não envie por canais públicos.

## Transferir

Após configurar uma chave SSH para o usuário remoto:

```powershell
scp .\dist\innova-content-agent-deploy.zip USUARIO@100.108.2.19:C:/Temp/
```

Na máquina Innovaapps:

```powershell
New-Item -ItemType Directory -Path C:\Apps\InnovaContentAgent -Force
Expand-Archive C:\Temp\innova-content-agent-deploy.zip C:\Apps\InnovaContentAgent -Force
Set-Location C:\Apps\InnovaContentAgent
.\scripts\install-innovaapps.ps1
```

## Validação

```powershell
docker compose ps
docker compose logs api --tail 50
Invoke-RestMethod http://100.108.2.19:8000/api/health
```

Somente depois dessas verificações os containers da máquina Erick devem ser
desligados:

```powershell
docker compose down
```

Não use `docker compose down -v`, pois essa opção remove os dados locais.

## Dados existentes

Se houver campanhas que precisem ser preservadas, faça `pg_dump` na máquina
Erick e restaure no PostgreSQL remoto antes do desligamento. O deploy inicial
não copia volumes Docker automaticamente.
