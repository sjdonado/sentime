import React from 'react';
import { Link } from 'react-router-dom';
import {
  Text,
  Input,
  FormControl,
  FormLabel,
  Button,
} from '@chakra-ui/core';
import styles from './Landing.module.scss';
import { ReactComponent as Analytics } from '../../assets/web-analytics.svg';

function Landing() {
  return (
    <div className={styles.container}>
      <div className={styles.phrase}>
        <Text fontSize="5xl">Sentime</Text>
      </div>
      <div className={styles.lower}>
        <div className={styles.child}>
          <Analytics className={styles.image} />
        </div>
        <div className={styles.child}>
          <Text fontSize="2xl">Solicita tu demo</Text>
          <FormControl isRequired className={styles['form-control']}>
            <FormLabel htmlFor="name">Nombre</FormLabel>
            <Input id="name" aria-describedby="name-helper-text" />
          </FormControl>
          <FormControl isRequired className={styles['form-control']}>
            <FormLabel htmlFor="company">Compañía</FormLabel>
            <Input id="company" aria-describedby="company-helper-text" />
          </FormControl>
          <FormControl isRequired className={styles['form-control']}>
            <FormLabel htmlFor="email">Correo</FormLabel>
            <Input type="email" id="email" aria-describedby="email-helper-text" />
          </FormControl>
          <Button
            className={styles.button}
            variantColor="teal"
          >
            Solicitar demo
          </Button>
          <Button
            className={styles.button}
            variantColor="teal"
            variant="outline"
            as={Link}
            to="/login"
          >
            Iniciar sesión
          </Button>
        </div>
      </div>
    </div>
  );
}


export default Landing;
