import React, { useState } from 'react';
import Proptypes from 'prop-types';
import ReactPlayer from 'react-player';

import {
  Text,
  Input,
  FormControl,
  FormLabel,
  Button,
  Flex,
  useToast,
} from '@chakra-ui/core';

import styles from './Landing.module.scss';

import { ReactComponent as Analytics } from '../../assets/web-analytics.svg';

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
    <>
      <div className={styles.container}>
        <div className={styles.phrase}>
          <Text fontSize="5xl">Sentime</Text>
          <Text className={styles.description} fontSize="2xl">Description</Text>
          <Button marginTop="10px" leftIcon="email" variantColor="teal" onClick={() => window.open('mailto:pastorizoj@uninorte.edu.co?subject=Solicitud%20demo%20Sentime', '_blank')} target="blank">Solicitar Demo</Button>
        </div>
        <Flex className={styles.lower} alignItems="center" justifyContent="space-between">
          <Flex paddingRight="92px">
            <ReactPlayer url="https://www.youtube.com/watch?v=xaazUgEKuVA" />
          </Flex>
          <Flex justifyContent="flex-start" width="100%" flex="5">
            <div className={styles.login}>
              <Text fontSize="3xl" marginBottom="24px">Login</Text>
              <FormControl className={styles['form-control']}>
                <FormLabel htmlFor="email">Correo electrónico</FormLabel>
                <Input
                  type="email"
                  name="email"
                  value={formData.email}
                  aria-describedby="email-helper-text"
                  onChange={handleInputChange}
                />
              </FormControl>
              <FormControl className={styles['form-control']}>
                <FormLabel htmlFor="password">Contraseña</FormLabel>
                <Input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                />
              </FormControl>
              <Button
                className={styles['submit-btn']}
                isLoading={isLoading}
                loadingText="Submitting"
                variantColor="teal"
                variant="outline"
                onClick={handleSubmit}
              >
                Ingresar
              </Button>
            </div>
          </Flex>
        </Flex>
      </div>
    </>
  );
}

Landing.propTypes = {
  setUserData: Proptypes.func.isRequired,
};

export default Landing;
