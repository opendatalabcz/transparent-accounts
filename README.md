# Zpracování transparentních účtů

Aplikace zpracovává polostrukturovaná data z transparentních ůčtů podporovaných bank a následně tyto data analyzuje.

Projekt byl vytvořen jako bakalářská práce na [Fakultě informačních technologií](https://fit.cvut.cz/) ve spolupráci s laboratoří [OpenDataLab](https://opendatalab.cz/).

Autor: [Jakub Janeček](https://github.com/KasenX)

---

## Instalační instrukce

0. Nainstalovat [Docker](https://www.docker.com/)
1. Stáhnout projekt
2. `$ cd transparent-accounts`
3. Nastavit proměnné prostředí (pro inspiraci lze použít také soubor `.env.example`)

```bash
$ cat > .env <<EOF
SECRET_KEY=secret123
DB_PASSWORD=secret456
DB_USER=postgres # Optional
DB_NAME=postgres # Optional
RABBITMQ_USER=admin
RABBITMQ_PASS=secret789
ANALYSIS_API_URL=http://localhost:5000/api
EOF
```

4. `$ docker-compose up`
5. Otevřít v prohlížeči: http://localhost:3000

## Contributing

🚧
