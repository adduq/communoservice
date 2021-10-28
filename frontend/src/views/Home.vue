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
              <input class="input" type="text" placeholder="Mots Clé(s)" v-model="query_mots_cles">
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
              <select v-model='query_typeservice'>
                <option>Tout</option>
                <option>Tonte de pelouse</option>
                <option>Gardiennage</option>
                <option>Déneigement</option>
                <option>Administration</option>
              </select>
            </div>
          </div>
          <div class="panel-section">
            <p class="ml-2 has-text-weight-bold has-text-black">
              Date
            </p>
            <input class="datepicker ml-2 mt-1" type="date" :min="dateToday" v-model="select_serviceday">
          </div>
          
          <div class="panel-block">
            <button v-on:click="sendQuery" class="button is-link is-outlined is-fullwidth" :class="isFetchingOffers ? 'is-loading':''">
              Rechercher
            </button>
          </div>
        </nav>
      </div>
      <div class="column is-two-thirds">
        <div class="box">
          <!-- <progress class="progress is-small is-primary" v-if="isFetchingOffers"></progress> -->
          <DetailedOffer v-for="offer in offers" v-bind:key="offer.id" v-bind:offer="offer" @click="showOfferModal(offer)"/>
        </div>
      </div>
    </div>
  </div>
  <div class="modal" :class="offerModalActive ? 'is-active' : ''">
    <div class="modal-background" @click="closeOfferModal()"></div>
    <div class="modal-card">
      <header class="modal-card-head">        
        <p class="modal-card-title" v-if="currentStep == 1">Détails de l'offre</p>
        <p class="modal-card-title" v-if="currentStep == 2">Choix des disponibilités</p>
        <p class="modal-card-title" v-if="currentStep == 3">Confirmation</p>
        <button class="delete has-background-danger" aria-label="close" @click="closeOfferModal()"></button>
      </header>
      <section class="modal-card-body">
        <ul class="steps is-small" ref="stepsSection">
          <li class="step-item is-info is-completed" :class="currentStep >= 1 ? 'is-active ' : ''">
            <div class="step-marker">
              <span class="icon">
                <i class="fa fa-align-justify"></i>
              </span>
            </div>
          </li>
          <li class="step-item is-info" :class="[currentStep >= 2 ? 'is-active' : '', step2Completed ? 'is-completed': '']">
            <div class="step-marker">
              <span class="icon">
                <i class="fa fa-calendar-check"></i>
              </span>
            </div>
          </li>
          <li class="step-item is-info" :class="[currentStep >= 3 ? 'is-active' : '', step3Completed ? 'is-completed': '']">
            <div class="step-marker">
              <span class="icon">
                <i class="fa fa-check"></i>
              </span>
            </div>
          </li>
        </ul>
        <div v-if="currentStep == 1">
          <p class="title has-text-centered">Détails de l'offre</p>
          <div class="columns is-mobile is-flex-wrap-wrap">
            <div class="column has-text-centered">
              <label class="label is-size-5">Service</label>
              <span class="tag has-text-weight-bold is-size-6">{{offerToShow.type_service}}</span>
            </div>
            <div class="column has-text-centered">
              <label class="label is-size-5">Taux horaire</label>
              <span class="tag has-text-weight-bold is-size-6">${{offerToShow.hourly_rate}}/h</span>
            </div>
            <div class="column has-text-centered">
              <label class="label is-size-5">Distance</label>
              <span class="tag has-text-weight-bold is-size-6">{{offerToShow.max_distance}}km</span>
            </div>
          </div>
          <label class="label has-text-centered bt-1 pt-2 is-size-5">Disponibilités</label>
          <div class="is-flex has-text-centered is-flex-wrap-wrap mt-2 is-justify-content-space-evenly is-family-monospace">
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.monday == true? 'is-info' : 'is-dark'" title="Lundi">
                L
              </span> 
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.tuesday == true? 'is-info' : 'is-dark'" title="Mardi">
                M
              </span>
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.thursday == true? 'is-info' : 'is-dark'" title="Mercredi">
                M
              </span>     
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.wednesday == true? 'is-info' : 'is-dark'" title="Jeudi">
                J
              </span>
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.friday == true? 'is-info' : 'is-dark'" title="Vendredi">
                V
              </span>
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.saturday == true? 'is-info' : 'is-dark'" title="Samedi">
                S
              </span>
              <span class="tag is-rounded ch-5 is-size-6" :class="offerToShow.sunday == true? 'is-info' : 'is-dark'" title="Dimanche">
                D
              </span>
          </div>
          <div class="is-flex is-justify-content-space-evenly mt-3 is-flex-wrap-wrap">
            <div class="is-flex is-align-items-center m-2">
              Disponible: 
              <span class="tag is-rounded ch-5 is-size-6 ml-2 is-info">
              </span>            
            </div>
            <div class="is-flex is-align-items-center m-2">
              Non disponible:
              <span class="tag is-rounded ch-5 is-size-6 ml-2 is-dark">
              </span>            
            </div>
          </div>
          <div class="has-text-centered mt-5 mb-5 bt-1 pt-2">
            <label class="label is-size-5">Description</label>
            <p class="is-size-6">{{offerToShow.description}}</p>
          </div>
          <div class="columns bt-1 pt-2 is-gapless">
            <div class="column">
              <div class="has-text-centered">
                <label class="label is-size-5">Date de création</label>
                <p class="is-size-6">{{offerToShow.date_added}}</p>
              </div>
            </div>
            <div class="column">
              <div class="has-text-centered">
                <label class="label is-size-5">Date d'éxpiration</label>
                <p class="is-size-6">{{offerToShow.expiration_date}}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="currentStep == 2">
          <div class="container profile">
            <div class="section profile-heading pt-0 pb-0">
              <div class="columns">
                <div class="column has-text-centered">
                  <figure class="image is-128x128 round-shadow has-image-centered">
                    <img class="is-rounded" src="https://owcdn.net/img/5bda50b474984.jpg" />
                    <i class="fas fa-circle" 
                      :class="offerUserInfo ? 'active-icon' : 'not-active-icon'"
                      :title="offerUserInfo ? 'Actif' : 'Inactif'"></i>
                  </figure>
                  <p>
                    <span class="title is-4 is-bold">
                      {{offerUserInfo.first_name + " " + offerUserInfo.last_name}}
                    </span>
                  </p>
                </div>
              </div>
              <div class="columns is-mobile is-flex-wrap-wrap">
                <div class="column has-text-centered">
                  <p class="has-text-weight-bold is-size-3">{{ offerUserInfo.nb_services_given }}</p>
                  <p>services rendus</p>
                </div>
                <div class="column has-text-centered">
                  <p class="has-text-weight-bold is-size-3">---</p>
                  <p>services actifs</p>
                </div>
                <div class="column has-text-centered">
                  <p class="has-text-weight-bold is-size-3">
                    {{ offerUserInfo.avg_rating_as_employee }}/10
                  </p>
                  <p>score</p>
                </div>
              </div>
            </div>
          </div>
            <label class="label has-text-centered mt-6 pt-2 is-size-5">Veuillez choisir une de mes disponibilités.</label>
            <div class="is-flex has-text-centered is-flex-wrap-wrap mt-2 mb-6 is-justify-content-space-evenly is-family-monospace">
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.monday ? 'is-info': '', !offerToShow.monday ? 'is-dark' : '']" 
                :disabled="!offerToShow.monday" title="Lundi"
                @click="selectedWeekdays.monday = !selectedWeekdays.monday">
                L
              </button> 
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.tuesday ? 'is-info' : '', !offerToShow.tuesday ? 'is-dark' : '']" 
                :disabled="!offerToShow.tuesday" title="Mardi"
                @click="selectedWeekdays.tuesday = !selectedWeekdays.tuesday">
                M
              </button>
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.thursday ? 'is-info' : '', !offerToShow.thursday ? 'is-dark' : '']" 
                :disabled="!offerToShow.thursday" title="Mercredi"
                @click="selectedWeekdays.thursday = !selectedWeekdays.thursday">
                M
              </button>     
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.wednesday ? 'is-info' : '', !offerToShow.wednesday ? 'is-dark' : '']" 
                :disabled="!offerToShow.wednesday" title="Jeudi"
                @click="selectedWeekdays.wednesday = !selectedWeekdays.wednesday">
                J
              </button>
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.friday ? 'is-info' : '', !offerToShow.friday ? 'is-dark' : '']" 
                :disabled="!offerToShow.friday" title="Vendredi"
                @click="selectedWeekdays.friday = !selectedWeekdays.friday">
                V
              </button>
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.saturday ? 'is-info' : '', !offerToShow.saturday ? 'is-dark' : '']"
                :disabled="!offerToShow.saturday" title="Samedi"
                @click="selectedWeekdays.saturday = !selectedWeekdays.saturday">
                S
              </button>
              <button class="button is-rounded ch-5 is-size-6" 
                :class="[selectedWeekdays.sunday ? 'is-info' : '', !offerToShow.sunday ? 'is-dark' : '']"
                :disabled="!offerToShow.sunday" title="Dimanche"
                @click="selectedWeekdays.sunday = !selectedWeekdays.sunday">
                D
              </button>
          </div>
        </div>
        <div v-if="currentStep == 3">
          <div class="has-text-centered" v-if="!clickedSend">
            <h2 class="title mb-5">Veuillez confirmer votre demande</h2>
            <label class="checkbox mb-5">
              <input type="checkbox" v-model="confirmationCheckbox">
              Je confirme avoir validé ma demande
            </label>
          </div>
          <div v-if="clickedSend">
            <h2 class="title has-text-centered mb-5">Demande envoyée avec succès</h2>
            <div class="animate__animated animate__zoomInDown">
              <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot is-flex is-justify-content-space-evenly">
          <button class="button is-primary is-rounded w-100" v-if="currentStep > 1" @click="currentStep--">
            <span class="icon"> 
              <i class="fa fa-arrow-left mr-2"></i>
              Retour
            </span>
          </button>
          <button class="button is-primary is-rounded w-100"
            :disabled="currentStep == 2 && Object.keys(selectedWeekdays).every((k) => !selectedWeekdays[k])"
            :title="currentStep == 2 && Object.keys(selectedWeekdays).every((k) => !selectedWeekdays[k]) ? 'Vous devez choisir au moins une journée':''"
            v-if="currentStep < 3" 
            @click="currentStep++">
            <span class="icon">
              Suivant 
              <i class="fa fa-arrow-right ml-2"></i>
            </span>
          </button>
          <button class="button is-primary is-rounded w-100"
            :disabled="currentStep == 3 && !confirmationCheckbox"
            :title="currentStep == 3 && !confirmationCheckbox ? 'Vous devez confirmer votre demande':''"
            v-if="currentStep == 3" 
            @click="clickedSend = true">
            <span class="icon">
              Envoyer 
              <i class="fa fa-paper-plane ml-2"></i>
            </span>
          </button>
      </footer> 
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import DetailedOffer from "@/components/DetailedOffer";
  import StepsWizard from "bulma-steps/dist/js/bulma-steps.js";
  export default {
    name: "Home",
    data() {
      return {
        // Offer modal
        currentStep: 1,
        step2Completed: false,
        step3Completed: false,
        offerToShow: Object,
        offerUserInfo: Object,
        offerModalActive: false,
        selectedWeekdays: {
          monday: false,
          tuesday: false,
          wednesday: false,
          thursday: false,
          friday: false,
          saturday: false,
          sunday: false,
        },
        confirmationCheckbox: false,
        clickedSend: false,
        
        // La valeur de "query" est hard codé pour le moment. Il va falloir faire categories[0] 
        // lorsque nous allons avoir la liste des catégories pour peupler le dropdown.
        query_typeservice: "Tout",
        query_serviceday: new Date(),
        query_mots_cles: '',
        offers: [],
        isFetchingOffers: false,
        select_serviceday: '',
        dateToday: '',
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
      StepsWizard.attach(this.$refs.stepsSection.el);
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
        const params = new URLSearchParams();

        if(this.query_typeservice != 'Tout'){
          params.append('type-service', this.query_typeservice);
        }

        if(this.query_serviceday instanceof Date && !isNaN(this.query_serviceday)){
          params.append('date', this.query_serviceday.toISOString().split('T')[0]);
          params.append('day-of-week', this.weekdays[this.query_serviceday.getDay()]);
        }

        if(this.query_mots_cles.split(' ').length > 0){
          this.query_mots_cles.trim();
          params.append('mots-cles', this.query_mots_cles.split(' '));
        }

        await axios
          .get("/api/v1/offers/search?" + params.toString())
          .then((response) => {
            this.offers = response.data;
          })
          .catch((error) => {
            console.log(error);
          });
        this.isFetchingOffers = false;
      },
      async getOfferUserInfo(user_id){
        await axios
        .get(`api/v1/userinfo/${user_id}/`)
        .then((response) =>{
          this.offerUserInfo = response.data;
        })
        .catch((error)=>{
          console.log(error);
        });
      },
      updateCalendarToday(){
        var current = new Date();
        this.query_serviceday = this.dateToday = `${current.getFullYear()}-${current.getMonth()+1}-${current.getDate()}`;
      },
      showOfferModal(offer){
        this.offerToShow = offer;
        this.offerModalActive = true;
        if(this.offerUserInfo.user != offer.user){
          this.getOfferUserInfo(offer.user);  
        }
      },
      closeOfferModal(){
        this.resetOfferModal();
      },
      resetOfferModal(){
        this.offerModalActive = false;
        this.currentStep = 1;
        this.step2Completed = false,
        this.step3Completed = false,
        this.offerToShow = {};
        this.offerUserInfo = {};
        this.confirmationCheckbox = false;
        this.clickedSend = false;
        Object.keys(this.selectedWeekdays).forEach(value => this.selectedWeekdays[value] = false);
      }
    },
  };
</script>
<style lang="scss" scoped>
  @import "../../node_modules/bulma-steps";
	.ch-5 {
		width: 5ch;
  }

  .checkmark__circle {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 4;
    stroke-miterlimit: 10;
    stroke: #26AD80;
    fill: none;
    animation: stroke 0.75s cubic-bezier(0.65, 0, 0.45, 1) forwards;
  }

  .checkmark {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: block;
    stroke-width: 2;
    stroke: #26AD80;
    stroke-miterlimit: 10;
    margin: 0 auto 30px;
    box-shadow: inset 0px 0px 0px #26AD80;
    animation: fill 0.5s ease-in-out 0.5s forwards, scale 0.5s ease-in-out .9s both;
    animation-delay: 1s;
  }

  .checkmark__check {
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke 0.5s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
    animation-delay: 1s;
  }

  @keyframes stroke {
    100% {
      stroke-dashoffset: 0;
    }
  }

  @keyframes scale {
    0%, 100% {
      transform: none;
    }
    50% {
      transform: scale3d(1.1, 1.1, 1);
    }
  }

  @keyframes fill {
    100% {
      box-shadow: inset 0px 0px 0px 60px transparent;
    }
  }
  
  .step-item{
    flex-basis: 0!important;
  }

</style>