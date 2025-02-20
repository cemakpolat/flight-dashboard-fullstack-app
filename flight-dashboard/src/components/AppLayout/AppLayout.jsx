import React from 'react';
import FlightVisualization from '../FlightVisualization/FlightVisualization';
import FlightTable from '../FlightTable/FlightTable';
import './AppLayout.css';

const AppLayout = () => {
  return (
    <div className="app-layout">
      <div className="visualization-container">
        <FlightVisualization />
      </div>
      <div className="table-container">
        <FlightTable />
      </div>
    </div>
  );
};

export default AppLayout;