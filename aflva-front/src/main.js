import 'bootstrap/dist/css/bootstrap.css';
import {createApp} from 'vue'
import App from './App.vue';
import router from './router';
import store from './store';
import axios from "axios";
import 'bootstrap'
import 'bootstrap/dist/js/bootstrap.bundle'
import {Tooltip} from "bootstrap";

let isRefreshing = false;
let refreshSubscribers = [];

axios.defaults.baseURL = 'https://afl-va.ru/api'
axios.interceptors.response.use(response => {
        return response
    }, error => {
        const {config, response: {status}} = error;
        const originalRequest = config;
        if (status === 401 && config.url === 'auth/jwt/refresh/') {
            store.dispatch('handleError', error)
            store.dispatch('logOut')
            router.push({name: 'Login'})
        }
        if (status === 401 && store.state.jwt.refresh) {
            if (!isRefreshing) {
                isRefreshing = true;
                store.dispatch('refreshToken').then((response) => {
                    isRefreshing = false;
                    onRrefreshed(response.data.access);
                    store.commit('updateStorage', {
                        access: response.data.access,
                        refresh: response.data.refresh
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
            store.dispatch('handleError', error)
            return Promise.reject(error);
        }
    }
)


function subscribeTokenRefresh(cb) {
    refreshSubscribers.push(cb);
}

function onRrefreshed(token) {
    refreshSubscribers.map(cb => cb(token));
}

createApp(App)
    .directive("tooltip", (el, binding, vnode, old)=>{
        new Tooltip(el, {title: binding.value, placement: binding.arg, trigger: 'hover'})
    })
    .use(store)
    .use(router, axios)
    .mount('#app')


// app.directive('tooltip',
// })


