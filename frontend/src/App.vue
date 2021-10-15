<template>
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
            <div class="navbar-item">
              <div class="dropdown is-hoverable" :class="dropdownRight ? 'is-right' : 'is-left'">
                <div class="dropdown-trigger">
                  <button class="button is-rounded has-text-centered" aria-haspopup="true"
                    aria-controls="dropdown-menu3">
                    <span class="icon is-small">
                      <i class="fas fa-angle-down" aria-hidden="true"></i>
                    </span>
                  </button>
                </div>
                <div class="dropdown-menu pu-2" id="dropdown-menu3" role="menu">
                  <div class="dropdown-content has-text-left">
                    <a href="#" class="dropdown-item" v-on:click="modalSettingsisActive = !modalSettingsisActive">
                      <span class="icon is-small mr-3">
                        <i class="fas fa-cog"></i>
                      </span>
                      <span> Paramêtres </span>
                    </a>
                    <hr class="dropdown-divider" />
                    <a href="#" @click="logout()" class="dropdown-item has-text-danger">
                      <span class="icon is-small mr-3">
                        <i class="fas fa-sign-out-alt"></i>
                      </span>
                      <span> Déconnexion </span>
                    </a>
                  </div>
                </div>
              </div>
            </div>
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

    <div class="modal" v-bind:class="{ 'is-active': modalSettingsisActive}">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Paramêtres</p>
          <button class="delete" v-on:click="modalSettingsisActive = !modalSettingsisActive"
            aria-label="close"></button>
        </header>
        <section class="modal-card-body">
          Configuration des paramêtres ici
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success w-100">Sauvegarder</button>
          <button class="button is-danger w-100"
            v-on:click="modalSettingsisActive = !modalSettingsisActive">Canceler</button>
        </footer>
      </div>
    </div>

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
  import {
    toast
  } from "bulma-toast";
  export default {
    data() {
      return {
        showNav: false,
        window: {
          width: 0,
          height: 0
        },
        dropdownRight: true,
        modalSettingsisActive: false,
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
      console.log(token);
    },
    mounted() {
      window.addEventListener('resize', this.handleResize);
      this.handleResize();
    },
    computed: {},
    methods: {
      async logout() {
        await axios
				.post("/api/v1/token/logout/")
				.then((response) => {
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
            animate: {
              in: "fadeInRightBig",
              out: "fadeOutLeftBig",
            },
          });
				})
				.catch((error) => {
					toast({
            message: "Une erreur est survenue...",
            type: "is-danger",
            dismissible: false,
            pauseOnHover: false,
            duration: 3000,
            position: "center",
            animate: {
              in: "fadeInRightBig",
              out: "fadeOutLeftBig",
            },
          });
				});
      },
      handleResize() {
        this.window.width = window.innerWidth;
        this.window.height = window.innerHeight;
        if (window.innerWidth > 1006) {
          this.showNav = false;
          this.dropdownRight = true;
        } else {
          this.dropdownRight = false;
        }
      },
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
  .navbar {
    border-radius: 0 !important;
  }
  .w-80{
    width: 80px!important;
  }
  .panel-section{
    border-bottom: 1px solid #ededed;
    padding: 10px 0 10px 0;
  }
  .datepicker{
    background-color: white;
    border-color: #dee2e5;
    border-radius: 0.4em;
    color: #2b3c4e;
    border-width: 2px;
    border-style: solid;
    font-size: 1em;
    padding-bottom: calc(0.5em - 1px);
    padding-left: calc(0.75em - 1px);
    padding-right: calc(0.75em - 1px);
    padding-top: calc(0.5em - 1px);
  }
</style>