import { Route, Routes } from 'react-router-dom';
import Header from './common/Header';
import HomePage from './home/HomePage';
import AccountsPage from './accounts/AccountsPage';
import AccountPage from './account/AccountPage';
import BanksPage from './banks/BanksPage';
import AboutPage from './about/AboutPage';
import ApiPage from './api/ApiPage';
import PageNotFound from './PageNotFound';

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ucty" element={<AccountsPage />} />
        <Route path="/ucty/:bankCode/:accNumber" element={<AccountPage />} />
        <Route path="/banky" element={<BanksPage />} />
        <Route path="/o-projektu" element={<AboutPage />} />
        <Route path="/api" element={<ApiPage />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}

export default App;
