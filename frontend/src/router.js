import { createRouter, createWebHistory } from "vue-router";
import store from "./store";
import Home from "./views/Home.vue";

import SignUp from "./views/SignUp.vue";
import LogIn from "./views/LogIn.vue";
import MyAccount from "./views/MyAccount.vue";
import Offer from "./views/Offer.vue";

const routes = [{
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: "/inscription",
        name: "SignUp",
        component: SignUp
    },
    {
        path: "/connexion",
        name: "LogIn",
        component: LogIn
    },
    {
        path: "/mon-compte",
        name: "MyAccount",
        component: MyAccount,
        meta: {
            requireLogin: true
        }
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

router.beforeEach((to, from, next) => {
    if (
        to.matched.some(record => record.meta.requireLogin) &&
        !store.state.isAuthenticated
    ) {
        next({ name: "LogIn", query: { to: to.path } });
    } else {
        next();
    }
});

export default router;