import {
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  LineElement,
  PointElement,
  TimeScale,
  Tooltip as TooltipJS
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import { cs } from 'date-fns/locale';
import { Card, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { DateCounts } from '../../types';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, TooltipJS, TimeScale);

interface Props {
  data: Array<DateCounts>;
  currency: string | null;
}

function ChartBalance({ data, currency }: Props): JSX.Element {
  const options = {
    responsive: true,
    parsing: {
      xAxisKey: 'date'
    },
    scales: {
      x: {
        type: 'time',
        time: {
          tooltipFormat: 'P'
        },
        adapters: {
          date: {
            locale: cs
          }
        }
      }
    },
    elements: {
      point: {
        radius: 0
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  const chartData = {
    datasets: [
      {
        label: `Zůstatek v ${currency}`,
        data: data,
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
          {/* @ts-ignore */}
          <Line options={options} data={chartData} />
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default ChartBalance;
