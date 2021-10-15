<template>
  <div class="page-my-account">
    <div class="container profile">
      <div class="section profile-heading">
        <div class="columns">
          <div class="column is-one-fifth">
            <figure class="image is-128x128 round-shadow has-image-centered">
              <img
                class="is-rounded"
                src="https://owcdn.net/img/5bda50b474984.jpg"
              />
              <i
                class="fas fa-circle"
                :class="userIsActive ? 'active-icon' : 'not-active-icon'"
              ></i>
            </figure>
          </div>
          <div class="column is-one-third">
            <p>
              <span class="title is-bold">{{
                userInfo.first_name + " " + userInfo.last_name
              }}</span>
            </p>
            <p class="tagline">
              I am a French Canadian Twitch streamer, former Overwatch League
              player, current Luminosity Gaming member and G FUEL partner.
            </p>
          </div>
          <div class="column ml-5">
            <div class="columns is-mobile is-centered">
              <template v-if="profileSwitch == false">
                <div class="column has-text-centered">
                  <p class="stat-val">{{ userInfo.nb_services_given }}</p>
                  <p class="stat-key">services rendus</p>
                </div>
                <div class="column has-text-centered">
                  <p class="stat-val">{{ offers.length }}</p>
                  <p class="stat-key">services actifs</p>
                </div>
                <div class="column has-text-centered">
                  <p class="stat-val">
                    {{ userInfo.avg_rating_as_employee }}/10
                  </p>
                  <p class="stat-key">score</p>
                </div>
              </template>
              <template v-if="profileSwitch == true">
                <div class="column has-text-centered">
                  <p class="stat-val">{{ userInfo.nb_services_received }}</p>
                  <p class="stat-key">services reçus</p>
                </div>
                <div class="column has-text-centered">
                  <p class="stat-val">{{ offers.length }}</p>
                  <p class="stat-key">services actifs</p>
                </div>
                <div class="column has-text-centered">
                  <p class="stat-val">
                    {{ userInfo.avg_rating_as_employer }}/10
                  </p>
                  <p class="stat-key">score</p>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="columns is-centered mt-6">
      <div class="column buttons has-addons is-half has-text-centered">
        <button
          class="button profile-toggle"
          v-on:click="profileSwitch = false"
          :class="profileSwitch == false ? 'is-success is-selected' : ''"
        >
          Employé
        </button>
        <button
          class="button profile-toggle"
          v-on:click="profileSwitch = true"
          :class="profileSwitch == true ? 'is-success is-selected' : ''"
        >
          Employeur
        </button>
      </div>
    </div>
    <div class="columns">
      <template v-if="profileSwitch == false">
        <div class="column">
          <div class="box">
            <h3 class="test-classe">Créer un service</h3>

            <div class="field">
              <label class="label">Type de service</label>
              <div class="control">
                <div class="select">
                  <select v-model="serviceType" class="w-200">
                    <option>Tonte de pelouse</option>
                    <option>Déneigement</option>
                    <option>Gardiennage</option>
                    <option>Administration</option>
                  </select>
                </div>
              </div>
            </div>
            <label class="label">Taux horaire</label>
            <div class="field has-addons">
              <p class="control">
                <span class="select">
                  <select>
                    <option>$</option>
                    <option>BTC</option>
                    <option>ETH</option>
                  </select>
                </span>
              </p>
              <p class="control">
                <input
                  v-model="hourlyRate"
                  class="input"
                  type="number"
                  placeholder="Montant"
                />
              </p>
            </div>

            <label class="label">Distance maximale</label>
            <div class="field has-addons">
              <p class="control">
                <input
                  v-model="maxDistance"
                  class="input"
                  type="number"
                  placeholder="Distance"
                />
              </p>
            </div>

            <div class="field">
              <label class="label">Disponibilités</label>
              <div>
                <div
                  class="columns is-mobile is-family-monospace buttons is-grouped is-justify-content-space-around mt-2"
                >
                  <div class="control ml-0">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.monday ? 'is-success' : ''"
                      v-on:click="daysSelected.monday = !daysSelected.monday"
                    >
                      L
                    </a>
                  </div>
                  <div class="control">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.tuesday ? 'is-success' : ''"
                      v-on:click="daysSelected.tuesday = !daysSelected.tuesday"
                    >
                      M
                    </a>
                  </div>
                  <div class="control">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.wednesday ? 'is-success' : ''"
                      v-on:click="
                        daysSelected.wednesday = !daysSelected.wednesday
                      "
                    >
                      M
                    </a>
                  </div>
                  <div class="control">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.thursday ? 'is-success' : ''"
                      v-on:click="
                        daysSelected.thursday = !daysSelected.thursday
                      "
                    >
                      J
                    </a>
                  </div>
                  <div class="control">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.friday ? 'is-success' : ''"
                      v-on:click="daysSelected.friday = !daysSelected.friday"
                    >
                      V
                    </a>
                  </div>
                  <div class="control">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.saturday ? 'is-success' : ''"
                      v-on:click="
                        daysSelected.saturday = !daysSelected.saturday
                      "
                    >
                      S
                    </a>
                  </div>
                  <div class="control mr-0">
                    <a
                      class="button is-rounded"
                      :class="daysSelected.sunday ? 'is-success' : ''"
                      v-on:click="daysSelected.sunday = !daysSelected.sunday"
                    >
                      D
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Expiration</label>
              <input
                type="date"
                v-bind:min="tomorrow"
                v-model="expirationDate"
              />
            </div>

            <div class="field">
              <label class="label">Message</label>
              <div class="control">
                <textarea
                  v-model="description"
                  class="textarea"
                  placeholder="Votre message ici..."
                ></textarea>
              </div>
            </div>

            <div class="field">
              <div class="control">
                <label class="checkbox">
                  <input type="checkbox" />
                  J'accepte les <a href="#">termes et conditions</a>
                </label>
              </div>
            </div>
            <div class="has-text-centered">
              <button class="button is-success w-200" v-on:click="validateForm">
                Créer
              </button>
            </div>
            <div class="notification is-danger mt-4" v-if="errors.length">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="box">
            <h3 class="test-classe">Mes services actifs</h3>

            <DetailedOffer
              v-for="offer in offers"
              v-bind:key="offer.id"
              v-bind:offer="offer"
            />
          </div>
        </div>

        <div class="column">
          <div class="box">
            <h3 class="test-classe">Historique</h3>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Location ici</p>
                  </div>
                </div>

                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-success">
                      <span class="icon">
                        <i class="fas fa-check-square"></i>
                      </span>
                      <span>Complété</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Location ici</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-warning">
                      <span class="icon">
                        <i class="fas fa-exclamation-triangle"></i>
                      </span>
                      <span>Cancelé</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Location ici</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-success">
                      <span class="icon">
                        <i class="fas fa-check-square"></i>
                      </span>
                      <span>Complété</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Localisation ici</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-danger">
                      <span class="icon">
                        <i class="fas fa-ban"></i>
                      </span>
                      <span>Non complété</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template v-if="profileSwitch == true">
        <div class="column">
          <div class="box">
            <h3 class="test-classe">Mes services prévus</h3>

            <ActiveOffer
              v-for="offer in offers"
              v-bind:key="offer.id"
              v-bind:offer="offer"
            />
          </div>
        </div>

        <div class="column">
          <div class="box">
            <h3 class="test-classe">Historique</h3>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Location ici</p>
                  </div>
                </div>

                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-success">
                      <span class="icon">
                        <i class="fas fa-check-square"></i>
                      </span>
                      <span>Complété</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Location ici</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-warning">
                      <span class="icon">
                        <i class="fas fa-exclamation-triangle"></i>
                      </span>
                      <span>Annulé</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Location ici</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-success">
                      <span class="icon">
                        <i class="fas fa-check-square"></i>
                      </span>
                      <span>Complété</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card mb-3 h-140">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        src="https://bulma.io/images/placeholders/96x96.png"
                        alt="Placeholder image"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title is-4">Type de service</p>
                    <p class="subtitle is-6">Localisation ici</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column is-half">
                    <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
                  </div>
                  <div class="column is-half pb-0">
                    <span class="icon-text has-text-danger">
                      <span class="icon">
                        <i class="fas fa-ban"></i>
                      </span>
                      <span>Non complété</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
    <span class="icon-text has-text-danger">
      <span class="icon">
        <i class="fas fa-arrow-right-from-bracket"></i>
      </span>
    </span>

    <div class="modal" v-bind:class="{ 'is-active': modalCreateisActive }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmation</p>
          <button
            class="delete"
            v-on:click="modalCreateisActive = !modalCreateisActive"
            aria-label="close"
          ></button>
        </header>
        <section class="modal-card-body">
          Êtes-vous certain de vouloir créer ce service?
        </section>
        <footer class="modal-card-foot">
          <button
            class="button is-danger w-100"
            v-on:click="modalCreateisActive = !modalCreateisActive"
          >
            Non
          </button>
          <button v-on:click="addNewOffer" class="button is-success w-100">
            Oui
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import DetailedOffer from "@/components/DetailedOffer";

export default {
  name: "MyAccount",
  data() {
    return {
      offers: [],
      modalCreateisActive: false,
      serviceType: "",
      description: "",
      hourlyRate: 10.5,
      maxDistance: 2,
      expirationDate: "",
      daysSelected: {
        monday: false,
        tuesday: false,
        wednesday: false,
        thursday: false,
        friday: false,
        saturday: false,
        sunday: false,
      },
      profileSwitch: false,
      userIsActive: true,
      userInfo: {},
      errors: [],
      tomorrow:""
    };
  },
  //Les components qu'on veut utiliser
  components: {
    DetailedOffer,
  },
  mounted() {
    document.title = "Mon compte | Communoservice";
    this.getUserInfo();
    this.tomorrow = this.getTomorrow();
  },
  methods: {
    getTomorrow() {
      var tomorrow = new Date();
      var dd = String(tomorrow.getDate()+1).padStart(2, "0");
      var mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); //January is 0.
      var yyyy = tomorrow.getFullYear();

      tomorrow = yyyy + "-" + mm + "-" + dd;
      return tomorrow;
    },
    async getAllOffers(userId) {
      await axios
        .get(`/api/v1/offers/user/${userId}/`)
        .then((response) => {
          this.offers = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    validateForm() {
      this.errors = [];
      if (this.serviceType === "") {
        this.errors.push("Il faut choisir un type.");
      }

      this.description = this.description.trim();

      if (this.hourlyRate < 0) {
        this.errors.push("Le taux horaire doit être un nombre positif.");
      }
      if (this.maxDistance < 0) {
        this.errors.push("La distance maximal doit être positive.");
      }
      let tomorrow = new Date();
      let selectedDate = new Date(this.expirationDate);
      if (selectedDate.getTime() < tomorrow.getTime()) {
        this.errors.push("Il faut choisir une date postérieure à aujourd'hui.");
      }

      if (!this.errors.length) {
        this.modalCreateisActive = true;
      }
    },
    async addNewOffer() {
      this.isLoading = true;
      let expiration = this.expirationDate=="" ? null : this.expirationDate;
      const newOffer = {
        user: this.userInfo.user_id,
        type_service: this.serviceType,
        description: this.description,
        hourly_rate: this.hourlyRate,
        max_distance: this.maxDistance,
        expiration_date:expiration,
        monday: this.daysSelected.monday,
        tuesday: this.daysSelected.tuesday,
        wednesday: this.daysSelected.wednesday,
        thursday: this.daysSelected.thursday,
        friday: this.daysSelected.friday,
        saturday: this.daysSelected.saturday,
        sunday: this.daysSelected.sunday,
      };
      //alert(JSON.stringify(newOffer));//pour validation.
      await axios
        .post("/api/v1/offers/", newOffer)
        .then((response,userId) => {
          this.isLoading = false;
          this.modalCreateisActive=false;
          console.log(response);
         this.getAllOffers(response.data.user);
        })
        .catch((error) => {
          this.modalCreateisActive=false;
          this.errors.push("Une erreur est survenue. Essayez à nouveau.");
          console.log(error);
        });
    },
    toSelectDate(payload) {
      alert(payload);
    },
    async getUserInfo() {
      await axios
        .get("/api/v1/userinfo/me")
        .then((response) => {
          this.userInfo = response.data;
          this.userIsActive = this.userInfo["is_active"];
          this.getAllOffers(this.userInfo.user_id)
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.profile-toggle {
  width: 8em !important;
}
.active-icon {
  position: absolute;
  right: 6%;
  bottom: 6%;
  font-size: 1.5em;
  color: rgb(49, 162, 76);
}
.not-active-icon {
  position: absolute;
  right: 6%;
  bottom: 6%;
  font-size: 1.5em;
  color: grey;
}
.stat-key {
  font-size: 20px;
  font-weight: 200;
}
.stat-val {
  font-size: 35px;
  font-weight: bold;
}
.tagline {
  padding: 20px 0;
  font-size: 16px;
  line-height: 1.4;
}
.avatar {
  object-fit: cover;
  border-radius: 50%;
  width: 150px;
  height: 150px;
  box-shadow: 0px 2px 8px 3px darkgrey;
}
p.title.is-bold {
  font-weight: bold;
}
</style>
