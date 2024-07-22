import React, { useState, useEffect } from 'react';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import BuildOutlinedIcon from '@mui/icons-material/BuildOutlined';
import { Line } from 'react-chartjs-2';
import './App.css';
import { Chart, registerables } from 'chart.js';
import io from 'socket.io-client';

Chart.register(...registerables);

const Statistic = ({ label, value }) => (
  <div className="text-center mb-2">
    <h2 className="text-white text-2xl font-bold">{value}</h2>
    <hr className="rainbow-gradient" />
    <p className="text-white text-sm">{label}</p>
  </div>
);

const socket = io('http://localhost:5000');

const Main = () => {
  const [showSplash, setShowSplash] = useState(true);
  const [andrewData, setAndrewData] = useState({});
  const [kamrynData, setKamrynData] = useState({});
  const [jordanData, setJordanData] = useState({});
  const [nickData, setNickData] = useState({});
  const [andrewImage, setAndrewImage] = useState('')
  const [kamrynImage, setKamrynImage] = useState('')
  const [jordanImage, setJordanImage] = useState('')
  const [nickImage, setNickImage] = useState('')
  const [manualChange, setManualChange] = useState(1);
  const [socketChange, setSocketChange] = useState(0);

    useEffect(() => {
      socket.on('db_change', data => {
        setSocketChange(prev => prev + data); // Increment socketChange state to trigger re-fetch
      });

      return () => {
        socket.off('db_change'); // Clean up the listener on component unmount
      };
    }, []);

    useEffect(() => {
      fetch('/api/stat?name=Andrew') // ? passes in the get request arg
        .then(response => response.json())
        .then(data => setAndrewData(data))
        .catch(error => console.error('Error:', error));

      fetch('/api/image?name=Andrew')// => call to api, api calls to func, func calls to image path, flask send_file converts path to img url, use url here
        .then(response => response.blob())
        .then(images => {
          let imgStatus = URL.createObjectURL(images);
          setAndrewImage(imgStatus);
        })
        .catch(error => console.error('Error:', error));
    }, [manualChange, socketChange]);
    
    useEffect(() => {
      fetch('/api/stat?name=Kamryn')
        .then(response => response.json())
        .then(data => setKamrynData(data))
        .catch(error => console.error('Error:', error));

      fetch('/api/image?name=Kamryn')// => call to api, api calls to func, func calls to image path, flask send_file converts path to img url, use url here
        .then(response => response.blob())
        .then(images => {
          let imgStatus = URL.createObjectURL(images);
          setKamrynImage(imgStatus);
        })
        .catch(error => console.error('Error:', error));
    }, [manualChange, socketChange]);
    
    useEffect(() => {
      fetch('/api/stat?name=Jordan')
        .then(response => response.json())
        .then(data => setJordanData(data))
        .catch(error => console.error('Error:', error));

      fetch('/api/image?name=Jordan')// => call to api, api calls to func, func calls to image path, flask send_file converts path to img url, use url here
        .then(response => response.blob())
        .then(images => {
          let imgStatus = URL.createObjectURL(images);
          setJordanImage(imgStatus);
        })
        .catch(error => console.error('Error:', error));
    }, [manualChange, socketChange]);
    
    useEffect(() => {
      fetch('/api/stat?name=Nick')
        .then(response => response.json())
        .then(data => setNickData(data))
        .catch(error => console.error('Error:', error));

      fetch('/api/image?name=Nick')// => call to api, api calls to func, func calls to image path, flask send_file converts path to img url, use url here
        .then(response => response.blob())
        .then(images => {
          let imgStatus = URL.createObjectURL(images);
          setNickImage(imgStatus);
        })
        .catch(error => console.error('Error:', error));
    }, [manualChange, socketChange]);
    
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const andrewDataObject = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: '# of Times Leaving',
        data: [andrewData.monday, andrewData.tuesday, andrewData.wednesday, andrewData.thursday, andrewData.friday, andrewData.saturday, andrewData.sunday],
        fill: true, 
        backgroundColor: 'rgba(0, 128, 128, 0.2)', 
        pointBackgroundColor: 'white',
        pointBorderColor: 'white',
        borderColor: 'purple',
        tension: 0.3
      },
    ],
  };
  
  const kamrynDataObject = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: '# of Times Leaving',
        data: [kamrynData.monday, kamrynData.tuesday, kamrynData.wednesday, kamrynData.thursday, kamrynData.friday, kamrynData.saturday, kamrynData.sunday],
        fill: true, 
        backgroundColor: 'rgba(0, 128, 128, 0.2)', 
        pointBackgroundColor: 'white',
        pointBorderColor: 'white',
        borderColor: 'purple',
        tension: 0.3
      },
    ],
  };
  
  const jordanDataObject = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: '# of Times Leaving',
        data: [jordanData.monday, jordanData.tuesday, jordanData.wednesday, jordanData.thursday, jordanData.friday, jordanData.saturday, jordanData.sunday],
        fill: true, 
        backgroundColor: 'rgba(0, 128, 128, 0.2)', 
        pointBackgroundColor: 'white',
        pointBorderColor: 'white',
        borderColor: 'purple',
        tension: 0.3
      },
    ],
  };
  
  const nickDataObject = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: '# of Times Leaving',
        data: [nickData.monday, nickData.tuesday, nickData.wednesday, nickData.thursday, nickData.friday, nickData.saturday, nickData.sunday],
        fill: true, 
        backgroundColor: 'rgba(0, 128, 128, 0.2)', 
        pointBackgroundColor: 'white',
        pointBorderColor: 'white',
        borderColor: 'purple',
        tension: 0.3
      },
    ],
  };
  
  const statistics = {
    Andrew: {
      avgTimesLeft: andrewData.avgTimesLeft,
      lastTimeEntered: andrewData.lastEnter,
      lastTimeExited: andrewData.lastExit,
      avgTimeAway: andrewData.avgTimeAway
    },
    Kamryn: {
      avgTimesLeft: kamrynData.avgTimesLeft,
      lastTimeEntered: kamrynData.lastEnter,
      lastTimeExited: kamrynData.lastExit,
      avgTimeAway: kamrynData.avgTimeAway
    },
    Jordan: {
      avgTimesLeft: jordanData.avgTimesLeft,
      lastTimeEntered: jordanData.lastEnter,
      lastTimeExited: jordanData.lastExit,
      avgTimeAway: jordanData.avgTimeAway
    },
    Nick: {
      avgTimesLeft: nickData.avgTimesLeft,
      lastTimeEntered: nickData.lastEnter,
      lastTimeExited: nickData.lastExit,
      avgTimeAway: nickData.avgTimeAway
    }
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

  const handleManualFix = (name) => {
    //determine new status
    let newStatus;
    switch (name) {
      case 'Andrew':
        newStatus = andrewData.status === 'Inside' ? 'Outside' : 'Inside';
        setAndrewData(prevState => ({ ...prevState, status: newStatus })); //creates a new obj with the new changes, obj are immutable, usestates are asynchronous 
        break;
      case 'Kamryn': 
        newStatus = kamrynData.status === 'Inside' ? 'Outside' : 'Inside';
        setKamrynData(prevState => ({ ...prevState, status: newStatus }));
        break;
      case 'Jordan':
        newStatus = jordanData.status === 'Inside' ? 'Outside' : 'Inside';
        setJordanData(prevState => ({ ...prevState, status: newStatus }));
        break;
      case 'Nick':
        newStatus = nickData.status === 'Inside' ? 'Outside' : 'Inside';
        setNickData(prevState => ({ ...prevState, status: newStatus }));
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

    if(manualChange === 1) {
      setManualChange(0);
    } else if(manualChange === 0) {
      setManualChange(1);
    }

  };

  return (
    <div className="bg-gray-900 w-screen min-h-screen flex flex-col md:flex-row">
      {showSplash && (
        <div className="splash-screen absolute inset-0 flex items-center justify-center z-50 gradient-background">
          <h1 className="text-white font-medium text-4xl">Aves Attendance</h1>
          <PendingActionsIcon className="ml-2" style={{ fontSize: 50, color: 'white' }} />
        </div>
      )}
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
        <h1 className={`font-medium font-custom text-4xl ${andrewData.status === 'Inside' ? 'text-green-400' : 'text-red-400'}`}>Andrew</h1> {/*ternary operator: condition ? expressionIfTrue : expressionIfFalse*/}
        <div className="h-64 mt-2 flex items-center justify-center rounded-xl">
          <img src={andrewImage} alt="Andrew" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={andrewDataObject} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Andrew.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Andrew.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Andrew.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Andrew.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Andrew')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12">Manual fix <BuildOutlinedIcon style={{ fontSize: 25, color: 'white' }}/></button>
      </div>
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
      <h1 className={`font-medium font-custom text-4xl ${kamrynData.status === 'Inside' ? 'text-green-400' : 'text-red-400'}`}>Kamryn</h1> {/*ternary operator: condition ? expressionIfTrue : expressionIfFalse*/}
        <div className="h-64 mt-2 flex items-center justify-center rounded-xl">
          <img src={kamrynImage} alt="Kamryn" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={kamrynDataObject} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Kamryn.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Kamryn.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Kamryn.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Kamryn.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Kamryn')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix <BuildOutlinedIcon style={{ fontSize: 25, color: 'white' }}/> </button>
      </div>
      <div className="md:w-1/4 w-full flex flex-col border-b md:border-r-2 md:border-b-2 border-zinc-500 items-center">
      <h1 className={`font-medium font-custom text-4xl ${jordanData.status === 'Inside' ? 'text-green-400' : 'text-red-400'}`}>Jordan</h1> {/*ternary operator: condition ? expressionIfTrue : expressionIfFalse*/}
        <div className="h-64 mt-2 flex items-center justify-center rounded-xl">
          <img src={jordanImage} alt="Jordan" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={jordanDataObject} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Jordan.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Jordan.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Jordan.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Jordan.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Jordan')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix <BuildOutlinedIcon style={{ fontSize: 25, color: 'white' }}/></button>
      </div>
      <div className="md:w-1/4 w-full flex flex-col items-center">
      <h1 className={`font-medium font-custom text-4xl ${nickData.status === 'Inside' ? 'text-green-400' : 'text-red-400'}`}>Nick</h1> {/*ternary operator: condition ? expressionIfTrue : expressionIfFalse*/}
        <div className="h-64 mt-2 flex items-center justify-center rounded-xl">
          <img src={nickImage} alt="Nick" className="max-w-full max-h-full" />
        </div>
        <div className="w-5/6 h-64 mt-2">
          <Line data={nickDataObject} options={options} />
        </div>
        <div className="w-5/6 mt-2 text-white grid grid-cols-2 gap-4">
          <Statistic label="Avg Times Left/day" value={statistics.Nick.avgTimesLeft} />
          <Statistic label="Last Time Entered" value={statistics.Nick.lastTimeEntered} />
          <Statistic label="Last Time Exited" value={statistics.Nick.lastTimeExited} />
          <Statistic label="Average Time Away/day" value={statistics.Nick.avgTimeAway} />
        </div>
        <button onClick={() => handleManualFix('Nick')} className="btn btn-moving-gradient btn-moving-gradient--blue mt-12"> Manual fix <BuildOutlinedIcon style={{ fontSize: 25, color: 'white' }}/></button>
      </div>
    </div>
  );
};

export default Main;