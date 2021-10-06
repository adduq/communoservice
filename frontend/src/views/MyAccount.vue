<template>
  <div class="page-my-account">
    <div class="columns is-mobile">
      <div class="column">
        <div class="buttons has-addons">
          <button class="button" v-on:click="profileSwitch = false" :class="profileSwitch == false ? 'is-success is-selected' : ''">Employé</button>
          <button class="button" v-on:click="profileSwitch = true" :class="profileSwitch == true ? 'is-success is-selected' : ''">Employeur</button>
        </div>
      </div>
      <div class="column">
        <figure class="image is-128x128 round-shadow has-image-centered">
          <img
            class="is-rounded"
            src="https://axim-auto.fr/wp-content/uploads/2019/09/0_200.png"
          />
          <i class="fas fa-circle" :class="userIsActive ? 'active-icon':'not-active-icon'"></i>
          <figcaption class="has-text-centered">[nom ici]</figcaption>
        </figure>
      </div>
      <div class="column has-text-right"></div>
    </div>
    <div class="columns mt-6">
      <template v-if="profileSwitch == false">
        <div class="column">
          <div class="box">
            <h3 class="test-classe">Créer un service</h3>

            <div class="field">
              <label class="label">Type de service</label>
              <div class="control">
                <div class="select">
                  <select class="w-200">
                    <option>Tonte de pelouse</option>
                    <option>Déneigement</option>
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
                <input class="input" type="text" placeholder="Montant" />
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
                      v-on:click="daysSelected.thursday = !daysSelected.thursday"
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
                      v-on:click="daysSelected.saturday = !daysSelected.saturday"
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
              <label class="label">Message</label>
              <div class="control">
                <textarea
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
              <button
                class="button is-success w-200"
                v-on:click="modalCreateisActive = !modalCreateisActive"
              >
                Créer
              </button>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="box">
            <h3 class="test-classe">Mes services actifs</h3>

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
            <h3 class="test-classe">Mes services prévues</h3>

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
          <button class="button is-success w-100">Oui</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ActiveOffer from "@/components/ActiveOffer";
export default {
  name: "MyAccount",
  data() {
    return {
      offers: [],
      modalCreateisActive: false,
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
    };
  },
  //Les components qu'on veut utiliser
  components: {
    ActiveOffer,
  },
  mounted() {
    document.title = "Mon compte | Communoservice";
    this.getAllOffers();
  },
  methods: {
    async getAllOffers(){
      this.$store.commit("setIsLoading", true);
      
      await axios
        .get("/api/v1/offers/")
        .then((response) => {
          this.offers = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    }
  },
};
</script>