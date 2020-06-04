import React from 'react';

import {
  Flex,
  Text,
} from '@chakra-ui/core';

function Banner() {
  return (
    <Flex
      backgroundColor="#008080"
      flexWrap="wrap"
      justifyContent="center"
      alignItems="center"
    >
      <Text color="white" fontSize="sm">
        Proyecto final desarrollado por John Fontalvo y Juan Rodríguez.
        Agradecimientos especiales a Emanuel Afanador | Universidad del Norte.
      </Text>
    </Flex>
  );
}


export default Banner;
