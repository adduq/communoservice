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
									:src="'/media/pfp_'+userInfo.user_id+'.jpg'" 
									@error="replaceByDefault"
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
			<template v-if="!profileSwitch">
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

							<div class="columns">
								<div class="column is-one-third">
									<div class="field">
									<label class="label">Type de service</label>
									<div class="control">
										<div class="select">
										<select v-model="serviceType" class="w-200">
											<option value="" disabled selected>Choisir parmi</option>
											<option
											v-for="type in serviceTypes"
											v-bind:key="type.name"
											>{{ type.name }}</option
											>
										</select>
										</div>
									</div>
									</div>

									<label class="label">Distance maximale</label>
									<div class="field has-addons">
									<p class="control">
										<input
										v-model="maxDistance"
										class="input"
										type="number"
										min="1"
										placeholder="Distance"
										/>
									</p>
									</div>

									<label class="label">Taux horaire</label>
									<div class="field has-addons">
										<p class="control">
										<input
											v-model="hourlyRate"
											class="input"
											type="number"
											min="0"
											placeholder="Montant"
										/>
										</p>
									</div>
								</div>
								<div class="column">
									<div class="field">
										<label class="label">Description</label>
										<div class="control">
										<textarea
											v-model="description"
											class="textarea"
											placeholder="Votre message ici..."
											rows="4"
										></textarea>
										</div>
									</div>

									<label class="label">Disponibilités</label>
									<div class="control">
									<label class="radio">
										<input type="radio" @click="closeAllDispoChoices()" name="dispo" v-model="isAlwaysDispo"  v-bind:value="true" checked>
										Toujours disponible
									</label>
									<label class="radio">
										<input type="radio" @click="resetDatepicker()" name="dispo" v-model="isAlwaysDispo"  v-bind:value="false">
										Préciser mes disponibilités
									</label>
									</div>
								</div>
							</div>

						<div :class="[isAlwaysDispo ? 'hidden' : 'field']">
							<div>
							<label class="label">
							Récurrence
						</label>
							<div class="field mb-2 mr-6"></div>
							<div
								class="is-flex has-text-centered is-flex-wrap-wrap mt-2 is-justify-content-space-evenly is-family-monospace"
							>
								<button
								id="2"
								class="button is-rounded day-button"
								:class="daysSelected.monday ? 'is-success' : ''"
								v-on:click="clickOnButton(2, daysSelected.monday)"
								>
								L
								</button>

								<button
								id="3"
								class="button is-rounded day-button"
								:class="daysSelected.tuesday ? 'is-success' : ''"
								v-on:click="clickOnButton(3, daysSelected.tuesday)"
								>
								M
								</button>

								<button
								id="4"
								class="button is-rounded day-button"
								:class="daysSelected.wednesday ? 'is-success' : ''"
								v-on:click="clickOnButton(4, daysSelected.wednesday)"
								>
								M
								</button>

								<button
								id="5"
								class="button is-rounded day-button"
								:class="daysSelected.thursday ? 'is-success' : ''"
								v-on:click="clickOnButton(5, daysSelected.thursday)"
								>
								J
								</button>

								<button
								id="6"
								class="button is-rounded day-button"
								:class="daysSelected.friday ? 'is-success' : ''"
								v-on:click="clickOnButton(6), daysSelected.friday"
								>
								V
								</button>

								<button
								id="7"
								class="button is-rounded day-button"
								:class="daysSelected.saturday ? 'is-success' : ''"
								v-on:click="clickOnButton(7, daysSelected.saturday)"
								>
								S
								</button>
								<button
								id="1"
								class="button is-rounded day-button"
								:class="daysSelected.sunday ? 'is-success' : ''"
								v-on:click="clickOnButton(1, daysSelected.sunday)"
								>
								D
								</button>
							</div>
							</div>
						<!---->
						<label @click="resetDatepicker()" class="checkbox mb-4">
							<input type="checkbox" v-model="isDatePickerPresent" />
							Préciser une date ou une sélection de jours
						</label>
						<div
							:class="[isDatePickerPresent ? '' : 'hidden']"
							id="datepicker"
						>
							<label class="label">Sélectionner un ou plusieurs jours
								<span class="icon is-info tooltip">
									<i class="fas fa-info-circle"></i>
									<span class="tooltiptext has-background-primary">
										Cliquez une fois pour choisir la date de début<br/>
										Cliquez une deuxième fois pour choisir la date de fin
									</span>
								</span>
							</label>
							
							<DatePicker
							v-model="range"
							mode="date"
							:masks="masks"
							is-range
							:min-date="minDate"
							:attributes="attributes"
							:drag-attribute="dragAttribute"
							:select-attribute="selectAttribute"
							:key="componentKey"
							is-expanded
							locale="fr"
							/>
						</div>
						<div
							class="notification is-danger p-2"
							v-if="datePickerError.length > 0"
						>
							<p v-for="error in datePickerError" v-bind:key="error">
							{{ error }}
							</p>
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
			<template v-if="profileSwitch">
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
								v-bind:isRecruiterCard="true"
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
								v-bind:isRecruiterCard="true"
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

export default {
	name: "MyAccount",
	//Les components qu'on veut utiliser
	components: {
		DetailedOffer,
		TerminatedOffer,
		ReservedOffer,
	},
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
			hourlyRate: "",
			maxDistance: "",
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

			/***Datepicker Début**/
			isAlwaysDispo:true,
			isShownDispoSection:false,
			isDatePickerPresent: false,
			startDate: "",
			endDate: "",
			minDate: new Date(),
			componentKey: 0,
			username: "",
			password: "",
			errors: [],
			dragAttribute: {
				highlight: {
				color: "green",
				fillMode: "light",
				},
			},
			selectAttribute: {
				highlight: {
				color: "green",
				fillMode: "light",
				},
				dates: this.range,
				order: 0,
			},
			attributes: [],
			range: null,
			masks: {
				title: "MMMM YYYY",
				weekdays: "W",
				navMonths: "MMM",
				input: ["L", "YYYY-MM-DD", "YYYY/MM/DD"],
				dayPopover: "WWW, MMM D, YYYY",
				data: ["YYYY-MM-DD"],
			},
			datePickerError: [],
			/***Datepicker Fin**/
		};
	},
	watch: {
    range(val) {
      if (val) {
        //console.log("watch reset pattern");
        this.resetPattern();
        this.resetDaysButtons();
        this.datePickerError = [];
      }
    },
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

			
			if (!this.isAlwaysDispo){
				if (!this.isDatePickerPresent){
					//Utilisateur veut préciser récurrence seulement.
					if (!this.validateAtLeastOneDisponibilityInWeek()){
						this.errors.push(
						"Indiquez une récurrence."
						);
					}
				}
				else{
					//Le datepicker est ouvert.
					if (!this.validateAtLeastOneDisponibilityInWeek() && this.range==null){
						this.errors.push(
						"Indiquez une récurrence ou une journée de disponibilité."
						);
					}
				}
			}

			console.log("passe validation");

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


			if (this.isAlwaysDispo){
				this.toggleAllDayButtonsToTrue();
			}
			else{
				if (this.isDatePickerPresent){
					if (!this.validateAtLeastOneDisponibilityInWeek() && this.range !=null){
						this.toggleAllDayThatAreInDatepicker();
					}
				}
			}

			const newOffer = {
				user: this.userInfo.user_id,
				type_service: this.serviceType,
				description: this.description,
				hourly_rate: this.hourlyRate,
				max_distance: this.maxDistance,
				monday: this.daysSelected.monday,
				tuesday: this.daysSelected.tuesday,
				wednesday: this.daysSelected.wednesday,
				thursday: this.daysSelected.thursday,
				friday: this.daysSelected.friday,
				saturday: this.daysSelected.saturday,
				sunday: this.daysSelected.sunday,
			};
			let startDate = this.range == null ? null : this.range.start.toISOString().substr(0, 10);
			let endDate = this.range == null ? null : this.range.end.toISOString().substr(0, 10);
			newOffer.start_date = startDate;
			newOffer.end_date = endDate;


			//alert(JSON.stringify(newOffer)); //pour validation.
			await axios
			.post("/api/v1/offers/", newOffer)
			.then((response) => {
				this.isLoading = false;
				this.modalCreateisActive = false;
				this.creationModalIsActive = false;
				this.resetDatepicker();
				this.resetInputs();
				// this.confirmeCreation = false;
				this.addActiveOffers({
					id_offer: response.data.id,
					id_user: response.data.user,
				});
			})
			.catch((error) => {
				this.modalCreateisActive = false;
				this.creationModalIsActive = true;
				// this.confirmeCreation = false;
				if (error.response.data["error"] == "profile_incomplete") {
					toast({
						message: "Profil incomplet. Veuillez completer votre profil dans les paramètres.",
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
					// this.errors.push(
					// 	"Profil incomplet. Veuillez completer votre profil dans les paramètres."
					// );
				} else {
					// this.errors.push("Une erreur est survenue. Essayez à nouveau.");
					toast({
						message: "Une erreur est survenue. Essayez à nouveau.",
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
				// console.log(error);
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
		/***Méthodes Datepicker Début**/
		datepickerChanged() {
		//console.log("day clicked");
		this.resetPattern();
		},
		confirm() {
		//console.log("Choix : " + JSON.stringify(this.range));
		//console.log("Valeurs du range : " + JSON.stringify(this.range.value));
		//console.log("Pattern choisi : " + JSON.stringify(this.attributes));
		},
		clickOnButton(weekDayIndex, isWeekdaySelected) {
		//console.log("attributes : " + JSON.stringify(this.attributes));

		this.datePickerError = [];
		if (document.getElementById("datepicker").className.includes("hidden")) {
			this.manageButtonWithoutRangeRestriction(
			weekDayIndex,
			isWeekdaySelected
			);
		} else {
			this.manageButtonClickWithRangeRestriction(
			weekDayIndex,
			isWeekdaySelected
			);
		}
		},
		manageButtonClickWithRangeRestriction(weekDayIndex, isWeekdaySelected) {
		//console.log("With range limits");
		let errorMessage =
			"Pour préciser un jour de la semaine, vous devez sélectionner une plage de jours.";
		let errorMessage2 =
			"Ce jour de semaine n'apparaît pas votre sélection du calendrier.";

		//console.log("range is " + JSON.stringify(this.range));

		if (this.range == null) {
			this.datePickerError.push(errorMessage);
			document.getElementById(weekDayIndex.toString()).blur();
			return;
		}
		let debut = this.range.start;
		let fin = this.range.end;
		let span = this.range.end - this.range.start;
		//console.log("span is " + span);
		if (span == 0) {
			this.datePickerError.push(errorMessage);
			return;
		}
		
		var daysArray = this.getDaysArray(debut, fin);
		//console.log("dates de la sélection : " + JSON.stringify(daysArray));
		let indexDayOfRangeSelected = [];
		daysArray.forEach((day) => {
			//console.log(day + " est un " + day.getDay());
			indexDayOfRangeSelected.push(day.getDay());
		});
		//Ajustement de l'indice par rapport à V-Calendar
		let indexToCheck = weekDayIndex - 1;
		if (indexDayOfRangeSelected.includes(indexToCheck)) {
			//console.log("L'index " + weekDayIndex + "est valide");
		} else {
			this.datePickerError.push(errorMessage2);
			document.getElementById(weekDayIndex.toString()).blur();
			return;
		}
		//console.log("Selected index : " + weekDayIndex);
		let notFound = true;
		let i = 0;
		let indexToDelete = -1;
		//console.log("attr : " + JSON.stringify(this.attributes.length));
		while (notFound && i < this.attributes.length) {
			if (this.attributes[i].hasOwnProperty("key")) {
			//console.log("Has property Key!!!");
			if (this.attributes[i].key == weekDayIndex) {
				//console.log("Has the right value : " + this.attributes[i].key);
				indexToDelete = i;
				//console.log("Element to delete in Attributes : " + i);
				notFound = false;
			} else i++;
			}
		}
		//console.log(indexToDelete);
		if (indexToDelete != -1 && this.attributes.length != 0) {
			//console.log("est présent");
			//Est présent
			this.attributes.splice(indexToDelete, 1);
					switch (weekDayIndex) {
			case 2:
				this.daysSelected.monday = !this.daysSelected.monday;
				break;
			case 3:
				this.daysSelected.tuesday = !this.daysSelected.tuesday;
				break;
			case 4:
				this.daysSelected.wednesday = !this.daysSelected.wednesday;
				break;
			case 5:
				this.daysSelected.thursday = !this.daysSelected.thursday;
				break;
			case 6:
				this.daysSelected.friday = !this.daysSelected.friday;
				break;
			case 7:
				this.daysSelected.saturday = !this.daysSelected.saturday;
				break;
			case 1:
				this.daysSelected.sunday = !this.daysSelected.sunday;
				break;
			case 3:
				break;
			default:
			}
		} else {
			//console.log("est pas présent encore");
			switch (weekDayIndex) {
			case 2:
				this.daysSelected.monday = !this.daysSelected.monday;
				break;
			case 3:
				this.daysSelected.tuesday = !this.daysSelected.tuesday;
				break;
			case 4:
				this.daysSelected.wednesday = !this.daysSelected.wednesday;
				break;
			case 5:
				this.daysSelected.thursday = !this.daysSelected.thursday;
				break;
			case 6:
				this.daysSelected.friday = !this.daysSelected.friday;
				break;
			case 7:
				this.daysSelected.saturday = !this.daysSelected.saturday;
				break;
			case 1:
				this.daysSelected.sunday = !this.daysSelected.sunday;
				break;
			case 3:
				break;
			default:
			}
			
			//console.log("a passé le toggle selected day");
			this.attributes.push({
			key: weekDayIndex,
			highlight: {
				color: "green",
				fillMode: "solid",
			},
			dates: {
				start: debut,
				end: fin,
				weekdays: [weekDayIndex],
			},
			order: 1,
			});
		}
		//console.log("Ajout dans le pattern réussi");
		
		this.datePickerError = [];
		},
		manageButtonWithoutRangeRestriction(weekDayIndex, isWeekdaySelected) {
		//console.log("no range restriction");
		this.toggleSelectedDay(weekDayIndex, isWeekdaySelected);
		},
		toEnableDaysButtons() {
		let buttons = document.getElementsByClassName("day-button");
		buttons.forEach((b) => (b.disabled = true));
		},
		toDisableDaysButtons() {
		let buttons = document.getElementsByClassName("day-button");
		buttons.forEach((b) => (b.disabled = false));
		},
		resetDaysButtons() {
		for (const property in this.daysSelected) {
			this.daysSelected[property] = false;
		}
		},
		resetPattern() {
		//console.log(JSON.stringify(this.range));
		//console.log("Suppression du pattern.");
		while (this.attributes.length > 0) {
			//console.log("Remove one attribute.");
			this.attributes.pop();
		} //note: ne pas remplacer par this.attributes=[] -->ne marche pas.
		},
		resetDatepicker() {
		this.range = null;
		this.resetPattern();
		this.resetDaysButtons();
		this.datePickerError = [];
		},
		resetRange() {
		if (this.resetNextDayClick) {
			this.resetNextDayClick = false;
			this.$nextTick(() => (this.range = null));
		}
		},
		toggleSelectedDay(weekDayIndex, isWeekdaySelected) {
		//console.log("dans fonction toggle");
		//console.log("weekdayindex vaut : " + weekDayIndex);
		//console.log("isWeekdaySelected vaut : " + isWeekdaySelected);
		switch (weekDayIndex) {
			case 2:
			this.daysSelected.monday = !this.daysSelected.monday;
			break;
			case 3:
			this.daysSelected.tuesday = !this.daysSelected.tuesday;
			break;
			case 4:
			this.daysSelected.wednesday = !this.daysSelected.wednesday;
			break;
			case 5:
			this.daysSelected.thursday = !this.daysSelected.thursday;
			break;
			case 6:
			this.daysSelected.friday = !this.daysSelected.friday;
			break;
			case 7:
			this.daysSelected.saturday = !this.daysSelected.saturday;
			break;
			case 1:
			this.daysSelected.sunday = !this.daysSelected.sunday;
			break;
			case 3:
			break;
			default:
		}
		isWeekdaySelected = !isWeekdaySelected;
		},
		getDaysArray(start, end) {
		for (
			var arr = [], dt = new Date(start);
			dt <= end;
			dt.setDate(dt.getDate() + 1)
		) {
			arr.push(new Date(dt));
		}
		return arr;
		},
		validateDateIsADayOfWeek(day, indexToCheck) {
		//console.log("entré dan fct." + indexToCheck);
		//Corriger décalage de VCalendar, dont les indices
		//commencent à 1 à partir du dimanche.
			indexToCheck = indexToCheck - 1;
			if (indexToCheck !== day.getDay()) {
				return false;
			}
		},
		resetInputs(){
			this.description = "";
			this.hourlyRate = "";
			this.serviceType = "";
		},
		validateAtLeastOneDisponibilityInWeek(){
		let minimumRecurrence = 1
		let countofTrue=0;
		
		this.daysSelected.monday ? countofTrue++: countofTrue;
		this.daysSelected.tuesday ? countofTrue++: countofTrue;
		this.daysSelected.wednesday ? countofTrue++: countofTrue;
		this.daysSelected.thursday ? countofTrue++: countofTrue;
		this.daysSelected.friday ? countofTrue++: countofTrue;
		this.daysSelected.saturday ? countofTrue++: countofTrue;
		this.daysSelected.sunday ? countofTrue++: countofTrue;

		return countofTrue>=minimumRecurrence;
	},
	closeAllDispoChoices(){
		this.resetDatepicker();
		this.toggleAllDayButtonsToTrue();
	},
	toggleAllDayButtonsToTrue(){
		this.daysSelected.monday=true;
		this.daysSelected.tuesday=true;
		this.daysSelected.wednesday=true;
		this.daysSelected.thursday=true;
		this.daysSelected.friday =true;
		this.daysSelected.saturday =true;
		this.daysSelected.sunday=true;
	},
	toggleAllDayThatAreInDatepicker(){
		var daysArray = this.getDaysArray(this.range.start, this.range.end);
      let indexDayOfRangeSelected = [];
      daysArray.forEach((day) => {
        console.log(day + " est un " + day.getDay());
		switch (day.getDay()) {
        case 1:
          this.daysSelected.monday = true;
          break;
        case 2:
          this.daysSelected.tuesday = true;
          break;
        case 3:
          this.daysSelected.wednesday = true;
          break;
        case 4:
          this.daysSelected.thursday = true;
          break;
        case 5:
          this.daysSelected.friday = true;
          break;
        case 6:
          this.daysSelected.saturday = true;
          break;
        case 0:
          this.daysSelected.sunday = true;
          break;
        default:
			break;
      }
    //     indexDayOfRangeSelected.push(day.getDay());
	// 	indexDayOfRangeSelected.foreach((index)=>{
	// 	  console.log("entre");
	// 	  //0=dimanche, 1=lundi,etc.
		   
	//   });
      });

	  
	},
	replaceByDefault(e){
		e.target.src = "/media/pfp_default.jpg"
	}
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
.hidden {
  	display: none;
}
.tooltip {
	position: relative;
	float: right;
}

.tooltip .tooltiptext {
	visibility: hidden;
	width: 200px;
	color: #fff;
	text-align: center;
	border-radius: 6px;
	padding: 5px 0;
	position: absolute;
	z-index: 10;
	top: 100%;
	right: 0;
	margin-left: -200px;
}

.tooltip:hover .tooltiptext {
  	visibility: visible;
}
</style>
