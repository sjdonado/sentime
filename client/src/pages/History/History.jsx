import React, { useEffect, useState } from 'react';

import {
  Text,
  Flex,
  CloseButton,
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
    accessor: 'date',
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
          if (data.length > 0) {
            const parsedData = data.map((elem) => ({
              ...elem,
              date: new Date(elem.created_at).toLocaleString(),
            }));
            setSearches(parsedData);
          }
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
      <Text className={styles.title} fontSize="3xl">Historial personal de búsqueda</Text>
      {selectedSearch && (
        <Flex
          flexDirection="column"
          border="1px solid #E2E8F0"
          borderRadius="4px"
          margin="auto 4px"
          padding="2"
        >
          <Flex
            flexDirection="row"
            justifyContent="space-between"
            alignItems="center"
            borderBottom="1px solid #E2E8F0"
            marginBottom="22px"
          >
            <Flex>
              <Text fontWeight="bold" marginRight="2">Identificador:</Text>
              <Text>{selectedSearch.id}</Text>
            </Flex>
            <Flex>
              <Text fontWeight="bold" marginRight="2">Resultados para el texto buscado:</Text>
              <Text>{selectedSearch.query}</Text>
            </Flex>
            <Flex>
              <Text fontWeight="bold" marginRight="2">Fecha:</Text>
              <Text>{selectedSearch.date}</Text>
            </Flex>
            <CloseButton
              size="lg"
              marginBottom="3"
              onClick={() => setSelectedSearch(null)}
            />
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
