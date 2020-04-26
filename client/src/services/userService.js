import axios from 'axios';
import { API_URL } from '../environment';

const basePath = 'users';

export const login = (email, password) => axios({
  method: 'post',
  url: `${API_URL}/${basePath}/login`,
  data: { email, password },
  withCredentials: true,
});

export const logout = () => axios({
  method: 'post',
  url: `${API_URL}/${basePath}/logout`,
});
