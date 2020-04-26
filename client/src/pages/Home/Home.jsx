import React, { useEffect, useState, useRef } from 'react';
import Proptypes from 'prop-types';

import socketIOClient from 'socket.io-client';
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps';
import HeatmapLayer from 'react-google-maps/lib/components/visualization/HeatmapLayer';

import {
  Flex,
  PseudoBox,
  Button,
  Text,
  List,
  ListItem,
  ListIcon,
  Progress,
  Divider,
} from '@chakra-ui/core';

import styles from './Home.module.scss';

import { API_URL, GOOGLE_MAPS_API_KEY } from '../../environment';
import { userLogout } from '../../services/userService';

const Map = withScriptjs(withGoogleMap(({ results }) => {
  const data = results.map(({ lat, lng, tweets }) => ({
    location: new window.google.maps.LatLng(lat, lng),
    weight: tweets.length,
  }));
  return (
    <GoogleMap
      defaultZoom={5}
      defaultCenter={{ lat: 4.1156735, lng: -72.9301367 }}
    >
      <HeatmapLayer data={data} radius={20} />
    </GoogleMap>
  );
}));

const googleMapURL = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=visualization`;
const socket = socketIOClient(API_URL);

/**
 * TEST:
  {
    tweetsAcum: 3,
    results: [{
      city: 'Armenia, Quindio, Colombia',
      tweets: 3,
    }],
  }
*/
function Home({ userEmail, logout }) {
  const [searchData, setSearchData] = useState({
    status: '',
    tweetsAcum: 0,
    results: [],
  });
  const [query, setQuery] = useState('');

  const handleOnTweets = ({ status, data }) => {
    if (status === 'processing') {
      const { city, tweets } = data;
      // console.log('tweets =>', tweets);
      setSearchData({
        status,
        tweetsAcum: searchData.tweetsAcum + tweets.length,
        results: [
          {
            city: city.formatted_address,
            lat: Number(city.geometry.location.lat),
            lng: Number(city.geometry.location.lng),
            tweets: tweets.length,
          },
          ...searchData.results,
        ],
      });
    }
    if (status === 'finished') {
      setSearchData({
        ...searchData,
        status,
      });
    }
  };

  useEffect(() => {
    socket.on('tweets', handleOnTweets);
    return () => socket.off('tweets');
  });

  const handleLogout = async () => {
    try {
      await userLogout();
      logout(null);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    socket.emit('search', JSON.stringify({ query }));
  };

  const isProcesing = searchData.status === 'processing';

  return (
    <div className={styles.container}>
      <Flex flexWrap="wrap" justifyContent="space-between" alignItems="center" marginBottom="6">
        <h1 className={styles.title}>Sentime</h1>
        <div className={styles.right}>
          <Text textAlign="center">
            {userEmail}
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
        onSubmit={handleSearch}
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
          disabled={isProcesing}
        />
        <Button
          type="submit"
          variantColor="teal"
          size="md"
          marginLeft="3"
          disabled={isProcesing}
        >
          Buscar
        </Button>
      </Flex>
      <Flex flexWrap="wrap">
        <Map
          results={searchData.results}
          googleMapURL={googleMapURL}
          loadingElement={<div style={{ height: '100%', maxWidth: 700 }} />}
          containerElement={(
            <div style={{
              flex: 7, marginTop: 12, height: '500px', maxWidth: 700,
            }}
            />
          )}
          mapElement={<div style={{ height: '100%', maxWidth: 700 }} />}
        />
        {(searchData.results.length > 0 || isProcesing) && (
        <Flex flexDirection="column" flex="3" padding="12px">
          <Progress
            color="teal"
            isAnimated={isProcesing}
            hasStripe={isProcesing}
            value={(searchData.results.length / 32) * 100}
            marginBottom="3"
          />
          <Text>{`Estado: ${searchData.status === 'processing' ? 'En proceso' : 'Finalizado'}`}</Text>
          <Text>{`Departamentos: ${searchData.results.length} de 32`}</Text>
          <Text>{`Total: ${searchData.tweetsAcum} tweets`}</Text>
          <Divider />
          <List spacing={3} height="400px" overflow="scroll">
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
  userEmail: Proptypes.string.isRequired,
  logout: Proptypes.func.isRequired,
};

export default Home;
