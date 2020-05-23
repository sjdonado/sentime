import React, { useEffect, useState } from 'react';

import {
  Flex,
  Text,
  List,
  ListItem,
  ListIcon,
  Divider,
} from '@chakra-ui/core';

import styles from './History.module.scss';
import { getHistory } from '../../services/userService';


function History() {
  const [searches, setSearches] = useState([]);

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


  return (
    <>
      <List spacing={3} height="400px" overflow="scroll">
        {searches.map(({ id, query }) => (
          <ListItem className={styles.statistic}>
            <ListIcon icon="check" />
            <Flex justifyContent="space-between" width="100%">
              <Text>{id}</Text>
              <Text>{`${query}`}</Text>
            </Flex>
          </ListItem>
        ))}
      </List>
      <Text fontSize="6xl">History</Text>
      <Flex flexDirection="column" flex="3" padding="12px">
        <Text>Resultados</Text>
        <Text>Departamentos: 32 de 32</Text>
        {/* <Text>{`Total: ${searchData.tweetsAcum} tweets`}</Text> */}
        <Divider />
        {/* <List spacing={3} height="400px" overflow="scroll">
          {searchData.results.map(({ city, tweets }) => (
            <ListItem className={styles.statistic}>
              <ListIcon icon="check-circle" color="green.500" />
              <Flex justifyContent="space-between" width="100%">
                <Text>{city}</Text>
                <Text>{`${tweets} tweets`}</Text>
              </Flex>
            </ListItem>
          ))}
        </List> */}
      </Flex>
    </>
  );
}

export default History;
