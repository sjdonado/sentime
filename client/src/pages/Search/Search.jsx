import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import socketIOClient from 'socket.io-client';

import {
  Flex,
  PseudoBox,
  Button,
  Text,
} from '@chakra-ui/core';

// import styles from './Search.module.scss';

import { API_URL } from '../../environment';
import SearchResults from '../../components/SearchResults/SearchResults';

const socket = socketIOClient(API_URL);

const DEFAULT_MESSAGE = 'Haz click en Buscar para empezar tu búsqueda';

function Search({ userData }) {
  const [searchData, setSearchData] = useState({
    status: '',
    tweetsAcum: 0,
  });
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
        console.log('total tweets =>', total, 'scores =>', scores);
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
    socket.emit('search', JSON.stringify({ query, hours: 2 }));
    setMessage('Búsqueda enviada!, esperando aprobación...');
  };

  const isProcesing = searchData.status === 'processing';

  return (
    <>
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
          disabled={isProcesing || (query && query.length === 0) || message !== DEFAULT_MESSAGE}
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
        <Text marginTop="6" textAlign="center">{message}</Text>
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
