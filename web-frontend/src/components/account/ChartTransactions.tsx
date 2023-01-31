import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip as TooltipJS,
  Legend,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Bar } from 'react-chartjs-2';
import { Card, OverlayTrigger, Tooltip } from 'react-bootstrap';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  TooltipJS,
  Legend
);

function ChartTransactions({ data }) {
  const options = {
    responsive: true,
    parsing: {
      xAxisKey: 'monthYear'
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      },
    },
  };

  const chartData = {
    datasets: [
      {
        label: 'Počet příchozích transakcí',
        data: data,
        backgroundColor: 'rgba(0, 0, 255)',
        parsing: {
          yAxisKey: 'incomingCount'
        }
      },
      {
        label: 'Počet odchozích transakcí',
        data: data,
        backgroundColor: 'rgba(255, 0, 0)',
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
          <Bar options={options} data={chartData} />
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default ChartTransactions;
