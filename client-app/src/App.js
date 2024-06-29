import React, { useState, useEffect } from 'react';
import './App.css';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import { useCookies } from 'react-cookie';
import { Routes, Route } from 'react-router-dom';

const Main = () => {
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="bg-gray-900 w-screen h-screen flex flex-row">
      {showSplash && (
        <div className="splash-screen absolute inset-0 flex items-center justify-center z-50 gradient-background">
          <h1 className="text-white text-4xl">Aves Attendance</h1>
          <PendingActionsIcon className = "ml-2" style={{ fontSize: 50 }}/>
        </div>
      )}
      <div className="w-1/4 h-full border-r border-white-200">
        <h1>hi</h1>
      </div>
      <div className="w-1/4 h-full border-r border-white-200">
        <h1>hi</h1>
      </div>
      <div className="w-1/4 h-full border-r border-white-200">
        <h1>hi</h1>
      </div>
      <div className="w-1/4 h-full">
        <h1>hi</h1>
      </div>
    </div>
  );
};

export default Main;

