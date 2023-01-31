import { useMemo } from 'react';
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  TimeSeriesScale,
  Title,
  Tooltip as TooltipJS
} from 'chart.js';
import { format } from 'date-fns';
import 'chartjs-adapter-date-fns';
import { Bar } from 'react-chartjs-2';
import { Card, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { DateCounts } from '../../types';
import { cs } from 'date-fns/locale';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, TooltipJS, Legend, TimeSeriesScale);

interface Props {
  data: Array<DateCounts>;
}

function ChartTransactions({ data }: Props): JSX.Element {

  // Group dates by week
  const grouped: Array<DateCounts> = useMemo(() => {
    let lastWeek: number = 0;
    return data.reduce((acc: Array<DateCounts>, item: DateCounts) => {
      // Get the current week number
      const date: Date = new Date(item.date);
      const week: number = Number(format(date, 'w'));
      // Current week differs from the last week -> add new item to accumulator
      if (lastWeek !== week) {
        acc.push({ date: item.date, incomingCount: 0, outgoingCount: 0 });
        lastWeek = week;
      }
      // Update last item's properties
      acc[acc.length - 1].incomingCount += item.incomingCount;
      acc[acc.length - 1].outgoingCount += item.outgoingCount;
      return acc;
    }, []);
  }, [data]);

  const options = {
    responsive: true,
    parsing: {
      xAxisKey: 'date'
    },
    scales: {
      x: {
        stacked: 'true',
        type: 'timeseries',
        time: {
          minUnit: 'week',
          tooltipFormat: 'P'
        },
        adapters: {
          date: {
            locale: cs
          }
        }
      },
      y: {
        stacked: true
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
        label: 'Počet příchozích transakcí',
        data: grouped,
        backgroundColor: 'rgba(0, 0, 255)',
        parsing: {
          yAxisKey: 'incomingCount'
        }
      },
      {
        label: 'Počet odchozích transakcí',
        data: grouped,
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
          {/* @ts-ignore */}
          <Bar options={options} data={chartData} />
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default ChartTransactions;
