import React from 'react';
import Proptypes from 'prop-types';
import { Link, useLocation } from 'react-router-dom';

import {
  Flex,
  Text,
  Button,
} from '@chakra-ui/core';

import { userLogout } from '../services/userService';

function Appbar({ userEmail, logout }) {
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await userLogout();
      logout(null);
    } catch (err) {
      console.log(err);
    }
  };

  const routes = [
    { name: 'Búsqueda', path: '/home' },
    { name: 'Historial', path: '/history' },
  ];

  return (
    <Flex flexWrap="wrap" justifyContent="space-between" alignItems="center" marginBottom="6">
      <Text fontSize="4xl">Sentime</Text>
      <Flex flex="2" justifyContent="flex-end" alignItems="center">
        {routes.map(({ name, path }) => (
          <Button
            key={path}
            marginLeft="2"
            variantColor="teal"
            variant={location.pathname.includes(path) ? 'solid' : 'outline'}
            as={Link}
            to={path}
          >
            {name}
          </Button>
        ))}
        <Text textAlign="center" marginLeft="2">{userEmail}</Text>
        <Button marginLeft="2" variantColor="pink" variant="outline" onClick={handleLogout}>Salir</Button>
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
