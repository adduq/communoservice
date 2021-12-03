<template>
	<div class="card mb-3 h-140" v-if="this.terminatedOffer">
		<div class="card-content">
			<div class="media">
				<div class="media-left">
					<figure class="image is-64x64">
						<img class="is-rounded" :src="imgPath" />
					</figure>
				</div>
				<div class="media-content">
					<p class="title is-4">{{ terminatedOffer.id_offer.type_service }}</p>
					<p class="subtitle is-6">
						{{
							terminatedOffer.id_offer.description.length >= 50
								? terminatedOffer.id_offer.description.substring(0, 50) + "..."
								: terminatedOffer.id_offer.description
						}}
					</p>
				</div>
			</div>

			<div class="is-flex is-flex-wrap-wrap is-justify-content-space-between">
				<div>
					<time
						datetime="2016-1-1"
						v-if="terminatedOffer.status === this.statusDispo.GIVEN"
					>
						Terminé le : {{ terminatedOffer.completed_date }}</time
					>
					<p v-else>L'offre n'a pas été achevée.</p>
					
					<p v-if="this.isRecruiterCard">
						Employé : {{ terminatedOffer.id_user.username }}
					</p>
					<p v-else>
						Recruteur : {{ terminatedOffer.id_recruiter.first_name }}
						{{ terminatedOffer.id_recruiter.last_name }}
						({{ terminatedOffer.id_recruiter.username }})
					</p>

					<p v-if="terminatedOffer.hourly_rate">
						Taux horaire : {{ terminatedOffer.hourly_rate }} $
					</p>
				</div>

				<div class="is-align-self-center">
					<span
						class="icon-text has-text-success"
						v-if="terminatedOffer.status === this.statusDispo.GIVEN"
					>
						<span class="icon">
							<i class="fas fa-check-square"></i>
						</span>
						<span>Complété</span>
					</span>
					<span
						class="icon-text has-text-warning"
						v-else-if="terminatedOffer.status === this.statusDispo.CANCEL"
					>
						<span class="icon">
							<i class="fas fa-exclamation-triangle"></i>
						</span>
						<span>Annulé</span>
					</span>
					<span class="icon-text has-text-danger" v-else>
						<span class="icon">
							<i class="fas fa-ban"></i>
						</span>
						<span>Non complété</span>
					</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";

export default {
	name: "TerminatedOffer",
	props: {
		terminatedOffer: Object,
		isRecruiterCard: false,
	},
	data() {
		return {
			statusDispo: {
				GIVEN: 0,
				NOT_GIVEN: 1,
				CANCEL: 2,
				NO_PRESENCE: 3,
			},
			imgPath: this.MEDIA_URL + "pfp_default.jpg",
		};
	},
	mounted() {
		let user_id = this.$parent.profileSwitch ? this.terminatedOffer.id_user.id : this.terminatedOffer.id_recruiter.id;
		this.getImgUrl(user_id);
	},
	methods: {
		async getImgUrl(user_id) {			
			await axios
				.get(
					`/api/v1/userinfo/${user_id}/profile-image/`
				)
				.then((res) => {
					this.imgPath = this.MEDIA_URL + res.data.imgName
				})
				.catch((err) => {
					console.log(err);
				});
		}
	}
};
</script>
