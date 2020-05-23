import React from 'react';
import Proptypes from 'prop-types';
import { Link } from 'react-router-dom';

import {
  Flex,
  Text,
  Button,
} from '@chakra-ui/core';

import { userLogout } from '../services/userService';

function Appbar({ userEmail, logout }) {
  const handleLogout = async () => {
    try {
      await userLogout();
      logout(null);
    } catch (err) {
      console.log(err);
    }
  };


  return (
    <Flex flexWrap="wrap" justifyContent="space-between" alignItems="center" marginBottom="6">
      <Text fontSize="4xl">Sentime</Text>
      <Flex flex="2" justifyContent="flex-end" alignItems="center">
        <Text textAlign="center">
          {userEmail}
        </Text>
        <Button marginLeft="2" variantColor="teal" as={Link} to="/history">Historial</Button>
        <Button marginLeft="2" variantColor="teal" variant="outline" onClick={handleLogout}>Salir</Button>
      </Flex>
    </Flex>
  );
}

Appbar.propTypes = {
  userEmail: Proptypes.string,
  logout: Proptypes.func.isRequired,
};

Appbar.defaultProps = {
  userEmail: '',
};

export default Appbar;
