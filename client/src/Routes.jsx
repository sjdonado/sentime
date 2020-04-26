import React from 'react';
import { useCookies } from 'react-cookie';

import './App.scss';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from 'react-router-dom';

import { Flex } from '@chakra-ui/core';

import PublicRoute from './components/PublicRoute';
import PrivateRoute from './components/PrivateRoute';
import Appbar from './components/Appbar';

import Login from './pages/Login/Login';
import Home from './pages/Home/Home';

const USER_COOKIE_NAME = 'session-user';

function Routes() {
  const [cookies, setCookie, removeCookie] = useCookies([USER_COOKIE_NAME]);

  const setUserEmail = (data) => {
    setCookie(USER_COOKIE_NAME, data, { path: '/', expires: new Date(Date.now() + 8.64e+7) });
  };

  const logout = () => {
    removeCookie(USER_COOKIE_NAME, { path: '/' });
  };

  const routes = [
    {
      isPublic: true,
      path: '/login',
      children: <Login setUserEmail={setUserEmail} />,
    },
    {
      isPublic: false,
      path: '/home',
      children: (
        <Flex width="100vw" height="100vh" flexDirection="column" padding="2">
          <Appbar userEmail={cookies[USER_COOKIE_NAME]} logout={logout} />
          <Home />
        </Flex>
      ),
    },
  ];

  return (
    <Router>
      <Switch>
        {routes.map(({ isPublic, path, children }) => (
          <Route key={path} path={path}>
            {isPublic ? (
              <PublicRoute isAuth={Boolean(cookies[USER_COOKIE_NAME])}>
                {children}
              </PublicRoute>
            ) : (
              <PrivateRoute isAuth={Boolean(cookies[USER_COOKIE_NAME])}>
                {children}
              </PrivateRoute>
            )}
          </Route>
        ))}
        <Redirect to="/login" />
      </Switch>
    </Router>
  );
}

export default Routes;
