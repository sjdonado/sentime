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
import Landing from './pages/Landing/Landing';
import Register from './pages/Register/Register';
import History from './pages/History/History';

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
      exact: true,
      path: '/',
      children: <Landing />,
    },
    {
      isPublic: true,
      path: '/register',
      children: <Register />,
    },
    {
      isPublic: false,
      path: '/history',
      children: <History />,
    },
    {
      isPublic: true,
      path: '/login',
      children: <Login setUserEmail={setUserEmail} />,
    },
    {
      isPublic: false,
      path: '/home',
      children: <Home />,
    },
  ];

  return (
    <Router>
      <Switch>
        {routes.map(({
          isPublic, path, children, exact,
        }) => (
          <Route key={path} path={path} exact={exact}>
            {isPublic ? (
              <PublicRoute isAuth={Boolean(cookies[USER_COOKIE_NAME])}>
                {children}
              </PublicRoute>
            ) : (
              <PrivateRoute isAuth={Boolean(cookies[USER_COOKIE_NAME])}>
                <Flex width="100vw" height="100vh" flexDirection="column" padding="2">
                  <Appbar userEmail={cookies[USER_COOKIE_NAME]} logout={logout} />
                  {children}
                </Flex>
              </PrivateRoute>
            )}
          </Route>
        ))}
        <Redirect to="/" />
      </Switch>
    </Router>
  );
}

export default Routes;
