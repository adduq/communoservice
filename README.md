<h1 align="center">Communoservice</h1>

<p align="center">
    Full-stack web project using Django REST Framework and Vue JS
    <br />
    <a href="https://github.com/vp-0/communoservice"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://communoservice.herokuapp.com">View Demo</a>
    ·
    <a href="https://github.com/vp-0/communoservice/issues">Report a bug</a>
    ·
    <a href="https://github.com/vp-0/communoservice/issues">Request a feature</a>
  </p>
</p>

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![Pull Requests][pullrequests-shield]][pullrequests-url]
[![Total Lines][lines-shield]][lines-url]
[![Open in VSCode][openin-shield]][openin-url]

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#context">Context</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


This project is our first and final assignement for our full-stack web course at 
[Cégep Garneau](https://www.cegepgarneau.ca/). 

### Context
An imaginary company wishes to carry out a project allowing people to create small
offers (ie: lawn mowing, carpentry, cleaning) in exchange for financial compensation.

### Built With

Here's a list of the frameworks that were used to create this project.
* [Vue JS](https://vuejs.org/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Axios](https://github.com/axios/axios)



<!-- GETTING STARTED -->
## Getting Started


To get a local copy up and running follow the next few steps.

### Prerequisites

In order to run communoservice locally, you will need to install the following applications:
*  [Docker](https://docs.docker.com/install/)
*  [Docker-Compose](https://docs.docker.com/compose/)
### Installation

1. Clone the repo
   ```
   git clone https://github.com/vp-0/communoservice.git
   ```
2. Navigate into the cloned repository
   ```
   cd  communoservice
   ```
3. Run docker compose
   ```
   docker-compose up --build
   ```
4. Wait until the container is up and running, then navigate to
   ```
   localhost:8000
   ```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/vp-0/communoservice/issues) for a list of proposed features (and known issues).


<!-- CONTACT -->
## Contact

Andrew - [@vanity_pw](https://twitter.com/vanity_pw) - andrewduquette@gmail.com




<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Bulma](https://bulma.io/)
* [Bulma-Toast](https://www.npmjs.com/package/bulma-toast)
* [Djoser](https://github.com/sunscrapers/djoser)
* [Django Cors Headers](https://pypi.org/project/django-cors-headers)
* [GitHub Actions](https://github.com/features/actions)
* [Font Awesome](https://fontawesome.com)
* [Heroku Hosting](https://www.heroku.com/)

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/vp-0/communoservice.svg?style=for-the-badge
[contributors-url]: https://github.com/vp-0/communoservice/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/vp-0/communoservice.svg?style=for-the-badge
[issues-url]: https://github.com/vp-0/communoservice/issues
[pullrequests-shield]: https://img.shields.io/github/issues-pr/vp-0/communoservice?style=for-the-badge
[pullrequests-url]: https://github.com/vp-0/communoservice/pulls
[lines-shield]: https://img.shields.io/tokei/lines/github/vp-0/communoservice?style=for-the-badge
[lines-url]: https://github.com/vp-0/communoservice/
[openin-shield]: https://img.shields.io/badge/Open%20in%20VSCode-%23007ACC?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAC00lEQVQYGX3BX2iVZRwH8O/ze//t/NkcRzdXmzZzLLYMmyVJUFQgzkQoqOsgAtNu6jK6kqjbIqOErrrTCBUUbBTYuZCMoDE0FZLp3DpnZ9s55313znmf/89TEV1JfT5s6uIG5LlvsPTdKViK8fCzr2H8wGEw1UIpNqgUYkRx38Bajqorb08ateWT62l+NrtxBSH+R0KAdhhbaelqp7X26MTTE9ix58UzG83u+7/l9Q9DEMHKHE4JoNiHf0UEKIvH1zh+lMZsC+ME3ZzDt4FiUtz75NE3viXvDYpbx44AHkjXwShAQIBx7PkGD37NtdsWBAzWGihtYD2QtXsQxkmienu+9MRzl3Yf++wylQaLulWHIXolU76qjI8DBmil0drkn/qocFkbCwsGrbQilXUUz3vo3/PS7PiJL38pPDL10eb68nllHQIiGGfxe231BI1MvlceHk2lyGG9h/UeoSzoZ0i507Kx8mYyMjHth3ZOiz9uIehs+F5x63xN0Tvh0Ni13dMz4Fw8ZJwHwPA30k0JsVF/26SNW7ybQQgBN/wY9OCOzsp89ZD44etro4NbkFQi5FwY4xmMB4wHSDY5XCc7bZr3pmy2CksRFO/CVMb7KzMH5yLbPXDv/CmkLQkqlENjPYwFjAUoSsTPNqRjtjwc5XcXbvZuXv3YxmWoTsrCkcl9Q299/pMqDR9fnDsDFoc14xms97Deg0yaxDpWkKwwl9XW9qulGx9Abr6qPQPP2jCSozJ7/IuuCz9p318aZFEC4wHjAdK9ZEaz3lGh9CxjcR4UBwDevmDT5Re0gxZSw0gBjEy+y7V72ToGbTwsi2JigYMz/hJjACP8I0xAqld1zTtPaa1aCgGMFHCMYB3ASgOwCBLCXxhjeEBYANP5dVe/vddysSh9ABcVgP4IPG8vNL7/6vUQ/8kDcR+YyFf04sIMje6q6t5msnrl6kmRpWf1/ev4E5Tbl9R3VUZRAAAAAElFTkSuQmCC&style=for-the-badge
[openin-url]: https://open.vscode.dev/vp-0/communoservice