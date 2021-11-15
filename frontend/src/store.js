import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
    state: {
        isAuthenticated: false,
        token: "",
        isLoading: false,
        isLocationSet: false,
        // TODO: Centraliser le userInfo afin de diminuer la rendondance
        userInfo: {}
    },
    mutations: {
        initializeStore(state) {

        },
        setIsLoading(state, status) {
            state.isLoading = status;
        },
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