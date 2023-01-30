import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  TimeScale,
  TimeSeriesScale,
  Title,
  Tooltip
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, TimeScale, TimeSeriesScale);

function ChartTransactions({ analysis }) {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const
      },
      title: {
        display: true,
        text: 'Počet transakcí v čase'
      }
    },
    parsing: {
      xAxisKey: 'date',
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

  const data = {
    datasets: [
      {
        label: 'Počet příchozích transakcí',
        data: analysis,
        lineTension: 1,
        borderColor: 'rgb(0, 0, 255)',
        backgroundColor: 'rgba(0, 0, 255, 0.5)',
        parsing: {
          yAxisKey: 'incomingCount'
        }
      },
      {
        label: 'Počet odchozích transakcí',
        data: analysis,
        lineTension: 1,
        borderColor: 'rgb(255, 0, 0)',
        backgroundColor: 'rgba(255, 0, 0, 0.5)',
        parsing: {
          yAxisKey: 'outgoingCount'
        }
      }
    ]
  };

  return <Line options={options} data={data} />;
}

export default ChartTransactions;
