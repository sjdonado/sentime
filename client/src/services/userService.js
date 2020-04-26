import { post } from '../lib/HttpClient';

const basePath = '/user';

export const login = (email, password) => post(`${basePath}/login`, { email, password })