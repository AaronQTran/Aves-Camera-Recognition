import React, { useState, useEffect } from 'react';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import { Line } from 'react-chartjs-2';
import './App.css';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const Statistic = ({ label, value }) => (
  <div className="text-center mb-2">
    <h2 className="text-white text-4xl font-bold">{value}</h2>
    <hr className="rainbow-gradient" />
    <p className="text-white text-sm">{label}</p>
  </div>
);


const Main = () => {
  const [showSplash, setShowSplash] = useState(true);
  const [andrewStatus, setAndrewStatus] = useState('Inside');
  const [kamrynStatus, setKamrynStatus] = useState('Inside');
  const [jordanStatus, setJordanStatus] = useState('Inside');
  const [nickStatus, setNickStatus] = useState('Inside');

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const data = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: '# of Times Leaving',
        data: [12, 19, 3, 5, 2, 3, 7], //fake data
        fill: true, 
        backgroundColor: 'rgba(0, 128, 128, 0.2)', 
        pointBackgroundColor: 'white',
        pointBorderColor: 'white',
        borderColor: 'purple',
        tension: 0.3
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'gray', 
        },
      },
      x: {
        grid: {
          color: 'gray', 
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: 'white', 
          font: {
            size: 13, 
            family: 'Arial' 
          }
        }
      }
    },
  };

  const statistics = {
    Andrew: {
      avgTimesLeft: 5,
      lastTimeEntered: '8:00 AM',
      lastTimeExited: '5:00 PM',
      avgTimeAway: '1h 30m'
    },
    Kamryn: {
      avgTimesLeft: 4,
      lastTimeEntered: '8:30 AM',
      lastTimeExited: '5:15 PM',
      avgTimeAway: '1h 15m'
    },
    Jordan: {
      avgTimesLeft: 6,
      lastTimeEntered: '9:00 AM',
      lastTimeExited: '5:45 PM',
      avgTimeAway: '2h'
    },
    Nick: {
      avgTimesLeft: 3,
      lastTimeEntered: '7:45 AM',
      lastTimeExited: '4:30 PM',
      avgTimeAway: '1h'
    }
  };

  const handleManualFix = (name) => {
    //determine new status
    let newStatus;
    switch (name) {
        case 'Andrew':
            newStatus = andrewStatus === 'Inside' ? 'Outside' : 'Inside';
            setAndrewStatus(newStatus);
            break;
        case 'Kamryn':
            newStatus = kamrynStatus === 'Inside' ? 'Outside' : 'Inside';
            setKamrynStatus(newStatus);
            break;
        case 'Jordan':
            newStatus = jordanStatus === 'Inside' ? 'Outside' : 'Inside';
            setJordanStatus(newStatus);
            break;
        case 'Nick':
            newStatus = nickStatus === 'Inside' ? 'Outside' : 'Inside';
            setNickStatus(newStatus);
            break;
        default:
            return;
    }

    fetch('/api/manualFix', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, status: newStatus }), //body = parameters/data sent to the api
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

{/* <button onClick={() => handleManualFix('Andrew')} class="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix </button> */}

  return (
    <div className="bg-gray-900 w-screen min-h-screen flex flex-col md:flex-row">
      {showSplash && (
        <div className="splash-screen absolute inset-0 flex items-center justify-center z-50 gradient-background">
          <h1 className="text-white font-medium text-4xl">Aves Attendance</h1>
          <PendingActionsIcon className="ml-2" style={{ fontSize: 50, color: 'white' }} />
        </div>
      )}
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className="font-medium text-red-500 font-custom text-4xl">Andrew</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Andrew" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Andrew.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Andrew.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Andrew.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Andrew.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Andrew')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix </button>
      </div>
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className="font-medium text-green-500 font-custom text-4xl">Kamryn</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Kamryn" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Kamryn.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Kamryn.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Kamryn.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Kamryn.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Kamryn')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix </button>
      </div>
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className="text-white font-medium font-custom text-4xl">Jordan</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Jordan" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Jordan.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Jordan.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Jordan.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Jordan.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Jordan')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix </button>
      </div>
      <div className="md:w-1/4 w-full flex flex-col items-center">
        <h1 className="text-white font-medium font-custom text-4xl">Nick</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Nick" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Nick.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Nick.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Nick.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Nick.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Nick')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix </button>
      </div>
    </div>
  );
};

export default Main;


