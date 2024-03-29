import axios from 'axios';
import { API_URL } from '../environment';

const basePath = 'users';

// eslint-disable-next-line import/prefer-default-export
export const register = (email, password, company) => axios({
  method: 'post',
  url: `${API_URL}/${basePath}/signup/4f3a0ca08e906`,
  data: { email, password, company },
  withCredentials: true,
});

