import React from 'react';
import PropTypes from 'prop-types';
import { Link, useLocation } from 'react-router-dom';

import {
  Flex,
  Text,
  Button,
} from '@chakra-ui/core';

import { userLogout } from '../services/userService';

function Appbar({ userData, logout }) {
  const location = useLocation();

  console.log(userData);

  const handleLogout = async () => {
    try {
      await userLogout();
      logout(null);
    } catch (err) {
      console.log(err);
    }
  };

  const routes = [
    { name: 'Búsqueda', path: '/search' },
    { name: 'Historial', path: '/history' },
    { name: 'Repositorio', path: '/allhistory' },
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
        <Text textAlign="center" marginLeft="2" maxWidth="140px" isTruncated>{userData.email}</Text>
        <Button marginLeft="2" variantColor="pink" variant="outline" onClick={handleLogout}>Salir</Button>
      </Flex>
    </Flex>
  );
}

Appbar.propTypes = {
  userData: PropTypes.shape({
    id: PropTypes.number.isRequired,
    email: PropTypes.string.isRequired,
  }).isRequired,
  logout: PropTypes.func.isRequired,
};

export default Appbar;
