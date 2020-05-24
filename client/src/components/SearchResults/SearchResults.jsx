import React from 'react';
import PropTypes from 'prop-types';

import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps';
import HeatmapLayer from 'react-google-maps/lib/components/visualization/HeatmapLayer';

import {
  Flex,
  Text,
  List,
  ListItem,
  ListIcon,
  Progress,
  Divider,
} from '@chakra-ui/core';

import { GOOGLE_MAPS_API_KEY } from '../../environment';

import styles from './SearchResults.module.scss';

const Map = withScriptjs(withGoogleMap(({ results }) => {
  const data = results.map(({ lat, lng, scores }) => ({
    location: new window.google.maps.LatLng(Number(lat), Number(lng)),
    weight: scores.pos_score,
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

function SearchResults({
  data,
  isProcesing,
  status,
}) {
  return (
    <Flex flexWrap="wrap">
      <Map
        results={data}
        googleMapURL={googleMapURL}
        loadingElement={<div className={styles.map} />}
        containerElement={<div className={styles.map} />}
        mapElement={<div className={styles.map} />}
      />
      <Flex flexDirection="column" flex="3" padding="12px">
        <Progress
          color="teal"
          isAnimated={isProcesing}
          hasStripe={isProcesing}
          value={(data.length / 32) * 100}
          marginBottom="3"
        />
        <Text>{`Estado: ${status === 'processing' ? 'En proceso' : 'Finalizado'}`}</Text>
        <Text>{`Departamentos: ${data.length} de 32`}</Text>
        <Text>{`Total: ${data.reduce((acum, elem) => acum + elem.total, 0)} tweets`}</Text>
        <Divider />
        <List spacing={3} height="400px" overflow="scroll">
          {data.map(({ city, total }) => (
            <ListItem className={styles.statistic}>
              <ListIcon icon="check-circle" color="green.500" />
              <Flex justifyContent="space-between" width="100%">
                <Text>{city.replace(', Colombia', '')}</Text>
                <Text>{`${total} tweets`}</Text>
              </Flex>
            </ListItem>
          ))}
        </List>
      </Flex>
    </Flex>
  );
}

SearchResults.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape({
    city: PropTypes.string,
    total: PropTypes.number,
    lat: PropTypes.number,
    lng: PropTypes.number,
    scores: PropTypes.number,
  })).isRequired,
  isProcesing: PropTypes.bool,
  status: PropTypes.string,
};

SearchResults.defaultProps = {
  isProcesing: false,
  status: 'finished',
};

export default SearchResults;
