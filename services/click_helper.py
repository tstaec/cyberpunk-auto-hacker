import pydirectinput

pydirectinput.PAUSE = 0.05  # pause between actions, if 0 strange things can happen
pydirectinput.FAILSAFE = False

# Cyberpunk is a special kind of trouble. Every time you switch to the game, the windows cursor is moved to the exact
# middle of the screen. Every movement in the Cyberpunk window does not move that cursor. Since we can not read the
# location of the cyberpunk cursor we need to force move it to the 0,0 location so we can use relative moves again.
def execute_clicks(matrix, targets, offset_matrix_x, offset_matrix_y):
    pydirectinput.move(-10000, -10000, relative=True)
    last_position = [0, 0]
    for target in targets:
        matrix_target = matrix[target[1]][target[0]]

        # We get the target coordinates in the space of the cut sub-image and need to calculate screen coordinates
        position_x = round(matrix_target.position[0] + offset_matrix_x)
        position_y = round(matrix_target.position[1] + offset_matrix_y)

        # Calculate the difference to the last position since we can't use absolute coordinates
        relative_x = position_x - last_position[0]
        relative_y = position_y - last_position[1]
        pydirectinput.moveRel(relative_x, relative_y, relative=True)
        pydirectinput.click()
        last_position = [position_x, position_y]

