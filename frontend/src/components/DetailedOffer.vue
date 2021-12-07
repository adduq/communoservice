<template>
	<a href="#search">
		<div class="card mb-3 h-140"
		:class="mustHaveChangeDateIcon ? 'has-background-danger-light': ''">
			<div class="card-content is-pointer-cursor" 
				:class="accountPage ? 'pb-0 mb-4' : ''"
				@click="$emit('click', this.offer)">
				<div class="media">
					<div class="media-left">
						<figure class="image is-64x64">
							<!-- <img class="is-rounded" :src="imgPath" /> -->
							<img
								class="is-rounded"
								:src="this.MEDIA_URL + 'pfp_' + offer.user + '.jpg'" 
								@error="replaceByDefault"
							/>
						</figure>
					</div>
					<div class="media-content is-clipped">
						<p class="title is-4">{{ offer.type_service }}</p>
						<p class="subtitle is-6">
							{{
								offer.description.length >= 50
									? offer.description.substring(0, 50) + "..."
									: offer.description
							}}
						</p>
					</div>
				</div>


				<div class="has-text-danger" v-if="offer.end_date != null">
					<time datetime="{{offer.end_date}}">
						Valide jusqu'au {{ offer.end_date }}
					<span v-if="mustHaveChangeDateIcon" class="icon is-info tooltip is-pulled-rigth">
						<i class="fas fa-exclamation-circle has-text-danger"></i>
						<span class="tooltiptext has-background-danger">
							L'offre n'est plus visible par les autres utilisateurs. Modifiez la date d'expiration pour rendre l'offre disponible.
						</span>
					</span>
					</time>
				</div>
				<div class="is-family-monospace is-flex is-justify-content-flex-end mt-3"
					:class="accountPage ? '' : 'is-size-4-desktop'">
					<span
						class="tag is-rounded"
						:class="offer.monday ? 'is-info' : 'is-dark'"
					>
						L
					</span>
					<span
						class="tag is-rounded"
						:class="offer.tuesday ? 'is-info' : 'is-dark'"
					>
						M
					</span>
					<span
						class="tag is-rounded"
						:class="offer.wednesday ? 'is-info' : 'is-dark'"
					>
						M
					</span>
					<span
						class="tag is-rounded"
						:class="offer.thursday ? 'is-info' : 'is-dark'"
					>
						J
					</span>
					<span
						class="tag is-rounded"
						:class="offer.friday ? 'is-info' : 'is-dark'"
					>
						V
					</span>
					<span
						class="tag is-rounded"
						:class="offer.saturday ? 'is-info' : 'is-dark'"
					>
						S
					</span>
					<span
						class="tag is-rounded"
						:class="offer.sunday ? 'is-info' : 'is-dark'"
					>
						D
					</span>
				</div>
			</div>

			<div v-if="accountPage" class="is-flex is-justify-content-center mb-4">
				<button class="button is-danger w-200" @click="deleteConfirmationModal = true">
					Supprimer
				</button>
			</div>
		</div>

		<div v-if="accountPage" class="modal" :class="{ 'is-active': deleteConfirmationModal }">
			<div
				class="modal-background"
				@click="deleteConfirmationModal = !deleteConfirmationModal"
			></div>
			<div class="modal-card">
				<header class="modal-card-head">
					<p class="modal-card-title">Confirmation</p>
					<button
						class="delete has-background-danger"
						@click="deleteConfirmationModal = !deleteConfirmationModal"
						aria-label="close"
					></button>
				</header>
				<section class="modal-card-body">
					Êtes-vous certain de vouloir supprimer ce service?
				</section>
				<footer class="modal-card-foot">
					<button
						class="button is-danger w-100"
						@click="deleteConfirmationModal = !deleteConfirmationModal"
					>
						Non
					</button>
					<button
						@click="deleteOffer"
						class="button is-success w-100"
					>
						Oui
					</button>
				</footer>
			</div>
		</div>
	</a>
</template>

<script>
import axios from "axios";

export default {
	name: "DetailedOffer",
	emits: ["click"],
	props: {
		offer: Object,
		accountPage: false,
	},
	watch: {
		offer: {
			handler() {
				this.addChangeEndDate();
			},
        deep: true
		}
	},
	data() {
		return {
			deleteConfirmationModal: false,
			// imgPath: this.MEDIA_URL + "pfp_default.jpg",
			mustHaveChangeDateIcon:false
		}
	},
	mounted() {
		// this.getImgUrl();

		if (this.accountPage)
			this.addChangeEndDate();

		// if ( document.URL.includes("mon-compte") ) {
		// 	this.addChangeEndDate();
		// }
	},
	methods: {
		async deleteOffer() {
			await axios
				.delete(
					`/api/v1/active-offers/${this.offer.id_active_offer}/`
				)
				.then((res) => {
					this.$parent.activeOffers = this.$parent.activeOffers
						.filter(el => el.id !== this.offer.id );

					// this.$parent.getAllOffersWithOffset(this.offer.user);
					this.$parent.getTotalOffers();

					this.$parent.getReservedOffersForUserWithOffset(this.offer.user);

					this.deleteConfirmationModal = !this.deleteConfirmationModal;
					// this.$parent.getAllOffers(this.offer.user);
					// this.$parent.getReservedOffersForUser(this.offer.user);
				})
				.catch((err) => {
					console.log(err);
				});
		},
		// async getImgUrl() {
		// 	await axios
		// 		.get(
		// 			`/api/v1/userinfo/${this.offer.user}/profile-image/`
		// 		)
		// 		.then((res) => {
		// 			this.imgPath = this.MEDIA_URL + res.data.imgName;
		// 		})
		// 		.catch((err) => {
		// 			console.log(err);
		// 		});
		// },
		replaceByDefault(e) {
			// console.clear();

			e.target.src = this.MEDIA_URL + 'pfp_default.jpg';
		},
		addChangeEndDate() {
			let offerEndDate = new Date(this.offer.end_date);
			let today = new Date();

			this.mustHaveChangeDateIcon = this.offer.end_date && (offerEndDate < today);

			// if(offerEndDate < today){
				// 	this.mustHaveChangeDateIcon = true;
			// }
		}
	}
};
</script>

<style scoped>
.is-pointer-cursor {
	cursor: pointer;
}

.tooltip {
	position: relative;

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