import pygame
import math
import random
import numpy as np
width = 800
height = 600
speed = 5
angular_velocity = 0.1
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the gyroblip class
class Gyroblip:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angle = 0
        self.speed = 0
        self.angular_velocity = 0
        self.energy = 500

        # Create a neural network
        self.neural_network = NeuralNetwork()

    def update(self):
        # Get sensor readings
        sensor_readings = self.get_sensor_readings()

        # Make a decision using the neural network
        action = self.neural_network.predict(sensor_readings)

        # Update the gyroblip's state based on the action and update energy accordingly
        if action == "turn left":
            if self.speed > 0:
                self.angular_velocity -= 0.1
            #self.energy -= 0.1
        elif action == "turn right":
            if self.speed > 0:
                self.angular_velocity += 0.1
            #self.energy -= 0.1
        elif action == "move forward":
            self.speed += 1
            self.energy -= 5
        elif action == "do nothing":
            pass

        # Check if the gyroblip has run out of energy
        if self.energy <= 0:
            print("Gyroblip has run out of energy!")

        # Update the gyroblip's position
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Update the gyroblip's angle
        self.angle += self.angular_velocity

        # Keep the gyroblip within the screen boundaries
        if self.x < 0:
            self.x = 0
            self.angular_velocity *= -1
        elif self.x > width:
            self.x = width
            self.angular_velocity *= -1
        if self.y < 0:
            self.y = 0
            self.angular_velocity *= -1
        elif self.y > height:
            self.y = height
            self.angular_velocity *= -1

    def get_sensor_readings(self):
        # Get sensor readings from the environment
        self.sensor_readings = [
            # Distance to the left wall
            self.x,
            # Distance to the right wall
            width - self.x,
            # Distance to the top wall
            self.y,
            # Distance to the bottom wall
            height - self.y,
        ]
        return self.sensor_readings

    def draw(self, screen):
        # Draw the gyroblip's body
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Display remaining energy above the gyroblip
        font = pygame.font.Font(None, 20)
        energy_text = font.render(f"Remaining Energy: {self.energy}", True, WHITE)
        screen.blit(energy_text, (self.x - self.radius, self.y - self.radius - 30))

        # Display sensor readings in a corner of the screen
        sensor_readings_text = font.render(str(self.sensor_readings), True, WHITE)
        screen.blit(sensor_readings_text, (10, 10))

# Define the neural network class
class NeuralNetwork:
    def __init__(self):
        # Initialize weights and biases using random values
        self.weights = np.random.rand(4, 4)
        self.biases = np.random.rand(4, 1)

    def predict(self, sensor_readings):
        # Convert sensor readings to input matrix
        sensor_readings = np.array(sensor_readings).reshape(1, 4)

        # Calculate net input of the hidden layer
        net_input_hidden = np.dot(sensor_readings, self.weights) + self.biases

        # Apply sigmoid activation function to hidden layer
        hidden_layer_output = np.where(net_input_hidden > 0, 1 / (1 + np.exp(-net_input_hidden)), 0)

        # Calculate net input of the output layer
        net_input_output = np.dot(hidden_layer_output, self.weights.T) + self.biases

        # Apply softmax function to output layer net input
        output_probabilities = np.exp(net_input_output) / np.sum(np.exp(net_input_output))

        # Choose action with highest probability
        action = np.argmax(output_probabilities)

        # Convert action index to action label
        action_labels = ["turn left", "turn right", "move forward", "do nothing"]
        action %= len(action_labels)
        action_label = action_labels[action]
        print(action_label)
        return action_label
# Define constants


# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gyroblip Simulation")

# Create a gyroblip
gyroblip = Gyroblip(400, 300, 20, RED)

# Main loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the gyroblip
    gyroblip.update()

    # Fill the background with black
    screen.fill(BLACK)

    # Draw the gyroblip
    gyroblip.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
