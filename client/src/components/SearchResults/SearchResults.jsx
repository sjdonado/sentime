import React, { useState } from 'react';
import PropTypes from 'prop-types';

import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps';
import HeatmapLayer from 'react-google-maps/lib/components/visualization/HeatmapLayer';
import { Pie, Bar } from 'react-chartjs-2';

import {
  Flex,
  Text,
  List,
  ListItem,
  ListIcon,
  Progress,
  Divider,
  Button,
  CloseButton,
} from '@chakra-ui/core';

import { GOOGLE_MAPS_API_KEY } from '../../environment';

import styles from './SearchResults.module.scss';

const Map = withScriptjs(withGoogleMap(({ results }) => {
  const data = results.map(({ lat, lng, scores }) => ({
    location: new window.google.maps.LatLng(Number(lat), Number(lng)),
    weight: scores.positive,
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

const cleanCity = (city) => city.replace(', Colombia', '').replace(' Province', '').replace(' Department', '')

function SearchResults({
  data,
  isProcesing,
  status,
}) {
  const [selectedRow, setSelectedRow] = useState();
  const [toggleView, setToggleView] = useState(false);

  return (
    <Flex flexWrap="wrap">
      <Flex flex="7" flexDirection="column" padding="6px">
        <Button
          variantColor="teal"
          variant="outline"
          size="sm"
          onClick={() => setToggleView(!toggleView)}
        >
          {toggleView ? 'Ver mapa de calor' : 'Ver diagráma de barras'}
        </Button>
        {toggleView ? (
          <Flex flexDirection="column">
            <Text
              margin="2"
              width="100%"
              textAlign="center"
              fontWeight="bold"
            >
              Diagráma de barras: Clasificación de los tweets encontrados en Colombia 
            </Text>
            <Bar
              className={styles.chart}
              data={{
                labels: ['Positivos', 'Negativos', 'Neutrales'],
                datasets: [{
                  label: 'Cantidad',
                  data: [
                    data.reduce((acum, { scores }) => acum + scores.positive, 0),
                    data.reduce((acum, { scores }) => acum + scores.negative, 0),
                    data.reduce((acum, { scores }) => acum + scores.neutral, 0),
                  ],
                  backgroundColor: 'rgba(255,99,132,0.2)',
                  borderColor: 'rgba(255,99,132,1)',
                  borderWidth: 1,
                  hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                  hoverBorderColor: 'rgba(255,99,132,1)',
                }],
              }}
            />
          </Flex>
        ) : (
          <Flex flexDirection="column">
            <Text
              margin="2"
              width="100%"
              textAlign="center"
              fontWeight="bold"
            >
              Mapa de calor: Clasificación de los tweets encontrados en todos los departamentos de Colombia (rojo/positivos)
            </Text>
            <Map
              results={data}
              googleMapURL={googleMapURL}
              loadingElement={<div className={styles.map} />}
              containerElement={<div className={styles.map} />}
              mapElement={<div className={styles.map} />}
            />
          </Flex>
        )}
      </Flex>
      <Flex flexDirection="column" flex="3" padding="6px">
        {selectedRow && (
          <Flex
            flex="4"
            flexDirection="column"
            justifyContent="flex-start"
            alignItems="flex-end"
            border="1px solid #E2E8F0"
            padding="2"
            borderRadius="4px"
            marginBottom="12px"
          >
            <Flex>
              <Text
                margin="2"
                width="100%"
                textAlign="center"
                fontWeight="bold"
              >
                Clasificación para este departamento
              </Text>
              <CloseButton
                size="lg"
                onClick={() => setSelectedRow(null)}
              />
            </Flex>
            <Text width="100%" textAlign="center" marginTop="2" marginBottom="4">{selectedRow.city}</Text>
            <Pie
              className={styles.chart}
              data={{
                labels: ['Positivos', 'Negativos', 'Neutrales'],
                datasets: [{
                  data: [
                    selectedRow.scores.positive,
                    selectedRow.scores.negative,
                    selectedRow.scores.neutral,
                  ],
                  backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                  ],
                  borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                  ],
                  borderWidth: 1,
                }],
              }}
            />
          </Flex>
        )}
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
        <List spacing={3} height="450px" overflow="scroll">
          {data.map(({ city, total, scores }) => (
            <ListItem className={styles.statistic}>
              <ListIcon icon="check-circle" color="green.500" />
              <Flex className={styles['list-item-container']} justifyContent="flex-end" width="100%">
                <Flex alignItems="center" justifyContent="space-between" width="100%">
                  <Text>{cleanCity(city)}</Text>
                  <Text>{`${total} tweets`}</Text>
                </Flex>
                <Button
                  size="sm"
                  variantColor="teal"
                  variant="solid"
                  onClick={() => setSelectedRow({ city, scores })}
                >
                  Detalles
                </Button>
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
