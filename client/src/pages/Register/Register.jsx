import React, { useState } from 'react';
// import Proptypes from 'prop-types';

import {
  Text,
  Input,
  FormControl,
  FormLabel,
  Button,
  useToast,
} from '@chakra-ui/core';

import styles from './Register.module.scss';

import { register } from '../../services/adminService';

function Register() {
  const toast = useToast();

  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    company: '',
  });

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const { email, password, company } = formData;
      await register(email, password, company);
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
      <Text fontSize="5xl">Registro</Text>
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
      <FormControl className={styles['form-control']}>
        <FormLabel htmlFor="company">Compañía</FormLabel>
        <Input
          type="text"
          name="company"
          value={formData.company}
          aria-describedby="company-helper-text"
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
        Registrar
      </Button>
    </div>
  );
}

export default Register;
