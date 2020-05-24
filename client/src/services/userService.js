import axios from 'axios';
import { API_URL } from '../environment';

const basePath = 'users';

export const login = (email, password) => axios({
  method: 'post',
  url: `${API_URL}/${basePath}/login`,
  data: { email, password },
  withCredentials: true,
});

export const userLogout = () => axios({
  method: 'post',
  url: `${API_URL}/${basePath}/logout`,
  withCredentials: true,
});

export const getHistory = () => axios({
  method: 'post',
  url: `${API_URL}/${basePath}/history`,
  withCredentials: true,
});
