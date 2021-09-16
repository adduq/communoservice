<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <strong>Communoservice</strong>
        </router-link>

        <a
          href="#"
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbar-menu"
          @click="afficherMenuMobile = !afficherMenuMobile"
        >
          <span aria-label="true"></span>
          <span aria-label="true"></span>
          <span aria-label="true"></span>
        </a>
      </div>

      <div
        class="navbar-menu"
        id="navbar-menu"
        v-bind:class="{ 'is-active': afficherMenuMobile }"
      >
        <div class="navbar-start">
          <div class="navbar-item">
            <form action="/search" method="get">
              <div class="field has-addons">
                <div class="control">
                  <input
                    type="text"
                    name="query"
                    class="input"
                    placeholder="Que recherchez-vous ?"
                  />
                </div>

                <div class="control">
                  <button class="button is-success">
                    <span class="icon"><i class="fas fa-search"></i></span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/mon-compte" class="button is-light">
                  Mon compte
                </router-link>
                <button @click="logout()" class="button is-danger"><i class="fas fa-sign-out-alt"></i></button>
              </template>

              <template v-else>
                <router-link to="/connexion" class="button is-light">
                  Connexion
                </router-link>
              </template>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div
      class="is-loading-bar has-text-centered"
      v-bind:class="{ 'is-loading': $store.state.isLoading }"
    >
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view />
    </section>

    <footer class="footer">
      <div class="content has-text-centered">
        <p>Copyright 
          <i class="fas fa-copyright" aria-hidden="true"></i>
          Communoservice 2021
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from 'bulma-toast';
export default {
  data() {
    return {
      afficherMenuMobile: false
    };
  },
  beforeCreate() {
    this.$store.commit("initializeStore");

    const token = this.$store.state.token;

    if (token) {
      axios.defaults.headers.common["Authorization"] = "Token " + token;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  },
  mounted() {
  },
  computed: {

  },
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("userid");
      this.$store.commit("removeToken");
      this.$router.push("/");
      toast({
          message: "Déconnecté avec succès!",
          type: "is-success",
          dismissible: false,
          pauseOnHover: false,
          duration: 3000,
          position: "center",
          animate: {in: 'fadeInRightBig', out: 'fadeOutLeftBig'}
			});
    },
  }
};
</script>

<style lang="scss">
// @import "../node_modules/bulma";
@import "../node_modules/bulmaswatch/flatly/bulmaswatch.scss";

.test-classe {
	@extend .title;
	@extend .is-4;
	@extend .has-text-centered;
}

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  &.is-loading {
    height: 80px;
  }
}
</style>
