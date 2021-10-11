<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">Bienvenue sur Communoservice</p>
        <p class="subtitle">
          Le meilleur site pour les services communautaires
        </p>
      </div>
    </section>

    <div class="columns is-multiline is-12">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">
          Liste des services
        </h2>
      </div>
    </div>
    <div class="columns mt-6">
      <div class="column">
        <nav class="panel">
          <p class="panel-heading">
            Recherche
          </p>
          <div class="panel-block is-flex-wrap-wrap">
            <p class="control has-icons-left is-full-width">
              <input class="input" type="text" placeholder="Mots Clé(s)">
              <span class="icon is-left">
                <i class="fas fa-search" aria-hidden="true"></i>
              </span>
            </p>
          </div>
          <div class="panel-section">
            <p class="ml-2 has-text-weight-bold has-text-black">
            Type de service
            </p>

            <div class="select ml-2 mt-1">
              <select v-model='query'>
                <option>Tonte de pelouse</option>
                <option>Gardiennage</option>
                <option>Déneigement</option>
              </select>
            </div>
          </div>
          <div class="panel-section">
            <p class="ml-2 has-text-weight-bold has-text-black">
              Date
            </p>
            <input class="datepicker ml-2 mt-1" type="date" :min="dateToday" v-model="serviceDateQuery">
          </div>
          
          <div class="panel-block">
            <button v-on:click="sendQuery" class="button is-link is-outlined is-fullwidth">
              Rechercher
            </button>
          </div>
        </nav>
      </div>
      <div class="column is-two-thirds">
        <div class="box">
          <progress class="progress is-small is-primary" v-if="isFetchingOffers"></progress>
          <DetailedOffer v-for="offer in offers" v-bind:key="offer.id" v-bind:offer="offer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import DetailedOffer from "@/components/DetailedOffer";
  export default {
    name: "Home",
    data() {
      return {
        offers: [],
        isFetchingOffers: false,
        activePanelTab: 'distance',
        attachedSliders: [],
        // La valeur de "query" est hard codé pour le moment. Il va falloir faire categories[0] 
        // lorsque nous allons avoir la liste des catégories pour peupler le dropdown.
        query: "Tonte de pelouse",
        dateToday: '',
        serviceDateQuery: '',
        weekdays: {
          0:"monday",
          1:"tuesday",
          2:"wednesday",
          3:"thursday",
          4:"friday",
          5:"saturday",
          6:"sunday",
        }
      };
    },
    components: {
      DetailedOffer,
    },
    mounted() {
      document.title = "Accueil | Communoservice";
      this.getAllOffers();
      this.updateCalendarToday();
    },
    renderTriggered() {
      // DEBUG pour le datepicker
      var chosenDate = new Date(this.serviceDateQuery);
      console.log(`${this.serviceDateQuery} is a ${this.weekdays[chosenDate.getDay()]}`);
    },
    methods: {
      async getAllOffers() {
        this.isFetchingOffers = true;
        await axios
          .get("/api/v1/offers/")
          .then((response) => {
            this.offers = response.data;
          })
          .catch((error) => {
            console.log(error);
          });
        this.isFetchingOffers = false;
      },
      async sendQuery() {
        this.isFetchingOffers = true;
        await axios
          .get("/api/v1/offers/search?type-service=" + this.query)
          .then((response) => {
            this.offers = response.data;
          })
          .catch((error) => {
            console.log(error);
          });
        this.isFetchingOffers = false;
      },
      updateCalendarToday(){
        var current = new Date();
        this.serviceDateQuery = this.dateToday = `${current.getFullYear()}-${current.getMonth()+1}-${current.getDate()}`;
      }
    },
  };
</script>