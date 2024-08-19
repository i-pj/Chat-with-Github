# Snake Game

This project is a simple implementation of the classic Snake game using Python and Pygame.

## Features

- The snake grows in length every time it eats food.
- The speed of the snake increases every time it eats food.
- The game ends when the snake collides with itself.

## Code Explanation

The main game loop is in the `gameLoop` function. Here's a brief overview of what the code does:

- The snake's position is stored in the `snake_List` list, with the head of the snake being the last element.
- If the length of `snake_List` is greater than `Length_of_snake`, the first element (the tail) is removed.
- If the head of the snake collides with any part of its body, the game ends.
- The `our_snake` function is called to draw the snake on the screen.
- The `score` function is called to display the current score.
- The screen is updated with `pygame.display.update()`.
- If the snake's head is at the same position as the food, new food is generated at a random position, the length of the snake is increased by 1, and the speed of the snake is increased.
- The game speed is controlled by the `clock.tick(snake_speed)` line.

## How to Run

To run the game, you need to have Python and Pygame installed. Once they are installed, you can run the game with the following command:

```bash
python main.py