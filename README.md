# Zdalnie sterowany pojazd z kamerą

![chase](https://user-images.githubusercontent.com/6802432/115985180-f518d200-a5aa-11eb-9031-ad7877e00b5b.jpg)


## Potrzebne rzeczy.
### Podwozie:
- Kawałek cienkiej deski lub sklejki (ja użyłem kawałka panela podłogowego) - wymiary wedle uznania.
- 4 koła https://botland.com.pl/kola-z-oponami/14245-kolo-z-opona-65x26mm-zolte.html
### Elektronika:
- Raspberry pi - ja użyłem Raspberry pi 3B+
- Karta pamięci microSD > 4 GB 
- sterownik silników pololu DRV8835 https://botland.com.pl/raspberry-pi-hat-kontrolery-silnikow-i-serw/2678-drv8835-dwukanalowy-sterownik-silnikow-11v12a-nakladka-dla-raspberry-pi-pololu-2753.html
- 4 silniki https://botland.com.pl/silniki-dc-katowe-z-przekladnia/16016-silnik-dc-148-3-6v-z-podwojnym-walem-200rpm.html
- Wzmacniacz https://botland.com.pl/czujniki-dzwieku/12806-wzmacniacz-audio-stereo-pam8403-5v-3w-dwukanalowy-czerwony-5903351241106.html
- Głośniki https://botland.com.pl/glosniki-analogowe/3468-glosnik-mg24-15-05w-8ohm-24x15x4mm.html
- Przewód jack 3,5mm https://botland.com.pl/przewody-i-zlacza-audio/2553-przewod-jack-35mm-stereo-dlugosc-15m-5900804012894.html
- Diody (dwie czerwone i dwie niebieskie)
- Dwa rezystory 330R
- Przewody
- Kamera do Raspberry Pi https://aliexpress.ru/item/1005001597402383.html?spm=a2g0s.9042311.0.0.1e5033edgNuFDn&_ga=2.24958962.939567052.1613203256-919384818.1613203256&sku_id=12000016727750468
### Zasilanie:
- koszyk na 6 baterii AA https://botland.com.pl/koszyki-na-baterie/2430-koszyk-na-6-baterii-typu-aa-r6-2x3.html
- 6 baterii lub akumulatorów AA
- Powerbank do zasilania Raspberry Pi
### Narzędzia:
- Lutownica
- Dwustronna taśma montażowa

## Konstrukcja
1. Przyklej silniki do podwozia taśmą montażową i załóż koła.
![kola](https://user-images.githubusercontent.com/6802432/115985428-204ff100-a5ac-11eb-8b88-09445fe6efec.jpg)
2. Przylutuj elementy sterownika silników.
 
![image](https://user-images.githubusercontent.com/6802432/115985508-702eb800-a5ac-11eb-9fb4-b7d78c30f266.png)

3. Przyklej koszyk na baterie do podwozia taśmą montażową.
4. Połącz przewody silników i koszyka ze sterownikiem. Jeżeli masz silniki bez przylutowanych przewodów, to najpierw musisz je przylutować. Podłącz przewody z koszyka na baterię z odpowiednimi złączami śrubowymi (plus do VIN, minus do GND). Podłącz silniki do pozostałych złącz śrubowych tak jak na rysunku. 

![image](https://user-images.githubusercontent.com/6802432/115985597-d582a900-a5ac-11eb-93c3-d95041450321.png)

5. Załóż sterownik na raspberry pi.
6. Przylutuj głośniki do wzmacniacza. Prawy głośnik do R+ i R-, lewy do L+ i L-, zasilanie z odpowiednich pinów RPI do +5V i GND.

![image](https://user-images.githubusercontent.com/6802432/115986206-63f82a00-a5af-11eb-9a04-df9d1377cc2f.png)

8. Przylutuj diody do rezystorów i Raspberry Pi. Niebieskie do pinu 20, a czerwone do pinu 21.
9. Podłącz i zamocuj kamerę (zawsze to rób przy wyłączonym rpi, bo łatwo kamerę uszkodzić.

## Oprogramowanie
### System
1. Zainstaluj system operacyjny Raspbian na karcie microSD, najjlepiej użyć rpi-imager z https://www.raspberrypi.org/software/
2. Uruchom Raspberry Pi z podłączonym ekranem (monitor lub tv) przez hdmi oraz klawiaturą i myszką przez USB.
3. Przejdź przez początkową konfigurację i połącz się z internetem.
4. W raspi-config -> interface options: Enable camera i ssh.
5. Uruchom ponownie.

### Sterowanie
1. Pobierz skrypt sterujący robotem z githuba: git clone https://github.com/slachy/roboticCar.git
2. cd roboticCar
3. Uruchomienie: sudo python chaseRobot.py
4. Start przy starcie systemu:
    - sudo systemctl edit --force --full chaseRobot.service  
```
[Unit]
Description=Robo Chase
Wants=network-online.target
After=network-online.target
[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/roboticCar/
ExecStart=/home/pi/roboticCar/chaseRobot.py
[Install]
WantedBy=multi-user.target
```
sudo systemctl enable chaseRobot.service

### Podgląd z kamery
1. Na RPI:
```
raspivid -t 999999 --hflip --vflip -o - -w 512 -h 512 -fps 15 | <ip> <port>
```
W zależności od przymocowania kamery można zmieniać przez --hflip i --vflip
2. Na PC:
```
nc -l -p 5001 | mplayer  -fps 24 -cache 512 -
```

### Aplikacja mobilna do sterowania
WIFI Command Center

## Nadwozie
Elementy nadwozia wydrukowałem na bloku technicznym. Wzory: https://www.analogi.net/razvivashki/shest-bumazhnyh-podelok-s-mashinkami-i-geroyami-shhenyachego-patrulya
Trzeba przeskalować odpowiednio, najlepiej zmierzyć średnice koła i dopasować odpowiednio szablon.


