
import axios from 'axios'
import qs from 'qs'

const baseURL = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
    paramsSerializer: params => qs.stringify(params, { arrayFormat: 'repeat' }), // Форматирование массивов как repeated
})

api.interceptors.response.use(
    response => response,
    error => {
        return Promise.reject(error)
    }
)

export default api