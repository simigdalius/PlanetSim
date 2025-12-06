# Εισάγω τις βιβλιοθήκες που χρειάζομαι
import pygame  #για τα 2d γραφικά
import math    #για τα μαθηματικά
pygame.init()  #αρχικοποίηση βιβλιοθήκης

#Φτιάχνω το window του pygame
WIDTH, HEIGHT = 1000, 800  #ορίζει το μέγεθος 
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #WIN=WINDOW 
    #βιβλιοθήκη, συνάρτηση display για να δείχνει το παράθυρο, συνάρτηση set_mode ορίζει το μέγεθος από τα δεδομένα WIDTH και HEIGHT

pygame.display.set_caption("Planet Simulation") #Βάζει τίτλο στο παράθυρο

BP = (0, 6, 33) #ορίζω το χρώμα Black Purple με RGB values
YELLOW = (255, 179, 26)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DG = (80, 78, 81)
WHITE = (250, 250, 250)

FONT = pygame.font.SysFont("comicsans", 16)

#Δημιουργώ τους πλανήτες
class Planet: #το class είναι ουσιαστικά μια κατηγορία από όπου δημιουργώ αντικείμενα
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU     #1AU = 100 pixels
    TIMESTEP = 3600 * 24  #1 DAY

    def __init__(self, x, y, radius, color, mass):
        self.x = x   #in m
        self.y = y   # in m
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win): 
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)    

        
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2,y - (distance_text.get_height()+50)/2))

       

   
   
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)  #η atan2 ειναι συναρτηση του math στην python που δίνει τη γωνία
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        #Υπολογίζω ταχύτητες
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        #Υπολογίζω θέσεις και τροχιά
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y)) #Ενώνει το x και y για να δώσει τη συνολική τροχιά





#Συνάρτηση που θα δημιουργεί τη λούπα ώστε να μένει ανοιχτό το παράθυρο (event loop)
def main():
    run = True #μεταβλητή που τη θέτω true
    clock = pygame.time.Clock() #ορίζω μεταβλητή Clock που ορίζει το frame rate, δηλαδή την ταχύτητα που θα αλλάζουν τα frames

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.37 * Planet.AU, 0 ,8, DG, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]





    
    while run: #όσο τρέχει το πρόγραμμα (η run είναι true)
        clock.tick(60) #ορίζω την ταχύτητα σε 60 frames per second
        WIN.fill(BP) #χρωματίζει το παράθυρο
        
        for event in pygame.event.get(): #μας δίνει τη λίστα για όλα τα events που θα συμβούν
            if event.type == pygame.QUIT: #εδώ έχουμε μόνο το εξής enent: πατάω το χ και κλείνει το παράθυρο
                run = False #τότε το run γίνεται false, δηλαδή κλείνει το παράθυρο

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update() #κάνει update κάθε φορά ότι γίνεται σε κάθε λούπα και το εμφανίζει για να μην εξαφανίζεται ότι δείχνει το παράθυρο

    pygame.quit()
    

main() 

