<template>
	<div class="page-my-account">
		<div class="box has-background-dark has-text-white">
			<div class="container profile">
				<div class="section profile-heading">
					<div class="columns">
						<div class="column has-text-centered">
							<figure
								class="image is-128x128 round-shadow has-image-centered"
							>
								<img
									class="is-rounded"
									src="https://owcdn.net/img/5bda50b474984.jpg"
								/>
								<span
									class="badge is-bottom-right"
									:class="
										userInfo.is_active
											? 'active-icon'
											: 'not-active-icon'
									"
									:title="
										userInfo.is_active ? 'Actif' : 'Inactif'
									"
								></span>
							</figure>
							<p class="mt-2">
								<span
									class="title is-bold has-text-white"
									v-if="
										userInfo.first_name &&
											userInfo.last_name
									"
								>
									{{
										userInfo.first_name +
											" " +
											userInfo.last_name
									}}
								</span>
								<span
									class="title is-bold has-text-white"
									v-else
								>
									{{ userInfo.username }}
								</span>
							</p>
							<p
								class="has-text-grey"
								v-if="userInfo.first_name && userInfo.last_name"
							>
								<i class="has-text-success">@</i>
								{{ userInfo.username }}
							</p>
							<p
								v-if="userInfo.user_bio"
								class="has-text-grey mt-3 is-italic user-bio"
							>
								{{ "“ " + userInfo.user_bio + " ”" }}
							</p>
						</div>
					</div>
					<div
						v-if="!profileSwitch"
						class="is-flex is-flex-wrap-wrap is-justify-content-space-evenly"
					>
						<div class="has-text-centered">
							<p class="has-text-weight-bold is-size-3">
								{{ userInfo.nb_services_given }}
							</p>
							<p>services rendus</p>
						</div>
						<div class="has-text-centered">
							<p class="has-text-weight-bold is-size-3">
								{{ activeOffers.length }}
							</p>
							<p>services actifs</p>
						</div>
						<div class="has-text-centered">
							<p class="has-text-weight-bold is-size-3">
								{{ userInfo.avg_rating_as_employee }}/10
							</p>
							<p>score</p>
						</div>
					</div>
					<div
						v-else
						class="is-flex is-flex-wrap-wrap is-justify-content-space-evenly"
					>
						<div class="has-text-centered">
							<p class="has-text-weight-bold is-size-3">
								{{ userInfo.nb_services_received }}
							</p>
							<p>services reçus</p>
						</div>
						<div class="has-text-centered">
							<p class="has-text-weight-bold is-size-3">
								{{ reservedOffersForRecruiter.length }}
							</p>
							<p>services en attente</p>
						</div>
						<div class="has-text-centered">
							<p class="has-text-weight-bold is-size-3">
								{{ userInfo.avg_rating_as_employer }}/10
							</p>
							<p>score</p>
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
					:class="
						profileSwitch == false ? 'is-success is-selected' : ''
					"
				>
					Employé
				</button>
				<button
					class="button profile-toggle"
					v-on:click="profileSwitch = true"
					:class="
						profileSwitch == true ? 'is-success is-selected' : ''
					"
				>
					Employeur
				</button>
			</div>
		</div>
		<div class="columns">
			<template v-if="profileSwitch == false">
				<div
					class="modal"
					:class="creationModalIsActive ? 'is-active' : ''"
				>
					<div
						class="modal-background"
						@click="closeOfferModal()"
					></div>
					<div class="modal-card">
						<header class="modal-card-head">
							<p class="modal-card-title">Créer un service</p>
							<button
								class="delete has-background-danger"
								v-on:click="closeOfferModal()"
								aria-label="close"
							></button>
						</header>

						<section class="modal-card-body">
							<div
								class="is-flex-desktop is-justify-content-space-between mr-6"
							>
								<div class="field">
									<label class="label">Type de service</label>
									<div class="control">
										<div class="select">
											<select
												v-model="serviceType"
												class="w-200"
											>
												<option
													value=""
													disabled
													selected
													>Choisir parmi</option
												>
												<option
													v-for="type in serviceTypes"
													v-bind:key="type.name"
													>{{ type.name }}</option
												>
											</select>
										</div>
									</div>
								</div>

                <div class="field mb-2 mr-6">
                  <label class="label">Expiration</label>
                  <input
                    type="date"
                    class="datepicker"
                    v-bind:min="tomorrow"
                    v-model="expirationDate"
                  />
                </div>
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
												:class="
													daysSelected.monday
														? 'is-success'
														: ''
												"
												v-on:click="
													daysSelected.monday = !daysSelected.monday
												"
											>
												L
											</a>
										</div>
										<div class="control">
											<a
												class="button is-rounded"
												:class="
													daysSelected.tuesday
														? 'is-success'
														: ''
												"
												v-on:click="
													daysSelected.tuesday = !daysSelected.tuesday
												"
											>
												M
											</a>
										</div>
										<div class="control">
											<a
												class="button is-rounded"
												:class="
													daysSelected.wednesday
														? 'is-success'
														: ''
												"
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
												:class="
													daysSelected.thursday
														? 'is-success'
														: ''
												"
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
												:class="
													daysSelected.friday
														? 'is-success'
														: ''
												"
												v-on:click="
													daysSelected.friday = !daysSelected.friday
												"
											>
												V
											</a>
										</div>
										<div class="control">
											<a
												class="button is-rounded"
												:class="
													daysSelected.saturday
														? 'is-success'
														: ''
												"
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
												:class="
													daysSelected.sunday
														? 'is-success'
														: ''
												"
												v-on:click="
													daysSelected.sunday = !daysSelected.sunday
												"
											>
												D
											</a>
										</div>
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
              <div class="">
                <label class="label">Entrez le range</label>
                <FullCalendar
                  ref="fullCalendar"
                  :options="calendarOptions"
                  :header="header"
                />
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
										J'accepte les
										<a href="#">termes et conditions</a>
									</label>
								</div>
							</div>
						</section>

						<footer
							class="modal-card-foot is-flex is-justify-content-center"
						>
							<button
								class="button is-success w-200"
								v-on:click="validateForm"
							>
								Créer
							</button>
							<button
								class="button is-danger w-200"
								v-on:click="closeOfferModal()"
							>
								Fermer
							</button>
						</footer>
					</div>
				</div>

				<div class="column">
					<div class="box">
						<p class="title has-text-centered">
							Mes services actifs
						</p>
						<div class="offers-container">
							<DetailedOffer
								v-for="offer in activeOffers"
								v-bind:key="offer.id"
								v-bind:offer="offer"
							/>
						</div>
						<div class="is-flex is-justify-content-center">
							<a
								href="#"
								class="button is-info mt-5"
								v-on:click="openCreationModal()"
							>
								<span class="icon is-small mr-3">
									<i
										class="fa fa-plus-circle"
										aria-hidden="true"
									></i>
								</span>
								<span> Créer un service </span>
							</a>
						</div>
					</div>
				</div>

				<div class="column">
					<div class="box">
						<p class="title has-text-centered">
							Mes services réservés
						</p>
						<div class="offers-container">
							<ReservedOffer
								v-for="offer in reservedOffersForUser"
								v-bind:key="offer.id"
								v-bind:reservedOffer="offer"
							/>
						</div>
					</div>
				</div>

				<div class="column">
					<div class="box">
						<p class="title has-text-centered">Historique</p>
						<div class="offers-container">
							<TerminatedOffer
								v-for="offer in terminatedOffersForUser"
								v-bind:key="offer.id"
								v-bind:terminatedOffer="offer"
							/>
						</div>
					</div>
				</div>
			</template>
			<template v-if="profileSwitch == true">
				<div class="column">
					<div class="box">
						<p class="title has-text-centered">
							Mes services prévus
						</p>
						<div class="offers-container">
							<ReservedOffer
								v-for="offer in reservedOffersForRecruiter"
								v-bind:key="offer.id"
								v-bind:reservedOffer="offer"
							/>
						</div>
					</div>
				</div>

				<div class="column">
					<div class="box">
						<p class="title has-text-centered">Historique</p>
						<div class="offers-container">
							<TerminatedOffer
								v-for="offer in terminatedOffersForRecruiter"
								v-bind:key="offer.id"
								v-bind:terminatedOffer="offer"
							/>
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
			<div
				class="modal-background"
				v-on:click="modalCreateisActive = !modalCreateisActive"
			></div>
			<div class="modal-card">
				<header class="modal-card-head">
					<p class="modal-card-title">Confirmation</p>
					<button
						class="delete has-background-danger"
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
						v-on:click="closeOfferModal()"
					>
						Non
					</button>
					<button
						v-on:click="addNewOffer"
						class="button is-success w-100"
					>
						Oui
					</button>
				</footer>
			</div>
		</div>
	</div>
</template>

<script>
// TODO: Création d'un loader pour les services.

import axios from "axios";
import DetailedOffer from "@/components/DetailedOffer";
import TerminatedOffer from "@/components/TerminatedOffer";
import ReservedOffer from "@/components/ReservedOffer";
import { toast } from "bulma-toast";

import "@fullcalendar/core/vdom"; // solves problem with Vite
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import frLocale from "@fullcalendar/core/locales/fr";

export default {
	name: "MyAccount",
	data() {
		return {
			activeOffers: [],
			terminatedOffersForUser: [],
			terminatedOffersForRecruiter: [],
			reservedOffersForUser: [],
			reservedOffersForRecruiter: [],
			serviceTypes: [],

      modalCreateisActive: false,

			serviceType: "",
			description: "",
			hourlyRate: 10.5,
			maxDistance: 1,
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
			tomorrow: "",
			creationModalIsActive: false,
		};
	},
	//Les components qu'on veut utiliser
	components: {
		DetailedOffer,
		TerminatedOffer,
		ReservedOffer,
	},
	mounted() {
		document.title = "Mon compte | Communoservice";
		this.getUserInfo();
		this.tomorrow = this.getTomorrow();
		this.getServiceTypes();
	},
	methods: {
		getTomorrow() {
			var tomorrow = new Date();
			var dd = String(tomorrow.getDate() + 1).padStart(2, "0");
			var mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); //January is 0.
			var yyyy = tomorrow.getFullYear();
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: "dayGridMonth",
        locales: [frLocale],
        selectable: true,
        select: this.select,
        dayHeaderFormat: { weekday: "short", omitCommas: true },
        headerToolbar: {
          start: "title", // will normally be on the left. if RTL, will be on the right
          center: "",
          end: "today prevYear,prev,next,nextYear", // will normally be on the right. if RTL, will be on the left
        },
      },
      header: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
      },
      startDate: String,
      endDate: String,
      profileSwitch: false,
      userIsActive: true,
      userInfo: {},
      errors: [],
      tomorrow: "",
      creationModalIsActive: false,
    };
  },
  //Les components qu'on veut utiliser
  components: {
    DetailedOffer,
    TerminatedOffer,
    ReservedOffer,
    FullCalendar,
  },
  mounted() {
    document.title = "Mon compte | Communoservice";
    this.getUserInfo();
    this.tomorrow = this.getTomorrow();
    this.getServiceTypes();
  },
  create() {
    let test = document.getElementsByClassName(".fc");
    // let test = this.$refs.fullCalendar.$el;
    console.log(test);
    test.render();
  },
  methods: {
    select(info) {
      alert("selected " + info.startStr + " to " + info.endStr);
    },
    getTomorrow() {
      var tomorrow = new Date();
      var dd = String(tomorrow.getDate() + 1).padStart(2, "0");
      var mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); //January is 0.
      var yyyy = tomorrow.getFullYear();

			tomorrow = yyyy + "-" + mm + "-" + dd;
			return tomorrow;
		},
		async getAllOffers(userId) {
			await axios
				.get(`/api/v1/active-offers/user/${userId}/`)
				.then((response) => {
					this.activeOffers = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async getTerminatedOffersForUser(userId) {
			await axios
				.get(`/api/v1/terminated-offers/user/${userId}/`)
				.then((res) => {
					this.terminatedOffersForUser = res.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async getReservedOffersForUser(userId) {
			await axios
				.get(`/api/v1/reserved-offers/user/${userId}/`)
				.then((res) => {
					this.reservedOffersForUser = res.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async getTerminatedOffersForRecruiter(recruiterId) {
			await axios
				.get(`/api/v1/terminated-offers/recruiter/${recruiterId}/`)
				.then((res) => {
					this.terminatedOffersForRecruiter = res.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async getReservedOffersForRecruiter(recruiterId) {
			await axios
				.get(`/api/v1/reserved-offers/recruiter/${recruiterId}/`)
				.then((res) => {
					this.reservedOffersForRecruiter = res.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async getServiceTypes() {
			await axios
				.get("/api/v1/service-types/")
				.then((res) => {
					this.serviceTypes = res.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		openCreationModal() {
			this.creationModalIsActive = !this.creationModalIsActive;
		},
		closeOfferModal() {
			this.creationModalIsActive = false;
			this.errors = [];
			this.modalCreateisActive = false;
		},
		validateForm() {
			this.errors = [];
			if (this.serviceType === "") {
				this.errors.push("Il faut choisir un type.");
			}

      this.description = this.description.trim();
      if (!this.description) {
        this.errors.push("La description ne peut pas être vide.");
      }

			if (this.hourlyRate < 0) {
				this.errors.push(
					"Le taux horaire doit être un nombre positif."
				);
			}
			if (this.maxDistance < 0) {
				this.errors.push("La distance maximal doit être positive.");
			}
			let tomorrow = new Date();
			let selectedDate = new Date(this.expirationDate);
			if (selectedDate.getTime() < tomorrow.getTime()) {
				this.errors.push(
					"Il faut choisir une date postérieure à aujourd'hui."
				);
			}

      if (!this.errors.length) {
        this.modalCreateisActive = true;

				this.creationModalIsActive = false;
			} else {
				for (let index = 0; index < this.errors.length; index++) {
					toast({
						message: this.errors[index],
						type: "is-danger",
						dismissible: true,
						pauseOnHover: true,
						duration: 4000,
						position: "bottom-right",
						animate: {
							in: "fadeInRightBig",
							out: "fadeOutRightBig",
						},
					});
				}
			}
		},
		async addNewOffer() {
			this.isLoading = true;
			let expiration =
				this.expirationDate == "" ? null : this.expirationDate;
			const newOffer = {
				user: this.userInfo.user_id,
				type_service: this.serviceType,
				description: this.description,
				hourly_rate: this.hourlyRate,
				max_distance: this.maxDistance,
				expiration_date: expiration,
				monday: this.daysSelected.monday,
				tuesday: this.daysSelected.tuesday,
				wednesday: this.daysSelected.wednesday,
				thursday: this.daysSelected.thursday,
				friday: this.daysSelected.friday,
				saturday: this.daysSelected.saturday,
				sunday: this.daysSelected.sunday,
			};
			await axios
				.post("/api/v1/offers/", newOffer)
				.then((response) => {
					this.isLoading = false;
					this.modalCreateisActive = false;
					this.creationModalIsActive = false;

					this.addActiveOffers({
						id_offer: response.data.id,
						id_user: response.data.user,
					});
				})
				.catch((error) => {
					this.modalCreateisActive = false;
					this.creationModalIsActive = true;
					if (error.response.data["error"] == "profile_incomplete") {
						toast({
							message:
								"Profil incomplet. Veuillez completer votre profil dans les paramètres.",
							type: "is-danger",
							dismissible: true,
							pauseOnHover: true,
							duration: 4000,
							position: "bottom-right",
							animate: {
								in: "fadeInRightBig",
								out: "fadeOutRightBig",
							},
						});
					} else {
						toast({
							message:
								"Une erreur est survenue. Essayez à nouveau.",
							type: "is-danger",
							dismissible: true,
							pauseOnHover: true,
							duration: 4000,
							position: "bottom-right",
							animate: {
								in: "fadeInRightBig",
								out: "fadeOutRightBig",
							},
						});
					}
				});
		},
		toSelectDate(payload) {
			alert(payload);
		},
		async addActiveOffers(activeOffer) {
			await axios
				.post("/api/v1/active-offers/", activeOffer)
				.then((response, userId) => {
					this.getAllOffers(activeOffer.id_user);
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async getUserInfo() {
			await axios
				.get("/api/v1/userinfo/me/")
				.then((response) => {
					this.userInfo = response.data;
					this.userIsActive = this.userInfo["is_online"];
					this.getAllOffers(this.userInfo.user_id);
					this.getTerminatedOffersForUser(this.userInfo.user_id);
					this.getTerminatedOffersForRecruiter(this.userInfo.user_id);
					this.getReservedOffersForUser(this.userInfo.user_id);
					this.getReservedOffersForRecruiter(this.userInfo.user_id);
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
option[value=""][disabled] {
	display: none;
}

.offers-container {
	max-height: 500px;
	overflow: hidden;
	overflow-y: scroll;
}
.offers-container::-webkit-scrollbar {
	width: 14px;
}

.offers-container::-webkit-scrollbar-thumb {
	border: 4px solid rgba(0, 0, 0, 0);
	background-clip: padding-box;
	border-radius: 9999px;
	background-color: #aaaaaa;
}
.user-bio{
	margin:auto;
	max-width: 500px;
}
</style>
