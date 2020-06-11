const addCityReducer = (state = [], action) => {
  switch (action.type) {
    case 'ADD':
      state.forEach((entry) => {
        if (entry.city === action.data.city) {
          return state;
        }
      });
      return [...state, action.data];
    default:
      return state;
  }
};

export default addCityReducer;
