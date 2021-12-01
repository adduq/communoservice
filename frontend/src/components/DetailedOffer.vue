<template>
		<div class="card mb-3 h-140">
			<div class="card-content is-pointer-cursor" 
				:class="accountPage ? 'pb-0 mb-4' : ''"
				@click="$emit('click', this.offer)">
				<div class="media">
					<div class="media-left">
						<figure class="image is-64x64">
							<img class="is-rounded" :src="imgPath" />
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
	data() {
		return {
			deleteConfirmationModal: false,
			imgPath: this.MEDIA_URL + "pfp_default.jpg",
		}
	},
	mounted() {
		this.getImgUrl();
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
		async getImgUrl() {
			await axios
				.get(
					`/api/v1/userinfo/${this.offer.user}/profile-image/`
				)
				.then((res) => {
					this.imgPath = this.MEDIA_URL + res.data.imgName;
				})
				.catch((err) => {
					console.log(err);
				});
		}
	}
};
</script>

<style scoped>
.is-pointer-cursor {
	cursor: pointer;
}
</style>