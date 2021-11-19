<template>
	<div class="page-log-in">
		<div class="columns">
			<div class="column is-4 is-offset-4">
				<h1 class="title">Connexion</h1>

				<form @submit.prevent="submitForm">
					<div class="field">
						<label>Nom d'utilisateur</label>
						<div class="control">
							<input type="text" class="input" v-model="username" />
						</div>
					</div>

					<div class="field">
						<label>Mot de passe</label>
						<div class="control">
							<input type="password" class="input" v-model="password" />
						</div>
					</div>

					<div class="notification is-danger" v-if="errors.length">
						<p v-for="error in errors" v-bind:key="error">{{ error }}</p>
					</div>

					<div class="field">
						<div class="control">
							<button
								class="button is-dark"
								:class="isLoading ? 'is-loading' : ''"
							>
								Connexion
							</button>
						</div>
					</div>

					<hr />

					Ou <router-link to="/inscription">M'inscrire!</router-link>
				</form>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
export default {
	name: "LogIn",
	data() {
		return {
			username: "",
			password: "",
			errors: [],
			isLoading: false,
		};
	},
	mounted() {
		document.title = "Connexion | Communoservice";
	},
	methods: {
		async submitForm() {
			this.isLoading = true;
			axios.defaults.headers.common["Authorization"] = "";
			localStorage.removeItem("token");

			const formData = {
				username: this.username,
				password: this.password,
			};

			await axios
				.post("/api/v1/token/login/", formData)
				.then((response) => {
					const token = response.data.auth_token;
					this.$store.commit("setToken", token);

					// axios.defaults.headers.common["Authorization"] = "Bearer " + token;
					axios.defaults.headers.common["Authorization"] = "Token " + token;
					// console.log(axios.defaults.headers.common["Authorization"]);
					localStorage.setItem("token", token);
					const toPath = this.$route.query.to || "/";
					this.$router.push(toPath);
				})
				.catch((error) => {
					if (error.response) {
						this.errors.splice(0);
						for (const property in error.response.data) {
							var outvar = "";
							switch (property) {
								case "username":
									outvar = "Nom d'utilisateur";
									break;
								case "password":
									outvar = "Mot de passe";
									break;
								default:
									outvar = "Erreur";
							}
							this.errors.push(`${outvar}: ${error.response.data[property]}`);
						}
					} else {
						this.errors.push("Une erreur est survenue");

						console.log(JSON.stringify(error));
					}
				});
			this.isLoading = false;
		},
	},
};
</script>
