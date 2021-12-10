<template>
	<div class="page-log-in">
		<div class="columns form-wrapper mt-6">
			<div class="column is-4 is-offset-4 has-text-centered">
				<h1 class="title">Connexion</h1>

				<form @submit.prevent="submitForm">
					<div class="field has-text-left">
					<p class="control has-icons-left">
						<input class="input" type="text" placeholder="Nom d'utilisateur" 
							:class="this.usernameError ? 'is-danger': ''"
							v-model="this.username" 
							@focus="this.usernameError = false" >
						<span class="icon is-small is-left">
						<i class="fas fa-user"></i>
						</span>
					</p>
					</div>
					<div class="field has-text-left">
					<p class="control has-icons-left">
						<input class="input" type="password" placeholder="Mot de passe" 
							:class="this.passwordError ? 'is-danger': ''" 
							v-model="this.password" 
							@focus="this.passwordError = false">
						<span class="icon is-small is-left">
						<i class="fas fa-lock"></i>
						</span>
					</p>
					</div>
					<div class="notification is-danger" v-if="this.errors.length">
						<p v-for="error in this.errors" v-bind:key="error">{{ error }}</p>
					</div>

					<div class="field">
						<div class="control">
							<button
								class="button is-primary login-button"
								:class="this.isLoading ? 'is-loading' : ''"
							>
								Connexion
							</button>
						</div>
					</div>

					<hr />

					Ou <router-link to="/inscription">m'inscrire!</router-link>
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
			usernameError: false,
			password: "",
			passwordError: false,
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

			const formData = {
				username: this.username,
				password: this.password,
			};
			if(this.validateFormData(formData)){
				await axios
					.post("/api/v1/token/login/", formData)
					.then((response) => {
						const token = response.data.auth_token;
						this.$store.commit("setToken", token);

						axios.defaults.headers.common["Authorization"] = "Token " + token;
						const toPath = this.$route.query.to || "/";
						this.$router.push(toPath);
						this.loadUserInfo();
					})
					.catch((error) => {
						if (error.response.status === 400) {
							this.errors.splice(0);
							for (const property in error.response.data) {
								switch (property) {
									case "non_field_errors":
										this.errors.push(`${error.response.data["non_field_errors"]}`);
										break;
								}
							}
						} else {
							this.errors.push("Une erreur est survenue");
						}
					});
			}
			this.isLoading = false;
		},
		async loadUserInfo(){
			await axios
				.get('/api/v1/userinfo/me/')
				.then((response) =>{
					this.$store.dispatch("changeUserInfo", response.data);
				})
				.catch((error) => {
					console.log(error);
				});
		},
		validateFormData(formData){
			this.errors.splice(0);
			let validUsername = true, validPassword = true;
			
			if(!formData.username.trim()){
				this.errors.push("Le nom d'utilisateur est invalide")
				validUsername = false;
				this.usernameError = true;
			}
			if(!formData.password.trim()){
				this.errors.push("Le mot de passe est invalide")
				validPassword = false;
				this.passwordError = true;
			}
			return validUsername && validPassword;
		}
	},
};
</script>
<style lang="scss" scoped>
.form-wrapper{
	min-height: 100vh;
}
.login-button{
	width: 100%;
}
</style>