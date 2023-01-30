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


function ChartBalance({ analysis }) {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const
      },
      title: {
        display: true,
        text: 'Vývoj zůstatku v čase'
      }
    },
    parsing: {
      xAxisKey: 'date',
    }
  };

  const data = {
    datasets: [
      {
        label: 'Zůstatek',
        data: analysis,
        lineTension: 1,
        borderColor: 'rgb(0, 0, 255)',
        backgroundColor: 'rgba(0, 0, 255, 0.5)',
        parsing: {
          yAxisKey: 'balance'
        }
      }
    ]
  };


  return <Line options={options} data={data} />
}

export default ChartBalance;
