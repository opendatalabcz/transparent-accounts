import {
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  LineElement,
  PointElement,
  TimeScale,
  TimeSeriesScale,
  Tooltip as TooltipJS
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2';
import { Card, OverlayTrigger, Tooltip } from 'react-bootstrap';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, TooltipJS, TimeScale, TimeSeriesScale);


function ChartBalance({ data }) {
  const options = {
    responsive: true,
    parsing: {
      xAxisKey: 'date',
    }
  };

  const chartData = {
    datasets: [
      {
        label: 'Zůstatek',
        data: data,
        lineTension: 1,
        borderColor: 'rgb(0, 0, 255)',
        backgroundColor: 'rgba(0, 0, 255, 0.5)',
        parsing: {
          yAxisKey: 'balance'
        }
      }
    ]
  };

  return (
    <Card className="h-100">
      <Card.Body>
        <Card.Title className="h6 ellipsis mb-1">
          <OverlayTrigger placement="bottom" overlay={<Tooltip>Vývoj zůstatku v čase</Tooltip>}>
            <span>Vývoj zůstatku v čase</span>
          </OverlayTrigger>
        </Card.Title>
        <Card.Text>
          <Line options={options} data={chartData} />
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default ChartBalance;
