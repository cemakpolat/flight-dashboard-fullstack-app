import React, { useContext } from 'react';
import { FlightContext } from '../../context/FlightContext';
import './FlightTable.css';

const FlightTable = () => {
  const { flights } = useContext(FlightContext);

  return (
    <table className="flight-table">
      <thead>
        <tr>
          <th>Flight ID</th>
          <th>Boarding</th>
          <th>Altitude (ft)</th>
          <th>Fuel (%)</th>
          <th>Issue</th>
          <th>Status</th>
          <th>Current Hub</th>
          <th>Target Hub</th>
          <th>Transition Hub</th>
        </tr>
      </thead>
      <tbody>
        {flights.map((flight) => {
          let statusClass = '';

          switch (flight.status) {
            case 'DELAYED':
              statusClass = 'delayed';
              break;
            case 'CANCELLED':
              statusClass = 'cancelled';
              break;
            case 'DIVERTED':
              statusClass = 'diverted'; // Added class for diverted status
              break;
            case 'BOARDING':
              statusClass = 'boarding';
              break;
            default:
              statusClass = ''; // No special class for other statuses
          }

          return (
            <tr key={flight.flight_id}>
              <td>{flight.flight_id}</td>
              <td>{flight.boarding_complete ? 'Complete' : 'Incomplete'}</td>
              <td>{flight.altitude}</td>
              <td>{flight.fuel_level}</td>
              <td>{flight.current_issue}</td>
              <td className={statusClass}>{flight.status}</td>
              <td>{flight.current_hub}</td>
              <td>{flight.target_hub}</td>
              <td>{flight.transition_hub}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default FlightTable;