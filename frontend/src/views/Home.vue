<template>
	<div class="home">
		<section class="hero is-large" :class="this.heroCollapsed ? 'collapse' : ''">
			<div class="hero-body has-text-centered">
				<p class="title mb-6 is-size-1 has-text-weight-bold">Bienvenue sur Communoservice</p>
				<p class="subtitle animate__animated animate__fadeInLeftBig">
					Le meilleur site pour les services communautaires
				</p>

				<a href="#search" class="animate__animated animate__fadeInUp button is-primary is-rounded animate__delay-1s mt-4">
					Rechercher
				 <i class="fas fa-chevron-down ml-2" aria-hidden="true"></i>
				</a>
			</div>
		</section>
		<div class="columns is-multiline is-12">
			<div class="column is-12">
				<h2 id="search" class="is-size-2 has-text-centered">
					{{$store.state.isAuthenticated && $store.state.userInfo.profile_is_completed ? 'Services offerts dans mon entourage': 'Liste des services actifs'}}
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
							<input
								class="input"
								type="text"
								placeholder="Mots Clé(s)"
								v-model="query_mots_cles"
							/>
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
							<select v-model="query_typeservice">
								<option>Tout</option>
								<option v-for="type in serviceTypes" v-bind:key="type.name">{{
									type.name
								}}</option>
							</select>
						</div>
					</div>
					<div class="panel-section">
						<p class="ml-2 has-text-weight-bold has-text-black">
							Date
						</p>
						<input
							class="datepicker ml-2 mt-1"
							type="date"
							:min="dateToday"
							v-model="select_serviceday"
						/>
					</div>

					<div class="panel-block">
						<button
							@click="sendQuery"
							class="button is-link is-outlined is-fullwidth"
						>
							Rechercher
						</button>
					</div>
					<!-- <div class="panel-block">
						<button
							@click="sendQuery"
							class="button is-link is-outlined is-fullwidth"
							:class="isFetchingOffers ? 'is-loading' : ''"
						>
							Rechercher
						</button>
					</div> -->
					<div class="panel-block" v-if="saveParams !== null">
						<button
							@click="resetSearchParams"
							class="button is-danger is-outlined is-fullwidth"
						>
							Réinitialiser la recherche
						</button>
					</div>
				</nav>
			</div>
			<div class="column is-two-thirds">
				<div class="box is-relative offers-box">
					<div class="loader-wrapper" :class="isFetchingOffersOnScroll ? 'is-active' : ''">
						<div class="is-loading" :class="isFetchingOffersOnScroll ? 'loader' : ''">
						</div>
					</div>
					<div id="list-services" class="offers-container" @scroll="scrollAction" v-if="this.offers.length > 0">
						<DetailedOffer
							v-for="offer in offers"
							v-bind:key="offer.id"
							v-bind:offer="offer"
							@click="showOfferModal(offer)"
						/>
					</div>
					<p v-if="!this.isFetchingOffersOnScroll && this.offers.length == 0" class="mt-4 is-size-4 has-text-centered">
						Aucune offre disponible à proximité.
					</p>
				</div>
			</div>
		</div>
	</div>
	<div class="modal" :class="offerModalActive ? 'is-active' : ''">
		<div class="modal-background" @click="closeOfferModal()"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title" v-if="currentStep == 1">
					Détails de l'offre
				</p>
				<p class="modal-card-title" v-if="currentStep == 2">
					Choix des disponibilités
				</p>
				<p class="modal-card-title" v-if="currentStep == 3">Confirmation</p>
				<button
					class="delete has-background-danger"
					aria-label="close"
					@click="closeOfferModal()"
				></button>
			</header>
			<section class="modal-card-body">
				<ul class="steps is-small" ref="stepsSection">
					<li
						class="step-item is-info is-completed"
						:class="currentStep >= 1 ? 'is-active ' : ''"
					>
						<div class="step-marker">
							<span class="icon">
								<i class="fa fa-align-justify"></i>
							</span>
						</div>
					</li>
					<li
						class="step-item is-info"
						:class="[
							currentStep >= 2 ? 'is-active' : '',
							step2Completed ? 'is-completed' : '',
						]"
					>
						<div class="step-marker">
							<span class="icon">
								<i class="fa fa-calendar-check"></i>
							</span>
						</div>
					</li>
					<li
						class="step-item is-info"
						:class="[
							currentStep >= 3 ? 'is-active' : '',
							step3Completed ? 'is-completed' : '',
						]"
					>
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
							<span class="tag has-text-weight-bold is-size-6">{{
								offerToShow.type_service
							}}</span>
						</div>
						<div class="column has-text-centered">
							<label class="label is-size-5">Taux horaire</label>
							<span class="tag has-text-weight-bold is-size-6"
								>${{ offerToShow.hourly_rate }}/h</span
							>
						</div>
						<div class="column has-text-centered">
							<label class="label is-size-5">Distance</label>
							<span class="tag has-text-weight-bold is-size-6"
								>{{ offerToShow.max_distance }}km</span
							>
						</div>
					</div>
					<label class="label has-text-centered bt-1 pt-2 is-size-5"
						>Disponibilités</label
					>
					<div
						class="is-flex has-text-centered is-flex-wrap-wrap mt-2 is-justify-content-space-evenly is-family-monospace"
					>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.monday == true ? 'is-info' : 'is-dark'"
							title="Lundi"
						>
							L
						</span>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.tuesday == true ? 'is-info' : 'is-dark'"
							title="Mardi"
						>
							M
						</span>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.wednesday == true ? 'is-info' : 'is-dark'"
							title="Mercredi"
						>
							M
						</span>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.thursday == true ? 'is-info' : 'is-dark'"
							title="Jeudi"
						>
							J
						</span>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.friday == true ? 'is-info' : 'is-dark'"
							title="Vendredi"
						>
							V
						</span>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.saturday == true ? 'is-info' : 'is-dark'"
							title="Samedi"
						>
							S
						</span>
						<span
							class="tag is-rounded ch-5 is-size-5"
							:class="offerToShow.sunday == true ? 'is-info' : 'is-dark'"
							title="Dimanche"
						>
							D
						</span>
					</div>
					<div
						class="is-flex is-justify-content-space-evenly mt-3 is-flex-wrap-wrap"
					>
						<div class="is-flex is-align-items-center m-2">
							Disponible:
							<span class="tag is-rounded ch-5 is-size-6 ml-2 is-info"> </span>
						</div>
						<div class="is-flex is-align-items-center m-2">
							Non disponible:
							<span class="tag is-rounded ch-5 is-size-6 ml-2 is-dark"> </span>
						</div>
					</div>
					<div class="has-text-centered mt-5 mb-5 bt-1 pt-2">
						<label class="label is-size-5">Description</label>
						<p class="is-size-6">{{ offerToShow.description }}</p>
					</div>
					<div class="columns bt-1 pt-2 is-gapless">
						<div class="column">
							<div class="has-text-centered">
								<label class="label is-size-5">Date de début</label>
								<p class="is-size-6">{{ offerToShow.start_date ? offerToShow.start_date : "---"}}</p>
							</div>
						</div>
						<div class="column">
							<div class="has-text-centered">
								<label class="label is-size-5">Date de fin</label>
								<p class="is-size-6">{{offerToShow.end_date ? offerToShow.end_date : "---"}}</p>
							</div>
						</div>
					</div>
				</div>
				<div v-if="currentStep == 2">
					<div class="container profile">
						<div class="section profile-heading pt-0 pb-0">
							<div class="columns">
								<div class="column has-text-centered">
									<figure
										class="image is-128x128 round-shadow has-image-centered"
									>
										<img
											class="is-rounded"
											:src="this.MEDIA_URL + 'pfp_' + offerUserInfo.user_id + '.jpg'" 
											@error="replaceByDefault"
										/>
										<span
											class="badge is-bottom-right"
											:class="offerUserInfo.is_online ? 'active-icon' : 'not-active-icon'"
											:title="offerUserInfo.is_online ? 'Actif' : 'Inactif'"
										></span>
									</figure>
									<p class="mt-2">
										<span
											class="title is-bold"
											v-if="offerUserInfo.first_name && offerUserInfo.last_name"
										>
											{{ offerUserInfo.first_name + " " + offerUserInfo.last_name }}
										</span>
										<span
											class="title is-bold has-text-white"
											v-else
										>
											{{ offerUserInfo.username }}
										</span>
									</p>
								</div>
							</div>
							<div class="columns is-mobile is-flex-wrap-wrap is-justify-content-center">
								<div class="column has-text-centered is-4-desktop">
									<p class="has-text-weight-bold is-size-3">
										{{ offerUserInfo.nb_services_given }}
									</p>
									<p>services rendus</p>
								</div>
								<div class="column has-text-centered is-4-desktop">
									<p class="has-text-weight-bold is-size-3">
										{{ offerUserInfo.avg_rating_as_employee }}/5
									</p>
									<p>score</p>
								</div>
							</div>
						</div>
					</div>
					<label class="label has-text-centered mt-6 pt-2 is-size-5">
						Veuillez choisir une de mes disponibilités.
					</label>

					<DatePicker
        				:disabled-dates="disableDates" v-model="dates" mode="date"
        				:min-date="minDate" :max-date="maxDate" is-expanded
        			/>

				</div>
				<div v-if="currentStep == 3">
					<div v-if="$store.state.isAuthenticated">
						<div v-if="$store.state.userInfo.profile_is_completed">
							<div class="has-text-centered" v-if="!clickedSend">
								<h2 class="title mb-5">Veuillez confirmer votre demande</h2>
								<div class="columns is-mobile is-flex-wrap-wrap">
									<div class="column has-text-centered is-6-desktop">
										<label class="label is-size-5">Employé</label>
										<span class="tag has-text-weight-bold is-size-6">
											{{ offerUserInfo.first_name + " " + offerUserInfo.last_name }}
										</span>
									</div>
									<div class="column has-text-centered is-6-desktop">
										<label class="label is-size-5">Taux horaire</label>
										<span class="tag has-text-weight-bold is-size-6">
											${{ offerToShow.hourly_rate }}/h
										</span>
									</div>
									<div class="column has-text-centered is-6-desktop">
										<label class="label is-size-5">Type du service</label>
										<span class="tag has-text-weight-bold is-size-6">
											{{ offerToShow.type_service }}
										</span>
									</div>
									<div class="column has-text-centered is-6-desktop">
										<label class="label is-size-5">Date de réservation</label>
										<span class="tag has-text-weight-bold is-size-6">
											{{ dates.toLocaleDateString("fr-CA") }}
										</span>
									</div>
								</div>
								<label class="checkbox mb-5">
									<input type="checkbox" v-model="confirmationCheckbox" />
									Je confirme avoir validé ma demande
								</label>
							</div>
							<div
								v-if="clickedSend"
								:class="isFetchingOffers ? 'is-loading' : ''"
							>
								<h2 class="title has-text-centered mb-5">
									Demande envoyée avec succès
								</h2>
								<div class="animate__animated animate__zoomInDown">
									<svg
										class="checkmark"
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 52 52"
									>
										<circle
											class="checkmark__circle"
											cx="26"
											cy="26"
											r="25"
											fill="none"
										/>
										<path
											class="checkmark__check"
											fill="none"
											d="M14.1 27.2l7.1 7.2 16.7-16.8"
										/>
									</svg>
								</div>
							</div>
						</div>
						<div
							v-else
							class="icon-text has-text-warning is-justify-content-center subtitle"
						>
							<span class="icon">
								<i class="fas fa-exclamation-triangle"></i>
							</span>
							<span class="has-text-black">Vous devez <a href="#" v-on:click="this.openParentSettingModal()">compléter votre profil</a> avant de pouvoir réserver!</span>
						</div>
					</div>
					<div
						v-else
						class="icon-text has-text-warning is-justify-content-center subtitle"
					>
						<span class="icon">
							<i class="fas fa-exclamation-triangle"></i>
						</span>
						<span class="has-text-black">Vous devez être connecté pour pouvoir réserver!</span>
					</div>
				</div>
			</section>
			<footer class="modal-card-foot is-flex is-justify-content-space-evenly">
				<button
					class="button is-primary is-rounded w-200"
					v-if="currentStep > 1 && !step3Completed"
					@click="currentStep--"
				>
					<span class="icon">
						<i class="fa fa-arrow-left mr-2"></i>
						Retour
					</span>
				</button>
				<button
					class="button is-primary is-rounded w-200"
					v-if="currentStep < 3 && !step3Completed"
					:disabled="currentStep == 2 && this.dates == null"
					:title="currentStep == 2 && this.dates == null
							? 'Vous devez choisir une journée' : ''"
					@click="
						currentStep == 2 ? (step2Completed = true) : '';
						currentStep++;
					"
				>
					<span class="icon">
						Suivant
						<i class="fa fa-arrow-right ml-2"></i>
					</span>
				</button>
				<button
					class="button is-primary is-rounded w-200"
					v-if="currentStep == 3 && !step3Completed"
					:disabled="
						currentStep == 3 && (!confirmationCheckbox || !$store.state.isAuthenticated || !$store.state.userInfo.profile_is_completed)"
					:title="
						currentStep == 3 &&
						!confirmationCheckbox &&
						$store.state.isAuthenticated &&
						$store.state.userInfo.profile_is_completed
							? 'Vous devez confirmer votre demande'
							: ''
					"
					@click="reserveOffer(offerToShow)"
				>
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
	components: {
		DetailedOffer,
	},
	emits: ['controlModalFromChild'],
	data() {
		return {
			// Offer modal
			currentStep: 1,
			step2Completed: false,
			step3Completed: false,
			heroCollapsed: false,
			offerToShow: Object,
			offerUserInfo: Object,
			offerModalActive: false,
			confirmationCheckbox: false,
			clickedSend: false,

			offerToReserve: {
				reservation_date: null,
				id_active_offer: null,
				id_recruiter: null,
				id_offer: null,
				id_user: null,
			},

			query_typeservice: "Tout",
			query_serviceday: new Date(),
			query_mots_cles: "",
			offers: [],
			serviceTypes: [],
			isFetchingOffers: false,
			isFetchingOffersOnScroll: false,
			totalOffers: 0,

			offset: 0,
			saveParams: null,

			select_serviceday: "",
			dateToday: "",
			weekdays: {
				0: "monday",
				1: "tuesday",
				2: "wednesday",
				3: "thursday",
				4: "friday",
				5: "saturday",
				6: "sunday",
			},

			// masks: [],
			disableDates: [],
			dates: null,
			minDate: null,
			maxDate: null,
		};
	},
	mounted() {
		document.title = "Accueil | Communoservice";
		// this.getAllOffers();
		this.getAllOffersWithOffset();
		this.getTotalOffers();

		this.updateCalendarToday();
		StepsWizard.attach(this.$refs.stepsSection.el);
		this.getServiceTypes();
		/*Un "observer" qui surveille tout
		changement dans le state concernant le userInfo.*/
		this.$store.watch(
      (state)=>{
        return this.$store.getters.getUserInfo;
      },
	  /**
	   * Lorsque la valeur du userInfo change, on récupère
	   * à nouveau les offres actives.
	   */
      (val)=>{
	//    this.getAllOffers();
		this.getAllOffersWithOffset();
      },
      {
		  //À spécifier si on observe les propriétés "nested" d'un objet.
        deep:true
      }
      );
	},
	watch: {
    	dates(val) {
      	if (val) {
        	// console.log(val);
        	this.dates = val;
      	}
    	},
  	},
	methods: {
		// async getAllOffers() {
		// 	this.isFetchingOffers = true;
		// 	await axios
		// 		.get("/api/v1/active-offers/")
		// 		.then((response) => {
		// 			this.offers = response.data;
		// 		})
		// 		.catch((error) => {
		// 			console.log(error);
		// 		});
		// 	this.isFetchingOffers = false;
		// },
		async getServiceTypes() {
			await axios
				.get("/api/v1/service-types/")
				.then((res) => {
					this.serviceTypes = res.data;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async reserveOffer(offer) {
			this.isFetchingOffers = true;

			this.offerToReserve.id_offer = offer.id;
			this.offerToReserve.id_user = offer.user;
			this.offerToReserve.hourly_rate = offer.hourly_rate;
			this.offerToReserve.reservation_date = this.dates.toLocaleDateString("fr-CA");
			// this.offerToReserve.reservation_date = this.dates.toISOString().split('T')[0];

			await this.getActiveOfferId(offer);
			await this.getRecruiterId();

			await axios
				.post("/api/v1/reserved-offers/", this.offerToReserve)
				.then((res) => {
					// console.log(res);
					// console.log(this.offerToReserve);

					this.isFetchingOffers = false;
					this.clickedSend = true;
					this.step3Completed = true;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getRecruiterId() {
			return axios
				.get("/api/v1/userinfo/me/")
				.then((res) => {
					this.offerToReserve.id_recruiter = res.data.user_id;

					// console.log(this.offerToReserve);
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getActiveOfferId(offer) {
			return axios
				.get(`/api/v1/active-offers/${offer.id}/${offer.user}/`)
				.then((res) => {
					this.offerToReserve.id_active_offer = res.data.id;

					// console.log(this.offerToReserve); 
					// console.log(res.data); 
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async sendQuery() {
			const params = new URLSearchParams();

			params.append("type-service", this.query_typeservice);

			this.query_serviceday = new Date(this.select_serviceday);
			if (
				this.query_serviceday instanceof Date &&
				!isNaN(this.query_serviceday)
			) {
				params.append(
					"date",
					this.query_serviceday.toISOString().split("T")[0]
				);
				params.append(
					"day-of-week",
					this.weekdays[this.query_serviceday.getDay()]
				);
			}

			let array_mots_cles = [];
			array_mots_cles = this.query_mots_cles.split(" ");
			if (array_mots_cles.length == 1 && array_mots_cles[0] == "") {
				array_mots_cles = [];
			}

			if (array_mots_cles.length > 0) {
				this.query_mots_cles.trim();
				params.append("mots-cles", array_mots_cles);
			}

			if (Array.from(params).length > 0) {
				// this.isFetchingOffers = true;
				// this.isFetchingOffersOnScroll = true;

				// params.append("offset", this.offset);
				this.saveParams = params.toString();

				this.offers = [];
				this.offset = 0;
				var scrollSurface = document.getElementById('list-services');
				if (scrollSurface)
					scrollSurface.scrollTop = 0;

				this.getSearchingOffersWithOffset();

				// await axios
				// 	.get("/api/v1/active-offers/search?" + params.toString())
				// 	.then((response) => {
				// 		this.offers = response.data;
				// 	})
				// 	.catch((error) => {
				// 		console.log(error);
				// 	});
				// this.isFetchingOffers = false;
				// this.isFetchingOffersOnScroll = false;
			}
		},
		async getOfferUserInfo(user_id) {
			await axios
				.get(`api/v1/userinfo/${user_id}/`)
				.then((response) => {
					this.offerUserInfo = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		updateCalendarToday() {
			var current = new Date();
			this.query_serviceday = this.dateToday = `${current.getFullYear()}-${current.getMonth() +
				1}-${current.getDate()}`;
		},
		showOfferModal(offer) {
			this.offerToShow = offer;
			this.offerModalActive = true;
			if (this.offerUserInfo.user != offer.user) {
				this.getOfferUserInfo(offer.user);
			}
			this.getReservedDates(offer);
		},
		closeOfferModal() {
			this.resetOfferModal();
		},
		resetOfferModal() {
			this.offerModalActive = false;
			this.currentStep = 1;
			(this.step2Completed = false),
				(this.step3Completed = false),
				(this.offerToShow = {});
			this.offerUserInfo = {};
			this.confirmationCheckbox = false;
			this.clickedSend = false;
			this.dates = null;
			// Object.keys(this.selectedWeekdays).forEach(
			// 	(value) => (this.selectedWeekdays[value] = false)
			// );
		},
		async getReservedDates(offer) {
			await axios
				.get(`/api/v1/reserved-offers/${offer.id}/`)
				.then((res) => {
					this.disableDates = [];
					for (let i = 0; i < res.data.length; i++) {
						let dayToDisable = {
							start: this.convertDaysForCalendar(res.data[i].reservation_date),
							end: this.convertDaysForCalendar(res.data[i].reservation_date)
						};

						this.disableDates.push(dayToDisable);
					}

					let daysOfWeek = [];
					this.daysOfWeekToDisable(daysOfWeek, offer);
					this.disableDates.push({weekdays: daysOfWeek});

					this.minDate = this.convertDaysForCalendar(offer.start_date);
					this.maxDate = this.convertDaysForCalendar(offer.end_date);

					// ! Note: À revoir
					if (!this.minDate) {
						var tomorrow = new Date();
						var dd = String(tomorrow.getDate() + 1).padStart(2, "0");
						var mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); //January is 0.
						var yyyy = tomorrow.getFullYear();

						tomorrow = yyyy + "-" + mm + "-" + dd;
						this.minDate = this.convertDaysForCalendar(tomorrow);
					}
				})
				.catch((err) => {
					console.log(err);
				});
		},
		convertDaysForCalendar(day) {
			if (day) {
				let dayTmp = day.toString().split('-');
				return new Date(dayTmp[0], dayTmp[1] - 1, dayTmp[2]);
			}
		},
		daysOfWeekToDisable(weekdays, offer) {
			if (!offer.sunday)
				weekdays.push(1);
			if (!offer.monday)
				weekdays.push(2);
			if (!offer.tuesday)
				weekdays.push(3);
			if (!offer.wednesday)
				weekdays.push(4);
			if (!offer.thursday)
				weekdays.push(5);
			if (!offer.friday)
				weekdays.push(6);
			if (!offer.saturday)
				weekdays.push(7);
		},
		replaceByDefault(e) {
			console.clear();

			e.target.src = this.MEDIA_URL + 'pfp_default.jpg';
		},
		scrollAction(e) {
			let elem = e.target;

			if(Math.round(elem.scrollTop + elem.clientHeight) >= elem.scrollHeight && elem.scrollHeight > 0 && !this.isFetchingOffersOnScroll) {
				if (this.saveParams === null)
					this.getAllOffersWithOffset();
				else
					this.getSearchingOffersWithOffset();

				this.getTotalOffers();
			}
		},
		async getAllOffersWithOffset() {
			this.isFetchingOffersOnScroll = true;

			if (this.offset <= this.totalOffers || !this.totalOffers) {
				await axios
					.get('/api/v1/active-offers/', {
						params: {
								offset: this.offset
							}
						})
					.then((res) => {
						this.offers = this.offers.concat(res.data);
						//Filtre pour retirer les offres expirées
						function keepEndDateAfterToday(offer) {
							let today = new Date();
							let offerEndDate = new Date(offer.end_date);
							return !offer.end_date || (offerEndDate > today);
						}
						this.offers = this.offers.filter(keepEndDateAfterToday);
						this.offset = this.offset + 5;
					})
					.catch((error) => {
						console.log(error);
					});
			}
			this.isFetchingOffersOnScroll = false;
		},
		async getSearchingOffersWithOffset() {
			this.isFetchingOffersOnScroll = true;

			if (this.offset < this.totalOffers || !this.totalOffers) {
				let params = new URLSearchParams(this.saveParams);
				params.append("offset", this.offset);

				await axios
					.get("/api/v1/active-offers/search?" + params.toString())
					.then((res) => {
						this.offers = this.offers.concat(res.data);

						this.offset = this.offset + 5;
					})
					.catch((error) => {
						console.log(error);
					});
			}
			this.isFetchingOffersOnScroll = false;
		},
		async getTotalOffers() {
			await axios
				.get('/api/v1/total-active-offers/', {
					params: {
							page: "home"
						}
					})
				.then((res) => {
					// console.log(res.data);
					this.totalOffers = res.data;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		resetSearchParams() {
			var scrollSurface = document.getElementById('list-services');
			if (scrollSurface)
					scrollSurface.scrollTop = 0;

			this.saveParams = null;
			this.offers = [];
			this.offset = 0;
			this.query_mots_cles = "";
			this.query_typeservice = "Tout";
			this.select_serviceday = "";

			this.getAllOffersWithOffset();
		},
		openParentSettingModal(){
			this.$emit('controlModalFromChild', true);
		},
	},
};
</script>

<style lang="scss" scoped>
	@import "../../node_modules/bulma-steps";

	.offers-container {
		max-height: 500px;
		overflow: hidden;
		overflow-y: scroll;
		// Pour Firefox
		scrollbar-width: thin;
		scrollbar-color: #aaaaaa rgba(0, 0, 0, 0);

		&::-webkit-scrollbar {
			width: 14px;
		}

		&::-webkit-scrollbar-thumb {
			border: 4px solid rgba(0, 0, 0, 0);
			background-clip: padding-box;
			border-radius: 9999px;
			background-color: #aaaaaa;
		}
	}

	.ch-5 {
		width: 5ch;
	}

	.checkmark__circle {
		stroke-dasharray: 166;
		stroke-dashoffset: 166;
		stroke-width: 4;
		stroke-miterlimit: 10;
		stroke: #26ad80;
		fill: none;
		animation: stroke 0.75s cubic-bezier(0.65, 0, 0.45, 1) forwards;
	}

	.checkmark {
		width: 100px;
		height: 100px;
		border-radius: 50%;
		display: block;
		stroke-width: 2;
		stroke: #26ad80;
		stroke-miterlimit: 10;
		margin: 0 auto 30px;
		box-shadow: inset 0px 0px 0px #26ad80;
		animation: fill 0.5s ease-in-out 0.5s forwards,
			scale 0.5s ease-in-out 0.9s both;
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
		0%,
		100% {
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

	.step-item {
		flex-basis: 0 !important;
	}
	.loader-wrapper {
		height: 94%;
    	width: 95%;
		opacity: 0;
		z-index: -1;
		transition: opacity 1s;
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 16px;
		position: absolute;
		background-color: rgba(255, 255, 255, 0.4);
			.loader {
				height: 80px;
				width: 80px;
				border: 4px solid darken($color: #dee2e5, $amount: 30);
				border-right-color: transparent;
				border-top-color: transparent;
			}
		&.is-active {
			opacity: 1;
			z-index: 1;
		}
	}
	.offers-box{
		min-height: 540px;
	}
	/**
	Style uniquement appliqué sur le bouton des paramètres.
	*/
	.button-service:hover{
		background-color: darken(#3488ce, 5%);
	}

	.hero{
		height: 100vh;
		overflow: hidden;
	}
	
	.collapse{
		height: 0px;
		transition: height 1s ease-in-out;
	}
</style>
