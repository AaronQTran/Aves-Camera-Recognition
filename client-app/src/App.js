import React, { useState, useEffect } from 'react';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import { useCookies } from 'react-cookie';
import { Routes, Route } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import './App.css';
import { Chart, registerables } from 'chart.js';
import { Line } from 'react-chartjs-2';
Chart.register(...registerables);

const Main = () => {
  const [showSplash, setShowSplash] = useState(true);

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
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      },
      {
        label: '# of Times Returning',
        data: [7, 3, 2, 5, 3, 19, 12], //fake data
        fill: false,
        borderColor: 'rgb(192, 75, 192)',
        tension: 0.1
      }
    ],
  };
  
  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="bg-gray-950 w-screen min-h-screen flex flex-col md:flex-row">
      {showSplash && (
        <div className="splash-screen absolute inset-0 flex items-center justify-center z-50 gradient-background">
          <h1 className="text-white font-medium text-4xl">Aves Attendance</h1>
          <PendingActionsIcon className="ml-2" style={{ fontSize: 50, color: 'white' }} />
        </div>
      )}
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className = "font-medium text-red-500 font-custom text-4xl">Andrew</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Andrew" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
      </div>
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className = "font-medium text-green-500 font-custom text-4xl">Kamryn</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Kamryn" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
      </div>
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className = "text-white font-medium font-custom text-4xl">Jordan</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Jordan" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
      </div>
      <div className="md:w-1/4 w-full flex flex-col items-center">
        <h1 className = "text-white font-medium font-custom text-4xl">Nick</h1>
        <div className="w-5/6 h-64 border border-white mt-2 flex items-center justify-center rounded-xl">
          <img src="path/to/your/image.jpg" alt="Nick" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={data} options={options} />
        </div>
      </div>
    </div>
  );
};

export default Main;


