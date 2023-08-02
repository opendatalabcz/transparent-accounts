import { Container } from 'react-bootstrap';

function AboutPage(): JSX.Element {
  return (
    <Container>
      <h1 className="my-4 text-center">O projektu 🎓</h1>
      <div className="fs-6 text-start">
        <p>
          Transparentní bankovní účty jsou jedním z nástrojů podporující otevřenost při financování.
          Politické subjekty mají povinnost používání transparentních účtů uloženou ze zákona.
          Takové účty standardně obsahují velké množství transakcí, a proto jejich detailní analýza
          může přinést zajímavé informace. Tato webová aplikace zpracovává data transparentních účtů
          z webových stránek bank. Aplikace následně získaná data analyzuje. Součástí analýzy jsou
          statistické údaje, agregace transakcí podle protistrany s vyhledáním protistrany v
          transakcích jiných transparentních účtů a vizualizace transakcí v čase.
        </p>
        <p>
          Projekt byl vytvořen jako{' '}
          <a href="https://dspace.cvut.cz/handle/10467/109558" target="_blank">
            bakalářská práce
          </a>{' '}
          na{' '}
          <a href="https://fit.cvut.cz" target="_blank" rel="noreferrer">
            Fakultě informačních technologií
          </a>{' '}
          ve spolupráci s laboratoří{' '}
          <a href="https://opendatalab.cz" target="_blank" rel="noreferrer">
            OpenDataLab
          </a>
          .
        </p>
        <p>
          Autor:{' '}
          <a href="https://www.linkedin.com/in/jakubjanecek12" target="_blank" rel="noreferrer">
            Jakub Janeček
          </a>
        </p>
      </div>
    </Container>
  );
}

export default AboutPage;
