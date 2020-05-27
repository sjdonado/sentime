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
import Search from './pages/Search/Search';
import Landing from './pages/Landing/Landing';
import Register from './pages/Register/Register';
import History from './pages/History/History';
import AllHistory from './pages/AllHistory/AllHistory';

const USER_DATA_COOKIE = 'session-user';

function Routes() {
  const [cookies, setCookie, removeCookie] = useCookies([USER_DATA_COOKIE]);

  const setUserData = (id, email) => {
    setCookie(USER_DATA_COOKIE, `${id},${email}`, { path: '/', expires: new Date(Date.now() + 8.64e+7) });
  };

  const getUserData = () => {
    const [id, email] = cookies[USER_DATA_COOKIE] ? cookies[USER_DATA_COOKIE].split(',') : '';
    return {
      id: Number(id),
      email,
    };
  };

  const logout = () => {
    removeCookie(USER_DATA_COOKIE, { path: '/' });
  };

  const routes = [
    {
      isPublic: true,
      exact: true,
      path: '/',
      children: <Landing setUserData={setUserData} />,
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
      isPublic: false,
      path: '/allhistory',
      children: <AllHistory />,
    },
    {
      isPublic: false,
      path: '/search',
      children: <Search userData={getUserData()} />,
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
              <PublicRoute isAuth={Boolean(cookies[USER_DATA_COOKIE])}>
                {children}
              </PublicRoute>
            ) : (
              <PrivateRoute isAuth={Boolean(cookies[USER_DATA_COOKIE])}>
                <Flex width="100vw" height="100vh" flexDirection="column" padding="2">
                  <Appbar userData={getUserData()} logout={logout} />
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
