import React from 'react';

import { ThemeProvider, theme, CSSReset } from '@chakra-ui/core';

import Routes from './Routes';

const customTheme = {
  ...theme,
  colors: {
    ...theme.colors,
    brand: {
      900: '#1a365d',
      800: '#153e75',
      700: '#2a69ac',
    },
  },
};

function App() {
  return (
    <ThemeProvider
      theme={customTheme}
    >
      <CSSReset />
      <Routes />
    </ThemeProvider>
  );
}

export default App;
