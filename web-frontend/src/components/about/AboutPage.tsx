import { Container } from 'react-bootstrap';

function AboutPage(): JSX.Element {
  return (
    <Container>
      <h1 className="my-4 text-center">O projektu 🎓</h1>
      <div className="fs-6 text-center">
        <p>
          Aplikace zpracovává polostrukturovaná data z transparentních ůčtů podporovaných bank a
          následně tyto data analyzuje.
        </p>
        <p>
          Projekt byl vytvořen jako bakalářská práce na{' '}
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
