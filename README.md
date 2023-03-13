# Zpracování transparentních účtů

Aplikace zpracovává polostrukturovaná data z transparentních ůčtů podporovaných bank a následně tyto data analyzuje.

Projekt byl vytvořen jako bakalářská práce na [Fakultě informačních technologií](https://fit.cvut.cz/) ve spolupráci s laboratoří [OpenDataLab](https://opendatalab.cz/).

Autor: [Jakub Janeček](https://github.com/KasenX)

---

## Instalační instrukce

0. Nainstalovat [Docker](https://www.docker.com/)
1. Stáhnout projekt
2. `$ cd transparent-accounts`
3. Vytvořit secrets (mimo secrets je možné do `.env` souboru přidat `DB_USER` a `DB_NAME`)

```bash
$ cat > .env <<EOF
DB_PASSWORD=secret123
SECRET_KEY=secret456
EOF
```

4. `$ docker-compose up`
5. Otevřít v prohlížeči: http://localhost:3000

## Contributing

🚧
