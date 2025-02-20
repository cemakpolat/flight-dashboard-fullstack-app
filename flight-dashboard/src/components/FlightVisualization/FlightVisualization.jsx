import React, { useContext } from 'react';
import { FlightContext } from '../../context/FlightContext';
import './FlightVisualization.css';


const FlightVisualization = () => {
  const { flights, completeFlight } = useContext(FlightContext);

  // Filter out canceled flights

  
  const activeFlights = flights.filter((flight) => (flight.status !== 'CANCELLED' && flight.status !== 'BOARDING'));

  console.log('Active flights:', activeFlights); // Debugging: Log active flights

  return (
    <div className="visualization">
      {activeFlights.map((flight) => {
        const animationName =
          flight.direction === 'left-to-right' ? 'moveLeftToRight' : 'moveRightToLeft';
        const isRightToLeft = flight.direction === 'right-to-left';
        return (
          <div
            key={flight.id}
            className="airplane"
            style={{
              left: flight.direction === 'left-to-right' ? '0%' : '100%',
              top: `${flight.top}vh`,
              animation: `${animationName} ${flight.duration}s linear`,
              transform: `translate(-50%, -50%) ${isRightToLeft ? 'scaleX(-1)' : ''}`,
            }}
            onAnimationEnd={() => completeFlight(flight.id)}
          >
            ✈️
          </div>
        );
      })}
    </div>
  );
};

export default FlightVisualization;