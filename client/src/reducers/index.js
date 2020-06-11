import { combineReducers } from 'redux';
import addCityReducer from './addCity';

const allReducers = combineReducers({
  cities: addCityReducer,
});

export default allReducers;
