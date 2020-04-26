/**
 * Get HTTP request
 * @param {String} path 
 * @param {String} params 
 * @param {String} query 
 */
export function get(path, params = '', query = '') {
  return fetch(`${path}/${params}${query}`, {
  })
  .then((response) => response.json())
}

/**
 * Get HTTP request
 * @param {String} path 
 * @param {Object} data 
 * @param {String} params 
 */
export function post(path, data, params = '') {
  return fetch(`${path}/${params}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then((response) => response.json())
}