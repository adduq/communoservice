import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
    state: {
        isAuthenticated: false,
        token: "",
        // TODO: Centraliser le userInfo afin de diminuer la rendondance
        userInfo: {
            first_name: '---',
            last_name: '---',
            user_bio:'---',
            location_lat:'',
            location_lon:'',
            profile_is_completed:false,
        }
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
            state.isAuthenticated = true;
        },
        removeToken(state) {
            state.token = "";
            state.isAuthenticated = false;
        },
        changeUserInfo (state, updatedUserInfo) {
            state.userInfo.first_name = updatedUserInfo.first_name
            state.userInfo.last_name = updatedUserInfo.last_name
            state.userInfo.user_bio = updatedUserInfo.user_bio
            state.userInfo.location_lat = updatedUserInfo.location_lat
            state.userInfo.location_lon = updatedUserInfo.location_lon
            state.userInfo.profile_is_completed = updatedUserInfo.profile_is_completed
          }
    },
    actions:{
      /**
       * Méthode à utiliser dans les composants enfants pour
       * changer le userInfo.
       * @param {*} context  Le contexte
       * @param {*} newUserInfo Le nouveau userInfo
       */
        changeUserInfo (context, newUserInfo) {
          context.commit("changeUserInfo", newUserInfo);
        }
     },
     getters: {
        getUserInfo: state => {
          return state.userInfo
        }
      },
    modules: {},
    plugins: [createPersistedState()]
});