import React from 'react';
import ReactDOM from 'react-dom/client';
import './colors.scss';
import './style.css';
import { BrowserRouter } from 'react-router-dom';
import App from './components/App';
import reportWebVitals from './reportWebVitals';
import { createInstance, MatomoProvider } from '@jonkoops/matomo-tracker-react';

const instance = createInstance({
  urlBase: 'https://matomo.opendatalab.cz/',
  siteId: 5,
  linkTracking: false
});

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
      <BrowserRouter>
        <MatomoProvider value={instance}>
        <App />
        </MatomoProvider>
      </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
