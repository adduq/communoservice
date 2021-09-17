<template>
  <!-- Vieux menu à enlever -->
  <!--<div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <strong>Communoservice</strong>
        </router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <template v-if="$store.state.isAuthenticated">
              <div class="dropdown is-hoverable">
                <div class="dropdown-trigger">
                  <button
                    class="button"
                    aria-haspopup="true"
                    aria-controls="dropdown-menu3"
                  >
                    <span class="icon is-small mr-3">
                      <i class="fas fa-angle-down" aria-hidden="true"></i>
                    </span>
                    <span> Menu </span>
                  </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                  <div class="dropdown-content">
                    <router-link to="/mon-compte" class="dropdown-item">
                      <span class="icon is-small mr-3">
                        <i class="fas fa-user-circle"></i>
                      </span>
                      <span> Mon compte </span>
                    </router-link>
                    <a
                      href="https://github.com/VP-0/communoservice"
                      class="dropdown-item"
                    >
                      <span class="icon is-small mr-3">
                        <i class="fab fa-github-square"></i>
                      </span>
                      <span> GitHub </span>
                    </a>
                    <a href="#" class="dropdown-item">
                      <span class="icon is-small mr-3">
                        <i class="fas fa-cog"></i>
                      </span>
                      <span> Paramêtres </span>
                    </a>
                    <hr class="dropdown-divider" />
                    <a
                      href="#"
                      @click="logout()"
                      class="dropdown-item has-text-danger"
                    >
                      <span class="icon is-small mr-3">
                        <i class="fas fa-sign-out-alt"></i>
                      </span>
                      <span> Déconnexion </span>
                    </a>
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <router-link to="/connexion" class="button is-light">
                Connexion
              </router-link>
            </template>
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
        <p>
          Copyright
          <i class="fas fa-copyright" aria-hidden="true"></i>
          Communoservice 2021
        </p>
      </div>
    </footer>
  </div>-->
  <div id="wrapper">
    <nav class="navbar">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          <h4 class="title is-4 has-text-weight-bold has-text-white">Communoservice</h4>
        </a>
        <div class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
      <div class="navbar-menu" :class="{ 'is-active': showNav }">
        <div class="navbar-start">
          <a class="navbar-item" href="/" @click="showNav = !showNav">
            Accueil
          </a>
          <a class="navbar-item" href="https://github.com/VP-0/communoservice" @click="showNav = !showNav">
            <span class="mr-2">GitHub</span>
            <span class="icon is-small">
              <i class="fab fa-github"></i>
            </span>
          </a>
        </div>
        <div class="navbar-end">
          <template v-if="$store.state.isAuthenticated">
            <router-link to="/mon-compte" class="navbar-item" @click="showNav = !showNav">
              <span class="mr-3">Mon compte</span>
              <span class="icon is-small mr-3">
                <i class="fas fa-user-circle"></i>
              </span>
            </router-link>
          </template>

          <template v-else>
            <router-link to="/connexion" class="navbar-item">
              <span class="mr-3">Connexion</span>
              <span class="icon is-small mr-3">
                <i class="fas fa-sign-in-alt"></i>
              </span>
            </router-link>
          </template>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view />
    </section>

    <footer class="footer">
      <div class="content has-text-centered">
        <p>
          Copyright
          <i class="fas fa-copyright" aria-hidden="true"></i>
          Communoservice 2021
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
  import axios from "axios";
  import {toast} from "bulma-toast";
  export default {
    data() {
      return {
        showNav: false,
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
    mounted() {},
    computed: {},
    methods: {
    },
  };
</script>

<style lang="scss">
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