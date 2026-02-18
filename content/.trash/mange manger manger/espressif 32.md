---
nom: "espressif 32"
qid: Q27921668
type: objet
categorie: objet
tags: "#objet"
image: esp32-esp-wroom-32_d.jpg
---

# ESP32

> [!Infobox]
> **ESP32**
> ![[esp32-esp-wroom-32_d.jpg|300]]
> - **Fabricant** : TSMC
> - **Précédé par** : ESP8266
> - **Développé par** : Espressif Systems
> - **Date d'annonce publique** : 5 novembre 2015
> - **Date de commercialisation** : 5 septembre 2016
> - **Nomme d'apres** : Espressif Systems, Architecture 32 bits
> - **Utilise** : Bluetooth, café akhawayn
> - **Capacité de stockage** : 520 kilo-octet
> - **Processeur** : Tensilica Xtensa LX6
> - **Fréquence d'horloge** : 160 mégahertz, 240 mégahertz

ESP32 est une série de microcontrôleurs de type système sur une puce (SoC) d'Espressif Systems, basé sur l'architecture Xtensa LX6 de Tensilica (en), intégrant la gestion du Wi-Fi et du Bluetooth (jusqu'à LE 5.0 et 5.1) en mode double, et un DSP. C'est une évolution d'ESP8266. Le principal outil de développement est ESP-IDF, logiciel libre développé par Espressif, écrit en C et utilisant le système temps réel FreeRTOS. Il intègre un nombre important de bibliothèques et on retrouve dans son écosystème des bibliothèques tierce libres pour différents types de périphériques liés à l'embarqué et au temps réel.
Le ESP32-C3, WiFi, BLE, Bluetooth, est une variante, annoncée et sorti en novembre 2020, compatible broche à broche avec l'ESP8266, mais utilisant l'architecture RISC-V 32 bits plutôt que Xtensa. Le support du développement via la plateforme et l'IDE d'Arduino est disponible depuis la bibliothèque ESP32 2.0.0.
Plus généralement, La série ESP32-C est basée sur RISC-V et la série ESP32-S sur Xtensa LX6.
Son support Wi-Fi et Bluetooth en fait un système apprécié dans le domaine de l'internet des objets.
Ce SoC rencontre un certain succès depuis quelques années à la fois pour son coût, ses capacités et son intégration dans un nombre croissant de systèmes.

## Caractéristiques techniques

Les ESP32 comprennent notamment les caractéristiques techniques suivantes:

Processeurs:
CPU: Xtensa double-cœur (ou simple-cœur), microprocesseur LX 32 bits, fonctionnant à 160 ou 240 MHz et fournissant jusqu'à 600 DMIPS;
coprocesseur ultra basse consommation (ULP);
Mémoire: 32 Mo SRAM;
Connectivité sans-fil:
Wi-Fi: 802.11 b/g/n;
Bluetooth: v 4.2 BR/EDR et BLE jusqu'à v 5.0 et v 5.1;
Interfaces de périphériques:
Segmentation 12-bit sur les ADC (SAR ADC) jusqu'à 18 canaux;
2 × 8 bit DAC;
10 × capteurs de toucher (GPIO de capteur capacitif (en));
4 × SPI;
2 × interfaces I²S;
2 × interfaces I²C;
3 × UART;
contrôleur hôte SD/SDIO/CE-ATA (en)/MMC/eMMC;
contrôleur esclave SDIO/SPI;
interface MAC Ethernet avec DMA dédié et support du protocole de temps précis IEEE 1588;
Bus de données CAN 2.0;
contrôleur infrarouge distant (TX/RX, jusqu'à 8 canaux);
Moteur PWM;
LED PWM (jusqu'à 16 canaux);
Capteur à effet Hall;
pré-amplificateur analogique ultra-basse consommation;
Sécurité:
Standard de sécurité supportant complètement IEEE 802.11,incluant WPA/WPA2 et WAPI de WFA;
Secure boot (démarrage sécurisé);
Chiffrement de la Flash;
1024-bit OTP, jusqu'à 768 bit pour les clients;
Accélération matérielle du chiffrement: AES, SHA-2, RSA, Cryptographie sur les courbes elliptiques (ECC), Générateur de nombres aléatoires (RNG);
Gestion de l'énergie:
low-dropout regulator (en) interne.
Domaines d'alimentation individuels pour le RTC
Alimentation en sommeil profond de 5 μA;
Réveil depuis des interruption GPIO, timer, mesure ADC, interruption du capteur de touché capacitif.

## Stockage intégré

L'ESP32 comprend la mémoire intégrée suivante:

## ESP32-S2

Comporte un processeur Xtensa LX7 pouvant monter jusqu'à 240 MHz
Un coprocesseur RISC-V est introduit pour le mode ULP.
Accélération matérielle du chiffrement
Il n'y a pas de fonctions Bluetooth
WiFi 2.4 Ghz (IEEE 802.11b/g/n)

## ESP32-S3

Comporte deux processeur Xtensa LX7 pouvant monter jusqu'à 240 MHz
Accélération matérielle du chiffrement
Wifi 802.11 b/g/n, Bluetooth 5.0 LE
Un coprocesseur RISC-V est toujours présent pour le mode ULP.

## ESP32-PICO-D4

Il s'agit d'un System in package (système dans un paquet) et non d'un SoC.

Deux processeurs Xtensa LX6
4MB SPI flash
WiFi 802.11 b/g/n/e/i, BT
consommation moyenne de 80 mA.

## ESP32-C2 (ESP8684)

Cœur d'architecture RISC-V 272 ko de SRAM intégré (16 ko de cache).

1 cœur RISC-V 32 bits basse consommation à 120 MHz
Accélération matérielle du chiffrement
576 ko de ROM
1 ko eFuse
WiFi 4.0 b/g/n 2.4 GHz largeur de bande 20 MHz (72.2 Mb/s max)
Bluetooth 5.0 LE
Extensions de chiffrement AES

## ESP32-C3 (ESP8686)

Contrairement à ses prédécesseurs, le microcontrôleur principal est un unique cœur d'architecture RISC-V RV32IMC 400 ko de SRAM intégré (16 ko de cache). Il permet l'utilisation de ESP-IDF, basé sur FreeRTOS, à une fréquence maximum de 160 MHz., il apporte cependant de meilleures performances qu'un seul cœur LX7 à 160 MHz.

1 cœur RISC-V 32 bits jusqu'à 160 MHz
Accélération du chiffrement
384 ko de ROM
WiFi 4.0 b/g/n 2.4 GHz largeur de bande 20 MHz, 40 MHz en 802.11n (150 Mb/s max)
Bluetooth 5.0 LE
Extensions de chiffrement AES

## ESP32-C5

Basé sur un cœur RISC-V pouvant monter jusqu'à 240 Mhz, ce module n'a pas d'unité d'accélération de chiffrement, mais gère par contre le WiFi 6.0 en double bande. Il permet l'utilisation de ESP-IDF, basé sur FreeRTOS.

1 cœur RISC-V 32 bits jusqu'à 240 MHz
dual-band WiFi 6.0 802.11ax (largeur de bande 20MHz) en 2.4 GHz et 5.0 GHz, WiFi 4.0 802.11b/g/n (largeur 20MHz et 40MHZ)
Bluetooth 5.0 LE
Sur circuit intégré: 400 ko RAM, 384 ko ROM
Capteur de température et système d'horloge temps-réel (RTC).

## ESP32-C6

Comme le C3, il se base sur un processeur d'architecture RISC-V.

1 cœur RISC-V 32 bits jusqu'à 160 MHz
Extension d'accélération du chiffrement AES
IEEE 802.11ax (Wi-Fi 6) à 2.4 GHz, supportant une bande passante de 20 MHz dans le mode 11ax et 20 or 40 MHz de bande passante dans les modes 802.11b/g/n
Bluetooth 5.0 LE (2 Mbps)

## ESP32-C61

Comme le C6, il se base sur un processeur d'architecture RISC-V.

1 cœur RISC-V 32 bits jusqu'à 160 MHz
Extension d'accélération du chiffrement AES, ECDSA-based Digital Signature (DS) peripheral, Trusted Execution Environment (TTE)
IEEE 802.11ax (Wi-Fi 6) à 2.4 GHz, supportant une bande passante de 20 MHz dans le mode 11ax et 20 ou 40 MHz de bande passante dans les modes 802.11b/g/n
Bluetooth 5.0 LE (2 Mbps) et BLE Mesh 1.1
Quad SPI PSRAM jusqu'à 120 MHz
module Event Task Matrix (ETM) module pour l'automatisation par déclencheur des tâches.

## ESP32-P4

L'ESP32-P4 est une version comportant deux contrôleurs RISC-V à 400Mhz et un contrôleur RISC-V basse consommation à 40 Mhz, pour le mode veille:

2 cœurs RISC-V 32 bits RV32IMAFCZc jusqu'à 400 MHz
1 cœur RISC-V 32 bits jusqu'à 40 MHz
Un NPU, un décodeur H264 et JPEG, ainsi qu'un processeur géométrique 2D.
Opérations vectorielles 128-bit, incluant les multiplication, addition, soustraction, décalage et comparaison
Accélération du chiffrement AES jusqu'à ECDSA.
Supporte ethernet, mais pas de réseau sans-fil.
Compatible MIPI I3C

## Série ESP32-H

Tous les SoC de la série ESP32-H utilisent le jeu d'instruction RISC-V.

## ESP32-H2

Également basé sur un cœur RISC-V 32 bits, orienté basse consommation et sécurité(en) « ESP32-H2 », sur Espressif.

IEEE 802.15.4
Thread, Zigbee, Bluetooth 5 (LE)

## Variantes à bas prix

Les ESP32-Pico sont notamment utilisés dans les montres connectées. Ils comportent 2 cœurs Tencilia LX6.

## Outils de développement et systèmes

Il est notamment supporté par les outils de programmation suivants:

ESP-IDF (développement en C, avec outils en Python, se base sur FreeRTOS, c'est le système de développement de base;
Apache NuttX, système compatible POSIX, porté sur ESP32-C3 (RISC-V) uniquement.
Arduino IDE avec le module ESP32 Arduino Core, interface en Java, développement en C++;
Espruino (en);
ESPHome, spécialisé domotique, comportant une interface web pour l'interaction;
FAUST, langage de programmation de traitement de données audio, utilisant son DSP;
Lua RTOS pour ESP32;
MicroPython, une variante pour l'embarqué du langage Python;
mruby (en), une variante pour l'embarqué du langage Ruby;
NodeMCU;
MicroEJ;
ESP32forth, programmation en Forth 32 bits pour ESP32

## IoT

Les Cartes IoT NodeMCU les plus récents utilisent ESP32-S à la place de ESP8266.
Le kit de développement modulaire M5Stack.
Les cartes IoT TTGO
Les cartes ESP32 d'uPesy
Différents modules réseau sans fil, supportant LoRa, WiFi et Bluetooth, autonomes ou intégrés dans d'autres cartes de développement, telles que les cartes de Sipeed basés sur des processeurs RISC-V.

## Synthétiseurs

L'ESP32 est adapté à la création des Synthétiseurs avancés, dont des synthétiseurs analogiques. Le langage FAUST ou la bibliothèque ESP32soundsynth permettent de faciliter le développement de synthétiseurs basés sur cette architecture. L'échantillonnage utilisant l'ADC intégré peut être effectué via la plateforme de développement Arduino.
Il est notamment adapté à des synthétiseurs au format Eurorack, comme le CTAG-Strämpler.
Qun-synthesizer est un synthétiseur analogique portable, basé sur la carte ESP32-LyraT, fonctionnant avec la carte mère Nunomo.

## Console de jeu portable

Hardkernel, a créé en 2018 Odroid-Go, une console de jeu portable à très bas prix basée sur cette puce.

## Faille de sécurité

Le 6 mars 2025, la société Tarlogic a annoncé une faille de sécurité majeure affectant ce composant et l'annonce a été relayée par plusieurs médias. Cette faille permet à un attaquant de prendre possession d'un appareil et de l'utiliser à sa guise. La communauté encourage vivement à mettre à jour ses équipements dans le dernier firmware disponible et à se maintenir informé des évolutions.

## Plaques modulaires à montage en surface

Les circuits imprimés à montage en surface (PCB) basés sur l'ESP32 contiennent directement le SoC ESP32 et sont conçus pour s'intégrer facilement à d'autres circuits imprimés. Des antennes en F inversé sinueux sont utilisées pour les antennes à pistes PCB. Une piste PCB est un chemin conducteur reliant les composants du circuit imprimé, permettant ainsi la connexion des signaux électriques, de l'alimentation et de la masse.

## Développement et autres cartes

Les cartes de développement et de dérivation étendent le câblage et peuvent ajouter des fonctionnalités, s'appuyant souvent sur les cartes de modules ESP32 et les rendant plus conviviales pour le développement.
