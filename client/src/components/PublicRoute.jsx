import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';

function PublicRoute({ isAuth, children }) {
  if (isAuth) {
    return <Redirect to="/home" />;
  }
  return children;
}

PublicRoute.propTypes = {
  isAuth: PropTypes.bool.isRequired,
  children: PropTypes.node.isRequired,
};

export default PublicRoute;
