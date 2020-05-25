import React, { useEffect, useState } from 'react';

import {
  Text,
  Flex,
  Button,
} from '@chakra-ui/core';

import styles from './History.module.scss';
import { getHistory } from '../../services/userService';

import Table from '../../components/Table';
import SearchResults from '../../components/SearchResults/SearchResults';

const columns = [
  {
    Header: 'Identificador',
    accessor: 'id',
  },
  {
    Header: 'Texto buscado',
    accessor: 'query',
  },
  {
    Header: 'Fecha',
    accessor: 'created_at',
  },
];

function History() {
  const [searches, setSearches] = useState([]);
  const [selectedSearch, setSelectedSearch] = useState();

  useEffect(() => {
    async function fetch() {
      if (searches.length === 0) {
        try {
          const { data } = await getHistory();
          setSearches(data);
          console.log(data);
        } catch (err) {
          console.log(err);
        }
      }
    }
    fetch();
  }, [searches, setSearches]);

  const handleRowClick = (e) => {
    let el = e.target;
    while (!Object.prototype.hasOwnProperty.call(el.dataset, 'rowindex')) el = el.parentNode;
    setSelectedSearch(searches[el.dataset.rowindex]);
  };

  return (
    <>
      <Text className={styles.title} fontSize="3xl">Historial de búsqueda</Text>
      {selectedSearch && (
        <Flex flexDirection="column">
          <Flex flexDirection="row" justifyContent="space-between" alignItems="center">
            <Flex>
              <Text fontWeight="bold" marginRight="2">Texto buscado:</Text>
              <Text>{selectedSearch.query}</Text>
            </Flex>
            <Button
              variantColor="teal"
              variant="outline"
              size="sm"
              marginBottom="3"
              onClick={() => setSelectedSearch(null)}
            >
              Cerrar
            </Button>
          </Flex>
          <SearchResults data={selectedSearch.results} />
        </Flex>
      ) }
      <Table
        className={styles['history-table']}
        columns={columns}
        data={searches}
        onRowClick={handleRowClick}
      />
    </>
  );
}

export default History;
