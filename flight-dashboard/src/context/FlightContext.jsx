import React, { createContext, useState, useEffect } from 'react';
import mqttClient from '../utils/mqttClient';

export const FlightContext = createContext();

export const FlightProvider = ({ children }) => {
  const [flights, setFlights] = useState([]);

  useEffect(() => {
    const handleMessage = (topic, message) => {
      try {
        const flightData = JSON.parse(message.toString());
        const newFlight = {
          ...flightData,
          id: flightData.flight_id, // Use flight_id as the unique ID
          top: Math.random() * 60, // Random vertical position within 60% of the screen height
          direction: Math.random() > 0.5 ? 'left-to-right' : 'right-to-left', // Random direction
        };

        setFlights((prevFlights) => [...prevFlights, newFlight]);

        // If the flight is canceled, remove it after 5 seconds
        if (newFlight.status === 'CANCELLED' || newFlight.status === 'BOARDING') {
          setTimeout(() => {
            setFlights((prevFlights) =>
              prevFlights.filter((flight) => flight.id !== newFlight.id)
            );
          }, 8000); // 5 seconds delay
        }
      } catch (error) {
        console.error('Error parsing flight data:', error);
      }
    };

    mqttClient.on('message', handleMessage);

    // Cleanup on unmount
    return () => {
      mqttClient.off('message', handleMessage);
    };
  }, []);

  const completeFlight = (flightId) => {
    setFlights((prevFlights) =>
      prevFlights.filter((flight) => flight.id !== flightId)
    );
  };

  return (
    <FlightContext.Provider value={{ flights, completeFlight }}>
      {children}
    </FlightContext.Provider>
  );
};