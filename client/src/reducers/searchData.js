const initState = {
  status: '',
  results: [],
};

const searchDataReducer = (state = initState, action) => {
  switch (action.type) {
    case 'ADD':
      if (state.results.findIndex(({ city }) => city === action.data.city) !== -1) {
        return state;
      }
      return {
        status: action.data.status,
        results: [...state.results, action.data.results],
      };
    case 'REMOVE_ALL':
      return initState;
    default:
      return state;
  }
};

export default searchDataReducer;
