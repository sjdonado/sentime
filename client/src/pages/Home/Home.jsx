import React, { useEffect, useState } from 'react';
import Proptypes from 'prop-types';

import socketIOClient from 'socket.io-client';
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps';
// import HeatmapLayer from "react-google-maps/lib/components/visualization/HeatmapLayer";

import {
  Flex,
  PseudoBox,
  Button,
  Text,
  List,
  ListItem,
  ListIcon,
  Progress,
} from '@chakra-ui/core';

import styles from './Home.module.scss';

import { API_URL, GOOGLE_MAPS_API_KEY } from '../../environment';
import { logout } from '../../services/userService';

const Map = withScriptjs(withGoogleMap(() => (
  <GoogleMap
    defaultZoom={5}
    defaultCenter={{ lat: 4.1156735, lng: -72.9301367 }}
  />
)));

const googleMapURL = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=visualization`;
const socket = socketIOClient(API_URL);

function Home(props) {
  const [searchData, setSearchData] = useState({
    tweetsAcum: 0,
    results: [{
      city: 'Armenia, Quindio, Colombia',
      tweets: 3,
    }],
  });
  const [query, setQuery] = useState('');

  const handleOnTweets = ({ status, data }) => {
    if (status === 'processing') {
      const { city, tweets } = data;
      console.log('tweets =>', tweets);
      setSearchData({
        tweetsAcum: searchData.tweetsAcum + tweets.length,
        results: [
          ...searchData.results,
          {
            city: city.formatted_address,
            tweets: tweets.length,
          },
        ],
      });
      // heatmapData.push({
      //   location: new google.maps.LatLng(Number(city.geometry.location.lat), Number(city.geometry.location.lng)),
      //   weight: tweets.length,
      // });
    }
  };

  useEffect(() => {
    socket.on('tweets', handleOnTweets);
    return () => socket.off('tweets');
  });

  const handleLogout = async () => {
    try {
      await logout();
      props.logout(null);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSearch = (e) => {
    e.preventDevault();
    socket.emit('search', JSON.stringify({ query }));
  };

  return (
    <div className={styles.container}>
      <Flex flexWrap="wrap" justifyContent="space-between" alignItems="center" marginBottom="6">
        <h1 className={styles.title}>Sentime</h1>
        <div className={styles.right}>
          <Text textAlign="center">
            test@test.com
          </Text>
          <Button variantColor="teal" variant="outline" onClick={handleLogout}>Salir</Button>
        </div>
      </Flex>
      <Flex
        as="form"
        width={[
          '100%', // base
          '75%', // 480px upwards
          '50%', // 768px upwards
          '40%', // 992px upwards
        ]}
        alignItems="center"
      >
        <PseudoBox
          as="input"
          placeholder="Persona, producto o servicio"
          type="text"
          flex="1"
          py={2}
          px={4}
          rounded="md"
          bg="gray.100"
          borderWidth="1px"
          _hover={{ borderColor: 'gray.200', bg: 'gray.200' }}
          _focus={{
            outline: 'none',
            bg: 'white',
            boxShadow: 'outline',
            borderColor: 'gray.300',
          }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={searchData.results.length > 0}
        />
        <Button
          variantColor="teal"
          size="md"
          marginLeft="3"
          onClick={handleSearch}
          disabled={searchData.results.length > 0}
        >
          Buscar
        </Button>
      </Flex>
      <Flex flexWrap="wrap">
        <Map
          googleMapURL={googleMapURL}
          loadingElement={<div style={{ height: '100%', maxWidth: 700 }} />}
          containerElement={(
            <div style={{
              flex: 7, marginTop: 12, height: '400px', maxWidth: 700,
            }}
            />
          )}
          mapElement={<div style={{ height: '100%', maxWidth: 700 }} />}
        />
        {searchData.results.length > 0 && (
        <Flex flexDirection="column" flex="3" padding="12px">
          <Progress color="teal" hasStripe isAnimated value={(searchData.results.length / 32) * 100} marginBottom="3" />
          <Text marginBottom="3">{`Total: ${searchData.tweetsAcum} tweets`}</Text>
          <List spacing={3}>
            {searchData.results.map(({ city, tweets }) => (
              <ListItem className={styles.statistic}>
                <ListIcon icon="check-circle" color="green.500" />
                <Flex justifyContent="space-between" width="100%">
                  <Text>{city}</Text>
                  <Text>{`${tweets} tweets`}</Text>
                </Flex>
              </ListItem>
            ))}
          </List>
        </Flex>
        )}
      </Flex>
    </div>
  );
}

Home.propTypes = {
  logout: Proptypes.func.isRequired,
};

export default Home;
