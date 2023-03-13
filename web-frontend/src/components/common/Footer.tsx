import { Fitcvut, Opendatalab } from '../../Icons/';

function Footer(): JSX.Element {
  return (
    <footer>
      <div className="p-3 mt-4 bg-light">
        <div className="row gx-3 align-items-center">
          <div className="col text-lg-start text-center">
            <p className="mb-1">
              Janeček Jakub, <i>Zpracování transparentních účtů</i> [online]. Bakalářská práce.
              Praha: ČVUT, Fakulta informačních technologií &amp; OpenDataLab, 2023. [cit. TBD]
              Dostupné z TBA.
            </p>
            <p className="mb-1">
              Zdroje dat: <i>vybrané banky</i>
            </p>
            <p className="mb-1">
              Kontakt: <a href="mailto: janecja9@fit.cvut.cz">janecja9@fit.cvut.cz</a>
            </p>
            <p className="mb-0 fst-italic">
              Provozovatel neodpovídá za správnost a úplnost zpracovaných dat a informací, ani tato
              neověřuje a zříká se zodpovědnosti za veškeré škody a újmy, které by použitím těchto
              dat mohly vzniknout.
            </p>
          </div>
          <div className="col-lg-auto text-center">
            <a href="https://fit.cvut.cz/" target="_blank">
              <Fitcvut height="70px" width="200px" />
            </a>
            &nbsp;
            <a href="https://opendatalab.cz/" target="_blank">
              <Opendatalab height="70px" width="100px" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
