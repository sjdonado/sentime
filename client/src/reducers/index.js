import { combineReducers } from 'redux';

import searchDataReducer from './searchData';

const allReducers = combineReducers({
  searchData: searchDataReducer,
});

export default allReducers;
