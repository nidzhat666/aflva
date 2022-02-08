import {createStore} from 'vuex'
import {userService} from '../services/user.service'
import {bookService} from '../services/book.service'


export default createStore({
    state: {
        user: null,
        auth_error: null,
        books: null
    },
    mutations: {
        loginRequest(state, user) {
            state.user = user
        },
        setUserErrorStatus(state, error) {
            state.auth_error = error
        },
        setBooks(state, books) {
            state.books = books
        }
    },
    getters: {
        getToken(state) {
            return state.user.token
        }
    },
    actions: {
        login({commit}, data) {
            return userService.userLogin(data).then(
                user => {
                    commit('setUserErrorStatus', null)
                    commit('loginRequest', user)
                    localStorage.email = data.email_or_username
                    localStorage.password = data.password
                    return
                },
                error => {
                    commit('setUserErrorStatus', error)
                    return
                })
        },
        books({commit, getters}) {
            return bookService.getAllBooks(getters.getToken).then(
                books => {
                    commit('setBooks', books)
                    return books
                }
            )
        }
    },
})
