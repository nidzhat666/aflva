import 'bootstrap/dist/css/bootstrap.css';
import {createApp} from 'vue'
import App from './App.vue';
import router from './router';
import store from './store';
import axios from "axios";
import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap/dist/js/bootstrap.bundle'

let isRefreshing = false;
let refreshSubscribers = [];

axios.defaults.baseURL = 'http://127.0.0.1:8000/api'
axios.interceptors.response.use(response => {
    return response
}, error => {
    const { config, response: { status, data } } = error;
    const originalRequest = config;
    if (status === 401 && config.url === 'auth/jwt/refresh/'){
        store.dispatch('handleError', data)
        store.dispatch('logOut')
        router.push({name: 'Login'})
    }
    if (status === 401 && store.state.jwt.refresh) {
        if (!isRefreshing) {
            console.log(store.getters.isLoggedIn)
            isRefreshing = true;
            store.dispatch('refreshToken').then((response)=>{
                isRefreshing = false;
                onRrefreshed(response.data.access);
                store.commit('updateStorage', {
                    access:response.data.access,
                    refresh:response.data.refresh
                })
            })
        }
        return new Promise((resolve) => {
            subscribeTokenRefresh(token => {
                originalRequest.headers['Authorization'] = 'Bearer ' + token;
                resolve(axios(originalRequest));
            });
        });
    } else {
        store.dispatch('handleError', data)
        return Promise.reject(error);
    }
    }
)


function subscribeTokenRefresh(cb){
    refreshSubscribers.push(cb);
}

function onRrefreshed(token) {
    refreshSubscribers.map(cb => cb(token));
}
createApp(App)
    .use(store)
    .use(router, axios)
    .mount('#app')



