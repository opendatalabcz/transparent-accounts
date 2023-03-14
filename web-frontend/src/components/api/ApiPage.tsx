import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import Config from '../../config';

function ApiPage(): JSX.Element {
  return <SwaggerUI url={Config.API_URL + '/api/swagger.json'} />;
}

export default ApiPage;
