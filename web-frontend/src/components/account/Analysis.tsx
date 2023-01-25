import { Container } from "react-bootstrap";
import AnalysisCard from "./AnalysisCard";

function Analysis() {
  const stats = [
    {
      name: "Počet transakcí",
      value: <span>622</span>,
    },
    {
      name: "Počet příchozích transakcí",
      value: <span>604</span>,
    },
    {
      name: "Počet odchozích transakcí",
      value: <span>18</span>,
    },
    {
      name: "Zůstatek",
      value: <span className="fs-3">21 221,98 CZK</span>,
    },
    {
      name: "Suma příjmů",
      value: <span className="fs-3">4 002 835,92 CZK</span>,
    },
    {
      name: "Suma výdajů",
      value: <span className="text-danger fs-3">-10 209 226,52 CZK</span>,
    },
    {
      name: "Průměrná výše příchozí transakce",
      value: <span className="fs-3">3 224,00 CZK</span>,
    },
    {
      name: "Průměrná výše odchozí transakce",
      value: <span className="text-danger fs-3">-386 235,50 CZK</span>,
    },
    {
      name: "Medián výše příchozí transakce",
      value: <span className="fs-3">0,01 CZK</span>,
    },
    {
      name: "Medián výše odchozí transakce",
      value: <span  className="text-danger fs-3">-20 000,00 CZK</span>,
    },
    {
      name: "Úroveň transparentnosti účtu",
      value: <span>12 %</span>,
      description: "Počítá se jako",
    },
    {
      name: "Uvedená poznámka",
      value: <span>100 %</span>,
      description: "V kolika procentech odchozích transakcí je uvedena jakákoliv poznámka.",
    },
  ];

  return (
    <Container className="analysis">
      <div className="row">
        {stats.map((stat) => (
          <AnalysisCard key={stat.name} metrics={stat} />
        ))}
      </div>
    </Container>
  );
}

export default Analysis;
