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
              <input class="input" type="text" placeholder="Search">
              <span class="icon is-left">
                <i class="fas fa-search" aria-hidden="true"></i>
              </span>
            </p>
            <a class="is-2">Recherche Avancée</a>
          </div>
          <p class="ml-2 has-text-weight-bold has-text-black">
            Type de service
          </p>
          <label class="panel-block">
            <input type="checkbox">
            Option 1
          </label>
          <p class="ml-2 has-text-weight-bold has-text-black">
            Distance
          </p>
          <label class="panel-block">
            Max (km)
            <input id="maxDistanceSlider" class="slider has-output is-fullwidth" min="0" max="100" value="50" step="10"
              type="range">
            <output for="maxDistanceSlider" class="w-80">50</output>
          </label>


          <div class="panel-block">
            <button class="button is-link is-outlined is-fullwidth">
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
  import bulmaSlider from "bulma-slider";
  export default {
    name: "Home",
    data() {
      return {
        offers: [],
        isFetchingOffers: false,
        activePanelTab: 'distance',
        attachedSliders: [],
      };
    },
    components: {
      DetailedOffer,
    },
    mounted() {
      document.title = "Accueil | Communoservice";
      this.getAllOffers();
    },
    renderTriggered() {
      if (this.attachedSliders.length == 0) {
        this.attachedSliders = bulmaSlider.attach();
        console.log("Sliders attached: " + this.attachedSliders.length)
      }
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
    },
  };
</script>