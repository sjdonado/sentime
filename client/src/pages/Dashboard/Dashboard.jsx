import React, { useEffect, useState } from 'react';
import Proptypes from 'prop-types';

import socketIOClient from 'socket.io-client';
// import { GoogleMap, Marker } from "react-google-maps"
// import HeatmapLayer from "react-google-maps/lib/components/visualization/HeatmapLayer";

import {
  Button,
} from '@chakra-ui/core';

import styles from './Dashboard.module.scss';

import { API_URL } from '../../environment';
import { logout } from '../../services/userService';

function Dashboard(props) {
  const [response, setResponse] = useState('');

  useEffect(() => {
    const socket = socketIOClient(API_URL);
    socket.on('tweets', (data) => {
      setResponse(data);
    });
  }, []);

  console.log('response', response);

  const handleLogout = async () => {
    try {
      await logout();
      props.logout(null);
    } catch (err) {
      console.log(err);
    }
  };
  return (
    <div>
      <div className={styles.header}>
        <h1 className={styles.title}>Sentime</h1>
        <div className={styles.right}>
          <span>test@test.com</span>
          <Button onClick={handleLogout}>Logout</Button>
        </div>
      </div>
    </div>
  );
}

Dashboard.propTypes = {
  logout: Proptypes.func.isRequired,
};

export default Dashboard;
