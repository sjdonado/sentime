import React, { useState } from 'react';
import Proptypes from 'prop-types';

import {
  Text,
  Input,
  FormControl,
  FormLabel,
  Button,
  Flex,
  useToast,
  Box,
  Heading,
  Checkbox,
} from '@chakra-ui/core';

import styles from './Landing.module.scss';

import { login } from '../../services/userService';


function Landing({ setUserData }) {
  const toast = useToast();

  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const { email, password } = formData;
      const { data } = await login(email, password);
      setUserData(data.id, data.email);
    } catch ({ message }) {
      toast({
        title: message,
        status: 'error',
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };


  return (
    <div className={styles.container}>
      <Flex className={styles.lower} justifyContent="space-between">
        <Flex flexDirection="column" paddingRight="92px">
          <Heading as="h2" size="xl" color="white">Sentime</Heading>
          <Text fontSize="2xl" color="white">Analiza los tweets colombianos</Text>
          <Box
            as="iframe"
            title="naruto"
            src="https://www.youtube.com/embed/aKqyobR9_aA"
            allowFullScreen
            minH="350px"
            marginTop="40px"
            marginBottom="40px"
          />
          <Text fontSize="md" color="white">
            Sentime se encarga de buscar por ti tweets en los 32 departamentos
            de Colombia, sólo necesitas ingresar una palabra, seleccionar el intervalo
            de horas y hacer click en buscar!
          </Text>
        </Flex>
        <Flex flexDirection="column" justifyContent="flex-start" width="100%">
          <Box className={styles['login-box']} rounded="lg" overflow="hidden">
            <Text fontSize="lg">¿Ya tienes cuenta?</Text>
            <Heading marginBottom="30px" fontSize="3xl">Iniciar Sesión</Heading>
            <FormControl className={styles['form-control']}>
              <FormLabel htmlFor="email">Correo electrónico</FormLabel>
              <Input
                type="email"
                name="email"
                value={formData.email}
                aria-describedby="email-helper-text"
                onChange={handleInputChange}
                placeholder="Ingresa tu correo electrónico"
              />
            </FormControl>
            <FormControl className={styles['form-control']}>
              <FormLabel htmlFor="password">Contraseña</FormLabel>
              <Input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Ingresa tu contraseña"
              />
            </FormControl>
            <Checkbox marginBottom="20px" marginTop="10px"> Mantener sesión abierta</Checkbox>
            <Button
              className={styles['submit-btn']}
              isLoading={isLoading}
              loadingText="Submitting"
              variantColor="teal"
              onClick={handleSubmit}
              width="100%"
              marginTop="20px"
              marginBottom="40px"
            >
              Ingresar
            </Button>
            <Text>¿No tienes una cuenta aún?</Text>
            <Text style={{ cursor: 'pointer' }} className={styles.demo} onClick={() => window.open('mailto:pastorizoj@uninorte.edu.co?subject=Solicitud%20demo%20Sentime', '_blank')}>Solicita una demo</Text>
          </Box>
        </Flex>
      </Flex>
    </div>
  );
}

Landing.propTypes = {
  setUserData: Proptypes.func.isRequired,
};

export default Landing;
