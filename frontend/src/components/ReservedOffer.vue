<template>
	<div class="card mb-3 h-140">
		<div class="card-content">
			<div class="media">
				<div class="media-left">
					<figure class="image is-64x64">
						<img
							class="is-rounded"
							:src="this.MEDIA_URL + 'pfp_' + imgId + '.jpg'" 
							@error="replaceByDefault"
						/>
					</figure>
				</div>
				<div class="media-content">
					<p class="title is-4">
						{{ reservedOffer.id_offer.type_service }}
					</p>
					<p
						class="subtitle is-6"
						v-if="this.reservedOffer.id_offer.description"
					>
						{{
							reservedOffer.id_offer.description.length >= 50
								? reservedOffer.id_offer.description.substring(0, 50) + "..."
								: reservedOffer.id_offer.description
						}}
					</p>
				</div>
			</div>

			<time datetime="2016-1-1" v-if="reservedOffer.reservation_date">
				Réservé pour le : {{ reservedOffer.reservation_date }}
			</time>
			<p v-if="this.isRecruiterCard">
				Employé : {{ reservedOffer.id_user.first_name }}
				{{ reservedOffer.id_user.last_name }}
				({{ reservedOffer.id_user.username }})
			</p>
			<p v-else>
				Recruteur : {{ reservedOffer.id_recruiter.first_name }}
				{{ reservedOffer.id_recruiter.last_name }}
				({{ reservedOffer.id_recruiter.username }})
			</p>

			<p v-if="reservedOffer.hourly_rate">
				Taux horaire : {{ reservedOffer.hourly_rate }} $
			</p>

			<div class="is-flex is-flex-wrap-wrap is-justify-content-end mt-4">
				<a class="button is-success complete-button" @click="terminateOfferIsActive = true">
					<span class="icon is-small">
						<i class="fa fa-check"></i>
					</span>
				</a>
			</div>
		</div>
	</div>


	<div class="modal" :class="terminateOfferIsActive ? 'is-active' : ''">
		<div class="modal-background" @click="terminateOfferIsActive = !terminateOfferIsActive">
		</div>
			<div class="modal-card">
				<header class="modal-card-head">
					<p class="modal-card-title">Terminer le service</p>
						<button
							class="delete has-background-danger"
							@click="terminateOfferIsActive = !terminateOfferIsActive"
							aria-label="close"
						></button>
				</header>

            	<section class="modal-card-body">
					<div class="field">
						<label class="label">Status du service</label>
						<div class="control">
							<div class="select">
								<select v-model="statusAttribue" class="w-200">
									<option v-for="type in statusService"
									v-bind:key="type.dispo" :value="type.dispo">
										{{ type.name }}
									</option>
								</select>
							</div>
						</div>
					</div>

					<div class="field">
						<label class="label">Mettre une note</label>
						<div class="control">
							<div class="rating has-text-centered">
								<star-rating :increment="0.5" :rating="noteService"
									:border-width="1" :max-rating="5" @update:rating ="setRating" :star-points="[23,2, 14,17, 0,19, 10,34, 7,50, 23,43, 38,50, 36,34, 46,19, 31,17]"
									:glow="5" glow-color="#ffd055" :star-size="50" :show-rating="false" :clearable="true" class="is-flex is-justify-content-center">									
								</star-rating>
								<span class="affiche-note">{{ noteService }}/5</span>
							</div>
						</div>
					</div>
            	</section>

				<footer class="modal-card-foot is-flex is-justify-content-center">
					<button
						class="button is-success w-200"
						@click="terminateOffer"
					>
						Terminer
					</button>
					<button
						class="button is-danger w-200"
						@click="terminateOfferIsActive = !terminateOfferIsActive"
					>
						Fermer
					</button>
				</footer>
			</div>
	</div>
</template>

<script>
import axios from "axios";
import StarRating from 'vue-star-rating';

export default {
	name: "ReservedOffer",
	props: {
		reservedOffer: null,
		isRecruiterCard: false,
	},
	components: {
		StarRating
	},
	data() {
		return {
			statusDispo: {
				GIVEN: 0,
				NOT_GIVEN: 1,
				CANCEL: 2,
				NO_PRESENCE: 3,
			},
			statusService: [
				{name: "Rendu", dispo: 0},
				{name: "Pas rendu", dispo: 1},
				{name: "Annulé", dispo: 2},
				{name: "Ne s'est pas présenté", dispo: 3},
			],
			statusAttribue: 0,
			noteService: 0,
			terminateOfferIsActive: false,
			imgId: "default",
		};
	},
	mounted() {
		this.imgId = this.$parent.profileSwitch ? this.reservedOffer.id_user.id : this.reservedOffer.id_recruiter.id;
	},
	methods: {
		setRating(note) {
			this.noteService = note;
		},
		async terminateOffer() {			
			if (parseInt(this.noteService) === 0)
				this.noteService = null;

			this.reservedOffer["status"] = this.statusAttribue;
			this.reservedOffer["rating"] = this.noteService;

			await this.deleteFromReservedOffer();

			this.terminateOfferIsActive = !this.terminateOfferIsActive
		},
		/**
		 * Permet de supprimer une offre des offres réservées.
		 */
		async deleteFromReservedOffer() {
			this.reservedOffer["completed_date"] = new Date().toLocaleDateString("fr-CA");

			await axios
			.delete(
				`/api/v1/reserved-offers/${this.reservedOffer.id}`,
				this.reservedOffer
			)
			.then((res) => {
				if (this.isRecruiterCard) {
					this.$parent.reservedOffersForRecruiter = this.$parent.reservedOffersForRecruiter
					.filter(el => el.id !== this.reservedOffer.id );
				} else {
					this.$parent.reservedOffersForUser = this.$parent.reservedOffersForUser
					.filter(el => el.id !== this.reservedOffer.id );
				}

				this.addToTerminatedOffer();
			})
			.catch((err) => {
				console.log(err);
			});
		},
		/**
		 * Permet d'ajouter une offre aux offres terminées.
		 */
		async addToTerminatedOffer() {
			this.reservedOffer["id_offer"] = this.reservedOffer.id_offer.id;
			this.reservedOffer["id_active_offer"] = this.reservedOffer.id_active_offer.id;
			this.reservedOffer["id_user"] = this.reservedOffer.id_user.id;
			this.reservedOffer["id_recruiter"] = this.reservedOffer.id_recruiter.id;
			this.reservedOffer["hourly_rate"] = this.reservedOffer.hourly_rate;

			await axios
				.post("/api/v1/terminated-offers/", this.reservedOffer)
				.then((res) => {
					if (this.isRecruiterCard) {
						this.$parent.totalReservedOfferRecruiter = this.$parent.totalReservedOfferRecruiter - 1;
						this.$parent.totalTerminatedOfferRecruiter = this.$parent.totalTerminatedOfferRecruiter + 1;

						this.$parent.getTerminatedOffersForRecruiterWithOffset(
							this.reservedOffer["id_recruiter"]
						);

						this.refreshEmployeeInfos(this.reservedOffer["id_user"], this.reservedOffer["id_recruiter"]);
					} else {
						this.$parent.totalReservedOfferUser = this.$parent.totalReservedOfferUser - 1;
						this.$parent.totalTerminatedOfferUser = this.$parent.totalTerminatedOfferUser + 1;

						this.$parent.getTerminatedOffersForUserWithOffset(
							this.reservedOffer["id_user"]
						);

						this.refreshRecruiterInfos(this.reservedOffer["id_recruiter"], this.reservedOffer["id_user"]);
					}					
				})
				.catch((err) => {
					console.log(err);
				});
		},
		/**
		 * Permet d'actualiser les informations de l'employé.
		 */
		async refreshEmployeeInfos(user_id, recruiter_id) {
			await axios
				.put(
					`/api/v1/userinfo/${user_id}/update-employee/${recruiter_id}/`,
					this.reservedOffer
				)
				.then((res) => {})
				.catch((err) => {
					console.log(err);
				});
		},
		/**
		 * Permet d'actualiser les informations de l'employeur.
		 */
		async refreshRecruiterInfos(recruiter_id, user_id) {
			await axios
				.put(
					`/api/v1/userinfo/${recruiter_id}/update-recruiter/${user_id}/`,
					this.reservedOffer
				)
				.then((res) => {})
				.catch((err) => {
					console.log(err);
				});
		},
		replaceByDefault(e) {
			console.clear();
			e.target.src = this.MEDIA_URL + 'pfp_default.jpg';
		},
	},
};
</script>

<style>
.affiche-note {
	font-size: 3rem;
}
.complete-button{
	position: absolute;
    right: 10px;
    top: 10px;
}
</style>
