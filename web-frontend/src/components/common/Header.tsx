import { Link } from 'react-router-dom';
import { BsBarChartFill, BsGithub } from 'react-icons/bs';
import { GiCapitol } from 'react-icons/gi';
import { FaCoins, FaGraduationCap } from 'react-icons/fa';
import { AiOutlineSetting } from 'react-icons/ai';
import { Nav, Navbar } from 'react-bootstrap';
import './Header.css';

function Header() {
  return (
    <Navbar collapseOnSelect expand="lg" bg="primary" variant="dark" className="py-0 px-3">
      <Navbar.Brand>
        <Nav.Link as={Link} to="/" className="py-0 me-5" id="brand-container">
          <div className="d-flex align-items-end">
            <BsBarChartFill size={56} id="brand-logo" />
            <span>ZPRACOVÁNÍ A ANALÝZA{'\n'}TRANSPARENTNÍCH ÚČTŮ</span>
          </div>
        </Nav.Link>
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="me-auto inside-nav">
          <Nav.Link as={Link} to="/ucty" className="me-xl-5">
            <FaCoins className="align-text-top" />
            Účty
          </Nav.Link>
          <Nav.Link as={Link} to="/banky" className="me-xl-5">
            <GiCapitol className="align-text-top" />
            Banky
          </Nav.Link>
          <Nav.Link as={Link} to="/o-projektu" className="me-xl-5">
            <FaGraduationCap className="align-text-top" />
            O&nbsp;projektu
          </Nav.Link>
          <Nav.Link as={Link} to="/api">
            <AiOutlineSetting className="align-text-top" />
            API
          </Nav.Link>
        </Nav>
        <Nav>
          <Nav.Link
            href="https://github.com/opendatalabcz/transparent-accounts/"
            target="_blank"
            rel="noreferrer">
            <BsGithub className="align-text-top" />
            GitHub
          </Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Header;
