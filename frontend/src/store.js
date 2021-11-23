import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
    state: {
        isAuthenticated: false,
        token: "",
        // TODO: Centraliser le userInfo afin de diminuer la rendondance
        userInfo: {}
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
            state.isAuthenticated = true;
        },
        removeToken(state) {
            state.token = "";
            state.isAuthenticated = false;
        }
    },
    actions: {},
    modules: {},
    plugins: [createPersistedState()]
});