# Parking Space Detector

<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<!-- <br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</p>
-->


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Running](#running)
* [Future Work](#Futurework)
* [License](#license)



<!-- ABOUT THE PROJECT -->
## About The Project

[![output_screenshot][product-screenshot]](assets/output.jpeg)

This project can be used anywhere to detect parking spaces. I've seen that parking spaces in malls use ultrasonic sensors to detect if a parking space is occupied or not.We know that the sensors are not that reliable as they can get damaged easily due to external forces. I've even seen that they have camera's are at every corner of the parking space for surveillance purposes. That is when I thought why not use only the camera for both purposes i.e parking space detection and surveillance.

This would reduce the cost of buying and replacing hardware and also just by using camera we can provide extra information like the  number plate, in time, out time etc. 

### Built With

* [Darknet](https://github.com/SravanChittupalli/darknet)
* [opencv-python 4.2.0.34 ](https://pypi.org/project/opencv-python/4.2.0.34/)

<!-- GETTING STARTED -->
### This repository contains:
    - Python code for detection
    - ROI selection code
    - 1 Video for testing

### Running

1. Clone and build [AlexyAb's darknet](https://github.com/SravanChittupalli/darknet) repository adn follow the build instructions giver there.
2. Clone this repository into darknet folder
```
git clone https://github.com/SravanChittupalli/Parking-space-detector.git
```
3. Download [weights](https://drive.google.com/file/d/1SCC_VWyjkAERlL2yscq-bRfRthWgA8xi/view?usp=sharing) into the darknet folder
4. Copy and Paste the contents of `code` folder into the darknet folder.
5. Copy the contents of `cfg` folder to `cfg` folder of darknet
6. copy the `test_videos` folder to `darknet` folder.
7. Open a terminal and run `python parking_project.py`



<!-- To-Do -->
## Future work

This model is very huge and is not deployable on an edge device. My plan is to work with smaller models and increase the efficiency.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

## Video Link

[Video](https://youtu.be/ubb5JhhuMLw)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/SravanChittupalli/Lane-following-bot-in-Gazebo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/SravanChittupalli/Lane-following-bot-in-Gazebo/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/SravanChittupalli/Lane-following-bot-in-Gazebo/stargazers
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/SravanChittupalli/Lane-following-bot-in-Gazebo/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/sravan-chittupalli-a3777b16a/
[product-screenshot]: assets/output.jpeg