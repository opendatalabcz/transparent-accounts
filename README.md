# Zpracování transparentních účtů

Transparentní bankovní účty jsou jedním z nástrojů podporující otevřenost při financování.
Politické subjekty mají povinnost používání transparentních účtů uloženou ze zákona.
Takové účty standardně obsahují velké množství transakcí, a proto jejich detailní analýza
může přinést zajímavé informace. Tato webová aplikace zpracovává data transparentních účtů
z webových stránek bank. Aplikace následně získaná data analyzuje. Součástí analýzy jsou
statistické údaje, agregace transakcí podle protistrany s vyhledáním protistrany v
transakcích jiných transparentních účtů a vizualizace transakcí v čase.

Projekt byl vytvořen jako bakalářská práce na [Fakultě informačních technologií](https://fit.cvut.cz/) ve spolupráci s laboratoří [OpenDataLab](https://opendatalab.cz/).

Autor: [Jakub Janeček](https://github.com/KasenX)

---

## Instalační instrukce

0. Nainstalovat [Docker](https://www.docker.com/)
1. Stáhnout projekt
2. `$ cd transparent-accounts`
3. Nastavit proměnné prostředí (pro inspiraci lze použít také soubor `.env.example`)

```bash
cat > .env <<EOF
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

Fetchování účtů probíhá každý den ve 3:00 (plánování lze změnit v [konfiguračním souboru](data-fetcher/app/config.py)). Až po té bude v aplikaci k dispozici zobrazení seznamu účtů a seznamu podporovaných bank.

## Přidání podpory pro další banku

Přidání podpory pro další banku je potřeba provést v komponentě [fetcher](data-fetcher/app/fetcher), která má za úkol získávání dat.

Aby aplikace mohla plně pracovat s transparentními účty další banky, je potřeba implementovat, jak získávání transparentních účtů, tak získávání transakcí. Do adresáře [fetcher](data-fetcher/app/fetcher) je potřeba přidat nový balíček, který bude obsahovat dvě třídy. První třída bude dědit z abstraktní třídy [AccountFetcher](data-fetcher/app/fetcher/account_fetcher.py) a bude se starat o získání dat o transparentních účtech z dané banky. Druhá třída bude dědit z abstraktní třídy [TransactionFetcher](data-fetcher/app/fetcher/transaction_fetcher.py) a bude mít za úkol získávání transakcí z daného transparentního účtu. Při implementaci nových tříd je vhodné využít pomocné funkce implementované v abstraktních třídách a zároveň se inspirovat u implementací tříd podporovaných bank. Mimo tyto dvě hlavní třídy je možné mít v balíčku další pomocné třídy nebo funkce. Testy by měly být umístěny do adresáře [tests](data-fetcher/tests).

Až bude implementace nových tříd funkční, je potřeba tyto třídy zaregistrovat v souboru [tasks.py](data-fetcher/app/tasks.py). V případě, že se bude jednat o novou banku poskytující transparentní účty, bude ještě potřeba rozšířit výčet bank nacházející se v souboru [tasks.py](data-fetcher/app/tasks.py) a doplnit metadata o bance do souboru [banks.json](analysis-api/banks.json) v komponentě [analysis-api](analysis-api).
