import { createStore } from 'vuex'
import router from "@/router";
import axios from "axios";
import {Toast} from 'bootstrap/dist/js/bootstrap.esm'

export default createStore({
  state: {
    jwt: {

    },
    error_message: ''
  },
  mutations: {
    updateStorage(state, {access, refresh}){
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + access;
      localStorage.setItem('jwt_access', access)
      state.jwt.access = access
      if (refresh){
        localStorage.setItem('jwt_refresh', refresh)
        state.jwt.refresh = refresh
      }
    },
    deleteStorage(state){
      localStorage.clear()
      state.jwt = {
      }
    },
    setError(state, message){
      state.error_message = message
    },
    setUser(state, user){
      state.user = user
    }
  },
  getters:{
    isLoggedIn(state){
      return state.jwt.access
    },
    user(state){
      return state.user
    }
  },
  actions: {
    logIn(context, data){
      axios.post('auth/jwt/create/', data)
          .then((response)=>{
            context.commit('updateStorage', response.data)
            router.push({ name: 'Home' })
            context.dispatch('hideError')
          })
    },
    initStorage(context){
      let jwt_access = localStorage.getItem('jwt_access')
      let jwt_refresh = localStorage.getItem('jwt_refresh')
      if (jwt_refresh) context.commit('updateStorage', {access: jwt_access, refresh: jwt_refresh})
    },
    refreshToken(context){
      return axios.post('auth/jwt/refresh/', {refresh: context.state.jwt.refresh})
          // .then(response =>{
          //   context.commit('updateStorage', {access: response.data.access})
          // })
    },
    logOut(context){
      context.commit('deleteStorage')
    },
    handleError(context, error){
      context.commit('setError', error.response.data?.detail || error.message)
      const toastLiveExample = document.getElementById('liveToast')
      const toast = new Toast(toastLiveExample)
      toast.show()
    },
    hideError(){
      const toastLiveExample = document.getElementById('liveToast')
      const toast = new Toast(toastLiveExample)
      toast.hide()
    },
    userObtain(context){
      axios.get('auth/users/me/')
          .then(response =>{
            context.commit('setUser', response.data)
          })
    }
  },
  modules: {
  }
})
