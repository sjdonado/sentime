import {
  useState,
  useEffect,
  Children,
  isValidElement,
  cloneElement,
} from 'react';

import PropTypes from 'prop-types';

import socketIOClient from 'socket.io-client';
import { useSelector, useDispatch } from 'react-redux';

import { SOCKET_IO_URL } from '../environment';

const socket = socketIOClient(SOCKET_IO_URL);

const DEFAULT_MESSAGE = 'Haz click en Buscar para empezar tu búsqueda';

function SocketIOProvider({ userData, children }) {
  const dispatch = useDispatch();
  const searchData = useSelector((state) => state.searchData);
  const [message, setMessage] = useState(DEFAULT_MESSAGE);

  const handleOnTweets = ({ id, status, data }) => {
    if (id === userData.id) {
      if (status === 'started') {
        setMessage('Búsqueda aceptada, obteniendo resultados...');
        dispatch({ type: 'REMOVE_ALL' });
      }
      if (status === 'task_in_process') {
        setMessage('Tienes una búsqueda en proceso, intena de nuevo una vez esta haya finalizado.');
      }
      if (status === 'processing') {
        const {
          city,
          lat,
          lng,
          total,
          scores,
        } = data;
        const newSearchData = {
          status,
          results: {
            city,
            lat,
            lng,
            total,
            scores,
          },
        };
        // console.log(cities);
        // console.log(newSearchData.results);
        if (searchData.results.length === 31) {
          Object.assign(newSearchData, { status: 'finished' });
          dispatch({ type: 'INCREMENT_TIME', startedAt: null });
        }
        dispatch({ type: 'ADD', data: newSearchData });
      }
    }
  };

  useEffect(() => {
    socket.on('tweets', handleOnTweets);
    const timer = searchData.startedAt !== null && setInterval(() => {
      dispatch({ type: 'INCREMENT_TIME', startedAt: (searchData.startedAt || 0) + 1 });
    }, 1000);
    return () => {
      socket.off('tweets');
      clearInterval(timer);
    };
  }, [searchData, dispatch]);

  const handleSearch = (e, query, hours) => {
    e.preventDefault();
    socket.emit('search', JSON.stringify({ query, hours }));
    setMessage('Búsqueda enviada, esperando respuesta del servidor...');
  };

  const childrenWithProps = Children.map(children, (child) => {
    if (isValidElement(child)) {
      return cloneElement(child, {
        searchData,
        startedAt: searchData.startedAt,
        message,
        handleSearch,
      });
    }
    return child;
  });

  return childrenWithProps;
}

SocketIOProvider.propTypes = {
  userData: PropTypes.shape({
    id: PropTypes.number.isRequired,
    email: PropTypes.string.isRequired,
  }).isRequired,
  children: PropTypes.node.isRequired,
};

export default SocketIOProvider;
