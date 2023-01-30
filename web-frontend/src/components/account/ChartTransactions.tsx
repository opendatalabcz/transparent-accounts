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

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TooltipJS,
  TimeScale,
  TimeSeriesScale
);

function ChartTransactions({ data }) {
  const options = {
    responsive: true,
    parsing: {
      xAxisKey: 'date'
    },
    scales: {
      x: {
        type: 'time' as const,
        time: {
          unit: 'month' as const
        }
      }
    },
    adapters: {
      date: { locale: 'cs' }
    }
  };

  const chartData = {
    datasets: [
      {
        label: 'Počet příchozích transakcí',
        data: data,
        lineTension: 1,
        borderColor: 'rgb(0, 0, 255)',
        backgroundColor: 'rgba(0, 0, 255, 0.5)',
        parsing: {
          yAxisKey: 'incomingCount'
        }
      },
      {
        label: 'Počet odchozích transakcí',
        data: data,
        lineTension: 1,
        borderColor: 'rgb(255, 0, 0)',
        backgroundColor: 'rgba(255, 0, 0, 0.5)',
        parsing: {
          yAxisKey: 'outgoingCount'
        }
      }
    ]
  };

  return (
    <Card className="h-100">
      <Card.Body>
        <Card.Title className="h6 ellipsis mb-1">
          <OverlayTrigger placement="bottom" overlay={<Tooltip>Počet transakcí v čase</Tooltip>}>
            <span>Počet transakcí v čase</span>
          </OverlayTrigger>
        </Card.Title>
        <Card.Text>
          <Line options={options} data={chartData} />
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default ChartTransactions;
