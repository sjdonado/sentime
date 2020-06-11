import React, { useState } from 'react';
import PropTypes from 'prop-types';

import {
  Flex,
  PseudoBox,
  Button,
  Text,
  Select,
} from '@chakra-ui/core';

import SearchResults from '../../components/SearchResults/SearchResults';

import styles from './Search.module.scss';

const DEFAULT_MESSAGE = 'Haz click en Buscar para empezar tu búsqueda';

function Search({
  searchData,
  startedAt,
  message,
  handleSearch,
}) {
  const [hours, setHours] = useState(0);
  const [query, setQuery] = useState('');

  const isProcesing = searchData.status === 'processing' && searchData.results.length < 32;

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
        onSubmit={(e) => handleSearch(e, query, hours)}
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
            || hours === 0 || (message !== DEFAULT_MESSAGE && isProcesing)}
        >
          Buscar
        </Button>
      </Flex>
      {((searchData.results.length > 0) || isProcesing) ? (
        <SearchResults
          data={searchData.results}
          isProcesing={isProcesing}
          status={searchData.status}
          startedAt={startedAt}
        />
      ) : (
        <Text marginTop="12" textAlign="center">{message}</Text>
      )}
    </>
  );
}

Search.propTypes = {
  searchData: PropTypes.shape({
    results: PropTypes.arrayOf(PropTypes.any).isRequired,
    status: PropTypes.string.isRequired,
  }).isRequired,
  startedAt: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  handleSearch: PropTypes.func.isRequired,
};

export default Search;
