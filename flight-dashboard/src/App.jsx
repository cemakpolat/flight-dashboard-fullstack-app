import React from 'react';
import { FlightProvider } from './context/FlightContext';
import AppLayout from './components/AppLayout/AppLayout';

function App() {
  return ( 
    <FlightProvider>
      <AppLayout />
    </FlightProvider>
  );
}

export default App;