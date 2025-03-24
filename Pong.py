''' Pong Game '''

import pygame
import random
import math
import time

def main():
   # initialize all pygame modules (some need initialization)   
   pygame.init()
   # create a pygame display window   
   pygame.display.set_mode((500, 400))
   # set the title of the display window   
   pygame.display.set_caption('Pong')  
   # get the display surface   
   w_surface = pygame.display.get_surface() 
   # create a game object   
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object   
   game.play()
   # quit pygame and clean up the pygame window   
   pygame.quit()


class Game:
   
   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      
      # === game specific objects
      self.score_left = 0  # number of seconds since the game started
      self.score_right = 0 
      self.ball = Ball('white', 7, [250, 200], [5,1], self.surface)
      self.paddle_left = Paddle('white', [75,175], [10,50], [0, 5],
                                self.surface)
      self.paddle_right = Paddle('white', [425,175], [10,50], [0, 5], 
                                 self.surface) 
      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box (game loop)
         # play frame
         self.handle_events()
         self.draw()
         if self.continue_game:
            self.update()
            self.collision()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 
         
   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      key_stroke = pygame.key.get_pressed()
      events = pygame.event.get() # a list of events
      if self.continue_game:
         self.handle_key_down(key_stroke) 
      
      for event in events: # event
         if event.type == pygame.QUIT:
            self.close_clicked = True 
         if event.type == pygame.KEYUP:
            self.handle_key_up(event)
         
   
   def handle_key_down(self, key_stroke):
      # checks if a key is pressed and does move function 
      # if it is the correct key
      if self.paddle_right.position[1] >= 0:
         if key_stroke[pygame.K_p]:
            self.paddle_right.move_up()
      if self.paddle_right.position[1] <= 350:
         if key_stroke[pygame.K_l]:
            self.paddle_right.move_down()             
      if self.paddle_left.position[1] >= 0:
         if key_stroke[pygame.K_q]:
            self.paddle_left.move_up() 
      if self.paddle_left.position[1] <= 350:
         if key_stroke[pygame.K_a]:
            self.paddle_left.move_down()        
      
            
   def handle_key_up(self, event):
      # when the key is not being pressed, it resets the velocity
      if event.key == pygame.K_p:
         self.paddle_right.stop()
      if event.key == pygame.K_l:
         self.paddle_right.stop()  
      if event.key == pygame.K_q:
         self.paddle_left.stop()
      if event.key == pygame.K_a:
         self.paddle_left.stop()      
         
         
   
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw() 
      self.paddle_left.draw()
      self.paddle_right.draw()
      self.draw_score()
      pygame.display.update()
   
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.ball.move()
        
   
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.score_left == 11:
         self.continue_game = False
      elif self.score_right == 11:
         self.continue_game = False         
         
         
   def collision(self):
      ran = random.randint(1,10)
      size = self.surface.get_size()
      # check if ball makes contact with the left paddle
      if (self.ball.center[1] >= self.paddle_left.position[1]  and
          self.ball.center[1] <= (self.paddle_left.position[1] + 
                                  self.paddle_left.dimensions[1]) and 
          self.ball.center[0] == 85) :
         self.ball.velocity[0] = -self.ball.velocity[0]
         self.ball.velocity[1] = -ran         
         self.bg_color = pygame.Color('pink')
         
      # check if ball makes contact with the right paddle
      elif (self.ball.center[1] >= self.paddle_right.position[1] and
      self.ball.center[1] <= (self.paddle_right.position[1] +
                              self.paddle_right.dimensions[1]) and
      self.ball.center[0] == 425):
         self.ball.velocity[0] = -self.ball.velocity[0]
         self.ball.velocity[1] = -ran
         self.bg_color = pygame.Color('blue')
         
      # add score for each collision with side walls
      if self.ball.center[0] + 7 >= 500: 
         self.score_left += 1
         
         
      if self.ball.center[0] - 7 <= 0:
         self.score_right += 1
         
         
         
         
   def draw_score(self):
      # Draw the current score
      string1 = f"{self.score_left}"
      string2 = f"{self.score_right}"
      font_size = 40
      fg_color = pygame.Color("white")
      # Step 1: Create a Font object
      font = pygame.font.SysFont('', font_size)
      # Step 2: Render the Font object
      text_box1 = font.render(string1, True, fg_color)
      text_box2 = font.render(string2, True, fg_color)
      
      # Step 3: Determine the location of text_box
      location1 = (0, 0)
      location2 = (460, 0)# top left
      # Step 4: Blit the text_box on the surface
      self.surface.blit(text_box1, location1)
      self.surface.blit(text_box2, location2)
     
class Ball:
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity,
                surface):
      # Initialize a ball.
      # - self is the ball to initialize
      # - color is the pygame.Color of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - radius is the int pixel radius of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      
   def move(self):
      # Change the location of the ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the ball
      
      size = self.surface.get_size()
      
      for i in range(0,2):
         # Bouncing
         if (self.center[i] <= self.radius or
         self.center[i] + self.radius >= size[i]):
            self.velocity[i] = -self.velocity[i]
         self.center[i] = (self.center[i] + self.velocity[i])
   
   def draw(self):
      # Draw the ball on the surface
      # - self is the ball
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
      

class Paddle:
   
   def  __init__(self, pad_color, pad_position, pad_dimensions, pad_velocity,
                 surface):
      # color is color of both paddles
      # dimensions is thw width and height of paddles
      # position is the current position of the paddles
      # surface is the surface of the display
      # velocity is the x and y coords that the paddles move at
      self.color = pygame.Color(pad_color)
      self.dimensions = pad_dimensions
      self.position = pad_position
      self.surface = surface
      self.velocity = pad_velocity
   
   def move_up(self):
      
      size = self.surface.get_size()
      # moves the paddle depending on the button being pressed
      # if the paddle reaches the border, it stops
      for i in range(0,2):
         self.position[i] = (self.position[i] - self.velocity[i]*1.5)
         if self.position[i] < 0:
            self.velocity[i] = 0
            
   def move_down(self):
      
      size = self.surface.get_size()
      # moves the paddle depending on the button being pressed
      # if the paddle reaches the border, it stops      
      for i in range(0,2):
         self.position[i] = (self.position[i] + self.velocity[i]*1.5)
         if self.position[i] > size[i] - self.dimensions[i]:
            self.velocity[i] = 0   
         
   def stop(self):
      # when the button is released, it sets the velocity ot the original
      self.velocity[1] = 5
   
   def draw(self):
      # Draw the ball on the surface
      # - self is the ball
      pygame.draw.rect(self.surface, self.color,
                       (self.position, self.dimensions))
      
main()
