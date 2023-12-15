# TEE PELI TÄHÄN
import pygame
import random

class omapeli:
    def __init__(self, vaikeus: int):
        pygame.init()
        #asetetaan kaikki muuttujat, kuvat ja fontit
        self.aloitus = False
        self.vaikeus = vaikeus  #vaikeustaso, jota voidaan muuttaa alustaessa ohjelma
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.lopfontti = pygame.font.SysFont("Arial", 50)
        self.pikkufontti = pygame.font.SysFont("Arial", 17)
        alkuteksti = self.lopfontti.render("Paina Enter aloittaaksesi pelin", True, (181, 165, 16))
        alkuteksti2 = self.fontti.render("Liikuta robottia nuolinäppäimillä", True, (181, 165, 16))
        alkuteksti3 = self.fontti.render("Kerää kolikoita ja väistele hirviötä", True, (181, 165, 16))
        alkuteksti4 = self.fontti.render("Vaikeustaso nousee joka 10. kolikko ja peli päättyy kun saat 50", True, (181, 165, 16))
        self.hirvio = pygame.image.load("hirvio.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.robo = pygame.image.load("robo.png")
        self.kolikkocount = -1
        
        #asetetaan näyttö
        self.naytto = pygame.display.set_mode((800, 800)) 
        pygame.display.set_caption("quite impossible")
        #luodaan pelille aloitus ruutu, johon peli aina siirtyy hävitessä, voittaessa ja aloittaessa
        while self.aloitus == False:
            self.naytto.fill((120, 120, 120))
            self.naytto.blit(alkuteksti, (70, 160))
            self.naytto.blit(alkuteksti2, (70, 300))
            self.naytto.blit(alkuteksti3, (70, 330))
            self.naytto.blit(alkuteksti4, (70, 360))
            pygame.display.flip()
            #peli alkaa kun painetaan Enteriä
            for tapahtuma in pygame.event.get():
                    if tapahtuma.type == pygame.KEYDOWN:
                        if tapahtuma.key == pygame.K_RETURN:
                            self.aloitus = True
                            break
                    if tapahtuma.type == pygame.KEYUP:
                        if tapahtuma.key == pygame.K_RETURN:
                            self.aloitus = False
                    
                    if tapahtuma.type == pygame.QUIT:
                        exit()
        #aloitetaan liikkujien eli hirviön ja robotin funktiot
        self.liikkujat()
        #aloitetaan kolikoiden oma erillinen funktio
        self.kolikot()
   

    def hirvioliikkumine(self):
        loseteksti = self.lopfontti.render("Hävisit!", True, (181, 165, 16))
        loseteksti2 = self.fontti.render("Sait " + str(self.kolikkocount) + " kolikkoa", True, (181, 165, 16))
        self.naytto.blit(self.hirvio, (self.hirvio_x, self.hirvio_y))

        #hirviön x akseli liikkuminen
        self.hirvio_x += self.hirv_xnopeus
        if self.hirv_xnopeus > 0 and self.hirvio_x+self.hirvio.get_width() >= 800:
            self.hirv_xnopeus = -random.randint(self.vaikeus, self.vaikeus*self.vaikeus) 
        if self.hirv_xnopeus < 0 and self.hirvio_x <= 0:
            self.hirv_xnopeus = random.randint(self.vaikeus, self.vaikeus*self.vaikeus)

        #hirviön y akseli liikkuminen
        self.hirvio_y += self.hirv_ynopeus
        if self.hirv_ynopeus > 0 and self.hirvio_y + self.hirvio.get_height() >= 800:
            self.hirv_ynopeus = -random.randint(self.vaikeus, self.vaikeus*self.vaikeus)
        if self.hirv_ynopeus < 0 and self.hirvio_y <= 60:
            self.hirv_ynopeus = random.randint(self.vaikeus, self.vaikeus*self.vaikeus)   

        #jos robotti osuu hirviöön, pelaaja häviää
        if self.hirvio_x - self.hirvio.get_width()+30 < self.x < self.hirvio_x + self.hirvio.get_width()-30 and self.hirvio_y - self.hirvio.get_height()+6< self.y < self.hirvio_y + self.hirvio.get_height()-25:
            self.naytto.blit(loseteksti, (320, 70))
            self.naytto.blit(loseteksti2, (323, 120))
            pygame.display.flip()
            pygame.time.delay(3000), omapeli(2)
            
            
    def liikkujat(self): 
        #asetetaan hirviön alkupaikka ja luodaan vaihtelevat nopeudet hirviölle, jotta se pomppii sattumanvaraisesti
        self.hirvio_x = 0
        self.hirvio_y = 60
        self.hirv_ynopeus = random.randint(self.vaikeus, self.vaikeus*self.vaikeus*2)
        self.hirv_xnopeus = random.randint(self.vaikeus, self.vaikeus*self.vaikeus*2)
        #asetetaan robotin alkupaikka ja luodaan sen liikkumista varten alustukset
        self.x = 0
        self.y = 800-self.robo.get_height()
        #asetetaan ensimmäinen kolikko samaan kohtaan kuin robotti alussa
        self.kolikkoy = self.y 
        self.kolikkox = self.x
        oikealle = False
        vasemmalle = False
        ylos = False
        alas = False

        kello = pygame.time.Clock()   

        while self.aloitus:
            #tehdään pelin silmukka ja kaikki tekstit, kolikot yms.
            self.naytto.fill((120, 120, 120))
            self.kolikot()
            pygame.draw.rect(self.naytto, (0, 0, 0), pygame.Rect(0, 0, 800, 60))
            lopetusteksti = self.lopfontti.render("Voitit pelin!", True, (181, 165, 16))  
            pikkuteksti = self.pikkufontti.render("Kerää kolikoita ja väistele hirviötä,", True, (181, 165, 16))  
            pikkuteksti2 = self.pikkufontti.render("vaikeustaso nousee joka 10. kolikko", True, (181, 165, 16))  
            kolikteksti = self.fontti.render("Kolikoita: " + str(self.kolikkocount) + "/50", True, (181, 165, 16))
            vaikteksti = self.fontti.render("Vaikeustaso: " + str(self.vaikeus-1) + "/5", True, (181, 165, 16))
            self.naytto.blit(vaikteksti, (25, 25))
            self.naytto.blit(kolikteksti, (625, 25))
            self.naytto.blit(pikkuteksti, (272, 10))
            self.naytto.blit(pikkuteksti2, (265, 30))

            if self.kolikkocount >= 50:
                self.naytto.blit(lopetusteksti, (280, 70))


            self.naytto.blit(self.robo, (self.x, self.y))
            self.hirvioliikkumine()
            pygame.display.flip()

            #koodi robotin liikuttamiselle
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = True
                    if tapahtuma.key == pygame.K_UP:
                        ylos = True
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = True

                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = False
                    if tapahtuma.key == pygame.K_UP:
                        ylos = False
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = False

                #jos pelaaja saa 50 kolikkoa, pelaaja voittaa (51 myös, jotta peli ei vahingossa jatku pidempään)
                if self.kolikkocount == 50 or self.kolikkocount == 51:
                    pygame.time.delay(3000), omapeli(2)
                    

                if tapahtuma.type == pygame.QUIT:
                    exit()
            
            #koodi, jotta robotti ei mene alueen ulkopuolelle
            if oikealle:
                if self.x + self.vaikeus <= 800-self.robo.get_width():
                    self.x += self.vaikeus*2
            if vasemmalle:
                if self.x - self.vaikeus >= 0:
                    self.x -= self.vaikeus*2
            if ylos:
                if self.y - self.vaikeus >= 60:
                    self.y -= self.vaikeus*2
            if alas:
                if self.y + self.vaikeus <= 800-self.robo.get_height():
                    self.y += self.vaikeus*2

            kello.tick(60)


    def kolikot(self): 
        #ensimmäinen kolikko menee robotin kanssa päällekkäin ja siksi kolikkojen alkuarvo on -1
        #aina kun pelaaja osuu kolikkoon, se vaihtaa paikkaa ja kolikkojen määrä nousee yhdellä
        if self.x-self.robo.get_width()+10 < self.kolikkox < self.x+self.robo.get_width() and self.y - self.robo.get_height()+40 < self.kolikkoy < self.y + self.robo.get_height():
            self.kolikkocount += 1
            
            if self.kolikkocount == 10:
                self.vaikeus += 1
            if self.kolikkocount == 20:
                self.vaikeus += 1
            if self.kolikkocount == 30:
                self.vaikeus += 1
            if self.kolikkocount == 40:
                self.vaikeus += 1
            
            self.kolikkox = random.randint(0,800-self.kolikko.get_width())   
            self.kolikkoy = random.randint(60,800-self.kolikko.get_height())   
            
        return self.naytto.blit(self.kolikko, (self.kolikkox, self.kolikkoy))


if __name__ == "__main__":
    omapeli(2)