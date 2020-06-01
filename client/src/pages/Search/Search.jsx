import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import socketIOClient from 'socket.io-client';

import {
  Flex,
  PseudoBox,
  Button,
  Text,
  Select,
} from '@chakra-ui/core';

// import styles from './Search.module.scss';

import { SOCKET_IO_URL } from '../../environment';
import SearchResults from '../../components/SearchResults/SearchResults';

import styles from './Search.module.scss';

const socket = socketIOClient(SOCKET_IO_URL);

const DEFAULT_MESSAGE = 'Haz click en Buscar para empezar tu búsqueda';

function Search({ userData }) {
  const [searchData, setSearchData] = useState({
    status: '',
    results: [],
  });
  const [hours, setHours] = useState(0);
  const [query, setQuery] = useState('');
  const [message, setMessage] = useState(DEFAULT_MESSAGE);

  const handleOnTweets = ({ id, status, data }) => {
    if (id === userData.id) {
      if (status === 'started') {
        setMessage('Búsqueda aceptada, obteniendo resultados...');
      }
      if (status === 'task_in_progress') {
        setMessage('Tienes una búsqueda en progreso, obteniendo resultados...');
      }
      if (status === 'denied') {
        setMessage('Búsqueda rechazada :(, intenta de nuevo más tarde');
      }
      if (status === 'processing') {
        const {
          city,
          lat,
          lng,
          total,
          scores,
        } = data;
        setSearchData({
          status,
          results: [
            {
              city,
              lat,
              lng,
              total,
              scores,
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
    }
  };

  useEffect(() => {
    socket.on('tweets', handleOnTweets);
    return () => socket.off('tweets');
  });

  const handleSearch = (e) => {
    e.preventDefault();
    socket.emit('search', JSON.stringify({ query, hours }));
    setMessage('Búsqueda enviada, esperando respuesta del servidor...');
  };

  const isProcesing = searchData.status === 'processing';

  return (
    <>
      <Flex
        as="form"
        width={[
          '100%', // base
          '85%', // 480px upwards
          '60%', // 768px upwards
          '50%', // 992px upwards
        ]}
        alignItems="center"
        marginBottom="2"
        onSubmit={handleSearch}
      >
        <PseudoBox
          as="input"
          placeholder="Persona, producto o servicio"
          type="text"
          flex="1"
          py={2}
          px={4}
          color="gray.600"
          rounded="md"
          borderWidth="1px"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={isProcesing}
        />
        <Select
          className={styles.select}
          color="gray.600"
          onChange={(e) => setHours(Number(e.target.value))}
          placeholder="Seleccione intervalo de horas"
          width="270px"
        >
          <option value="2">&lt; 2 Horas</option>
          <option value="8">&lt; 8 Horas</option>
          <option value="24">&lt; 24 Horas</option>
        </Select>
        <Button
          type="submit"
          variantColor="teal"
          size="md"
          marginLeft="3"
          disabled={isProcesing || (query && query.length === 0)
            || hours === 0 || message !== DEFAULT_MESSAGE}
        >
          Buscar
        </Button>
      </Flex>
      {((searchData && searchData.results && searchData.results.length > 0) || isProcesing) ? (
        <SearchResults
          data={searchData.results}
          isProcesing={isProcesing}
          status={searchData.status}
        />
      ) : (
        <Text marginTop="12" textAlign="center">{message}</Text>
      )}
    </>
  );
}

Search.propTypes = {
  userData: PropTypes.shape({
    id: PropTypes.number.isRequired,
    email: PropTypes.string.isRequired,
  }).isRequired,
};

export default Search;
